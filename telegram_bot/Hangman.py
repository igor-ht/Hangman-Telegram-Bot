import random
from bot_settings import LETTER_BLOCKS


class HangmanState:
    def __init__(self, chat_id):
        self.id = chat_id
        self.word = ""
        self.display = "◻"
        self.chances = 7
        self.state = "start"

    def start_game(self):
        self.state = "game"
        self.word = random.choice(["python", "javascript", "ruby", "java", "colbo"])
        self.display = "◻" * len(self.word)
        self.chances = 7

    def check_letter(self, letter):
        if letter in self.word:
            self.update_display(letter)
            self.check_game()
        else:
            self.chances -= 1
            self.check_game()

    def update_display(self, letter):
        self.display = "".join(
            [
                (
                    "◻"
                    if char != letter and self.display[i] == "◻"
                    else LETTER_BLOCKS[char]
                )
                for i, char in enumerate(self.word)
            ]
        )

    def check_game(self):
        if self.chances < 1:
            self.state = "lost"
        elif "◻" not in self.display:
            self.state = "won"
