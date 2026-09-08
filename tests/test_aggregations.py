import datetime

import pandas as pd
import pytest

from frontend.data import (
    aggregate_installations,
    cocktail_count,
    cumulate_installations,
    filter_dataframe,
    serving_aggregation,
    sum_volume,
    time_aggregation,
)
from frontend.models import CocktailSchema, InstallationSchema

# aggregations must stay clean under future pandas versions from dependabot
pytestmark = pytest.mark.filterwarnings("error::FutureWarning", "error::DeprecationWarning")

_FULL_RANGE = (datetime.date(2026, 8, 1), datetime.date(2026, 9, 1))
_ALL_LANGUAGES = ["en", "de"]
_ALL_MACHINES = ["M1", "M2", "M3"]
_ALL_RECIPES = ["Mojito", "Mai Tai", "Cuba Libre"]


def _filtered(df: pd.DataFrame) -> pd.DataFrame:
    return filter_dataframe(df, _ALL_LANGUAGES, _ALL_MACHINES, _ALL_RECIPES, False, _FULL_RANGE)


def test_filter_dataframe_passes_matching_rows(cocktails_df):
    assert len(_filtered(cocktails_df)) == 6


def test_filter_dataframe_restricts_by_criteria(cocktails_df):
    only_m1 = filter_dataframe(cocktails_df, _ALL_LANGUAGES, ["M1"], _ALL_RECIPES, False, _FULL_RANGE)
    assert set(only_m1[CocktailSchema.machine_name]) == {"M1"}
    out_of_range = filter_dataframe(
        cocktails_df,
        _ALL_LANGUAGES,
        _ALL_MACHINES,
        _ALL_RECIPES,
        False,
        (datetime.date(2020, 1, 1), datetime.date(2020, 1, 2)),
    )
    assert out_of_range.empty


@pytest.mark.parametrize("country_split", [True, False])
def test_sum_volume_counts_all_cocktails(cocktails_df, country_split):
    volumes = sum_volume(_filtered(cocktails_df), country_split)
    assert volumes[CocktailSchema.cocktail_count].sum() == 6
    # volume column is converted to litre
    assert volumes[CocktailSchema.cocktail_volume].sum() == pytest.approx(1.5)


def test_cocktail_count_limits_and_ranks_recipes(cocktails_df):
    counted = cocktail_count(_filtered(cocktails_df), 2, True)
    # Mojito (3x) ranks before Mai Tai (2x), Cuba Libre (1x) is cut by the limit
    assert counted[CocktailSchema.cocktail_name].iloc[0] == "Mojito"
    assert "Cuba Libre" not in set(counted[CocktailSchema.cocktail_name])


def test_cocktail_count_without_split(cocktails_df):
    counted = cocktail_count(_filtered(cocktails_df), 2, False)
    assert counted[CocktailSchema.cocktail_count].to_list() == [3, 2]


@pytest.mark.parametrize("machine_split", [True, False])
def test_serving_aggregation_rounds_to_25(cocktails_df, machine_split):
    servings = serving_aggregation(_filtered(cocktails_df), machine_split, 1)
    assert set(servings[CocktailSchema.volume]) <= {200, 225, 250, 275, 300}


def test_serving_aggregation_filters_minimum_count(cocktails_df):
    servings = serving_aggregation(_filtered(cocktails_df), False, 2)
    counts = servings.groupby(CocktailSchema.volume)[CocktailSchema.cocktail_count].sum()
    assert (counts >= 2).all()


@pytest.mark.parametrize(("hourly", "machine_split"), [(True, True), (False, False)])
def test_time_aggregation_keeps_total(cocktails_df, hourly, machine_split):
    timed = time_aggregation(_filtered(cocktails_df), hourly, machine_split)
    assert timed[CocktailSchema.cocktail_count].sum() == 6


def test_aggregate_installations_counts_by_os(installations_df):
    aggregated = aggregate_installations(installations_df)
    assert aggregated[InstallationSchema.INSTALLATIONS_COUNT].sum() == 4


def test_cumulate_installations_reaches_total(installations_df):
    cumulated = cumulate_installations(installations_df, False)
    assert cumulated[InstallationSchema.INSTALLATIONS_COUNT].max() == 4


def test_cumulate_installations_with_os_split(installations_df):
    cumulated = cumulate_installations(installations_df, True)
    assert not cumulated.empty
    assert set(cumulated[InstallationSchema.OS]) == set(installations_df[InstallationSchema.OS])
