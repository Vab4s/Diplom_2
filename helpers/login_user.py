import requests
from data.endpoints import POST_LOGIN, POST_LOGOUT

def login_user(email, password):
    payload = {"email": email, "password": password}
    response = requests.post(POST_LOGIN, data=payload)
    assert response.status_code == 200

def logout_user(token):
    payload = {"token": token}
    response = requests.post(POST_LOGOUT, data=payload)
    assert response.status_code == 200
