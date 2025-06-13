import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from unittest.mock import patch, mock_open, call
from burger import (
    get_order_timestamp,
    GetBun,
    calculate_burger_price,
    getMeat,
    GET_SAUCE,
    get_cheese123,
    AssembleBurger,
    SaveBurger,
    BURGER_COUNT,
    last_burger,
)
import re


class TestBurgerMaker(unittest.TestCase):

    def test_get_order_timestamp_format(self):
        ts = get_order_timestamp()
        self.assertIsInstance(ts, str)
        # Vérifie que ça ressemble à un datetime
        self.assertRegex(ts, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    @patch("builtins.input", return_value="sesame")
    def test_GetBun(self, mock_input):
        bun = GetBun()
        self.assertEqual(bun, "sesame")

    @patch("builtins.input", return_value="brioche")
    def test_get_bun(self, mock_input):
        bun = GetBun()
        self.assertEqual(bun, "brioche")

    def test_calculate_burger_price_basic(self):
        price = calculate_burger_price(["bun"])
        expected = 2.0 * 1.1 * 1.1  # tax applied twice
        self.assertAlmostEqual(price, expected)

    def test_calculate_burger_price_multiple(self):
        ingredients = ["bun", "cheese", "tomato"]
        base = 2.0 + 1.0 + 0.5
        expected = base * 1.1 * 1.1
        self.assertAlmostEqual(calculate_burger_price(ingredients), expected)

    def test_calculate_burger_price_unknown(self):
        # Unknown ingredients should be ignored (value = 0)
        self.assertAlmostEqual(calculate_burger_price(["unknown"]), 0)

    @patch("builtins.input", return_value="beef")
    def test_getMeat(self, mock_input):
        meat = getMeat()
        self.assertEqual(meat, "beef")

    def test_GET_SAUCE(self):
        sauce = GET_SAUCE()
        self.assertEqual(sauce, "ketchup and mustard")

    @patch("builtins.input", return_value="cheddar")
    def test_get_cheese123(self, mock_input):
        cheese = get_cheese123()
        self.assertEqual(cheese, "cheddar")

    @patch("builtins.input", side_effect=["brioche", "beef", "cheddar"])
    def test_AssembleBurger(self, mock_input):
        burger = AssembleBurger()
        self.assertIn("brioche", burger)
        self.assertIn("beef", burger)
        self.assertIn("cheddar", burger)
        self.assertIn("ketchup", burger)  # from GET_SAUCE
        self.assertTrue(len(burger) > 0)


    @patch("builtins.open", new_callable=mock_open)
    def test_SaveBurger(self, mock_open_file):
        burger_text = "TestBurger"
        SaveBurger(burger_text, burger_count=42)

        # Vérifie les appels à open()
        expected_calls = [
            call("/tmp/burger.txt", "w"),
            call("/tmp/burger_count.txt", "w"),
        ]
        mock_open_file.assert_has_calls(expected_calls, any_order=True)

        # Vérifie les écritures dans les fichiers
        handle = mock_open_file()
        handle.write.assert_any_call("TestBurger")
        handle.write.assert_any_call("42")


        
    @patch("builtins.input", side_effect=["brioche", "beef", "cheddar"])
    @patch("builtins.open", new_callable=mock_open)
    def test_MAIN_integration(self, mock_file, mock_input):
        # Test de bout en bout d'une exécution typique
        burger = AssembleBurger()
        SaveBurger(burger)
        self.assertIn("brioche", burger)
        self.assertIn("cheddar", burger)
        self.assertTrue(mock_file.called)


if __name__ == "__main__":
    unittest.main()
