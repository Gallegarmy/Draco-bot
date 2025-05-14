
from telegram import Update
from telegram.ext import ContextTypes
from .constants import MEETING_DESCRIPTION, ENTER_START_TIME, ENTER_NUM_PLAYERS
from utils.logger import logger
from .keyboards.calendar_keyboard import create_calendar_keyboard
from .keyboards.players_keyboard import create_num_keyboard


async def first_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    if context.chat_data.get("edit_id", None) is None:    
        event_message_id = "current"
    else:
        event_message_id = context.chat_data["edit_id"]
    context.chat_data[event_message_id]["meeting_name"] = update.message.text
    await update.message.reply_text("¿Cuál es la descripción de la quedada?")
    return MEETING_DESCRIPTION
    

async def second_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if context.chat_data.get("edit_id", None) is None:    
        event_message_id = "current"
    else:
        event_message_id = context.chat_data["edit_id"]
    context.chat_data[event_message_id]["meeting_description"] = update.message.text
    await update.message.reply_text("¿Hasta cuantos jugadores se permiten en la partida?\n(marcar 30 si no hay límite)",
                                    reply_markup=create_num_keyboard())
    return ENTER_NUM_PLAYERS


async def process_num_players(update: Update, context: ContextTypes.DEFAULT_TYPE) ->int:
    if context.chat_data.get("edit_id", None) is None:    
        event_message_id = "current"
    else:
        event_message_id = context.chat_data["edit_id"]
    context.chat_data[event_message_id]["max_players"] = update.callback_query.data
    await update.callback_query.edit_message_text("Indique la fecha de inicio", reply_markup=create_calendar_keyboard("start_date"))
    logger.info("Start time keyboard shown")
    return ENTER_START_TIME