import telegram
from ..utils import get_username, is_fullgame
from utils.logger import logger
from ..keyboards.keyboard_builder import build_attendance_keyboard
from ..final_message_builder import build_final_message
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from contextlib import suppress


async def attendance_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    username = await get_username(update)
    event_id, action = query.data.split(',')
    alert, response_msg = handle_meeting_action(event_id, action, username,context)
    await query.answer(response_msg, show_alert=alert)
    logger.info(response_msg)

    message = build_final_message(context.chat_data[event_id])
    reply_markup = build_attendance_keyboard(event_id)
    with suppress(telegram.error.BadRequest):
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

def handle_meeting_action(event_id, action, username, context):
    alert = False
    response_msg = ''
    # We handle the event of user joining, leaving, adding or removing a guest
    found = any(username in user for user in context.chat_data[event_id]["players"])
    #We check if the user is already present on the list
    if found:
        #We get the index of the person already present on the list
        if action == "join":
            response_msg = "Usuario ya agregado en la lista"
        elif action == "+1":
            if is_fullgame(context, event_id):
                response_msg = "Partida sin sitios disponibles"
            else:
                #We add +1 to the guest field
                context.chat_data[event_id]["players"][username] += 1
                response_msg = f"{username} +1!"
        elif action == "leave":
            #We remove the user from the list
            del context.chat_data[event_id]["players"][username]
            response_msg = "Usuario quitado de la quedada"
        elif action == "-1":
            #We verify if the user has guests
            if context.chat_data[event_id]["players"][username] > 0:
                context.chat_data[event_id]["players"][username] -= 1
            else:
                response_msg = "Sin invitados que quitar"
                alert = True
    else:
        if action == 'join':
            if is_fullgame(context, event_id):
                response_msg = "Partida sin sitios disponibles"
            else:
                context.chat_data[event_id]["players"][username] = 0
                response_msg = f"{username} joined!"
        elif action == "+1":
            if is_fullgame(context, event_id):
                response_msg = "Partida sin sitios disponibles"
            else:
                context.chat_data[event_id]["players"][username] += 0
                response_msg = f"{username} +1!"
        elif action == '-1':
            response_msg = "El usuario no está en la lista"
    return alert, response_msg