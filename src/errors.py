import pandas as pd


def merge_data(actuals, baselines, changes):
    """Merge three DataFrames related to projection errors together.

    Parameters
    ----------
    actuals : pandas.DataFrame
        Contains actual outlays by fiscal year, outlay category, and outlay
        subcategory. (Read in from input_data/actual_outlays.csv)
    baselines : pandas.DataFrame
        Contains baseline outlays projections (Read in from
        input_data/baseline_outlays.csv)
    changes : pandas.DataFrame
        Contains changes to baseline outlays projections (Read in from
        input_data/baseline_outlays_changes.csv)

    Returns
    -------
    merged_df : pandas.DataFrame
        Contains the merged and filtered data from the three input sources.
    """
    # Errors analyses are only performed on Analysis of President's Budget (APB)
    # baselines -- which are typically referred to as "Spring" baselines.
    APBs = baselines[baselines["APB_flag"] == True]

    # Merge APBs and actuals
    APBs_actuals = pd.merge(
        APBs,
        actuals,
        how = "left",
        left_on = ["outlay_category", "outlay_subcategory", "projected_fiscal_year"],
        right_on = ["outlay_category", "outlay_subcategory", "fiscal_year"]
    )

    APBs_actuals = APBs_actuals.drop(columns=["fiscal_year"])

    # Only want to take account for legislative changes (not economic or
    # technical changes) in calculation of projection errors.
    leg_changes = changes.loc[(changes["change_category"] == "Legislative"), :]

    # Rename to better column name
    leg_changes = leg_changes.rename(columns={
        "changes_projected_outlay" : "legislative_outlay_change"
        }
    )

    # Merge ABPs and leg_changes
    APBs_actuals_leg_changes = pd.merge(
        APBs_actuals,
        leg_changes,
        how = "right",
        on = ["outlay_category", "outlay_subcategory", "projected_fiscal_year"]
    )

    # Change date columns to datetime data types, so they can be compared
    # in the filtering operation, below
    for col in ["changes_baseline_date", "baseline_date"]:
        APBs_actuals_leg_changes[col] = pd.to_datetime(
            APBs_actuals_leg_changes[col],
            format="%Y-%m-%d"
        )

    # Only keep legislative changes that are AFTER the baseline date
    APBs_actuals_leg_changes = APBs_actuals_leg_changes[
        APBs_actuals_leg_changes["changes_baseline_date"] >
        APBs_actuals_leg_changes["baseline_date"]
    ]

    # Aggregate legislative outlay changes
    agg_cols = [
        "outlay_category",
        "outlay_subcategory",
        "projected_fiscal_year",
        "projected_year_number"
    ]

    APBs_actuals_leg_changes_aggregated = APBs_actuals_leg_changes.groupby(
        agg_cols)["legislative_outlay_change"].sum()

    # Merge APBs_actuals and aggregated legislative changes
    merged_df = pd.merge(
        APBs_actuals,
        APBs_actuals_leg_changes_aggregated,
        how = "inner",
        on = agg_cols
    )

    # Only keep fical years 2021 and earlier
    merged_df = merged_df[merged_df["projected_fiscal_year"] <= 2021]

    # Filter out Fannie and Freddie data from further calculations
    merged_df = merged_df.loc[merged_df["outlay_subcategory"] != "Fannie Freddie", :]

    return merged_df


def calc_errors(merged_data):
    """Calculate a variety of projection error statistics.

    Parameters
    ----------
    merged_data : pandas.DataFrame
        DataFrame created in merge_data(), which pulls together the
        actual_outlays, baseline_outlays, and baseline_outlays_changes
        data.

    Returns
    -------
    merged_data : pandas.DataFrame
        Same DataFrame as read in, but with additional columns of projection
        error statistics.
    """
    merged_data.loc[:, "adjusted_projection"] = (
        merged_data["baseline_projected_outlay"] +
        merged_data["legislative_outlay_change"]
    )

    merged_data.loc[:, "projection_error"] = (
        merged_data["adjusted_projection"] -
        merged_data["actual_outlay"]
    )

    merged_data.loc[:, "projection_error_pct_actual"] = (
        merged_data["projection_error"] /
        merged_data["actual_outlay"]
    ).mul(100)

    return merged_data


def calc_summary_stats(errors):
    """Calculate summary statistics of outlay projection errors.

    Parameters
    ----------
    errors : pandas.DataFrame
        DataFrame containing disaggregated projection errors.

    Returns
    -------
    summary_stats : pandas.DataFrame
        DataFrame with summary errors statistics:
            * average error,
            * average absolute error
            * root mean squared error (RMSE), and
            * two_thirds_spread (central two-thirds of the error distribution)
        grouped by outlay_category, outlay_subcategory, and projected_year_number
    """
    # Creates a copy of the DataFrame passed into the function,
    # so we aren't augmenting the external DataFrame.
    errors = errors.copy()

    # Then group by outlay subcategory and projected year number and
    # calculate summary stats
    group_cols = ["outlay_category", "outlay_subcategory", "projected_year_number"]
    summary_stats = errors.groupby(group_cols).aggregate({
        "projection_error_pct_actual" : [
            ("average_error", lambda error: error.mean()),
            ("average_absolute_error", lambda error: abs(error).mean()),
            ("RMSE", lambda error: ((error ** 2).mean()) ** 0.5),
            ("two_thirds_spread", lambda error: error.quantile(5/6) - error.quantile(1/6))
        ]
    }).reset_index()

    # Clean up column names
    summary_stats.columns = [
        "outlay_category",
        "outlay_subcategory",
        "projected_year_number",
        "average_error",
        "average_absolute_error",
        "RMSE",
        "two_thirds_spread"
    ]

    outlay_cats = ["Total", "Mandatory", "Discretionary", "Net Interest"]
    outlay_subcats = [
        "Total",
        "Total Mandatory",
        "Social Security",
        "Medicare",
        "Medicaid",
        "Fannie Freddie",
        "Other Mandatory",
        "Total Discretionary",
        "Defense Discretionary",
        "Nondefense Discretionary",
        "Net Interest"
    ]

    summary_stats["outlay_category"] = pd.Categorical(
        summary_stats["outlay_category"],
        categories = outlay_cats,
        ordered = True
    )

    summary_stats["outlay_subcategory"] = pd.Categorical(
        summary_stats["outlay_subcategory"],
        categories = outlay_subcats,
        ordered = True
    )

    summary_stats.sort_values(by=group_cols, inplace=True)

    return summary_stats
