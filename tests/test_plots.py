"""Every plot builder must still construct after dependency bumps (plotly, streamlit)."""

import datetime

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
from frontend.plots import (
    _generate_excluded_days,
    _get_machine_color_map,
    generate_installation_time_chart,
    generate_installation_treemap,
    generate_recipes_treemap,
    generate_serving_size_bars,
    generate_time_plot,
    generate_volume_treemap,
)
from frontend.views.machine import display_machine_types

pytestmark = pytest.mark.filterwarnings("error::FutureWarning", "error::DeprecationWarning")


@pytest.mark.parametrize("split", [True, False])
def test_all_plot_builders_construct(cocktails_df, installations_df, split):
    filtered = filter_dataframe(
        cocktails_df,
        ["en", "de"],
        ["M1", "M2", "M3"],
        ["Mojito", "Mai Tai", "Cuba Libre"],
        False,
        (datetime.date(2026, 8, 1), datetime.date(2026, 9, 1)),
    )
    generate_volume_treemap(sum_volume(filtered, split), split)
    generate_recipes_treemap(cocktail_count(filtered, 2, split), split)
    generate_time_plot(time_aggregation(filtered, split, split), split)
    generate_serving_size_bars(serving_aggregation(filtered, split, 1), split)
    generate_installation_time_chart(cumulate_installations(installations_df, split), split)
    generate_installation_treemap(aggregate_installations(installations_df))


def test_machine_color_map_covers_all_machines(cocktails_df):
    colors = _get_machine_color_map(cocktails_df)
    assert set(colors) == {"M1", "M2", "M3"}


def test_excluded_days_leaves_used_days(cocktails_df):
    from frontend.models import CocktailSchema

    excluded = _generate_excluded_days(cocktails_df[CocktailSchema.receivedate])
    assert "2026-08-02" in excluded
    assert "2026-08-01" not in excluded


def test_machine_showcase_renders_with_valid_assets():
    # exercises the machine data list and all picture paths
    display_machine_types()
