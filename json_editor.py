import json, os, sqlite3, timeit
from deck_manager import Deck, Card, Collection

connection = sqlite3.connect("test.db")
cursor = connection.cursor()

