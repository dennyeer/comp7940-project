import asyncio
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from app.config import settings
from app.db import get_message_logs_collection
from app.services.llm_service import generate_reply
from app.services.log_service import save_message_log


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    welcome_message = (
        "Hi! I am CloudTrip AI Bot, your AI travel concierge. ✈️🌍\n\n"
        "I can help you with:\n"
        "- travel itinerary planning\n"
        "- attraction and activity suggestions\n"
        "- transport and packing advice\n"
        "- common travel problems during trips\n\n"
        "Try asking me something like:\n"
        "- Plan a 3-day Tokyo trip for me\n"
        "- What should I do if my flight is delayed?\n"
        "- What should I pack for Bangkok in July?"
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_message = (
        "CloudTrip AI Bot can support two main travel scenarios:\n\n"
        "1. Travel planning\n"
        "- Plan a 5-day Seoul trip\n"
        "- Suggest attractions in Sydney for a weekend\n"
        "- Build a budget itinerary for Bangkok\n\n"
        "2. Travel problem-solving\n"
        "- My flight is delayed. What should I do?\n"
        "- It is raining in Tokyo. What indoor places can I visit?\n"
        "- I lost my passport abroad. What should I do first?\n\n"
        "Available commands:\n"
        "/start - Show welcome message\n"
        "/help - Show this help message\n\n"
        "You can simply send your travel question directly in natural language."
    )
    await update.message.reply_text(help_message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user text messages."""
    if not update.message or not update.effective_user:
        return

    user = update.effective_user
    user_message = update.message.text.strip() if update.message.text else ""

    if not user_message:
        await update.message.reply_text("Please send a text message.")
        return

    collection = get_message_logs_collection()

    try:
        llm_result = generate_reply(user_message)
        reply_text = llm_result["reply_text"]

        await update.message.reply_text(reply_text)

        save_message_log(
            collection=collection,
            telegram_user_id=user.id,
            username=user.username,
            user_message=user_message,
            bot_reply=reply_text,
            response_time_ms=llm_result["response_time_ms"],
            estimated_cost=llm_result["estimated_cost"],
            prompt_tokens=llm_result["prompt_tokens"],
            completion_tokens=llm_result["completion_tokens"],
            status="success",
        )

    except Exception as exc:
        logger.exception("Failed to process message: %s", exc)

        error_reply = (
            "Sorry, I ran into a problem while processing your travel request. "
            "Please try again in a moment."
        )
        await update.message.reply_text(error_reply)

        try:
            save_message_log(
                collection=collection,
                telegram_user_id=user.id,
                username=user.username,
                user_message=user_message,
                bot_reply=None,
                response_time_ms=None,
                estimated_cost=None,
                prompt_tokens=None,
                completion_tokens=None,
                status="error",
            )
        except Exception as db_exc:
            logger.exception("Failed to save error log: %s", db_exc)


def build_bot_application() -> Application:
    """Create and configure the Telegram bot application."""
    application = Application.builder().token(settings.telegram_bot_token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return application


async def run_bot() -> None:
    """Run the Telegram bot in polling mode."""
    application = build_bot_application()

    logger.info("Starting Telegram bot polling...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    while True:
        await asyncio.sleep(3600)