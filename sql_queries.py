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

    query = """
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


def browse_decks() -> dict:
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


def get_card(card_id:int) -> dict:
    """Gets the card data from db for later inititalization.

    Args:
        id (int): card id

    Returns:
        dict: card data.
    """

    query = f"select * from cards where id ='{card_id}'"
    result = request(query)
    return result


def edit_card(data:dict) -> None:
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
                WHERE   id = '{data["id_"]}'
    """
    request(query)


def add_card(data:dict, deck_name:str) -> None:
    """ Add a new card to deck.

    Args:
        data(dict): key-value pairs.
        deck_name(str): name of the deck.
    """

    query = """INSERT INTO CARDS(  key_0,
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
        deck_name
    )
    request(query, values)


def delete_card(id_:int) -> None:
    """ Delete card form db.
    """
    query = f"""DELETE FROM cards
                WHERE id = {id_}
    """
    request(query)


def train_data() -> list:
    query = """SELECT   decks.name,
                        decks.description,
                        decks.language_1,
                        SUM(CASE
                                WHEN    cards.key_0_next_date < 
                                            datetime('now', 'localtime')
                                AND     cards.key_0_next_date != ""
                                AND     cards.deck = name
                                THEN    1
                                ELSE    0
                            END) AS language_1_due_cards,
                        MIN(cards.key_0_next_date)
                            FILTER(
                                WHERE   cards.deck = name)
                            AS language_1_next_due,
                        decks.language_2,
                        SUM(CASE
                                WHEN    cards.key_1_next_date < 
                                            datetime('now', 'localtime')
                                AND     cards.key_0_next_date != ""
                                AND NOT ""
                                AND     cards.deck = name
                                THEN    1
                                ELSE    0
                            END) AS language_2_due_cards,
                        MIN(cards.key_1_next_date)
                            FILTER(
                                WHERE   cards.deck = name)
                            AS language_2_next_due
                FROM        cards,
                            decks
                GROUP BY    decks.name
    """
    result = request(query)
    return result

def get_due(deck_name:str, front:str) -> list:
    languages = get_languages(deck_name)
    keys = {
        languages[0]:"key_0_next_date",
        languages[1]:"key_1_next_date",

    }
    key = keys[front]
    query = f"""SELECT   *
                FROM     cards
                WHERE   {key} < datetime('now', 'localtime')
                AND     {key} != ""
                AND     deck = '{deck_name}'
                ORDER BY {key}
    """
    result = request(query)
    if isinstance(result, dict):
        result = [result]
    return result

def get_unlearned(deck_name:str) -> dict or None:
    query = f"""SELECT  *
                FROM    cards
                WHERE   key_0_last_date = ""
                AND     deck = '{deck_name}'
                OR      key_1_last_date = ""
                AND     deck = '{deck_name}'
                LIMIT   1
    """
    result = request(query)
    return result

def set_due(id_:int) -> None:
    query = f"""UPDATE  CARDS
                SET     key_0_last_date = datetime('now', 'localtime'),
                        key_0_next_date = datetime('now', 'localtime'),
                        key_1_last_date = datetime('now', 'localtime'),
                        key_1_next_date = datetime('now', 'localtime')
                WHERE   id = {id_}
    """
    request(query)