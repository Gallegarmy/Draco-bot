from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger
from .constants import ENTER_START_TIME
from .calendar.telegramcalendar import create_calendar
from .utils import get_username


async def quedada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Add the user that created the event to the dict
    event_id = update.message.message_id
    context.chat_data["current_event_id"] = str(event_id)
    context.chat_data["current"] = {
        "creator_id": update.message.from_user.id,
        "start_date": None,
        "start_time": None,
        "meeting_type": "Open",
        "players": {
            f"{await get_username(update)}":0
        }
    }
    logger.info(f"Building quedada message: message id {event_id}")
    #Starts the routin that will ask for start time, end time and status
    message = "Indique la fecha de inicio"
    reply_markup = create_calendar("start_date")
    await update.message.reply_text(message, reply_markup=reply_markup)
    logger.info("Start time keyboard shown")
    return ENTER_START_TIME