from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "cloudcampus-ai-bot",
        "database": "mongodb",
        "llm_provider": "hkbu_ai_api",
    }


@router.get("/ready")
def readiness_check():
    return {
        "status": "ready",
    }