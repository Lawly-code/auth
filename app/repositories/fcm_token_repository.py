from lawly_db.db_models import FCMToken
from sqlalchemy import select

from repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class FCMTokenRepository(BaseRepository):
    model = FCMToken

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def update_fcm_token(
        self, user_id: int, device_id: str, fcm_token: str
    ) -> bool:
        """
        Обновляет FCM токен для пользователя и возвращает True, если токен обновлен. False, если токен не найден
        :param user_id: ID пользователя
        :param device_id: ID устройства
        :param fcm_token: FCM токен
        """
        query = select(self.model).where(
            self.model.user_id == user_id, self.model.device_id == device_id
        )
        result = await self.session.execute(query)
        token = result.scalar()
        if not token:
            return False
        if token.token == fcm_token:
            return True
        token.token = fcm_token
        await self.session.commit()
        return True
