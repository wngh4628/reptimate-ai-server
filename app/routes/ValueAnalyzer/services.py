import datetime
from typing import List
from analyzer_lateral.lateral import Lateral
from analyzer_top.topmode_test import TopMode
from analyzer_gender.gender import Gender
from fastapi import Depends, UploadFile, APIRouter, Header, File
from os import path
from utils.S3 import s3_uploader
from sqlalchemy.orm import Session
from routes.ValueAnalyzer.dtos.ValueAnalyzer_dto import ValueAnalyzerCreate,ValueAnalyze
from database.conn import db
from database.schema import ValueAnalyzerSchema
import jwt
from dotenv import dotenv_values


base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
router = APIRouter(prefix='/services')

@router.post("/ValueAnalyzer", summary="도마뱀 가치 판단 기능", description="*files의 첫 번째에는 Top 이미지 두번쨰에는 left 마지막은 right")
async def assessValue(data: ValueAnalyze = Depends(), files: List[UploadFile] = File(...),
        session: Session = Depends(db.session)):
    topAnalyzer = TopMode(base_dir + '/analyzer_top/datasets/train/weights/best.pt')
    lateralAnalyzer = Lateral(base_dir+'/analyzer_lateral/datasets/train/weights/best.pt')
    save_dir = base_dir+'/analyzer_lateral/datasets/test/images'
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = ''
    topImgPath = ''
    leftLateralImgPath = ''
    righLateraltImgPath = ''
    # 이미지를 순회하면서 각각 원본 이름으로 저장
    for idx, file in enumerate(files):
        # 현재 시간을 포함한 파일 이름 생성
        file_name_without_extension = f"{current_time}_{file.filename.rsplit('.', 1)[0]}"
        if idx == 0: # 탑 이미지
            file_name = os.path.join(save_dir, f"{file_name_without_extension}_topImgPath.jpeg")
            topImgPath = file_name
        elif idx == 1: # 왼쪽 레터럴 이미지
            file_name = os.path.join(save_dir, f"{file_name_without_extension}_leftLateralImgPath.jpeg")
            leftLateralImgPath = file_name
        elif idx == 2:# 오른쪽 레터럴 이미지
            file_name = os.path.join(save_dir, f"{file_name_without_extension}_righLateraltImgPath.jpeg")
            righLateraltImgPath = file_name
        # 파일을 지정된 디렉토리에 저장
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

    # 머리, 등, 꼬리 검사
    try:
        topResult = topAnalyzer.analyze_image(topImgPath, current_time+"_top_")
        print("topResult, ", topResult)
    except Exception as e:
        # 예외 처리
        error_message = 'Top Part Error'
        return {"error": error_message}
    #왼쪽 레터럴 검사
    try:
        leftResult = lateralAnalyzer.analyze_image(leftLateralImgPath,current_time+"_left_")
    except Exception as e:
        # 예외 처리
        error_message = str(e)
        return {"error": error_message}
    # 오른쪽 레터럴 검사
    try:
        rightResult = lateralAnalyzer.analyze_image(righLateraltImgPath,current_time+"_right_")
    except Exception as e:
        # 예외 처리
        error_message = str(e)
        return {"error": error_message}
    total_score = (leftResult.get('score') + rightResult.get('score') + topResult.get("haed_score") + topResult.get("tail_score") + topResult.get("dorsal_score"))/5
    result = {
        "left_lateral_Info": leftResult,
        "right_lateral_Info": rightResult,
        "haed_score": topResult.get("haed_score"),
        "tail_score": topResult.get("tail_score"),
        "dorsal_score": topResult.get("dorsal_score"),
        "left_lateral_score": leftResult.get('score'),
        "right_lateral_score": rightResult.get('score'),
        "total_score": total_score,
    }

    data = ValueAnalyzerCreate.updateFrom(65, data.pet_name, data.pet_moff, data.gender, topResult.get("haed_score"),
                                          topResult.get("dorsal_score"), topResult.get("tail_score"), leftResult.get('score'),rightResult.get('score'), total_score,leftResult, rightResult)
    print("data: ", data)
    await insert_value_analyzer(data, files, session)
    return result

# POST 요청 처리
@router.post("/file/ValueAnalyzer_result_save")
async def insert_value_analyzer(
        data: ValueAnalyzerCreate = Depends(),
        files: List[UploadFile] = File(...),
        session: Session = Depends(db.session)):
    #s3_uploader를 사용하여 이미지 업로드
    for idx, file in enumerate(files):

        uploaded_image = s3_uploader.upload_image(file, 'ValueAnalyzer')
        image_url = uploaded_image['message'].split('URL: ')[1]
        # idx에 따라 필드 설정
        if idx == 0:
            data.top_img = image_url
        elif idx == 1:
            data.left_img = image_url
        elif idx == 2:
            data.right_img = image_url
    value_analyzer = ValueAnalyzerSchema(**data.dict())  # ValueAnalyzerCreate 모델의 데이터를 ValueAnalyzer 모델로 변환
    session.add(value_analyzer)
    session.commit()
    session.refresh(value_analyzer)
    return '저장 완료'

@router.post("/file/gender_discrimination")
async def gender_discrimination(
        file: UploadFile,
        session: Session = Depends(db.session)):
    #s3_uploader를 사용하여 이미지 업로드
    genderAnalyzer = Gender(base_dir + '/analyzer_gender/datasets/train/weights/best.pt')
    save_dir = base_dir + '/analyzer_gender/datasets/test/images'
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name_without_extension = f"{current_time}_{file.filename.rsplit('.', 1)[0]}"
    file_name = os.path.join(save_dir, f"{file_name_without_extension}_genderImgPath.jpeg")
    with open(file_name, "wb") as f:
        f.write(file.file.read())
    genderResult = genderAnalyzer.analyze_image(file_name, current_time + "_gender_")
    os.remove(file_name)
    return genderResult

