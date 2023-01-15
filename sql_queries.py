import sqlite3
from config import DATABASE

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
    """ Generate deck-descritpion-numberofcards dict.
    """

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
    """Make a list of languages pair.

    Args: 
        deck_name (str): name of deck.

    Returns:
        (list): list of languages 
    """

    query = f"""SELECT  language_1,
                        language_2
                FROM    decks
                WHERE   name = '{deck_name}'
            """
    result = request(query)
    languages = [result["language_1"], result["language_2"]]
    return languages


def init_deck(deck_name:str) -> dict:
    """Get deck metadata.

    Args:
        deck_name (str):

    Returns:
        Constructs a dict with these keys:
            name (str): Deck name
            language_1, language_2 (str): Deck languages
            description (str): Deck description
    """

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


def init_cards(deck_name:str) -> list:
    """Extract card data from db.

        Args:
            deck_name: name of the deck.

        Returns: (list of dicts)
        This is used later for inititalizing card objects.
    """

    query = f"""SELECT  *
                FROM    CARDS
                WHERE   deck ='{deck_name}'
    """
    result = request(query)
    return result


def get_card(id:int) -> dict:
    """Gets the card data from db for later inititalization.

    Args:
        id (int): card id

    Returns:
        dict: card data.
    """

    query = f"select * from cards where id ='{id}'"
    result = request(query)
    return result


def edit_card(data:dict):
    """ Change card data.

    Args:
        data (dict): dict with data values.
    """

    query = f"""UPDATE  cards
                SET     key_0 = "{data["key0"]}",
                        key_1 = "{data["key1"]}",
                        key_0_last_date = "{data["key0_last"]}",
                        key_0_next_date = "{data["key0_next"]}",
                        key_1_last_date = "{data["key1_last"]}",
                        key_1_next_date = "{data["key1_next"]}"
                WHERE   id = '{data["id"]}'
    """
    request(query)

def add_card(data:dict):
    query = f"""INSERT INTO CARDS(  key_0,
                                    key_1,
                                    key_0_last_date,
                                    key_0_next_date,
                                    key_1_last_date,
                                    key_1_next_date,
                                    deck
                            )
                            VALUES  (?,?,?,?,?,?,?)
    """
    values = (
        data["key0"],
        data["key1"],
        data["key0_last"],
        data["key0_next"],
        data["key1_last"],
        data["key1_next"],
        data["deck"]
    )
    request(query, values)