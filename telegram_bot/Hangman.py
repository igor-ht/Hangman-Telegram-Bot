import random
from bot_settings import LETTER_BLOCKS


class HangmanState:
    def __init__(
        self, chat_id: int, word="", chances=7, inserted_letters=[], state="start"
    ):
        self.chat_id = chat_id
        self.word = word
        self.chances = chances
        self.inserted_letters = inserted_letters
        self.state = state

    def display(self):
        display = "".join(
            [
                LETTER_BLOCKS[letter] if letter in self.inserted_letters else "◻"
                for letter in self.word
            ]
        )
        return display

    def start_game(self):
        self.state = "game"
        self.word = random.choice(["python", "javascript", "ruby", "java", "colbo"])
        self.chances = 7
        self.inserted_letters = []

    def check_letter(self, letter):
        if letter not in self.inserted_letters:
            self.inserted_letters.append(letter)
        if letter not in self.word:
            self.chances -= 1
        self.check_game()

    def check_game(self):
        if self.chances < 1:
            self.state = "lost"
        elif "◻" not in self.display():
            self.state = "won"
