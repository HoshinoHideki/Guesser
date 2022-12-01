from datetime import datetime

DATABASE = "data_v3.json"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

BLANK_CARD = {
    "key_0": "",
    "key_1": "",
    "card_id": "",
    "key_0_data": {
        "last_date": "",
        "next_date": "",
    },
    "key_1_data": {
        "last_date": "",
        "next_date": "",
    }
}

ITEM_STRUCTURE = {
    "deck":{
        "languages":
            ["",""],
        "cards":[BLANK_CARD,]
    }
}

DATA_FOLDER = "decks/"

FACTOR = 5