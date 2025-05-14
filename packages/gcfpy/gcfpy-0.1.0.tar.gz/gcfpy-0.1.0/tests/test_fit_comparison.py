import os
import warnings

import numpy as np
import pandas as pd
import pytest
from gcfpy.app.main_window import MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog


@pytest.fixture
def linear_csv_path():
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../examples/data/linear.csv")
    )


@pytest.mark.parametrize("method", ["leastsq", "odr"])
def test_fit_comparison_workflow(qtbot, linear_csv_path, tmp_path, method):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()
    df = pd.read_csv(linear_csv_path)

    fit_tab.load_data_into_tab(df, file_path=linear_csv_path)
    fit_tab.formula_text.setPlainText("y = a * x + b")
    fit_tab.fit_options_dialog.method_combo.setCurrentText(method)

    qtbot.mouseClick(fit_tab.fit_control.run_fit_button, Qt.LeftButton)
    qtbot.waitUntil(lambda: fit_tab.results_text.toPlainText() != "", timeout=3000)
    window.toolbar.add_fit_action.trigger()

    table = fit_tab.fit_options_dialog.params_table
    table.cellWidget(0, 2).setText("10")  # a = 10
    table.cellWidget(1, 2).setText("2")  # b = 0

    qtbot.mouseClick(fit_tab.fit_control.run_fit_button, Qt.LeftButton)
    qtbot.waitUntil(lambda: fit_tab.results_text.toPlainText() != "", timeout=3000)
    window.toolbar.add_fit_action.trigger()

    manager = fit_tab.comparison_manager

    assert len(manager.stored_fits) == 2
    assert not manager.comparison_mode

    window.toolbar.toggle_comparison_action.trigger()
    assert manager.comparison_mode
    assert manager.dock_comparison is not None
    assert manager.comparison_plot is not None
    assert manager.comparison_table is not None
    assert manager.fit_list.count() == 2

    window.toolbar.toggle_comparison_action.trigger()
    assert not manager.comparison_mode

    csv_path = tmp_path / "export.csv"
    manager.export_comparison_csv = lambda: csv_path.write_text("dummy")
    manager.export_comparison_csv()
    assert csv_path.exists()
    window.close()


@pytest.mark.parametrize("strategy", ["1D", "Fit per Y"])
def test_fit_comparison_manager_features(qtbot, tmp_path, strategy):
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=".*invalid value encountered in divide.*",
            category=RuntimeWarning,
            module="lmfit",
        )

        window = MainWindow()
        qtbot.addWidget(window)
        window.show()
        window.add_fit_tab()
        fit_tab = window.get_current_fit_tab()

        if strategy == "1D":
            df = pd.DataFrame(
                {"X": np.linspace(1, 10, 20), "Y": 2 * np.linspace(1, 10, 20) + 1}
            )
        else:
            x = np.tile(np.linspace(1, 10, 20), 5)
            y = np.repeat(np.linspace(1, 4, 5), 20)
            z = 2 * x + y + 1
            df = pd.DataFrame({"X": x, "Y": y, "Z": z})

        fit_tab.load_data_into_tab(df, "dummy.csv")
        fit_tab.formula_text.setPlainText(
            "y = a*x + b" if strategy == "1D" else "z = a*x + b*y + c"
        )
        if strategy == "Fit per Y":
            fit_tab.fit_control.strategy_selector.setCurrentText("Fit per Y")
        fit_tab.fit_options_dialog.method_combo.setCurrentText("leastsq")

        qtbot.mouseClick(fit_tab.fit_control.run_fit_button, Qt.LeftButton)
        qtbot.waitUntil(lambda: fit_tab.plot_widget.result is not None, timeout=3000)

        fit_tab.comparison_manager.store_current_fit()
        fit_tab.comparison_manager.toggle_comparison_mode(True)

        parameter_table = fit_tab.comparison_manager.create_parameter_table()
        assert parameter_table.rowCount() > 0
        assert parameter_table.columnCount() > 0

        item = fit_tab.comparison_manager.fit_list.item(0)
        item.setText("CustomName: y=a*x + b")
        item.setCheckState(Qt.Checked)
        fit_tab.comparison_manager.handle_fit_list_change(item)

        csv_path = tmp_path / "comparison.csv"

        def mock_dialog(*args, **kwargs):
            return str(csv_path), "CSV Files (*.csv)"

        QFileDialog.getSaveFileName = staticmethod(mock_dialog)
        fit_tab.comparison_manager.export_comparison_csv()
        assert csv_path.exists()

        fit_tab.comparison_manager.reset()
        assert len(fit_tab.comparison_manager.stored_fits) == 0
        window.close()
