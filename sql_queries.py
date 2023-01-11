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


def index_info():
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
        SUM(CASE    WHEN    key_0_next_date < datetime('now', 'localtime')
                    AND     key_1_next_date < datetime('now', 'localtime')
                    THEN    2
                    WHEN    key_0_next_date < datetime('now', 'localtime')
                    OR      key_1_next_date < datetime('now', 'localtime') 
                    THEN    1
                    ELSE 0
                    END)
            AS total_due
        FROM cards
"""
    result = request(query)
    return result