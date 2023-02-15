from . import *


class TestUsuariosApi(TestBase):
    # GET
    def test_get_usuarios(self):
        response = self.client.get(
            self.urls['base'],
            headers=self.token_super_user
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['succses'], True)

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

    def test_zz_get_sin_usuarios(self):
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

    def test_get_one_usuario(self):
        response = self.client.get(
            self.urls['base'] + '1',
            headers=self.token_super_user
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['succses'], True)
        self.assertEqual(response.get_json()['message'], 'usuario encontrado')
        self.assertEqual(response.get_json()['data']['id'], 1)

    def test_get_one_false_usuario(self):
        response = self.client.get(
            self.urls['base'] + '10',
            headers=self.token_super_user
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['succses'], False)
        self.assertEqual(response.get_json()[
                         'message'], 'no existe la usuario con id: 10')

    # POST
    def test_create_usuario(self):
        from faker import Faker
        from app.tests.factories.Pension import create_one_pension

        faker = Faker(99)
        pension = create_one_pension()
        pension.save()

        response = self.client.post(
            self.urls['base'],
            json={
                "email": faker.email(),
                "name": faker.name(),
                "phone": faker.phone_number(),
                "sex": "M",
                "password": "123456",
                "pension_id": pension.id
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['succses'], True)
        self.assertEqual(response.get_json()['message'], 'registro exitoso')

    def test_create_usuario_datos_erroneos(self):
        from faker import Faker
        from app.tests.factories.Pension import create_one_pension

        faker = Faker(99)
        pension = create_one_pension()
        pension.save()

        response = self.client.post(
            self.urls['base'],
            json={
                "email": "email",
                "name": 123,
                "phone": faker.phone_number(),
                "sex": "M",
                "password": "123456",
                "pension_id": pension.id
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['succses'], False)
        self.assertGreater(len(str(response.get_json()['message'])), 10)

    def test_create_usuario_existente(self):
        from faker import Faker
        from app.tests.factories.Pension import create_one_pension

        faker = Faker(99)
        pension = create_one_pension()
        pension.save()

        response = self.client.post(
            self.urls['base'],
            json={
                "email": self.usuario.email,
                "name": faker.name(),
                "phone": faker.phone_number(),
                "sex": "M",
                "password": "123456",
                "pension_id": pension.id
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['succses'], False)
        self.assertEqual(response.get_json()[
                         'message'], 'Ya existe un registro con estos datos')

    def test_create_error_db(self):
        from faker import Faker
        from app.tests.factories.Pension import create_one_pension
        from app.Models.Usuario import Usuario

        faker = Faker(95)
        pension = create_one_pension()
        pension.save()
        save = Usuario.save
        Usuario.save = lambda self: False

        response = self.client.post(
            self.urls['base'],
            json={
                "email": faker.email(),
                "name": faker.name(),
                "phone": faker.phone_number(),
                "sex": "M",
                "password": "123456",
                "pension_id": pension.id
            }
        )

        Usuario.save = save

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['succses'], False)
        self.assertEqual(response.get_json()['message'], 'registro erroneo')

    # PUT PATCH
    def test_update_usuario(self):
        response = self.client.patch(
            self.urls['base']+str(self.usuario.id),
            json={
                "email": "update@gmail.com",
                "password": "123456",
                "phone": "123456789",
            },
            headers=self.token_user
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['succses'], True)
        self.assertEqual(response.get_json()[
                         'message'], 'actualizacion exitosa')

    def test_update_usuario_con_datos_erroneos(self):
        response = self.client.patch(
            self.urls['base']+str(self.usuario.id),
            json={
                "email": "update@gmail.com",
            },
            headers=self.token_user
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['succses'], False)
        self.assertGreater(len(str(response.get_json()['message'])), 10)

    def test_update_usuario_error_db(self):
        from app.Models.Usuario import Usuario

        save = Usuario.save
        Usuario.save = lambda self: False

        response = self.client.patch(
            self.urls['base']+str(self.usuario.id),
            json={
                "email": "update@gmail.com",
                "password": "123456",
                "phone": "123456789",
            },
            headers=self.token_user
        )

        Usuario.save = save
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['succses'], False)
        self.assertEqual(response.get_json()[
                         'message'], 'Algo salio mal en la DB')

    # delete
    def test_zz_delete_usuario(self):
        response = self.client.delete(
            self.urls['base']+str(self.usuario.id),
            headers=self.token_user
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['succses'], True)
        self.assertEqual(response.get_json()[
                         'message'], 'Eliminacion exitosa')

    def test_zz_delete_usuario_error_db(self):
        from app.Models.Usuario import Usuario

        usuario_nuevo = create_one_user()
        usuario_nuevo.save()

        request = self.client.post(
            self.urls['login'],
            json={
                "email": usuario_nuevo.email,
                "password": "123456"
            }
        )

        token = request.get_json()['data']['token']

        delete = Usuario.unsave
        Usuario.unsave = lambda self: False

        response = self.client.delete(
            self.urls['base']+str(usuario_nuevo.id),
            headers={'Authorization': 'Bearer '+token}
        )

        Usuario.unsave = delete

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['succses'], False)
        self.assertEqual(response.get_json()[
                         'message'], 'Algo salio mal')