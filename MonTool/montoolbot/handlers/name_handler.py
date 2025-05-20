from telegram import Update
from telegram.ext import ContextTypes

from utils.states import ASK_EMAIL
import logging

logger = logging.getLogger("tg_bot")


async def collect_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents NAME handler
    """
    try:
        user_name = update.message.text
        context.user_data["user_name"] = user_name
        await update.message.reply_text(
            f"Got your name, {context.user_data["user_name"]}! \nPlease provide your email (!Should be the same as used in MonTool service!):")
        logger.info("NAME handler is triggered")
        return ASK_EMAIL
    except Exception as error:
        logger.error(f"Error in NAME handler - {error}")
