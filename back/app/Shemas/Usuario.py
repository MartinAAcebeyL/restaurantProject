from . import *


class UsuarioShema(Schema):
    class Meta:
        ordered = True
        fields = ('id', 'name', 'phone', 'sex',  'email',
                  'password', 'administrador', 'resgistred',
                  'pension_id')

class ParamsUpdateUsuarioShema(Schema):
    phone = fields.Str(required=True, validate=Length(min=5, max=40),
                       error_messages={
        "required": {"message": "Telefono requerido"}
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

class ParamsCreateUsuarioShema(ParamsUpdateUsuarioShema):
    name = fields.Str(required=True,
                      validate=Length(min=10, max=50),
                      error_messages={
                          "required": {"message": "Nombre requerido", "code": 400}
                      })
    sex = fields.Str(required=True, validate=OneOf(choices=['F', 'M', 'O']),
                     error_messages={
        "required": {"message": "Sexo requerido"}
    })

    pension_id = fields.Int(required=True,
                            error_messages={
                                "required": {"message": "pension_id requerido"}
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


usuario_shema = UsuarioShema()
usuario_shemas = UsuarioShema(many=True)

paramsCreateUsuarioShema = ParamsCreateUsuarioShema()
paramsUpdateUsuarioShema = ParamsUpdateUsuarioShema()
loginParamsUsuarioShema = LoginParamsUsuarioShema()