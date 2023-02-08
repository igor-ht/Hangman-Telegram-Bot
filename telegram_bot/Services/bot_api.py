from Logger.logger import logger
from Controllers.Hangman import HangmanState
import Settings.bot_settings as bot_settings
from telegram import Update
from telegram.ext import CallbackContext
from Model.mongoDB import connect_mongodb_hangman
from Controllers.GameControl import GameControl

database = connect_mongodb_hangman()
game_control = GameControl(database)


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if game_control.find_chat(chat_id):
        logger.info(f"> chat id #{chat_id} already exists")
        context.bot.send_message(
            chat_id, "Send /game to start playing or /help for more information"
        )
    else:
        game_control.add_chat(HangmanState(chat_id))
        logger.info(f"GameState created with chat id #{chat_id}")
        context.bot.send_message(chat_id, bot_settings.WELCOME)


def game(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    game = game_control.get_game(chat_id)
    if game and game[0].state == "start":
        game[0].start_game()
        logger.info(f"chat id #{chat_id} started playing")
        context.bot.send_message(chat_id, bot_settings.GAME)
        context.bot.send_message(
            chat_id, f"{game[0].display} - {game[0].chances} chances left"
        )
    elif game[0].state == "won" or game[0].state == "lost":
        game[0].start_game()
        logger.info(f"chat id #{chat_id} playing new game")
        context.bot.send_message(chat_id, bot_settings.GAME)
        context.bot.send_message(
            chat_id, f"{game[0].display} - {game[0].chances} chances left"
        )
    elif game[0].state == "game":
        context.bot.send_message(chat_id, "Send a single letter guess")


def help_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, bot_settings.HELP)


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    letter = update.effective_message.text.lower()
    game = game_control.get_game(chat_id)
    if len(letter) > 1 or not letter.isalpha():
        context.bot.send_message(chat_id, "Send a single letter guess.")
    if game and game[0].state == "game":
        game[0].check_letter(letter)
        logger.info(f"chat id #{chat_id} inserted letter {letter}")
        context.bot.send_message(
            chat_id, f"{game[0].display} - {game[0].chances} chances left"
        )
        if game[0].state == "lost":
            context.bot.send_message(chat_id, f"Nice try! The word was: {game[0].word}")
            # game[0].start_game()
        elif game[0].state == "won":
            context.bot.send_message(
                chat_id, f"Well Done! You got the right word! -> {game[0].word}"
            )
            # game[0].start_game()
    else:
        context.bot.send_message(
            chat_id, "Send /start to start playing or /game to play again"
        )
        # game_control.add_chat(HangmanState(chat_id))
        # logger.info(f"GameState created with chat id #{chat_id}")
        # context.bot.send_message(chat_id, bot_settings.WELCOME)
