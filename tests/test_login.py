from httpx import AsyncClient
from lawly_db.db_models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def test_register_login_logout(ac: AsyncClient, session: AsyncSession):
    resp_register = await ac.post(
        "/api/v1/register",
        json={
            "email": "test_mail@gmail.com",
            "name": "Николай Телешов",
            "password": "суперсекретный_пароль",
            "device_id": "4965483F-2297-4FAF-AD26-D6F2BA888684",
            "device_os": "android 13",
            "device_name": "samsung s23",
            "agree_to_terms": True,
        },
    )
    assert resp_register.status_code == 200
    response_json = resp_register.json()
    assert "access_token" in response_json
    assert "refresh_token" in response_json

    resp_login = await ac.post(
        "/api/v1/login",
        json={
            "email": "test_mail@gmail.com",
            "password": "суперсекретный_пароль",
            "device_id": "4965483F-2297-4FAF-AD26-D6F2BA888684",
            "device_os": "android 13",
            "device_name": "samsung s23",
        },
    )
    assert resp_login.status_code == 200
    response_json = resp_login.json()
    assert "access_token" in response_json
    assert "refresh_token" in response_json

    resp_refresh_tokens = await ac.post(
        "/api/v1/refresh-tokens",
        json={
            "device_id": "4965483F-2297-4FAF-AD26-D6F2BA888684",
            "device_os": "android 13",
            "device_name": "samsung s23",
            "refresh_token": response_json["refresh_token"],
        },
    )
    assert resp_refresh_tokens.status_code == 200
    response_json = resp_refresh_tokens.json()
    assert "access_token" in response_json
    assert "refresh_token" in response_json

    resp_logout = await ac.post(
        "/api/v1/logout",
        json={
            "device_id": "4965483F-2297-4FAF-AD26-D6F2BA888684",
            "refresh_token": response_json["refresh_token"],
        },
    )
    assert resp_logout.status_code == 202

    user = await session.execute(
        select(User).where(User.email == "test_mail@gmail.com")
    )
    await session.delete(user.scalar_one())
    await session.commit()
