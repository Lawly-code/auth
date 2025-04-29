import random
import string
import uuid

from httpx import AsyncClient
from lawly_db.db_models import User, RefreshSession
from sqlalchemy.ext.asyncio import AsyncSession

from dto import RegisterDTO
from repositories.cipher_repository import CipherRepository


async def test_refresh_tokens(
    ac: AsyncClient, register_dto: RegisterDTO, session: AsyncSession
):
    resp_refresh = await ac.post(
        "/api/v1/refresh-tokens",
        json={
            "refresh_token": str(register_dto.refresh_session.refresh_token),
            "device_id": register_dto.refresh_session.device_id,
            "device_os": register_dto.refresh_session.device_os,
            "device_name": register_dto.refresh_session.device_name,
            "user_id": register_dto.user.id,
        },
    )
    assert resp_refresh.status_code == 200
    data = resp_refresh.json()
    assert data.get("access_token") is not None
    assert data.get("refresh_token") is not None


async def test_refresh_tokens_with_invalid_device_id(
    ac: AsyncClient, register_dto: RegisterDTO
):
    resp_refresh = await ac.post(
        "/api/v1/refresh-tokens",
        json={
            "refresh_token": str(register_dto.refresh_session.refresh_token),
            "device_id": "4965483F-2297-4FAF-AD26",
            "device_os": "android 13",
            "device_name": "samsung s23",
        },
    )
    assert resp_refresh.status_code == 422


async def test_refresh_tokens_with_run_out_time(ac: AsyncClient, session: AsyncSession):
    cipher_repository = CipherRepository()

    user = User(
        email="".join(
            [random.choice(string.ascii_letters + string.digits) for _ in range(5)]
        )
        + "@gmail.com",
        password=cipher_repository.hash_password("super_secret_password"),
        name="Николай Телешов",
    )
    session.add(user)
    await session.commit()
    refresh_session = RefreshSession(
        user_id=user.id,
        refresh_token=uuid.uuid4(),
        ip="78.123.321.121",
        device_os="android 13",
        device_name="samsung s23",
        device_id="4965483F-2297-4FAF-AD26-D6F2BA888684",
        expires_in=12345678,
    )
    session.add(refresh_session)
    await session.commit()
    resp_refresh = await ac.post(
        "/api/v1/refresh-tokens",
        json={
            "refresh_token": str(refresh_session.refresh_token),
            "device_id": refresh_session.device_id,
            "device_os": refresh_session.device_os,
            "device_name": refresh_session.device_name,
            "user_id": user.id,
        },
    )
    assert resp_refresh.status_code == 403
    await session.delete(user)
    await session.commit()
