import datetime
from typing import List
from analyzer_gender.gender import Gender
from fastapi import Depends, UploadFile, APIRouter, File
from os import path
from sqlalchemy.orm import Session
from routes.ValueAnalyzer.dtos.ValueAnalyzer_dto import ValueAnalyzerCreate,ValueAnalyze
from database.conn import db
from routes.ValueAnalyzer.service import ai_service


base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
router = APIRouter(prefix='/ai')

@router.post("/ValueAnalyzer", summary="도마뱀 가치 판단 기능", description="*files의 첫 번째에는 Top 이미지 두번쨰에는 left 마지막은 right")
async def assessValue(data: ValueAnalyze = Depends(), files: List[UploadFile] = File(...),
        ai_service: ai_service = Depends(ai_service),
        session: Session = Depends(db.session)):

    # 가치 판단 기능 실행
    result = await ai_service.assess_value(data, files)  # assess_value 메서드 호출
    # 결과 데이터 및 이미지 s3 저장
    await ai_service.analyzer_auto_save(result, files, session)

    return result

@router.post("/analyzer_save", summary="결과 저장하는 기능", description="*로그인 되어야 저장 가능합니다. 로그인 안됬으면 로그인 후에 해당 기능 실행해주세요!")
async def analyzer_save(
        idx: int,
        userIdx: int,
        petName: str,
        ai_service: ai_service = Depends(ai_service),
        session: Session = Depends(db.session)):

    # 로그인이 되어 있는 상태에서 가치 판단 결과 저장
    result = await ai_service.analyzer_save(idx, userIdx, petName, ai_service, session)  # assess_value 메서드 호출

    return result

@router.post("/gender_discrimination", summary="암수 구분 기능")
async def gender_discrimination(
        file: UploadFile,
        ai_service: ai_service = Depends(ai_service)):
    genderResult = ai_service.gender_discrimination(file)
    return genderResult


