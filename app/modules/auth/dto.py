from pydantic import BaseModel


class LoginUserDTO(BaseModel):
    email: str
    name: str
    password: str
    device_id: str
    device_os: str
    device_name: str


class LoginUserWithIPDTO(LoginUserDTO):
    ip: str


class RegisterUserDTO(BaseModel):
    email: str
    name: str
    password: str
    device_id: str
    device_os: str
    device_name: str
    agree_to_terms: bool


class RegisterUserWithIPDTO(RegisterUserDTO):
    ip: str


class AuthTokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
