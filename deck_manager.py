import json
import random
from config import *


class Card:
    """A simple object, has "front" and "back" attributes.
    """
    def __init__(self, front, back, id):
        self.front = front
        self.back = back
        self.id = id


def load_database():
    """This gets called every time some changes are made in the database."""
    with open(DATABASE, "r", encoding="utf-8") as file:
        database = json.load(file)
    return database


def get_fields(deck):
    """Makes a list starting with "id" and containing both key values.
    """
    database = load_database()
    deck = database[deck]
    fields = ["id"] + deck["languages"]
    return fields


def find_item(item_id, deck):
    """Find a dictionary with the matching id key value.
    Return empty dict if failed.
    """
    database = load_database()
    deck = database[deck]["cards"]
    out_item = {}
    for item in deck:
        if item["card_id"] == item_id:
            out_item = item
    return out_item


def update_item(deck, item_id, data):
    """
    Gets access to the database, finds an item with corresponding id and
    updates values.
    :param deck: string containing name of the deck
    :param item_id: id string to compare with.
    :param data: data dict fetched from the form.
    :return: Doesn't return anything.
    """
    database = load_database()
    deck = database[deck]["cards"]
    for item in deck:
        if item["card_id"] == item_id:
            for key in data:
                item[key] = data[key]
            with open(DATABASE, "w", encoding="utf-8") as database_file:
                json.dump(
                    database,
                    database_file,
                    ensure_ascii=False,
                    indent=4)
    else:
        return "ID not found."


def list_langs(field_list):
    """takes a list of fields, filters "id" out"""
    return field_list[1:]


def load_deck(deck):
    """
    Shortcut function for loading a specific deck from database.
    :param deck: name of the deck.
    :return: returns a deck: list of dicts.
    """
    database = load_database()
    deck = database[deck]["cards"]
    return deck


def list_decks():
    """Returns a list containing strings of deck names."""
    database = load_database()
    decks = sorted(database.keys())
    return decks


def pick_card(deck, front):
    """
    This makes a Card object from the deck.
    deck: list object containing dictionary objects.
    front: string value telling function which value assign to the front.
    Function then picks a random dict and checks whether one of its "key
    values" matches front value set by user. Then it assigns this value to
    the front attribute of a card, and the other one - to the back.
    """
    database = load_database()
    deck = database[deck]
    cards = deck["cards"]
    entry = random.choice(cards)  # picks up a dict
    card = Card("", "", "")
    if front == deck["languages"][0]:
        card.front = entry["key_0"]
        card.back = entry["key_1"]
    elif front == deck["languages"][1]:
        card.front = entry["key_1"]
        card.back = entry["key_0"]
    else:
        pass
    card.id = entry["card_id"]
    return card


def add_card(deck, data):
    database = load_database()
    deck = database[deck]
    cards = deck["cards"]
    new_item = {"key_0": "",
                "key_1": "",
                "card_id": "",
                "key_0_data": {
                    "last_date": "",
                    "next_date": "",
                    },
                "key_1_data": {
                    "last_date": "",
                    "next_date": "",
                    }
                }
    new_id = 0
    for card in cards:
        if int(card["card_id"]) >= new_id:
            new_id += 1
    new_item["card_id"] = str(new_id)
    new_item["key_0"] = data["key_0"]
    new_item["key_1"] = data["key_1"]
    cards.append(new_item)
    with open(DATABASE, "w", encoding="utf-8") as database_file:
        json.dump(
            database,
            database_file,
            ensure_ascii=False,
            indent=4)
    return f"Added entry number {new_id} to deck {deck['languages'][0]}"
