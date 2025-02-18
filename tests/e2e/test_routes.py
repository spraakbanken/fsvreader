import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_index(client: AsyncClient, snapshot) -> None:
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == snapshot
