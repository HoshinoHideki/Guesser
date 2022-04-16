import random
import easygui
import json
import text_messages


class Card:
    def __init__(self, front, back):
        self.front = front
        self.back = back


def generate_batch(source, number, front, back):
    """
    This generates a list of Сard objects from the source.
    The Сard object has two attributes: "front" and "back".
    Attribute "front" designates which key is the front value.
    Attribute "back" designates which key the back value.
    """

    source = random.sample(source, number)
    batch = list()

    for entry in source:
        # Every iterable is a dict with two entries.
        # Dict key designates whether it is a front or a back of the card.
        # Dict values = values of the attributes.
        card = Card(front=entry[front], back=entry[back])
        batch.append(card)

    return batch


def show_batch(batch):
    """
    This will start a sequence of cards for the player.
    Takes in a dictionary of Card objects with ".front" and ".back" attributes
    and then shows each front card and then back card.
    There is no feedback from user yet.
    """

    counter = 1

    # Iterate through cards:
    for card in batch:
        # Front text content:
        question_message = f"""
                   Card {counter} of {len(batch)}
                   What is "{card.front}"?
                   """
        # Back text content:
        answer_message = f"""
                   The correct answer is: "{card.back}"
                   Next?"""

        easygui.msgbox(question_message, TITLE)
        easygui.msgbox(answer_message, TITLE)
        counter += 1


TITLE = "Guesser"

# Load the database
with open("alphabet.json", "r", encoding="utf-8") as file:
    database = json.load(file)

# Greetings
easygui.msgbox(text_messages.hello, TITLE)

# Main Loop.
while True:
    mainmenu = easygui.choicebox(msg="Select what you want to do.",
                                 title="Language Guesser",
                                 choices=["Train", "Browse"])

    if mainmenu == "Train":
        # TODO:
            # Choosing a pool of exercise.
            # Choosing a front\back mode.
        # Let's ask the player if he wants to practice recognition or recall.
        # front_choice = [] #a piece of code that generates a list consisting
        # ["english", "armenian"]
        # front = easygui.choicebox(
        #     text_messages.modeMessage,
        #     choices=front_choice,
        #     title=TITLE)

        # Now Generating a batch of random N cards.
        # Maybe ask user to specify how many?
        new_batch = generate_batch(database["alphabet"], 5, "armenian", "english")

        # Show the training batch.
        show_batch(new_batch)

    if mainmenu == "Browse":
        # this shows a list of cards without any functionality.
        # to do: choice whether to show english or armenian letters.
        alphabet_choices = list()
        for item in database["alphabet"]:
            alphabet_choices.append(f'{item["armenian"]}: {item["english"]}')
        alphabet_lookup = easygui.choicebox("List of cards:",
                                            title=TITLE,
                                            choices=alphabet_choices,
                                            )
    if not mainmenu:
        break
