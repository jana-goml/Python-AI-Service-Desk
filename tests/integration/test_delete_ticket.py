from unittest.mock import AsyncMock, patch
import pytest
from app.services import ticket_service

@pytest.mark.asyncio
async def test_delete_ticket_happy_path(client):
    with patch.object(ticket_service,"delete_ticket",new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = None
        response = await client.delete("/tickets/t-1")
    assert response.status_code == 204
    assert response.text == ""
