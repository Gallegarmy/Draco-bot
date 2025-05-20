from utils.logger import logger
from ..apis.gcalendar import create_event
from ..constants import ENTER_CONFIRMATION
from ..keyboards.keyboard_builder import build_attendance_keyboard
from ..final_message_builder import build_final_message
import re
from datetime import datetime
from telegram.ext import ContextTypes, ConversationHandler
from telegram import InlineKeyboardMarkup, Update


async def process_meeting_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    action = query.data
    if str(query.from_user.id) != str(context.chat_data["current"]["creator_id"]):
        return

    context.chat_data["current"]["meeting_type"] = str(action)
    message = build_final_message(context.chat_data["current"])
    reply_markup = build_attendance_keyboard(context.chat_data["current_event_id"])
    logger.info("Summary keyboard about to show")
    event_message_id = context.chat_data["current_event_id"]

    # Persists the collected game info and creates the GCalendar event
    context.chat_data[event_message_id] = context.chat_data["current"]
    create_event(context.chat_data[event_message_id])

    # Cleans the draft game infoso that another game could be created
    del context.chat_data["current_event_id"]
    del context.chat_data["current"]
    result = ENTER_CONFIRMATION

    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    return result
