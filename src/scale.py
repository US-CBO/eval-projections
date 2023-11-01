import pandas as pd


def scale_actuals(actuals, GDP):
    """Calculate the share of actual outlays, revenues, deficits, and debt
     as a percentage of GDP.

    Parameters
    ----------
    actuals : pandas.DataFrame
        DataFrame containing actual, historical revenue, outlay, deficit,
        and debt values
    GDP : pandas.DataFrame
        DataFrame containing actual, historical GDP values

    Returns
    -------
    pandas.DataFrame
        A merged DataFrame of the two input DataFrames, with an additional
        column "actuals_pct_GDP" representing the percentage of actuals
        relative to GDP

    Notes
    -----
    - The function merges the actuals and GDP data based on the fiscal year.
    - It calculates the share of actuals as (actual_value / GDP) * 100.
    - Data for "Fannie Freddie" oultays are filtered out.
    """

    actuals_GDP = pd.merge(actuals, GDP, how="left", on=["fiscal_year"])

    actuals_GDP["actuals_pct_GDP"] = (
        actuals_GDP["actual_value"] / actuals_GDP["GDP"] * 100
    )

    # Filter out Fannie and Freddie data
    actuals_GDP = actuals_GDP.loc[actuals_GDP["subcategory"] != "Fannie Freddie"]

    output_cols = [
        "component",
        "category",
        "subcategory",
        "fiscal_year",
        "actual_value",
        "GDP",
        "actuals_pct_GDP",
    ]

    return actuals_GDP[output_cols]
