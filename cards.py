import random


class Card:
    def __init__(self, front, back):
        self.front = front
        self.back = back


def pick_card(deck, front):
    """
    This picks a Card object from the deck.
    The Сard object has two attributes: "front" and "back".
    Attribute "front" designates which key is the front value.
    Attribute "back" designates which key the back value.
    """
    entry = random.choice(deck) # picks up a dict
    for key in entry.keys():
        if key.startswith("key_") and not key.endswith(front):
            back=entry[key]
        elif key.startswith("key_") and key.endswith(front):
            front=entry[key]
    card = Card(front=front, back=back)
    return card
