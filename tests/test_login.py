from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from dto import RegisterDTO


async def test_login(ac: AsyncClient, register_dto: RegisterDTO, session: AsyncSession):
    resp_login = await ac.post(
        "/api/v1/login",
        json={
            "email": register_dto.user.email,
            "password": "super_secret_password",
            "device_id": register_dto.refresh_session.device_id,
            "device_os": register_dto.refresh_session.device_os,
            "device_name": register_dto.refresh_session.device_name,
        },
    )
    assert resp_login.status_code == 200
    response_json = resp_login.json()
    assert "access_token" in response_json
    assert "refresh_token" in response_json


async def test_login_with_not_valide_email(ac: AsyncClient, session: AsyncSession):
    resp_login = await ac.post(
        "/api/v1/login",
        json={
            "email": "test_mail",
            "password": "super_secret_password",
            "device_id": "4965483F-2297-4FAF-AD26-D6F2BA888684",
            "device_os": "android 13",
            "device_name": "samsung s23",
        },
    )
    assert resp_login.status_code == 422


async def test_login_with_wrong_device_id(ac: AsyncClient, session: AsyncSession):
    resp_login = await ac.post(
        "/api/v1/login",
        json={
            "email": "test_mail@gmail.com",
            "password": "super_secret_password",
            "device_id": "4965483F-2297-4FAF-AD26",
            "device_os": "android 13",
            "device_name": "samsung s23",
        },
    )
    assert resp_login.status_code == 422


async def test_login_with_wrong_email(
    ac: AsyncClient, register_dto: RegisterDTO, session: AsyncSession
):
    resp_login = await ac.post(
        "/api/v1/login",
        json={
            "email": "not_test_mail@gmail.com",
            "password": "super_secret_password",
            "device_id": register_dto.refresh_session.device_id,
            "device_os": register_dto.refresh_session.device_os,
            "device_name": register_dto.refresh_session.device_name,
        },
    )
    assert resp_login.status_code == 401


async def test_login_with_wrong_password(
    ac: AsyncClient, register_dto: RegisterDTO, session: AsyncSession
):
    resp_login = await ac.post(
        "/api/v1/login",
        json={
            "email": register_dto.user.email,
            "password": "not_super_secret_password",
            "device_id": register_dto.refresh_session.device_id,
            "device_os": register_dto.refresh_session.device_os,
            "device_name": register_dto.refresh_session.device_name,
        },
    )
    assert resp_login.status_code == 401


async def test_login_with_not_valid_password(
    ac: AsyncClient, register_dto: RegisterDTO, session: AsyncSession
):
    resp_login = await ac.post(
        "/api/v1/login",
        json={
            "email": register_dto.user.email,
            "password": "коля1234",
            "device_id": register_dto.refresh_session.device_id,
            "device_os": register_dto.refresh_session.device_os,
            "device_name": register_dto.refresh_session.device_name,
        },
    )
    assert resp_login.status_code == 422
