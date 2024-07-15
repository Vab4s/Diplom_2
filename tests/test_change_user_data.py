import allure
import requests

from helpers.register_random_user import generate_random_string
from helpers.register_random_user import register_new_user_and_return_userdata_and_response
from helpers.delete_user import delete_user
from helpers.login_user import login_user, logout_user

from data.endpoints import PATCH_CHANGE_USER

class TestChangeUserData:
    @classmethod
    @allure.title('Создание пользователя и необходимых переменных')
    def setup_class(cls):
        cls.user_data, cls.response_text, cls.response_code = register_new_user_and_return_userdata_and_response()
        cls.email, cls.password, cls.name = cls.user_data

    def test_change_user_email_with_auth(self):
        new_email = f'{generate_random_string()}@{generate_random_string(5)}.{generate_random_string(3)}'
        payload = {"email": new_email}
        response = requests.patch(PATCH_CHANGE_USER, data=payload, headers={"Authorization": self.response_text['accessToken']})
        assert (response.json()['success'] is True
                and response.json()['user']['email'] == new_email
                and response.json()['user']['name']
                and response.status_code == 200)

        requests.patch(PATCH_CHANGE_USER, data={"email": self.email},
                                  headers={"Authorization": self.response_text['accessToken']})

    def test_change_user_password_with_auth(self):
        new_password = generate_random_string()
        payload = {"password": new_password}
        response = requests.patch(PATCH_CHANGE_USER, data=payload,
                                  headers={"Authorization": self.response_text['accessToken']})
        assert (response.json()['success'] is True
                and response.json()['user']['email']
                and response.json()['user']['name']
                and login_user(self.email, new_password)
                and response.status_code == 200)

        logout_user(self.response_text)

    def test_change_user_name_with_auth(self):
        new_name = generate_random_string()
        payload = {"name": new_name}
        response = requests.patch(PATCH_CHANGE_USER, data=payload,
                                  headers={"Authorization": self.response_text['accessToken']})
        assert (response.json()['success'] is True
                and response.json()['user']['email']
                and response.json()['user']['name'] == new_name
                and response.status_code == 200)

        requests.patch(PATCH_CHANGE_USER, data={"name": self.name},
                                  headers={"Authorization": self.response_text['accessToken']})

    def test_change_user_email_without_auth(self):
        new_email = generate_random_string()
        payload = {"email": new_email}
        response = requests.patch(PATCH_CHANGE_USER, data=payload)
        assert (response.json()['success'] is False
                and response.json()['message'] == 'You should be authorised'
                and response.status_code == 401)

    def test_change_user_password_without_auth(self):
        new_password = generate_random_string()
        payload = {"password": new_password}
        response = requests.patch(PATCH_CHANGE_USER, data=payload)
        assert (response.json()['success'] is False
                and response.json()['message'] == 'You should be authorised'
                and response.status_code == 401)

    def test_change_user_name_without_auth(self):
        new_name = generate_random_string()
        payload = {"name": new_name}
        response = requests.patch(PATCH_CHANGE_USER, data=payload)
        assert (response.json()['success'] is False
                and response.json()['message'] == 'You should be authorised'
                and response.status_code == 401)

    @classmethod
    @allure.title('Удаление созданного пользователя')
    def teardown_class(cls):
        delete_user(cls.user_data, cls.response_text)
