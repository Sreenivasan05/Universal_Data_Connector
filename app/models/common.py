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
    model_config = {"json_schema_extra": {
        "example": {                                        
            "data": [{"customer_id": 1, "name": "Alice"}],
            "metadata": {
                "total_results": 50,
                "returned_results": 10,
                "source": "crm",
                "data_type": "tabular_crm",
                "data_freshness": "2026-02-20 10:00 UTC",
                "context": "Showing 10 of 50 results"
            }
        }
    }}
    data: list[Any]
    metadata: Metadata