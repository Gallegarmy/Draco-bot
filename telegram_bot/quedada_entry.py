from telegram import Update,  InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import structlog
logger = structlog.get_logger()
from .message_builder import build_message
from .keyboard_builder import build_keyboard

async def quedada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Building quedada message")
    message = build_message()
    reply_markup = InlineKeyboardMarkup(build_keyboard())
    logger.info("Quedada message built")
    await update.message.reply_text(message, reply_markup=reply_markup)
    logger.info("Quedada message sent")