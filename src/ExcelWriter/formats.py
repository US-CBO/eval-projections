"""Module for creating Excel formats for xlsxwriter."""

def create_formats(workbook):
    """Create a dictionary of format objects for xlsxwriter.

    Parameters
    ----------
    workbook : xlsxwriter.Workbook
        Excel workbook to be written out.

    Returns
    -------
    formats : dict
    """
    formats = {
        'default' : workbook.add_format({
            'font' : 'Arial',
            'size' : 11,
            'valign' : 'bottom',
            'align' : 'left',
        }),

        'url' : workbook.add_format({
            'font' : 'Arial',
            'size' : 11,
            'color' : '1F497D',  # dark blue for hyperlinks
            'valign' : 'bottom',
        }),

        'bold' : workbook.add_format({
            'font' : 'Arial',
            'size' : 11,
            'valign' : 'bottom',
            'bold' : True,
        }),

        'italic' : workbook.add_format({
            'font' : 'Arial',
            'size' : 11,
            'valign' : 'bottom',
            'italic' : True,
        }),

        'center' : workbook.add_format({
            'font' : 'Arial',
            'size' : 11,
            'valign' : 'bottom',
            'align' : 'center',
        }),

        'data_header' : workbook.add_format({
            'font' : 'Arial',
            'size' : 11,
            'text_wrap' : True,
            'valign' : 'bottom',
            'align' : 'center',
            'top' : 1,
            'bottom' : 1,
        }),

        'numeric_1' : workbook.add_format({
            'font' : 'Arial',
            'size' : 11,
            'num_format': '#,##0.0',
            'valign' : 'bottom',
            'align' : 'center',
        }),

        'bottom_border' : workbook.add_format({
            'font' : 'Arial',
            'size' : 11,
            'bottom' : 1,
        }),

        'wrapped' : workbook.add_format({
            'font' : 'Ariel',
            'size' : 11,
            'text_wrap' : True,
            'align' : 'left',
            'valign' : 'top'
        }),
    }

    return formats