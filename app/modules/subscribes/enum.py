from enum import Enum


class GetSubscribesEnum(Enum):
    ACCESS_DENIED = "access_denied"
    NOT_FOUND = "not_found"


class SubscribeStatusEnum(Enum):
    SUCCESS = "success"
    INVALID_TARIFF_ID = "invalid_tariff_id"
    ALREADY_SUBSCRIBED = "already_subscribed"
