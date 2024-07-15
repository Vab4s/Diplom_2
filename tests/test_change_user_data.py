import allure
import requests

from helpers.register_random_user import generate_random_string
from helpers.register_random_user import register_new_user_and_return_userdata_and_response
from helpers.delete_user import delete_user
from helpers.response_body_check import response_body_change_user_check

from data.endpoints import PATCH_CHANGE_USER
from data.response_messages import ERROR_UNAUTHORIZED

@allure.story('Проверка изменения данных пользователя')
class TestChangeUserData:
    @classmethod
    @allure.title('Создание пользователя и необходимых переменных')
    def setup_class(cls):
        cls.user_data, cls.response_text, cls.response_code = register_new_user_and_return_userdata_and_response()
        cls.email, cls.password, cls.name = cls.user_data
        cls.access_token = cls.response_text['accessToken']
        cls.refresh_token = cls.response_text['refreshToken']

    @allure.title('Проверка изменения поля email пользователя  авторизацией')
    @allure.description('В вонце теста поле email озвращается к исходному значению self.email')
    def test_change_user_email_with_auth(self):
        new_email = f'{generate_random_string()}@{generate_random_string(5)}.{generate_random_string(3)}'
        payload = {"email": new_email}
        response = requests.patch(PATCH_CHANGE_USER, data=payload, headers={"Authorization": self.response_text['accessToken']})

        assert (response_body_change_user_check(response.json(), new_email, self.name) is True
                and response.status_code == 200)

        requests.patch(PATCH_CHANGE_USER, data={"email": self.email}, headers={"Authorization": self.access_token})

    @allure.title('Проверка изменения поля password пользователя  авторизацией')
    @allure.description('Корректность изменения пароля проверяется путём авторизации с новым паролем.'
                        'В вонце теста поле password озвращается к исходному значению self.password')
    def test_change_user_password_with_auth(self):
        new_password = generate_random_string()
        payload = {"password": new_password}
        response = requests.patch(PATCH_CHANGE_USER, data=payload,
                                  headers={"Authorization": self.response_text['accessToken']})

        assert (response_body_change_user_check(response.json(), self.email, self.name, password=new_password, token=self.refresh_token) is True
                and response.status_code == 200)

        requests.patch(PATCH_CHANGE_USER, data={"password": self.password}, headers={"Authorization": self.access_token})

    @allure.title('Проверка изменения поля name пользователя  авторизацией')
    @allure.description('К вонце теста поле name озвращается к исходному значению self.name')
    def test_change_user_name_with_auth(self):
        new_name = generate_random_string()
        payload = {"name": new_name}
        response = requests.patch(PATCH_CHANGE_USER, data=payload,
                                  headers={"Authorization": self.access_token})

        assert (response_body_change_user_check(response.json(), self.email, new_name) is True
                and response.status_code == 200)

        requests.patch(PATCH_CHANGE_USER, data={"name": self.name}, headers={"Authorization": self.response_text['accessToken']})

    @allure.title('Проверка изменения поля email пользователя без авторизации')
    def test_change_user_email_without_auth(self):
        new_email = generate_random_string()
        payload = {"email": new_email}
        response = requests.patch(PATCH_CHANGE_USER, data=payload)

        assert (response_body_change_user_check(response.json(), message=ERROR_UNAUTHORIZED) is False
                and response.status_code == 401)

    @allure.title('Проверка изменения поля password пользователя без авторизации')
    def test_change_user_password_without_auth(self):
        new_password = generate_random_string()
        payload = {"password": new_password}
        response = requests.patch(PATCH_CHANGE_USER, data=payload)

        assert (response_body_change_user_check(response.json(), message=ERROR_UNAUTHORIZED) is False
                and response.status_code == 401)

    @allure.title('Проверка изменения поля name пользователя без авторизации')
    def test_change_user_name_without_auth(self):
        new_name = generate_random_string()
        payload = {"name": new_name}
        response = requests.patch(PATCH_CHANGE_USER, data=payload)

        assert (response_body_change_user_check(response.json(), message=ERROR_UNAUTHORIZED) is False
                and response.status_code == 401)

    @classmethod
    @allure.title('Удаление созданного пользователя')
    def teardown_class(cls):
        delete_user(cls.user_data, cls.response_text)
