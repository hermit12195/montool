from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger("tg_bot")


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents ABOUT handler
    """
    try:
        logger.info("ABOUT handler is triggered")
        await update.message.reply_text("We are professionals!")
    except Exception as error:
        logger.error(f"Error in ABOUT handler - {error}")
