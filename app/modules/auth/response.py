from modules.auth import LoginUserDTO, RegisterUserDTO

login_response = {
    200: {"description": "Успешная аутентификация", "model": LoginUserDTO},
    401: {"description": "Неверные учетные данные"},
}

register_response = {
    201: {"description": "Пользователь успешно зарегистрирован", "model": RegisterUserDTO},
    409: {"description": "Пользователь с таким email уже существует"},
}

logout_response = {
    202: {"description": "Успешный выход из системы"},
}