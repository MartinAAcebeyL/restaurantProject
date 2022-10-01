import json
from flask import request
from flask import Blueprint
from ..Models.Pensionado import Pensionado
from ..shemas import pensionado_shema, pensionado_shemas, paramsPensionadoShema

from ..responses import *

api = Blueprint('api', __name__, url_prefix="/restaurant/pensionados")


@api.route("/", methods=["GET"])
def get_pensionados():
    pensionados = Pensionado.query.all()
    if len(pensionados) <= 0:
        return not_found(message="No existen datos")

    order = request.args.get('order', 'asc')
    page = int(request.args.get('page', 1))

    pensionados = Pensionado.get_by_page(order=order, curret_page=page)

    return response(
                    pensionado_shemas.dump(pensionados), 
                    message=f"existe {len(pensionados)} registros"
                    )


@api.route("/<id>", methods=["GET"])
def get_pensionado(id):
    pensionado = Pensionado.query.get(id)
    if pensionado is None:
        return not_found(message=f"no se encontro al registro con el id: {id}")
    return response(pensionado_shema.dump(pensionado), "usuario encontrado")

@api.route("/", methods=["POST"])
def create_pensionado():
    response = request.get_json()

    pensionado_shema_validate = paramsPensionadoShema.validate(response)

    if pensionado_shema_validate:
        return bad_request(message=pensionado_shema_validate)

    pensionado = Pensionado.create(name=response['name'], phone=response['phone'],
                            email=response['email'], sex=response['sex'])
    print(pensionado_shema.dump(pensionado))
    if pensionado.save():
        return pensionado_shema.dump(pensionado)
    return bad_request(message="en prueba")

@api.route("/<id>", methods=["PATCH, PUT"])
def update_pensionado(id):
    pensionado = Pensionado.query.get(id)

    pensionado.email = request.json.get('email', pensionado.email)
    pensionado.name = request.json.get('name', pensionado.name)
    pensionado.phone = request.json.get('phone', pensionado.phone)
    pensionado.sex = request.json.get('sex', pensionado.sex)

    if pensionado.save():
        return pensionado_shema.dump(pensionado)
    return bad_request()

@api.route("/<id>", methods=["DELETE"])
def delete_pensionado(id):
    pensionado = Pensionado.query.get(id)
    if pensionado.unsave():
        return pensionado_shema.dump(pensionado)
    return bad_request()