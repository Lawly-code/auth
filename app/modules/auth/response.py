from modules.auth import AuthTokenResponseDTO, LoginUserDTO

login_response = {
    200: {"description": "Успешная аутентификация", "model": LoginUserDTO},
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
}
