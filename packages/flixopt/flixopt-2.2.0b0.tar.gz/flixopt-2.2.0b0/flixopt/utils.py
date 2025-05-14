"""
This module contains several utility functions used throughout the flixopt framework.
"""

import logging
from typing import Any, Dict, List, Literal, Optional, Union

import numpy as np
import xarray as xr

logger = logging.getLogger('flixopt')


def round_floats(obj, decimals=2):
    if isinstance(obj, dict):
        return {k: round_floats(v, decimals) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [round_floats(v, decimals) for v in obj]
    elif isinstance(obj, float):
        return round(obj, decimals)
    elif isinstance(obj, int):
        return obj
    elif isinstance(obj, np.ndarray):
        return np.round(obj, decimals).tolist()
    elif isinstance(obj, xr.DataArray):
        return obj.round(decimals).values.tolist()
    return obj


def convert_dataarray(
    data: xr.DataArray, mode: Literal['py', 'numpy', 'xarray', 'structure']
) -> Union[List, np.ndarray, xr.DataArray, str]:
    """
    Convert a DataArray to a different format.

    Args:
        data: The DataArray to convert.
        mode: The mode to convert to.
            - 'py': Convert to python native types (for json)
            - 'numpy': Convert to numpy array
            - 'xarray': Convert to xarray.DataArray
            - 'structure': Convert to strings (for structure, storing variable names)

    Returns:
        The converted data.

    Raises:
        ValueError: If the mode is unknown.
    """
    if mode == 'numpy':
        return data.values
    elif mode == 'py':
        return data.values.tolist()
    elif mode == 'xarray':
        return data
    elif mode == 'structure':
        return f':::{data.name}'
    else:
        raise ValueError(f'Unknown mode {mode}')
