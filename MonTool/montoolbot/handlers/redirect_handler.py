import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from handlers.back_handler import back
import logging

logger = logging.getLogger("tg_bot")


async def redirect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents REDIRECT handler, handles communication with admin user.
    """
    try:
        logger.info("REDIRECT handler is triggered")
        keyboard = [["Back to Welcome Menu"]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        if not context.user_data["case_id"].endswith("replied") and update.message.text != "Back to Welcome Menu":
            await update.message.reply_text(
                f"The Support case #{context.user_data["case_id"]} was submitted! Administrator will contact you soon!",
                reply_markup=markup)
            await context.bot.send_message(chat_id=os.getenv("ADMIN_ID"),
                                           text=f"New Support case from {context.user_data["user_name"]} | @{update.message.from_user["username"]}"
                                                f" | ID: {context.user_data["user_id"]}. \n Context: {update.message.text}")
            context.user_data["case_id"] += "replied"
            return await handle_option(update, context)
        else:
            await context.bot.send_message(chat_id=os.getenv("ADMIN_ID"),
                                           text=update.message.text)
            return await handle_option(update, context)
    except Exception as error:
        logger.error(f"Error in REDIRECT handler - {error}")


async def handle_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles return to Welcome Menu
    """
    try:
        logger.info("HANDLE OPTION in REDIRECT is triggered")
        if update.message.text == "Back to Welcome Menu":
            return await back(update, context)
    except Exception as error:
        logger.error(f"Error in HANDLE OPTION/REDIRECT handler - {error}")
