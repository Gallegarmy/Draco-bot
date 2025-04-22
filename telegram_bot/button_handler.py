from telegram import Update,  InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import logger
from shared import joined,data
from .keyboards.keyboard_builder import build_keyboard
from .final_message_builder import build_final_message
from .keyboards.end_time_keyboard_builder import build_end_keyboard
from .keyboards.status_keyboard import build_status_keyboard
import re

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_id = user.id
    action = query.data

    # Ensure the user is in the dict
    if user_id not in joined:
        joined[user_id] = {"name": user.full_name, "guests": 0}

    if "Start" in action:
        message, reply_markup = await process_meeting_start(action)
    elif "End" in action:
        message, reply_markup = await process_meeting_end(action)
    elif "Open" in action or "Closed" in action:
        message, reply_markup = await process_meeting_type(action)
    else:
        #We handle the event of user joining, leaving, adding or removing a guest
        if action == "join":
            joined[user_id]["guests"] = 0
            await query.answer("You joined!")
            logger.info("User joined")
        elif action == "+1":
            joined[user_id]["guests"] += 1
            await query.answer("You joined with +1!")
            logger.info("+1 guest")
        elif action == "leave":
            if user_id in joined:
                del joined[user_id]
            await query.answer("You left.")
            logger.info("User left")
        elif action == "-1":
            if user_id in joined and joined[user_id]["guests"] > 0:
                joined[user_id]["guests"] -= 1
                await query.answer("Removed one guest.")
                logger.info("-1 guest")
            else:
                await query.answer("No guests to remove.", show_alert=True)
        message = build_final_message(joined,data)
        reply_markup = InlineKeyboardMarkup(build_keyboard())
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')


async def process_meeting_start(action):
    message = "Indique la hora de fin"
    # We trim the 'Start-' string to insert the hour into the shared dictionary
    data["start"] = re.sub('Start-', '', str(action))
    # We build the keyboard asking for an ending time
    reply_markup = InlineKeyboardMarkup(build_end_keyboard())
    logger.info("End time message sent")
    return message, reply_markup


async def process_meeting_end(action):
    # We trim the 'End-' string to insert the hour into the shared dictionary
    data["end"] = re.sub('End-', '', str(action))
    if int(data["start"][0:2]) > int(data["end"][0:2]):
        message = "La hora de finalización no puede ser antes que la hora de inicio, vuelva a indicar la hora de finalización."
        keyboard = build_end_keyboard()
        log_message = "End time was previous to Start time. End message re-sent"
    else:
        message = "Indique si la quedada es abierta o cerrada"
        # We trim the 'End-' string to insert the hour into the shared dictionary
        keyboard = build_status_keyboard()
        log_message = "Status message sent"
    logger.info(log_message)
    reply_markup = InlineKeyboardMarkup(keyboard)
    return message, reply_markup


async def process_meeting_type(action):
    """
    We mark the event as open or closed in the shared dictionary
    :param action:
    :return:
    """
    data["status"] = str(action)
    message = build_final_message(joined, data)
    reply_markup = InlineKeyboardMarkup(build_keyboard())
    logger.info("Final message sent")
    return message, reply_markup

