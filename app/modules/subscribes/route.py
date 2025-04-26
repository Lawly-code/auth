from fastapi import APIRouter, Depends, status, Response

from api.auth.auth_bearer import JWTHeader, JWTBearer
from modules.subscribes import (
    TariffDTO,
    add_subscription_response,
    get_tariffs_response,
    tariffs_description,
    user_subscribe_description,
)

from modules.subscribes.dto import SubscriptionDTO, SubscriptionWithUserIdDTO
from modules.subscribes.enum import GetSubscribesEnum, SubscribeStatusEnum
from modules.subscribes.response import get_subscription_response
from services.subscribe_service import SubscribeService

router = APIRouter(tags=["Подписки"])


@router.post(
    "/subscribe",
    summary="Оформление подписки",
    description=user_subscribe_description,
    status_code=status.HTTP_201_CREATED,
    responses=add_subscription_response,
)
async def subscribe_to_tariff(
    subscribe: SubscriptionDTO,
    subscribe_service: SubscribeService = Depends(SubscribeService),
    token: JWTHeader = Depends(JWTBearer()),
):
    """
    Оформление подписки на тариф
    """
    result = await subscribe_service.subscribe_to_tariff_service(
        subscribe_dto=SubscriptionWithUserIdDTO(
            **subscribe.model_dump(), user_id=token.user_id
        ),
    )
    if result == SubscribeStatusEnum.INVALID_TARIFF_ID:
        return Response(
            status_code=status.HTTP_409_CONFLICT, content="Некорректный ID тарифа"
        )
    if result == SubscribeStatusEnum.SUCCESS:
        return Response(
            status_code=status.HTTP_201_CREATED, content="Подписка оформлена"
        )
    if result == SubscribeStatusEnum.ALREADY_SUBSCRIBED:
        return Response(
            status_code=status.HTTP_409_CONFLICT,
            content="Уже оформлена подписка на тариф",
        )


@router.get(
    "/subscribe",
    summary="Получение информации о подписке у текущего пользователя",
    description=user_subscribe_description,
    status_code=status.HTTP_200_OK,
    responses=get_subscription_response,
)
async def get_user_subscription(
    subscribe_service: SubscribeService = Depends(SubscribeService),
    token: JWTHeader = Depends(JWTBearer()),
):
    """
    Получение информации о подписке
    """
    subscription = await subscribe_service.get_user_subscription_service(
        user_id=token.user_id
    )
    if subscription == GetSubscribesEnum.NOT_FOUND:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="Подписка не найдена"
        )
    if subscription == GetSubscribesEnum.ACCESS_DENIED:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN, content="Нет доступа к подписке"
        )

    return subscription


@router.get(
    "/tariffs",
    summary="Получение списка доступных тарифов",
    description=tariffs_description,
    response_model=list[TariffDTO],
    status_code=status.HTTP_200_OK,
    responses=get_tariffs_response,
)
async def get_available_tariffs(
    subscribe_service: SubscribeService = Depends(SubscribeService),
):
    """
    Получение списка доступных тарифов
    """
    result = await subscribe_service.get_all_tariffs_service()
    if not result:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="Нет доступных тарифов"
        )
    return await subscribe_service.get_all_tariffs_service()
