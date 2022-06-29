import os
from typing import List, Type

CONNECTION_API_BASE_URL = os.environ["CONNECTION_API_BASE_URL"]
LOCATION_API_BASE_URL = os.environ["LOCATION_API_BASE_URL"]
PERSON_API_HOST = os.environ["PERSON_API_HOST"]


class BaseConfig:
    CONFIG_NAME = "base"
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "dev"
    SECRET_KEY = os.getenv(
        "DEV_SECRET_KEY", "You can't see California without Marlon Widgeto's eyes"
    )
    DEBUG = True
    CONNECTION_API_BASE_URL = f"{CONNECTION_API_BASE_URL}"
    LOCATION_API_BASE_URL = f"{LOCATION_API_BASE_URL}"
    PERSON_API_HOST = f"{PERSON_API_HOST}"
    TESTING = False
class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "Thanos did nothing wrong")
    DEBUG = True
    CONNECTION_API_BASE_URL = f"{CONNECTION_API_BASE_URL}"
    LOCATION_API_BASE_URL = f"{LOCATION_API_BASE_URL}"
    PERSON_API_HOST = f"{PERSON_API_HOST}"
    TESTING = True

class ProductionConfig(BaseConfig):
    CONFIG_NAME = "prod"
    SECRET_KEY = os.getenv("PROD_SECRET_KEY", "I'm Ron Burgundy?")
    DEBUG = False
    CONNECTION_API_BASE_URL = f"{CONNECTION_API_BASE_URL}"
    LOCATION_API_BASE_URL = f"{LOCATION_API_BASE_URL}"
    PERSON_API_HOST = f"{PERSON_API_HOST}"
    TESTING = False

EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
