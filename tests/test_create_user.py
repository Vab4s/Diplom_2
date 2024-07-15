import allure
from helpers.register_random_user import register_new_user_and_return_userdata_and_response
from helpers.delete_user import delete_user


@allure.story('Проверка создания пользователя')
class TestCreateUser:
    @allure.title('Корректное создание пользователя')
    @allure.description('Заполнены все поля')
    def test_create_user_with_correct_data(self):
        user_data, response_text, response_code = register_new_user_and_return_userdata_and_response()
        email, _, name = user_data
        assert (response_text['success'] is True
                and response_text['user']['email'] == user_data[0]
                and response_text['user']['name'] == user_data[2]
                and response_text['accessToken']
                and response_text['refreshToken']
                and response_code == 200)

        delete_user(user_data, response_text)

    @allure.title('Создание дубликата пользователя')
    @allure.description('Все поля заполнены данными уже созданного пользователя')
    def test_create_duplicate_user(self):
        user_data, response_text, _ = register_new_user_and_return_userdata_and_response()
        new_courier_data, new_response_text, new_response_code = register_new_user_and_return_userdata_and_response(user_data)
        assert (new_response_text['success'] is False
                and new_response_text['message'] == 'User already exists'
                and new_response_code == 403)

        delete_user(user_data, response_text)

    @allure.title('Создание пользователя без заполнения поля login')
    @allure.description('Поле "login" не заполнено')
    def test__create_user_without_email(self):
        user_data, response_text, response_code = register_new_user_and_return_userdata_and_response(custom_email='')
        assert (response_text['success'] is False
                and response_text['message'] == 'Email, password and name are required fields'
                and response_code == 403)

    @allure.title('Создание пользователя без заполнения поля "password"')
    @allure.description('Поле "password" не заполнено')
    def test__create_user_without_password(self):
        user_data, response_text, response_code = register_new_user_and_return_userdata_and_response(custom_password='')
        assert (response_text['success'] is False
                and response_text['message'] == 'Email, password and name are required fields'
                and response_code == 403)

    @allure.title('Создание пользователя без заполнения поля "name"')
    @allure.description('Поле "name" не заполнено')
    def test__create_user_without_name(self):
        user_data, response_text, response_code = register_new_user_and_return_userdata_and_response(custom_name='')
        assert (response_text['success'] is False
                and response_text['message'] == 'Email, password and name are required fields'
                and response_code == 403)
