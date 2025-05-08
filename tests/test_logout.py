from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.auth_handler import sign_jwt
from dto import RegisterDTO


async def test_logout(
    ac: AsyncClient, register_dto: RegisterDTO, session: AsyncSession
):
    resp_login = await ac.post(
        "/api/v1/logout",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        json={
            "refresh_token": str(register_dto.refresh_session.refresh_token),
            "device_id": register_dto.refresh_session.device_id,
        },
    )

    assert resp_login.status_code == 202
    refresh_login = await ac.post(
        "/api/v1/refresh-tokens",
        json={
            "refresh_token": str(register_dto.refresh_session.refresh_token),
            "device_name": register_dto.refresh_session.device_name,
            "device_os": register_dto.refresh_session.device_os,
            "device_id": register_dto.refresh_session.device_id,
            "user_id": register_dto.user.id,
        },
    )
    assert refresh_login.status_code == 401


async def test_logout_with_invalid_device_id(
    ac: AsyncClient, register_dto: RegisterDTO
):
    resp_login = await ac.post(
        "/api/v1/logout",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        json={
            "refresh_token": str(register_dto.refresh_session.refresh_token),
            "device_name": register_dto.refresh_session.device_name,
            "device_os": register_dto.refresh_session.device_os,
            "device_id": "4965483F-2297-4FAF----",
        },
    )
    assert resp_login.status_code == 422


async def test_logout_with_not_match_token(ac: AsyncClient, register_dto: RegisterDTO):
    resp_login = await ac.post(
        "/api/v1/logout",
        json={
            "refresh_token": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "device_name": register_dto.refresh_session.device_name,
            "device_os": register_dto.refresh_session.device_os,
            "device_id": register_dto.refresh_session.device_id,
        },
    )
    assert resp_login.status_code == 401


async def test_logout_with_not_match_device_id(
    ac: AsyncClient, register_dto: RegisterDTO
):
    resp_login = await ac.post(
        "/api/v1/logout",
        json={
            "refresh_token": str(register_dto.refresh_session.refresh_token),
            "device_name": register_dto.refresh_session.device_name,
            "device_os": register_dto.refresh_session.device_os,
            "device_id": "4965483F-2297-4FAF-AD26-D6F2BA888888",
        },
    )
    assert resp_login.status_code == 401
