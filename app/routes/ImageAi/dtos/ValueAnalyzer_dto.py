from pydantic import BaseModel
import json
from typing import Optional
class ValueAnalyzerCreate(BaseModel):
    user_idx: Optional[int] = None
    pet_name: str = '릴리'
    morph: str = '릴리 화이트'
    gender: str = '암컷'
    head_score: int = 60
    dorsal_score: int = 80
    tail_score: int = 100
    left_score: int = 80
    right_score: int = 80
    total_score: int = 80
    left_info: str = '{"score": 50, "SecondPercent": 10.444589272052365, "ThirdPercent": 0.0, "RGB": [[79, 47, 0], [151, 129, 80]]}'
    right_info: str = '{"score": 50, "SecondPercent": 10.444589272052365, "ThirdPercent": 0.0, "RGB": [[79, 47, 0], [151, 129, 80]]}'
    top_img: str = '1'
    left_img: str = '1'
    right_img: str = '1'

    @staticmethod
    def updateFrom(
            user_idx: int,
            pet_name: str,
            morph: str,
            gender: str,
            head_score: int,
            dorsal_score: int,
            tail_score: int,
            left_score: int,
            right_score: int,
            total_score: int,
            left_info: dict,
            right_info: dict,
    ):

        value_analyzer_create = ValueAnalyzerCreate(
            user_idx=user_idx,
            pet_name=pet_name,
            morph=morph,
            gender=gender,
            head_score=head_score,
            dorsal_score=dorsal_score,
            tail_score=tail_score,
            left_score=left_score,
            right_score=right_score,
            total_score=total_score,
            left_info=json.dumps(left_info),
            right_info=json.dumps(right_info),
        )
        return value_analyzer_create

class ValueAnalyze(BaseModel):
    morph: str = '릴리 화이트'
    gender: str = '암컷'

class ValueAnalyzerResult():
    idx: int
    user_idx: Optional[int] = None
    pet_name: str
    morph: str
    gender: str
    head_score: int
    dorsal_score: int
    tail_score: int
    left_score: int
    right_score: int
    total_score: int
    left_info: str
    right_info: str
    top_img: str
    left_img: str
    right_img: str

    def updateFrom(idx,ValueAnalyzerCreate):
        valueAnalyzerResult = ValueAnalyzerResult(
            idx=idx,
            user_idx=ValueAnalyzerCreate.user_idx,
            pet_name=ValueAnalyzerCreate.pet_name,
            morph=ValueAnalyzerCreate.morph,
            gender=ValueAnalyzerCreate.gender,
            head_score=ValueAnalyzerCreate.head_score,
            dorsal_score=ValueAnalyzerCreate.dorsal_score,
            tail_score=ValueAnalyzerCreate.tail_score,
            left_score=ValueAnalyzerCreate.left_score,
            right_score=ValueAnalyzerCreate.right_score,
            total_score=ValueAnalyzerCreate.total_score,
            left_info=ValueAnalyzerCreate.left_info_str,
            right_info=ValueAnalyzerCreate.right_info_str,
        )
        return valueAnalyzerResult