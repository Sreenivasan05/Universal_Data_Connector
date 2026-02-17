from pydantic import BaseModel
from datetime import datetime

class Customer(BaseModel):
    id: str
    name: str
    email : str
    created_at : datetime
    status : str