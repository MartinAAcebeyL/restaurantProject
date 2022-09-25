from . import db
from sqlalchemy import Enum
from datetime import datetime
from sqlalchemy.event import listen

class Pensionado(db.Model):
    __tablename__ = "pensionados"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable = False, unique = True)
    phone = db.Column(db.String(10), nullable = False, unique = True)
    email = db.Column(db.String(80), nullable = False, unique = True)
    sex = db.Column(db.Enum("M", "F", "O"), nullable=False, server_default="M")
    resgistred = db.Column(db.DateTime(), nullable=False, default= datetime.now())


# def insertar_registros(*args, **kwargs):
#     db.session.add(
#         Pensionado(name='titulo 1',email="descripcion 1", phone="descripcion 1")
#     )
    

#     db.session.commit()

# listen(Pensionado.__table__, "after_create", insertar_registros)