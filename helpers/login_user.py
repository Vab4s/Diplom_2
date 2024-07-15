import requests
from data.endpoints import POST_LOGIN, POST_LOGOUT

def login_user(email, password):
    payload = {"email": email, "password": password}
    response = requests.post(POST_LOGIN, data=payload)
    if response.status_code == 200:
        return True
def logout_user(response_text):
    payload = {"token": response_text['refreshToken']}
    response = requests.post(POST_LOGOUT, data=payload)
    if response.status_code == 200:
        return True
