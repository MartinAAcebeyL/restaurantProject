from . import *


class Pension(db.Model):
    __tablename__ = "pensiones"

    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Integer)
    tiempo = db.Column(db.Enum("M", "L"), nullable=False, server_default="M")
    tipo = db.Column(db.Boolean(), nullable=False)
    observaciones = db.Column(db.Integer, nullable=True)
    cantidad_faltante = db.Column(db.Integer, nullable=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    resgistred = db.Column(db.DateTime(), nullable=False,
                           default=datetime.now())

    @classmethod
    def create(cls, monto, tiempo, tipo, observaciones):
        
        return Pension(monto=monto, tiempo=tiempo, tipo=tipo,
                       observaciones=observaciones)

    @classmethod
    def get_by_page(cls, order, curret_page, per_page=10):
        sort = desc(Pension.id) if order == "desc" else asc(Pension.id)
        tasks = Pension.query.order_by(sort).paginate(curret_page, per_page)
        return tasks.items

    @classmethod
    def exist(cls, phone, email, show=False):
        pensiondos = cls.query.filter(
            or_(cls.phone == phone, cls.email == email))
        if show:
            print(pensiondos.all())
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
    usuario = Pension.create(
        name="Martin Acebey L", phone="+59173883448",
        sex="M", email="martinaal2000@gmail.com",
        password="administrador", administrador=True)

    if not usuario.save():
        print('error, ADMIN no se introdujo a ls BD')

    # default_password = '123456789'
    # for i in range(49):
    #     name = fake.name()
    #     phone = fake.phone_number()
    #     sex = random.choice(['M', 'F'])
    #     email = fake.email()
    #     password = default_password

    #     usuario = Pension.create(
    #         name=name, phone=phone, sex=sex, email=email,
    #         password=password)

    #     if not usuario.save():
    #         print(f'{i} error, no se introdujo a ls BD')


# listen(Pension.__table__, "after_create", insertar_registros)
