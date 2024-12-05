from datetime import datetime
import os.path
import pandas as pd

from ExcelWriter.read_parameters import read_parameters
from ExcelWriter.worksheets import worksheets
from ExcelWriter.make_data_underlying_figures import make_all_data
from ExcelWriter.formats import create_formats
from ExcelWriter.write_contents import write_contents
from ExcelWriter.write_data import write_data
from ExcelWriter.write_header import write_header
from ExcelWriter.write_footer import write_footer
from ExcelWriter.get_data_dims import get_data_dims

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_PATH = os.path.abspath(f"{CURRENT_PATH}/../output_data")

params = read_parameters(f"{CURRENT_PATH}/../Excel_parameters.yml")
worksheets = make_all_data(worksheets)  # Create all the data and add them to the worksheets dictionary

def write_Excel(params=params, worksheets=worksheets):
    """Write the Excel file based on the parameters and worksheets provided.

    Parameters
    ----------
    params : named tuple, by default params
        High-level parameters for the Excel file.
    worksheets : dict, by default worksheets
        Contains worksheet-specific parameters for the Excel file.

    Returns
    -------
    None; Writes Excel file to disk.
    """
    # Excel file details
    filename = f'{params.PUB_NUM}-data.xlsx'
    filepath = os.path.join(os.path.abspath(f"{OUTPUT_PATH}/Excel"), filename)
    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    workbook  = writer.book

    formats = create_formats(workbook)

    # Start by writing out Contents sheet
    workbook = write_contents(workbook, worksheets, params, formats)

    # Then write each worksheet based on info in the worksheets dictionary
    with workbook as wb:
        for ws in worksheets:
            current_worksheet = wb.add_worksheet(ws)
            data_len, data_width = get_data_dims(worksheets[ws]['data'])

            write_data(worksheets, ws, writer, formats)
            write_header(current_worksheet, worksheets, ws, params, formats)
            write_footer(current_worksheet, worksheets, ws, formats, data_len, data_width)

        # Set a fixed creation date, so each run doesn't produce
        # differences in the binary Excel file.
        wb.set_properties({'created' : datetime(1974, 7, 12, 12, 27)})

    print(f"Data Underlying Figures Excel file for CBO publication {params.PUB_NUM} created successfully.")
    print(f"Excel file written to: {OUTPUT_PATH}\\Excel.\n")

    return None

if __name__ == '__main__':
    write_Excel()
