import Settings.bot_settings as bot_settings
from Logger.logger import logger
from Services.bot_api import start, game, help_rules, respond
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    Updater,
)

def bot():
    updater = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    game_handler = CommandHandler("game", game)
    dispatcher.add_handler(game_handler)

    help_handler = CommandHandler("help", help_rules)
    dispatcher.add_handler(help_handler)

    message_handler = MessageHandler(Filters.text, respond)
    dispatcher.add_handler(message_handler)


    logger.info("* Start polling...")
    updater.start_polling()  # Starts polling in a background thread.
    updater.idle()  # Wait until Ctrl+C is pressed
    logger.info("* Server turning off! *")

bot()
