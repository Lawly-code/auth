from modules.documents import PrivacyPolicyDTO
from shared import base_response

privacy_response = {
    **base_response,
    200: {
        "description": "Текст политики конфиденциальности",
        "model": PrivacyPolicyDTO
    }
}