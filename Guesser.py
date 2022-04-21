import random
import json
from flask import Flask, render_template
app = Flask(__name__)


class Card:
    def __init__(self, front, back):
        self.front = front
        self.back = back


def generate_batch(source, number, front, back):
    """
    This generates a list of "Сard" objects from the source.
    The Сard object has two attributes: "front" and "back".
    Attribute "front" designates which key is the front value.
    Attribute "back" designates which key the back value.
    """

    source = random.sample(source, number)
    new_batch = list()

    for entry in source:
        # Every iterable is a dict with two entries.
        # Dict key designates whether it is a front or a back of the card.
        # Dict values = values of the attributes.
        card = Card(front=entry[front], back=entry[back])
        new_batch.append(card)
    return new_batch


# def show_batch(batch):
#     """
#     This will start a sequence of cards for the player.
#     Takes in a dictionary of Card objects with ".front" and ".back"
#     attributes and then shows each front card and then back card.
#     There is no feedback from user yet.
#     """
#     global counter
#     front = batch[counter].front
#     back = batch[counter].back
#     return front, back, counter


# Routing. Move to different module?
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/browse")
def browse():
    return render_template("browse.html", data=database["alphabet"])


@app.route("/train")
def train():
    global counter, data
    counter = 0
    data = generate_batch(database["alphabet"], 5, "armenian", "english")
    return render_template("train.html",
                           front=data[counter].front,
                           back=data[counter].back,
                           counter=counter,
                           data=data)


@app.route("/train/next")
def train_next():
    global counter, data
    counter += 1
    if counter >= (len(data)):
        return render_template("/done.html")
    else:
        return render_template("train.html",
                               front=data[counter].front,
                               back=data[counter].back,
                               counter=counter,
                               data=data)


# Set globals?
counter = 0
data = []

# Load the database
# TODO: Testing stuff with just armenian alphabet. Possibly expand?
with open("alphabet.json", "r", encoding="utf-8") as file:
    database = json.load(file)

# Start frontend
if __name__ == "__main__":
    app.run(debug=True)


