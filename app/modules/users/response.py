from modules.users import UserInfoDTO
from shared import base_response

get_subscription_response = {
    **base_response,
    200: {"description": "Данные о подписке", "model": UserInfoDTO},
    404: {"description": "Подписка не найдена"},
}

get_user_info_response = {
    **base_response,
    200: {"description": "Данные пользователя", "model": UserInfoDTO},
    401: {"description": "Пользователь не найден"},
    409: {"description": "У пользователя нет подписки"},
}

create_or_update_fcm_token_response = {
    **base_response,
    200: {"description": "FCM токен успешно обновлён"},
    401: {"description": "Пользователь не найден"},
}
