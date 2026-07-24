from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy import String
from app.core.database import Base
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(String,primary_key=True,default = lambda:str(uuid4()))
    title = Column(String(100),nullable=False)
    priority = Column(String(10),nullable=False)
    status = Column(String(20),nullable=False,default="open")
    assignee_email = Column(String(254),nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)


    