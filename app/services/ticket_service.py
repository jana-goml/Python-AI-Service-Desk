from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import TicketNotFoundError
from app.models.ticket import Ticket
from app.repositories import ticket_repository
from fastapi import HTTPException
from fastapi import status

async def create_ticket(db:AsyncSession,ticket_data):
    ticket = Ticket(title=ticket_data.title,priority=ticket_data.priority,status="open",assignee_email=ticket_data.assignee_email)
    return await(
        ticket_repository.create_ticket(
            db,
            ticket
        )
    )

async def get_all_tickets(db:AsyncSession,status=None,priority=None):
    return await(
        ticket_repository.get_all_tickets(
            db,
            status,
            priority,
        )
    )

async def get_ticket(db:AsyncSession,ticket_id):
    ticket = await (
        ticket_repository.get_ticket_by_id(
            db,
            ticket_id,
        )
    )
    if not ticket:
        raise TicketNotFoundError(ticket_id)
    return ticket

async def update_ticket(db:AsyncSession,ticket_id,update_data):
    ticket = await(ticket_repository.get_ticket_by_id(db,ticket_id))
    if (ticket.status == "closed" and update_data.status is not None and update_data.status != "closed"):
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Closed tickets cannot be reopened",
    )
    if not ticket:
        raise TicketNotFoundError(ticket_id)
    if update_data.title is not None:
        ticket.title = update_data.title
    if update_data.priority is not None:
        ticket.priority = update_data.priority
    if update_data.status is not None:
            ticket.status = update_data.status
    if update_data.assignee_email is not None:
        ticket.assignee_email = update_data.assignee_email
    return await(
        ticket_repository.update_ticket(
            db,
            ticket
        )
    )

async def delete_ticket(db:AsyncSession,ticket_id):
    ticket = await(ticket_repository.get_ticket_by_id(db,ticket_id))
    if not ticket:
        raise TicketNotFoundError(ticket_id)
    await ticket_repository.delete_ticket(db,ticket)
    return ticket