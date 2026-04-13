import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    telegram_bot_token: str
    hkbu_api_key: str
    hkbu_base_url: str
    hkbu_model: str
    hkbu_api_ver: str
    mongodb_uri: str
    mongodb_db_name: str
    mongodb_collection_name: str
    admin_telegram_user_id: str
    app_env: str
    port: int

    @staticmethod
    def from_env() -> "Settings":
        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        hkbu_api_key = os.getenv("HKBU_API_KEY", "").strip()
        hkbu_base_url = os.getenv("HKBU_BASE_URL", "").strip()
        hkbu_model = os.getenv("HKBU_MODEL", "").strip()
        hkbu_api_ver = os.getenv("HKBU_API_VER", "").strip()

        mongodb_uri = os.getenv("MONGODB_URI", "").strip()
        mongodb_db_name = os.getenv("MONGODB_DB_NAME", "cloudcampus_ai").strip()
        mongodb_collection_name = os.getenv("MONGODB_COLLECTION_NAME", "message_logs").strip()

        admin_telegram_user_id = os.getenv("ADMIN_TELEGRAM_USER_ID", "").strip()
        app_env = os.getenv("APP_ENV", "development").strip()
        port = int(os.getenv("PORT", "8000"))

        if not telegram_bot_token:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN.")
        if not hkbu_api_key:
            raise ValueError("Missing HKBU_API_KEY.")
        if not hkbu_base_url:
            raise ValueError("Missing HKBU_BASE_URL.")
        if not hkbu_model:
            raise ValueError("Missing HKBU_MODEL.")
        if not hkbu_api_ver:
            raise ValueError("Missing HKBU_API_VER.")
        if not mongodb_uri:
            raise ValueError("Missing MONGODB_URI.")

        return Settings(
            telegram_bot_token=telegram_bot_token,
            hkbu_api_key=hkbu_api_key,
            hkbu_base_url=hkbu_base_url,
            hkbu_model=hkbu_model,
            hkbu_api_ver=hkbu_api_ver,
            mongodb_uri=mongodb_uri,
            mongodb_db_name=mongodb_db_name,
            mongodb_collection_name=mongodb_collection_name,
            admin_telegram_user_id=admin_telegram_user_id,
            app_env=app_env,
            port=port,
        )


settings = Settings.from_env()