from unittest.mock import AsyncMock, patch
import pytest
from app.core.exceptions import TicketNotFoundError
from app.services import ticket_service

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ticket_id",
    [
        "missing-1",
        "ghost-99",
    ],
)
async def test_get_ticket_by_id_not_found_failure(client,ticket_id):
    with patch.object(ticket_service,"get_ticket",new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = TicketNotFoundError(ticket_id)
        response = await client.get(f"/tickets/{ticket_id}")
    assert response.status_code == 404
    assert response.json()["error"] == "ticket_not_found"
    assert response.json()["id"] == ticket_id
