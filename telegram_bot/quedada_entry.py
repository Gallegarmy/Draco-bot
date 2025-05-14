from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger
from .constants import MEETING_NAME
from .utils import get_username


async def quedada(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    #Add the user that created the event to the dict
    event_id = update.message.message_id
    context.chat_data["current_event_id"] = str(event_id)
    context.chat_data["edit_id"] = None
    context.chat_data["current"] = {
        "creator_id": update.message.from_user.id,
        "meeting_name": None,
        "meeting_description": None,
        "max_players": 30,
        "start_date": None,
        "start_time": None,
        "meeting_type": "Open",
        "players": {
            f"{await get_username(update)}":0
        }
    }
    logger.info(f"Building quedada message: message id {event_id}")
    #Starts the routin that will ask for start time, end time and status
    await update.message.reply_text("¿Cuál es el nombre de la quedada?")
    return MEETING_NAME
