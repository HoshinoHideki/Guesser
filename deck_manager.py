import json
import os
from datetime import datetime
from config import BLANK_CARD, DATE_FORMAT, DATA_FOLDER, FACTOR


class Flashcard:
    """A simple object, has "front" and "back" attributes.
    """
    # maybe I don't need it yet?
    def __init__(self, front, back, card_id):
        self.front = front
        self.back = back
        self.id = card_id


class Collection:
    """Whole collection of decks.
    Needed mostly for stats and summaries.

    Returns:
        Collection: collection of stuff.
    """

    def __init__(self) -> None:
        self.decks = [Deck(deck) for deck in os.listdir(DATA_FOLDER)]
        self.total_cards = 0
        self.total_due = 0

        # counts useful stuff
        for deck in self.decks:
            self.total_cards += len(deck.cards)
            for language in deck.languages:
                self.total_due += len(deck.get_due(language))


class Card:
    """General Card object, creates a card from json data.
    """  
    
    def __init__(self, data:dict, languages:list) -> None:
        """Card object constructor.

        Args:
            data (dict): json dict that's used to build the card.
        """

        self.id = data["card_id"]
        self.key0 = data["key_0"]
        self.key1 = data["key_1"]
        self.key0_last = data["key_0_data"]["last_date"]
        self.key0_next = data["key_0_data"]["next_date"]
        self.key1_last = data["key_1_data"]["last_date"]
        self.key1_next = data["key_1_data"]["next_date"]
        self.languages = languages
    

class Deck:
    """Deck object.
        Contains deck metadata and a list of Card objects.
    """

    def __init__(self, deck_name:str) -> None:
        """Deck constructor.

        Args:
            deck_name (str): file name.
            name (str): name of the deck. usually the same as filename. can be
                different for various testing reasons.
            languages (list): list of strings.
            cards (list): Makes a list of card objects.
        """

        filepath = DATA_FOLDER + deck_name
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.name = data["name"]
        self.languages = data["languages"]
        self.cards = [Card(card, self.languages) for card in data["cards"]]


    def save(self, filename:str):
        """Saves the deck to a json file.

        Args:
            filename (str): name of the file to which to save the deck.
            Left for testing purposes.
        """

        filepath = DATA_FOLDER + filename + ".json"

        data = {}
        data["name"] = self.name
        data["languages"] = self.languages
        data["cards"] = []

        for card in self.cards:
            outcard = {}
            outcard["key_0"] = card.key0
            outcard["key_1"] = card.key1
            outcard["card_id"] = card.id
            outcard["key_0_data"] = {}
            outcard["key_1_data"]= {}
            outcard["key_0_data"]["last_date"] = card.key0_last
            outcard["key_0_data"]["next_date"] = card.key0_next
            outcard["key_1_data"]["last_date"] = card.key1_last
            outcard["key_1_data"]["next_date"] = card.key1_next
            data["cards"].append(outcard)

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(
                        data,     # data
                        file,               # filename
                        ensure_ascii=False, # for readability
                        indent=4)


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

        # gives method the right attribute.
        keys = {self.languages[0]:"key0_next", self.languages[1]:"key1_next"}
        keynext = keys[front]

        for card in self.cards:
            # try to objectify the date.
            try:
                key = Key(card, front)
                next_date = datetime.strptime(
                    key.next,
                    DATE_FORMAT
                )
                # add to deck only if its time is due
                if next_date < datetime.now():
                    self.due.append(card)
            # do nothinh if onjectification fails
            except:
                pass
        
        self.due = sorted(self.due, key=lambda card: getattr(card, keynext))

        return self.due


    def add_card(self, data:dict):
        """Adds a new card to the deck.

        Args:
            data (dict): takes a dictionary from the web form.
        """

        
        card = Card(BLANK_CARD, languages=self.languages) # make a blank
        card.id = self.increment_id() # create ID

        # this filters out key-value pairs that are not already present.
        for key in data.keys():
            if key in card.__dict__.keys():
                setattr(card, key, data[key])

        self.cards.append(card) # add card
        self.save(self.name) # save changes


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

        self.save(self.name)


    def update_date(self, id:str, front:str, method:str) -> None:
        """Updates card's date in accordance with the method given by the user.

        Args:
            id (str): card ID
            front (str): language to use
            method (str): method string to specify what to do
        """

        now = str(datetime.now().replace(microsecond=0)) # current time
        card = self.get_card(id)

        # takes only needed paramaters for ease of use.
        key = Key(card, front)
        
        # this will set next due date equal to current date + 
        # + (time passed since the last review * factor). 
        if method == "update":
            key.next = increment_date(key.last, FACTOR)
            key.last = now
        
        # this just sets everything to right now.
        elif method == "reset":
            key.last = now
            key.next = now

        data = key.generate_data(front, self.languages)
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

        source_card: Card = self.get_due(front)[0]
                
        flashcard = Flashcard("", "", "")
        flashcard.id = source_card.id
        
        if front == self.languages[0]:
            flashcard.front = source_card.key0
            flashcard.back = source_card.key1
        elif front == self.languages[1]:
                flashcard.front = source_card.key1
                flashcard.back = source_card.key0
        else:
            pass
        
        return flashcard


    def get_nearest(self, front:str) -> str:
        """Gets the nearest due date of the deck. 

        Args:
            front (str): language to check

        Returns:
            str: date in string form
        """

        nearest_date = ""
        now = datetime.now()

         # gives method the right attribute.
        keys = {self.languages[0]:"key0_next", self.languages[1]:"key1_next"}
        keynext = keys[front]

        # sorts by next date
        cards = sorted(self.cards, key=lambda card: getattr(card, keynext))

        # deletes cards with empty dates
        cards = [card for card in cards if getattr(card, keynext) != ""]

        if len(cards) == 0:
            #TODO: change this to something else.
            nearest_date = "Right now"  

        elif objectify_date(getattr(cards[0], keynext)) < now:
            nearest_date = "Right now"
        
        else:
            nearest_date = getattr(cards[0], keynext)
        
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
    

    def take_cards(self, id_list:list) -> list:
        """Makes of custom list of cards, selected by id.
        Currently serves no purpose, but might come handy later.

        Args:
            id_list (list): list of id strings.

        Returns:
            list: list of cards.
        """

        list = []

        for id in id_list:
            list.append(self.get_card(id))
        return list
        ...


class Key:
    def __init__(self, card:Card, front) -> None:
        """Auxillary class, helps dealing with card data.

        Args:
            card (Card): card from which to take data.
            front (_type_): which language to update.
            languages (_type_): _description_
        """

        if front == card.languages[0]:
            self.last = card.key0_last
            self.next = card.key0_next

        elif front == card.languages[1]:
            self.last = card.key1_last
            self.next = card.key1_next
    
    def generate_data(self, front, languages):
        if front == languages[0]:
            data = {
                "key0_last":self.last,
                "key0_next":self.next,
                }
        elif front == languages[1]:
            data = {
                "key1_last":self.last,
                "key1_next":self.next,
                }
        return data


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

