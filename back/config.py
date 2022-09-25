from decouple import config

class Config:
    pass

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"{config('DB')}://{config('USER')}:{config('PASSWORD')}@+config('DB')"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Test(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/resto_acby"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    "development": Development,
    "test": Test
}