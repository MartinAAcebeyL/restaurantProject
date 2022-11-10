from . import *
from ..Models.Usuario import Usuario
from ..Shemas.Usuario import (usuario_shema, usuario_shemas,
                              paramsCreateUsuarioShema, paramsUpdateUsuarioShema, loginParamsUsuarioShema)
from ..funtions_jwt import write_token, time_token, check_token

from flasgger import swag_from

api = Blueprint('api_usuarios', __name__)


def exist_pension(func):
    def wrapper(*args, **kwargs):
        usuario = Usuario.query.filter_by(id=kwargs['id']).first()
        if usuario is None:
            return not_found(f"no existe la usuario con id:{kwargs['id']}")
        return func(usuario)
    wrapper.__name__ = func.__name__
    return wrapper


@api.route("/", methods=["GET"])
@swag_from("./documentation/Usuario/Get-All.yaml")
def get_usuarios():
    usuarios = Usuario.query.all()
    if len(usuarios) <= 0:
        return not_found(message="No existen datos")

    order = request.args.get('order', 'asc')
    page = int(request.args.get('page', 1))

    usuarios = Usuario.get_by_page(order=order, curret_page=page)

    return response(
        usuario_shemas.dump(usuarios),
        message=f"existe {len(usuarios)} registros"
    )


@api.route("/<id>", methods=["GET"])
@swag_from("./documentation/Usuario/Get.yaml")
@exist_pension
def get_usuario(usuario):
    return response(usuario_shema.dump(usuario), "usuario encontrado")


@api.route("/", methods=["POST"])
@swag_from("./documentation/Usuario/Create.yaml")
def create_usuario():
    response_json = request.get_json()
    usuario_shema_validate = paramsCreateUsuarioShema.validate(response_json)

    if usuario_shema_validate:
        return bad_request(message=usuario_shema_validate)

    if Usuario.exist(response_json['phone'], response_json['email']):
        return bad_request(message="Ya existe un registro con estos datos")

    if not 'administrador' in response_json:
        response_json['administrador'] = False

    usuario = Usuario.create(name=response_json['name'], phone=response_json['phone'],
                             email=response_json['email'], sex=response_json['sex'],
                             administrador=response_json['administrador'],
                             password=response_json['password'],
                             pension_id=response_json['pension_id'])
    if usuario.save():
        return response(data=usuario_shema.dump(usuario), message="registro exitoso")

    return bad_request(message="registro erroneo")


@api.route("/<id>", methods=["PATCH", "PUT"])
@swag_from("./documentation/Usuario/Update.yaml")
@exist_pension
def update_usuario(usuario):
    response_json = request.get_json()
    usuario_shema_messages = paramsUpdateUsuarioShema.validate(response_json)
    if usuario_shema_messages:
        return bad_request(message=usuario_shema_messages)

    usuario.email = request.json.get('email', usuario.email)
    usuario.name = request.json.get('name', usuario.name)
    usuario.phone = request.json.get('phone', usuario.phone)
    usuario.sex = request.json.get('sex', usuario.sex)
    usuario.administrador = request.json.get(
        'administrador', usuario.administrador)
    usuario.password = generate_password_hash(
        password=request.json.get('password'), method='sha256')

    if usuario.save():
        return response(usuario_shema.dump(usuario), message="actualizacion exitosa")
    return bad_request(message="Algo salio mal en la DB")


@api.route("/<id>", methods=["DELETE"])
@swag_from("./documentation/Usuario/Delete.yaml")
@exist_pension
def delete_usuario(usuario):
    if usuario.unsave():
        return response(usuario_shema.dump(usuario), message="Eliminacion exitosa")
    return bad_request(message="Algo salio mal")


@api.route("/login", methods=['POST'])
@swag_from("./documentation/Usuario/Login.yaml")
def user_login():
    data = request.get_json()
    error_messages = loginParamsUsuarioShema.validate(data)

    if error_messages:
        return bad_request(message=error_messages)

    usuario = Usuario.query.filter_by(email=data.get('email')).first()

    if not usuario:
        return bad_request(message="no existe el user con estos datos")

    if check_password_hash(usuario.password, data.get('password')):
        return write_token(data=data, time={"minutes": 5}, heads={"user": "i am"})

    return bad_request(message="datos incorectos")


@api.route("/verifyToken", methods=['GET'])
@swag_from("./documentation/Usuario/Verify-token.yaml")
def verify_token():
    token = request.headers.get('Authorization').split(" ")[1]
    return check_token(token=token, show=True)