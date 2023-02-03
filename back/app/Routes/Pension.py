from . import *
from app.Models.Pension import Pension
from app.Shemas.Pension import paramsPensionShema
api = Blueprint('api_pension', __name__)


def exist_pension(func):
    def wrapper(*args, **kwargs):
        pension = Pension.query.filter_by(id=kwargs['id']).first()
        print(pension)
        if pension is None:
            return not_found(f"no existe la pension con id:{kwargs['id']}")
        return func(pension)
    wrapper.__name__ = func.__name__
    return wrapper


@api.route("/", methods=["POST"])
@swag_from("./documentation/Pension/Create.yaml")
def create():
    data = request.get_json()
    data_is_valid = paramsPensionShema.validate(data)
    if data_is_valid:  # si la data no es valida entra
        return bad_request(message=data_is_valid)
    pension = Pension.create(**data)
    if pension.save():
        data['id'] = pension.id
        data['tipo'] = pension.tipo
        return response(
            data=data,
            message="Pension creada")
    return bad_request(message="Datos incorrectos")


@api.route("/<int:id>", methods=["GET"])
@swag_from("./documentation/Pension/Verificar-Consumo.yaml")
@exist_pension
def vericar_consumo(pension):
    if not pension.activo:
        return bad_request(message=f"este pension no esta activa")
    return response({"dias_restantes": pension.dias_restantes()}, message="")


@api.route("/<int:id>", methods=["PATCH"])
@swag_from("./documentation/Pension/Aumentar-Consumo.yaml")
@exist_pension
def aumentar_consumo(pension):
    if not (pension.activo and pension.verificar_dias_restantes):
        return bad_request(message="Ya no tiene almuerzo disnibles")

    pension.aumentar_consumo()
    return response({"consumido": pension.cantidad_consumida},
                    message="Se agrego correctamente")
