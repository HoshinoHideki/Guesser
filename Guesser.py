import json
from flask import Flask, render_template, request
from flask_wtf import Form
from cards import *

app = Flask(__name__)


def get_fields(dict_list):
    fields = ["id", ]
    for dictionary in dict_list:
        for field in dictionary.keys():
            if field != "id" and field != "data" and field not in fields:
                fields.insert(len(fields), field)
        fields[1:].sort()
    return fields


def find_item(item_id, deckname):
    out_item = {}
    for item in deckname:
        if item["id"] == item_id:
            out_item = item
    return out_item


def update_item(deck, item_id, data):
    global database
    for item in deck:
        if item["id"] == item_id:
            for key in data:
                item[key] = data[key]
            with open("data_s.json", "w", encoding="utf-8") as database_file:
                json.dump(
                    database,
                    database_file,
                    ensure_ascii=False,
                    indent=4)
    else:
        return "ID not found."


# Routing. Move to different module?
@app.route("/")
@app.route("/index/")
def index():
    return render_template("index.html")


@app.route("/browse/")
def browse():
    decks = list_decks(database)
    return render_template("deck_select.html", decks=decks)


@app.route("/browse/<deckname>")
def browse_deck(deckname):
    deck = load_deck(database, deckname)
    fields = get_fields(deck)
    return render_template("browse.html",
                           deckname=deckname,
                           deck=deck,
                           fields=fields)


@app.route("/edit/<deckname>/<card_id>", methods=["POST", "GET"])
def edit_item(deckname, card_id):
    if request.method == "GET":
        fields = get_fields(deckname)
        item = find_item(card_id, deckname)
        return render_template("edit.html", item=item, fields=fields)
    if request.method == "POST":
        update_item(deckname, request.form["id"], request.form)
        return "done"


@app.route("/train/<deck>/front_select/")
def deck_lang_select(deck):
    langs = list_langs(get_fields(database[deck]))
    return render_template("train_select_lang.html", deck=deck, langs=langs)


@app.route("/train/")
@app.route("/train/select/")
def train():
    return render_template("train_select_deck.html",
                           decks=list_decks(database))


@app.route("/train/<deck>/<front>")
def train_deck(deck, front):
    card = pick_card(database[deck], front=front)
    return render_template("train.html",
                           front=card.front,
                           back=card.back,
                           deck=deck,
                           lang=front)


@app.route("/test/", methods=['POST', 'GET'])
def ttest():
    """
    Test route for receiving and storing data
    """
    form = Form
    form.armenian = "Test"
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


def list_langs(field_list):
    """takes a list of fields, filters them out"""
    langs = []
    for field in field_list:
        if field.startswith("key_"):
            langs.append(field[4:])
    return langs


def load_deck(database, deck):
    deck = database[deck]
    return deck


def list_decks(database):
    decks = []
    for key in database.keys():
        decks.append(key)
    decks.sort()
    return decks


def load_database(name):
    with open(name, "r", encoding="utf-8") as file:
        database = json.load(file)
    return database


database = load_database("data_s.json")


# Start frontend
if __name__ == "__main__":
    app.run(debug=True)
