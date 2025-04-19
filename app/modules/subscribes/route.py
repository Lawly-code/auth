from fastapi import APIRouter, Depends, status
from lawly_db.db_models.db_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from modules.subscribes import add_subscription_response, UserSubscriptionDTO, TariffDTO, get_tariffs_response, \
    tariffs_description, user_subscribe_description

router = APIRouter(tags=["Подписки"])


@router.post(
    "/subscribe/{tariff_id}",
    summary="Оформление подписки",
    description=user_subscribe_description,
    response_model=UserSubscriptionDTO,
    status_code=status.HTTP_200_OK,
    responses=add_subscription_response
)
async def subscribe_to_tariff(
        tariff_id: int,
        session: AsyncSession = Depends(get_session),
):
    pass


@router.get(
    "/tariffs",
    summary="Получение списка доступных тарифов",
    description=tariffs_description,
    response_model=list[TariffDTO],
    responses=get_tariffs_response
)
async def get_available_tariffs(
        session: AsyncSession = Depends(get_session)
):
    pass
