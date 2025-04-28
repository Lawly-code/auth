from modules.auth import AuthTokenResponseDTO

login_response = {
    200: {"description": "Успешная аутентификация", "model": AuthTokenResponseDTO},
    401: {"description": "Неверные учетные данные"},
}

register_response = {
    200: {
        "description": "Пользователь успешно зарегистрирован",
        "model": AuthTokenResponseDTO,
    },
    409: {"description": "Пользователь с таким email уже существует"},
}

logout_response = {
    202: {"description": "Успешный выход из системы"},
    403: {"description": "Неверные учетные данные"},
}

refresh_token_response = {
    200: {"description": "Токены успешно обновлены", "model": AuthTokenResponseDTO},
    403: {"description": "Неверные учетные данные"},
}
