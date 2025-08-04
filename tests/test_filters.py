import unittest
import pandas as pd
from core.filters import filter_by_status, filter_by_type, filter_by_dual_type

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
        "type_1": ["Grass", "Fire", "Water", "Normal", "Water", "Normal", "Normal"],
        "type_2": ["Poison", "N/A", "N/A", "Flying", "Ground", "Steel", "Steel"],
        "status": [
            "Normal",
            "Normal",
            "Normal",
            "Normal",
            "Normal",
            "Sub Legendary",
            "Legendary",
        ],
    }
)


class TestFilterByType(unittest.TestCase):

    def setUp(self):
        self.df = dummy_df.copy()

    def test_filter_by_primary_type_returns_match(self):
        result = filter_by_type(self.df, "Fire")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "Charmander")

    def test_filter_by_secondary_type_returns_match(self):
        result = filter_by_type(self.df, "Flying")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "Pidgey")

    def test_filter_by_type_returns_multiple_matches(self):
        result = filter_by_type(self.df, "Water")
        self.assertEqual(len(result), 2)

        names = set(result["name"])
        expected_names = {"Squirtle", "Gastrodon"}

        self.assertSetEqual(names, expected_names)

    def test_filter_by_nonexistent_type_returns_no_matches(self):
        result = filter_by_type(self.df, "ThisIsAFakeType")
        self.assertTrue(result.empty)


class TestFilterByDualTypes(unittest.TestCase):

    def setUp(self):
        self.df = dummy_df.copy()

    def test_filter_by_types_returns_multiple_matches(self):
        result = filter_by_dual_type(self.df, "Normal", "Steel")
        self.assertEqual(len(result), 2)

        names = set(result["name"])
        expected_names = {"OmegaArmormon Burst Mode", "OmegaArmormon Chaos Mode"}

        self.assertSetEqual(names, expected_names)

    def test_filter_by_types_in_reverse_returns_match(self):
        result = filter_by_dual_type(self.df, "Flying", "Normal")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "Pidgey")

    def test_filter_by_types_ensuring_symmetrical(self):
        result1 = filter_by_dual_type(self.df, "Normal", "Steel")
        result2 = filter_by_dual_type(self.df, "Steel", "Normal")
        self.assertSetEqual(set(result1["name"]), set(result2["name"]))

    def test_filter_singular_matching_type_returns_empty(self):
        single_dummy = pd.DataFrame(
            {"name": ["Fakeasaur"], "type_1": ["Grass"], "type_2": ["Poison"]}
        )
        result = filter_by_dual_type(single_dummy, "Grass", "Flying")
        self.assertTrue(result.empty)

    def test_filter_by_nonexistent_dual_types_returns_no_matches(self):
        result = filter_by_dual_type(self.df, "ThisIsA", "FakeType")
        self.assertTrue(result.empty)


class TestFilterByStatus(unittest.TestCase):

    def setUp(self):
        self.df = dummy_df.copy()

    def test_filter_by_status_legendary_returns_single_entry(self):
        result = filter_by_status(self.df, "Legendary")
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["name"], "OmegaArmormon Chaos Mode")

    def test_filter_by_status_normal_returns_multiple_matches(self):
        result = filter_by_status(self.df, "Normal")
        self.assertEqual(len(result), 5)

        names = set(result["name"])
        expected_names = {"Bulbasaur", "Charmander", "Squirtle", "Pidgey", "Gastrodon"}

        self.assertSetEqual(names, expected_names)

    def test_filter_by_fake_status_returns_no_matches(self):
        result = filter_by_status(self.df, "MadeUpStatus404")
        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
