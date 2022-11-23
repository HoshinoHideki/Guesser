import json, os

with open("data_v3.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for key in data.keys():
    filename = "decks/" + key + ".json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data[key], file, ensure_ascii=False, indent=4)

# path = "decks\\"

# decks = os.listdir(path)

# for deck in decks:
#     print("decks\\"+deck)
# with open("data_v4.json", "w", encoding="utf-8") as file:
#     json.dump(data, file, ensure_ascii=False, indent=None)