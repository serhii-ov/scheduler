from httpx import AsyncClient


async def get_auth_headers(
    client: AsyncClient,
    phone_number: str,
    password: str,
) -> dict:
    response = await client.post(
        "/api/users/login",
        data={
            "username": phone_number,
            "password": password,
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

