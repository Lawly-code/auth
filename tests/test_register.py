from httpx import AsyncClient
from lawly_db.db_models import User, Tariff
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def test_register(ac: AsyncClient, session: AsyncSession):
    tariff = Tariff(
        name="Базовый",
        description="Базовый тариф",
        price=0,
        consultations_count=0,
        ai_access=False,
        is_base=True,
        custom_templates=False,
        unlimited_docs=False,
    )
    session.add(tariff)
    await session.commit()
    resp_register = await ac.post(
        "/api/v1/register",
        json={
            "email": "test_mail@gmail.com",
            "name": "Николай Телешов",
            "password": "super_secret_password",
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
    user = await session.execute(
        select(User).where(User.email == "test_mail@gmail.com")
    )
    await session.delete(tariff)
    await session.commit()
    await session.delete(user.scalar_one())
    await session.commit()


async def test_register_with_wrong_email(ac: AsyncClient, session: AsyncSession):
    resp_register = await ac.post(
        "/api/v1/register",
        json={
            "email": "test_mail",
            "name": "Николай Телешов",
            "password": "super_secret_password",
            "device_id": "4965483F-2297-4FAF-AD26-D6F2BA888684",
            "device_os": "android 13",
            "device_name": "samsung s23",
            "agree_to_terms": True,
        },
    )
    assert resp_register.status_code == 422


async def test_register_with_wrong_device_id(ac: AsyncClient, session: AsyncSession):
    resp_register = await ac.post(
        "/api/v1/register",
        json={
            "email": "test_mail@gmail.com",
            "name": "Николай Телешов",
            "password": "super_secret_password",
            "device_id": "4965483F-2297-4FAF-AD26",
            "device_os": "android 13",
            "device_name": "samsung s23",
            "agree_to_terms": True,
        },
    )
    assert resp_register.status_code == 422


async def test_register_with_wrong_device_os(ac: AsyncClient, session: AsyncSession):
    resp_register = await ac.post(
        "/api/v1/register",
        json={
            "email": "test_mail@gmail.com",
            "name": "Николай Телешов",
            "password": "super_secret_password",
            "device_id": "4965483F-2297-4FAF-AD26",
            "device_os": "banana-os 13",
            "device_name": "samsung s23",
            "agree_to_terms": True,
        },
    )
    assert resp_register.status_code == 422


async def test_re_register(ac: AsyncClient, session: AsyncSession):
    tariff = Tariff(
        name="Базовый",
        description="Базовый тариф",
        price=0,
        consultations_count=0,
        ai_access=False,
        is_base=True,
        custom_templates=False,
        unlimited_docs=False,
    )
    session.add(tariff)
    await session.commit()

    resp_register = await ac.post(
        "/api/v1/register",
        json={
            "email": "test_mail@gmail.com",
            "name": "Николай Телешов",
            "password": "super_secret_password",
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

    resp_re_register = await ac.post(
        "/api/v1/register",
        json={
            "email": "test_mail@gmail.com",
            "name": "Николай Телешов",
            "password": "super_secret_password",
            "device_id": "4965483F-2297-4FAF-AD26-D6F2BA888684",
            "device_os": "android 13",
            "device_name": "samsung s23",
            "agree_to_terms": True,
        },
    )
    assert resp_re_register.status_code == 409
    await session.delete(tariff)
    await session.commit()
    user = await session.execute(
        select(User).where(User.email == "test_mail@gmail.com")
    )
    await session.delete(user.scalar_one())
    await session.commit()
