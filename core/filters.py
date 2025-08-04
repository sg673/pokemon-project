import pandas as pd


# Filter by type
def filter_by_type(df: pd.DataFrame, type: str) -> pd.DataFrame:
    """
    This function takes a dataframe and a type, filtering the dataframe to
    include pokemon that have that type.

    Parameters:
        - df: A DataFrame
        - type: A string, should match one of the potential Pokemon types,
        in English.

    Returns: A DataFrame
    """
    return df[(df["type_1"] == type) | (df["type_2"] == type)]


# Filter to matching two types
# Should this be consolidated into the previous function?
def filter_by_dual_type(df: pd.DataFrame, type_1: str, type_2: str) -> pd.DataFrame:
    """
    This function takes a dataframe and two types, filtering the dataframe to
    include pokemon matching both types.

    Parameters:
        - df: A DataFrame
        - type_1: A string, should match one of the potential Pokemon types,
        in English.
        - type_2: A string, should match one of the potential Pokemon types,
        in English.

    Returns: A DataFrame
    """
    return df[
        (
            (df["type_1"] == type_1) & (df["type_2"] == type_2)
            | (df["type_1"] == type_2) & (df["type_2"] == type_1)
        )
    ]


# Filter by status (Legendary/Mythical)
def filter_by_status(df: pd.DataFrame, status: str) -> pd.DataFrame:
    """
    This function takes a dataframe and a status (of a pokemon) and filters
    the dataframe to only include pokemon of that status.
    Filters by status:

    Parameters:
        - df: A DataFrame
        - status: A string referring to the status of a Pokemon. Valid options
        are "Normal", "Sub Legendary", "Legendary".

    Returns: A DataFrame
    """
    return df[(df["status"] == status)]
