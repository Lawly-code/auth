from models.dto import LoginUserDTO
from repositories.cipher_repository import CipherRepository
from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.cipher_repo = CipherRepository()

    async def login(self, login: str, password: str):
        hashed_password = self.cipher_repo.hash_password(password)
        await self.user_repo.login(LoginUserDTO(login=login, password=hashed_password))
