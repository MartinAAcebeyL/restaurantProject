from flask import request, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flasgger import swag_from

from ..responses import *
from app.funtions_jwt import check_token


def is_the_same_user(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', "0 0").split(" ")[1]
        check_token_ = check_token(token=token)

        if type(check_token_) == tuple and check_token_[1] == 400:
            return not_found(message=check_token_[0].get_json().get('message'))

        header_user = check_token(
            token=token).get('header').get('user')

        if header_user.get('id') != args[0].id:
            return bad_request(message="No es el mismo usuario")

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
