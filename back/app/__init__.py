from flask import Flask

from .Models import db
from .Routes import db


app = Flask(__name__)


def create_app(config):
    app.config.from_object(config)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app