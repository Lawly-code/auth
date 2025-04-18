from fastapi import APIRouter
from lawly_db.db_models.db_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from starlette import status

from descriptions.auth import register_user, login_user, logout_user
from models.dto import RegisterUserDTO, InfoModelDto, LoginUserDTO

router = APIRouter()


@router.post(
    "/register",
    response_model=RegisterUserDTO,
    summary="Регистрация пользователя",
    description=register_user,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Пользователь успешно зарегистрирован", "model": RegisterUserDTO},
        400: {"description": "Ошибка валидации данных", "model": InfoModelDto},
        409: {"description": "Пользователь с таким email уже существует", "model": InfoModelDto},
    }
)
async def register(session: AsyncSession = Depends(get_session)):
    pass


@router.post(
    "/login",
    response_model=LoginUserDTO,
    summary="Авторизация пользователя",
    description=login_user,
    responses={
        200: {"description": "Успешная аутентификация", "model": LoginUserDTO},
        401: {"description": "Неверные учетные данные", "model": InfoModelDto},
    }
)
async def login(session: AsyncSession = Depends(get_session)):
    pass


@router.post(
    "/logout",
    response_model=InfoModelDto,
    summary="Выход пользователя",
    description=logout_user,
    responses={
        200: {"description": "Успешный выход из системы", "model": InfoModelDto},
        401: {"description": "Не авторизован", "model": InfoModelDto},
    }
)
async def logout(session: AsyncSession = Depends(get_session)):
    pass
