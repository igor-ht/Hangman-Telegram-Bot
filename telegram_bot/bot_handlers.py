import bot_settings as bot_settings
from mongoDB import connect_mongodb_hangman
from logger import logger
from GameControl import GameControl
from Hangman import HangmanState
from telegram import Update
from telegram.ext import CallbackContext

game_control: GameControl


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    database = connect_mongodb_hangman()
    game_control = GameControl(database)
    context.bot.send_message(chat_id, bot_settings.WELCOME)
    if game_control.find_chat(chat_id):
        logger.info(f"> user with chat_id #{chat_id} already exists")
        game = game_control.get_game_from_db(chat_id)
        game = HangmanState(chat_id)
        game_control.update_game(game)
    else:
        game_control.create_new_game(chat_id)
        logger.info(f"new user created with chat_id #{chat_id}")


def game(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    database = connect_mongodb_hangman()
    game_control = GameControl(database)
    game = game_control.get_game_from_db(chat_id)
    if not game:
        start(update, context)
    elif game.state == "start":
        game.start_game()
        game_control.update_game(game)
        logger.info(f"chat_id #{chat_id} started playing")
        context.bot.send_message(chat_id, bot_settings.GAME)
        context.bot.send_message(
            chat_id, f"{game.display()} 👉 {game.chances} chances left"
        )
    elif game.state == "won" or game.state == "lost":
        game.start_game()
        game_control.update_game(game)
        logger.info(f"chat_id #{chat_id} playing new game")
        context.bot.send_message(chat_id, bot_settings.GAME)
        context.bot.send_message(
            chat_id, f"{game.display()} 👉 {game.chances} chances left"
        )
    elif game.state == "game":
        context.bot.send_message(chat_id, "Send a single letter guess")


def help_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, bot_settings.HELP)


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    database = connect_mongodb_hangman()
    game_control = GameControl(database)
    letter = update.effective_message.text.lower()
    game = game_control.get_game_from_db(chat_id)
    if game.state == "game":
        if len(letter) > 1 or not letter.isalpha():
            context.bot.send_message(chat_id, "Send single letter guesses only.")
        else:
            game.check_letter(letter)
            game_control.update_game(game)
            logger.info(f"chat_id #{chat_id} inserted letter {letter}")
            context.bot.send_message(
                chat_id, f"{game.display()} 👉 {game.chances} chances left"
            )
            if game.state == "lost":
                logger.info(f"chat_id #{chat_id} lost!")
                context.bot.send_message(
                    chat_id,
                    f"Nice try! The word was 👉 {game.word}\n👉 /game to play again",
                )
            elif game.state == "won":
                logger.info(f"chat_id #{chat_id} won!")
                context.bot.send_message(
                    chat_id,
                    f"Well Done! You got the right word! 👉 {game.word}\n👉 /game to play again",
                )
    else:
        context.bot.send_message(
            chat_id, "👉 /start to start playing or 👉 /game to play again"
        )
