import unittest
from app.Models.Usuario import Usuario
from faker import Faker
from app.tests.factories.Usuario import create_one_user


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from app import create_app
        from config import config

        config = config["test"]
        cls.app = create_app(config)
        cls.client = cls.app.test_client()

        cls.usuario = create_one_user()
        cls.super_usuario = create_one_user(administrador=True)
        cls.usuario.save()
        cls.super_usuario.save()

        cls.urls_usuario = {
            "base": "usuarios/",
            "login": "usuarios/login"
        }
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        from app import db

        db.session.remove()
        db.drop_all()

        return super().tearDownClass()

    def setUp(self) -> None:

        request = self.client.post(
            TestBase.urls_usuario["login"],
            json={
                "email": TestBase.super_usuario.email,
                "password": "123456"
            }
        )

        self.header = {"Authorization": "Bearer " +
                       request.get_json()['token']}

        return super().setUp()

    def test_algo(self):
        pass
