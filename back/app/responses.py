from flask import jsonify

def response(data:dict, message):
    return jsonify(
        {
            'succses':True,
            'message':message,
            'data':data
        }
    ),200

def not_found(message):
    return jsonify(
        {
            'succses':False,
            'data':{},
            'message': message,
            'code':404
        }
    ),404

def bad_request(message):
    return jsonify(
        {
            'succses':False,
            'data':{},
            'message': message,
            'code':400
        }
    ),400