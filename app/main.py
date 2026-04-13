from fastapi import FastAPI
from app.routes.health import router as health_router

app = FastAPI(title="CloudCampus AI Bot")

app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "CloudCampus AI Bot is running."}