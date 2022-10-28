from . import *

class UsuarioShema(Schema):
    class Meta:
        ordered = True
        fields = ('id', 'name', 'phone', 'sex',  'email',
                  'password', 'administrador', 'resgistred',
                  'pension_id')

class ParamsUsuarioShema(Schema):
    name = fields.Str(required=True,
                      validate=Length(min=10, max=50),
                      error_messages={
                          "required": {"message": "Nombre requerido", "code": 400}
                      })

    phone = fields.Str(required=True, validate=Length(min=5, max=40),
                       error_messages={
        "required": {"message": "Telefono requerido"}
    })

    sex = fields.Str(required=True, validate=OneOf(choices=['F', 'M', 'O']),
                     error_messages={
        "required": {"message": "Sexo requerido"}
    })

    email = fields.Email(required=True, validate=Length(min=10, max=80),
                         error_messages={
        "required": {"message": "email requerido"}
    })

    password = fields.Str(required=True,
                      validate=Length(min=6),
                      error_messages={
                          "required": {"message": "Password requerido"}
                      })


class LoginParamsUsuarioShema(Schema):
    email = fields.Email(required=True, validate=Length(min=10, max=80),
                         error_messages={
        "required": {"message": "email requerido"}
    })

    password = fields.Str(required=True,
                          validate=Length(min=6),
                          error_messages={
                              "required": {"message": "Password requerido"}
                          })

usuario_shema  = UsuarioShema()
usuario_shemas = UsuarioShema(many=True)

paramsUsuarioShema = ParamsUsuarioShema()
loginParamsUsuarioShema = LoginParamsUsuarioShema()