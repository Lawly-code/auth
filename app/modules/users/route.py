from fastapi import APIRouter, Depends, status, Response

from api.auth.auth_bearer import JWTHeader, JWTBearer
from modules.users import (
    UserInfoDTO,
    get_user_info_description,
    get_user_info_response,
)
from modules.users.enum import GetUserInfoEnum
from services.user_service import UserService

router = APIRouter(tags=["Пользователи"])


@router.get(
    "/user",
    summary="Получение информации о текущем пользователе",
    description=get_user_info_description,
    status_code=status.HTTP_200_OK,
    response_model=UserInfoDTO,
    responses=get_user_info_response,
)
async def get_current_user_info(
    user_service: UserService = Depends(UserService),
    token: JWTHeader = Depends(JWTBearer()),
):
    result = await user_service.get_user_info_service(user_id=token.user_id)
    if result == GetUserInfoEnum.ACCESS_DENIED:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN, content="Пользователь не найден"
        )
    if result == GetUserInfoEnum.NOT_SUBSCRIBED:
        return Response(
            status_code=status.HTTP_409_CONFLICT, content="У пользователя нет подписки"
        )
    return result
