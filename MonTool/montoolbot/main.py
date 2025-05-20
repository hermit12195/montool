import os
import sys

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler

from handlers import start_handler, back_handler, profile_handler, name_handler, phone_handler, redirect_handler, \
    reply_handler, welcome_handler, email_handler
from utils.states import HANDLE_OPTION, ASK_PHONE, ASK_NAME, PROFILE, HANDLE_OPTION2, ADMIN_REDIRECT, BACK, WELCOME, \
    WAITING_FOR_CONTACT, ASK_EMAIL

import logging
from logging.config import dictConfig
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MonTool.settings')

dictConfig(settings.LOGGING)

logger = logging.getLogger("tg_bot")

load_dotenv()
TOKEN = os.getenv("TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_handler.start),
                  CommandHandler("reply", reply_handler.reply)],
    states={
        WELCOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, welcome_handler.welcome)],
        HANDLE_OPTION: [CallbackQueryHandler(welcome_handler.handle_option)],
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_handler.collect_name)],
        ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_handler.collect_email)],
        ASK_PHONE: [MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), phone_handler.collect_phone)],
        PROFILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_handler.profile)],
        HANDLE_OPTION2: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_handler.handle_option)],
        ADMIN_REDIRECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, redirect_handler.redirect)],
        BACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, back_handler.back)],
        WAITING_FOR_CONTACT: [MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), phone_handler.create)]
    },
    fallbacks=[CommandHandler("back", back_handler.back)],
    allow_reentry=True,
)

app.add_handler(conv_handler)
logger.info("Bot is running...")

app.run_polling()
