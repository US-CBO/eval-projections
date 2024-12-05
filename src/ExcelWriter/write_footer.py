"""Module contains function to write footer in each worksheet."""

def write_footer(current_worksheet, worksheets, key, formats, data_len, data_width):
    """Write the last row for each worksheet in Data Underlying Figures workbook, with
    hyperlink back to Contents worksheet.

    Parameters
    ----------
    current_worksheet : xlsxwriter worksheet object
        Current worksheet to write header to.
    key : str
        Key for the worksheets dictionary
    formats : dict
        Dictionary of cell formats.
    data_len : int
        Length (number of rows) in the data written on a given worksheet.
    data_width : int
        Width (number of columns) in the data written on a given worksheet.

    Returns
    -------
    worksheet : xlsxwriter worksheet object
        Same worksheet object passed in, but with header content written to it.
    """
    last_data_row = worksheets[key]['start_data_row'] + data_len
    line_row = last_data_row
    url_row = line_row + 2

    # Write line
    for c in range(data_width):
        current_worksheet.write(line_row, c, '', formats['bottom_border'])

    # Write hyperlink back to Contents
    url_string = 'Back to Table of Contents'
    url = 'internal:Contents!A1'

    # Merge a few cells across to make full text of link clickable
    merge_range = 'A' + str(url_row+1) + ':C' + str(url_row+1)
    current_worksheet.merge_range(merge_range, None, formats['url'])

    # Note: Need to merge cells first, then write URL
    current_worksheet.write_url(url_row, 0, url, formats['url'], string=url_string)

    return current_worksheet
