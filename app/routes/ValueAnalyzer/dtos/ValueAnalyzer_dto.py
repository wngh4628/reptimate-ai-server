# Pydantic 모델 정의
from pydantic import BaseModel

class ValueAnalyzerCreate(BaseModel):
    user_idx: int = 65
    pet_name: str = '릴리'
    moff: str = '릴리 화이트'
    Gender: str = '암컷'
    head_score: int = '60'
    dorsal_score: int = '80'
    tail_score: int = '100'
    left_score: int = '80'
    right_score: int = '80'
    total_score: int = '80'
    left_info: str = {
        "score": 50,
        "SecondPercent": 10.444589272052365,
        "ThirdPercent": 0.0,
        "RGB": [
            [
                79,
                47,
                0
            ],
            [
                151,
                129,
                80
            ]
        ]
    }
    right_info: str = {
        "score": 50,
        "SecondPercent": 10.444589272052365,
        "ThirdPercent": 0.0,
        "RGB": [
            [
                79,
                47,
                0
            ],
            [
                151,
                129,
                80
            ]
        ]
    }
    top_img: str = '1'
    left_img: str = '1'
    right_img: str = '1'

class ValueAnalyze(BaseModel):
    pet_name: str = '릴리'
    moff: str = '릴리 화이트'
    Gender: str = '암컷'