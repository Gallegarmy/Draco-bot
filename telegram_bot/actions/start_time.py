from utils.logger import logger
from ..constants import ENTER_MEETING_TYPE
from ..keyboards.status_keyboard import build_meeting_type_keyboard
import re
from datetime import datetime
from telegram.ext import ContextTypes, ConversationHandler
from telegram import InlineKeyboardMarkup, Update


async def process_meeting_start_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ConversationHandler:
    query = update.callback_query
    if str(query.from_user.id) != str(context.chat_data["current"]["creator_id"]):
        return


    action = query.data
    # We trim the 'Start-' string to insert the hour into the context_data dictionary
    context.chat_data["current"]["start_time"] = re.sub('start_time-', '', str(action))
    # We build the keyboard asking for meeting status
    logger.info("Meeting type keyboad about to show")

    reply_markup = build_meeting_type_keyboard()
    message = "Indique si la quedada es abierta o cerrada"
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    result = ENTER_MEETING_TYPE
    return result