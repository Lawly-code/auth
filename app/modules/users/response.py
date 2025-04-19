from modules.users import UserSubscriptionDTO
from shared import base_response

get_subscription_response = {
    **base_response,
    200: {"description": "Данные о подписке", "model": UserSubscriptionDTO},
    404: {"description": "Подписка не найдена"},
}

get_user_info_response = {
    **base_response,
    200: {"description": "Данные пользователя", "model": UserSubscriptionDTO}
}