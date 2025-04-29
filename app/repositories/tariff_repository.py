from lawly_db.db_models import Tariff
from sqlalchemy import select

from repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class TariffRepository(BaseRepository):
    model = Tariff

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all_tariffs(self) -> list[Tariff]:
        """
        Возвращает все тарифы
        :return: список тарифов
        """
        query = select(self.model)
        _ = await self.session.execute(query)
        return list(_.scalars().all())
