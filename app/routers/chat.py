from google.api_core.exceptions import ResourceExhausted
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.llm_agent import LLMService
from app.services.data_service import DataService
import logging



logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

def get_data_service() -> DataService:
    return DataService()

def get_llm_service(data_service: DataService = Depends(get_data_service),) -> LLMService:
    return LLMService(data_service=data_service)

@router.post("/", response_model=ChatResponse)
def chat(body: ChatRequest, llm_service: LLMService = Depends(get_llm_service)):
    print("iam here")
    try:
        reply = llm_service.run_agent(body.query)
        return ChatResponse(response=reply)
    except ResourceExhausted:
        raise HTTPException(
            status_code=429,
            detail="AI service is busy, please try again in a few seconds."
        )
    except Exception as exc:
        logger.exception("Agent error for query: %s", body.query)
        raise HTTPException(
            status_code=500, 
            detail="Agent error"
        )
