from modules.subscribes import UserSubscriptionDTO
from shared import base_response

add_subscription_response = {
    **base_response,
    200: {"description": "Подписка успешно оформлена", "model": UserSubscriptionDTO},
}

get_tariffs_response = {
    **base_response,
    200: {
        "description": "Список тарифов",
        "model": list[UserSubscriptionDTO],
    },
}
