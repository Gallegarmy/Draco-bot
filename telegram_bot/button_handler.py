import re

from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger
from datetime import datetime
from .final_message_builder import build_final_message
from .keyboards.keyboard_builder import build_keyboard
from .keyboards.time_keyboard_builder import build_time_keyboard
from .keyboards.status_keyboard import build_status_keyboard
from .calendar.telegramcalendar import create_calendar, process_calendar_selection
from .utils import get_username


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    username = await get_username(update)
    action = query.data
    
    if "PREV-MONTH" in action or "NEXT-MONTH" in action:
        arguments = action.split(';')
        if "start_date" in context.chat_data:            
            reply_markup = create_calendar("end_date",arguments[2],arguments[3])
            message = "Indique la fecha de fin"
        else:
            reply_markup = create_calendar("start_date",arguments[2],arguments[3])
            message="Indique la fecha de inicio"
    else:
        if "start_date" in action:
            message, reply_markup = process_meeting_start_date(action,context)
        elif "start_time" in action:
            message, reply_markup = process_meeting_start_time(action,context)
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
    message = "Indique si la quedada es abierta o cerrada"
    # We trim the 'Start-' string to insert the hour into the context_data dictionary
    context.chat_data["start_time"] = re.sub('start_time-', '', str(action))
    # We build the keyboard asking for meeting status
    reply_markup = build_status_keyboard()
    logger.info("Status message sent")
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
    #We check if the user is already present on the list
    if found:
        #We get the index of the person already present on the list
        index = next((i for i, item in enumerate(context.chat_data["joined"]) if username in item[0]), -1)
        if action == "join":  
            response_msg = "Usuario ya agregado en la lista"
        elif action == "+1":
            #We add +1 to the guest field
            context.chat_data["joined"][index][1] += 1
            response_msg = f"{username} +1!"
        elif action == "leave":
            #We remove the user from the list
            context.chat_data["joined"].pop(index)
            response_msg = "Usuario quitado de la quedada"
        elif action == "-1":
            #We verify if the user has guests
            if context.chat_data["joined"][index][1] == 0:
                response_msg = "Sin invitados que quitar"
                alert = True
            else:
                context.chat_data["joined"][index][1] -= 1
    else:
        if action == 'join':            
            context.chat_data["joined"].append([username,0])
            response_msg = f"{username} joined!"
        elif action == "+1":
            context.chat_data["joined"].append([username,1])
            response_msg = f"{username} +1!"
        elif action == '-1':
            response_msg = "El usuario no está en la lista"
    return alert, response_msg
