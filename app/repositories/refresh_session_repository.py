from sqlalchemy.ext.asyncio import AsyncSession


class RefreshSessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def refresh_token(self, refresh_token: str) -> bool:
        pass
