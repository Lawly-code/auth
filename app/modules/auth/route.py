from fastapi import APIRouter, Depends, Response, status

from api.auth.auth_bearer import JWTHeader, JWTBearer
from modules.auth import (
    AuthTokenResponseDTO,
    LoginUserDTO,
    RegisterUserDTO,
    RegisterUserWithIPDTO,
    login_response,
    login_user_description,
    logout_response,
    logout_user_description,
    register_response,
    register_user_description,
    refresh_token_description,
    login_lawyer_description,
    LoginLawyerWithIPDTO,
    LoginLawyerDTO,
    TokenModelDTO,
    RefreshTokenModelDTO,
    RefreshTokenWithIPModelDTO,
    LogoutDTO,
    LogoutWithUserIDDTO,
    RefreshTokenLawyerModelDTO,
    RefreshTokenLawyerWithIPModelDTO,
    LogoutLawyerWithUserIDDTO,
    LogoutLawyerDTO,
    LoginUserWithIPDTO,
)
from modules.auth.response import refresh_token_response
from services.auth_service import AuthService
from shared.utils import ip_address_getter

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
    auth_service: AuthService = Depends(AuthService),
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
    auth_service: AuthService = Depends(AuthService),
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
    "/login-lawyer",
    response_model=AuthTokenResponseDTO,
    summary="Авторизация юриста",
    description=login_lawyer_description,
    responses=login_response,
)
async def login_lawyer(
    login_lawyer_dto: LoginLawyerDTO,
    auth_service: AuthService = Depends(AuthService),
    ip_address: str = Depends(ip_address_getter),
):
    result = await auth_service.login_lawyer(
        login_lawyer=LoginLawyerWithIPDTO(
            ip=ip_address, **login_lawyer_dto.model_dump()
        )
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
    auth_service: AuthService = Depends(AuthService),
    ip_address: str = Depends(ip_address_getter),
):
    result = await auth_service.refresh_tokens(
        refresh=RefreshTokenWithIPModelDTO(ip=ip_address, **refresh.model_dump())
    )
    if not result:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Неверные учетные данные",
        )
    return result


@router.post(
    "/refresh-tokens-lawyer",
    response_model=TokenModelDTO,
    summary="Обновление токенов юриста",
    description=refresh_token_description,
    responses=refresh_token_response,
)
async def refresh_tokens_lawyer(
    refresh: RefreshTokenLawyerModelDTO,
    auth_service: AuthService = Depends(AuthService),
    ip_address: str = Depends(ip_address_getter),
):
    result = await auth_service.refresh_tokens_lawyer(
        refresh_lawyer=RefreshTokenLawyerWithIPModelDTO(
            ip=ip_address, **refresh.model_dump()
        )
    )
    if not result:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
    logout_dto: LogoutDTO,
    auth_service: AuthService = Depends(AuthService),
    token: JWTHeader = Depends(JWTBearer()),
):
    result = await auth_service.logout(
        logout_dto=LogoutWithUserIDDTO(user_id=token.user_id, **logout_dto.model_dump())
    )
    if not result:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED, content="Неверные учетные данные"
        )
    return Response(
        status_code=status.HTTP_202_ACCEPTED, content="Выход из системы выполнен"
    )


@router.post(
    "/logout-lawyer",
    summary="Выход юриста",
    description=logout_user_description,
    responses=logout_response,
    status_code=status.HTTP_202_ACCEPTED,
)
async def logout_lawyer(
    logout_dto: LogoutLawyerDTO,
    auth_service: AuthService = Depends(AuthService),
    token: JWTHeader = Depends(JWTBearer()),
):
    result = await auth_service.logout_lawyer(
        logout_lawyer=LogoutLawyerWithUserIDDTO(
            user_id=token.user_id, **logout_dto.model_dump()
        )
    )
    if not result:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED, content="Неверные учетные данные"
        )
    return Response(
        status_code=status.HTTP_202_ACCEPTED, content="Выход из системы выполнен"
    )
