from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger("tg_bot")


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents BACK handler
    """
    try:
        from .welcome_handler import welcome
        logger.info("BACK handler is triggered")
        return await welcome(update, context)
    except Exception as error:
        logger.error(f"Error in BACK handler - {error}")
