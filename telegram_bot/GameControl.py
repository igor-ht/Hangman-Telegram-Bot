from Hangman import HangmanState


class GameControl:
    def __init__(self, database):
        self.database = database
        self.user = self.database.get_collection("users")

    def create_new_game(self, id):
        new_game = {
            "chat_id": id,
            "word": "",
            "chances": 7,
            "inserted_letters": [],
            "state": "start",
        }
        res = self.user.insert_one(new_game)
        return res.inserted_id

    def get_game_from_db(self, id):
        result = self.user.find_one({"chat_id": id})
        result.pop("_id")
        game = HangmanState(**result)
        return game

    def find_chat(self, id):
        result = self.user.find_one({"chat_id": id})
        if result:
            return True
        return False

    def update_game(self, game: HangmanState):
        game_from_db = self.get_game_from_db(game.chat_id)
        result = self.user.update_one(
            {"chat_id": game_from_db.chat_id},
            {
                "$set": {
                    "word": game.word,
                    "chances": game.chances,
                    "inserted_letters": game.inserted_letters,
                    "state": game.state,
                }
            },
        )
        return result

    def del_chat(self, id):
        result = self.user.delete_one({"chat_id": id})
        return result
