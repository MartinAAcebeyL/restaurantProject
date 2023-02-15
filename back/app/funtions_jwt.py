from flask import jsonify
from jwt import encode, decode
from jwt.exceptions import DecodeError, ExpiredSignatureError
from jwt.api_jwt import decode_complete
from decouple import config
from datetime import datetime, timedelta
from .responses import token_error, token_time_out


def time_token(time_dict: dict):
    time = datetime.now()
    if not time_dict:
        return time + timedelta(days=30)
    final_time = time + timedelta(days=time_dict.get('days', 0),
                                  hours=time_dict.get('hours', 0),
                                  minutes=time_dict.get('minutes', 0),
                                  seconds=time_dict.get('seconds', 0)
                                  )

    return final_time.timestamp()


def write_token(data: dict, heads: dict = {}, time: dict = {}):
    time = time_token(time)

    token = encode(payload={**data, "exp": time},
                   key=config('SECRET_KEY'),
                   algorithm="HS256",
                   headers={**heads})

    return jsonify({
        "token": token
    })


def check_token(token):
    try:
        data = decode_complete(token, config(
            'SECRET_KEY'),
            algorithms=['HS256'])
        del data['signature']
        return data
    except DecodeError:
        return token_error()
    except ExpiredSignatureError:
        return token_time_out()
