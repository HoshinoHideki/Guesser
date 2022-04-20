import random
import easygui
import json
# import text_messages
from flask import Flask, render_template
app = Flask(__name__)


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
        # Front text content:
    global counter
    front = batch[counter].front
    back = batch[counter].back
    return front, back, counter


TITLE = "Guesser"

# Load the database
with open("alphabet.json", "r", encoding="utf-8") as file:
    database = json.load(file)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/browse")
def browse():
    return render_template("browse.html", data=database["alphabet"])


@app.route("/train")
def train():
    global batch
    global counter
    counter = 0
    batch = generate_batch(database["alphabet"], 5, "armenian", "english")
    front, back, counter = show_batch(batch)
    return render_template("train.html",front=front, back=back, counter=counter, batch=batch)


@app.route("/train/next")
def train_next():
    global counter, batch
    counter += 1
    if counter >= (len(batch)):
        return "You are done"
    else:
        front, back, counter = show_batch(batch)
        return render_template("train.html", front=front, back=back, counter=counter, batch = batch)

# Greetings
# easygui.msgbox(text_messages.hello, TITLE)


if __name__ == "__main__":
    app.run(debug=True)

# Main Loop.
# while True:
#     mainmenu = easygui.choicebox(msg="Select what you want to do.",
#                                  title="Language Guesser",
#                                  choices=["Train", "Browse"])
#
#     if mainmenu == "Train":
#         # TODO:
#             # Choosing a pool of exercise.
#             # Choosing a front\back mode.
#         # Let's ask the player if he wants to practice recognition or recall.
#         # front_choice = [] #a piece of code that generates a list consisting
#         # ["english", "armenian"]
#         # front = easygui.choicebox(
#         #     text_messages.modeMessage,
#         #     choices=front_choice,
#         #     title=TITLE)
#
#         # Now Generating a batch of random N cards.
#         # Maybe ask user to specify how many?
#         new_batch = generate_batch(database["alphabet"],
#                                    5, "armenian", "english")
#
#         # Show the training batch.
#         show_batch(new_batch)
#
#     if mainmenu == "Browse":
#         # this shows a list of cards without any functionality.
#         # to do: choice whether to show english or armenian letters.
#         alphabet_choices = list()
#         for item in database["alphabet"]:
#             alphabet_choices.append(f'{item["armenian"]}: {item["english"]}')
#         alphabet_lookup = easygui.choicebox("List of cards:",
#                                             title=TITLE,
#                                             choices=alphabet_choices,
#                                             )
#     if not mainmenu:
#         break
