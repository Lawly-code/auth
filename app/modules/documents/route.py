from fastapi import APIRouter
from modules.documents import PrivacyPolicyDTO, privacy_policy_description
from config import privacy_policy_text

router = APIRouter(tags=["Документы"])


@router.get(
    "/privacy-policy",
    summary="Получение текста политики конфиденциальности",
    description=privacy_policy_description,
    response_model=PrivacyPolicyDTO,
    responses={
        200: {
            "description": "Текст политики конфиденциальности",
            "model": PrivacyPolicyDTO,
        }
    },
)
async def get_privacy_policy():
    return PrivacyPolicyDTO(content=privacy_policy_text)
