def calc_errors(merged_data, component):
    """
    Calculate projection error statistics for a given budgetary component.

    This function calculates projection error statistics based on the
    provided merged data, which includes baseline projections, legislative
    changes, and actual values.

    The calculations depend on the budgetary component being analyzed
    ("outlay", "revenue", "deficit", or "debt").

    The projection error statistics calculated are:
        - projection error
        - projection error as a percent of actual
        - projection error as a percent of GDP

    Parameters
    ----------
    merged_data : pandas.DataFrame
        DataFrame created by merging various input DataFrames using
        `merge.merge_data()`

    component : str
        The fiscal component for which projection errors are calculated
        ("outlay", "revenue", "deficit", or "debt")

    Returns
    -------
    pandas.DataFrame
        The input DataFrame with additional columns containing projection
        error statistics
    """
    merged_data = merged_data.copy()

    merged_data["adjusted_projection"] = (
        merged_data["value"] + merged_data[f"legislative_{component}_change"]
    )

    merged_data["projection_error"] = (
        merged_data["adjusted_projection"] - merged_data["actual_value"]
    )

    if component == "deficit":
        merged_data["projection_error"] *= -1

    if component in ["deficit", "debt"]:
        merged_data["projection_error_pct_GDP"] = (
            merged_data["projection_error"] / merged_data["GDP"] * 100
        )

    else:
        merged_data["projection_error_pct_actual"] = (
            merged_data["projection_error"] / merged_data["actual_value"] * 100
        )

    return merged_data
