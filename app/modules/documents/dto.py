from pydantic import BaseModel


class PrivacyPolicyDTO(BaseModel):
    content: str  # HTML-контент политики конфиденциальности
