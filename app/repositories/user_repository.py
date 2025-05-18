from lawly_db.db_models import User, Lawyer
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

    async def get_user_by_id(self, user_id: int, session: AsyncSession) -> model:
        """
        Возвращает пользователя по id

        :param user_id: id пользователя
        :return: объект класса User
        """
        query = select(self.model).where(self.model.id == user_id)
        _ = await session.execute(query)
        return _.scalar()

    async def login_lawyer(self, email: str, hash_password: str) -> model | None:
        """
        Проверяет на то существует ли пользователь с таким email и паролем
        email: почта пользователя
        hash_password: пароль пользователя
        :return: id пользователя или None
        """
        query = (
            select(self.model)
            .join(Lawyer)
            .where(
                Lawyer.user_id == self.model.id,
                self.model.email == email,
                self.model.password == hash_password,
            )
        )
        _ = await self.session.execute(query)
        return _.scalar()
