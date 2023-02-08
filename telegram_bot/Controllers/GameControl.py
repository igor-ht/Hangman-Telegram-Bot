from typing import List
from Controllers.Hangman import HangmanState


class GameControl:
    def __init__(self, db):
        self.db = db
        self.user = self.db.get_collection("users")
        self.games: List[HangmanState] = []

    def get_game(self, id):
        return [game for game in self.games if game.id == id]

    def find_chat(self, id):
        result = self.user.find({"chat_id": id})
        game = self.get_game(id)
        if result and game:
            return True
        return False

    def del_chat(self, id):
        self.games = [game for game in self.games if game.id != id]
        result = self.user.delete_one({"chat_id": id})
        return result

    def add_chat(self, hangman: HangmanState):
        if hangman not in self.games:
            self.games.append(hangman)
        user_info = {
            "chat_id": hangman.id,
        }
        if not self.user.find({"chat_id": hangman.id}):
            result = self.user.insert_one(user_info)
            return result.inserted_id
        return hangman.id
