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


def save_database(database) -> json:
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


def list_decks() -> list:
    """Returns a sorted list containing strings of deck names."""

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
    cards = load_database()[deck_name]["cards"]
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

    now = str(datetime.now().replace(microsecond=0))
    
    if method == "update":
        card[key_string]["next_date"] = increment_date(
            card[key_string]["last_date"])

    if method == "reset":
        card[key_string]["next_date"] = now
    card[key_string]["last_date"] = now

    update_card(deck_name, card)
    print(f"update card id #{card['card_id']}, method {method}")


def increment_date(input_date:str) -> str:
    """
    Takes a date, increments it by built-in algorhythm, subject for
    customization in the future.

    TODO: Custimizable multiplication factor.
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
    output_date = str(output_date.replace(microsecond=0))
    return output_date


def objectify_date(date:str):
    return datetime.strptime(date, DATE_FORMAT)


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

    new_card = BLANK_CARD.copy()
    
    # increment ID (make a function?)
    new_card["card_id"] = 0
    for card in cards:
        if int(card["card_id"]) >= new_card["card_id"]:
            new_card["card_id"] += 1
    new_card["card_id"] = str(new_card["card_id"]) # turn it into str

    for key in data.keys():
        new_card[key] = data[key]

    cards.append(new_card)

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
    
    source_card = random.choice(deck.get("cards"))
    languages = deck.get("languages")
    
    flashcard = Card("", "", "")
    flashcard.id = source_card["card_id"]  
    
    if front == languages[0]:
        flashcard.front = source_card["key_0"]
        flashcard.back = source_card["key_1"]
    elif front == languages[1]:
        flashcard.front = source_card["key_1"]
        flashcard.back = source_card["key_0"]
    else:
        pass

    return flashcard


def get_due(deck_name:str, front:str) -> dict:
    """ Filters out only those cards that are due to train.

    - loads a deck into memory
    - gets a key string for front card data.
    - removes the cards that are not due.
    - returns the deck only with due cards.
    """

    deck = load_database()[deck_name]
    cards = deck["cards"]

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
    cards.sort(key=lambda card:card[key_string]["next_date"])
    return deck


def set_due(deck_name:str, front:str, card_number:int):
    """ Sets a number of cards "due".

    Not used as of now, but might become handy later.

    - Loads cards.
    - Gets a key_string
    - Sets a number of cards next_date parameter to right now.
    - Returns "Empty" if no new cards are in the deck. 
    """
    cards = load_database()[deck_name]["cards"]
    key_string = get_key_string(deck_name, front)   
    counter = 0

    for card in list(cards):
        if card[key_string]["last_date"] == "":

            update_date(deck_name, card["card_id"], front, "update")
            counter += 1

            if counter == card_number:
                break
            # make a 1-card deck with the new card.
    if counter == 0:
        return "Empty"
    else:
        return "Done"

def set_both_due(deck_name:str, card_id:str):
    """Resets both key data values for a given card id.

    """
    for front in get_languages(deck_name):
        update_date(deck_name, card_id, front, "reset")


def count_due(deck_name:str, *front:str or list) -> int:
    """Counts the number of "due" cards.

    If front argument is given, counts only those cards that correspond
    to the given language.
    """

    due_number = 0

    if front == ():
        front = load_database()[deck_name]["languages"]

    for language in list(front):
        deck = get_due(deck_name, front=language)
        due_number += len(deck["cards"])

    return due_number

def total_cards(*deck_names:list) -> int:
    """Counts how many cards are there in all decks.

    Can take specific decks as an argument.
    """
    total_cards = 0
    if deck_names == ():
        deck_names = load_database().keys()
    for deck in list(deck_names):
        total_cards += len(load_database()[deck]["cards"])
    return total_cards

def total_due()-> int:
    """Counts how many due cards are there in total."""

    total_due = 0
    for deck in load_database().keys():
        total_due += count_due(deck)
    return total_due


def get_next_card_due(deck_name:str, front:str) ->str:
    """Gets the nearest date for the chosen deck and front."""
    next_due_date = ""
    now = datetime.now()
    key_string = get_key_string(deck_name, front)
    for card in load_database()[deck_name]["cards"]:
        try:
            next_date = objectify_date(card[key_string]["next_date"])
            if next_date < now:
                next_due_date = "Right now"
                break
            if next_date > now:
                if next_due_date == "":
                    next_due_date = next_date.replace(microsecond=0)
                elif next_date < next_due_date:
                    next_due_date = next_date.replace(microsecond=0)
            else:
                pass
        except:
            pass
    return str(next_due_date)


def get_next_id(deck_name:str, number:int) -> list:
    """ Finds the ids of set number of cards that were not studied yet.
    """
    id_list = []
    cards = load_database()[deck_name]["cards"]
    counter = 0
    for card in cards:
        if card["key_0_data"]["last_date"] == "" or \
            card["key_1_data"]["last_date"] == "":
                id_list.append(card["card_id"])
                counter += 1
                if counter == number:
                    break
    return id_list

def create_learn_deck(deck_name:str, id_list:list) -> list:
    deck = load_database()[deck_name]
    deck["cards"] = []
    cards = deck["cards"]
    for id in id_list:
        cards.append(get_card(id, deck_name))
    return deck