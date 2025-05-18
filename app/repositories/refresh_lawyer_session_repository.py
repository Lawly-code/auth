import time
import uuid

from lawly_db.db_models import RefreshSessionLawyer
from repositories.base_repository import BaseRepository
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class RefreshSessionLawyerRepository(BaseRepository):
    model = RefreshSessionLawyer

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def refresh_token(self, refresh_token: str) -> bool:
        pass

    async def get_all_user_sessions_count(self, user_id: int) -> int:
        """
        Возвращает количество истёкших сессий пользователя.
        """
        now = int(time.time())
        query = select(func.count(self.model.id)).where(
            self.model.user_id == user_id, self.model.expires_in > now
        )

        result = await self.session.execute(query)
        count = result.scalar_one()
        return count

    async def delete_all_user_sessions(self, user_id: int):
        """
        Удаляет все сессии пользователя
        :param user_id: id пользователя
        :return:
        """
        query = select(self.model).where(self.model.user_id == user_id)
        _ = await self.session.execute(query)
        sessions = _.scalars().all()
        for session in sessions:
            await self.session.delete(session)

    async def refresh_session_delete(self, refresh_session: model):
        """
        Удаляет сессию
        :param refresh_session: объект класса RefreshSession
        :return:
        """
        await self.session.delete(refresh_session)
        await self.session.commit()

    async def get_by_refresh_token(
        self, refresh_token: uuid.UUID, fingerprint: str
    ) -> model | None:
        """
        Возвращает сессию по refresh_token и fingerprint
        :param refresh_token: refresh_token
        :param fingerprint: fingerprint
        :return: объект класса RefreshSession
        """
        query = select(self.model).where(
            self.model.refresh_token == str(refresh_token),
            self.model.fingerprint == fingerprint,
        )
        _ = await self.session.execute(query)
        return _.scalar()
