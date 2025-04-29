import json

from pydantic import BaseModel
from pydantic import field_validator
from datetime import datetime


class DateRangeValidationMixin:
    @field_validator("end_date")
    def validate_date_range(cls, end_date: datetime, info):
        start_date = info.data.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("end_date must be later than start_date.")
        return end_date


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


class SubscriptionDTO(DateRangeValidationMixin, BaseModel):
    tariff_id: int
    start_date: datetime
    end_date: datetime
    count_lawyers: int = 0
    consultations_total: int = 0
    consultations_used: int = 0
    can_user_ai: bool = False
    can_create_custom_templates: bool = False
    unlimited_documents: bool = False


class SubscriptionWithUserIdDTO(SubscriptionDTO, BaseModel):
    user_id: int


class GetUserSubscriptionDTO(BaseModel):
    tariff: TariffDTO
    start_date: datetime
    end_date: datetime
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
