import numpy as np
import pytest
from gcfpy.controllers.data_preprocessing import smooth_data, weight_data


def test_smooth_data_avg():
    y = np.array([1, 2, 3, 4, 5, 6, 7])
    result = smooth_data(y, method="avg")
    assert isinstance(result, np.ndarray)
    assert not np.isnan(result).all()


def test_smooth_data_savgol():
    y = np.array([1, 2, 3, 4, 5, 6, 7])
    result = smooth_data(y, method="savgol")
    assert isinstance(result, np.ndarray)
    assert not np.isnan(result).all()


def test_smooth_data_none():
    y = np.array([1, 2, 3])
    result = smooth_data(y, method="none")
    assert np.all(result == y)


def test_smooth_data_invalid():
    y = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        smooth_data(y, method="invalid")


def test_weight_data_none():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    w, (sx, sy), sigma = weight_data(x, y, method="none")
    assert np.allclose(w, 1)
    assert np.allclose(sx, 0)
    assert np.allclose(sy, 0)
    assert sigma is None


def test_weight_data_x_err_provided():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    x_err = np.array([0.1, 0.2, 0.3])
    w, (sx, sy), sigma = weight_data(x, y, x_err=x_err, method="x_err")
    assert np.allclose(sx, x_err)
    assert np.allclose(sy, 0)
    assert sigma is None
    assert np.allclose(w, 1)


def test_weight_data_x_err_generated():
    x = np.array([10, 20, 30])
    y = np.array([1, 2, 3])
    w, (sx, sy), sigma = weight_data(x, y, method="x_err")
    assert np.allclose(sx, 0.1 * np.abs(x))
    assert np.allclose(sy, 0)
    assert sigma is None
    assert np.allclose(w, 1)


def test_weight_data_y_err_provided():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    y_err = np.array([0.1, 0.2, 0.3])
    w, (sx, sy), sigma = weight_data(x, y, y_err=y_err, method="y_err")
    assert np.allclose(sx, 0)
    assert np.allclose(sy, y_err)
    assert np.allclose(sigma, y_err)
    assert np.allclose(w, 1.0 / (y_err**2))


def test_weight_data_y_err_generated():
    x = np.array([1, 2, 3])
    y = np.array([10, 20, 30])
    w, (sx, sy), sigma = weight_data(x, y, method="y_err")
    expected = 0.1 * np.abs(y)
    assert np.allclose(sx, 0)
    assert np.allclose(sy, expected)
    assert np.allclose(sigma, expected)
    assert np.allclose(w, 1.0 / (expected**2))


def test_weight_data_xy_err():
    x = np.array([10, 20, 30])
    y = np.array([100, 200, 300])
    w, (sx, sy), sigma = weight_data(x, y, method="xy_err")
    expected_x = 0.1 * np.abs(x)
    expected_y = 0.1 * np.abs(y)
    assert np.allclose(sx, expected_x)
    assert np.allclose(sy, expected_y)
    assert np.allclose(sigma, expected_y)
    assert np.allclose(w, 1.0 / (expected_y**2))
