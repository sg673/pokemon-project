import unittest
import pandas as pd
from core.filters import filter_by_status, filter_by_type, filter_by_dual_type


class TestFilterByType(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
            {
                "name": ["Bulbasaur", "Charmander", "Squirtle", "Pidgey"],
                "type_1": ["Grass", "Fire", "Water", "Normal"],
                "type_2": ["Poison", None, None, "Flying"],
            }
        )

    def test_filter_by_primary_type(self):
        result = filter_by_type(self.df, "Fire")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "Charmander")

    def test_filter_by_secondary_type(self):
        result = filter_by_type(self.df, "Flying")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "Pidgey")

    def test_filter_by_type_multiple(self):
        result = filter_by_type(self.df, "Poison")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "Bulbasaur")

    def test_filter_by_type_no_matches(self):
        result = filter_by_type(self.df, "Electric")
        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
