BASE = 'https://stellarburgers.nomoreparties.site'

GET_USER_ORDERS = BASE + '/api/orders'
GET_INGREDIENTS = BASE + '/api/ingredients'     # Получение данных об ингредиентах
POST_CREATE_USER = BASE + '/api/auth/register'  # Создание пользователя
POST_LOGIN = BASE + '/api/auth/login'           # Логин пользователя
POST_LOGOUT = BASE + '/api/auth/logout'         # Выход из системы
POST_CREATE_ORDER = BASE + '/api/orders'        # Создание заказа
DELETE_USER = BASE + '/api/auth/user'           # Удаление пользователя
PATCH_CHANGE_USER = BASE + '/api/auth/user'     # Изменение данных пользователя
