from deta import Deta
import pandas as pd


def generate_df(cocktail_deta: Deta.Base):
    cocktails = cocktail_deta.fetch().items
    df = pd.DataFrame(cocktails)
    df.drop("key", axis=1, inplace=True)
    return df


def sum_volume(df: pd.DataFrame) -> pd.DataFrame:
    volumes = df.groupby(["countrycode", "machinename"])["volume"] \
        .agg(["sum", "count"]) \
        .rename(columns={"sum": "Cocktail Volume in ml", "count": "Number of Cocktails"}) \
        .reset_index()
    return volumes
