import json, os, sqlite3
from deck_manager import Deck, Card, Collection

connection = sqlite3.connect("test.db")
cursor = connection.cursor()

# def synchronize():
#     for deck in collection.decks:
#         for card in deck.cards:
#             statement = f"""replace into {deck.name} (
#                 id, key_0, key_1, key_0_last_date, key_0_next_date, 
#                 key_1_last_date, key_1_next_date, deck)
#                 values (?, ?, ?, ?, ?, ?, ?, ?);"""
#             values = (card.id, card.key0, card.key1, card.key0_last, card.key0_next,
#                 card.key1_last, card.key1_next, deck.name)
#             cursor.execute(statement, values)
#         connection.commit()

