"""Module for writing the header rows for each worksheet in the Data Underlying Figures workbook."""

def write_header(current_worksheet, worksheets, key, params, formats, contents=False):
    """Write the first two header rows for each worksheet in Data Underlying Figures workbook.

    Parameters
    ----------
    current_worksheet : xlsxwriter worksheet object
        Current worksheet to write header to.
    worksheets : dict
        Dictionary containing parameters for each worksheet to be written.
    key : str
        Key for the worksheets dictionary
    params : namedtuple
        All the parameters for the CBOdist package.
        (Created in utils.read_parameters())
    formats : dict
        Dictionary of cell formats.
    contents : boolean, by default False
        Set to True only for Contents worksheet to handle different cell
        merging on the Contents worksheet.

    Returns
    -------
    current_worksheet : xlsxwriter worksheet object
        Same worksheet object passed in, but with header content written to it.
    """

    # First row (Note: rows are zero-indexed)
    header = f"This file presents the data underlying the figures in CBO's {params.PUB_DATE} report "
    pub_title = f"{params.PUB_TITLE}{params.START_YEAR} to {params.END_YEAR}."

    current_worksheet.write_rich_string(0, 0, formats['default'], header, formats['italic'], pub_title)

    # Second row
    url_string = f'www.cbo.gov/publication/{params.PUB_NUM}'
    url = f'http://{url_string}'

    current_worksheet.write_url(1, 0, url, formats['url'], string=url_string)

    # Merge a few cells across to make full text of link clickable
    # (but don't do this for Contents worksheet)
    if not contents:
        current_worksheet.set_row(0, None, formats['default'])
        current_worksheet.merge_range('A2:D2', '')

        # Skip two rows (row indexes 2 and 3)

        # Only write out table Figure number, title, and units if not Contents page
        current_worksheet.write(4, 0, f'{key}.', formats['bold'])
        current_worksheet.write(5, 0, f'{worksheets[key]["title"]}', formats['bold'])
        current_worksheet.write(6, 0, worksheets[key]['units'], formats['bottom_border'])

    return current_worksheet
