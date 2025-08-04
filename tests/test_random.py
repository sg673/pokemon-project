import unittest
import pandas as pd
from core.random import generate_random_rows

# Set up dummy dataframe to test on
dummy_df = pd.DataFrame(
    {
        "name": [
            "Bulbasaur",
            "Charmander",
            "Squirtle",
            "Pidgey",
            "Gastrodon",
            "OmegaArmormon Burst Mode",
            "OmegaArmormon Chaos Mode",
        ],
        "pokedex_number": [1, 2, 3, 4, 5, 6, 7],
    }
)


class TestRandom(unittest.TestCase):

    def setUp(self):
        self.df = dummy_df.copy()

    def test_generate_one_row_returns_one_row(self):
        result = generate_random_rows(self.df, -1, 1)
        self.assertEqual(len(result), 1)

    def test_generate_five_rows_returns_five_rows(self):
        result = generate_random_rows(self.df, -1, 5)
        self.assertEqual(len(result), 5)

    def test_generator_should_never_return_excluded(self):
        result = generate_random_rows(self.df, 1, 6)
        self.assertEqual(len(result), 6)

        names = set(result["name"])
        expected_names = {
            "Charmander",
            "Squirtle",
            "Pidgey",
            "Gastrodon",
            "OmegaArmormon Burst Mode",
            "OmegaArmormon Chaos Mode"}

        self.assertSetEqual(names, expected_names)
