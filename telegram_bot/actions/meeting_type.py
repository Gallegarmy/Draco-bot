from utils.logger import logger
from ..keyboards.keyboard_builder import build_attendance_keyboard
from ..final_message_builder import build_final_message
import re
from datetime import datetime
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup

def process_meeting_type(action: str,context: ContextTypes.DEFAULT_TYPE) -> (str, InlineKeyboardMarkup):
    """
    We mark the event as open or closed in the shared dictionary
    :param action:
    :param context:
    :return:
    """
    context.chat_data["current"]["meeting_type"] = str(action)
    message = build_final_message(context.chat_data["current"])
    reply_markup = build_attendance_keyboard(context.chat_data["current_event_id"])
    logger.info("Summary keyboard about to show")
    return message, reply_markup