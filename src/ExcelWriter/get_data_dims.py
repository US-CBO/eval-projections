"""Module contains function to get the dimensions of the data to be written."""

def get_data_dims(df):
    """Get the dimensions of the data to be written.

    Parameters
    ----------
    df : pd.DataFrame
        The data to be written.

    Returns
    -------
    tuple : The dimensions of the data to be written.
    """
    return df.shape