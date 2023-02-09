import bot_settings as bot_settings
from mongoDB import connect_mongodb_hangman
from GameControl import GameControl
from logger import logger
from bot_handlers import start, game, help_rules, respond
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    Updater,
)


database = connect_mongodb_hangman()
game_control = GameControl(database)
logger.info(f"** Singleton GameControl created **")


def bot():
    updater = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CommandHandler("game", game))

    dispatcher.add_handler(CommandHandler("help", help_rules))

    dispatcher.add_handler(MessageHandler(Filters.text, respond))

    logger.info("* Start polling...")
    updater.start_polling()  # Starts polling in a background thread.
    updater.idle()  # Wait until Ctrl+C is pressed
    logger.info("* Server turning off! *")


bot()
