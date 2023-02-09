from . import *


class TestUsuariosApi(TestBase):
    def test_get_usuarios(self):
        response = self.client.get(
            self.urls['base'],
            headers=self.token_super_user
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['succses'], True)
        self.assertEqual(len(response.get_json()['data']), 2)

    def test_get_usuarios_sin_token(self):
        response = self.client.get(
            self.urls['base'],
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['succses'], False)
        self.assertEqual(response.get_json()[
                         'message'], 'Error en la validacion del token')

    def test_get_usuarios_con_token_incorrecto(self):
        response = self.client.get(
            self.urls['base'],
            headers=self.token_user
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['succses'], False)
        self.assertEqual(response.get_json()[
                         'message'], 'No tiene permisos para esta ruta')

    def test_z_get_sin_usuarios(self):
        from app import db
        from app.tests.factories.Usuario import create_one_user

        db.session.query(Usuario).delete()
        db.session.commit()

        usuario = create_one_user(administrador=True)
        usuario.save()

        response = self.client.post(
            self.urls['login'],
            json={
                "email": usuario.email,
                "password": "123456"
            }
        )
        token = response.get_json().get("data").get("token")

        response = self.client.get(
            self.urls['base'],
            headers={"Authorization": f"Bearer {token}"}
        )
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()[
            'message'], 'No existen datos')
        self.assertEqual(response.get_json()['succses'], False)
