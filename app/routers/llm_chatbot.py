from fastapi import APIRouter
from app.services.llm_agent import LLMSERVICE
from app.services.data_service import DataService

router = APIRouter()

@router.get("/chat/")
def chatbot(user_query:str):
    data_service = DataService()
    llm_service = LLMSERVICE(data_service)
    reply = llm_service.run_agent(user_query)
    return reply