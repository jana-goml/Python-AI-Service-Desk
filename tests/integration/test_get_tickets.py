from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
import pytest
from app.services import ticket_service

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,priority",
    [
        ("open","high"),
        (None,None),
    ],
)
async def test_get_all_tickets_happy_path(client,status,priority):
    mock_ticket = SimpleNamespace(
        id="t-1",
        title="VPN Issue",
        priority="high",
        status="open",
        assignee_email=None,
        created_at=datetime.now(timezone.utc)
        
    )
    with patch.object(ticket_service,"get_all_tickets",new_callable=AsyncMock) as mock_get:
        mock_get.return_value = [mock_ticket]
        query = f"?status={status}" if status else ""
        response = await client.get(f"/tickets/{query}")
    assert response.status_code == 200
    assert len(response.json()) == 1
