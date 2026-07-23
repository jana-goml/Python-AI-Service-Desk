from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
import pytest
from app.services import ticket_service

@pytest.mark.asyncio
async def test_create_ticket_happy_path(client):
    created_mock = SimpleNamespace(
        id="t-100",
        title="Printer Issue",
        priority="high",
        status="open",
        assignee_email="admin@test.com",
    )
    with patch.object(ticket_service,"create_ticket",new_callable=AsyncMock) as mock_create:
        mock_create.return_value = created_mock
        response = await client.post(
            "/tickets/",
            json={
                "title":"Printer Issue",
                "priority":"high",
                "assignee_email":"admin@test.com",
            },
        )
    assert response.status_code == 201
    assert response.json()["id"] == "t-100"
    assert response.json()["status"] == "open"

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "priority",
    [
        "urgent",
        "critical",
    ],
)
async def test_create_ticket_invalid_priority_failure(client,priority):
    response = await client.post(
        "/tickets/",
        json={
            "title":"Printer Issue",
            "priority":priority,
        },
    )
    assert response.status_code == 422
