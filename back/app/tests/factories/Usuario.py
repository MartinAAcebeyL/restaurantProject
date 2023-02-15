from . import *
from .Pension import create_one_pension


def create_one_user(administrador: bool = False):
    pension = create_one_pension()
    usuario = Usuario.create(
        name=faker.name(),
        phone=faker.phone_number(),
        sex=faker.random_element(elements=("M", "F")),
        email=faker.email(),
        password="123456",
        pension_id=pension.id,
        administrador=administrador,
    )

    return usuario


def get_token(client, email, password):
    response = client.post(
        "usuarios/login",
        json={
            "email": email,
            "password": password
        }
    )
    token = response.get_json().get("data").get("token")

    return token
