from collections import namedtuple
import yaml


def read_parameters(file):
    """Read in the parameters yaml file and return parameters as a namedtuple.

    Parameters
    ----------
    file : str
        Name of file containing the Excel parameters for the data underlying
        the figures Excel output file.

    Returns
    -------
    params : namedtuple
        A namedtuple containing all the parameters used in the CBOdist package.

    """
    with open(file) as param_file:
        parameters = yaml.load(param_file, Loader=yaml.FullLoader)

    Parameters = namedtuple('Parameters', parameters.keys())
    params = Parameters(*parameters.values())

    return params

