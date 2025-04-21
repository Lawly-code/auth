from repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class RefreshSessionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def refresh_token(self, refresh_token: str) -> bool:
        pass
