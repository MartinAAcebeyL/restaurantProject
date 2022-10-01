from random import choices
from marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import Length, OneOf


class PensionadoShema(Schema):
    class Meta:
        ordered = True
        fields = ('id', 'name', 'phone', 'email', 'sex', 'resgistred')


class ParamsPensionadoShema(Schema):
    name = fields.Str(required=True,
                      validate=Length(min=10, max=50),
                      error_messages={
                          "required": {"message": "Nombre requerido", "code": 400}
                      })

    email = fields.Email(required=True, validate=Length(min=10, max=80),
                         error_messages={
        "required": {"message": "email requerido"}
    })

    phone = fields.Str(required=True, validate=Length(min=5, max=40),
                       error_messages={
        "required": {"message": "Telefono requerido"}
    })
    
    sex = fields.Str(required=True, validate=OneOf(choices=['F', 'M', 'O']),
                     error_messages={
        "required": {"message": "Sexo requerido"}
    })


pensionado_shema = PensionadoShema()
pensionado_shemas = PensionadoShema(many=True)

paramsPensionadoShema = ParamsPensionadoShema()
