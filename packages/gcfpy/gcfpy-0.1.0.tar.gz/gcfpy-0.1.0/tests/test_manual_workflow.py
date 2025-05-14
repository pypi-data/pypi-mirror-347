import os

import numpy as np
import pandas as pd
import pytest
from gcfpy.app.main_window import MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit


@pytest.fixture
def linear_csv_path():
    return os.path.join(os.path.dirname(__file__), "../examples/data", "linear.csv")


def test_manual_fit_workflow(qtbot, linear_csv_path):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()

    df = pd.read_csv(linear_csv_path)
    fit_tab.load_data_into_tab(df, file_path=linear_csv_path)
    fit_tab.formula_text.setPlainText("y = a*x + b")

    manual_btn = fit_tab.fit_control.manual_button
    qtbot.mouseClick(manual_btn, Qt.LeftButton)

    manual = fit_tab.manual_control
    assert manual is not None
    assert not manual.dock_manual.isHidden()

    assert "a" in manual.param_sliders
    assert "b" in manual.param_sliders

    slider_a = manual.param_sliders["a"]
    label_a = manual.param_labels["a"]
    min_input = manual.slider_ranges[slider_a]["min_box"]
    max_input = manual.slider_ranges[slider_a]["max_box"]

    slider_a.setValue(50)
    qtbot.wait(100)
    val_txt = label_a.text()
    assert val_txt.startswith("a:")

    min_input.setText("0.1")
    max_input.setText("10.0")
    qtbot.keyClick(min_input, Qt.Key_Enter)
    qtbot.wait(100)
    qtbot.keyClick(max_input, Qt.Key_Enter)
    qtbot.wait(100)

    p0_found = False
    for row in range(fit_tab.fit_options_dialog.params_table.rowCount()):
        param_item = fit_tab.fit_options_dialog.params_table.item(row, 0)
        if param_item and param_item.text() == "a":
            p0_widget = fit_tab.fit_options_dialog.params_table.cellWidget(row, 2)
            if isinstance(p0_widget, QLineEdit):
                p0_val = float(p0_widget.text())
                assert 0.1 <= p0_val <= 10.0
                p0_found = True
    assert p0_found
    fit_tab.manual_control.toggle_manual_dock()

    assert not fit_tab.manual_control.dock_manual.isVisible()
    assert fit_tab.xy_table.rowCount() == 2
    window.close()


@pytest.fixture
def linear_2d_csv_path():
    return os.path.join(
        os.path.dirname(__file__), "../examples/data", "example_2d_fit_data.csv"
    )


def test_manual_fit_workflow_2d(qtbot, linear_2d_csv_path):
    path = linear_2d_csv_path
    x = np.tile(np.linspace(0, 10, 10), 10)
    y = np.repeat(np.linspace(0, 5, 10), 10)
    z = 2 * x + 3 * y + 1
    df = pd.DataFrame({"X": x, "Y": y, "Z": z})
    df.to_csv(path, index=False)

    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()

    fit_tab.load_data_into_tab(df, file_path=str(path))

    fit_tab.fit_control.strategy_selector.setCurrentText("Fit per Y")
    fit_tab.formula_text.setPlainText("z = a*x + b*y + c")

    fit_tab.manual_control.toggle_manual_dock()
    assert fit_tab.manual_control.dock_manual.isVisible()

    slider = next(iter(fit_tab.manual_control.param_sliders.values()))
    qtbot.mouseClick(slider, Qt.LeftButton)

    assert fit_tab.xy_table.rowCount() >= 5
    assert fit_tab.xy_table.verticalHeaderItem(2).text() == "Z"
    assert fit_tab.xy_table.verticalHeaderItem(3).text() == "Manual"
    assert fit_tab.xy_table.verticalHeaderItem(4).text() == "Residual"

    fit_tab.manual_control.toggle_manual_dock()
    assert not fit_tab.manual_control.dock_manual.isVisible()

    window.close()
