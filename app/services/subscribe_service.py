import datetime

from fastapi import Depends
from lawly_db.db_models import Subscribe
from lawly_db.db_models.db_session import get_session

from modules.subscribes.dto import (
    SubscriptionWithUserIdDTO,
    GetUserSubscriptionWithUserIdDTO,
)
from modules.subscribes.enum import GetSubscribesEnum, SubscribeStatusEnum
from modules.users.dto import TariffDTO
from repositories.subscribe_repository import SubscribeRepository
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.tariff_repository import TariffRepository


class SubscribeService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.subscribe_repo = SubscribeRepository(session)
        self.tariff_repo = TariffRepository(session)

    async def subscribe_to_tariff_service(
        self, subscribe_dto: SubscriptionWithUserIdDTO
    ) -> SubscribeStatusEnum:
        if await self.subscribe_repo.check_user_subscription(
            user_id=subscribe_dto.user_id
        ):
            return SubscribeStatusEnum.ALREADY_SUBSCRIBED
        tariff = await self.tariff_repo.get_tariff_by_id(subscribe_dto.tariff_id)
        if not tariff:
            return SubscribeStatusEnum.INVALID_TARIFF_ID

        subscribe = Subscribe(
            user_id=subscribe_dto.user_id,
            tariff_id=tariff.id,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
            consultations_total=tariff.consultations_count,
            can_user_ai=tariff.ai_access,
            can_create_custom_templates=tariff.custom_templates,
            unlimited_documents=tariff.unlimited_docs,
        )
        await self.subscribe_repo.save(entity=subscribe, session=self.session)
        return SubscribeStatusEnum.SUCCESS

    async def get_user_subscription_service(
        self, user_id: int
    ) -> GetUserSubscriptionWithUserIdDTO | GetSubscribesEnum:
        subscription = await self.subscribe_repo.get_user_subscription(user_id=user_id)
        if not subscription:
            return GetSubscribesEnum.NOT_FOUND
        if subscription.user_id != user_id:
            return GetSubscribesEnum.ACCESS_DENIED
        return GetUserSubscriptionWithUserIdDTO.model_validate(subscription)

    async def get_all_tariffs_service(self) -> list[TariffDTO] | None:
        tariffs = await self.tariff_repo.get_all_tariffs()
        if not tariffs:
            return None
        return [
            TariffDTO.model_validate(tariff, from_attributes=True) for tariff in tariffs
        ]
