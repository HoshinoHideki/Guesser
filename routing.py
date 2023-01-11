from flask import Flask, render_template, request, url_for, redirect
from Guesser import app
from deck_manager import *
import sql_queries

@app.route("/")
@app.route("/index/")
def index():
    """Starting page. Tells you how many decks there are, how many cards
    in total and how many of them are due.
    """

    index = sql_queries.index_info()
    return render_template(
        "index.html",
        number_of_decks = index["total_decks"],
        total_cards = index["total_cards"],
        total_due= index["total_due"],
        )


@app.route("/browse/")
def browse():
    """Displays a list of decks in the app, with number of cards per deck.

    Context Args:
        collection: Collection object.
    """

    collection = Collection()

    return render_template(
        "browse/select_deck.html", 
        collection = collection,
        )


@app.route("/browse/<deck_name>/", methods=["GET", "POST"])
def browse_deck(deck_name: str):
    """GET: Displays a table of all entries in a selected deck.
    POST: Updates or adds a card to deck via web interface.

    Args:
        deck_name (str): Name of deck.
    
    Context Args:
        deck (dict): Dictionary containing deck data and information.
    """
    
    deck = Deck(deck_name)
    
    if request.method == "GET":
        return render_template("browse/deck.html", 
                                deck=deck)

    if request.method == "POST":
        if request.form["action"] == "edit":
            deck.edit_card(request.form["id"], request.form)
        if request.form["action"] == "add":
            deck.add_card(request.form)
        if request.form["action"] == "delete":
            deck.delete_card(id=request.form["id"])
    return redirect(url_for("browse_deck", deck_name=deck.name))


@app.route("/train/")
def train():
    """Lists user decks available for training, as well giving the number
       of due cards and setting a timer until the next due card.

    Context Args:
        collection: Collection object.
    """

    collection = Collection()

    return render_template(
        "train/choose_deck.html",
        collection=collection,
        )


@app.route("/train/<deck_name>/<front>", methods=["GET", "POST"])
def train_deck(deck_name: str, front: str):
    """Actual training interface. 
    
    Course of actions:
        1. Get the due cards. If no due cards are up: redirects to new card
        adding interface.
        2. Pick one card from the due deck and generate flashcard.
        3. The training page shows you the front card, you need to
        remember the end card. That's about it.
        Then it shows you the right answer, and based on your response
        (button pressed), resets the card's timer values or increments it.

    GET:
        Gets a card to train. If no card is available, redirects to learning
        a new card.

    POST:
        Updates the date and redirects to the same page.

    Possible modifications: multiple choice buttons. 
    Or entry field, though I'm not sure.

    Args:
        deck_name  (str): deck name string.
        front      (str): front card language.
    Context Args:
        deck           (Deck): Dictionary containing deck data and information.
        due_deck       (list): Dictionary deck with non-due cards stripped.
        flashcard (flashcard): card object, generated by fn.
        due_cards       (int): number of cards left. 
    """
    
    deck = Deck(deck_name)

    if request.method == "GET":
        due_deck = deck.get_due(front)

        # redirects to adding new cards if there are no due.
        if len(due_deck) == 0:
            return redirect(url_for(
                "learn", 
                deck_name=deck_name, 
                front=front))

        # picks a card and generates a quiz page.
        else:
            flashcard = deck.make_flashcard(front)
            number_of_cards = len(due_deck)
            return render_template(
                "train/train.html",
                flashcard=flashcard,
                deck_name=deck_name,
                front=front,
                deck=deck,
                )
    
    if request.method == "POST":
        flashcard = deck.get_card(request.form["id"])
        deck.update_date(request.form["id"], front, request.form["method"])
        return redirect(url_for(
            "train_deck", 
            deck_name=deck_name,
            front=front
            )
        )


@app.route("/learn/<deck_name>/<front>", methods=["POST", "GET"])
def learn(deck_name: str, front: str):
    """An interface for adding new due cards to the deck.
    
    
    GET: Asks whether you want to learn new cards or not.

    POST: Checks if there are new cards to learn in the deck and if the card
          is already shown to user.
          If no cards left, redirects to the "oops page".
          If card is already shown to user and he agrees to add them to deck,
          sets due date to right now.

    Subject for rewriting. 

    Args:
        deck_name (str): Deck name.
        front (str): Front language.

    Context args:
        result (str): Either "Done" or "Empty".
        deck (dict): Dictionary containing deck data and information.
    """

    
    # Runs a confirmation message if accessed via ordinary GET request.
    if request.method == "GET":
        return render_template(
            "new/cards.html", 
            deck_name=deck_name,
            front=front,
            action = "confirm",
            )

    if request.method == "POST":
        deck = Deck(deck_name)

        # learn a new card if there are any 
        if request.form["action"] == "learn":
            learn_deck = deck.get_unlearned()

            # prompt to add new cards if no unlearned cards.
            if len(learn_deck) == 0:
                return render_template("new/oops.html", deck_name=deck_name)

            else:
                card = learn_deck[0]
                deck.set_due(learn_deck[0].id)
                return render_template(
                        "new/cards.html",
                        card=card, 
                        deck_name=deck_name,
                        languages=deck.languages
                        )

        if request.form["action"] == "review":
            return redirect(
                url_for("train_deck", deck_name=deck_name, front=front))
