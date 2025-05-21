from ..constants import ENTER_CONFIRMATION
from ..keyboards.confirm_keyboard import build_confirm_keyboard
from ..final_message_builder import build_final_message
from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update


async def process_meeting_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    action = query.data
    if str(query.from_user.id) != str(context.chat_data["current"]["creator_id"]):
        return

    context.chat_data["current"]["meeting_type"] = str(action)
    message = build_final_message(context.chat_data["current"])
    reply_markup = build_confirm_keyboard()

    result = ENTER_CONFIRMATION

    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    return result
