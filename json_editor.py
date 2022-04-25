import json

with open("data_copy.json", "r", encoding="utf-8") as file:
	data = json.load(file)

for entry in data["alphabet"]:
	entry["key_0"] = entry.pop("key_armenian")
	entry["key_1"] = entry.pop("key_english")
	entry["card_id"] = entry.pop("id")
	entry["lang_data"] = ["armenian", "english"]
	entry["key_0_data"] = {"last_date":"", "next_date":""}
	entry["key_1_data"] = {"last_date":"", "next_date":""}
	entry.pop("data")


with open("data_copy_v2.json", "w", encoding="utf-8") as file:
	json.dump(data, file, ensure_ascii=False, indent=4)