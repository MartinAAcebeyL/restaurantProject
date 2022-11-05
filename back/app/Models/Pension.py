from . import *


class Pension(db.Model):
    __tablename__ = "pensiones"

    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Integer, nullable=False, default=350)
    # si es medio o mes completo
    tipo = db.Column(db.Boolean())
    universitario = db.Column(db.Boolean(), nullable=False)
    # 0 => no universitario // 1 => universitario
    almuerzo_completo = db.Column(db.Boolean(), nullable=False, default=True)
    # 0 => solo segundos || 1=> completo
    activo = db.Column(db.Boolean(), nullable=False, default=True)
    observaciones = db.Column(db.Text, nullable=True)
    cantidad_consumida = db.Column(db.Integer, nullable=True, default=0)
    resgistred_at = db.Column(db.DateTime(), nullable=False,
                              default=datetime.now())

    # crear una nueva instancia
    @classmethod
    def create(cls, monto, universitario, almuerzo_completo, activo):
        tipo = True if monto in [350, 300] else False
        return Pension(monto=monto, universitario=universitario,
                       almuerzo_completo=almuerzo_completo,
                       tipo=tipo, activo=activo)

    def dias_restante(self) -> int:
        tiene_almuerzos = self.verificar_dias_restantes()
        if tiene_almuerzos:
            tipo = 30 if self.tipo else 15
            return tipo - self.cantidad_consumida
        self.activo = False
        return 0

    def verificar_dias_restantes(self) -> bool:
        tiempo = 30 if self.tipo else 15
        return self.cantidad_consumida <= tiempo

    def aumentar_consumo(self) -> int:
        tiene_almuerzos = self.verificar_dias_restantes()
        if tiene_almuerzos:
            self.cantidad_consumida += 1
            return
        return -1

    def save(self) -> bool:
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def unsave(self) -> bool:
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def __str__(self) -> str:
        return f"Pension {self.monto} id: {self.id}"

    def to_representation(self) -> dict:
        return {
            "id": self.id,
            "monto": self.monto,
            "universitario": self.universitario,
            "almuerzo_completo": self.almuerzo_completo,
            "activo": self.activo,
            "observaciones": self.observaciones,
            "cantidad_consumida": self.cantidad_consumida,
            "resgistred_at": self.resgistred_at
        }

# monto, universitario, almuerzo_completo, activo


def registrar_pension() -> int:
    monto = random.choice([350, 175, 300, 150])
    universitario = fake.boolean(chance_of_getting_true=25)
    almuerzo_completo = fake.boolean(chance_of_getting_true=80)
    activo = fake.boolean(chance_of_getting_true=70)

    pension = Pension.create(monto=monto, universitario=universitario,
                             almuerzo_completo=almuerzo_completo, activo=activo)
    pension.save()
    return pension.id
