from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
import pytest
from pydantic import ValidationError
from fastapi import HTTPException
from app.core.exceptions import TicketNotFoundError
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.services import ticket_service

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.fixture
def base_ticket_data():
    return {"title": "Database connection failing","priority": "high","assignee_email": "admin@example.com"}

@pytest.fixture
def sample_ticket_model():
    return SimpleNamespace(
        id="t-101",
        title="Database connection failing",
        priority="high",
        status="open",
        assignee_email="admin@example.com",
    )

def test_ticket_create_schema_valid_fields(base_ticket_data):
    req = TicketCreate(**base_ticket_data)
    assert req.title == "Database connection failing"
    assert req.priority == "high"
    assert req.assignee_email == "admin@example.com"

@pytest.mark.parametrize("priority",["low","medium","high"])
def test_ticket_create_valid_priorities(priority,base_ticket_data):
    base_ticket_data["priority"] = priority
    req = TicketCreate(**base_ticket_data)
    assert req.priority == priority

@pytest.mark.parametrize("priority",["urgent","critical","highest",""])
def test_ticket_create_invalid_priorities(priority, base_ticket_data):
    base_ticket_data["priority"] = priority
    with pytest.raises(ValidationError):
        TicketCreate(**base_ticket_data)

@pytest.mark.parametrize("payload",[
    {"priority": "high"},  
    {"title": "Printer Issue"},  
    {},  
])
def test_ticket_create_missing_required_fields(payload):
    with pytest.raises(ValidationError):
        TicketCreate(**payload)

@pytest.mark.parametrize("title",[None,12345,["invalid"]])
def test_ticket_create_invalid_title_types(title,base_ticket_data):
    base_ticket_data["title"] = title
    with pytest.raises(ValidationError):
        TicketCreate(**base_ticket_data)

@pytest.mark.parametrize("email",[
    "user@example.com",
    "john.doe+service@domain.org",
    "tech_admin@sub.company.co.uk",
    None,
])
def test_ticket_create_valid_email_formatting(email,base_ticket_data):
    base_ticket_data["assignee_email"] = email
    req = TicketCreate(**base_ticket_data)
    assert req.assignee_email == email

@pytest.mark.parametrize("invalid_email",[
    12345,
    ["invalid_email@domain.com"],
    {"email": "test@domain.com"},
])
def test_ticket_create_invalid_email_formatting(invalid_email,base_ticket_data):
    base_ticket_data["assignee_email"] = invalid_email
    with pytest.raises(ValidationError):
        TicketCreate(**base_ticket_data)

@pytest.mark.asyncio
async def test_service_create_ticket_default_status(mock_db,base_ticket_data):
    ticket_data = TicketCreate(**base_ticket_data)
    with patch.object(ticket_service, "ticket_repository") as mock_repo:
        mock_repo.create_ticket = AsyncMock(side_effect=lambda db,t:t)
        result = await ticket_service.create_ticket(mock_db,ticket_data)
    assert result.status == "open"
    assert result.title == "Database connection failing"

@pytest.mark.parametrize("ticket_id",["t-101","t-999"])
@pytest.mark.asyncio
async def test_service_get_ticket_success(mock_db,sample_ticket_model,ticket_id):
    sample_ticket_model.id = ticket_id
    with patch.object(ticket_service,"ticket_repository") as mock_repo:
        mock_repo.get_ticket_by_id = AsyncMock(return_value=sample_ticket_model)
        result = await ticket_service.get_ticket(mock_db,ticket_id)
    assert result.id == ticket_id

@pytest.mark.parametrize("missing_id",["t-missing","ghost-id"])
@pytest.mark.asyncio
async def test_ticket_not_found_exception_format(mock_db,missing_id):
    with patch.object(ticket_service,"ticket_repository") as mock_repo:
        mock_repo.get_ticket_by_id = AsyncMock(return_value=None)
        with pytest.raises(TicketNotFoundError) as exc_info:
            await ticket_service.get_ticket(mock_db,missing_id)
    assert exc_info.value.ticket_id == missing_id

@pytest.mark.parametrize("status,priority",[("open","high"),("in_progress",None)])
@pytest.mark.asyncio
async def test_service_get_all_tickets_filtered(mock_db,sample_ticket_model,status,priority):
    with patch.object(ticket_service, "ticket_repository") as mock_repo:
        mock_repo.get_all_tickets = AsyncMock(return_value=[sample_ticket_model])
        results = await ticket_service.get_all_tickets(mock_db,status=status,priority=priority)
    assert len(results) == 1
    mock_repo.get_all_tickets.assert_called_once_with(mock_db,status,priority)

@pytest.mark.parametrize("update_field,new_value",[
    ("title", "Updated Title"),
    ("status", "in_progress"),
    ("priority", "low"),
])
@pytest.mark.asyncio
async def test_service_update_ticket_success(mock_db,sample_ticket_model,update_field,new_value):
    update_data = TicketUpdate(**{update_field:new_value})
    with patch.object(ticket_service, "ticket_repository") as mock_repo:
        mock_repo.get_ticket_by_id = AsyncMock(return_value=sample_ticket_model)
        mock_repo.update_ticket = AsyncMock(side_effect=lambda db,t: t)
        updated = await ticket_service.update_ticket(mock_db,"t-101",update_data)
    assert getattr(updated,update_field) == new_value

@pytest.mark.parametrize("new_status",["open","in_progress"])
@pytest.mark.asyncio
async def test_service_update_closed_ticket_reopen_failure(mock_db, sample_ticket_model, new_status):
    sample_ticket_model.status = "closed"
    update_data = TicketUpdate(status=new_status)
    with patch.object(ticket_service, "ticket_repository") as mock_repo:
        mock_repo.get_ticket_by_id = AsyncMock(return_value=sample_ticket_model)
        with pytest.raises(HTTPException) as exc_info:
            await ticket_service.update_ticket(mock_db, "t-101", update_data)
    assert exc_info.value.status_code == 400
    assert "Closed tickets cannot be reopened" in exc_info.value.detail