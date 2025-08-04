import load_data as ld
import pandas as pd

df = ld.load_data()

print(df)


# Filter by type
def filter_by_type(df, type: str) -> pd.DataFrame:
    return df


# Filter by status (Legendary/Mythical)
def filter_by_status(df, status: str) -> pd.DataFrame:
    return df
