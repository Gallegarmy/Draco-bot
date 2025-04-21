from telegram import Update,  InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import logger
from .message_builder import build_message
from .keyboard_builder import build_keyboard
from shared import joined

async def quedada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    #Add the user that created the event to the dict
    joined[user_id] = {"name": user.username if user.username else user.full_name, "guests": 0}
    logger.info("Building quedada message")
    message = build_message(joined)
    reply_markup = InlineKeyboardMarkup(build_keyboard())
    logger.info("Quedada message built")
    await update.message.reply_text(message, reply_markup=reply_markup)
    logger.info("Quedada message sent")