import requests
import allure

from helpers.register_random_user import register_new_user_and_return_userdata_and_response, generate_random_string
from helpers.response_body_check import response_body_create_login_user_check
from helpers.delete_user import delete_user

from data.endpoints import *
from data.response_messages import ERROR_INCORRECT_LOGIN_DATA


@allure.story('Проверка авторизации пользователя')
class TestLoginCourier:
    @classmethod
    @allure.title('Создание пользователя и необходимых переменных')
    def setup_class(cls):
        cls.user_data, cls.response_text, _ = register_new_user_and_return_userdata_and_response()
        cls.email, cls.password, _ = cls.user_data

    @allure.title('Проверка авторизации пользователя с корректными данными')
    @allure.description('Переданы все обязательные поля, успешный запрос возвращает "success": True')
    def test_login_fields_filled_with_correct_data(self):
        payload = {'email': self.email, 'password': self.password}
        response = requests.post(POST_LOGIN, data=payload)

        assert (response_body_create_login_user_check(response.json(), self.user_data) is True
                and response.status_code == 200)

    @allure.title('Проверка авторизации пользователя c указанием некорректного email\'а')
    def test_incorrect_login(self):
        payload = {'email': generate_random_string(), 'password': self.password}
        response = requests.post(POST_LOGIN, data=payload)

        assert (response_body_create_login_user_check(response.json(), message=ERROR_INCORRECT_LOGIN_DATA) is False
                and response.status_code == 401)

    @allure.title('Проверка авторизации пользователя c указанием некорректного пароля')
    def test_incorrect_password(self):
        payload = {'login': self.email, 'password': generate_random_string()}
        response = requests.post(POST_LOGIN, data=payload)

        assert (response_body_create_login_user_check(response.json(), message=ERROR_INCORRECT_LOGIN_DATA) is False
                and response.status_code == 401)

    @allure.title('Проверка авторизации пользователя c без email\'а')
    def test_login_without_login(self):
        payload = {'email': '', 'password': self.password}
        response = requests.post(POST_LOGIN, data=payload)

        assert (response_body_create_login_user_check(response.json(), message=ERROR_INCORRECT_LOGIN_DATA) is False
                and response.status_code == 401)

    @allure.title('Проверка авторизации пользоветеля c без пароля')
    def test_login_without_login(self):
        payload = {'email': self.email, 'password': ''}
        response = requests.post(POST_LOGIN, data=payload)

        assert (response_body_create_login_user_check(response.json(), message=ERROR_INCORRECT_LOGIN_DATA) is False
                and response.status_code == 401)

    @allure.title('Проверка авторизации несуществующего пользователя')
    def test_login_with_nonexistent_user(self):
        random_email = f'{generate_random_string(10)}@{generate_random_string(5)}.{generate_random_string(3)}'
        payload = {'email': generate_random_string(), 'password': random_email}
        response = requests.post(POST_LOGIN, data=payload)

        assert (response_body_create_login_user_check(response.json(), message=ERROR_INCORRECT_LOGIN_DATA) is False
                and response.status_code == 401)

    @classmethod
    @allure.title('Удаление созданного пользователя')
    def teardown_class(cls):
        delete_user(cls.user_data, cls.response_text)
