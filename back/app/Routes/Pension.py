from crypt import methods
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

#para crear una nueva pension
@api.route("/", methods=["POST"])
def create():
    data = request.get_json()
    data_is_valid = paramsPensionShema.validate(data)
    if data_is_valid:#si la data no es valida entra
        return bad_request(message=data_is_valid)
    pension = Pension.create(**data)
    if pension.save():
        data['id']=pension.id
        data['tipo'] = pension.tipo
        return response(
            data=data,
            message="Pension creada")
    return bad_request(message="Datos incorrectos")

"""
monto = db.Column(db.Integer, nullable=False, default=350)
universitario = db.Column(db.Boolean(), nullable=False)
#0 => no universitario // 1 => universitario
almuerzo_completo = db.Column(db.Boolean(), nullable=False, default=True)
#0 => solo segundos || 1=> completo
activo = db.Column(db.Boolean(), nullable=False, default=True)
observaciones = db.Column(db.Text, nullable=True)
cantidad_consumida = db.Column(db.Integer, nullable=True, default=0)
"""
def exist_pension(func):
    def wrapper(*args, **kwargs):
        pension = Pension.query.filter_by(id=kwargs['id']).first()
        print(pension)
        if pension is None:
            return not_found("no existe la pension")
        return func(pension)
    wrapper.__name__ = func.__name__
    return wrapper

@api.route("/<int:id>", methods=["OTHER"])
@exist_pension
def vericar_consumo(pension):
    print(pension.to_representation())

    if not pension.activo:
        return bad_request(message=f"este pension no esta activa")
    return prueba()

@api.route("/<int:id>", methods=["POST"])
@exist_pension
def aumentar_consumo(pension):
    pension