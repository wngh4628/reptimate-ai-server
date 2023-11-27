from typing import List,Union
from fastapi import UploadFile, File, Depends
from sqlalchemy.orm import Session
from core.analyzer_lateral.lateral import Lateral
from core.analyzer_top.topmode_test import TopMode
from core.analyzer_gender.gender import Gender
from core.analyzer_img_checker.img_checker import Img_checker
from utils.S3 import s3_uploader
# from routes.TextAi.schemas.ChattingBot_schema import ChattingBotSchema
# from routes.TextAi.dtos.ChattingBot_dto import ValueAnalyzerCreate, ValueAnalyze
from os import path
import os
import datetime
from core.database.conn import db
from fastapi import HTTPException
import shutil
import json
from utils.color_utils import find_similar_colors, rgb2lab
from utils.linebreeding_utils import morph_re_selection, score_compare_selection, make_morph_explanation, sort_feature_order

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
class text_ai_service:
    #챗봇 답변 주는 기능
    def response_chatting_bot(self, info_object):

        return 1