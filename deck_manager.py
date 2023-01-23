"""
Method collection for manipulating data.
"""

from datetime import datetime
from config import BLANK_CARD, DATE_FORMAT, FACTOR
import sql_queries


class Flashcard:
    """A simple object, has "front" and "back" attributes.
    """
    # maybe I don't need it yet?
    def __init__(self, id_, front, back):
        self.id_ = id_
        self.front = front
        self.back = back


class Card:
    """General Card object.
    """


    def __init__(self, data:dict, languages:list):
        """Card constructor. Takes a tuple from the sql database and
        a languages list.
        """

        if isinstance(data, dict):
            self.id_ = data["id"]
            self.key0 = data["key_0"]
            self.key1 = data["key_1"]
            self.key0_last = data["key_0_last_date"]
            self.key1_last = data["key_1_last_date"]
            self.key0_next = data["key_0_next_date"]
            self.key1_next = data["key_1_next_date"]
            self.deck = data["deck"]
        self.languages = languages


    def get_data(self, front:str, key:str) -> str:
        """Returns data according to specified type and front language.

        Args:
            front (str): one of the two languages
            type (str): either "last" or "next".

        Returns:
            str: needed stat string
        """

        keys = {
            "last":{
                self.languages[0]:self.key0_last,
                self.languages[1]:self.key1_last,
            },
            "next":{
                self.languages[0]:self.key0_next,
                self.languages[1]:self.key1_next,
            },
        }

        return keys[key][front]


    def set_data(self, front:str, key:str, data:str):
        """Edit attribute according to card keys.

        Args:
            front (str): language
            key (str): "last" or "next"
            data (str): data to replace
        """

        keys = {
            self.languages[0]:{
                "last":"key0_last",
                "next":"key0_next",
            },
            self.languages[1]:{
                "last":"key1_last",
                "next":"key1_next",
            },
        }
        setattr(self, keys[front][key], data)


class Deck:
    """Deck object.
        Contains deck metadata and a list of Card objects.
    """

    def __init__(self, deck_name:str):
        deck_data = sql_queries.init_deck(deck_name)
        card_data = sql_queries.init_cards(deck_name)
        self.name = deck_name
        self.languages = sql_queries.get_languages(deck_name)
        self.description = deck_data["description"]
        self.cards = [Card(card, self.languages) for card in card_data]
        self.unlearned = []


    def get_card(self, id_:str or int) -> Card:
        """Gets a card by id.

        Args:
            id (str): card id.

        Returns:
            Card: first card with matching ID (if not unique).
            Empty string if didn't find.
        """

        check = isinstance(id_, int)
        if not check:
            id_ = int(id_)
        card = Card(sql_queries.get_card(id_), languages=self.languages)
        return card


    def add_card(self, data:dict):
        """Adds a new card to the deck.

        Args:
            data (dict): takes a dictionary from the web form.
        """

        card = Card(BLANK_CARD, languages=self.languages) # make a blank

        #this filters out key-value pairs that are not already present.
        #maybe rewrite later?
        for key in data.keys():
            if key in card.__dict__:
                setattr(card, key, data[key])
        data = card.__dict__
        data["deck"] = self.name  #add deck name.
        sql_queries.add_card(data=data, deck_name=self.name)


    def edit_card(self, id_:str or int, data:dict):
        """Gets a card by id, edits according to data given in dictionary.

        Args:
            id (str): card id
            data (dict): data to add to the card.
        """

        card = self.get_card(id_)
        for key in data.keys():
            if key in card.__dict__:
                setattr(card, key, data[key])

        sql_queries.edit_card(card.__dict__)


    def delete_card(self, id_:str or int) -> None:
        """Sends a query to delete the card from db.

        Args:
            id (str): id of the card.
        """

        check = isinstance(id_, int)
        if not check:
            id_ = int(id_)
        sql_queries.delete_card(id_)


def increment_date(input_date:str) -> str:
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
    output_date = ""
    # Set to now if the date is empty.
    if input_date == "":
        output_date = now
    # Check if date is according to the format.
    elif isinstance(datetime.strptime(input_date, DATE_FORMAT),
        datetime):
        input_date = datetime.strptime(input_date, DATE_FORMAT)
        difference = now - input_date
        output_date = now + (difference * FACTOR)
    # In case of any inconsistencies just reset the date to now.
    else:
        output_date = now
    # Strip microseconds.
    output_date = str(output_date.replace(microsecond=0))
    return output_date

def get_due(deck_name, front:str) -> list:
    """Make a deck consisting only of due cards.

    Args:
        front (str): language of deck front.

    Returns:
        list: list of Cards.
    """

    languages = sql_queries.get_languages(deck_name)

    data = sql_queries.get_due(deck_name, front)
    cards = []
    if len(data) != 0:
        cards = [Card(card, languages) for card in data]
    return cards

def make_flashcard(deck_name:str, front:str) -> Flashcard:
    """ Make a flashcard from deck.
    Args:
        deck_name (str)
        front (str)
    """

    languages = sql_queries.get_languages(deck_name)
    card_data = sql_queries.get_due(deck_name, front)[0]
    card = Card(card_data, languages)
    flashcard = Flashcard(card.id_, card.key0, card.key1)
    if flashcard.front == languages[1]:
        flashcard.front, flashcard.back = (
            flashcard.back, flashcard.front
        )
    return flashcard

def update_date(id_:int, front:str, method:str) -> None:
    """Updates card's date in accordance with the method given by the
    user.

    Update: set next due date equal to:
    "current date + (time passed since the last review * factor)"

    Reset: set both to right now.

    Args:
        id (str): card ID
        front (str): language to use
        method (str): method string to specify what to do
    """

    card_data = sql_queries.get_card(int(id_))
    deck_name = card_data["deck"]
    languages = sql_queries.get_languages(deck_name)
    card = Card(card_data, languages)
    now = str(datetime.now().replace(microsecond=0)) # current time
    match method:
        case "update":
            last = card.get_data(front, "last")
            card.set_data(front, "next", increment_date(last))
            card.set_data(front, "last", now)
        case "reset":
            card.set_data(front, "next", now)
            card.set_data(front, "last", now)

    data = card.__dict__
    sql_queries.edit_card(data)


def get_unlearned(deck_name:str) -> Card:
    """ Get cards that are now learned yet.

    Args:
        deck_name (str): Name of the deck.
    """

    card_data = sql_queries.get_unlearned(deck_name)
    if len(card_data) == 0:
        return ""
    languages = sql_queries.get_languages(deck_name)
    card = Card(card_data, languages)
    return card
