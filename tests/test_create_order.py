import allure
import requests

from helpers.register_random_user import register_new_user_and_return_userdata_and_response, generate_random_string
from helpers.delete_user import delete_user
from helpers.random_order import order
from helpers.response_body_check import response_body_create_order_check

from data.endpoints import POST_CREATE_ORDER
from data.response_messages import ERROR_EMPTY_INGREDIENTS, ERROR_ELEVEN_SYMBOLS_HASH


@allure.story('Проверка создания заказа')
class TestCreateOrder:
    @classmethod
    @allure.title('Создание пользователя и необходимых переменных')
    def setup_class(cls):
        cls.user_data, cls.response_text, cls.response_code = register_new_user_and_return_userdata_and_response()
        cls.access_token = cls.response_text['accessToken']

    @allure.title('Создание заказа авторизованного пользователя с ингредиентами')
    def test_create_order_with_authorization_with_ingredients(self):
        new_order = order()
        response = requests.post(POST_CREATE_ORDER, data=new_order, headers={"Authorization": self.access_token})

        assert response_body_create_order_check(response) is True and response.status_code == 200

    @allure.title('Создание заказа неавторизованного пользователя с ингредиентами')
    def test_create_order_without_authorization_with_ingredients(self):
        new_order = order()
        response = requests.post(POST_CREATE_ORDER, data=new_order)

        assert response_body_create_order_check(response) is True and response.status_code == 200

    @allure.title('Создание заказа авторизованного пользователя без ингредиентов')
    def test_create_order_with_authorization_without_ingredients(self):
        new_order = order(0)
        response = requests.post(POST_CREATE_ORDER, data=new_order, headers={"Authorization": self.access_token})

        assert response_body_create_order_check(response, message=ERROR_EMPTY_INGREDIENTS) is False and response.status_code == 400

    @allure.title('Создание заказа неавторизованного пользователя без ингредиентов')
    def test_create_order_without_authorization_without_ingredients(self):
        new_order = order(0)
        response = requests.post(POST_CREATE_ORDER, data=new_order, headers={"Authorization": self.access_token})

        assert response_body_create_order_check(response,
                                                message=ERROR_EMPTY_INGREDIENTS) is False and response.status_code == 400

    @allure.title('Создание заказа авторизованного пользователя с некорректным хэшем ингредиентов')
    def test_create_order_with_authorization_with_wrong_hash(self):
        new_order = order(3, hash=False)
        response = requests.post(POST_CREATE_ORDER, data=new_order, headers={"Authorization": self.access_token})

        assert response_body_create_order_check(response) is False and response.status_code == 500

    @allure.title('Создание заказа неавторизованного пользователя с некорректным хэшем ингредиентов')
    def test_create_order_without_authorization_with_wrong_hash(self):
        new_order = order(3, hash=False)
        response = requests.post(POST_CREATE_ORDER, data=new_order)

        assert response_body_create_order_check(response) is False and response.status_code == 500

    @allure.title('Создание заказа авторизованного пользователя с некорректным хэшем, состоящим из 12 символов')
    def test_create_order_with_authorization_with_wrong_hash_with_eleven_symbols(self):
        new_order = {'ingredients': [f'{generate_random_string(12)}']}
        response = requests.post(POST_CREATE_ORDER, data=new_order, headers={"Authorization": self.access_token})

        assert response_body_create_order_check(response,
                                                message=ERROR_ELEVEN_SYMBOLS_HASH) is False and response.status_code == 400

    @allure.title('Создание заказа неавторизованного пользователя с некорректным хэшем, состоящим из 12 символов')
    def test_create_order_without_authorization_with_wrong_hash_with_eleven_symbols(self):
        new_order = {'ingredients': [f'{generate_random_string(12)}']}
        response = requests.post(POST_CREATE_ORDER, data=new_order)

        assert response_body_create_order_check(response,
                                                message=ERROR_ELEVEN_SYMBOLS_HASH) is False and response.status_code == 400

    @classmethod
    @allure.title('Удаление созданного пользователя')
    def teardown_class(cls):
        delete_user(cls.user_data, cls.response_text)
