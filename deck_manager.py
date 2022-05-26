import json
import random
from datetime import datetime
from config import DATABASE, BLANK_CARD, DATE_FORMAT


class Card:
    """A simple object, has "front" and "back" attributes.
    """
    # maybe I don't need it yet?
    def __init__(self, front, back, card_id):
        self.front = front
        self.back = back
        self.id = card_id


def load_database() -> dict: 
    """This gets called every time you need to access the database.
    
    Returns python object (dict).
    """

    with open(DATABASE, "r", encoding="utf-8") as file:
        database = json.load(file)
    return database


def save_database(database:dict) -> json:
    """Function for saving changes if they were made.

    Saves data model from memory into the file.
    """
    with open(DATABASE, "w", encoding="utf-8") as file:
                json.dump(
                    database,           # data
                    file,               # filename
                    ensure_ascii=False, # for readability
                    indent=4)
    return "Database saved."


def list_decks() -> dict:
    """Returns a sorted list containing strings of deck names."""
    # 
    return sorted(load_database().keys())


def get_languages(deck_name:str) -> list:
    """Makes a list starting with "id" and containing both key values.

    Args:
        deck_name (str): name of the deck.
    """

    return load_database()[deck_name]["languages"]


def get_key_string(deck_name:str, front:str) -> str:
    """ Returns either "key_0_data" or "key_1_data".

    Checks the deck and returns one of the two values based on argument
    "front" and the index of a "languages" key inside the deck. 
    """
    languages = load_database()[deck_name]["languages"]
    if front == languages[0]:
        key_string = "key_0_data"
    elif front == languages[1]:
        key_string = "key_1_data"
    return key_string


def get_card(card_id:str, deck_name:str) -> dict:
    """Find a dictionary with the matching id key value.

    Return empty dict if failed.

    Args:
        card_id (str): card's ID.
    """
    database = load_database()
    cards = database[deck_name]["cards"]
    out_card = {}
    for card in cards:
        if card["card_id"] == card_id:
            out_card = card
    return out_card


def update_card(deck_name:str, data:dict) -> None:
    """
    Update existing item via form.

    Gets access to the database, finds an item with corresponding id and
    updates given values.
    
    Args:
        deck_name (str): Name of deck
        data (dict): data dict fetched from the form.
    
    Doesn't return anything.
    """
    database = load_database()
    cards = database[deck_name]["cards"]
    for card in cards:
        if card["card_id"] == data["card_id"]:
            for key in data:
                card[key] = data[key]
            save_database(database)


def update_date(deck_name:str, card_id:str, front:str, method:str) -> None:
    """Updates the dates on a half of a card.

    - finds a card by id.
    - checks which key data to use.
    - updates dates based on the user input 
    - saves database from memory to file
    """

    card = get_card(card_id, deck_name)

    key_string = get_key_string(deck_name, front)

    NOW = str(datetime.now().replace(microsecond=0))
    
    if method == "update":
        card[key_string]["next_date"] = increment_date(
            card[key_string]["last_date"])
    if method == "reset":
        card[key_string]["next_date"] = NOW
    card[key_string]["last_date"] = NOW

    update_card(deck_name, card)


def increment_date(input_date:str) -> str:
    """
    Takes a date, increments it by built-in algorhythm, subject for
    customization in the future.
    """
    now = datetime.now()
    format = DATE_FORMAT
    output_date = ""
    if input_date == "":
        output_date = now
    elif isinstance(datetime.strptime(input_date, format),
        datetime):
        input_date = datetime.strptime(input_date, format)
        difference = now - input_date
        output_date = now + (difference * 5)
    output_date = output_date.replace(microsecond=0)
    return str(output_date)


def add_card(deck_name:str, data:dict) -> None:
    """ Adds a new card to the deck with data filled by user.

    - Loads database into memory.
    - Creates a dict with pre-determined item keys.
    - Assigns a new id to the new card (auto-incrementing the biggest one).
    - Assigns values sent via the web form. 
    - Adds the item to the deck in memory.
    - Saves the deck from memory to file.

    Args:
        deck_name (str): name of the deck.
        data (dict): dict sent by web form.
    """

    database = load_database()
    cards = database[deck_name]["cards"]

    new_item = BLANK_CARD
    
    # increment ID (make a function?)
    new_item["card_id"] = 0
    for card in cards:
        if int(card["card_id"]) >= new_item["card_id"]:
            new_item["card_id"] += 1
    new_item["card_id"] = str(new_item["card_id"]) # turn it into str

    # maybe do this procedurally:
    for key in data.keys():
        new_item[key] = data[key]

    cards.append(new_item)

    save_database(database)


def pick_card(deck:list, front:str) -> Card:
    """
    This creates a Card object from the deck.

    The function then access a list of decls languages and checks whether 
    one of its "key values" matches front value set by the user. 
    Then it assigns this value to the front attribute of a card, 
    and the other one - to the back.

    Args:
    deck (list): list of card dicts.
    front (str): string value telling function which value assign as the
    card's front.   
    """
    
    entry = random.choice(deck.get("cards"))
    languages = deck.get("languages")
    
    card = Card("", "", "")
    card.id = entry["card_id"]   
    if front == languages[0]:
        card.front, card.back = entry["key_0"], entry["key_1"]
    elif front == languages[1]:
        card.front, card.back = entry["key_1"], entry["key_0"]
    else:
        pass

    return card


def get_due(deck_name:str, front:str) -> dict:
    """ Filters out only those cards that are due to train.

    - loads a deck into memory
    - gets a key string for front card data.
    - removes the cards that are not due.
    - returns the deck only with due cards.
    """

    due_deck = load_database()[deck_name]
    cards = due_deck["cards"]

    key_string = get_key_string(deck_name, front)

    for card in list(cards):
        try:
            next_date = datetime.strptime(
                card[key_string]["next_date"], 
                DATE_FORMAT)
            if next_date < datetime.now():
                pass
            else:
                cards.remove(card)
        except:
            cards.remove(card)
    return due_deck


def create_due(deck_name:str, front:str, card_number:int):
    """ Makes a number of cards "due".

    - Loads langs and cards data from deck.
    """

    cards = load_database()[deck_name]["cards"]

    key_string = get_key_string(deck_name, front)
    
    counter = 0
    for card in cards:
        if card[key_string]["last_date"] == "":
            update_date(deck_name, card["card_id"], front, "update")

            counter += 1
            if counter == card_number:
                break

    if counter == 0:
        return "Empty"
    else:
        return "Done"


def count_due(deck_name):
    number=0
    for language in load_database()[deck_name]["languages"]:
        deck = get_due(deck_name, front=language)
        number += len(deck["cards"])
    return number