from flask import Flask
from flask_migrate import Migrate

from .Models import db
from .Models.Pensionado import Pensionado

from .Routes.Pensionado import api

app = Flask(__name__)
db.init_app(app)

migrate = Migrate(app, db)

def create_app(config):

    app.config.from_object(config)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()


    return app