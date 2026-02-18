from pydantic import BaseModel
from typing import Any, List

class Metadata(BaseModel):
    total_results: int
    returned_results: int
    data_freshness: str
    data_type: str = "Unknown"
    source: str = ""
    context : str = ""

class DataResponse(BaseModel):
    data: List[Any]
    metadata: Metadata
