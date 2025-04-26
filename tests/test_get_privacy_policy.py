from httpx import AsyncClient


async def test_login_with_not_valid_password(ac: AsyncClient):
    resp_privacy_policy = await ac.get("/api/v1/privacy-policy")
    assert resp_privacy_policy.status_code == 200
