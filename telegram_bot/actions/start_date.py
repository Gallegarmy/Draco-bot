from utils.logger import logger
from ..keyboards.time_keyboard_builder import build_time_keyboard
import re
from datetime import datetime
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup

def process_meeting_start_date(action: str,context: ContextTypes.DEFAULT_TYPE) -> (str, InlineKeyboardMarkup):
    # We trim the 'CALENDAR;start_date;' string to insert the date into the context_data dictionary
    start_date = re.sub('CALENDAR;start_date;', '', str(action))
    start_date = datetime.strptime(start_date, '%Y;%m;%d').date()
    context.chat_data["current"]["start_date"] = start_date
    message = "Indique la hora de inicio"
    reply_markup = build_time_keyboard('start_time')
    log_message = "Start time keyboard about to show"
    logger.info(log_message)
    return message, reply_markup