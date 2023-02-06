import unittest
from app.Models.Usuario import Usuario
from faker import Faker
from app.tests.factories.Usuario import create_one_user


class TestBase(unittest.TestCase):
    def setUp(self) -> None:
        from app import create_app, db
        from config import config

        faker = Faker(12)

        config = config["test"]
        self.app = create_app(config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        self.urls_usuario = {
            "base_usuario": "usuarios/",
            "login": "usuarios/login",
        }

        self.usuario = create_one_user()
        self.super_usuario = create_one_user(administrador=True)

        print(self.super_usuario.email, self.super_usuario.password)

        request = self.client.post(
            self.urls_usuario["login"],
            json={
                "email": "admin@gmail.com",
                "password": "123456"
            }
        )

        print("test")
        print(request.get_json())
        print(request)

        request= self.client.get(
            self.urls_usuario["base_usuario"],
        )

        print("despues")
        print(request.get_json())
        print(request)


        return super().setUp()

    def test_algo(self):
        pass
