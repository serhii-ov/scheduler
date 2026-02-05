from httpx import AsyncClient


async def get_auth_headers(
    client: AsyncClient,
    *,
    phone_number: str,
    password: str,
) -> dict[str, str]:
    response = await client.post(
        "/api/users/login",
        data={
            "username": phone_number,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200, response.text

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# =========================================================================================
async def get_auth_headers(
    client: AsyncClient,
    phone_number: str,
    password: str,
) -> dict[str, str]:
    response = await client.post(
        "/api/users/login",
        data={
            "username": phone_number,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200, response.text
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
