from fastapi import FastAPI

from app.api.routes import health, auth, admin, shifts, manager, staff, rewards, points

app = FastAPI()

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(shifts.router)
app.include_router(manager.router)
app.include_router(staff.router)
app.include_router(rewards.router)
app.include_router(points.router)