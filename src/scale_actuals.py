import pandas as pd


def scale_actuals(actuals, GDP):
    """Calculate actual outlays as a share of GDP.

    Parameters
    ----------
    actuals : pandas.DataFrame
        DataFrame containing actual, historical outlay values.
    GDP : pandas.DataFrame
        DataFrame containing actual, historical GDP values.

    Returns
    -------
    pandas.DataFrame
        Merged DataFrame of the two input DataFramess, with an additional
        column containing actual_outlay_pct_GDP, and only containing data
        for fiscal_year 1993 onward.
    """
    outlays_and_GDP = pd.merge(
        actuals,
        GDP,
        how="left",
        on=["fiscal_year"]
    )

    # Filter out data before 1993
    outlays_and_GDP = outlays_and_GDP[outlays_and_GDP["fiscal_year"] >= 1993]

    # Calc outlays as a percent of GDP
    outlays_and_GDP.loc[:, "actual_outlay_pct_GDP"] = (
        (outlays_and_GDP["actual_outlay"] / outlays_and_GDP["GDP"]).mul(100)
    )

    # Filter out Fannie and Freddie data
    outlays_and_GDP = outlays_and_GDP.loc[
        outlays_and_GDP["outlay_subcategory"] != "Fannie Freddie"
    ]

    # Filter out Defense and Nondefense Outlays before 1998
    discretionary_cols = ["Defense Discretionary", "Nondefense Discretionary"]
    outlays_and_GDP = outlays_and_GDP.loc[
        ~(  # Note the negation
            (outlays_and_GDP["outlay_subcategory"].isin(discretionary_cols)) &
            (outlays_and_GDP["fiscal_year"] < 1998)
        )
    ]

    # Write out data
    output_cols = [
        "outlay_category",
        "outlay_subcategory",
        "fiscal_year",
        "actual_outlay",
        "GDP",
        "actual_outlay_pct_GDP"
    ]

    return outlays_and_GDP[output_cols]
