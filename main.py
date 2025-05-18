from telegram import Update
from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackQueryHandler, ConversationHandler, ContextTypes,
)

from telegram_bot.constants import ENTER_START_TIME, ENTER_MEETING_TYPE, ENTER_START_DATE, MEETING_NAME, \
    MEETING_DESCRIPTION, ENTER_NUM_PLAYERS
from utils.logger import logger
from telegram_bot.quedada_entry import quedada
from telegram_bot.message_handler import first_answer, second_answer, process_num_players
from telegram_bot.actions.action_handler import action_handler
from telegram_bot.actions.attendance import attendance_button_handler
import tracemalloc
from dotenv import load_dotenv
import os

tracemalloc.start()

def main():
    logger.info("Starting the bot application")

    # Load environment variables
    load_dotenv()    


    # Create an updater object with your bot's token
    application = ApplicationBuilder().token(get_bot_token()).read_timeout(60).write_timeout(60).build()

    logger.info("Application built", token=get_bot_token())

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("quedada", quedada)],
        states={
            MEETING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_answer)],
            MEETING_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_answer)],
            ENTER_NUM_PLAYERS: [CallbackQueryHandler(process_num_players)],
            ENTER_START_TIME: [CallbackQueryHandler(action_handler)],
            ENTER_START_DATE: [CallbackQueryHandler(action_handler)],
            ENTER_MEETING_TYPE: [CallbackQueryHandler(action_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conversation_handler)
    application.add_handler(CallbackQueryHandler(attendance_button_handler))

    logger.info("Starting bot polling")
    application.run_polling()
    logger.info("Bot polling started successfully")


def get_bot_token():
    token = os.environ["BOT_TOKEN"]
    logger.info("Bot token retrieved successfully")
    return token

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END


if __name__ == "__main__":
    main()