import allure
import requests

from helpers.register_random_user import register_new_user_and_return_userdata_and_response
from helpers.delete_user import delete_user
from helpers.response_body_check import response_body_get_check

from data.endpoints import GET_USER_ORDERS
from data.response_messages import ERROR_UNAUTHORIZED

@allure.story('Проверка получения списка заказов')
class TestGetOrders:
    @classmethod
    @allure.title('Создание пользователя и необходимых переменных')
    def setup_class(cls):
        cls.user_data, cls.response_text, cls.response_code = register_new_user_and_return_userdata_and_response()
        cls.email, cls.password, cls.name = cls.user_data
        cls.access_token = cls.response_text['accessToken']

    @allure.title('Получение списка заказов авторизованного пользователя')
    def test_get_orders_authorized_user(self):
        response = requests.get(GET_USER_ORDERS, headers={"Authorization": self.access_token})

        assert response_body_get_check(response) is True and response.status_code == 200

    @allure.title('Получение списка заказов неавторизованного пользователя')
    def test_get_order_unauthorized_user(self):
        response = requests.get(GET_USER_ORDERS)

        assert response_body_get_check(response, message=ERROR_UNAUTHORIZED) is False and response.status_code == 401

    @classmethod
    @allure.title('Удаление созданного пользователя')
    def teardown_class(cls):
        delete_user(cls.user_data, cls.response_text)
