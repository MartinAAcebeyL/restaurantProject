from . import *
from ..Models.Pension import Pension
from ..Shemas.Pension import paramsPensionShema
api = Blueprint('api_pension', __name__)

"""
tareas: 
    crear
    verificar consumido
    dias que faltan

"""
# monto, universitario, almuerzo_completo, activo


@api.route("/", methods=["POST"])
def create():
    data = request.get_json()
    data_is_valid = paramsPensionShema.validate(data)
    if data_is_valid:#si la data no es valida entra
        return bad_request(message=data_is_valid)
    pension = Pension.create(**data)
    if pension.save():
        return response(data=data,message="Pension creada")
    return bad_request(message="Datos incorrectos")


@api.route("/<int:id>", methods=["GET"])
def vericar_consumo(id):
    pension = Pension.query.filter_by(id=id).first()
    print(pension.to_representation())

    if not pension.activo:
        return bad_request(message=f"este pension no esta activa")
    return prueba()