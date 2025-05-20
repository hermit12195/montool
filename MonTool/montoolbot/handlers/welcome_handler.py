from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from database.db import user_list
from handlers.profile_handler import profile
from utils.states import HANDLE_OPTION, ASK_NAME
import logging

logger = logging.getLogger("tg_bot")


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents WELCOME handler
    """
    try:
        logger.info("WELCOME handler is triggered")
        keyboard = [
            [InlineKeyboardButton("My Profile", callback_data="profile")],
            [InlineKeyboardButton("About Us", callback_data="about")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Took you back to the Welcome Menu", reply_markup=ReplyKeyboardRemove())
        await update.message.reply_text("Choose option:", reply_markup=markup)
        return HANDLE_OPTION
    except Exception as error:
        logger.error(f"Error in WELCOME handler - {error}")


async def handle_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Provides ability to check user`s profile and get ABOUT US information
    """
    try:
        logger.info("HANDLE OPTION in WELCOME handler is triggered")
        query = update.callback_query
        option = query.data
        if option == "about":
            await context.bot.send_message(chat_id=query.message.chat.id, text="We are professionals!")
        elif option == "profile":
            user_id = update.effective_user.id
            context.user_data["user_id"] = user_id
            user = await user_list(user_id)
            if user:
                user = user[0]
                await context.bot.send_message(chat_id=query.message.chat.id,
                                               text=f"Hope you are fine today, {user["tg_name"]}!")
                context.user_data["user_id"] = user['tg_id']
                context.user_data["user_name"] = user['tg_name']
                context.user_data["user_email"] = user['email']
                context.user_data["user_phone"] = user['phone']
                return await profile(update, context)
            else:
                await context.bot.send_message(chat_id=query.message.chat.id,
                                               text=f"Well, you don`t have profile yet:(\n But don`t worry, we`ll handle it in a moment.\n Please provide your name:")
                return ASK_NAME
    except Exception as error:
        logger.error(f"Error in HANDLE OPTION/WELCOME handler - {error}")
