import os

import pandas as pd
import pytest
from gcfpy.app.main_window import MainWindow
from PyQt5.QtCore import Qt


@pytest.fixture
def linear_csv_path():
    return os.path.join(os.path.dirname(__file__), "../examples/data", "linear.csv")


def test_manual_fit_button(qtbot, linear_csv_path):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()

    df = pd.read_csv(linear_csv_path)
    fit_tab.load_data_into_tab(df, file_path=linear_csv_path)

    manual_button = fit_tab.fit_control.manual_button

    assert manual_button is not None
    assert manual_button.isEnabled()

    qtbot.mouseClick(manual_button, Qt.LeftButton)

    assert hasattr(fit_tab, "manual_control")
    assert hasattr(fit_tab.manual_control, "dock_manual")
    assert not fit_tab.manual_control.dock_manual.isHidden()
    window.close()
