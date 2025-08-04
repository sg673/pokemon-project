import pandas as pd


def generate_random_rows(
    df: pd.DataFrame, excluded_mon: int = -1, num_of_mons: int = 1
) -> pd.DataFrame:
    # Exclude the row with pokedex_number == exclude_mon
    filtered_df = df[df["pokedex_number"] != excluded_mon]

    # Sample and return the required number of rows
    return filtered_df.sample(n=num_of_mons)