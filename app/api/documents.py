from fastapi import APIRouter

from descriptions.documents import privacy_policy
from models.dto import PrivacyPolicyDTO

router = APIRouter()


@router.get(
    "/privacy-policy",
    summary="Получение текста политики конфиденциальности",
    description=privacy_policy,
    tags=["Документы"],
    response_model=PrivacyPolicyDTO,
    responses={
        200: {
            "description": "Текст политики конфиденциальности",
            "model": PrivacyPolicyDTO
        }
    }
)
async def get_privacy_policy():
    # Здесь логика получения текста, например, из базы, файла или константы
    return PrivacyPolicyDTO(content="<h1>Политика конфиденциальности</h1><p>Текст...</p>")
