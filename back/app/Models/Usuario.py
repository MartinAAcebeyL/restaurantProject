from sqlalchemy import text 
from . import *
from .Pension import Pension

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),  nullable=False)
    phone = db.Column(db.String(40), nullable=False, unique=True)
    sex = db.Column(db.Enum("M", "F", "O"), nullable=False, server_default="M")
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(90), nullable=False)
    administrador = db.Column(
        db.Boolean(), nullable=False, default=False)
    resgistred = db.Column(db.DateTime(), nullable=False,
                           default=datetime.now())

    pension_id = db.Column(db.Integer, db.ForeignKey('pensiones.id'))
    pension = db.relationship("Pension", overlaps="usuario_id")

    # registro_id = db.Column(db.Integer, db.ForeignKey('registros.id'))
    # registro = db.relationship("Registro")


    @classmethod
    def create(cls, name, phone, sex, email, password, pension_id=None, administrador=False):
        hashed_password = generate_password_hash(password=password, method='sha256')
        return Usuario(name=name, phone=phone, sex=sex, 
                       email=email, pension_id=pension_id,
                       password=hashed_password, administrador=administrador)

    @classmethod
    def get_by_page(cls, order, curret_page, per_page = 10):
        sort = desc(Usuario.id) if order == "desc" else asc(Usuario.id)
        tasks = Usuario.query.order_by(sort).paginate(curret_page, per_page)
        return tasks.items

    @classmethod
    def exist(cls, phone, email, show=False):
        pensiondos = cls.query.filter(
            or_(cls.phone == phone, cls.email == email))
        if show: print(pensiondos.all())
        return True if pensiondos.count() > 0 else False
    
    def set_password(self, password):
        self.password = generate_password_hash(
            password=password, method='sha256')

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
    usuario = Usuario.create(
        name="Martin Acebey L", phone="+59173883448", 
        sex="M", email="martinaal2000@gmail.com",
        password="administrador", administrador=True)

    if not usuario.save():
        print('error, ADMIN no se introdujo a ls BD')


    default_password = '123456789'
    for i in range(49):
        name = fake.name()
        phone = fake.phone_number()
        sex = random.choice(['M', 'F'])
        email = fake.email()
        password = default_password

        ids = [i.id for i in Pension.query.all()]
        pension_id = fake.random_element(elements=ids)
        
        usuario = Usuario.create(\
            name=name, phone=phone, sex=sex, email=email,\
            password=password,pension_id=pension_id)
        
        if not usuario.save():
            print(f'{i} error, no se introdujo a ls BD')


listen(Usuario.__table__, "after_create", insertar_registros)