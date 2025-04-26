from datetime import datetime

from lawly_db.db_models import Subscribe
from sqlalchemy import select

from repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class SubscribeRepository(BaseRepository):
    model = Subscribe

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_user_subscription(self, user_id: int) -> model | None:
        """
        Получение информации о подписке
        :param user_id: ID пользователя
        :return: Подписка
        """
        query = select(self.model).where(
            self.model.user_id == user_id, self.model.end_date >= datetime.now()
        )
        _ = await self.session.execute(query)
        return _.scalar()

    async def check_user_subscription(self, user_id: int) -> model | None:
        """
        Проверка подписки пользователя
        :param user_id: ID пользователя
        :return: Подписка
        """
        query = select(self.model).where(
            self.model.user_id == user_id, self.model.end_date >= datetime.now()
        )
        _ = await self.session.execute(query)
        return _.scalar()

    async def get_actual_subscribe_by_user_id(self, user_id: int) -> model | None:
        """
        Получение актуальной подписки пользователя
        :param user_id: ID пользователя
        :return: Подписка
        """
        query = select(self.model).where(
            self.model.user_id == user_id, self.model.end_date >= datetime.now()
        )
        _ = await self.session.execute(query)
        return _.scalar()
