import unittest
from deck_manager import *
import sql_queries

class Test_Card(unittest.TestCase):
    def test_Card_init(self):
        deck_names = [deck["name"] for deck in sql_queries.browse_decks()]
        for deck_name in deck_names:
            deck = Deck(deck_name)
            for card in deck.cards:
                self.assertIsInstance(card, Card)
                self.assertIsInstance(card.id_, int)
                self.assertIsInstance(card.key0, str)
                self.assertIsInstance(card.key1, str)
                self.assertIsInstance(card.key0_last, str)
                self.assertIsInstance(card.key1_last, str)
                self.assertIsInstance(card.key0_next, str)
                self.assertIsInstance(card.key1_next, str)
                self.assertIsInstance(card.deck, str)
                self.assertIsInstance(card.languages, list)


class Test_Flashcard(unittest.TestCase):
    def test_init(self):
        id = 65
        front = "test_front"
        back = "test_back"
        flashcard = Flashcard(id, front, back)
        self.assertTrue(isinstance(flashcard, Flashcard))
    
    def test_new_flascard(self):
        deck_names = [deck["name"] for deck in sql_queries.browse_decks()]
        for deck_name in deck_names:
            languages = sql_queries.get_languages(deck_name)
            for language in languages:
                    if len(sql_queries.get_due(deck_name, language)):
                        flashcard = make_flashcard(deck_name, language)
                        self.assertIsInstance(flashcard, Flashcard)


class Test_Deck_Methods(unittest.TestCase):
    def test_Deck_init(self):
        deck_names = [deck["name"] for deck in sql_queries.browse_decks()]
        for deck_name in deck_names:
            test_deck = Deck(deck_name)
            self.assertIsInstance(test_deck, Deck)
            self.assertTrue(test_deck.description)
            self.assertIsInstance(test_deck.description, str)
            self.assertTrue(test_deck.languages)
            self.assertIsInstance(test_deck.languages, list)
            self.assertTrue(test_deck.cards)
            self.assertIsInstance(test_deck.cards, list)
    

    def test_due_deck_init(self):
        deck_names = [deck["name"] for deck in sql_queries.browse_decks()]
        for deck_name in deck_names:
            deck = Deck(deck_name)
            due_0 = get_due(deck_name, deck.languages[0])
            due_1 = get_due(deck_name, deck.languages[1])
            self.assertTrue(
                (
                    isinstance(due_0, list) or 
                    len(due_0) == 0
                ) and (
                    isinstance(due_1, list) or 
                    len(due_1) == 0
                )
            )

    def test_get_unlearned(self):
        deck_names = [deck["name"] for deck in sql_queries.browse_decks()]
        for deck_name in deck_names:
            card = get_unlearned(deck_name)
            if card != "":
                self.assertIsInstance(card, Card)
                self.assertIsInstance(card.id_, int)
                self.assertIsInstance(card.key0, str)
                self.assertIsInstance(card.key1, str)
                self.assertIsInstance(card.key0_last, str)
                self.assertIsInstance(card.key1_last, str)
                self.assertIsInstance(card.key0_next, str)
                self.assertIsInstance(card.key1_next, str)
                self.assertIsInstance(card.deck, str)
                self.assertIsInstance(card.languages, list)