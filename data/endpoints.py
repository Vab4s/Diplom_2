BASE = 'https://stellarburgers.nomoreparties.site'

POST_CREATE_USER = BASE + '/api/auth/register'  # Создание пользователя
POST_LOGIN = BASE + '/api/auth/login'           # Логин пользователя
POST_LOGOUT = BASE + '/api/auth/logout'         # Выход из системы

DELETE_USER = BASE + '/api/auth/user'           # Удаление пользователя

PATCH_CHANGE_USER = BASE + '/api/auth/user'     # Изменение данных пользователя

GET_INGREDIENTS = BASE + '/api/ingredients'     # Получение данных об ингредиентах
