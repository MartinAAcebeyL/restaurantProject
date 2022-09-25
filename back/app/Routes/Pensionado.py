from flask import jsonify
from flask import Blueprint

api = Blueprint('api', __name__, url_prefix="/restaurant/pensionados")


@api.route("/", methods=["GET"])
def get_pensionados():
    
    return jsonify({
        "hola":"como estas",
        "hola 1":"como estas 1",
        "hola 2":"como estas 2",
        "hola 3":"como estas 3"
    })