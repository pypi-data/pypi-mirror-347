from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from gcfpy.utils.data_loader import DataLoader


@pytest.fixture
def dummy_parent():
    mock = MagicMock()
    mock.toolbar = MagicMock()
    mock.get_current_fit_tab.return_value = MagicMock()
    mock.get_current_fit_tab.return_value.plot_widget = MagicMock()
    return mock


def test_read_csv_valid(tmp_path, dummy_parent):
    file_path = tmp_path / "valid.csv"
    file_path.write_text("X,Y\n1,2\n3,4")
    loader = DataLoader(dummy_parent)
    df = loader.read_csv(str(file_path))
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["X", "Y"]
    assert len(df) == 2


def test_read_csv_missing_columns(tmp_path, dummy_parent):
    file_path = tmp_path / "bad.csv"
    file_path.write_text("A,B\n1,2")
    loader = DataLoader(dummy_parent)
    with patch.object(loader, "_show_error") as mock_error:
        df = loader.read_csv(str(file_path))
        assert df is None
        mock_error.assert_called_once()


def test_read_csv_with_nans(tmp_path, dummy_parent):
    file_path = tmp_path / "nan.csv"
    file_path.write_text("X,Y\n1,\n3,4")
    loader = DataLoader(dummy_parent)
    with patch.object(loader, "_show_error") as mock_error:
        df = loader.read_csv(str(file_path))
        assert df is None
        mock_error.assert_called_once()

def test_load_data_unsupported(tmp_path, dummy_parent):
    file_path = tmp_path / "unsupported.txt"
    file_path.write_text("dummy")
    loader = DataLoader(dummy_parent)
    df, path = loader.load_data(str(file_path))
    assert df is None
    assert path is None


@patch("gcfpy.utils.data_loader.QMessageBox")
def test_show_error_box(mock_msgbox, dummy_parent):
    loader = DataLoader(dummy_parent)
    loader._show_error("hello")
    assert mock_msgbox.return_value.setText.called


def test_update_toolbar_on_load(dummy_parent):
    loader = DataLoader(dummy_parent)
    loader._update_toolbar_on_load()
    dummy_parent.toolbar.enable_toolbar_options.assert_called_once_with(True)
    dummy_parent.toolbar.enable_toolbar_plot_options.assert_called_once_with(False)
    dummy_parent.toolbar.enable_comparison.assert_called_once_with(False)


def test_get_previous_file_reads_file(tmp_path, dummy_parent):
    filepath = tmp_path / "previous.txt"
    filepath.write_text("test.csv")
    loader = DataLoader(dummy_parent)
    loader.prev_data_file = str(filepath)
    result = loader.get_previous_file()
    assert result == "test.csv"


def test_get_previous_file_missing(dummy_parent):
    loader = DataLoader(dummy_parent)
    loader.prev_data_file = "/non/existent/path.csv"
    result = loader.get_previous_file()
    assert result is None
