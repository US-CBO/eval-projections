import pandas as pd

agg_cols = [
    "component",
    "category",
    "subcategory",
    "projected_fiscal_year",
    "projected_year_number",
]

leg_labels = {
    "revenue": "legislative_revenue_change",
    "outlay": "legislative_outlay_change",
    "deficit": "legislative_deficit_change",
    "debt": "legislative_deficit_change",
}


def merge_data(dfs, component):
    """
    Merge and filter data from multiple DataFrames related to
    projection errors.

    This function combines actuals, baseline projections, changes, and GDP
    data to create a merged and filtered DataFrame for a given budgetary
    component (outlay, revenue, deficit, or debt).

    Parameters
    ----------
    dfs : tuple of pandas.DataFrame
        A tuple containing the following DataFrames:
            - actuals: Contains actual outlays, revenues, deficits, and
                debt by fiscal year, category, and subcategory
            - baselines: Contains baseline outlays, revenues, deficits,
                and debt projections
            - changes: Contains changes to baseline outlays, revenues,
                deficits, and debt projections
            - GDP: Contains GDP data to merge with the baseline and
                actuals

    component : str
        The component for which data is being merged
        ("outlay", "revenue", "deficit", "debt")

    Returns
    -------
    sorted_data : pandas.DataFrame
        Contains the merged and filtered data for the specified
        budgetary component

    Raises
    ------
    AssertionError
        If the given budgetary component is not in
        ["outlay", "revenue", "deficit", "debt"]

    Notes
    -----
    This function performs the following steps:
    1. Select relevant baseline data for the specified component.
    2. Merge actuals with the selected baselines.
    3. Merge GDP data with the merged actuals and baselines.
    4. Retrieve legislative changes related to the specified component.
    5. Merge legislative changes with the merged data.
    6. Aggregate legislative changes and calculate cumulative effects.
    7. Merge aggregated legislative changes with the merged data.
    8. Filter the merged data based on specific criteria.
    9. Sort the filtered data to maintain hierarchy and ordering.

    The resulting DataFrame contains the merged and sorted data for
    further analysis.
    """
    assert component in ["outlay", "revenue", "deficit", "debt"]

    # Unpack the dfs parameter
    actuals, baselines, changes, GDP = dfs

    relevant_baselines = get_relevant_baselines(baselines, component)
    bl_act = merge_baselines_actuals(relevant_baselines, actuals)
    bl_act_GDP = merge_on_GDP(bl_act, GDP)
    leg_changes = get_leg_changes(changes, component)
    bl_act_leg = merge_on_leg_changes(bl_act_GDP, leg_changes)
    bl_act_leg_agg = aggregate_leg_changes(bl_act_leg, component)
    merged_df = merge_on_agg_leg_changes(bl_act_GDP, bl_act_leg_agg)
    filtered_data = filter_merged_data(merged_df)
    sorted_data = sort_data(filtered_data, component)

    return sorted_data


def get_relevant_baselines(baselines, component):
    """
    Get the relevant subset of baseline projection data for merging.

    This function filters the baseline projection data based on the
    given budgetary component and the source of the baseline
    projections (Winter or Spring) that should be used for the given
    component.

    Parameters
    ----------
    baselines : pandas.DataFrame
        DataFrame containing baseline outlay, revenue, deficit, and debt
        projections

    component : str
        The budgetary component for which data is being filtered
        ("outlay", "revenue", "deficit", "debt")

    Returns
    -------
    pandas.DataFrame
        A subset of the baselines DataFrame containing the relevant
        baseline projection data

    Notes
    -----
    - For revenue error analysis, Winter baselines are used.
    - For other error analyses (outlay, deficit, debt), Spring baselines are used.
    - The relevant subset of baselines is determined based on the
        component argument passed into the function and the `Winter_flag`
        or `Spring_flag` values indicating the source of the baseline
        projections.
    """
    which_baseline = {
        "revenue": "Winter",
        "outlay": "Spring",
        "deficit": "Spring",
        "debt": "Spring",
    }

    component_cond = baselines["component"] == component
    baseline_cond = baselines[f"{which_baseline[component]}_flag"] == True

    relevant_baselines = baselines.loc[component_cond & baseline_cond, :]

    return relevant_baselines


def merge_baselines_actuals(relevant_baselines, actuals):
    """
    Merge relevant baselines with actual data based on specific criteria.

    Parameters
    ----------
    relevant_baselines : DataFrame
        A DataFrame containing relevant baseline data

    actuals : DataFrame
        A DataFrame containing actual data

    Returns
    -------
    DataFrame
        A DataFrame resulting from the merge operation, containing relevant
        baseline data and matched actual data

    Notes
    -----
    This function merges the `relevant_baselines` DataFrame with the
    `actuals` DataFrame using a left join operation.

    The merge is performed based on the following columns:
        - `component`
        - `category`
        - `subcategory`
        - `projected_fiscal_year`

    The `fiscal_year` column from `actuals` is matched with
    `projected_fiscal_year` from `relevant_baselines`.

    After the merge, the `fiscal_year` column from `actuals` is dropped to
    eliminate redundancy in the result.
    """
    bl_act = pd.merge(
        relevant_baselines,
        actuals,
        how="inner",
        left_on=["component", "category", "subcategory", "projected_fiscal_year"],
        right_on=["component", "category", "subcategory", "fiscal_year"],
    )

    bl_act = bl_act.drop(columns=["fiscal_year"])

    return bl_act


def merge_on_GDP(bl_act, GDP):
    """
    Merge data containing relevant baselines and actuals with GDP data
    based on fiscal year.

    Parameters
    ----------
    bl_act : DataFrame
        A DataFrame containing relevant baseline and actual data

    GDP : DataFrame
        A DataFrame containing GDP (Gross Domestic Product) data

    Returns
    -------
    DataFrame
        A DataFrame resulting from the merge operation, containing relevant
        baseline and actual data matched with GDP data.

    Notes
    -----
    This function merges the `bl_act` DataFrame (containing relevant
    baseline and actual data) with the `GDP` DataFrame using a left join
    operation.

    The merge is performed based on the `projected_fiscal_year` column from
    `bl_act` and the `fiscal_year` column from `GDP`.

    After the merge, the `fiscal_year` column from `GDP` is dropped to
    eliminate redundancy in the result.
    """
    bl_act_GDP = pd.merge(
        bl_act,
        GDP,
        how="left",
        left_on=["projected_fiscal_year"],
        right_on=["fiscal_year"],
    )

    bl_act_GDP = bl_act_GDP.drop(columns=["fiscal_year"])

    return bl_act_GDP


def get_leg_changes(changes, component):
    """
    Get legislative changes from a DataFrame of changes based on the
    given budgetary component.

    Parameters
    ----------
    changes : DataFrame
        A DataFrame containing various types of changes, including
        legislative changes

    component : str
        A string specifying the component for which legislative changes
        should be extracted

    Returns
    -------
    DataFrame
        A DataFrame containing only legislative changes for the given
        component

    Notes
    -----
    This function takes a DataFrame `changes` that includes different types
    of changes, such as legislative, economic, or technical changes. It
    extracts and returns a DataFrame containing only legislative changes
    based on the given `component` parameter.

    If `component` is "debt", the function filters legislative changes with
    `component` set to "deficit".

    If `component` is any other string, it filters legislative changes for
    that specific `component` and returns them as is.

    Finally, the `value` column is renamed to the appropriate label defined
    in `leg_labels`.
    """
    changes = changes.copy()

    if component == "debt":
        filtered_changes = changes.loc[changes["component"] == "deficit", :].copy()
        filtered_changes.loc[:, "component"] = "debt"
    else:
        filtered_changes = changes.loc[changes["component"] == component, :]

    # Only want to take account for legislative changes
    # (not economic or technical changes) in calculation of projection errors.
    leg_changes = filtered_changes.loc[
        filtered_changes["change_category"] == "Legislative", :
    ]

    # Rename to better column name
    leg_changes = leg_changes.rename(columns={"value": leg_labels[component]})

    return leg_changes


def merge_on_leg_changes(baselines_actuals, leg_changes):
    """
    Merge baselines and actuals data with legislative changes based on
    specific criteria.

    Parameters
    ----------
    baselines_actuals : DataFrame
        A DataFrame containing relevant baseline and actual data

    leg_changes : DataFrame
        A DataFrame containing legislative changes data

    Returns
    -------
    DataFrame
        A DataFrame resulting from the merge operation, containing relevant
        baseline and actual data matched with legislative changes data

    Notes
    -----
    This function merges the `baselines_actuals` DataFrame (containing
    relevant baseline and actual data) with the `leg_changes` DataFrame
    (containing legislative changes) using a right join operation.

    The merge is performed based on the following columns:
        - `component`
        - `category`
        - `subcategory`
        - `projected_fiscal_year`

    After the merge, date columns `changes_baseline_date` and
    `baseline_date` are converted to datetime data types for comparison
    in the filtering operation. The function keeps only legislative changes
    that occurred AFTER the baseline date.
    """
    merged = pd.merge(
        baselines_actuals,
        leg_changes,
        how="right",
        on=["component", "category", "subcategory", "projected_fiscal_year"],
    )

    # Change date columns to datetime data types, so they can be compared
    # in the filtering operation, below
    for col in ["changes_baseline_date", "baseline_date"]:
        merged[col] = pd.to_datetime(merged[col], format="%Y-%m-%d")

    # Only keep legislative changes that are AFTER the baseline date
    cond = merged["changes_baseline_date"] > merged["baseline_date"]
    merged = merged.loc[cond, :]

    return merged


def aggregate_leg_changes(bl_act_leg, component):
    """
    Aggregate legislative changes for a specific component from a DataFrame.

    Parameters
    ----------
    bl_act_leg : DataFrame
        A DataFrame containing relevant baseline, actual, and legislative
        changes data

    component : str
        A string specifying the component for which legislative changes
        should be aggregated

    Returns
    -------
    DataFrame
        A DataFrame containing aggregated legislative changes for the
        given component

    Notes
    -----
    This function aggregates legislative changes from the `bl_act_leg`
    DataFrame, which includes relevant baseline, actual, and legislative
    changes data. The aggregation is performed based on the given
    `component`.

    If `component` is "debt", the function calculates the cumulative
    legislative deficit changes over the entire projection period and
    creates a column `legislative_debt_change` representing the debt change effects.

    For CBO's revenue, outlay, and deficit projections, the effects of
    legislation and the value of those effects are applied to individual
    projection years. For debt, by contrast, the effects of subsequent
    legislation are cumulative across all relevant projection years.

    For example, for the 6th projection year, the effects of legisation on
    debt projections are the cumulaitve deficit effects in the 1st, 2nd,
    3rd, 4th, 5th, and 6th projection years.

    See Appendix B of An Evaluation of CBO's Past Deficit and Debt
    Projections for a more detailed example:
    https://www.cbo.gov/publication/55234

    Additionally, it adjusts the debt values by multiplying them by -1 to
    accurately account for the direction of debt changes.
    """
    bl_act_leg_agg = (
        bl_act_leg.groupby(agg_cols)[leg_labels[component]].sum().reset_index()
    )

    if component == "debt":
        bl_act_leg_agg["baseline_year"] = (
            bl_act_leg_agg["projected_fiscal_year"]
            - bl_act_leg_agg["projected_year_number"]
            + 1
        ).astype("int")

        bl_act_leg_agg[leg_labels[component]] *= -1

        def calc_cum_deficit_effects(row):
            cond_1 = bl_act_leg_agg["baseline_year"] == row["baseline_year"]
            cond_2 = (
                bl_act_leg_agg["projected_year_number"] <= row["projected_year_number"]
            )

            return bl_act_leg_agg.loc[cond_1 & cond_2, leg_labels[component]].sum()

        bl_act_leg_agg["legislative_debt_change"] = bl_act_leg_agg.apply(
            calc_cum_deficit_effects, axis=1
        )

        bl_act_leg_agg.drop(columns=["baseline_year"], inplace=True)

    return bl_act_leg_agg


def merge_on_agg_leg_changes(bl_act, agg_leg_changes):
    """
    Merge relevant baseline and actual data with aggregated legislative
    changes data.

    Parameters
    ----------
    bl_act : DataFrame
        A DataFrame containing relevant baseline and actual data

    agg_leg_changes : DataFrame
        A DataFrame containing aggregated legislative changes data

    Returns
    -------
    DataFrame
        A DataFrame resulting from the merge operation, containing relevant
        baseline, actual data, and aggregated legislative changes data

    Notes
    -----
    This function merges the `bl_act` DataFrame (containing relevant
    baseline and actual data) with the `agg_leg_changes` DataFrame
    (containing aggregated legislative changes data) using an inner join
    operation. The merge is performed based on the given `agg_cols`.
    """
    merged_df = pd.merge(bl_act, agg_leg_changes, how="inner", on=agg_cols)

    return merged_df


def filter_merged_data(merged_df):
    """
    Filter merged data based on specified conditions.

    Parameters
    ----------
    merged_df : DataFrame
        A DataFrame containing merged data, typically the result of
        previous data operations

    Returns
    -------
    DataFrame
        A DataFrame resulting from filtering the input data based on
        specified conditions

    Notes
    -----
    This function filters the input DataFrame 'merged_df' to include only
    rows that meet specific conditions. The conditions applied are:
    1. Rows where `subcategory` is not equal to "Fannie Freddie."
    2. Rows where `projected_year_number` is not equal to 0.
    """
    cond_1 = merged_df["subcategory"] != "Fannie Freddie"
    cond_2 = merged_df["projected_year_number"] != 0

    filtered_df = merged_df.loc[cond_1 & cond_2, :]

    return filtered_df


def sort_data(merged_data, component):
    """
    Sort merged data based on specified sorting criteria.

    Parameters
    ----------
    merged_data : DataFrame
        A DataFrame containing merged data, typically the result of
        previous data operations

    component : str
        A string specifying the component for which data should be sorted

    Returns
    -------
    DataFrame
        A DataFrame resulting from sorting the input data based on
        specified criteria

    Notes
    -----
    This function sorts the input DataFrame `merged_data` based on specific
    sorting criteria determined by the `component` parameter.

    Sorting Criteria:
    Rows are first sorted by the following columns in ascending order:
        - `component`
        - `category`
        - `subcategory`
        - `projected_year_number`

    Additionally, the `category` and `subcategory` columns are sorted based
    on predefined orderings specific to the `component` parameter.
    """
    merged_data = merged_data.copy()

    sort_cols = ["component", "category", "subcategory", "projected_year_number"]

    cats = {
        "revenue": [
            "Total",
            "Individual Income Taxes",
            "Payroll Taxes",
            "Corporate Income Taxes",
            "Customs Duties",
            "Excise Taxes",
            "Estate and Gift Taxes",
            "Miscellaneous Receipts",
        ],
        "outlay": ["Total", "Mandatory", "Discretionary", "Net Interest"],
        "deficit": ["Total"],
        "debt": ["Total"],
    }

    subcats = {
        "revenue": [
            "Total",
            "Individual Income Taxes",
            "Payroll Taxes",
            "Corporate Income Taxes",
            "Customs Duties",
            "Excise Taxes",
            "Estate and Gift Taxes",
            "Miscellaneous Receipts",
        ],
        "outlay": [
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
            "Net Interest",
        ],
        "deficit": ["Total"],
        "debt": ["Total"],
    }

    merged_data["category"] = pd.Categorical(
        merged_data["category"], categories=cats[component], ordered=True
    )

    merged_data["subcategory"] = pd.Categorical(
        merged_data["subcategory"], categories=subcats[component], ordered=True
    )

    merged_data.sort_values(by=sort_cols, inplace=True)

    return merged_data
