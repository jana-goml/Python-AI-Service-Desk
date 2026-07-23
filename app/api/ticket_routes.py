from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.schemas.ticket import TicketCreate
from app.schemas.ticket import TicketResponse
from app.schemas.ticket import TicketUpdate
from app.services import ticket_service

router = APIRouter(prefix="/tickets",tags=["Tickets"])

@router.post(
    "/",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket(ticket:TicketCreate,db:AsyncSession = Depends(get_db)):
    return await ticket_service.create_ticket(
        db,
        ticket
    )

@router.get(
    "/",
    response_model=list[TicketResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_tickets(status:Optional[str] = None,priority:Optional[str] = None,db:AsyncSession = Depends(get_db)):
    return await ticket_service.get_all_tickets(
        db,
        status=status,
        priority=priority
    )

@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
)
async def get_ticket(ticket_id:str,db:AsyncSession = Depends(get_db)):
    return await ticket_service.get_ticket(
        db,
        ticket_id
    )

@router.put(
    "/{ticket_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
)
async def update_ticket(ticket_id:str,ticket:TicketUpdate,db:AsyncSession = Depends(get_db)):
    return await ticket_service.update_ticket(
        db,
        ticket_id,
        ticket
    )

@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_ticket(ticket_id:str,db:AsyncSession = Depends(get_db)):
    await ticket_service.delete_ticket(
        db,
        ticket_id
    )
    return None