import json

from pydantic import BaseModel
from pydantic import field_validator
from datetime import datetime


class TariffDTO(BaseModel):
    id: int
    name: str
    description: str | None = None
    features: list[str] = []
    price: int
    consultations_count: int = 0
    ai_access: bool = False
    custom_templates: bool = False
    unlimited_docs: bool = False
    is_base: bool

    @field_validator("features", mode="before")
    def parse_features(cls, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValueError("features must be a valid JSON list")
        return value

    class Config:
        from_attributes = True


class SubscriptionDTO(BaseModel):
    tariff_id: int


class SubscriptionWithUserIdDTO(SubscriptionDTO, BaseModel):
    user_id: int


class GetUserSubscriptionDTO(BaseModel):
    tariff: TariffDTO
    start_date: datetime
    end_date: datetime | None = None
    count_lawyers: int
    consultations_total: int
    consultations_used: int
    can_user_ai: bool
    can_create_custom_templates: bool
    unlimited_documents: bool


class GetUserSubscriptionWithUserIdDTO(GetUserSubscriptionDTO, BaseModel):
    user_id: int

    class Config:
        from_attributes = True
