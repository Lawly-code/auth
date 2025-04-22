from fastapi import APIRouter, Depends, Response, status
from modules.auth import (
    AuthTokenResponseDTO,
    LoginUserDTO,
    LoginUserWithIPDTO,
    RegisterUserDTO,
    RegisterUserWithIPDTO,
    login_response,
    login_user_description,
    logout_response,
    logout_user_description,
    register_response,
    register_user_description,
)
from modules.auth.descriptions import refresh_token_description
from modules.auth.dto import (
    LogoutDTO,
    RefreshTokenModelDTO,
    RefreshTokenWithIPModelDTO,
    TokenModelDTO,
)
from modules.auth.response import refresh_token_response
from services.auth_service import AuthService
from services.services import auth_service_getter, ip_address_getter

router = APIRouter(tags=["Авторизация"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description=register_user_description,
    responses=register_response,
    response_model=AuthTokenResponseDTO,
)
async def register(
    register_user: RegisterUserDTO,
    auth_service: AuthService = Depends(auth_service_getter),
    ip_address: str = Depends(ip_address_getter),
):
    result = await auth_service.register(
        register_user=RegisterUserWithIPDTO(ip=ip_address, **register_user.model_dump())
    )
    if not result:
        return Response(
            status_code=status.HTTP_409_CONFLICT,
            content="Пользователь с таким email уже существует",
        )
    return result


@router.post(
    "/login",
    response_model=AuthTokenResponseDTO,
    summary="Авторизация пользователя",
    description=login_user_description,
    responses=login_response,
)
async def login(
    login_user_dto: LoginUserDTO,
    auth_service: AuthService = Depends(auth_service_getter),
    ip_address: str = Depends(ip_address_getter),
):
    result = await auth_service.login(
        login_user=LoginUserWithIPDTO(ip=ip_address, **login_user_dto.model_dump())
    )
    if not result:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Неверный логин или пароль",
        )
    return result


@router.post(
    "/refresh-tokens",
    response_model=TokenModelDTO,
    summary="Обновление токенов",
    description=refresh_token_description,
    responses=refresh_token_response,
)
async def refresh_tokens(
    refresh: RefreshTokenModelDTO,
    auth_service: AuthService = Depends(auth_service_getter),
    ip_address: str = Depends(ip_address_getter),
):
    result = await auth_service.refresh_tokens(
        refresh=RefreshTokenWithIPModelDTO(ip=ip_address, **refresh.model_dump())
    )
    if not result:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
            content="Неверные учетные данные",
        )
    return result


@router.post(
    "/logout",
    summary="Выход пользователя",
    description=logout_user_description,
    responses=logout_response,
    status_code=status.HTTP_202_ACCEPTED,
)
async def logout(
    logout_dto: LogoutDTO, auth_service: AuthService = Depends(auth_service_getter)
):
    result = await auth_service.logout(logout_dto=logout_dto)
    if not result:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Сессия не найдена",
        )
    return Response(
        status_code=status.HTTP_202_ACCEPTED,
        content="Выход из системы выполнен",
    )
