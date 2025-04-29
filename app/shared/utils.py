from fastapi import Request
from fastapi.datastructures import Headers


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
