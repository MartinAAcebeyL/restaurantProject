from . import *

class UsuarioShema(Schema):
    class Meta:
        ordered = True
        fields = ('id', 'name', 'phone', 'email', 'sex', 'resgistred')

class ParamsUsuarioShema(Schema):
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


usuario_shema  = UsuarioShema()
usuario_shemas = UsuarioShema(many=True)

paramsUsuarioShema = ParamsUsuarioShema()