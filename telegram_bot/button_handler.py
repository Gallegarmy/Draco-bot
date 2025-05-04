import re
from contextlib import suppress

import telegram
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.logger import logger
from datetime import datetime

from .constants import ENTER_START_DATE, ENTER_START_TIME, ENTER_MEETING_TYPE
from .final_message_builder import build_final_message
from .keyboards.keyboard_builder import build_attendance_keyboard
from .keyboards.calendar_keyboard import create_calendar_keyboard
from .keyboards.time_keyboard_builder import build_time_keyboard
from .keyboards.status_keyboard import build_meeting_type_keyboard
from .utils import get_username


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        elif "Open" in action or "Closed" in action:
            message, reply_markup = process_meeting_type(action,context)
            event_message_id = context.chat_data["current_event_id"]
            context.chat_data[event_message_id] = context.chat_data["current"]
            del context.chat_data["current_event_id"]
            del context.chat_data["current"]
            result = ConversationHandler.END

    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    return result


def process_meeting_start_date(action,context):
    # We trim the 'CALENDAR;start_date;' string to insert the date into the context_data dictionary
    start_date = re.sub('CALENDAR;start_date;', '', str(action))
    start_date = datetime.strptime(start_date, '%Y;%m;%d').date()
    context.chat_data["current"]["start_date"] = start_date
    message = "Indique la hora de inicio"
    reply_markup = build_time_keyboard('start_time')
    log_message = "Start time keyboard about to show"
    logger.info(log_message)
    return message, reply_markup

def process_meeting_start_time(action,context):
    message = "Indique si la quedada es abierta o cerrada"
    # We trim the 'Start-' string to insert the hour into the context_data dictionary
    context.chat_data["current"]["start_time"] = re.sub('start_time-', '', str(action))
    # We build the keyboard asking for meeting status
    reply_markup = build_meeting_type_keyboard()
    logger.info("Meeting type keyboad about to show")
    return message, reply_markup

def process_meeting_type(action, context):
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


def is_fullgame(context, event_id):
    current_players = len(context.chat_data[event_id]["players"].keys())
    current_guests = sum(context.chat_data[event_id]["players"].values())
    total_players = current_players + current_guests
    is_full_game = total_players >= int(context.chat_data[event_id]["max_players"])
    return is_full_game
