from datetime import datetime, timedelta

from lawly_db.db_models import Tariff, Subscribe
from protos.user_service.client import UserServiceClient
from sqlalchemy.ext.asyncio import AsyncSession

from dto import RegisterDTO


async def test_user_get_info(
    user_grpc_client: UserServiceClient,
    register_dto: RegisterDTO,
    session: AsyncSession,
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

    response = await user_grpc_client.get_user_info(register_dto.user.id)
    assert response.user_id == register_dto.user.id
