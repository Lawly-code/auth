import re
import uuid
from pydantic import BaseModel, EmailStr, IPvAnyAddress, field_validator

# Регулярки
DEVICE_ID_REGEX = r'^(?:[A-Z0-9]+\.[A-Z0-9]+\.[A-Z0-9]+|[A-F0-9]+\-[A-F0-9]+\-[A-F0-9]+\-[A-F0-9]+\-[A-F0-9]+)$'
DEVICE_OS_REGEX = r'^(android|ios)\s\d+$'


# Отдельные миксины для валидации
class DeviceIDValidationMixin:
    @field_validator("device_id")
    def validate_device_id(cls, value: str) -> str:
        if not re.fullmatch(DEVICE_ID_REGEX, value):
            raise ValueError("Invalid device_id format.")
        return value


class DeviceOSValidationMixin:
    @field_validator("device_os")
    def validate_device_os(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not re.fullmatch(DEVICE_OS_REGEX, normalized):
            raise ValueError(
                "device_os must be in format 'Android <version>' or 'iOS <version>'"
            )
        return value


# Общий миксин, если нужна валидация и ID, и OS
class DeviceValidationMixin(DeviceIDValidationMixin, DeviceOSValidationMixin):
    pass


# DTO-шки


class LoginUserDTO(DeviceValidationMixin, BaseModel):
    email: EmailStr
    password: str
    device_id: str
    device_os: str
    device_name: str


class LoginUserWithIPDTO(LoginUserDTO):
    ip: IPvAnyAddress


class RegisterUserDTO(DeviceValidationMixin, BaseModel):
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


class LogoutDTO(DeviceIDValidationMixin, BaseModel):
    device_id: str
    refresh_token: uuid.UUID
