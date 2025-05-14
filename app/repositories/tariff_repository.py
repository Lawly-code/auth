from lawly_db.db_models import Tariff
from sqlalchemy import select

from repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class TariffRepository(BaseRepository):
    model = Tariff

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_tariff_by_id(self, tariff_id: int) -> Tariff | None:
        """
        Возвращает тариф по ID
        :param tariff_id: ID тарифа
        :return: объект класса Tariff
        """

        query = select(self.model).where(self.model.id == tariff_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all_tariffs(self) -> list[Tariff]:
        """
        Возвращает все тарифы
        :return: список тарифов
        """
        query = select(self.model)
        _ = await self.session.execute(query)
        return list(_.scalars().all())

    async def get_base_tariff(self) -> Tariff | None:
        """
        Возвращает базовый тариф
        :return: объект класса Tariff
        """
        query = select(self.model).where(self.model.is_base.is_(True))
        result = await self.session.execute(query)
        return result.scalar()
