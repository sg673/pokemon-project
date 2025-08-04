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
