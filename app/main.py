from fastapi import FastAPI

from app.api.routes import health, auth

app = FastAPI()

app.include_router(health.router)
app.include_router(auth.router)