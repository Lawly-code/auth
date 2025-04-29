from fastapi import Depends
from lawly_db.db_models.db_session import get_session

from sqlalchemy.ext.asyncio import AsyncSession

from modules.users import UserInfoDTO, TariffDTO
from modules.users.enum import GetUserInfoEnum
from repositories.subscribe_repository import SubscribeRepository
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.user_repo = UserRepository(session)
        self.subscribe_repo = SubscribeRepository(session)

    async def get_user_info_service(
        self, user_id: int
    ) -> UserInfoDTO | GetUserInfoEnum:
        user = await self.user_repo.get_user_by_id(user_id, self.session)
        if not user:
            return GetUserInfoEnum.ACCESS_DENIED
        subscribe = await self.subscribe_repo.get_actual_subscribe_by_user_id(
            user_id=user.id
        )
        if not subscribe:
            return GetUserInfoEnum.NOT_SUBSCRIBED
        return UserInfoDTO(
            user_id=user.id,
            tariff=TariffDTO.model_validate(subscribe.tariff, from_attributes=True),
            start_date=subscribe.start_date,
            end_date=subscribe.end_date,
        )
