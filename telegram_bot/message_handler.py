
from telegram import Update
from telegram.ext import ContextTypes
from .constants import MEETING_DESCRIPTION, ENTER_START_TIME
from utils.logger import logger
from .calendar.telegramcalendar import create_calendar

async def first_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["current"]["meeting_name"] = update.message.text
    await update.message.reply_text("¿Cuál es la descripción de la quedada?")
    return MEETING_DESCRIPTION

async def second_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["current"]["meeting_description"] = update.message.text
    await update.message.reply_text("Indique la fecha de inicio", reply_markup=create_calendar("start_date"))
    logger.info("Start time keyboard shown")
    return ENTER_START_TIME