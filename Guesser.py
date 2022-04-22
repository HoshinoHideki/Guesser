import random
import json
from flask import Flask, render_template, request
from flask_wtf import Form
from wtforms import StringField, SubmitField

app = Flask(__name__)


class Card:
    def __init__(self, front, back):
        self.front = front
        self.back = back


class LetterForm(Form):
    armenian = StringField("Armenian")
    english = StringField("English")
    submit = SubmitField("Send")


def pick_card(deck, front, back):
    """
    This generates a list of "Сard" objects from the deck.
    The Сard object has two attributes: "front" and "back".
    Attribute "front" designates which key is the front value.
    Attribute "back" designates which key the back value.
    """
    entry = random.choice(deck)
    card = Card(front=entry[front], back=entry[back])
    return card


# Routing. Move to different module?
@app.route("/")
@app.route("/index/")
def index():
    return render_template("index.html")


@app.route("/browse/")
def browse():
    decks = []
    for deck in database.keys():
        decks.append(deck)
    return render_template("deck_select.html", decks=decks)


@app.route("/browse/<deck>")
def browse_deck(deck):
    return render_template("browse.html", deck=deck, data=database[deck])


@app.route("/edit/<deck>/<int:card_id>")
def edit_item(deck, card_id):
    for item in database[deck]:
        if item["id"] == card_id:
            return render_template("edit.html", item=item)


@app.route("/train")
def train():
    card = pick_card(database["alphabet"], front="armenian", back="english")
    return render_template("train.html",
                           front=card.front,
                           back=card.back)


@app.route("/test/", methods=['POST', 'GET'])
def ttest():
    """
    Test route for recieving and storing data
    """
    form = LetterForm()
    if request.method == 'POST':
        letter = {"armenian": request.form["armenian"],
                  "english": request.form["english"]
                  }
        with open("test.json", "r+", encoding="utf-8") as database_file:
            data = json.load(database_file)
            data["letters"].append(letter)
            database_file.seek(0)
            json.dump(data, database_file, ensure_ascii=False, indent=4)
        return "Added!"
    else:  # request.method == "GET":
        return render_template("letter.html", form=form)


# Load the database
# TODO: Testing stuff with just armenian alphabet. Possibly expand?
with open("data2.json", "r", encoding="utf-8") as file:
    database = json.load(file)


# Start frontend
if __name__ == "__main__":
    app.run(debug=True)


