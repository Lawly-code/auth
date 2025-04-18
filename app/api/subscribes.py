from typing import List

from fastapi import APIRouter, Depends
from lawly_db.db_models.db_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from descriptions.user import subscription_form
from models.dto import UserSubscriptionDTO, InfoModelDto, TariffDTO

router = APIRouter()


@router.post(
    "/subscribe/{tariff_id}",
    summary="Оформление подписки",
    description=subscription_form,
    response_model=UserSubscriptionDTO,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Подписка успешно оформлена", "model": UserSubscriptionDTO},
        400: {"description": "Некорректный запрос", "model": InfoModelDto},
        401: {"description": "Не авторизован", "model": InfoModelDto},
    }
)
async def subscribe_to_tariff(
        tariff_id: int,
        session: AsyncSession = Depends(get_session),
):
    pass


@router.get(
    "/tariffs",
    summary="Получение списка доступных тарифов",
    description="Получение информации о всех доступных тарифных планах",
    tags=["Подписки"],
    response_model=List[TariffDTO],
    responses={
        200: {"description": "Список тарифов", "model": List[TariffDTO]}
    }
)
async def get_available_tariffs(
        session: AsyncSession = Depends(get_session)
):
    pass
