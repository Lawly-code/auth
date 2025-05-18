import re
import uuid
from pydantic import BaseModel, EmailStr, IPvAnyAddress, field_validator

DEVICE_ID_REGEX = (
    r'^(?:'
    r'[A-Z0-9]+\.[A-Z0-9]+\.[A-Z0-9]+'
    r'|'
    r'[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}'
    r'|'
    r'[A-Z0-9]+\.[0-9]{6}\.[0-9]{3}(?:\.[A-Z0-9]+)?'
    r')$'
)
DEVICE_OS_REGEX = r'^(android\s\d+|ios\s\d+(\.\d+)?)$'
PASSWORD_REGEX = r'^[\x20-\x7E]+$'

FINGERPRINT_REGEX = r'^[a-zA-Z0-9\-]{10,200}$'  # Пример: UUID или нечто подобное


class FingerprintValidationMixin:
    @field_validator("fingerprint", mode="before")
    @classmethod
    def validate_fingerprint(cls, value: str) -> str:
        if not re.fullmatch(FINGERPRINT_REGEX, value):
            raise ValueError(
                "Недопустимый fingerprint. Ожидается строка от 10 до 200 символов (только буквы, цифры, дефис)."
            )
        return value


# Миксины с валидаторами, можно и как обычные классы
class PasswordValidationMixin:
    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.fullmatch(PASSWORD_REGEX, value):
            raise ValueError(
                "Пароль должен содержать только латинские символы и допустимые спецсимволы."
            )
        return value


class DeviceIDValidationMixin:
    @field_validator("device_id", mode="before")
    @classmethod
    def validate_device_id(cls, value: str) -> str:
        if not re.fullmatch(DEVICE_ID_REGEX, value):
            raise ValueError("Неверный формат идентификатора устройства.")
        return value


class DeviceOSValidationMixin:
    @field_validator("device_os", mode="before")
    @classmethod
    def validate_device_os(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not re.fullmatch(DEVICE_OS_REGEX, normalized):
            raise ValueError(
                "Поле device_os должно быть в формате 'Android <версия>' или 'iOS <версия>'."
            )
        return value


# Комбинирующий миксин
class DeviceValidationMixin(DeviceIDValidationMixin, DeviceOSValidationMixin):
    pass


# DTO модели
class LoginUserDTO(PasswordValidationMixin, DeviceValidationMixin, BaseModel):
    email: EmailStr
    password: str
    device_id: str
    device_os: str
    device_name: str


class LoginUserWithIPDTO(LoginUserDTO):
    ip: IPvAnyAddress


class LoginLawyerDTO(FingerprintValidationMixin, PasswordValidationMixin, BaseModel):
    email: EmailStr
    password: str
    user_agent: str
    fingerprint: str


class LoginLawyerWithIPDTO(LoginLawyerDTO):
    ip: IPvAnyAddress


class RegisterUserDTO(PasswordValidationMixin, DeviceValidationMixin, BaseModel):
    email: EmailStr
    name: str
    password: str
    device_id: str
    device_os: str
    device_name: str
    agree_to_terms: bool


class RegisterUserWithIPDTO(RegisterUserDTO):
    ip: IPvAnyAddress


class AuthTokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str


class TokenModelDTO(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenModelDTO(DeviceValidationMixin, BaseModel):
    device_id: str
    device_os: str
    device_name: str
    refresh_token: uuid.UUID


class RefreshTokenWithIPModelDTO(RefreshTokenModelDTO):
    ip: IPvAnyAddress


class RefreshTokenLawyerModelDTO(FingerprintValidationMixin, BaseModel):
    refresh_token: uuid.UUID
    user_agent: str
    fingerprint: str


class RefreshTokenLawyerWithIPModelDTO(RefreshTokenLawyerModelDTO):
    ip: IPvAnyAddress


class LogoutDTO(DeviceIDValidationMixin, BaseModel):
    device_id: str
    refresh_token: uuid.UUID


class LogoutWithUserIDDTO(LogoutDTO):
    user_id: int


class LogoutLawyerDTO(FingerprintValidationMixin, BaseModel):
    fingerprint: str
    refresh_token: uuid.UUID


class LogoutLawyerWithUserIDDTO(LogoutLawyerDTO):
    user_id: int
