from . import db
from . import fake
from . import phone_number

from sqlalchemy import Enum
from datetime import datetime
from sqlalchemy.event import listen
from sqlalchemy import asc, desc
import random
class Pensionado(db.Model, ):
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

    @classmethod
    def get_by_page(cls, order, curret_page, per_page = 10):
        sort = desc(Pensionado.id) if order=="desc" else asc(Pensionado.id)
        tasks = Pensionado.query.order_by(sort).paginate(curret_page, per_page)
        return tasks.items
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def unsave(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

def insertar_registros(*args, **kwargs):
    for i in range(58):
        name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        sex = random.choice(['M', 'F'])
        pensionado = Pensionado.create(name=name, phone=phone, email=email, sex=sex)
        if not pensionado.save():
            print(f'{i} error, no se introdujo a ls BD')


listen(Pensionado.__table__, "after_create", insertar_registros)