import random
import easygui
from vocab import alphabet
import text_messages

TITLE = "Guesser"


def generate_batch(source, number, mode):
    """
    This will generate a specific number of cards from the source,
    with mode 0/1 expressing whether they will be asking to match
    the card's key or value.
    """
    source = random.sample(source.items(), number)
    if mode == 0:
        result = {k: v for k, v in source}
    else:
        result = {v: k for k, v in source}
    return result


def show_batch(batch):
    """
    This will start a sequence of cards for the player.
    Takes in a dictionary with keys (front of a card) and values
    (back of a card.)
    """
    counter = 1

    for card in batch.keys():
        question_message = f"""
        Card {counter} of {len(batch.keys())}
        What is letter "{card}"?
        """
        answer_message = f"""
        The correct answer is: "{batch[card]}"
        Next?"""

        easygui.msgbox(question_message, TITLE)
        easygui.msgbox(answer_message, TITLE)
        counter += 1


# Greetings
easygui.msgbox(text_messages.hello, TITLE)

# Telling user only alphabet practice is gonna work.
easygui.msgbox(text_messages.alphabetMessage, TITLE)

# Let's ask the player if he wants to practice recognition or recall.
chosen_mode = easygui.indexbox(
    text_messages.modeMessage,
    choices=text_messages.modeChoices,
    title=TITLE)

# Now Generating a batch of random N cards.
# Maybe ask user to specify it?
new_batch = generate_batch(alphabet, 5, chosen_mode)

show_batch(new_batch)
