from utils.logger import logger
from ..constants import ENTER_START_TIME, ENTER_START_DATE
from ..keyboards.calendar_keyboard import create_calendar_keyboard
from ..keyboards.time_keyboard_builder import build_time_keyboard
import re
from datetime import datetime
from telegram.ext import ContextTypes, ConversationHandler
from telegram import InlineKeyboardMarkup, Update

async def process_meeting_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler:
    query = update.callback_query
    action = query.data
    if str(query.from_user.id) != str(context.chat_data["current"]["creator_id"]):
        return

    if any(x in action for x in ("PREV-MONTH", "NEXT-MONTH")):
        arguments = action.split(';')
        year = arguments[2]
        month = arguments[3]
        date_type = "start_date"

        reply_markup = create_calendar_keyboard(date_type, year, month)
        message="Indique la fecha de inicio"
        result = ENTER_START_DATE
    else:
        # We trim the 'CALENDAR;start_date;' string to insert the date into the context_data dictionary
        start_date = re.sub('CALENDAR;start_date;', '', str(action))
        start_date = datetime.strptime(start_date, '%Y;%m;%d').date()
        context.chat_data["current"]["start_date"] = start_date

        log_message = "Start time keyboard about to show"
        logger.info(log_message)

        reply_markup = build_time_keyboard('start_time')
        message = "Indique la hora de inicio"
        result = ENTER_START_TIME

    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    return result