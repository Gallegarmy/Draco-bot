import re

from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger
from shared import joined,data
from datetime import datetime
from .final_message_builder import build_final_message
from .keyboards.keyboard_builder import build_keyboard
from .keyboards.time_keyboard_builder import build_time_keyboard
from .keyboards.status_keyboard import build_status_keyboard
from .calendar.telegramcalendar import create_calendar
from .utils import get_username


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    username = await get_username(update)
    action = query.data


    if "start_date" in action:
        message, reply_markup = process_meeting_start_date(action,context)
    elif "start_time" in action:
        message, reply_markup = process_meeting_start_time(action,context)
    elif "end_date" in action:
        message, reply_markup = process_meeting_end_date(action,context)
    elif "end_time" in action:
        message, reply_markup = process_meeting_end_time(action,context)
    elif "Open" in action or "Closed" in action:
        message, reply_markup = process_meeting_type(action,context)
    else:
        print(action)
        alert, response_msg = handle_meeting_action(action, username,context)
        await query.answer(response_msg, show_alert=alert)
        logger.info(response_msg)
        message = build_final_message(context)
        reply_markup = build_keyboard()
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')


def process_meeting_start_date(action,context):
    # We trim the 'CALENDAR;start_date;' string to insert the date into the context_data dictionary
    context.chat_data["start_date"] = re.sub('CALENDAR;start_date;', '', str(action))
    print(context.chat_data)
    start_date = datetime.strptime(context.chat_data["start_date"], '%Y;%m;%d').date()
    if start_date >= datetime.today().date() :
        message = "Indique la hora de inicio"
        reply_markup = build_time_keyboard('start_time')
        log_message = "Start time message sent"
    else:
        message = "La fecha de inicio no puede ser anterior a la fecha actual"
        reply_markup = create_calendar("start_date")
        log_message = "Start date was previous to current date. Start date message re-sent"
    logger.info(log_message)
    return message, reply_markup

def process_meeting_start_time(action,context):
    message = "Indique la fecha de fin"
    # We trim the 'Start-' string to insert the hour into the context_data dictionary
    context.chat_data["start_time"] = re.sub('start_time-', '', str(action))
    # We build the keyboard asking for an ending time
    reply_markup = create_calendar('end_date')
    logger.info("End date message sent")
    return message, reply_markup

def process_meeting_end_date(action,context):
    # We trim the 'CALENDAR;end_date;' string to insert the date into the context_data dictionary
    context.chat_data["end_date"] = re.sub('CALENDAR;end_date;', '', str(action))
    print(context.chat_data)
    start_date = datetime.strptime(context.chat_data["start_date"], '%Y;%m;%d').date()
    end_date = datetime.strptime(context.chat_data["end_date"], '%Y;%m;%d').date()
    if start_date <= end_date :
        message = "Indique la hora de fin"
        reply_markup = build_time_keyboard('end_time')
        log_message = "End time message sent"
    else:
        message = "La fecha de fin no puede ser anterior a la fecha de inicio"
        reply_markup = create_calendar("start_date")
        log_message = "End date was previous to Start date. End date message re-sent"
    logger.info(log_message)
    return message, reply_markup



def process_meeting_end_time(action,context):
    # We trim the 'End-' string to insert the hour into the context_data dictionary
    context.chat_data["end_time"] = re.sub('end_time-', '', str(action))
    if int(context.chat_data["start_time"][0:2]) > int(context.chat_data["end_time"][0:2]):
        message = "La hora de finalización no puede ser antes que la hora de inicio, vuelva a indicar la hora de finalización."
        keyboard = build_time_keyboard('end_time')
        log_message = "End time was previous to Start time. End message re-sent"
    else:
        message = "Indique si la quedada es abierta o cerrada"
        # We trim the 'End-' string to insert the hour into the shared dictionary
        keyboard = build_status_keyboard()
        log_message = "Status message sent"
    logger.info(log_message)
    reply_markup = keyboard
    return message, reply_markup


def process_meeting_type(action,context):
    """
    We mark the event as open or closed in the shared dictionary
    :param action:
    :return:
    """
    context.chat_data["status"] = str(action)
    message = build_final_message(context)
    reply_markup = build_keyboard()
    logger.info("Final message sent")
    return message, reply_markup


def handle_meeting_action(action, username, context):
    alert = False
    response_msg = ''
    # We handle the event of user joining, leaving, adding or removing a guest
    found = any(username in user for user in context.chat_data["joined"])
    if found:
        #Obtenemos el index del usuario ya presente en la lista
        index = next((i for i, item in enumerate(context.chat_data["joined"]) if username in item[0]), -1)
        if action == "join":  
            response_msg = "Usuario ya agregado en la lista"
           # else:
           #     response_msg = f"{username} joined!"
           #     context.chat_data["joined"].append([username,0])
        elif action == "+1":
            #Añadimos uno al campo de invitados
            context.chat_data["joined"][index][1] += 1
            #else:
            #    context.chat_data["joined"].append([username,1])
            response_msg = f"{username} +1!"
        elif action == "leave":
            #Quitamos al usuario de la lista
            context.chat_data["joined"].pop(index)
            response_msg = "Usuario quitado de la quedada"
            #else:
            #    response_msg = "El usuario no está en la lista en la lista"
        elif action == "-1":
            #Obtenemos el index del usuario ya presente en la lista
            index = next((i for i, item in enumerate(context.chat_data["joined"]) if username in item[0]), -1)
            if context.chat_data["joined"][index][1] == 0:
                response_msg = "Sin invitados que quitar"
                alert = True
            else:
                context.chat_data["joined"][index][1] -= 1
    return alert, response_msg
