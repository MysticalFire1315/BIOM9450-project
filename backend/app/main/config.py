import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    DEBUG = False
    # Swagger
    RESTX_MASK_SWAGGER = False


config_by_name = dict(dev=Config, test=Config, prod=Config)

key = Config.SECRET_KEY
