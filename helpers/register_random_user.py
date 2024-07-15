import requests
import random
import string
import allure
from data.endpoints import POST_CREATE_USER


@allure.step('Генерация данных пользователя')
def generate_random_string(length=9):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


@allure.step('Регистрация нового пользователя')
def register_new_user_and_return_userdata_and_response(account=None, custom_email=None, custom_password=None, custom_name=None):

    user_data = []

    # генерируем емаил, пароль и имя пользователя
    email = f'{generate_random_string(10)}@{generate_random_string(5)}.{generate_random_string(3)}'
    password = generate_random_string(10)
    name = generate_random_string(10)

    # собираем тело запроса
    if account == None:
        payload = {
            "email": email if custom_email == None else custom_email,
            "password": password if custom_password == None else custom_password,
            "name": name if custom_name == None else custom_name
        }
    else:
        payload = {
            "email": account[0],
            "password": account[1],
            "name": account[2]
        }

    # отправляем запрос на регистрацию и сохраняем ответ в переменную response
    response = requests.post(POST_CREATE_USER, data=payload)

    # если регистрация прошла успешно (код ответа 200), добавляем в список емаил и пароль пользователя
    if response.status_code == 200:
        user_data.append(email)
        user_data.append(password)
        user_data.append(name)

    # возвращаем регистрационные данные, тело ответа и код ответа
    return user_data, response.json(), response.status_code
