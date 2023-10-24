from typing import List,Union
from fastapi import UploadFile, File, Depends
from sqlalchemy.orm import Session
from core.analyzer_lateral.lateral import Lateral
from core.analyzer_top.topmode_test import TopMode
from core.analyzer_gender.gender import Gender
from core.analyzer_img_checker.img_checker import Img_checker
from utils.S3 import s3_uploader
from routes.ValueAnalyzer.schemas.ValueAnalyer_schema import ValueAnalyzerSchema
from routes.ValueAnalyzer.dtos.ValueAnalyzer_dto import ValueAnalyzerCreate, ValueAnalyze
from os import path
import os
import datetime
from core.database.conn import db
from fastapi import HTTPException
import shutil

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
class ai_service:
    async def assess_value(self, data: ValueAnalyze, files: List[UploadFile]):
        topAnalyzer = TopMode(base_dir + '/core/analyzer_top/datasets/train/weights/best.pt')
        lateralAnalyzer = Lateral(base_dir + '/core/analyzer_lateral/datasets/train/weights/best.pt')
        img_checker = Img_checker(base_dir + '/core/analyzer_img_checker/datasets/train/weights/best.pt')
        save_dir = base_dir + '/core/analyzer_lateral/datasets/test/images'
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = ''
        topImgPath = ''
        leftLateralImgPath = ''
        righLateraltImgPath = ''
        # 이미지를 순회하면서 각각 원본 이름으로 저장
        for idx, file in enumerate(files):
            # 현재 시간을 포함한 파일 이름 생성
            file_name_without_extension = f"{current_time}_{file.filename.rsplit('.', 1)[0]}"
            if idx == 0:  # 탑 이미지
                file_name = os.path.join(save_dir, f"{file_name_without_extension}_topImgPath.jpeg")
                topImgPath = file_name
            elif idx == 1:  # 왼쪽 레터럴 이미지
                file_name = os.path.join(save_dir, f"{file_name_without_extension}_leftLateralImgPath.jpeg")
                leftLateralImgPath = file_name
            elif idx == 2:  # 오른쪽 레터럴 이미지
                file_name = os.path.join(save_dir, f"{file_name_without_extension}_righLateraltImgPath.jpeg")
                righLateraltImgPath = file_name
            # 파일을 지정된 디렉토리에 저장
            file_path = os.path.join(save_dir, file_name)
            with open(file_path, "wb") as f:
                f.write(file.file.read())

        # 이미지가 크레스티드 게코인지 확인 - 현재는 gecko 클래스 탐지하면 통과하함
        img_checker.img_checking(topImgPath)
        img_checker.img_checking(leftLateralImgPath)
        img_checker.img_checking(righLateraltImgPath)

        # 머리, 등, 꼬리 검사
        try:
            topResult = topAnalyzer.analyze_image(topImgPath, current_time + "_top_")
        except Exception as e:
            # 예외 처리
            error_message = 'Top Part Error'
            return {"error": error_message}
        # 왼쪽 레터럴 검사
        try:
            leftResult = lateralAnalyzer.analyze_image(leftLateralImgPath, current_time + "_left_")
        except Exception as e:
            # 예외 처리
            error_message = str(e)
            return {"error": error_message}
        # 오른쪽 레터럴 검사
        try:
            rightResult = lateralAnalyzer.analyze_image(righLateraltImgPath, current_time + "_right_")
        except Exception as e:
            # 예외 처리
            error_message = str(e)
            return {"error": error_message}

        total_score = (leftResult.get('score') + rightResult.get('score') + topResult.get("haed_score") + topResult.get(
            "tail_score") + topResult.get("dorsal_score")) / 5

        # 결과 저장
        result = ValueAnalyzerCreate.updateFrom(None, 'auto_save', data.moff, data.gender, topResult.get("haed_score"),
                                            topResult.get("dorsal_score"), topResult.get("tail_score"),
                                            leftResult.get('score'),rightResult.get('score'),
                                            total_score, leftResult, rightResult)
        return result

    async def analyzer_auto_save(
            self,
            result: ValueAnalyzerCreate,
            files: List[UploadFile] = File(...),
            session: Session = Depends(db.session)):

        # s3_uploader를 사용하여 이미지 업로드
        for idx, file in enumerate(files):
            uploaded_image = s3_uploader.upload_image(file, 'ValueAnalyzer')
            image_url = uploaded_image['message'].split('URL: ')[1]
            # idx에 따라 필드 설정
            if idx == 0:
                result.top_img = image_url
            elif idx == 1:
                result.left_img = image_url
            elif idx == 2:
                result.right_img = image_url

        value_analyzer = ValueAnalyzerSchema(**result.dict())  # ValueAnalyzerCreate 모델의 데이터를 ValueAnalyzer 모델로 변환
        session.add(value_analyzer)
        session.commit()
        session.refresh(value_analyzer)
        return '저장 완료'

    async def analyzer_save(
            self,
            idx: int,
            userIdx: int,
            petName: str,
            session: Session = Depends(db.session)):

        value_analyzer = session.query(ValueAnalyzerSchema).filter(ValueAnalyzerSchema.idx == idx).first()

        # 해당하는 idx의 행이 없으면 예외 처리
        if not value_analyzer:
            raise HTTPException(status_code=404, detail="Value Analyzer not found")

        # userIdx와 petName 업데이트
        value_analyzer.user_idx = userIdx
        value_analyzer.pet_name = petName

        # 변경사항 커밋
        session.commit()

    async def gender_discrimination(
            self,
            file: UploadFile):
        # 훈련 데이터 파일 경로를 넣어주며 클래스 생성
        genderAnalyzer = Gender(base_dir + '/core/analyzer_gender/datasets/train/weights/best.pt')
        # 받은 이미지 저장할 경로 설정
        save_dir = base_dir + '/core/analyzer_gender/datasets/test/images'
        # 저장할 이미지 이름에 현제 날짜와 시간을 넣어 주기 위한 날짜 & 시간
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # 이름 합치기 & 가공
        file_full_name = f"{current_time}_{file.filename.rsplit('.', 1)[0]}"
        # 최종 파일 이름
        file_name = os.path.join(save_dir, f"{file_full_name}_genderImgPath.jpeg")
        # 세그멘테이션 결과 이미지 경로
        result_path = f"{save_dir}/{file_full_name}/{file_full_name}_genderImgPath.jpeg"
        # 이미지 저장
        with open(file_name, "wb") as f:
            await file.seek(0)
            # 파일을 먼저 읽은 다음에 저장
            contents = await file.read()
            f.write(contents)
        # 본격적으로 성별 구분 기능 실행. 저장된 이미지 경로와 결과물 저장할 이름 만들 떄 필요한 값들 넣어줌
        genderResult = genderAnalyzer.analyze_image(file_name, save_dir, file_full_name)

        # # 세그멘테이션 결과 이미지 file로 객체화
        with open(result_path, "rb") as sagFile:
            resultFile = sagFile.read()
        # 다쓴 이미지는 삭제, 영구 저장할 이미지는 S3에 저장함
        returnImg = s3_uploader.upload_local_image(resultFile, 'gender_discrimination', f"{file_full_name}_gender_result.jpeg")
        # 세그멘테이션 결과물 디렉토리 삭제
        dir_path = f"{save_dir}/{file_full_name}"
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print(f"Error: {e.strerror}")

        # 원본 이미지 삭제
        os.remove(file_name)
        result = {"result": genderResult, "returnImg": returnImg['message'].split('URL: ')[1]}
        return result
