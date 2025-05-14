from fastapi import APIRouter, Depends, status, Response

from api.auth.auth_bearer import JWTHeader, JWTBearer
from modules.users import (
    UserInfoDTO,
    get_user_info_description,
    get_user_info_response,
    create_or_update_fcm_token_description,
    create_or_update_fcm_token_response,
    UpdateFCMTokenDTO,
    UpdateFCMTokenWithUserIdDTO,
)
from modules.users.enum import GetUserInfoEnum
from services.fcm_token_service import FCMTokenService
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
            status_code=status.HTTP_401_UNAUTHORIZED, content="Пользователь не найден"
        )
    if result == GetUserInfoEnum.NOT_SUBSCRIBED:
        return Response(
            status_code=status.HTTP_409_CONFLICT, content="У пользователя нет подписки"
        )
    return result


@router.post(
    "/fcm-update",
    summary="Обновление или создание FCM токена",
    description=create_or_update_fcm_token_description,
    status_code=status.HTTP_200_OK,
    responses=create_or_update_fcm_token_response,
)
async def create_or_update_fcm_token(
    fcm_token_dto: UpdateFCMTokenDTO,
    fcm_token_service: FCMTokenService = Depends(FCMTokenService),
    token: JWTHeader = Depends(JWTBearer()),
):
    await fcm_token_service.update_or_create_fcm_token_service(
        UpdateFCMTokenWithUserIdDTO(**fcm_token_dto.model_dump(), user_id=token.user_id)
    )
    return Response(status_code=status.HTTP_200_OK, content="FCM токен обновлён")
