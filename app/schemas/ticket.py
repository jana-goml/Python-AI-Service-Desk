from typing import Literal
from pydantic import BaseModel, Field
from pydantic import ConfigDict
from datetime import datetime

class TicketCreate(BaseModel):
    title:str
    priority:Literal["low","medium","high"]
    assignee_email:str | None = None

class TicketUpdate(BaseModel):
    title:str | None = None
    priority:Literal["low","medium","high"] | None = None
    status:Literal["open","in_progress","resolved"] | None = None
    assignee_email:str | None = None

class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:str
    title:str
    priority:Literal["low","medium","high"]
    status:Literal["open","in_progress","resolved"]
    assignee_email:str | None = None
    created_at: datetime

class SummarizeRequest(BaseModel):
    ticket_description: str = Field(min_length=10, max_length=5_000)

class SummarizeResponse(BaseModel):
    summary: str
    suggested_response: str




    