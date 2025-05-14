import os

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from gcfpy.app.main_window import MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


@pytest.fixture
def linear_csv_path():
    return os.path.join(os.path.dirname(__file__), "../examples/data", "linear.csv")


@pytest.mark.parametrize("method", ["lmfit", "odr", "emcee"])
def test_toolbar_plot_toggles(qtbot, linear_csv_path, method):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()

    df = pd.read_csv(linear_csv_path)
    fit_tab.load_data_into_tab(df, file_path=linear_csv_path)
    fit_tab.formula_text.setPlainText("y=a*x + b")
    fit_tab.fit_options_dialog.method_combo.setCurrentText(method)

    qtbot.mouseClick(fit_tab.fit_control.run_fit_button, Qt.LeftButton)
    qtbot.waitUntil(lambda: fit_tab.results_text.toPlainText() != "", timeout=5000)

    def get_button_for_action(toolbar, action):
        for child in toolbar.findChildren(QWidget):
            if hasattr(child, "defaultAction") and child.defaultAction() == action:
                return child
        return None

    residual_btn = get_button_for_action(
        window.toolbar, window.toolbar.toggle_residuals_action
    )
    confidence_btn = get_button_for_action(
        window.toolbar, window.toolbar.toggle_confidence_action
    )
    components_btn = get_button_for_action(
        window.toolbar, window.toolbar.toggle_components_action
    )
    components_2d_btn = get_button_for_action(
        window.toolbar, window.toolbar.toggle_confidence_2d_action
    )

    if method != "emcee":
        qtbot.mouseClick(residual_btn, Qt.LeftButton)

        qtbot.mouseClick(confidence_btn, Qt.LeftButton)

        qtbot.mouseClick(components_btn, Qt.LeftButton)
        qtbot.mouseClick(components_2d_btn, Qt.LeftButton)

    plt.close("all")
    window.close()
