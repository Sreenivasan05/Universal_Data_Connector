from fastapi import FastAPI
from app.routers import health

app = FastAPI(title="Universal Data connector")

app.include_router(health.router)
