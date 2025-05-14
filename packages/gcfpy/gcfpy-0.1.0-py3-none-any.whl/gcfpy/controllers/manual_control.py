import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from gcfpy.widgets import BaseDockWidget

from .code_generator import generate_python_code
from .formula_tools import extract_parameters


class ManualControl:
    """
    ManualControl panel for interactive manual fitting.
    """

    def __init__(self, parent):
        """Initializes the Manual Adjustments dock."""
        self.parent = parent
        self.dock_manual = BaseDockWidget("Manual Adjustments", parent)
        self.manual_layout = QVBoxLayout()
        self.manual_widget = QWidget()
        self.manual_widget.setLayout(self.manual_layout)
        self.dock_manual.setWidget(self.manual_widget)
        self.dock_manual.setHidden(True)

        self.parent.addDockWidget(Qt.RightDockWidgetArea, self.dock_manual)

        self.param_sliders = {}
        self.param_labels = {}
        self.slider_ranges = {}
        self.grid_layout = None

    def toggle_manual_dock(self):
        """Toggles visibility of the manual control dock and XY table rows."""
        if (
            not hasattr(self.parent, "manual_control")
            or self.parent.manual_control is None
        ):
            print("Recreating manual mode object.")
            self.parent.manual_control = ManualControl(self.parent)

        if (
            hasattr(self, "dock_manual")
            and self.dock_manual
            and not self.dock_manual.isHidden()
        ):
            print("Closing manual mode.")
            self.toggle_manual_column(False)
            self.dock_manual.hide()
            # self.dock_manual.deleteLater()
            # del self.dock_manual
            self.parent.fit_control.manual_button.setText("Manual")
            return

        self.toggle_manual_column(True)
        self.setup_manual_sliders()
        self.dock_manual.show()
        self.parent.fit_control.manual_button.setText("Close Manual")

    def setup_manual_sliders(self):
        """Creates sliders dynamically based on parameters."""
        while self.manual_layout.count():
            item = self.manual_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.grid_layout is not None:
            while self.grid_layout.count():
                item = self.grid_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                elif item.spacerItem():
                    self.grid_layout.removeItem(item)

            self.manual_layout.removeItem(self.grid_layout)
            self.grid_layout.deleteLater()
            self.grid_layout = None

        self.grid_layout = QGridLayout()
        formula = self.parent.formula_text.toPlainText()
        parameters = sorted(extract_parameters(formula))

        for row, param in enumerate(parameters):
            slider_label = QLabel(f"{param}: 1.0")
            min_input = QLineEdit("1.0")
            max_input = QLineEdit("100.0")
            slider = QSlider(Qt.Horizontal)

            min_input.setFixedWidth(80)
            max_input.setFixedWidth(80)
            min_input.setAlignment(Qt.AlignCenter)
            max_input.setAlignment(Qt.AlignCenter)

            slider.setMinimum(1)
            slider.setMaximum(100)
            slider.setValue(10)
            slider.setTickPosition(QSlider.NoTicks)

            spacer = QSpacerItem(20, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)

            self.param_labels[param] = slider_label
            self.param_sliders[param] = slider
            self.slider_ranges[slider] = {
                "min_box": min_input,
                "max_box": max_input,
            }

            slider.valueChanged.connect(
                lambda value, p=param, s=slider: self.update_slider_value(value, p, s)
            )
            min_input.editingFinished.connect(
                lambda p=param, min_box=min_input, max_box=max_input, s=slider: self.update_slider_range(
                    p, min_box, max_box, s, is_min=True
                )
            )

            max_input.editingFinished.connect(
                lambda p=param, min_box=min_input, max_box=max_input, s=slider: self.update_slider_range(
                    p, min_box, max_box, s, is_min=False
                )
            )

            self.grid_layout.addWidget(slider_label, row, 4)
            self.grid_layout.addItem(spacer, row, 3)
            self.grid_layout.addWidget(min_input, row, 0)
            self.grid_layout.addWidget(slider, row, 1)
            self.grid_layout.addWidget(max_input, row, 2)

        self.manual_layout.addLayout(self.grid_layout)

    def update_manual_plot(self):
        """Updates manual fit plot and residuals in the XY table."""
        if not hasattr(self, "param_sliders"):
            return

        param_values = {}
        for param, slider in self.param_sliders.items():
            min_val = float(
                self.slider_ranges[slider]["min_box"].text().replace(",", ".")
            )
            max_val = float(
                self.slider_ranges[slider]["max_box"].text().replace(",", ".")
            )
            if min_val == max_val:
                max_val += 1e-6
            use_log = abs(np.log10(max_val / min_val)) > 3
            if use_log:
                real_val = 10 ** (
                    np.log10(min_val)
                    + ((slider.value() - 1) / 99)
                    * (np.log10(max_val) - np.log10(min_val))
                )
            else:
                real_val = min_val + ((slider.value() - 1) / 99) * (max_val - min_val)
            param_values[param] = real_val

        function_code = generate_python_code(self.parent.formula_text.toPlainText())
        if "### ERROR" in function_code:
            return

        exec(function_code, globals())
        if "fit_function" in globals():
            fit_func = globals()["fit_function"]
            import inspect

            mode = self.parent.current_mode
            if mode == "2D":
                nbr_params = 2
            else:
                nbr_params = 1

            if len(inspect.signature(fit_func).parameters) - nbr_params != len(
                param_values
            ):
                self.parent.show_error_message(
                    "Mismatch between sliders and formula parameters."
                )
                return

            strategy = self.parent.fit_control.get_current_strategy()

            if mode == "2D" and strategy == "Fit per Y":
                df = self.parent.df
                if df is None or df.empty:
                    return

                x_vals = df["X"].values
                y_vals = df["Y"].values
                z_vals = df["Z"].values

                z_manual = fit_func(x_vals, y_vals, **param_values)
                z_residual = z_vals - z_manual

                self.parent.plot_widget.plot_manual_fit_per_y(fit_func, param_values)

                if self.parent.xy_table.rowCount() < 5:
                    self.parent.xy_table.setRowCount(5)
                    self.parent.xy_table.setVerticalHeaderLabels(
                        ["X", "Y", "Z", "Manual", "Residual"]
                    )

                for col, (z_m, z_r) in enumerate(zip(z_manual, z_residual)):
                    self.parent.xy_table.setItem(3, col, QTableWidgetItem(f"{z_m:.3e}"))
                    self.parent.xy_table.setItem(4, col, QTableWidgetItem(f"{z_r:.3e}"))
            else:
                x_vals = self.parent.plot_widget.data_x
                y_vals = self.parent.plot_widget.data_y
                if x_vals is not None and y_vals is not None:
                    y_manual = fit_func(x_vals, **param_values)
                    y_residual = y_vals - y_manual
                    for col, (y_m, y_r) in enumerate(zip(y_manual, y_residual)):
                        self.parent.xy_table.setItem(
                            2, col, QTableWidgetItem(f"{y_m:.3e}")
                        )
                        self.parent.xy_table.setItem(
                            3, col, QTableWidgetItem(f"{y_r:.3e}")
                        )
                    self.parent.plot_widget.plot_manual_fit(fit_func, param_values)

    def update_slider_value(self, value, param, slider):
        """Handles label update and refresh after slider value changes."""
        min_val = float(self.slider_ranges[slider]["min_box"].text().replace(",", "."))
        max_val = float(self.slider_ranges[slider]["max_box"].text().replace(",", "."))
        if min_val == max_val:
            max_val += 1e-6
        use_log = abs(np.log10(max_val / min_val)) > 3
        if use_log:
            real_val = 10 ** (
                np.log10(min_val)
                + ((value - 1) / 99) * (np.log10(max_val) - np.log10(min_val))
            )
        else:
            real_val = min_val + ((value - 1) / 99) * (max_val - min_val)
        self.param_labels[param].setText(f"{param}: {real_val:.6g}")
        self.update_params_tab_from_manual(param, real_val)
        self.update_manual_plot()

    def update_slider_range(self, param, min_box, max_box, slider, is_min):
        """Updates slider bounds and refreshes display."""
        try:
            min_val = float(min_box.text().replace(",", "."))
            max_val = float(max_box.text().replace(",", "."))
            if min_val == max_val:
                max_val += 1e-6
            slider.setMinimum(1)
            slider.setMaximum(100)
            self.param_labels[param].setText(f"{param}: {min_val:.2g} → {max_val:.2g}")
            self.update_slider_value(slider.value(), param, slider)
        except Exception:
            min_box.setText("1e-4")
            max_box.setText("1e2")

    def toggle_manual_column(self, enable):
        """Adds or removes Manual and Residual rows in the XY table."""
        if enable and self.parent.xy_table.rowCount() == 2:
            self.parent.xy_table.setRowCount(4)
            self.parent.xy_table.setVerticalHeaderLabels(
                ["X", "Y", "Manual", "Residual"]
            )
        elif not enable and self.parent.xy_table.rowCount() == 4:
            self.parent.xy_table.setRowCount(2)
            self.parent.xy_table.setVerticalHeaderLabels(["X", "Y"])

    def update_params_tab_from_manual(self, param, value):
        """Propagates manual parameter values to FitOptionsWindow (p0 field)."""
        if hasattr(self.parent.fit_options_dialog, "params_table"):
            for row in range(self.parent.fit_options_dialog.params_table.rowCount()):
                param_item = self.parent.fit_options_dialog.params_table.item(row, 0)
                if param_item and param_item.text() == param:
                    p0_input = self.parent.fit_options_dialog.params_table.cellWidget(
                        row, 2
                    )
                    if isinstance(p0_input, QLineEdit):
                        p0_input.setText(f"{value:.6g}")
