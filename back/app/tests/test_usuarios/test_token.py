from . import *
from app.tests.factories.Usuario import get_token
from app.funtions_jwt import write_token, check_token


class TestToken(TestBase):
    def test_time_token(self):
        usuario = create_one_user()
        usuario.save()

        token = write_token(
            data={
                "email": usuario.email,
                "password": "123456"
            },
            time={
                "days": -1
            }
        ).get_json().get('token')

        time = check_token(token)[0].get_json()

        self.assertEqual(time.get("message"), "El token expiro")
        self.assertEqual(time.get("code"), 400)

    def test_verify_token(self):
        usuario = create_one_user()
        usuario.save()

        token = get_token(client=self.client,
                          email=usuario.email,
                          password="123456")

        verify = self.client.get(
            "usuarios/verifyToken",
            headers={"Authorization": "Bearer " + token}
        )

        self.assertEqual(verify.status_code, 200)

    def test_is_the_same_user(self):
        usuario = create_one_user()
        usuario.save()

        response = self.client.delete(
            f"usuarios/{usuario.id}",
            headers=self.token_user
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json().get(
            "message"), "No es el mismo usuario")

    def test_is_the_same_user_1(self):
        usuario = create_one_user()
        usuario.save()

        token = get_token(client=self.client,
                          email=usuario.email,
                          password="123456")

        response = self.client.delete(
            f"usuarios/{usuario.id}",
            headers={"Authorization": "Bearer " + token+"1"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json().get(
            "message"), "Error en la validacion del token")
