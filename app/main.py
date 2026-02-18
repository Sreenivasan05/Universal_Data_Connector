from fastapi import FastAPI
from app.routers import health, data, llm_chatbot
import uvicorn

app = FastAPI(title="Universal Data connector")

app.include_router(health.router)
app.include_router(data.router)
app.include_router(llm_chatbot.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)