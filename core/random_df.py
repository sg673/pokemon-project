import pandas as pd


def generate_random_rows(
    df: pd.DataFrame, excluded_mon: int = -1, num_of_mons: int = 1
) -> pd.DataFrame:
    """
    This function takes a DataFrame, a Pokedex number, and a number of Pokemon.
    It excludes that Pokedex number from the DataFrame then returns a selection
    of Pokemon equal in number to num_of_mons

    Parameters:
        - df: A DataFrame
        - excluded_mon: An integer, should correspond to a Pokedex number
        - num_of_mons: Integer denoting the number of rows you want returned

    Returns: A DataFrame
    """
    # Exclude the row with pokedex_number == exclude_mon
    filtered_df = df[df["pokedex_number"] != excluded_mon]

    # Sample and return the required number of rows
    return filtered_df.sample(n=num_of_mons)