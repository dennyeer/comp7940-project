from datetime import datetime
from pymongo.collection import Collection


def save_message_log(
    collection: Collection,
    telegram_user_id: int,
    username: str | None,
    user_message: str,
    bot_reply: str | None,
    response_time_ms: int | None,
    estimated_cost: float | None,
    status: str = "success",
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
) -> str:
    """
    Save one chatbot interaction to MongoDB.
    """
    document = {
        "telegram_user_id": telegram_user_id,
        "username": username,
        "user_message": user_message,
        "bot_reply": bot_reply,
        "response_time_ms": response_time_ms,
        "estimated_cost": estimated_cost,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "status": status,
        "created_at": datetime.utcnow(),
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)