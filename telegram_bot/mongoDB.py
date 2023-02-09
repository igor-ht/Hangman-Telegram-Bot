from pymongo import MongoClient


def connect_mongodb_hangman():
    client = MongoClient()
    db = client.get_database("hangman")
    return db
