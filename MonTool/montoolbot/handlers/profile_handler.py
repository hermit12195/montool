import uuid

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from database.db import server_list
from handlers.back_handler import back
from utils.states import HANDLE_OPTION2, ADMIN_REDIRECT, BACK
import logging

logger = logging.getLogger("tg_bot")


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents PROFILE handler
    """
    try:
        logger.info("PROFILE handler is triggered")
        await context.bot.send_message(chat_id=context.user_data["user_id"], text=
        f"Profile loaded!\n"
        f"Name: {context.user_data['user_name']}\n"
        f"Email: {context.user_data['user_email']}\n"
        f"Phone: {context.user_data['user_phone']}"
                                       )
        keyboard = [["My Servers", "My Balance"], ["Support", "Back to Welcome Menu"]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(
            chat_id=context.user_data["user_id"],
            text="Choose option:",
            reply_markup=markup
        )
        return HANDLE_OPTION2
    except Exception as error:
        logger.error(f"Error in PROFILE handler - {error}")


async def handle_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Returns the list of servers of the authorised user, provides ability to check the user balance and contact admin.
    """
    try:
        logger.info("HANDLE OPTION in PROFILE handler is triggered")
        option = update.message.text
        if option == "My Servers":
            s_list = await server_list(context.user_data["user_id"])
            if s_list:
                await context.bot.send_message(chat_id=context.user_data["user_id"],
                                               text=f"Here is the list of your servers:")
                for s in s_list:
                    await context.bot.send_message(chat_id=context.user_data["user_id"],
                                                   text=f'🖥️<b>{s["server_name"]}</b>',
                                                   parse_mode=ParseMode.HTML, )
                    await context.bot.send_message(chat_id=context.user_data["user_id"],
                                                   text=f'IP: {s["server_ip"]}',
                                                   parse_mode=ParseMode.HTML, )
                    await context.bot.send_message(chat_id=context.user_data["user_id"],
                                                   text=f'OS: {s["os_name"]}',
                                                   parse_mode=ParseMode.HTML, )
                    await context.bot.send_message(chat_id=context.user_data["user_id"],
                                                   text=f'Status: {s["status"]}',
                                                   parse_mode=ParseMode.HTML, )
            else:
                await context.bot.send_message(chat_id=context.user_data["user_id"],
                                               text=f"You don`t have any servers monitored yet:(")
        elif option == "Support":
            context.user_data["case_id"] = uuid.uuid4().hex[:8]
            await update.message.reply_text("Please explain in detail the matter of your request:")
            return ADMIN_REDIRECT
        elif option == "My Balance":
            await context.bot.send_message(chat_id=context.user_data["user_id"],
                                           text="Common, man! You are homeless, you have zero balance:)")
        elif option == "Back to Welcome Menu":
            return await back(update, context)
    except Exception as error:
        logger.error(f"Error in HANDLE OPTION/PROFILE handler - {error}")
