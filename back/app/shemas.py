from marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import Length

class PensionadoShema(Schema):
    class Meta:
        fields = ('id', 'name', 'phone', 'email', 'sex', 'resgistred')

class ParamsTaskShema(Schema):
    name = fields.Str(required=True, validate=Length(max=50))
    email = fields.Str(required=True, validate=Length(max=50))
    phone = fields.Str(required=True, validate=Length(max=50))
    sex = fields.Str(required=True, validate=Length(max=50))

pensionado_shema = PensionadoShema()
pensionado_shemas = PensionadoShema(many=True)