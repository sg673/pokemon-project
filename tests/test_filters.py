import unittest
import pandas as pd
from core.filters import filter_by_status, filter_by_type, filter_by_dual_type

# TODO: dual types and status test
# TODO: DRY on SetUp
# TODO: dCheck what the null types got changed to

# Set up dummy dataframe to test on
dummy_df = pd.DataFrame(
    {
        "name": [
            "Bulbasaur",
            "Charmander",
            "Squirtle",
            "Pidgey",
            "OmegaArmormon Burst Mode",
            "OmegaArmormon Chaos Mode",
        ],
        "type_1": ["Grass", "Fire", "Water", "Normal", "Normal", "Normal"],
        "type_2": ["Poison", None, None, "Flying", "Steel", "Steel"],
    }
)


class TestFilterByType(unittest.TestCase):

    def setUp(self):
        self.df = dummy_df.copy()

    def test_filter_by_primary_type(self):
        result = filter_by_type(self.df, "Fire")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "Charmander")

    def test_filter_by_secondary_type(self):
        result = filter_by_type(self.df, "Flying")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "Pidgey")

    def test_filter_by_type_multiple_matches(self):
        result = filter_by_type(self.df, "Normal")
        self.assertEqual(len(result), 2)

        names = set(result["name"])
        expected_names = {"Pidgey", "OmegaArmormon Burst Mode"}

        self.assertEqual(names, expected_names)

    def test_filter_by_type_no_matches(self):
        result = filter_by_type(self.df, "Electric")
        self.assertTrue(result.empty)


class TestFilterByDualTypes(unittest.TestCase):

    # Set up dummy dataframe to test on
    def setUp(self):
        self.df = dummy_df.copy()

    def test_filter_by_types(self):
        result = filter_by_dual_type(self.df, "Normal", "Steel")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "OmegaArmormon Burst Mode")

    def test_filter_by_types_reverse_matches(self):
        result = filter_by_dual_type(self.df, "Flying", "Normal")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "Pidgey")

    def test_filter_by_types_multiple_matches(self):
        result = filter_by_type(self.df, "Poison")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "Bulbasaur")

    def test_filter_by_type_no_matches(self):
        result = filter_by_type(self.df, "Electric")
        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
