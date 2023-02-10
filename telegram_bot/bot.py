import bot_settings as bot_settings
from logger import logger
from bot_handlers import start, game, help_rules, respond
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    Updater,
)


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
