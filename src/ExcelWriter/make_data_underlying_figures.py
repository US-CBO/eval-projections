import os
import numpy as np
import pandas as pd
from functools import reduce


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
INPUT_PATH = os.path.abspath(f"{CURRENT_PATH}/../../input_data")
OUTPUT_PATH = os.path.abspath(f"{CURRENT_PATH}/../../output_data")

metric_names = {
    'average_error': 'Average Error',
    'average_absolute_error': 'Average Absolute Error',
    'RMSE': 'Root Mean Square Error',
    'two_thirds_spread': 'Two-Thirds Spread of Errors'
}

metric_descriptors = {
    'Average Error': 'Centeredness',
    'Average Absolute Error': 'Accuracy',
    'Root Mean Square Error': 'Accuracy',
    'Two-Thirds Spread of Errors': 'Dispersion'
}

# Extract data for the 2nd, 6th, and 11th projection years
projection_years = [2, 6, 11]


def make_all_data(worksheets):
    """Create all the data for the underlying figures and add them to the worksheets dictionary.

    Parameters
    ----------
    worksheets : dict
        A dictionary of worksheet names and their settings. (Created in `worksheets.py`)

    Returns
    -------
    dict
        Same worksheets dictionary with the 'data' key added to each worksheet.
    """
    worksheets['Figure 1']['data'] = make_quality_data('deficit', projection_years)
    worksheets['Figure 2']['data'] = make_projection_errors_data('deficit', projection_years)
    worksheets['Figure 3']['data'] = make_infographic_2_data(projection_years)
    worksheets['Figure 4']['data'] = make_infographic_3_data(projection_years, start_year=1993)
    worksheets['Figure 5']['data'] = make_quality_data('debt', projection_years)
    worksheets['Figure 6']['data'] = make_projection_errors_data('debt', projection_years)
    worksheets['Figure 8']['data'] = make_leg_changes_data('deficit', projection_years)
    worksheets['Figure 9']['data'] = make_leg_changes_data('debt', projection_years)
    worksheets['Figure 10']['data'] = make_figure_6_data(projection_years=[2], start_year=2020)
    worksheets['Figure B-1']['data'] = make_infographic_b1_data(projection_years)

    return worksheets


def make_quality_data(component, projection_years):
    """Make the data for the quality metrics for a given component and projection years.

    Parameters
    ----------
    component : str
        Either 'deficit' or 'debt'.
    projection_years : list
        Which projection years to extract from the errors data.

    Returns
    -------
    df : pd.DataFrame
    """
    assert component in ['deficit', 'debt'], "Invalid component name."

    df = pd.read_csv(f"{OUTPUT_PATH}/{component}_projection_errors_summary_stats.csv")

    # Filter and select the data
    keep_cols = list(metric_names.keys()) + ['projected_year_number']
    df = df.loc[df['projected_year_number'].isin(projection_years), keep_cols]
    df = df.rename(columns=metric_names)

    # Transpose the data
    df = df.set_index('projected_year_number')
    df = df.T.reset_index(names='Metric')

    # Add the Description column and move it to the front
    df['Description'] = df['Metric'].map(metric_descriptors)
    cols = df.columns.tolist()
    df = df[[cols[-1]] + cols[:-1]]

    # Clean up the index/column names
    df.index.rename(None, inplace=True)
    df.rename_axis(None, axis="columns", inplace=True)
    rename_dict = {c : f"Year {str(c)}" for c in df.columns if type(c) == int}
    df.rename(columns=rename_dict, inplace=True)
    df.rename(columns={'Year 2': 'Budget Year'}, inplace=True)

    return df


def make_projection_errors_data(
        component,
        projection_years,
        category='Total',
        subcategory='Total',
        start_year=1984,
        leg_changes=False,
        calc_averages=True,
        apply_rounding=True
    ):
    """Make the data for the projection errors for a given component and projection years.

    Parameters
    ----------
    component : str
        Either 'deficit', 'debt', 'outlay', or 'revenue'.
    projection_years : list
        Which years to include in the data.
    category : str, optional
        Major category of the component, by default 'Total'
    subcategory : str, optional
        Subcategory of the category, by default 'Total'
    start_year : int, optional
        Start of projected_fiscal_year to extract from the errors data, by default 1984
    leg_changes : bool, optional
        Whether to extract errors associated with legislative changes, by default False
    calc_averages : bool, optional
        Whether to calculate average errors over period of data extracted, by default True
    apply_rounding : bool, optional
        Whether to apply rounding; don't want to do this when values will have
        additional operations on them, by default True

    Returns
    -------
    pd.DataFrame
    """
    assert component in ['deficit', 'debt', 'outlay', 'revenue'], "Invalid component name."

    df = pd.read_csv(f"{OUTPUT_PATH}/{component}_projection_errors.csv")

    # Filter and select the data
    keep_cols = ['projected_fiscal_year', 'projected_year_number']
    if leg_changes:
        keep_cols += ['leg_change_pct_GDP']
    else:
        keep_cols += ['projection_error_pct_GDP']

    filter_conditions = (
        (df['projected_year_number'].isin(projection_years)) &
        (df['category'] == category) &
        (df['subcategory'] == subcategory) &
        (df['Spring_flag'] == True) &
        (df['projected_fiscal_year'] >= start_year)
    )
    df = df.loc[filter_conditions, keep_cols]

    # Pivot the data
    if leg_changes:
        values = 'leg_change_pct_GDP'
    else:
        values = 'projection_error_pct_GDP'

    df = df.pivot(
        index='projected_fiscal_year',
        columns='projected_year_number',
        values=values
    )

    # Calculate the average error for each projection year
    for c in df.columns:
        df.rename(columns={c: f"Year {str(c)}"}, inplace=True)
        if calc_averages:
            col_name = f"Average {str(c)}th-Year Error"
            df[col_name] = df[f"Year {str(c)}"].mean()
            df[col_name] = df[col_name].where(df[f"Year {str(c)}"].notna(), other=np.nan)

        # Clean up column names
        df.rename(columns={'Average 2th-Year Error': 'Average Budget Year Error'}, inplace=True)
        df.rename(columns={'Year 2': 'Budget Year'}, inplace=True)

    # Clean up indexs
    df = df.reset_index(names='Year')
    df = df.rename_axis(None, axis="columns")

    # Rounding
    if apply_rounding:
        df = df.round(1)
        df['Year'] = df['Year'].round(0)

    return df


def make_infographic_2_data(projection_years):
    """Make the data for Infographic 2.

    Makes calls to make_projection_errors_data.

    Parameters
    ----------
    projection_years : list
        Which projection years to extract from the errors data.

    Returns
    -------
    pd.DataFrame
    """
    components = ['deficit', 'outlay', 'revenue']

    dfs = {}
    for component in components:
        dfs[component] = make_projection_errors_data(component, projection_years)
        # Remove the 'Average' columns
        dfs[component] = dfs[component].loc[:, [c for c in dfs[component].columns if 'Average' not in c]]
        # Rename the columns
        dfs[component].columns = ["Year"] + [f"{c} {component.title()} Error" for c in dfs[component].columns[1:]]

        if component == 'revenue':
            for col in dfs[component].columns[1:]:
                dfs[component][col] = dfs[component][col] * -1

    # Merge the DataFrames on Year
    df = reduce(lambda left, right: pd.merge(left, right, on='Year'), dfs.values())

    # Rearrange the column order
    cols = ["Year"]
    for years in ["Budget Year", "Year 6", "Year 11"]:
        for component in components:
            cols.append(f"{years} {component.title()} Error")

    return df[cols]


def make_infographic_3_data(projection_years, start_year=1993):
    """Make the data for Infographic 3.

    Makes calls to make_projection_errors_data.

    Parameters
    ----------
    projection_years : list
        Which projection years to extract from the errors data.
    start_year : int, optional
        Start of projected_fiscal_year to extract from the errors data, by default 1993

    Returns
    -------
    pd.DataFrame
    """
    deficits = make_projection_errors_data(
        'deficit',
        projection_years,
        start_year=start_year,
        calc_averages=False
    )
    deficits.columns = ["Year"] + [f"{c} Deficit Error" for c in deficits.columns[1:]]

    net_interest = make_projection_errors_data(
        'outlay',
        projection_years,
        category='Net Interest',
        subcategory='Net Interest',
        calc_averages=False
    )
    net_interest.columns = ["Year"] + [f"{c} Net Interest Error" for c in net_interest.columns[1:]]

    df = pd.merge(deficits, net_interest, on='Year')

    # Calculate the primary deficits
    for year in ['Budget Year', 'Year 6', 'Year 11']:
        df[f"{year} Primary Deficit Error"] = (
            df[f"{year} Deficit Error"].astype('float') -
            df[f"{year} Net Interest Error"].astype('float')
        )

    # Rearrange the column order
    cols = ["Year"]
    for years in ["Budget Year", "Year 6", "Year 11"]:
        cols.append(f"{years} Deficit Error")
        cols.append(f"{years} Primary Deficit Error")
        cols.append(f"{years} Net Interest Error")

    return df[cols]


def make_leg_changes_data(component, projection_years):
    """Make the data for the legislative changes for a given component and projection years.

    Parameters
    ----------
    component : str
        Either 'deficit' or 'debt'.
    projection_years : list
        Which projection years to extract from the errors data.

    Returns
    -------
    pd.DataFrame
    """
    assert component in ['deficit', 'debt'], "Invalid component name."

    df = pd.read_csv(f"{OUTPUT_PATH}/{component}_projection_errors.csv")

    # Filter and select the data
    keep_cols = [
        'projected_fiscal_year',
        'projected_year_number',
        'projection_error_pct_GDP',
        'leg_change_pct_GDP'
    ]
    filter_condition = df['projected_year_number'].isin(projection_years)
    df = df.loc[filter_condition, keep_cols]

    # Calculate the average absolute values for each projected year
    average_abs_values = df.groupby('projected_year_number').agg({
        'leg_change_pct_GDP': lambda x: x.abs().mean(),
        'projection_error_pct_GDP': lambda x: x.abs().mean()
    }).reset_index()

    # Rename columns for clarity
    average_abs_values.rename(columns={
        'leg_change_pct_GDP': 'Average Absolute Effect of Legislation',
        'projection_error_pct_GDP': 'Average Absolute Error'
    }, inplace=True)

    # Melt the DataFrame to unpivot it
    melted_df = average_abs_values.melt(
        id_vars='projected_year_number',
        var_name='Metric',
        value_name='Value'
    )

    # Pivot the DataFrame to get the desired format
    out_df = melted_df.pivot(
        index='Metric',
        columns='projected_year_number',
        values='Value'
    )

    # Clean up the index
    out_df = out_df.reindex(index=[
        'Average Absolute Error',
        'Average Absolute Effect of Legislation'
        ])
    out_df.reset_index(inplace=True)

    out_df.columns = [' ', 'Budget Year', '6th Year', '11th Year']

    return out_df.round(1)


def make_figure_6_data(projection_years, start_year=2020):
    """Make the data for Figure 6.

    Makes calls to make_projection_errors_data.

    Parameters
    ----------
    projection_years : list
        Which projection years to extract from the errors data.
    start_year : int, optional
        Start of projected_fiscal_year to extract from the errors data, by default 2020

    Returns
    -------
    pd.DataFrame
    """
    dfs = {}
    # Create leg effects data
    dfs['Mandatory'] = make_projection_errors_data(
        'outlay',
        projection_years,
        category='Mandatory',
        subcategory='Total Mandatory',
        start_year=start_year,
        leg_changes=True,
        calc_averages=False
    )

    dfs['Discretionary'] = make_projection_errors_data(
        'outlay',
        projection_years,
        category='Discretionary',
        subcategory='Total Discretionary',
        start_year=start_year,
        leg_changes=True,
        calc_averages=False
    )

    dfs['Total Revenue'] = make_projection_errors_data(
        'revenue',
        projection_years,
        category='Total',
        subcategory='Total',
        start_year=start_year,
        leg_changes=True,
        calc_averages=False,
        apply_rounding=False
    )

    dfs['Individual Income Taxes'] = make_projection_errors_data(
        'revenue',
        projection_years,
        category='Individual Income Taxes',
        subcategory='Individual Income Taxes',
        start_year=start_year,
        leg_changes=True,
        calc_averages=False,
        apply_rounding=False
    )

    # And add in the total deficit errors, too
    dfs['Total Deficit'] = make_projection_errors_data(
        'deficit',
        projection_years,
        start_year=start_year,
        leg_changes=False,
        calc_averages=False
    )

    # Rename the columns in each DataFrame
    for k, v in dfs.items():
        v.rename(columns={'Budget Year': k}, inplace=True)

    # Merge the DataFrames on Year
    df = reduce(lambda left, right: pd.merge(left, right, on='Year'), dfs.values())

    # Calculate the "Other Revenue" category
    df['Total Revenue'] = df['Total Revenue'] * -1
    df['Individual Income Taxes'] = df['Individual Income Taxes'] * -1
    df['Other Revenue'] = df['Total Revenue'] - df['Individual Income Taxes']
    df['Individual Income Taxes'] = df['Individual Income Taxes'].round(1)
    df['Other Revenue'] = df['Other Revenue'].round(1)
    df.drop(columns='Total Revenue', inplace=True)

    return df[['Year', 'Mandatory', 'Discretionary', 'Individual Income Taxes', 'Other Revenue', 'Total Deficit']]


def make_infographic_b1_data(projection_years, start_year=1993):
    """Make the data for Infographic B-1.

    Makes calls to make_projection_errors_data.

    Parameters
    ----------
    projection_years : list
        Which projection years to extract from the errors data.
    start_year : int, optional
        Start of projected_fiscal_year to extract from the errors data, by default 1993

    Returns
    -------
    pd.DataFrame
    """
    dfs = {}
    # Create leg effects DataFrames
    dfs['Mandatory'] = make_projection_errors_data(
        'outlay',
        projection_years,
        category='Mandatory',
        subcategory='Total Mandatory',
        start_year=start_year,
        leg_changes=True,
        calc_averages=False
    )

    dfs['Discretionary'] = make_projection_errors_data(
        'outlay',
        projection_years,
        category='Discretionary',
        subcategory='Total Discretionary',
        start_year=start_year,
        leg_changes=True,
        calc_averages=False
    )

    dfs['Net Interest'] = make_projection_errors_data(
        'outlay',
        projection_years,
        category='Net Interest',
        subcategory='Net Interest',
        start_year=start_year,
        leg_changes=True,
        calc_averages=False
    )

    dfs['Total Revenue'] = make_projection_errors_data(
        'revenue',
        projection_years,
        category='Total',
        subcategory='Total',
        start_year=start_year,
        leg_changes=True,
        calc_averages=False,
        apply_rounding=False
    )

    dfs['Individual Income Taxes'] = make_projection_errors_data(
        'revenue',
        projection_years,
        category='Individual Income Taxes',
        subcategory='Individual Income Taxes',
        start_year=start_year,
        leg_changes=True,
        calc_averages=False,
        apply_rounding=False
    )

    # Rename the columns in each DataFrame so they have the component/category name in them
    for k, v in dfs.items():
        for c in v.columns:
            if c != 'Year':
                v.rename(columns={c: f"{c} {k}"}, inplace=True)

    # Merge the DataFrames on Year
    df = reduce(lambda left, right: pd.merge(left, right, on='Year'), dfs.values())

    # Calculate the "Other Revenue" category for all years
    for year in ['Budget Year', 'Year 6', 'Year 11']:
        df[f"{year} Total Revenue"] = df[f"{year} Total Revenue"] * -1
        df[f"{year} Individual Income Taxes"] = df[f"{year} Individual Income Taxes"] * -1
        df[f"{year} Other Revenue"] = df[f"{year} Total Revenue"] - df[f"{year} Individual Income Taxes"]
        df.drop(columns=[f"{year} Total Revenue"], inplace=True)

        for measure in ['Individual Income Taxes', 'Other Revenue']:
            df[f"{year} {measure}"] = df[f"{year} {measure}"].round(1)
            # Set revenue components to NaN if the mandatory component is NaN
            df[f"{year} {measure}"] = df[f"{year} {measure}"].where(df[f"{year} Mandatory"].notna(), other=np.nan)

    # Select the columns to write out
    out_cols = ['Year']
    for year in ['Budget Year', 'Year 6', 'Year 11']:
        for component in [
            'Mandatory',
            'Discretionary',
            'Net Interest',
            'Individual Income Taxes',
            'Other Revenue']:
            out_cols.append(f"{year} {component}")

    return df[out_cols]
