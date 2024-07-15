import allure

@allure.step('Проверка тела ответа сервера')
def response_body_create_login_check(response_text, user_data=None, message=None):
    if response_text['success'] and isinstance(response_text['user'], dict)\
            and response_text['user']['email'] == user_data[0]\
            and response_text['user']['name'] == user_data[2]\
            and response_text['accessToken']\
            and response_text['refreshToken']:
        return True
    elif response_text['success'] is False and response_text['message'] == message:
        return False

@allure.step('Проверка тела ответа сервера')
def response_body_change_check(response_text, new_user_data, user_data=None, message=None):
    if response_text['success'] and isinstance(response_text['user'], dict)\
            and response_text['user']['email'] == user_data[0]\
            and response_text['user']['name'] == user_data[2]:
        return True
    elif response_text['success'] is False and response_text['message'] == message:
        return False
