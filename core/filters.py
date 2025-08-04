import pandas as pd


# Filter by type
def filter_by_type(df: pd.DataFrame, type: str) -> pd.DataFrame:
    return df[(df["type_1"] == type) | (df["type_2"] == type)]


# Filter to matching two types
# Should this be consolidated into the previous function?
def filter_by_dual_type(df: pd.DataFrame,
                        type_1: str,
                        type_2: str) -> pd.DataFrame:
    return df[
        (
            (df["type_1"] == type_1) & (df["type_2"] == type_2)
            | (df["type_1"] == type_2) & (df["type_2"] == type_1)
        )
    ]


# Filter by status (Legendary/Mythical)
def filter_by_status(df, status: str) -> pd.DataFrame:
    return df[(df["status"] == status)]
