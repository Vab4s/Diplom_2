import allure
import requests

from helpers.register_random_user import register_new_user_and_return_userdata_and_response
from helpers.delete_user import delete_user
from data.endpoints import GET_USER_ORDERS

class TestGetOrders:
    @classmethod
    @allure.title('Создание пользователя и необходимых переменных')
    def setup_class(cls):
        cls.user_data, cls.response_text, cls.response_code = register_new_user_and_return_userdata_and_response()
        cls.email, cls.password, cls.name = cls.user_data
        cls.access_token = cls.response_text['accessToken']
    def test_get_order_authorized_user(self):
        response = requests.get(GET_USER_ORDERS, headers={"Authorization": self.access_token})
        assert response.json()['success'] is True and response.status_code == 200

    def test_get_order_unauthorized_user(self):
        response = requests.get(GET_USER_ORDERS)
        assert (response.json()['success'] is False
                and response.json()['message'] == 'You should be authorised'
                and response.status_code == 401)

    @classmethod
    @allure.title('Удаление созданного пользователя')
    def teardown_class(cls):
        delete_user(cls.user_data, cls.response_text)
