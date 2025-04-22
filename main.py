from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from utils.logger import logger
from telegram_bot.quedada_entry import quedada
from telegram_bot.button_handler import button_handler
import tracemalloc
from dotenv import load_dotenv
import os

tracemalloc.start()


def get_bot_token():
    token = os.environ["BOT_TOKEN"]
    logger.info("Bot token retrieved successfully")
    return token


def main():
    logger.info("Starting the bot application")

    # Load environment variables
    load_dotenv()    


    # Create an updater object with your bot's token
    application = ApplicationBuilder().token(get_bot_token()).read_timeout(60).write_timeout(60).build()

    logger.info("Application built", token=get_bot_token())

    commands = {
        "quedada": quedada,
    }

    for comm_string, funct in commands.items():
        application.add_handler(CommandHandler(comm_string, funct))
        #logger.info("Command registered", command=comm_string, handler=funct.__name__)

    application.add_handler(CallbackQueryHandler(button_handler))


    logger.info("Starting bot polling")
    application.run_polling()
    logger.info("Bot polling started successfully")


if __name__ == "__main__":
    main()