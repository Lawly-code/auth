from fastapi import Depends
from lawly_db.db_models import FCMToken
from lawly_db.db_models.db_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from modules.users import UpdateFCMTokenWithUserIdDTO
from repositories.fcm_token_repository import FCMTokenRepository


class FCMTokenService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.fcm_token_repo = FCMTokenRepository(session)

    async def update_or_create_fcm_token_service(
        self, fcm_token_dto: UpdateFCMTokenWithUserIdDTO
    ):
        """
        Обновляет или создает FCM токен для пользователя
        :param fcm_token_dto: DTO с данными для обновления или создания токена
        """

        if not await self.fcm_token_repo.update_fcm_token(
            user_id=fcm_token_dto.user_id,
            device_id=fcm_token_dto.device_id,
            fcm_token=fcm_token_dto.fcm_token,
        ):
            fcm_token = FCMToken(
                user_id=fcm_token_dto.user_id,
                device_id=fcm_token_dto.device_id,
                token=fcm_token_dto.fcm_token,
            )
            await self.fcm_token_repo.save(entity=fcm_token, session=self.session)
