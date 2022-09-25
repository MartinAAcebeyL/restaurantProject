from . import db
from . import fake
from . import phone_number

from sqlalchemy import Enum
from datetime import datetime
from sqlalchemy.event import listen
import random
class Pensionado(db.Model):
    __tablename__ = "pensionados"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False, unique = True)
    phone = db.Column(db.String(40), nullable = False, unique = True)
    email = db.Column(db.String(80), nullable = False, unique = True)
    sex = db.Column(db.Enum("M", "F", "O"), nullable=False, server_default="M")
    resgistred = db.Column(db.DateTime(), nullable=False, default= datetime.now())

    @classmethod
    def create(cls, name, phone, email, sex):
        return Pensionado(name=name, phone=phone, email=email, sex=sex)
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

def insertar_registros(*args, **kwargs):
    for i in range(5):
        name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        sex = random.choice(['M', 'F'])
        print(name, phone, email, sex)
        pensionado = Pensionado.create(name=name, phone=phone, email=email, sex=sex)
        if not pensionado.save():
            print(f'{i} error, no se introdujo a ls BD')


listen(Pensionado.__table__, "after_create", insertar_registros)