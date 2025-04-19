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


class UserSubscriptionDTO(BaseModel):
    id: int
    user_id: int
    tariff: TariffDTO
    start_date: datetime
    end_date: datetime
    days_left: int