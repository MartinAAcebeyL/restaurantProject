import  sqlalchemy

class Config:
    SECRET_KEY = "123456"

class Development_config(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/resto_acby"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    "development": Development_config,
    "default": Development_config
}