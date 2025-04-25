from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger
from .keyboards.time_keyboard_builder import build_time_keyboard
from .calendar.telegramcalendar import create_calendar
from shared import joined
from .utils import get_username


async def quedada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    #Add the user that created the event to the dict
    context.chat_data["joined"] = [[f"{await get_username(update)}",0]]
    logger.info("Building quedada message")
    #Starts the routin that will ask for start time, end time and status
    message = "Indique la hora de inicio"
    reply_markup = create_calendar("start_date")
    await update.message.reply_text(message, reply_markup=reply_markup)
    logger.info("Start time message sent")