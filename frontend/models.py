
from dataclasses import dataclass


@dataclass
class DataFrameStats():
    countries: int
    machines: int
    recipes: int
    cocktails: int
    volume: int
    first_data: str
    last_data: str


class CocktailSchema():
    machine_name: str = "Machine Name"
    cocktail_name: str = "Cocktail Name"
    cocktail_count: str = "Number of Cocktails"
    cocktail_volume: str = "Cocktail Volume in Litre"
    volume: str = "Volume"
    language: str = "Language"
    receivedate: str = "Received Date"


class ReceivedData():
    COUNTRYCODE = "countrycode"
    MACHINENAME = "machinename"
    COCKTAILNAME = "cocktailname"
    VOLUME = "volume"
    RECEIVEDATE = "receivedate"
