import pandas as pd


def load_data():
    """
    Load the Pokémon dataset.
    returns a DataFrame with the Pokémon data.
    """
    df = pd.read_csv("data/pokemon.csv")

    # Data cleaning
    df = df.dropna()  # Remove missing values
    return df


if __name__ == "__main__":
    print(load_data())
