from fastapi import FastAPI

from app.api.routes import health, auth, admin, shifts

app = FastAPI()

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(shifts.router)