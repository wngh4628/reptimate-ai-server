from dataclasses import dataclass
from os import path, environ
from dotenv import dotenv_values
base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

@dataclass
class Config:
    """
    기본 Configuration
    """
    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DEBUG: bool = False
    TEST_MODE: bool = False
    print('base_dir: ', base_dir)
    USER = dotenv_values(base_dir + '/app/.env').get("USER")
    PWD = dotenv_values(base_dir + '/app/.env').get("PWD")
    HOST = dotenv_values(base_dir + '/app/.env').get("HOST")
    PORT = dotenv_values(base_dir + '/app/.env').get("PORT")
    DATABASE_NAME = dotenv_values(base_dir + '/app/.env').get("DATABASE_NAME")
    DB_URL: str = f'mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DATABASE_NAME}?charset=utf8mb4'

    print('DB_URL: ', DB_URL)

@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig(Config):
    DB_URL: str = "mariadb.cnx6ygbfwdvi.ap-northeast-2.rds.amazonaws.com"
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("API_ENV", "local")]()


