from typing import List,Union
from fastapi import UploadFile, File, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from utils.S3 import s3_uploader
from routes.TextAi.schemas.ChattingBot_schema import ChattingBotSchema
# from routes.TextAi.dtos.ChattingBot_dto import ValueAnalyzerCreate, ValueAnalyze
from os import path
import os
import datetime
from core.database.conn import db
from fastapi import HTTPException
import shutil
import json

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
import fasttext

class text_ai_service:
    #챗봇 답변 주는 기능
    async def response_chatting_bot(self, request_data):
        model = fasttext.load_model(base_dir + "/core/chatting_bot_model/model_cooking_reptile.bin")

        predict = model.predict(request_data.request_text)
        return predict

    #db에 있는 문서를 가져와서 보여주는 기능
    async def get_chatting_document(self, predict_result, session: Session = Depends(db.session)):

        # 예측 결과로 분류 값 추출
        classification = predict_result[0][0].split("__label__")
        # 분류 카테고리로 db의 데이터 가져옴
        document = await self.get_one_chetting_condition(classification[1], session)
        result_json = {
            "classification": document[0].categorey,
            "probability_predicted": predict_result[1][0], # 예측 확률
            "document": document[0].document,
        }
        return result_json

    async def get_one_chetting_condition(
            #모프 종류, 추천 모프 데이터 가져오기
            self,
            classification,
            session: Session = Depends(db.session)):

        chattingBotSchema_datas = session.query(ChattingBotSchema).filter(ChattingBotSchema.categorey == str(text(classification))).all()
        return chattingBotSchema_datas