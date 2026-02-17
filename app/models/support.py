from pydantic import BaseModel
from datetime import datetime

class SupportTicket(BaseModel):
    ticket_id: str
    customer_id : str
    subject : str
    priority : str
    created_at : datetime
    status : str