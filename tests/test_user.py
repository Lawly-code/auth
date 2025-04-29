from datetime import datetime, timedelta

from httpx import AsyncClient
from lawly_db.db_models import Tariff, Subscribe
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.auth_handler import sign_jwt
from dto import RegisterDTO


async def test_get_user_subscription(
    ac: AsyncClient, register_dto: RegisterDTO, session: AsyncSession
):
    tariff = Tariff(
        name="test",
        description="test description",
        features=["test 1", "test 2"],
        price=100,
        consultations_count=2,
        ai_access=True,
        custom_templates=True,
        unlimited_docs=True,
    )
    session.add(tariff)
    await session.commit()
    subscribe = Subscribe(
        user_id=register_dto.user.id,
        tariff_id=tariff.id,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        count_lawyers=tariff.consultations_count,
        consultations_total=tariff.consultations_count,
        consultations_used=0,
        can_user_ai=tariff.ai_access,
        can_create_custom_templates=tariff.custom_templates,
        unlimited_documents=tariff.unlimited_docs,
    )
    session.add(subscribe)
    await session.commit()

    resp_get_subscription = await ac.get(
        "/api/v1/user",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
    )
    assert resp_get_subscription.status_code == 200
    response_json = resp_get_subscription.json()
    assert "user_id" in response_json
    assert "tariff" in response_json
    assert "start_date" in response_json
    assert "end_date" in response_json
    await session.delete(subscribe)
    await session.delete(tariff)
    await session.commit()


async def test_get_user_subscription_without_not_subscription(
    ac: AsyncClient, register_dto: RegisterDTO, session: AsyncSession
):
    resp_get_subscription = await ac.get(
        "/api/v1/user",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
    )
    assert resp_get_subscription.status_code == 409
