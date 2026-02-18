from fastapi import APIRouter, HTTPException, Query
from app.models.common import DataResponse
from app.services.data_service import DataService

router = APIRouter(prefix="/data")

_service = DataService()


@router.get("/{source}",response_model=DataResponse)
def get_data(source: str) -> DataResponse:
    return _service.get_data(source=source)
