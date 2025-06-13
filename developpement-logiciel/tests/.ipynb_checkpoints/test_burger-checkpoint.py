import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, mock_open, call

from burger import (
    get_order_timestamp,
    get_bun,
    calculate_burger_price,
    get_meat,
    get_sauce,
    get_cheese,
    assemble_burger,
    save_burger,
)


class TestBurgerMaker(unittest.TestCase):

    def test_get_order_timestamp_format(self):
        ts = get_order_timestamp()
        self.assertIsInstance(ts, str)
        self.assertRegex(ts, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    @patch("builtins.input", return_value="sesame")
    def test_get_bun(self, mock_input):
        bun = get_bun()
        self.assertEqual(bun, "sesame")

    def test_calculate_burger_price_basic(self):
        price = calculate_burger_price(["bun"])
        expected = 2.0 * 1.1 * 1.1
        self.assertAlmostEqual(price, expected)

    def test_calculate_burger_price_multiple(self):
        ingredients = ["bun", "cheese", "tomato"]
        base = 2.0 + 1.0 + 0.5
        expected = base * 1.1 * 1.1
        self.assertAlmostEqual(calculate_burger_price(ingredients), expected)

    def test_calculate_burger_price_unknown(self):
        self.assertAlmostEqual(calculate_burger_price(["unknown"]), 0)

    @patch("builtins.input", return_value="beef")
    def test_get_meat(self, mock_input):
        meat = get_meat()
        self.assertEqual(meat, "beef")

    def test_get_sauce(self):
        sauce = get_sauce()
        self.assertEqual(sauce, "ketchup and mustard")

    @patch("builtins.input", return_value="cheddar")
    def test_get_cheese(self, mock_input):
        cheese = get_cheese()
        self.assertEqual(cheese, "cheddar")

    @patch("builtins.input", side_effect=["brioche", "beef", "cheddar"])
    def test_assemble_burger(self, mock_input):
        burger = assemble_burger()
        self.assertIn("brioche", burger)
        self.assertIn("beef", burger)
        self.assertIn("cheddar", burger)
        self.assertIn("ketchup", burger)
        self.assertTrue(len(burger) > 0)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_burger(self, mock_open_file):
        burger_text = "TestBurger"
        save_burger(burger_text)

        expected_calls = [
            call("/tmp/burger.txt", "w"),
            call("/tmp/burger_count.txt", "w"),
        ]
        mock_open_file.assert_has_calls(expected_calls, any_order=True)

        handle = mock_open_file()
        handle.write.assert_any_call("TestBurger")
        # Le nombre de burgers écrits peut varier, donc on ne teste pas la valeur exacte ici


    @patch("builtins.input", side_effect=["brioche", "beef", "cheddar"])
    @patch("builtins.open", new_callable=mock_open)
    def test_main_integration(self, mock_file, mock_input):
        burger = assemble_burger()
        save_burger(burger)
        self.assertIn("brioche", burger)
        self.assertIn("cheddar", burger)
        self.assertTrue(mock_file.called)


if __name__ == "__main__":
    unittest.main()

