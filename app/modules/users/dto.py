from datetime import datetime

from pydantic import BaseModel, constr

FCM_TOKEN_REGEX = r'^[\w\-:.]+$'


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
    name: str
    email: str
    tariff: TariffDTO
    start_date: datetime
    end_date: datetime | None = None


class UpdateFCMTokenDTO(BaseModel):
    fcm_token: constr(
        strip_whitespace=True, min_length=100, max_length=512, pattern=FCM_TOKEN_REGEX
    )
    device_id: str


class UpdateFCMTokenWithUserIdDTO(UpdateFCMTokenDTO):
    user_id: int
