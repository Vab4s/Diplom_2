import allure
from helpers.login_user import login_user, logout_user

@allure.step('Проверка тела ответа сервера на post-запрос оздания/авторизации пользователя')
def response_body_create_login_user_check(response_text, user_data=None, message=None):
    if response_text['success']\
            and response_text['user']['email'] == user_data[0]\
            and response_text['user']['name'] == user_data[2]\
            and response_text['accessToken']\
            and response_text['refreshToken']:
        return True
    elif response_text['success'] is False and response_text['message'] == message:
        return False

@allure.step('Проверка тела ответа сервера на patch-запрос изменения пользователя')
def response_body_change_user_check(response_text, email=None, name=None, password=None, token=None, message=None):
    if response_text['success']\
            and response_text['user']['email'] == email\
            and response_text['user']['name'] == name:
        if password:
            login_user(email, password)
            logout_user(token)
        return True
    elif response_text['success'] is False and response_text['message'] == message:
        return False

@allure.step('Проверка тела ответа сервера на post-запрос оздания заказа')
def response_body_create_order_check(response, message=None):
    if 'Internal Server Error' in response.text:
        return False
    elif response.json()['success'] and response.json()['name'] and response.json()['order']:
        return True
    elif not response.json()['success'] and response.json()['message'] == message:
        return False

@allure.step('Проверка тела ответа сервера')
def response_body_get_check(response, message=None):
    if response.json()['success']:
        return True
    elif not response.json()['success'] and response.json()['message'] == message:
        return False
