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
    consultations_count: int
    ai_access: bool
    custom_templates: bool
    unlimited_docs: bool
    is_base: bool


class UserInfoDTO(BaseModel):
    user_id: int
    tariff: TariffDTO
    start_date: datetime
    end_date: datetime | None = None
