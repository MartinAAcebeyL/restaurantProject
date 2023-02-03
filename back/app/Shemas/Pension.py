from . import *


class ParamsPensionShema(Schema):
    monto = fields.Int(required=True)
    universitario = fields.Boolean(required=True)
    almuerzo_completo = fields.Boolean(required=True)
    activo = fields.Boolean(required=True)


paramsPensionShema = ParamsPensionShema()
