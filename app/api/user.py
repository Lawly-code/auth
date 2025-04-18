from fastapi import APIRouter, Depends
from lawly_db.db_models.db_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from descriptions.user import subscription_form, get_user_info, user_subscription
from models.dto import UserDTO, InfoModelDto, UserSubscriptionDTO

router = APIRouter()


@router.get(
    "/user",
    summary="Получение информации о текущем пользователе",
    description=get_user_info,
    response_model=UserDTO,
    responses={
        200: {"description": "Данные пользователя", "model": UserDTO},
        401: {"description": "Не авторизован", "model": InfoModelDto}
    }
)
async def get_current_user_info(
        session: AsyncSession = Depends(get_session)
):
    pass


@router.get(
    "/user/subscription",
    summary="Получение информации о подписке пользователя",
    description=user_subscription,
    response_model=UserSubscriptionDTO,
    responses={
        200: {"description": "Данные о подписке", "model": UserSubscriptionDTO},
        401: {"description": "Не авторизован", "model": InfoModelDto},
        404: {"description": "Подписка не найдена", "model": InfoModelDto},
    }
)
async def get_user_subscription_info(session: AsyncSession = Depends(get_session)):
    pass
