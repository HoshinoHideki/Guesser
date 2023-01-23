from datetime import datetime

class config:
    ...

# format of date and time to convert from object to string and back
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# empty template for creating a new card
BLANK_CARD = {
    "id_":"",
    "key_0":"",
    "key_1":"",
    "key_0_last_date":"",
    "key_0_next_date":"",
    "key_1_last_date":"",
    "key_1_next_date":"",
    "deck":"",
}

# time multiplication factor
FACTOR = 5

DATABASE = "database.db"