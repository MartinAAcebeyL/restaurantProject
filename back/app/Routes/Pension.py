from . import *
from ..Models.Pension import Pension

api = Blueprint('api_pension', __name__)

"""
tareas: 
    crear
    verificar consumido
    dias que faltan

"""
# monto, universitario, almuerzo_completo, activo
@api.route("/", methods = ["POST"])
def create():
   response = request.get_json()
   
   print(response)
   return prueba()

