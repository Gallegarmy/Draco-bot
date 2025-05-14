from utils.logger import logger
from ..keyboards.status_keyboard import build_meeting_type_keyboard
import re
from datetime import datetime
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup


def process_meeting_start_time(action: str,context: ContextTypes.DEFAULT_TYPE) -> (str, InlineKeyboardMarkup):
    if context.chat_data.get("edit_id", None) is None:    
        event_message_id = "current"
    else:
        event_message_id = context.chat_data["edit_id"]
    message = "Indique si la quedada es abierta o cerrada"
    # We trim the 'Start-' string to insert the hour into the context_data dictionary
    context.chat_data[event_message_id]["start_time"] = re.sub('start_time-', '', str(action))
    # We build the keyboard asking for meeting status
    reply_markup = build_meeting_type_keyboard()
    logger.info("Meeting type keyboad about to show")
    return message, reply_markup