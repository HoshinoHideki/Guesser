import random


class Card:
    """A simple object, has "front" and "back" attributes.
    """
    def __init__(self, front, back):
        self.front = front
        self.back = back


def pick_card(deck, front):
    """
    This makes a Card object from the deck.
    deck: list object containing dictionary objects.
    front: string value telling function which value assign to the front.
    Function then picks a random dict and checks whether one of its "key
    values" matches front value set by user. Then it assigns this value to
    the front attribute of a card, and the other one - to the back.
    """
    entry = random.choice(deck) # picks up a dict
    for key in entry.keys():
        if key.startswith("key_") and not key.endswith(front):
            back=entry[key]
        elif key.startswith("key_") and key.endswith(front):
            front=entry[key]
    card = Card(front=front, back=back)
    return card
