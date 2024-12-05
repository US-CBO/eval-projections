import pandas as pd


def write_data(worksheets, ws, writer, formats):
    """Write the data to the Excel file.

    Parameters
    ----------
    worksheets : dict
        Dictionary containing parameters for each worksheet to be written.
    ws : str
        Key for the worksheets dictionary of the current worksheet to write.
    writer : pd.ExcelWriter object
        Writer object to write to Excel file, using the xlsxwriter engine.
    formats : dict
        Dictionary of cell formats.

    Returns
    -------
    None; Writes data to Excel file.
    """
    df = worksheets[ws]['data']
    start_row = 8

    df.to_excel(
        writer,
        sheet_name = ws,
        startrow = start_row,
        header = False,
        index = False
    )

    current_worksheet = writer.sheets[ws]

    # Format the columns
    current_worksheet.set_column(0, 0, worksheets[ws]['width_col_A'], formats['center'])
    if ws in ['Figure 1', 'Figure 5']:
        current_worksheet.set_column(1, 1, worksheets[ws]['width_col_B'], formats['center'])
        current_worksheet.set_column(2, len(df.columns)-1, worksheets[ws]['width_data_cols'], formats[worksheets[ws]['fmt']])
    else:
        current_worksheet.set_column(1, len(df.columns), worksheets[ws]['width_data_cols'], formats[worksheets[ws]['fmt']])

    # Write column labels
    for c, col_label in enumerate(df.columns):
        current_worksheet.write(start_row-1, c, col_label, formats['data_header'])

    return None
