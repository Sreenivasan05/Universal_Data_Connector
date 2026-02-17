from pydantic import BaseModel
from datetime import date

class Metrics(BaseModel):
    metric : str
    date : date
    value : str