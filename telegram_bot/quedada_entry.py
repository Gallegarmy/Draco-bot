from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger
from .keyboards.time_keyboard_builder import build_time_keyboard
from shared import joined
from .utils import get_username


async def quedada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    #Add the user that created the event to the dict
    joined[user_id] = {"name": await get_username(update), "guests": 0}
    logger.info("Building quedada message")
    #Starts the routin that will ask for start time, end time and status
    message = "Indique la hora de inicio"
    reply_markup = build_time_keyboard('Start')
    await update.message.reply_text(message, reply_markup=reply_markup)
    logger.info("Start time message sent")