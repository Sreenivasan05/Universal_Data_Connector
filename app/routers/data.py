from fastapi import APIRouter, HTTPException, Query
from app.models.common import DataResponse
from app.services.data_service import DataService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/data")

_service = DataService()


@router.get("/{source}",response_model=DataResponse)
def get_data(source: str) -> DataResponse:
    try:
        return _service.get_data(source=source)
    except Exception as exc:
        logger.exception("Unexpected error fetching data from '%s'", source)
        raise HTTPException(status_code=500, detail="Internal server error") from exc
