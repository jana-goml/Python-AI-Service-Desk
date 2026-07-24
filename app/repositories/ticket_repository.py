from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket

async def create_ticket(db:AsyncSession,ticket:Ticket):
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket

async def get_all_tickets(db:AsyncSession,status=None,priority=None):
    query = select(Ticket)
    if status:
        query = query.where(Ticket.status == status)
    if priority:
        query = query.where(Ticket.priority == priority)
    result = await db.execute(query)
    return result.scalars().all()

async def get_ticket_by_id(db:AsyncSession,ticket_id:str):
    result = await db.execute(
        select(Ticket).where(Ticket.id == ticket_id))
    return result.scalar_one_or_none()

async def update_ticket(db:AsyncSession,ticket:Ticket):
    await db.commit()
    await db.refresh(ticket)
    return ticket

async def delete_ticket(db:AsyncSession,ticket:Ticket):
    await db.delete(ticket)
    await db.commit()


    