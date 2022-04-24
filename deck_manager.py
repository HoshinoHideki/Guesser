import json


def get_fields(dict_list):
    """Makes a list starting with "id" and containing both key values.
    """
    fields = ["id", ]
    for dictionary in dict_list:
        for field in dictionary.keys():
            if field.startswith("key_") and not field in fields:
                fields.insert(len(fields), field)
        fields[1:].sort()
    return fields


def find_item(item_id, deckname):
    """Find a dictionary with the matching id key value. 
    Return empty dict if failed.
    """
    out_item = {}
    for item in deckname:
        if item["id"] == item_id:
            out_item = item
    return out_item


# TODO: make this work directly with the database file and not with the python object!
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


def list_langs(field_list):
    """takes a list of fields, filters them out"""
    langs = []
    for field in field_list:
        if field.startswith("key_") and not field in langs:
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