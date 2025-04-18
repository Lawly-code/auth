from datetime import datetime
from typing import List

from pydantic import BaseModel


class LoginUserDTO(BaseModel):
    login: str
    password: str


class RegisterUserDTO(BaseModel):
    name: str
    email: str
    password: str
    agree_to_terms: bool


class InfoModelDto(BaseModel):
    code: int
    message: str
    details: dict


class UserDTO(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime


class TariffDTO(BaseModel):
    id: int
    name: str
    description: str
    price: int
    features: List[str]


class UserSubscriptionDTO(BaseModel):
    id: int
    user_id: int
    tariff: TariffDTO
    start_date: datetime
    end_date: datetime
    days_left: int


class PrivacyPolicyDTO(BaseModel):
    content: str  # HTML-контент политики конфиденциальности

