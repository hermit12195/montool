from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger("tg_bot")


async def collect_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents EMAIL handler
    """
    try:
        from handlers.phone_handler import collect_phone
        user_email = update.message.text
        context.user_data["user_email"] = user_email
        logger.info("EMAIL handler is triggered")
        return await collect_phone(update, context)
    except Exception as error:
        logger.error(f"Error in EMAIL handler - {error}")
