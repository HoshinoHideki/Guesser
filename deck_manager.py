from datetime import datetime
from config import BLANK_CARD, DATE_FORMAT, FACTOR, DATABASE
import sqlite3


class Flashcard:
    """A simple object, has "front" and "back" attributes.
    """
    # maybe I don't need it yet?
    def __init__(self, card_id, front, back):
        self.id = card_id
        self.front = front
        self.back = back

class Collection:
    """Whole collection of decks.
    Needed mostly for stats and summaries.

    Returns:
        Collection: collection of stuff.
    """

    def __init__(self) -> None:
        # connect to sql database
        sql_line = "select name from decks"
        deck_names = [tuple[0] for tuple in execute_sql(sql_line)]
        self.decks = [Deck(deck_name) for deck_name in deck_names]

        self.total_cards = 0
        self.total_due = 0

        # count useful stuff
        for deck in self.decks:
            self.total_cards += len(deck.cards)
            for language in deck.languages:
                self.total_due += len(deck.get_due(language))


class Card:
    """General Card object.
    """  
    
    def __init__(self, data:tuple, languages:list):
        """Card constructor. Takes a tuple from the sql database and
        a languages list.

        """
        self.id = data[0]
        self.key0 = data[1]
        self.key1 = data[2]
        self.key0_last = data[3]
        self.key0_next = data[4]
        self.key1_last = data[5]
        self.key1_next = data[6]
        self.languages = languages


    def get_data(self, front:str, type:str) -> str:
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

        return keys[type][front]
    

    def set_data(self, front:str, type:str, data:str):
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
        setattr(self, keys[front][type], data)


class Deck:
    """Deck object.
        Contains deck metadata and a list of Card objects.
    """

    def __init__(self, deck_name:str):
        self.name = deck_name
        statements = {
            "languages":    f"""select  language_1, 
                                        language_2 
                                from    decks 
                                where   name = '{deck_name}'
                            """,

            "description":  f"""select  description
                                from    decks
                                where   name = '{deck_name}'
                            """,

            "cards":        f"""select  id, 
                                        key_0, 
                                        key_1, 
                                        key_0_last_date, 
                                        key_0_next_date, 
                                        key_1_last_date, 
                                        key_1_next_date
                                from    {deck_name}
                            """,
        }
        self.languages = list(execute_sql(statements["languages"])[0])
        self.description = execute_sql(statements["description"])[0][0]
        cards = execute_sql(statements["cards"])
        self.cards = [Card(data, self.languages) for data in cards]


    def get_card(self, id:str) -> Card:
        """Gets a card by id.

        Args:
            id (str): card id.

        Returns:
            Card: first card with matching ID (if not unique).
            Empty string if didn't find.
        """

        card = ""
        for card in self.cards:
            if card.id == id:
                return card


    def get_due(self, front:str) -> list:
        """Makes a list of due cards.

        Args:
            front (str): front language by which to search

        Returns:
            list: List of due cards.
        """

        self.due = []
        # get due cards:
        for card in self.cards:
            next_date = card.get_data(front, "next")
            now = str(datetime.now())
            if next_date < now and next_date != "":
                self.due.append(card)          
        # sort them by the next due date
        self.due.sort(key=lambda card: card.get_data(front, "next"))
        return self.due


    def add_card(self, data:dict):
        """Adds a new card to the deck.

        Args:
            data (dict): takes a dictionary from the web form.
        """

        card = Card(BLANK_CARD, languages=self.languages) # make a blank
        card.id = self.increment_id() # create ID

        # this filters out key-value pairs that are not already present.
        # TODO: maybe rewrite later?
        for key in data.keys():
            if key in card.__dict__.keys():
                setattr(card, key, data[key])
        statement = f"""insert into {self.name} (id,
                                                 key_0,
                                                 key_1,
                                                 key_0_last_date, 
                                                 key_0_next_date,
                                                 key_1_last_date,
                                                 key_1_next_date,
                                                 deck)
                        values (?, ?, ?, ?, ?, ?, ?, ?);
        """
        values = (card.id,
                  card.key0, 
                  card.key1,
                  card.key0_last,
                  card.key0_next,
                  card.key1_last,
                  card.key1_next,
                  self.name)
        execute_sql(statement, values)


    def edit_card(self, id:str, data:dict):
        """Gets a card by id, edits according to data given in dictionary.

        Args:
            id (str): card id
            data (dict): data to add to the card.
        """

        card = self.get_card(id)
        for key in data.keys():
            if key in card.__dict__.keys():
                setattr(card, key, data[key])
        # update the database now
        statement = f"""update {self.name}
                        set key_0 = "{card.key0}",
                            key_1 = "{card.key1}",
                            key_0_last_date = "{card.key0_last}",
                            key_0_next_date = "{card.key0_next}",
                            key_1_last_date = "{card.key1_last}",
                            key_1_next_date = "{card.key1_next}"
                            where id = "{card.id}"
        """
        execute_sql(statement)


    def delete_card(self, id:str):
        for index, card in enumerate(self.cards):
            if card.id == id:
                self.cards.pop(index)
                break
        statement = f"""
            delete from {self.name}
            where id = {id}
        """
        execute_sql(statement)


    def update_date(self, id:str, front:str, method:str) -> None:
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

        now = str(datetime.now().replace(microsecond=0)) # current time
        card = self.get_card(id)

        if method == "update":
            last = card.get_data(front, "last")
            card.set_data(front, "next", increment_date(last))
            card.set_data(front, "last", now)

        elif method == "reset":
            card.set_data(front, "next", now)
            card.set_data(front, "last", now)

        data = card.__dict__
        self.edit_card(id, data)


    def increment_id(self) -> None:
        """Generates the next unused id.

        Returns:
            id (str): stringified id.
        """
        
        id = 0

        for card in self.cards:
            if int(card.id) >= id:
                id += 1
        return str(id)


    def make_flashcard(self, front:str) -> Flashcard:
        """Makes a Flashcard object for web interface.

        Args:
            front (str): which language to use as a front.

        Returns:
            Flashcard: Flashcard object.
        """

        # get the earliest due card from the deck.
        source_card: Card = self.get_due(front)[0]
        # make a flashcard
        flashcard = Flashcard(
            source_card.id, 
            source_card.key0, 
            source_card.key1
        )
        # swap front and back if needed.
        if front == self.languages[1]:
            flashcard.front, flashcard.back = (
                source_card.key1, source_card.key0
            )
        return flashcard


    def get_nearest(self, front:str) -> str:
        """Gets the nearest due date of the deck. 

        Args:
            front (str): language to check

        Returns:
            str: date in string form
        """

        nearest_date = ""
        now = str(datetime.now())

        # deletes cards with empty dates
        cards = [
            card for card in self.cards if card.get_data(front, "next") != ""
        ]
        # sorts cards by next date
        cards.sort(key=lambda card: card.get_data(front, "next"))

        if len(cards) == 0 or cards[0].get_data(front, "next") < now:
            #TODO: change this to something else.
            nearest_date = "Right now"  
        else:
            nearest_date = cards[0].get_data(front, "next")

        return nearest_date


    def set_due(self, id:str):
        """Sets due a card with the given id, both ways.
        Can be used in the future for resetting cards.

        Args:
            id (str): id of a card to set due.
        """

        self.update_date(id, self.languages[0], "reset")
        self.update_date(id, self.languages[1], "reset")


    def get_unlearned(self) -> list:
        """Makes a list of unlearned cards.

        Returns:
            list: _description_
        """
        self.unlearned = []

        for card in self.cards:
            if card.key0_last == "" or card.key1_last == "":
                self.unlearned.append(card)

        return self.unlearned


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


def objectify_date(date:str) -> datetime:
    """Makes a string into a datetime object.
    Not needed for now. TODO: delete this?

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


def execute_sql(statement:str, *values:tuple):
    """Makes an SQL query that doesn't need any results.

    Args:
        statement (str): _description_
    """

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(statement, *values)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
    return result

