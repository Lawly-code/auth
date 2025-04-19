from lawly_db.db_models.db_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from modules.auth import login_response, register_response, logout_response, RegisterUserDTO, LoginUserDTO, \
    register_user_description, login_user_description, logout_user_description

router = APIRouter(tags=["Авторизация"])


@router.post(
    "/register",
    response_model=RegisterUserDTO,
    summary="Регистрация пользователя",
    description=register_user_description,
    status_code=status.HTTP_201_CREATED,
    responses=register_response
)
async def register(session: AsyncSession = Depends(get_session)):
    pass


@router.post(
    "/login",
    response_model=LoginUserDTO,
    summary="Авторизация пользователя",
    description=login_user_description,
    responses=login_response
)
async def login(session: AsyncSession = Depends(get_session)):
    pass


@router.post(
    "/logout",
    summary="Выход пользователя",
    description=logout_user_description,
    responses=logout_response,
    status_code=status.HTTP_202_ACCEPTED
)
async def logout(session: AsyncSession = Depends(get_session)):
    pass
