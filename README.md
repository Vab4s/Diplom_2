## Дипломный проект. Задание 3: Юнит-тесты

### Автотесты для проверки веб-приложения Stellar Burgers

### Структура проекта

Директория data:
    
    endpoints.py - API эндпоинты
    ingredients.py - список ингредиентов
    response_messages.py - ответы сервера

Директория helpers:

    delete_user.py - удаление пользователя
    login_user.py - логин пользователя
    random_order.py - создание списка ингредиентов
    register_random_user.py - регистрация рандомного пользователя
    response_body_check.py -проверка тела ответа

Директория tests:

    test_change_user_data.py - Проверка создания пользователя
    test_create_order.py - Проверка логина пользователя
    test_create_user.py - Проверка изменения данных пользователя
    test_get_orders.py - Проверка создание заказа
    test_login_user.py - Проверка получения заказов конкретного пользователя