import json

with open("data_v3.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for key in data.keys():
    ...


with open("data_v4.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=None)