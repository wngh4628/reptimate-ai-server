from typing import List
from fastapi import Depends, UploadFile, APIRouter, File
from os import path
from sqlalchemy.orm import Session
from routes.TextAi.dtos.ChattingBot_dto import ChattingBot
from core.database.conn import db
from routes.TextAi.service import text_ai_service
from utils.FileChecker import FileChecker


base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
router = APIRouter(prefix='/text_ai')

@router.post("/chatting_bot", summary="채팅 봇", description="자연어 생성 모델을 통해 답변을 추출한다.")
async def chattingBot(data: ChattingBot = Depends(),
        text_ai_service: text_ai_service = Depends(text_ai_service),
        session: Session = Depends(db.session)):

    # 가치 판단 기능 실행
    UserResult = await text_ai_service.response_chatting_bot(data)  # assess_value 메서드 호출
    print("data")
    print(data)
    # 결과 데이터 및 이미지 s3 저장
    # await ai_service.analyzer_auto_save(UserResult, files, session)

    # print("UserResult")
    # print(UserResult)
    # print("UserResult")
    # get_analyzer_result = await text_ai_service.get_analyzer_data(UserResult, session)  # 분석

    return data
