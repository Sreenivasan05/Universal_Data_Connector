from fastapi import FastAPI
from app.routers import health, data
import uvicorn

app = FastAPI(title="Universal Data connector")

app.include_router(health.router)
app.include_router(data.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)