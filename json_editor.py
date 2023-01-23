import os, sqlite3, timeit
from deck_manager import Deck, Card

connection = sqlite3.connect("test.db")
cursor = connection.cursor()

