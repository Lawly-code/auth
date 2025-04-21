import uuid
from datetime import UTC, datetime, timedelta

from api.auth.auth_handler import sign_jwt
from config import settings
from lawly_db.db_models import RefreshSession, User
from modules.auth import AuthTokenResponseDTO, LoginUserWithIPDTO, RegisterUserWithIPDTO
from repositories.cipher_repository import CipherRepository
from repositories.refresh_session_repository import RefreshSessionRepository
from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.refresh_session_repo = RefreshSessionRepository(session)
        self.cipher_repo = CipherRepository()

    async def login(
        self, login_user: LoginUserWithIPDTO
    ) -> AuthTokenResponseDTO | None:
        hashed_password = self.cipher_repo.hash_password(login_user.password)
        user = await self.user_repo.login(
            email=login_user.email, hash_password=hashed_password
        )
        if not user:
            return None
        if (
            await self.refresh_session_repo.get_all_user_sessions_count(user_id=user.id)
            >= settings.jwt_settings.max_user_sessions
        ):
            await self.refresh_session_repo.delete_all_user_sessions(user_id=user.id)
        access_token = sign_jwt(user_id=user.id)
        refresh_expires = get_refresh_expires_timestamp()
        refresh_token = RefreshSession(
            user_id=user.id,
            refresh_token=uuid.uuid4(),
            ip=login_user.ip,
            device_os=login_user.device_os,
            device_name=login_user.device_name,
            device_id=login_user.device_id,
            expires_in=refresh_expires,
        )
        await self.refresh_session_repo.save(entity=refresh_token, session=self.session)
        return AuthTokenResponseDTO(
            refresh_token=str(refresh_token.refresh_token), access_token=access_token
        )

    async def register(
        self, register_user: RegisterUserWithIPDTO
    ) -> AuthTokenResponseDTO | None:
        if await self.user_repo.get_user_by_email(
            email=register_user.email, session=self.session
        ):
            return None
        hashed_password = self.cipher_repo.hash_password(register_user.password)
        user = User(
            email=register_user.email, password=hashed_password, name=register_user.name
        )
        await self.user_repo.save(entity=user, session=self.session)
        access_token = sign_jwt(user_id=user.id)
        refresh_expires = get_refresh_expires_timestamp()
        refresh_token = RefreshSession(
            user_id=user.id,
            refresh_token=uuid.uuid4(),
            ip=register_user.ip,
            device_os=register_user.device_os,
            device_name=register_user.device_name,
            device_id=register_user.device_id,
            expires_in=refresh_expires,
        )
        await self.refresh_session_repo.save(entity=refresh_token, session=self.session)
        return AuthTokenResponseDTO(
            refresh_token=str(refresh_token.refresh_token), access_token=access_token
        )


def get_refresh_expires_timestamp() -> int:
    """
    Возвращает UTC timestamp истечения срока refresh токена.
    Использует timezone-aware datetime объект.
    """
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.jwt_settings.refresh_token_expire_minutes
    )
    return int(expires_at.timestamp())
