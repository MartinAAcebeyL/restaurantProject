from crypt import methods
from . import api

@api.route("/pensionados", methods=["GET"])
def get_pensionados():
    pass