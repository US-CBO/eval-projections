def calc_summary_stats(errors, component):
    """
    Calculate summary statistics of projection errors for a given budgetary
    component.

    For each projection year (1st through 11th) and component (outlay,
    revenue, deficit, and debt) the summary statistics calculated are:
        - average error
        - average absolute error
        - root mean squared error (RMSE)
        - two-thirds spread (central two-thirds of the error distribution)

    Parameters
    ----------
    errors : pandas.DataFrame
        DataFrame containing disaggregated projection errors

    component : str
        The component for which projection errors are analyzed
        ("outlay", "revenue", "deficit", "debt")

    Returns
    -------
    summary_stats : pandas.DataFrame
        DataFrame with summary statistics of projection errors for each
        budgetary component grouped by:
            - component
            - category
            - subcategory
            - projected_year_number

        The summary statistics include:
            - average_error: average projection error
            - average_absolute_error: average absolute projection error
            - RMSE: Root Mean Squared Error
            - two_thirds_spread: Central two-thirds of the error distribution
    """
    errors = errors.copy()

    group_cols = ["component", "category", "subcategory", "projected_year_number"]

    if component in ["deficit", "debt"]:
        error_col = "projection_error_pct_GDP"
    else:
        error_col = "projection_error_pct_actual"

    summary_stats = errors.groupby(group_cols, observed=True).agg(
        {
            error_col: [
                ("average_error", lambda error: error.mean()),
                ("average_absolute_error", lambda error: abs(error).mean()),
                ("RMSE", lambda error: ((error ** 2).mean()) ** 0.5),
                ("two_thirds_spread", lambda error: error.quantile(5/6) - error.quantile(1/6))
            ]
        }
    )

    # Reset index so index is not a Multilevel index based on group_cols after
    # the groupby(), above.
    summary_stats.reset_index(inplace=True)

    # Clean up column names
    stats_cols = [
        "average_error",
        "average_absolute_error",
        "RMSE",
        "two_thirds_spread"
    ]

    summary_stats.columns = group_cols + stats_cols

    return summary_stats
