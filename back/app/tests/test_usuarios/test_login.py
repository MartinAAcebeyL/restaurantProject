from . import *


class TestLogin(TestBase):
    def test_super_user_sin_data(self):
        respose = self.client.post(
            self.urls['login'],
            json={
                "email": self.super_usuario.email,
            }
        )
        
        self.assertEqual(respose.status_code, 400)
        self.assertEqual(respose.get_json()[
                         'message']['password']['message'], 'Password requerido')
        self.assertEqual(respose.get_json()['succses'], False)

    def test_super_user_sin_password(self):
        respose = self.client.post(
            self.urls['login'],
            json={
                "password": "123456"
            }
        )

        self.assertEqual(respose.status_code, 400)
        self.assertEqual(respose.get_json()[
                         'message']['email']['message'], 'email requerido')
        self.assertEqual(respose.get_json()['succses'], False)

    def test_super_user_con_data_incorrecta(self):
        respose = self.client.post(
            self.urls['login'],
            json={
                "email": self.super_usuario.email,
                "password": "1234567"
            }
        )
        print(respose.get_json())

        self.assertEqual(respose.status_code, 400)
        self.assertEqual(respose.get_json()['message'], 'datos incorectos')
        self.assertEqual(respose.get_json()['succses'], False)

    def test_super_user_con_data_correcta(self):
        respose = self.client.post(
            self.urls['login'],
            json={
                "email": self.super_usuario.email,
                "password": "123456"
            }
        )
        print(respose.get_json())

        self.assertEqual(respose.status_code, 200)
        self.assertEqual(respose.get_json()['data']['token'], self.token_super_user['Authorization'].split(' ')[1])
        self.assertEqual(respose.get_json()['succses'], True)
