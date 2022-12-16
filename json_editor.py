import json, os, sqlite3
from deck_manager import Deck, Card
from config import DATA_FOLDER

connection = sqlite3.connect("test.db")
cursor = connection.cursor()

def load_decks():
    statement = """select name from decks"""
    cursor.execute(statement)
    deck_names = cursor.fetchall()
    decks = [Deck(deck[0]) for deck in deck_names]
    return decks

decks = load_decks()


def populate_decks(decks):
    # iterating through decks
    for deck in decks:
        print(f"Populating deck {deck.name}")
        
        # making a list of values for the deck
        data_list = []
        
        # iterating through cards
        for card in deck.cards:
            item = (
                str(card.card_id), 
                str(card.key_0),
                str(card.key_1), 
                str(card.key_0_data["last_date"]),
                str(card.key_0_data["next_date"]),
                str(card.key_1_data["last_date"]),
                str(card.key_1_data["next_date"]),
                deck.name,
            )
            data_list.append(item)
        
        # make a statement for each card
        statement = f"""insert into {deck.name} (
            id, key_0, key_1, key_0_last_date, key_0_next_date, 
            key_1_last_date, key_1_next_date, deck)
            values (?, ?, ?, ?, ?, ?, ?, ?);"""
        
        # iterate through list and execute statement:
        for item in data_list:
            cursor.execute(statement, item)
    connection.commit()
    
populate_decks(decks)
# connection.commit()