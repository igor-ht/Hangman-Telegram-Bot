from pymongo import MongoClient

database = None


def connect_mongodb_hangman():
    client = MongoClient()
    db = client.get_database("hangman")
    return db


def check_mongodb_connection():
    if not database:
        return False
    else:
        return True
