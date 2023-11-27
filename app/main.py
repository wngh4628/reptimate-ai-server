from dataclasses import asdict
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from core.common.config import conf
from core.database.conn import db
from routes.ImageAi import controller_image
from routes.TextAi import controller_text
from core.middlewares.token_validator import access_control
from core.middlewares.trusted_hosts import TrustedHostMiddleware

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


def create_app():
    """
    앱 함수 실행
    :return:
    """
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    # 데이터 베이스 이니셜라이즈

    # 레디스 이니셜라이즈

    # 미들웨어 정의
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=["/health"])


    if conf().DEBUG:
        app.include_router(controller_image.router, tags=["이미지 처리 AI"], dependencies=[Depends(API_KEY_HEADER)])
    else:
        app.include_router(controller_image.router, tags=["이미지 처리 AI"])

    if conf().DEBUG:
        app.include_router(controller_text.router, tags=["자연어 처리 AI"], dependencies=[Depends(API_KEY_HEADER)])
    else:
        app.include_router(controller_text.router, tags=["자연어 처리 AI"])



    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
