from fastapi import APIRouter, Depends, status
from lawly_db.db_models.db_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from modules.users import get_user_info_description, subscription_form_description, get_subscription_response, UserDTO, \
    UserSubscriptionDTO, get_user_info_response

router = APIRouter(tags=["Пользователи"])


@router.get(
    "/user",
    summary="Получение информации о текущем пользователе",
    description=get_user_info_description,
    response_model=UserDTO,
    responses=get_user_info_response
)
async def get_current_user_info(
        session: AsyncSession = Depends(get_session)
):
    pass


@router.get(
    "/user/subscription",
    summary="Получение информации о подписке пользователя",
    description=subscription_form_description,
    response_model=UserSubscriptionDTO,
    responses=get_subscription_response
)
async def get_user_subscription_info(session: AsyncSession = Depends(get_session)):
    pass
