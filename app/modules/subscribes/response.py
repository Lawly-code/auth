from modules.subscribes import GetUserSubscriptionDTO, TariffDTO
from shared import base_response

add_subscription_response = {
    **base_response,
    201: {"description": "Подписка успешно оформлена"},
    409: {"description": "Ошибка оформления подписки"},
}

get_subscription_response = {
    **base_response,
    200: {"description": "Информация о подписке", "model": GetUserSubscriptionDTO},
    404: {"description": "Подписка не найдена"},
    403: {"description": "Нет доступа к подписке"},
}

get_tariffs_response = {
    **base_response,
    200: {
        "description": "Список тарифов",
        "model": list[TariffDTO],
    },
    404: {"description": "Нет доступных тарифов"},
}
