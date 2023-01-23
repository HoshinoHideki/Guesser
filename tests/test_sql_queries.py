import unittest
from sql_queries import *

class TestQuery(unittest.TestCase):
    def test_request(self):
        # this tests if list truncating for single row works:
        single_row = """Select count(*) from cards"""
        result = request(single_row)
        self.assertIsInstance(result, dict)

        #this tests if request returns a list of dicts by default:
        multiple_rows = "Select * from decks"
        result = request(multiple_rows)
        self.assertIsInstance(result, list)


    def test_index_info(self):
        result = index_info()
        self.assertIsInstance(result, dict)


    def test_browse_decks(self):
        result = browse_decks()
        self.assertIsInstance(result, list or dict)
        for deck in result:
            self.assertEqual(len(deck.keys()), 3)
            self.assertIsInstance(deck["name"], str)
            self.assertIsInstance(deck["cards"], int)


    def test_get_languages(self):
        deck_names = [deck["name"] for deck in browse_decks()]
        for deck_name in deck_names: 
            languages = get_languages(deck_name)
            self.assertEqual(len(languages), 2)
            for language in languages:
                self.assertIsInstance(language, str)


    def test_init_deck(self):
        deck_names = [deck["name"] for deck in browse_decks()]
        for deck_name in deck_names:
            dic = init_deck(deck_name)
            self.assertIsInstance(dic, dict)

    def test_init_cards(self):
        deck_names = [deck["name"] for deck in browse_decks()]
        for deck_name in deck_names:
            cards = init_cards(deck_name)
            self.assertIsInstance(cards, list)
            for card in cards:
                self.assertIsInstance(card, dict)


    def test_due_deck(self):
        deck_names = [deck["name"] for deck in browse_decks()]
        for deck_name in deck_names:
            languages = get_languages(deck_name)
            for language in languages:
                due_cards = get_due(deck_name, language)
                self.assertTrue(
                    isinstance(due_cards, list) or 
                    len(due_cards) == 0
                )
    
    def test_unlearned(self):
        deck_names = [deck["name"] for deck in browse_decks()]
        for deck_name in deck_names:
            unlearned = get_unlearned(deck_name)
            self.assertTrue(
                isinstance(unlearned, dict) or 
                len(unlearned) == 0
            )
            if len(unlearned) != 0:
                self.assertEqual(unlearned["deck"], deck_name)
                self.assertEqual(unlearned["key_0_next_date"], "")
                self.assertEqual(unlearned["key_1_next_date"], "")
                self.assertEqual(unlearned["key_0_last_date"], "")
                self.assertEqual(unlearned["key_1_last_date"], "")

