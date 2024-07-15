import allure
import requests
import re

from helpers.register_random_user import register_new_user_and_return_userdata_and_response, generate_random_string
from helpers.delete_user import delete_user
from helpers.random_order import order
from data.endpoints import POST_CREATE_ORDER

class TestCreateOrder:
    @classmethod
    @allure.title('Создание пользователя и необходимых переменных')
    def setup_class(cls):
        cls.user_data, cls.response_text, cls.response_code = register_new_user_and_return_userdata_and_response()
        cls.access_token = cls.response_text['accessToken']

    def test_create_order_with_authorization_with_ingredients(self):
        new_order = order()
        response = requests.post(POST_CREATE_ORDER, data=new_order, headers={"Authorization": self.access_token})
        assert (response.json()['success'] is True
                and response.json()['name']
                and len(response.json()['order']['ingredients']) == len(new_order['ingredients'])
                and response.status_code == 200)

    def test_create_order_without_authorization_with_ingredients(self):
        new_order = order()
        response = requests.post(POST_CREATE_ORDER, data=new_order)
        assert (response.json()['success'] is True
                and response.json()['name']
                and re.fullmatch(r'\d{4}', str(response.json()['order']['number']))
                and response.status_code == 200)

    def test_create_order_with_authorization_without_ingredients(self):
        new_order = order(0)
        response = requests.post(POST_CREATE_ORDER, data=new_order, headers={"Authorization": self.access_token})
        assert (response.json()['success'] is False
                and response.json()['message'] == 'Ingredient ids must be provided'
                and response.status_code == 400)

    def test_create_order_without_authorization_without_ingredients(self):
        new_order = order(0)
        response = requests.post(POST_CREATE_ORDER, data=new_order, headers={"Authorization": self.access_token})
        assert (response.json()['success'] is False
                and response.json()['message'] == 'Ingredient ids must be provided'
                and response.status_code == 400)

    def test_create_order_with_authorization_with_wrong_hash(self):
        new_order = order(3, hash=False)
        response = requests.post(POST_CREATE_ORDER, data=new_order, headers={"Authorization": self.access_token})
        assert 'Internal Server Error' in response.text and response.status_code == 500

    def test_create_order_without_authorization_with_wrong_hash(self):
        new_order = order(3, hash=False)
        response = requests.post(POST_CREATE_ORDER, data=new_order)
        assert 'Internal Server Error' in response.text and response.status_code == 500

    def test_create_order_with_authorization_with_wrong_hash_with_eleven_symbols(self):
        new_order = {'ingredients': [f'{generate_random_string(12)}']}
        response = requests.post(POST_CREATE_ORDER, data=new_order, headers={"Authorization": self.access_token})
        assert (response.json()['success'] is False
                and response.json()['message'] == 'One or more ids provided are incorrect'
                and response.status_code == 400)

    def test_create_order_without_authorization_with_wrong_hash_with_eleven_symbols(self):
        new_order = {'ingredients': [f'{generate_random_string(12)}']}
        response = requests.post(POST_CREATE_ORDER, data=new_order)
        assert (response.json()['success'] is False
                and response.json()['message'] == 'One or more ids provided are incorrect'
                and response.status_code == 400)

    @classmethod
    @allure.title('Удаление созданного пользователя')
    def teardown_class(cls):
        delete_user(cls.user_data, cls.response_text)