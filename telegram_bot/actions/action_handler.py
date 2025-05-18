from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from ..apis.gcalendar import create_event
from ..constants import ENTER_START_DATE, ENTER_START_TIME, ENTER_MEETING_TYPE
from ..keyboards.calendar_keyboard import create_calendar_keyboard
from .start_date import process_meeting_start_date
from .start_time import process_meeting_start_time
from .meeting_type import process_meeting_type



async def action_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler:
    query = update.callback_query
    action = query.data
    if str(query.from_user.id) != str(context.chat_data["current"]["creator_id"]):
        return

    if any(x in action for x in ("PREV-MONTH", "NEXT-MONTH")):
        arguments = action.split(';')
        year = arguments[2]
        month = arguments[3]
        date_type = "start_date"
        message="Indique la fecha de inicio"
        reply_markup = create_calendar_keyboard(date_type, year, month)
        result = ENTER_START_DATE
    else:
        if "start_date" in action:
            message, reply_markup = process_meeting_start_date(action, context)
            result = ENTER_START_TIME
        elif "start_time" in action:
            message, reply_markup = process_meeting_start_time(action, context)
            result = ENTER_MEETING_TYPE
        elif "Abierta" in action or "Cerrada" in action:
            message, reply_markup = process_meeting_type(action,context)
            event_message_id = context.chat_data["current_event_id"]

            # Persists the collected game info and creates the GCalendar event
            context.chat_data[event_message_id] = context.chat_data["current"]
            create_event(context.chat_data[event_message_id])

            # Cleans the draft game infoso that another game could be created
            del context.chat_data["current_event_id"]
            del context.chat_data["current"]
            result = ConversationHandler.END

    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    return result







