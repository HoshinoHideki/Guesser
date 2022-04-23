import json

with open("data2.json","r+", encoding="utf-8") as file:
    data = json.load(file)

for entry in data["alphabet"]:
    entry["data"] = {}

with open("data_new.json", "w", encoding="utf-8")as output:
    json.dump(data, output, ensure_ascii=False, indent=4)