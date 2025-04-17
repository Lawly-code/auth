from models.dto import LoginUserDTO
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def login(self, login_data: LoginUserDTO) -> int | None:
        """
        Validating the login of user

        :param login_data: LoginUserDTO
        :return: if user exists, return user_id else None
        """
        pass
