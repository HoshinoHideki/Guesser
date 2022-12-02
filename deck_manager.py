import json
import random
import os
from datetime import datetime
from config import BLANK_CARD, DATE_FORMAT, DATA_FOLDER, FACTOR
from copy import deepcopy


class Flashcard:
    """A simple object, has "front" and "back" attributes.
    """
    # maybe I don't need it yet?
    def __init__(self, front, back, card_id):
        self.front = front
        self.back = back
        self.id = card_id


class Deck:
    """Deck object.
        Contains deck metadata and a list of Card objects.
    """

    def __init__(self, deck_name:str) -> None:
        """Deck constructor method.

        Args:
            deck_name (str): file name.
            name (str): name of the deck. usually the same as filename. can be
                different for various testing reasons.
            languages (list): list of strings.
            cards (list): Makes a list of card objects.
        """

        filepath = DATA_FOLDER + deck_name + ".json"
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.name = data["name"]
        self.languages = data["languages"]
        self.cards = [Card(card) for card in data["cards"]]


    def save(self, filename:str):
        """Saves the deck to a json file.

        Args:
            filename (str): name of the file to which to save the deck.
        """

        filepath = DATA_FOLDER + filename + ".json"

        data = {}
        data["name"] = self.name
        data["languages"] = self.languages
        data["cards"] = [card.__dict__ for card in self.cards]

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(
                        data,     # data
                        file,               # filename
                        ensure_ascii=False, # for readability
                        indent=4)


class Card:
    """General Card object, creates a card from json data.
    """
    
    
    def __init__(self, data:dict) -> None:
        """Card object constructor.

        Args:
            data (dict): json dict that's used to build the card.
        """
        for key in data.keys():
            setattr(self, key, data[key])


def load_deck(deck_name:str) -> dict:
    """Takes a deck name and loads a dict.

    Args:
        deck_name (str): name of the deck (filename).

    Returns:
        dict: the deck.
    """

    deck = {}
    filepath = DATA_FOLDER + deck_name + ".json"

    with open(filepath, "r", encoding="utf-8") as file:
        deck = json.load(file)
    print(f"loading deck {deck_name}")

    return deck


def save_deck(deck:dict) -> json:
    """Saves the deck to a json file.

    Args:
        deck (dict): Dictionary containing deck data and information.

    Returns:
        json: saves to json file.
    """


    filepath = DATA_FOLDER + deck["name"] + ".json"


    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
                    deck,     # data
                    file,               # filename
                    ensure_ascii=False, # for readability
                    indent=4)


def list_decks() -> list:
    """Returns a list containing strings of deck names."""
    
    
    print("Calling function 'List decks.'")

    deck_list = os.listdir(DATA_FOLDER)
    
    for index, deck_name in enumerate(deck_list):
        deck_list[index] = deck_name[:-5] # temporary measure
    
    return deck_list


def get_key_string(deck:dict, front:str) -> str:
    """ Returns either "key_0_data" or "key_1_data".

    Checks the deck and returns one of the two values based on argument
    "front" and the index of a "languages" key inside the deck.

    Args:
        deck (dict): Dictionary containing deck data and information.
        front     (str): Language that is used as front of the card.
    """

    print(f"Getting Key String for deck {deck['name']}, front {front}")
    
    languages = deck["languages"]
    if front == languages[0]:
        key_string = "key_0_data"
    elif front == languages[1]:
        key_string = "key_1_data"
    
    return key_string


def get_card(card_id:str, deck:dict) -> dict:
    """Find the first dictionary with the matching card_id key value.

    Return empty dict if failed.

    Args:
        card_id (str): card's ID.
        deck (dict): Dictionary containing deck data and information.
    """

    print(f"calling function get_card, deck {deck['name']}, id {card_id}")

    out_card = {}
    for card in deck["cards"]:
        if card["card_id"] == card_id:
            out_card = card
            break
    return out_card


def update_card(deck:dict, data:dict) -> None:
    """
    Update existing item via form.

    Gets access to the database, finds an item with corresponding id and
    updates given values, then saves the deck.

    Args:
        deck (dict): Dictionary containing deck data and information.
        data (dict): data dict fetched from the form.
    
    Doesn't return anything.
    """
    
    print(f"Updating card in the deck {deck['name']}.")

    for card in deck["cards"]:
        if card["card_id"] == data["card_id"]:
            for key in data:
                card[key] = data[key]
            save_deck(deck)
            break


def update_date(deck:dict, card_id:str, front:str, method:str) -> None:
    """Updates the dates on a half of a card.

    - finds a card by id.
    - checks which key data to use.
    - updates dates based on the user input 
    - saves database from memory to file

    Args:
        deck (dict): Dictionary containing deck data and information.
        card_id          (str): Id of a card.
        front            (str): Language that is used as front of the card.
        method           (str): Either "update" or "reset".
    """

    card = get_card(card_id, deck)

    key_string = get_key_string(deck, front)

    now = str(datetime.now().replace(microsecond=0))
    
    # Update: increment the next date.
    if method == "update":
        card[key_string]["next_date"] = increment_date(
            card[key_string]["last_date"], FACTOR)

    # Reset: set the next date to right now.
    elif method == "reset":
        card[key_string]["next_date"] = now
    
    # Set the last date to right now in any case.
    card[key_string]["last_date"] = now

    # write the changes.
    update_card(deck, card)

    # logging.
    print(f"update card id #{card['card_id']}, method {method}")


def increment_date(input_date:str, factor:int) -> str:
    """
    Takes a date, increments it by built-in algorhythm, subject for
    customization in the future.

    Args:
        input_date       (str): Date string to be modified.
        factor           (int): Number by which multiplicate dates.
    
    Returns:
        multiplicated date.
    """


    now = datetime.now()
    format = DATE_FORMAT
    output_date = ""

    # Set to now if the date is empty.
    if input_date == "":
        output_date = now

    # Check if date is according to the format.
    elif isinstance(datetime.strptime(input_date, format),
        datetime):
        input_date = datetime.strptime(input_date, format)
        difference = now - input_date
        output_date = now + (difference * factor)
    
    # In case of any inconsistencies just reset the date to now.
    else:
        output_date = now
    
    # Strip microseconds.
    output_date = str(output_date.replace(microsecond=0))

    return output_date


def objectify_date(date:str) -> datetime:
    """Makes a string into a datetime object.

    Args:
        date (str): date in a string format.

    Returns:
        datetime: object.
    """

    try:
        date = datetime.strptime(date, DATE_FORMAT)

    # In case anything goes wrong.
    except:
        return "Error"

    return date


def add_card(deck:dict, data:dict) -> None:
    """ Adds a new card to the deck with data filled by user.

    - Loads database into memory.
    - Creates a dict with pre-determined item keys.
    - Assigns a new id to the new card (auto-incrementing the biggest free one).
    - Assigns values sent via the web form. 
    - Adds the item to the deck in memory.
    - Saves the deck from memory to file.

    Args:
        deck (dict): Dictionary containing deck data and information.
        data (dict): dict sent by web form.
    """
    

    new_card = BLANK_CARD.copy()
    
    # increment ID
    new_card["card_id"] = 0
    for card in deck["cards"]:
        if int(card["card_id"]) >= new_card["card_id"]:
            new_card["card_id"] += 1
    new_card["card_id"] = str(new_card["card_id"]) # turn it into str

    # add the data from the form to the dict.
    for key in data.keys():
        new_card[key] = data[key]

    # add to the list
    deck["cards"].append(new_card)

    # save changes
    save_deck(deck)


def pick_card(deck:dict, front:str) -> Flashcard:
    """
    This creates a Flashcard object from the deck.

    The function then access a list of decls languages and checks whether 
    one of its "key values" matches front value set by the user. 
    Then it assigns this value to the front attribute of a card, 
    and the other one - to the back.

    Args:
        deck (dict): Dictionary containing deck data and information.
        front (str): string value telling function which value assign as the
            card's front.

    Returns:
        Flashcard: custom object.
    """


    # pick a dict
    source_card = random.choice(deck.get("cards"))
    
    # pick a language pair
    languages = deck["languages"]
    
    # create empty card
    flashcard = Flashcard("", "", "")
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


def get_due(deck:dict, front:str) -> dict:
    """ Filters out only those cards that are due to train.

    - loads a deck into memory
    - gets a key string for front card data.
    - removes the cards that are not due.
    - returns the deck only with due cards.

    Args:
        deck (dict): Dictionary containing deck data and information.
        front (str): name of the front language

    Returns "deck" dictionary.
    """

    due_deck = deepcopy(deck)
    cards = due_deck["cards"]
    key_string = get_key_string(deck, front)

    for card in list(cards):
        try:
            # leave all cards that are due to right now.
            next_date = datetime.strptime(
                card[key_string]["next_date"], 
                DATE_FORMAT)
            if next_date < datetime.now():
                pass
            else:
                # remove from the list if the date is not due yet.
                cards.remove(card)
        except:
            # remove from the list if objectification goes wrong.
            cards.remove(card)
    
    # sort by date of next review
    cards.sort(key=lambda card:card[key_string]["next_date"])
    return due_deck


def set_due(deck:dict, front:str, card_number:int):
    """ Sets a number of cards "due".

    Not used as of now, but might become handy later.

    - Loads cards.
    - Gets a key_string
    - Sets a number of cards next_date parameter to right now.
    - Returns "Empty" if no new cards are in the deck. 
    """
    cards = deck["cards"]
    key_string = get_key_string(deck, front)   
    counter = 0

    for card in list(cards):
        if card[key_string]["last_date"] == "":

            update_date(deck, card["card_id"], front, "update")
            counter += 1

            if counter == card_number:
                break
            # make a 1-card deck with the new card.
    if counter == 0:
        return "Empty"
    else:
        return "Done"


def set_both_due(deck:dict, card_id:str):
    """Resets both key data values for a given card id.

    Args:
    deck (dict): Dictionary containing deck data and information.
    card_id          (str): Id of a card.
    """

    for front in deck["languages"]:
        update_date(deck, card_id, front, "reset")


def count_due_new(deck:dict, *front:str or list):
    due_new = 0
    if front == ():
        front = deck["languages"]
    
    for language in list(front):
        due_deck = get_due()
    return due_new


def count_due(deck:dict, *front:str or list) -> int:
    """Counts the number of "due" cards.

    If front argument is given, counts only those cards that correspond
    to the given language.

    Args:
    deck (dict): Dictionary containing deck data and information.
    front            (str ot list): Language that is used as front of 
                                    the card.
    """

    due_number = 0

    # takes both languages as front if no front is given
    if front == ():
        front = deck["languages"]

    for language in list(front):
        print(f"Counting due cards in deck {deck['name']}, front {language}")
        due_deck = get_due(deck, front=language)
        due_number += len(due_deck["cards"])

    return due_number


def total_cards(deck:dict) -> int:
    """Counts how many cards are there in all decks.
        Can take specific decks as an argument.

    Args:
        deck (dict): Dictionary containing deck data and information.

    Returns:
        int: number of cards
    """

    total_cards = 0

    if "cards" in deck:
        print(f"Calculating total number of cards in deck {deck['name']}")
        total_cards += len(deck["cards"])
    
    else:
        print(f"Calculating total number of cards in the database")
        for inner_deck in deck:
            total_cards += len(deck[inner_deck]["cards"])    
    return total_cards


def total_due(database:dict)-> int:
    """Counts how many due cards are there in total.
    
    Args:
        database (dict): database.
    """

    print("Calculating total number of due cards.")

    total_due = 0
    for deck in database.keys():
        total_due += count_due(database[deck])
    return total_due


def get_next_card_due(deck:dict, front:str) -> str:
    """Gets the nearest date for the chosen deck and front.
    If the nearest date is past right now, returns "Right now" 
    
    Args:
        deck (dict): Dictionary containing deck data and information.
        front            (str): name of the front language
    """

    next_due_date = ""
    now = datetime.now()
    key_string = get_key_string(deck, front)

    #skim through the deck
    for card in deck["cards"]:
        # if next date is objectifiable
        try:
            next_date = objectify_date(card[key_string]["next_date"])
            # if the date is earlier than right now, return "Right Now"
            if next_date < now:
                next_due_date = "Right now"
                break
            # if the date is no earlier than tight now.
            if next_date > now:
                # replace if the date is empty
                if next_due_date == "":
                    next_due_date = next_date.replace(microsecond=0)
                # if it's earlier then previous stored date, replace it.
                elif next_date < next_due_date:
                    next_due_date = next_date.replace(microsecond=0)
            # if somehow it's neither do nothing
            else:
                next_date = "some error occured"
        # do nothing if the data is not objectifiable.
        except:
            pass
    return str(next_due_date)


def get_next_id(deck:dict, number:int) -> list:
    """ Finds the ids of set number of cards that were not studied yet.
    Returns a list of strings.

    Args:
        deck (dict): Dictionary containing deck data and information.
        number           (int): Number of cards.
    """

    id_list = []
    counter = 0
    for card in deck["cards"]:
        if card["key_0_data"]["last_date"] == "" or \
            card["key_1_data"]["last_date"] == "":
                id_list.append(card["card_id"])
                counter += 1
                if counter == number:
                    break
    return id_list

def create_learn_deck(deck:dict, id_list:list) -> dict:
    """Creates a deck with only the new learning cards.
    (For learning pages)
    
    Args:
        deck (dict): Dictionary containing deck data and information.
        id_list         (list): list of card decks

    Returns:
        deck            (dict): deck with cards and metadata
    """

    learn_deck = deepcopy(deck)
    learn_deck["cards"] = []
    cards = learn_deck["cards"]
    for id in id_list:
        cards.append(get_card(id, deck))
    return learn_deck