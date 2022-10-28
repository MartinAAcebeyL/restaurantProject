from . import *


class Pension(db.Model):
    __tablename__ = "pensiones"

    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Integer, nullable=False, default=350)
    universitario = db.Column(db.Boolean(), nullable=False)
    #0 => no universitario // 1 => universitario
    almuerzo_completo = db.Column(db.Boolean(), nullable=False, default=True)
    #0 => solo segundos || 1=> completo
    activo = db.Column(db.Boolean(), nullable=False, default=True)
    observaciones = db.Column(db.Text, nullable=True)
    cantidad_consumida = db.Column(db.Integer, nullable=True, default=0)
    resgistred_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.now())

    @classmethod
    def create(cls, monto, universitario, almuerzo_completo, activo):
        return Pension(monto=monto, universitario=universitario, 
                       almuerzo_completo=almuerzo_completo, activo=activo)

    def verificar_comsumido(self, dias_pensionados):
        if self.cantidad_consumida >= dias_pensionados:
            self.activo=False
        self.cantidad_consumida+=1


    def dias_restante(self):
        self.monto in [350, 300] if self.verificar_comsumido(30) else self.verificar_comsumido(15)

        if not self.activo:
            return "debe renobar pension"

        if self.tiempo == "M":
            return 30 - self.cantidad_consumida
        return 15 - self.cantidad_consumida


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

    def __str__(self) -> str:
        return f"Pension {self.monto} id: {self.id}"

    def to_representation(self):
        return {
            "id":self.id,
            "monto": self.monto,
            "universitario": self.universitario,
            "almuerzo_completo": self.almuerzo_completo,
            "activo": self.activo,
            "observaciones": self.observaciones,
            "cantidad_consumida": self.cantidad_consumida,
            "resgistred_at": self.resgistred_at
        }

# monto, universitario, almuerzo_completo, activo
def registrar_pension():
    monto = random.choice([350, 175, 300, 150])
    universitario = fake.boolean(chance_of_getting_true=25)
    almuerzo_completo = fake.boolean(chance_of_getting_true=80)
    activo = fake.boolean(chance_of_getting_true=70)

    pension = Pension.create(monto=monto, universitario=universitario,
        almuerzo_completo=almuerzo_completo, activo=activo)
    pension.save()
    return pension.id