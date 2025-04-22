from telegram import Update,  InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import logger
from .final_message_builder import build_final_message
from .keyboards.start_time_keyboard_builder import build_start_keyboard
from shared import joined

async def quedada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    #Add the user that created the event to the dict
    joined[user_id] = {"name": user.username if user.username else user.full_name, "guests": 0}
    logger.info("Building quedada message")
    #Starts the routin that will ask for start time, end time and status
    message = "Indique la hora de inicio"
    reply_markup = InlineKeyboardMarkup(build_start_keyboard())
    await update.message.reply_text(message, reply_markup=reply_markup)
    logger.info("Start time message sent")