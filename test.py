from cgi import test
import json
from datetime import datetime, timedelta
import random
from deck_manager import get_due, count_due, get_key_string, get_next_card_due, get_next_id, load_database, total_cards
import re

# def pick(words, key):
#     lst = []
#     for dt in word_pool:
#         for word in [words]:
#             if word not in dt["tags"]:
#                 break
#         else:
#             lst.append(dt[key])
#     return random.choice(lst)
    

word_pool = [
    {
        "key_1": "kin",
        "key_2": "woman",
        "tags": ["noun", "feminine"]
    },
    {   "key_1": "mard",
        "key_2": "man",
        "tags" : ["noun", "masculine"]

    },
    {   "key_1": "azat",
        "key_2": "free",
        "tags" : ["noun",]

    },
]


pattern = r"\[(\w+)\]"
phrase = "[noun] [to be] [a] [man]"

match = re.findall(pattern, phrase)

# print(match)

def find_translation(deck_name, word):
    for card in load_database()[deck_name]["cards"]:
        if word == card["key_0"]:
            return card["key_1"]
        elif word == card["key_1"]:
            return card["key_0"]
    return "Not found"

print(find_translation("vocabulary","man"))