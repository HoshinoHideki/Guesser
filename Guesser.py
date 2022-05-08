
from flask import Flask, render_template, request, url_for, redirect
from deck_manager import *


app = Flask(__name__)


# Routing. Move to different module?
@app.route("/")
@app.route("/index/")
def index():
    """Starting page. Doesn't take any arguments (yet?)"""

    return render_template("index.html")


@app.route("/browse/")
def browse():
    """Displays a list of decks in the app.
    decks = list of deck name strings."""

    decks = list_decks()
    return render_template("deck_select.html", decks=decks)


@app.route("/browse/<deck>/", methods=["POST", "GET"])
def browse_deck(deck):
    """Displays a table of all entries in a select deck.
    deck = a list of dictionaries. Used for building table.
    fields = a list of column names.
    deckname = a string with the name of deck."""
    if request.method == "GET":
        cards = load_deck(deck)
        fields = get_fields(deck)
        return render_template("browse_deck.html",
                               deck=deck,
                               cards=cards,
                               fields=fields)

    if request.method == "POST":
        update_item(deck, request.form["card_id"], request.form)
        cards = load_deck(deck)
        fields = get_fields(deck)
        return render_template("browse_deck.html",
                               deck=deck,
                               cards=cards,
                               fields=fields)


@app.route("/browse/<deckname>/<card_id>/", methods=["POST", "GET"])
def edit_item(deckname, card_id):
    """GET: Opens an editing interface for a card selected by ID.
    Currently it only lets you edit the key value pairs.
    POST: Finds card selected by ID in the database,
    replaces the key values entered by user via the form.
    deckname: string containing deck's name.
    card_id: id key value.
    card: dictionary object representing the card.
    fields: list of strings representing the key values"""

    if request.method == "GET":
        fields = get_fields(deckname)
        card = find_item(card_id, deckname)
        return render_template("browse_deck_item.html",
                               card=card,
                               fields=fields)

    if request.method == "POST":
        update_item(deckname, request.form["card_id"], request.form)
        return "Item edited."


@app.route("/train/<deck>/front_select/")
def deck_lang_select(deck):
    """Lets user choose the front-card and the end-card of the language pair.
    deck: string with the deck name.
    langs: list object containing sorted language pair."""

    langs = list_langs(get_fields(deck))
    return render_template("train_deck_front.html", deck=deck, langs=langs)


@app.route("/train/")
@app.route("/train/select/")
def train():
    """Lists user decks available for training. 
    decks: list object containing string names of available decks.
    """
    decks = list_decks()
    return render_template("train_deck.html", decks=decks)


@app.route("/train/<deckname>/<front>")
def train_deck(deckname, front):
    """Actual training interface. It shows you the front card, you need to
    remember the end card. That's about it.
    Possible modifications: Okay/Again button like in anki or
    multiple choice buttons. Or entry field, though I'm not sure.
    deck: string object representing deck name
    front: string object indicating which value pair is front card.
    card: card object with front and back attributes, generated by fn.
    """    
    card = pick_card(deckname, front=front)
    return render_template("train.html",
                           front=card.front,
                           back=card.back,
                           deckname=deckname,
                           lang=front)


@app.route("/test/", methods=["GET", "POST"])
def test_page():
    if request.method == "GET":
        return render_template("testbutton.html")
    pass


# Start frontend
if __name__ == "__main__":
    app.run(debug=True)
