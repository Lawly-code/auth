from lawly_db.db_models import User
from repositories.base_repository import BaseRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository):
    model = User

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def login(self, email: str, hash_password: str) -> model | None:
        """
        Проверяет на то существует ли пользователь с таким email и паролем
        email: почта пользователя
        hash_password: пароль пользователя
        :return: id пользователя или None
        """
        query = select(self.model).where(
            self.model.email == email, self.model.password == hash_password
        )
        _ = await self.session.execute(query)
        return _.scalar()

    async def get_user_by_email(self, email: str, session: AsyncSession) -> model:
        """
        Возвращает пользователя по email

        :param email: email пользователя
        :return: объект класса User
        """
        query = select(self.model).where(self.model.email == email)
        _ = await session.execute(query)
        return _.scalar()
