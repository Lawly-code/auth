from fastapi import Depends, Request
from fastapi.datastructures import Headers
from lawly_db.db_models.db_session import get_session
from services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession


def extract_request_data(headers: Headers) -> str:
    host = headers.get("Cf-Connecting-Ip")
    if host:
        return host

    host = headers.get("X-Forwarded-For")
    if host:
        return host
    host = headers.get("X-ProxyUser-Ip")

    if host:
        return host

    host = headers.get("X-Real-IP")

    if host:
        return host


def ip_address_getter(request: Request) -> str:
    host = extract_request_data(request.headers)
    if not host:
        host = request.client.host
    return host


def auth_service_getter(session: AsyncSession = Depends(get_session)):
    return AuthService(session=session)
