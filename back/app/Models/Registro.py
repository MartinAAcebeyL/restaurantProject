from . import *


class Registro(db.Model):
    __tablename__ = "registros"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime(), nullable=False)
    sopa = db.Column(db.String(50), nullable=False)
    segundo = db.Column(db.String(50), nullable=False)
    observaciones = db.Column(db.Integer, nullable=True)

    # relaciones
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    @classmethod
    def create(cls, fecha, sopa, segundo, observaciones):
        return Registro(fecha=fecha, sopa=sopa, segundo=segundo,
                        observaciones=observaciones)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def unsave(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False
