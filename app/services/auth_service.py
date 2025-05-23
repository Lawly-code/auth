import uuid
from datetime import UTC, datetime, timedelta

from fastapi import Depends
from lawly_db.db_models.db_session import get_session

from api.auth.auth_handler import sign_jwt
from config import settings
from lawly_db.db_models import RefreshSession, User, Subscribe, RefreshSessionLawyer
from modules.auth import (
    AuthTokenResponseDTO,
    LoginUserWithIPDTO,
    RegisterUserWithIPDTO,
    RefreshTokenLawyerWithIPModelDTO,
    RefreshTokenWithIPModelDTO,
    LogoutWithUserIDDTO,
    TokenModelDTO,
    LogoutLawyerWithUserIDDTO,
    LoginLawyerWithIPDTO,
)

from repositories.cipher_repository import CipherRepository
from repositories.refresh_lawyer_session_repository import (
    RefreshSessionLawyerRepository,
)
from repositories.refresh_session_repository import RefreshSessionRepository
from repositories.subscribe_repository import SubscribeRepository
from repositories.tariff_repository import TariffRepository
from repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.user_repo = UserRepository(session)
        self.refresh_session_repo = RefreshSessionRepository(session)
        self.refresh_lawyer_session_repo = RefreshSessionLawyerRepository(session)
        self.cipher_repo = CipherRepository()
        self.subscribe_repo = SubscribeRepository(session)
        self.tariff_repo = TariffRepository(session)

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
        refresh_expires = self.get_refresh_expires_timestamp()
        refresh_token = RefreshSession(
            user_id=user.id,
            refresh_token=uuid.uuid4(),
            ip=str(login_user.ip),
            device_os=login_user.device_os,
            device_name=login_user.device_name,
            device_id=login_user.device_id,
            expires_in=refresh_expires,
        )
        await self.refresh_session_repo.save(entity=refresh_token, session=self.session)
        return AuthTokenResponseDTO(
            refresh_token=str(refresh_token.refresh_token), access_token=access_token
        )

    async def login_lawyer(
        self, login_lawyer: LoginLawyerWithIPDTO
    ) -> AuthTokenResponseDTO | None:
        hashed_password = self.cipher_repo.hash_password(login_lawyer.password)
        user = await self.user_repo.login_lawyer(
            email=login_lawyer.email, hash_password=hashed_password
        )
        if not user:
            return None
        if (
            await self.refresh_lawyer_session_repo.get_all_user_sessions_count(
                user_id=user.id
            )
            >= settings.jwt_settings.max_user_sessions
        ):
            await self.refresh_lawyer_session_repo.delete_all_user_sessions(
                user_id=user.id
            )
        access_token = sign_jwt(user_id=user.id, lawyer=True)
        refresh_expires = self.get_refresh_expires_timestamp()
        refresh_token = RefreshSessionLawyer(
            user_id=user.id,
            refresh_token=uuid.uuid4(),
            ip=str(login_lawyer.ip),
            fingerprint=login_lawyer.fingerprint,
            user_agent=login_lawyer.user_agent,
            expires_in=refresh_expires,
        )
        await self.refresh_lawyer_session_repo.save(
            entity=refresh_token, session=self.session
        )
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
        refresh_expires = self.get_refresh_expires_timestamp()
        refresh_token = RefreshSession(
            user_id=user.id,
            refresh_token=uuid.uuid4(),
            ip=str(register_user.ip),
            device_os=register_user.device_os,
            device_name=register_user.device_name,
            device_id=register_user.device_id,
            expires_in=refresh_expires,
        )
        await self.refresh_session_repo.save(entity=refresh_token, session=self.session)

        tariff = await self.tariff_repo.get_base_tariff()
        subscribe = Subscribe(
            user_id=user.id,
            tariff_id=tariff.id,
            start_date=datetime.now(),
            end_date=None,
            consultations_total=tariff.consultations_count,
            can_user_ai=tariff.ai_access,
            can_create_custom_templates=tariff.custom_templates,
            unlimited_documents=tariff.unlimited_docs,
            is_base=tariff.is_base,
        )
        await self.subscribe_repo.save(entity=subscribe, session=self.session)
        return AuthTokenResponseDTO(
            refresh_token=str(refresh_token.refresh_token), access_token=access_token
        )

    async def refresh_tokens(
        self, refresh: RefreshTokenWithIPModelDTO
    ) -> TokenModelDTO | None:
        refresh_session = await self.refresh_session_repo.get_by_refresh_token(
            refresh_token=refresh.refresh_token,
            device_id=refresh.device_id,
        )
        if not refresh_session:
            return None
        if refresh_session.expires_in < datetime.now(UTC).timestamp():
            return None
        await self.refresh_session_repo.refresh_session_delete(
            refresh_session=refresh_session
        )
        refresh_expires = self.get_refresh_expires_timestamp()
        new_refresh_token = RefreshSession(
            user_id=refresh_session.user_id,
            refresh_token=uuid.uuid4(),
            ip=str(refresh.ip),
            device_os=refresh.device_os,
            device_name=refresh.device_name,
            device_id=refresh.device_id,
            expires_in=refresh_expires,
        )
        await self.refresh_session_repo.save(
            entity=new_refresh_token, session=self.session
        )
        access_token = sign_jwt(user_id=refresh_session.user_id)
        return TokenModelDTO(
            refresh_token=str(new_refresh_token.refresh_token),
            access_token=access_token,
        )

    async def refresh_tokens_lawyer(
        self, refresh_lawyer: RefreshTokenLawyerWithIPModelDTO
    ) -> TokenModelDTO | None:
        refresh_session = await self.refresh_lawyer_session_repo.get_by_refresh_token(
            refresh_token=refresh_lawyer.refresh_token,
            fingerprint=refresh_lawyer.fingerprint,
        )
        if not refresh_session:
            return None
        if refresh_session.expires_in < datetime.now(UTC).timestamp():
            return None
        await self.refresh_lawyer_session_repo.refresh_session_delete(
            refresh_session=refresh_session
        )
        refresh_expires = self.get_refresh_expires_timestamp()
        new_refresh_token = RefreshSessionLawyer(
            user_id=refresh_session.user_id,
            refresh_token=uuid.uuid4(),
            ip=str(refresh_lawyer.ip),
            fingerprint=refresh_lawyer.fingerprint,
            user_agent=refresh_lawyer.user_agent,
            expires_in=refresh_expires,
        )
        await self.refresh_session_repo.save(
            entity=new_refresh_token, session=self.session
        )
        access_token = sign_jwt(user_id=refresh_session.user_id, lawyer=True)
        return TokenModelDTO(
            refresh_token=str(new_refresh_token.refresh_token),
            access_token=access_token,
        )

    async def logout(self, logout_dto: LogoutWithUserIDDTO) -> bool:
        refresh_session = await self.refresh_session_repo.get_by_refresh_token(
            refresh_token=logout_dto.refresh_token,
            device_id=logout_dto.device_id,
        )
        if not refresh_session:
            return False
        await self.refresh_session_repo.refresh_session_delete(
            refresh_session=refresh_session
        )
        return True

    async def logout_lawyer(self, logout_lawyer: LogoutLawyerWithUserIDDTO) -> bool:
        refresh_session = await self.refresh_lawyer_session_repo.get_by_refresh_token(
            refresh_token=logout_lawyer.refresh_token,
            fingerprint=logout_lawyer.fingerprint,
        )
        if not refresh_session:
            return False
        await self.refresh_lawyer_session_repo.refresh_session_delete(
            refresh_session=refresh_session
        )
        return True

    @staticmethod
    def get_refresh_expires_timestamp() -> int:
        """
        Возвращает UTC timestamp истечения срока refresh токена.
        Использует timezone-aware datetime объект.
        """
        expires_at = datetime.now(UTC) + timedelta(
            minutes=settings.jwt_settings.refresh_token_expire_minutes
        )
        return int(expires_at.timestamp())
