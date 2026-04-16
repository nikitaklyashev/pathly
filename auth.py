from werkzeug.security import generate_password_hash, check_password_hash
from password_strength import PasswordPolicy
from db import get_user_by_login

def validate_password(password, confirm_password):
    CONFIRM_PASSWORD_ERROR = "Пароли не совпадают!"
    EMPTY_PASSWORD_ERROR = "Пароль не может быть пустым!"
    PASSWORD_STRENGTH_ERROR = "Пароль должен быть длиной не менее 8 символов, включать заглавную букву и цифру!"

    if not password:
        return EMPTY_PASSWORD_ERROR

    if password != confirm_password:
        return CONFIRM_PASSWORD_ERROR


    policy = PasswordPolicy.from_names(
        length=8,
        numbers=1,
        uppercase=1,
    )
    
    result = policy.test(password)

    if result:
        return PASSWORD_STRENGTH_ERROR
    
    return "SUCCESS"


def validate_login(login): 
    EMPTY_LOGIN_ERROR = "Вы не ввели логин!"
    LENGTH_LOGIN_ERROR = "Логин должен быть длиной не менее 4 символов!"
    EXISTS_LOGIN_ERROR = "Пользователь с таким именем уже существует!"

    if not login:
        return EMPTY_LOGIN_ERROR

    if len(login) < 4:
        return LENGTH_LOGIN_ERROR
    
    if get_user_by_login(login):
        return EXISTS_LOGIN_ERROR

    return "SUCCESS"
