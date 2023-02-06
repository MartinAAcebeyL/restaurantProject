from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger

from .Models import db
from .Models.Pension import Pension
from .Models.Usuario import Usuario
from .Models.Registro import Registro

from .Routes.Usuario import api as api_usuarios
from .Routes.Pension import api as api_pension



def create_app(config):
    app = Flask(__name__)

    migrate = Migrate()
    swagger = Swagger()
    app.config.from_object(config)
    
    app.app_context().push()

    app.register_blueprint(api_usuarios, url_prefix="/usuarios")
    app.register_blueprint(api_pension,  url_prefix="/usuario/pension")

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        db.create_all()
    swagger.init_app(app)
    return app