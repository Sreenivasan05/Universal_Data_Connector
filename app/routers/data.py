from fastapi import APIRouter, HTTPException, Query
from app.models.common import DataResponse
from app.services.data_service import DataService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/data")

_service = DataService()


@router.get(
            "/{source}",
    response_model=DataResponse,
    summary="Query a data source",            
    description="""
    Fetch records from CRM, support, or analytics.
    Results are filtered, sorted, and optimized for voice.
    
    **Sources:**
    - `crm` — customer records, sorted by created_at desc
    - `support` — tickets, sorted by priority then date
    - `analytics` — metrics, raw or aggregated
    """,
    responses={
        200: {"description": "Data returned successfully"},
        404: {"description": "Unknown source"},
        422: {"description": "Invalid query parameters"},
    }
)
def get_data(source: str) -> DataResponse:
    try:
        return _service.get_data(source=source)
    except Exception as exc:
        logger.exception("Unexpected error fetching data from '%s'", source)
        raise HTTPException(status_code=500, detail="Internal server error") from exc
