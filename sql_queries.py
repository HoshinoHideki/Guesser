import sqlite3
from config import DATABASE
from datetime import datetime

def request(statement:str, *values:tuple) ->list or dict:
    """Generate a result from an sql query.
    Takes a statement and then possibly arguments in a tuple to execute.
    Commits any changes in the db.

    Args:
        statement (str): Query to perform.

    Returns:
        list or dict: Creates a list of dicts with column names as keys.
        If query returns only one row, returns only one dictionary.
    """

    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(statement, *values)
        rows = cursor.fetchall()

        dicts = []
        for row in rows:
            dic = {key:row[key] for key in row.keys()}
            dicts.append(dic)

        connection.commit()
        cursor.close()
    if len(dicts) == 1: 
        dicts = dicts[0]
    return dicts


def index_info() -> dict:
    """
    Crunches some numbers for the index page:
        total_decks: number of decks
        total_cards: number of cards
        total_due: number of due cards
            (one card with both fronts due counts as two)
    """

    query = f"""
        SELECT  COUNT(distinct deck)
                    AS  total_decks,
                COUNT(id)
                    AS  total_cards,
                SUM(CASE
                        WHEN    key_0_next_date = ""
                        OR      key_0_next_date = ""
                        THEN    0
                        WHEN    key_0_next_date < datetime('now', 'localtime')
                        AND     key_1_next_date < datetime('now', 'localtime')
                        THEN    2
                        WHEN    key_0_next_date < datetime('now', 'localtime')
                        OR      key_1_next_date < datetime('now', 'localtime')
                        AND     key_1_next_date != ""
                        THEN    1
                        ELSE 0
                        END)
                    AS total_due
        FROM cards
"""
    result = request(query)
    return result


def browse_decks():
    query = """
        SELECT  decks.name,
                decks.description,
                SUM(CASE    WHEN    deck = name
                            THEN    1 
                            ELSE    0
                            END
                    ) as cards
        FROM    cards,
                decks
        GROUP   BY name;
    """
    result = request(query)
    return result


def get_languages(deck_name:str) -> list:
    query = f"""SELECT  language_1,
                        language_2
                FROM    decks
                WHERE   name = '{deck_name}'
            """
    result = request(query)
    languages = [result["language_1"], result["language_2"]]
    return languages

def init_deck(deck_name:str) -> dict: 
    query = f"""
        SELECT  name,
                language_1,
                language_2,
                description
        FROM    decks
        WHERE   name = '{deck_name}'
    """
    result = request(query)
    return result