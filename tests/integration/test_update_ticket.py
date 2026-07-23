from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
import pytest
from fastapi import HTTPException, status
from app.services import ticket_service

@pytest.mark.asyncio
async def test_update_ticket_happy_path(client):
    updated_mock = SimpleNamespace(
        id="t-1",
        title="Updated Title",
        priority="low",
        status="in_progress",
        assignee_email=None,
    )
    with patch.object(ticket_service,"update_ticket",new_callable=AsyncMock) as mock_update:
        mock_update.return_value = updated_mock
        response = await client.put(
            "/tickets/t-1",
            json={
                "title":"Updated Title",
                "status":"in_progress",
            },
        )
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

@pytest.mark.asyncio
async def test_update_closed_ticket_reopen_edge_case(client):
    with patch.object(ticket_service,"update_ticket",new_callable=AsyncMock) as mock_update:
        mock_update.side_effect = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Closed tickets cannot be reopened")
        response = await client.put(
            "/tickets/t-closed",
            json={
                "status":"open",
            },
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Closed tickets cannot be reopened"
