import json, os

with open("data_s.json", "r", encoding="utf-8") as file:
    data = json.load(file)

newdata = data["alphabet"]

path=os.path.curdir
print(path)
with open("./decks/alphabet.json", "w", encoding="utf-8") as file:
    json.dump(newdata, file, ensure_ascii=False, indent=3)