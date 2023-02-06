from decouple import config

class Config:
    SECRET_key = config('SECRET_KEY')

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config("URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Test(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config("URI_TEST")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    TESTING = True
    TEST = True


config = {
    "development": Development,
    "test": Test
}