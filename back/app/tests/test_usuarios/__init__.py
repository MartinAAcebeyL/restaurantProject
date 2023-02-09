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

        cls.urls = {
            "base": "usuarios/",
            "login": "usuarios/login"
        }

        request = cls.client.post(
            cls.urls["login"],
            json={
                "email": cls.super_usuario.email,
                "password": "123456"
            })
        token = request.get_json().get("data").get("token")
        cls.token_super_user = {"Authorization": "Bearer " + token}

        request = cls.client.post(
            cls.urls["login"],
            json={
                "email": cls.usuario.email,
                "password": "123456"
            }
        )
        token = request.get_json().get("data").get("token")
        cls.token_user = {"Authorization": "Bearer " + token}

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        from app import db

        db.session.remove()
        db.drop_all()

        return super().tearDownClass()
