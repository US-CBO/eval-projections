from ExcelWriter.write_header import write_header


def write_contents(workbook, worksheets, params, formats):
    """Write out the Contents worksheet for the Data Underlying Figures Excel workbook.

    Parameters
    ----------
    workbook : xlsxwriter workbook object
        The Data Underlying the Figures workbook.
    worksheets : dict
        Dictionary containing parameters for each worksheet to be written.
    params : namedtuple
        All the parameters for data underlying the figures file. (Created by read_parameters.py)
    formats : dict
        Dictionary containing cell formats used throughout.

    Returns
    -------
    workbook : xlsxwriter workbook object
        Same workbook passed in, but now with a Contents worksheet added to it.
    """
    col_A_width = 120

    current_worksheet = workbook.add_worksheet('Contents')

    # Format column A
    current_worksheet.set_column('A:A', col_A_width, formats['default'])

    # Write header rows
    current_worksheet = write_header(current_worksheet, worksheets, None, params, formats, contents=True)

    # Write worksheet title
    current_worksheet.write(4, 0, 'Contents', formats['bold'])

    # Write out anchor text with hyperlinks to each worksheet
    row = 5  # Starting at row 5
    for ws in worksheets.keys():
        url = f"internal:'{ws}'!A1"
        anchor_text = f'{ws}. {worksheets[ws]["title"]}'
        current_worksheet.write_url(row, 0, url, formats['url'], string=anchor_text)

        row += 1

    return workbook
