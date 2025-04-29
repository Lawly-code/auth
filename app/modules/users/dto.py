from datetime import datetime

from pydantic import BaseModel


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
    features: list[str]


class UserInfoDTO(BaseModel):
    user_id: int
    tariff: TariffDTO
    start_date: datetime
    end_date: datetime
