from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from telegram_bot.final_message_builder import build_final_message
from telegram_bot.keyboards.keyboard_builder import build_attendance_keyboard
from utils.logger import logger
from telegram_bot.apis.gcalendar import create_event


async def process_confirmation(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    action = query.data
    if str(query.from_user.id) != str(context.chat_data["current"]["creator_id"]):
        return

    if action == "submit":
        event_message_id = context.chat_data["current_event_id"]

        # Persists the collected game info and creates the GCalendar event
        context.chat_data[event_message_id] = context.chat_data["current"]

        logger.info("Summary keyboard about to show")
        message = build_final_message(context.chat_data["current"])
        message = "¿Desea confirmar creación de la partida?\n" + message
        reply_markup = build_attendance_keyboard(context.chat_data["current_event_id"])
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

        create_event(context.chat_data[event_message_id])
    else:
        await query.edit_message_text(f"Creación de partida '{context.chat_data['current']['meeting_name']}' cancelada", parse_mode='Markdown')

    # Cleans the draft game info so that another game could be created
    del context.chat_data["current_event_id"]
    del context.chat_data["current"]

    result = ConversationHandler.END
    return result
