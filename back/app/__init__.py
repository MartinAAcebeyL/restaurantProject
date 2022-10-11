from re import A
from flask import Flask
from flask_migrate import Migrate

from .Models import db
from .Models.Usuario import Usuario
from .Models.Pension import Pension

from .Routes.Usuario import api



def create_app(config):
    app = Flask(__name__)

    # migrate = Migrate()
    app.config.from_object(config)
    app.register_blueprint(api)

    with app.app_context():
        db.init_app(app)
        # migrate.init_app(app, db)
        db.create_all()

    return app