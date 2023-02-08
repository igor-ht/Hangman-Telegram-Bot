from typing import List
from Controllers.Hangman import HangmanState


class GameControl:

    _instance = None
    # method to create and certify that only one unique instance of the class GameControl is in the application
    def __new__(cls, db):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = db
            cls._instance.user = cls._instance.db.get_collection("users")
            cls._instance.games: List[HangmanState] = []
        return cls._instance

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
        result = self.user.find_one({"chat_id": hangman.id})
        if not result:
            res = self.user.insert_one(user_info)
            return res.inserted_id
        return hangman.id
