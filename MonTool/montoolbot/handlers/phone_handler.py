from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from database.db import update_user, email_check
from handlers.profile_handler import profile
from handlers.email_handler import collect_email
from utils.states import PROFILE, WAITING_FOR_CONTACT
from handlers.welcome_handler import welcome
import logging

logger = logging.getLogger("tg_bot")


async def collect_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents PHONE handler
    """
    try:
        phone_button = KeyboardButton("📱 Share Phone Number", request_contact=True)
        keyboard = [[phone_button]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            f"Got your email, {context.user_data["user_name"]}! Now, please provide your phone number:",
            reply_markup=markup)
        logger.info("PHONE is triggered")
        return WAITING_FOR_CONTACT
    except Exception as error:
        logger.error(f"Error in PHONE handler - {error}")


async def create(update, context):
    """
    Updates the database with Telegram profile data if the email is verified
    """
    try:
        if update.message.contact is not None:
            context.user_data["user_phone"] = update.message.contact["phone_number"]
            email_is_valid = await email_check(context.user_data["user_email"])
            if email_is_valid:
                await update_user(context.user_data["user_id"], context.user_data["user_name"],
                                  context.user_data["user_email"],
                                  context.user_data["user_phone"])
                return await profile(update, context)
            else:
                await context.bot.send_message(chat_id=context.user_data["user_id"],
                                               text=f"The email provided '{context.user_data["user_email"]}' does not exist in the Montool Database. Please sign up first!")
                return await welcome(update, context)
    except Exception as error:
        logger.error(f"Error during user update - {error}")
