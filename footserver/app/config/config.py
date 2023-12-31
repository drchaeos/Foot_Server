from dataclasses import dataclass
from os import path, environ

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


@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True
    DB_URL: str = "mysql+pymysql://admin:Foot123!!@foot.cdsgdwyfywvv.ap-northeast-2.rds.amazonaws.com/foot"


@dataclass
class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DB_URL: str = "mysql+pymysql://admin:Foot123!!@foot.cdsgdwyfywvv.ap-northeast-2.rds.amazonaws.com/foot"


@dataclass
class TestConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True
    DEBUG: bool = False
    DB_URL: str = "mysql+pymysql://admin:Foot123!!@foot.cdsgdwyfywvv.ap-northeast-2.rds.amazonaws.com/foot"


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("API_ENV", "local")]()
