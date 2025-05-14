import pytest  # noqa: I001
import pandas as pd
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QFileDialog

from gcfpy.app.main_window import MainWindow, main

from unittest.mock import patch, MagicMock


@pytest.fixture
def window(qtbot):
    win = MainWindow()
    qtbot.addWidget(win)
    win.show()
    return win


@pytest.fixture
def sample_df():
    return pd.DataFrame({"X": range(10), "Y": [2 * x + 1 for x in range(10)]})


def test_add_and_get_tab(window):
    window.add_fit_tab()
    assert window.get_current_fit_tab() is not None


def test_rename_tab_logic(qtbot, window):
    index = window.tabs.currentIndex()
    window.rename_tab(index)
    tab_bar = window.tabs.tabBar()
    editor = tab_bar.tabButton(index, tab_bar.LeftSide)
    assert isinstance(editor, QLineEdit)
    editor.setText("New Name")
    editor.editingFinished.emit()
    assert window.tabs.tabText(index) == "New Name"
    window.close()


def test_duplicate_tab_with_data(window, sample_df):
    tab = window.get_current_fit_tab()
    tab.load_data_into_tab(sample_df, "dummy.csv")
    window.duplicate_tab(0)
    assert window.tabs.count() == 2
    new_tab = window.tabs.widget(1)
    assert new_tab.df.equals(sample_df)
    window.close()


def test_export_data_success(window, sample_df, monkeypatch, tmp_path):
    tab = window.get_current_fit_tab()
    tab.load_data_into_tab(sample_df, "dummy.csv")

    export_path = tmp_path / "test_export.csv"
    monkeypatch.setattr(
        QFileDialog,
        "getSaveFileName",
        lambda *args, **kwargs: (str(export_path), "csv"),
    )
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: None)

    window.export_data()
    assert export_path.exists()
    exported_df = pd.read_csv(export_path)
    assert exported_df.equals(sample_df)
    window.close()


def test_export_data_cancel(window, sample_df, monkeypatch):
    tab = window.get_current_fit_tab()
    tab.load_data_into_tab(sample_df, "dummy.csv")
    monkeypatch.setattr(
        QFileDialog, "getSaveFileName", lambda *args, **kwargs: ("", "csv")
    )
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: None)
    window.export_data()
    window.close()


@pytest.fixture
def main_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


def test_add_and_close_tab(main_window, qtbot):
    initial_count = main_window.tabs.count()
    main_window.add_fit_tab()
    assert main_window.tabs.count() == initial_count + 1

    main_window.close_fit_tab(main_window.tabs.currentIndex())
    assert main_window.tabs.count() == initial_count


def test_restore_default_view(main_window):
    current_tab = main_window.get_current_fit_tab()
    assert current_tab is not None
    main_window.restore_default_view()
    for name, (action, dock) in main_window.view_actions_per_tab[current_tab].items():
        assert action.isChecked()
        assert dock.isVisible()


def test_unload_data(main_window, qtbot):
    df = pd.DataFrame({"X": [1, 2], "Y": [3, 4]})
    tab = main_window.get_current_fit_tab()
    tab.load_data_into_tab(df, file_path="dummy.csv")
    assert tab.df is not None

    main_window.unload_data()
    assert tab.df is None


def test_enable_disable_toolbar(main_window):
    main_window.enable_toolbar_buttons(True)
    assert main_window.toolbar.toggle_confidence_action.isEnabled()

    main_window.enable_toolbar_buttons(False)
    assert not main_window.toolbar.toggle_confidence_action.isEnabled()


def test_get_current_fit_tab_returns_none_when_invalid(main_window):
    main_window.tabs.addTab(QMessageBox(), "Not a FitTab")
    main_window.tabs.setCurrentIndex(main_window.tabs.count() - 1)
    assert main_window.get_current_fit_tab() is None


@patch("gcfpy.app.main_window.DataLoader")
@patch("gcfpy.app.main_window.save_previous_file")
def test_load_data_from_menu(mock_save, mock_loader, main_window):
    mock_df = pd.DataFrame({"X": [1, 2], "Y": [3, 4]})
    mock_loader.return_value.load_data.return_value = (mock_df, "dummy.csv")

    main_window.load_data_from_menu()

    tab = main_window.get_current_fit_tab()
    assert tab.df.equals(mock_df)
    mock_save.assert_called_once_with("dummy.csv")


@patch("gcfpy.app.main_window.load_previous_file", return_value="previous.csv")
@patch("gcfpy.app.main_window.DataLoader")
@patch("os.path.exists", return_value=True)
def test_load_previous_data_success(mock_exists, mock_loader, mock_prev, main_window):
    mock_df = pd.DataFrame({"X": [1, 2], "Y": [3, 4]})
    mock_loader.return_value.load_data.return_value = (mock_df, "previous.csv")

    main_window.load_previous_data()

    tab = main_window.get_current_fit_tab()
    assert tab.df.equals(mock_df)


@patch("gcfpy.app.main_window.load_previous_file", return_value=None)
def test_load_previous_data_missing_file(mock_prev, main_window):
    # Should not crash even if no file
    main_window.load_previous_data()


def test_inject_data_into_tab(main_window):
    df = pd.DataFrame({"X": [1], "Y": [2]})
    main_window._inject_data_into_tab(df, "injected.csv", "Injected")
    tab = main_window.get_current_fit_tab()
    assert tab.df.equals(df)


@patch("gcfpy.app.main_window.QApplication")
@patch("gcfpy.app.main_window.MainWindow")
def test_main_runs_without_error(mock_window_cls, mock_qapp):
    mock_app = MagicMock()
    mock_qapp.return_value = mock_app
    mock_window = MagicMock()
    mock_window_cls.return_value = mock_window

    with patch("gcfpy.app.main_window.sys") as mock_sys:
        mock_sys.argv = []
        mock_sys.exit = lambda code: None  # prevent exit
        main()

    mock_app.setWindowIcon.assert_called()
    mock_window.show.assert_called()
    mock_app.exec_.assert_called()
