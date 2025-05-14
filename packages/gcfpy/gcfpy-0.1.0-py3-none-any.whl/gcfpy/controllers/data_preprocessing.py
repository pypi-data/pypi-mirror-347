import numpy as np
import pandas as pd
from scipy.signal import savgol_filter


def smooth_data(y, method):
    """
    Apply smoothing to 1D data using the specified method.

    Args:
        y (array-like): Input data.
        method (str): Smoothing method: 'avg', 'savgol', or 'none'.

    Returns:
        np.ndarray: Smoothed data (NaNs replaced if needed).

    Raises:
        ValueError: If an unknown smoothing method is passed.

    """
    if method == "avg":
        y_smooth = pd.Series(y).rolling(window=5, center=True).mean().to_numpy()
    elif method == "savgol":
        y_smooth = savgol_filter(y, window_length=5, polyorder=2)
    elif method == "none":
        return np.asarray(y)
    else:
        raise ValueError(f"Unknown smoothing method: '{method}'")

    if np.isnan(y_smooth).any():
        y_smooth = np.nan_to_num(y_smooth, nan=np.nanmean(y))

    return y_smooth


def weight_data(x_data, y_data, x_err=None, y_err=None, method="none"):
    """
    Generate weights for fitting based on provided errors.

    Args:
        x_data (array-like): X values.
        y_data (array-like): Y values.
        x_err (array-like or None): X-axis errors.
        y_err (array-like or None): Y-axis errors.
        method (str): One of 'x_err', 'y_err', 'xy_err', or 'none'.

    Returns:
        np.ndarray: Array of weights.

    """
    if method == "x_err":
        if x_err is None:
            x_err = 0.1 * np.abs(x_data)
        sx = x_err
        sy = np.zeros_like(y_data)
        sigma = None
        weights = np.ones_like(y_data)

    elif method == "y_err":
        if y_err is None:
            y_err = 0.1 * np.abs(y_data)
        sx = np.zeros_like(x_data)
        sy = y_err
        sigma = y_err
        weights = 1.0 / (y_err**2)

    elif method == "xy_err":
        if x_err is None:
            x_err = 0.1 * np.abs(x_data)
        if y_err is None:
            y_err = 0.1 * np.abs(y_data)
        sx = x_err
        sy = y_err
        sigma = np.sqrt(y_err**2)
        weights = 1.0 / (sigma**2)

    else:  # "none"
        sx = np.zeros_like(x_data)
        sy = np.zeros_like(y_data)
        sigma = None
        weights = np.ones_like(y_data)

    return weights, (sx, sy), sigma
