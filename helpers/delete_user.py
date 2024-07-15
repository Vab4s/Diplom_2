import requests
import allure
from data.endpoints import DELETE_USER


@allure.step('Удаление курьера')
@allure.description('"email" и "password" берутся из user_data, возвращаемого функцией регистрации юзера,'
                    'токен берётся из словаря response.json() по ключу "accessToken"')
def delete_user(userdata, response_text):
    payload = {"email": userdata[0], "password": userdata[1]}
    requests.delete(DELETE_USER, data=payload, headers={"Authorization": response_text['accessToken']})
