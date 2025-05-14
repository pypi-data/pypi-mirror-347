import os
from unittest.mock import patch

import pandas as pd
import pytest
from gcfpy.app.main_window import MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox


@pytest.fixture
def linear_csv_path():
    return os.path.join(os.path.dirname(__file__), "../examples/data", "linear.csv")


def test_basic_fit_flow(qtbot, linear_csv_path):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()

    df = pd.read_csv(linear_csv_path)
    fit_tab.load_data_into_tab(df, file_path=linear_csv_path)

    fit_tab.formula_text.setPlainText("y=a*x + b")

    qtbot.mouseClick(fit_tab.fit_control.run_fit_button, Qt.LeftButton)

    qtbot.waitUntil(lambda: fit_tab.results_text.toPlainText() != "", timeout=3000)

    assert "Fit Statistics" in fit_tab.results_text.toPlainText()
    window.close()


def test_reset_fit_clears_plot_and_text(qtbot, linear_csv_path):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()

    df = pd.read_csv(linear_csv_path)
    fit_tab.load_data_into_tab(df, file_path=linear_csv_path)
    fit_tab.formula_text.setPlainText("y=a*x + b")
    qtbot.mouseClick(fit_tab.fit_control.run_fit_button, Qt.LeftButton)

    qtbot.waitUntil(lambda: fit_tab.results_text.toPlainText() != "", timeout=3000)
    qtbot.mouseClick(fit_tab.fit_control.reset_fit_button, Qt.LeftButton)
    assert fit_tab.results_text.toPlainText().strip() == ""
    window.close()


def test_invalid_formula_warning(qtbot, linear_csv_path):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()

    df = pd.read_csv(linear_csv_path)
    fit_tab.load_data_into_tab(df, file_path=linear_csv_path)

    fit_tab.formula_text.setPlainText("")

    with patch.object(QMessageBox, "warning") as mock_warning:
        qtbot.mouseClick(fit_tab.fit_control.run_fit_button, Qt.LeftButton)
        assert mock_warning.called
    window.close()


def test_add_fit_to_comparison(qtbot, linear_csv_path):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()

    df = pd.read_csv(linear_csv_path)
    fit_tab.load_data_into_tab(df, file_path=linear_csv_path)
    fit_tab.formula_text.setPlainText("y=a*x + b")

    qtbot.mouseClick(fit_tab.fit_control.run_fit_button, Qt.LeftButton)
    qtbot.waitUntil(lambda: fit_tab.results_text.toPlainText() != "", timeout=3000)

    window.toolbar.enable_comparison(True)

    window.toolbar.add_fit_action.trigger()

    stored = fit_tab.comparison_manager.stored_fits

    assert isinstance(stored, list)
    assert len(stored) == 1
    assert "formula" in stored[0]
    window.close()
