from fastapi import FastAPI
from app.routes.health import router as health_router

app = FastAPI(title="CloudTrip AI Bot")

app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "CloudTrip AI Bot is running."}