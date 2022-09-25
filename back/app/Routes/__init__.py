from sys import prefix
from flask import Blueprint

api = Blueprint('api', __name__, url_prefix="/pension")