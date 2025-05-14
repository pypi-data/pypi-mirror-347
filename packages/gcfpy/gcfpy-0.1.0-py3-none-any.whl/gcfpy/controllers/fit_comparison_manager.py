import csv
from collections import namedtuple

import numpy as np
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from gcfpy.widgets import BaseDockWidget

from .formula_tools import parse_formula


class FitComparisonManager:
    """
    Manage the storage and comparison of multiple fit results.
    """

    def __init__(self, fit_tab):
        """
        Initialize the FitComparisonManager.

        Args:
            fit_tab (FitTab): The parent tab that contains data and UI references.

        """
        self.fit_tab = fit_tab
        self.stored_fits = []
        self.comparison_mode = False

        self.comparison_plot = None
        self.comparison_table = None
        self.dock_comparison = None
        self.fit_list = None
        self.fig = None
        self.ax = None

        self.parameter_table = None
        self.fit_names = []
        self.multi1d_results = []

    def store_current_fit(self):
        """
        Store the current fit result and its parameters, including multi-1D support.
        """
        result = self.fit_tab.plot_widget.result
        method = self.fit_tab.fit_options.get("method", "leastsq")
        strategy = self.fit_tab.fit_control.get_current_strategy()
        formula = self.fit_tab.formula_text.toPlainText()

        if result is None:
            print("No fit to store.")
            return

        is_lmfit = hasattr(result, "params") and hasattr(result, "chisqr")

        if strategy == "Fit per Y":
            residual = (
                getattr(result, "residual", None)
                if is_lmfit
                else result.get("residual")
            )
            z_data = getattr(self.fit_tab.plot_widget, "data_z", None)
            if residual is not None and z_data is not None:
                residual = np.asarray(residual).flatten()
                z_data = np.asarray(z_data).flatten()
                rmse = np.sqrt(np.mean(residual**2))
                r2 = (
                    1 - (np.var(residual) / np.var(z_data))
                    if np.var(z_data) > 0
                    else None
                )
            else:
                rmse, r2 = None, None
        else:
            residual = (
                getattr(result, "residual", None)
                if is_lmfit
                else result.get("residual")
            )
            y_data = self.fit_tab.plot_widget.data_y
            y_var = np.var(y_data) if y_data is not None else None
            rmse = np.sqrt(np.mean(residual**2)) if residual is not None else None
            r2 = (
                1 - (np.var(residual) / y_var)
                if residual is not None and y_var
                else None
            )

        if is_lmfit:
            params = result.params
            aic = result.aic
            bic = result.bic
            chisqr = result.chisqr
            redchi = result.redchi
        else:
            Param = namedtuple("Param", ["value", "stderr"])

            class ParamsContainer:
                def __init__(self, values_dict, stderr_dict):
                    self._values = values_dict
                    self._stderr = stderr_dict

                def valuesdict(self):
                    return self._values

                def __getitem__(self, key):
                    return Param(
                        self._values.get(key, None),
                        self._stderr.get(key, None),
                    )

                def __iter__(self):
                    return iter(self._values)

            params = ParamsContainer(result["params"], result.get("stderr", {}))
            aic = result.get("aic", None)
            bic = result.get("bic", None)
            chisqr = result.get("sum_square", None)
            redchi = result.get("redchi", result.get("reduced_chi2", None))

        fit_data = {
            "formula": formula,
            "method": method,
            "params": params,
            "aic": aic,
            "bic": bic,
            "rmse": rmse,
            "r_squared": r2,
            "chi_square": chisqr,
            "reduced_chi_square": redchi,
        }

        self.stored_fits.append(fit_data)
        self.fit_names.append(f"Fit {len(self.fit_names) + 1}")
        print(f"Fit stored: {formula} using {method}")

    def toggle_comparison_mode(self, enabled):
        """
        Toggle the comparison mode on or off.

        Args:
            enabled (bool): Whether to activate or deactivate the mode.

        """
        self.comparison_mode = enabled
        if enabled:
            self.activate_comparison_mode()
        else:
            self.deactivate_comparison_mode()

    def activate_comparison_mode(self):
        """Switch UI to comparison mode, hiding unnecessary docks."""
        self.fit_tab.dock_formula.setVisible(False)
        self.fit_tab.dock_xy.setVisible(False)
        self.fit_tab.fit_control.dock_fit.setVisible(False)
        if hasattr(self.fit_tab.manual_control, "dock_manual"):
            self.fit_tab.manual_control.dock_manual.setVisible(False)
        self.fit_tab.dock_plot.setVisible(False)
        self.fit_tab.dock_results.setVisible(False)

        self.create_comparison_ui()

    def deactivate_comparison_mode(self):
        """Restore normal UI after exiting comparison mode."""
        self.fit_tab.dock_formula.setVisible(True)
        self.fit_tab.dock_xy.setVisible(True)
        self.fit_tab.fit_control.dock_fit.setVisible(True)
        self.fit_tab.dock_plot.setVisible(True)
        self.fit_tab.dock_results.setVisible(True)

        if self.dock_comparison:
            self.fit_tab.removeDockWidget(self.dock_comparison)
            self.dock_comparison = None

    def create_comparison_ui(self):
        """
        Create a new dock with a plot, fit selection list, and table for comparing fits.
        """
        if self.dock_comparison is None:
            self.dock_comparison = BaseDockWidget("Fit Comparison", self.fit_tab)
            comparison_widget = QWidget()
            layout = QVBoxLayout()

            self.comparison_plot = self.create_comparison_plot()
            self.matplotlib_toolbar = NavigationToolbar(
                self.comparison_plot, self.fit_tab
            )
            self.fit_list = self.create_fit_list()
            self.comparison_table = self.create_comparison_table()
            # self.parameter_table = self.create_parameter_table()

            layout.addWidget(self.matplotlib_toolbar)
            layout.addWidget(self.comparison_plot)
            layout.addWidget(self.fit_list)
            layout.addWidget(self.comparison_table)
            # layout.addWidget(self.parameter_table)

            comparison_widget.setLayout(layout)
            self.dock_comparison.setWidget(comparison_widget)

            self.fit_tab.addDockWidget(Qt.TopDockWidgetArea, self.dock_comparison)

            self.redraw_comparison_plot()
            export_button = QPushButton("Export Comparison CSV")
            export_button.clicked.connect(self.export_comparison_csv)
            layout.addWidget(export_button)

    def create_comparison_plot(self):
        """Generate a plot comparing all stored fits."""
        self.fig = Figure(figsize=(7, 4))
        self.ax = self.fig.add_subplot(111)

        mode = getattr(self.fit_tab, "current_mode", "1D")
        strategy = self.fit_tab.fit_control.get_current_strategy()

        if mode == "2D" and strategy == "Fit per Y":
            df = self.fit_tab.df
            if df is not None:
                self.ax.scatter(df["X"], df["Z"], color="blue", s=10, label="Data")
                self.ax.set_xlabel("X")
                self.ax.set_ylabel("Z")
        else:
            x = self.fit_tab.plot_widget.data_x
            y = self.fit_tab.plot_widget.data_y
            if x is not None and y is not None:
                self.ax.scatter(x, y, color="blue", label="Data")
                x_margin = 0.1 * (x.max() - x.min())
                y_margin = 0.1 * (y.max() - y.min())
                self.ax.set_xlim(x.min() - x_margin, x.max() + x_margin)
                self.ax.set_ylim(y.min() - y_margin, y.max() + y_margin)

        self.ax.legend()
        self.comparison_plot = FigureCanvas(self.fig)
        return self.comparison_plot

    def redraw_comparison_plot(self):
        """Redraws the comparison plot based on selected fits."""
        if self.comparison_plot is None or self.ax is None:
            print("Warning: `comparison_plot` is not initialized.")
            return

        self.ax.clear()

        mode = getattr(self.fit_tab, "current_mode", "1D")
        strategy = self.fit_tab.fit_control.get_current_strategy()
        colors = ["red", "green", "purple", "orange", "brown", "cyan"]

        if mode == "2D" and strategy == "Fit per Y":
            df = self.fit_tab.df
            if df is None:
                return

            self.ax.scatter(df["X"], df["Z"], color="blue", s=10, label="Data")

            unique_y = np.unique(df["Y"])
            for i, fit in enumerate(self.stored_fits):
                item = self.fit_list.item(i)
                if not item or item.checkState() != Qt.Checked:
                    continue

                params = fit["params"]
                p_dict = (
                    params.valuesdict() if hasattr(params, "valuesdict") else params
                )
                parsed_formula = parse_formula(fit["formula"])
                fit_func = eval(
                    "lambda x, y, " + ", ".join(p_dict.keys()) + ": " + parsed_formula,
                    {"np": np},
                )

                for y_val in unique_y:
                    x_vals = df[df["Y"] == y_val]["X"].values
                    z_fit = fit_func(x_vals, y_val, **p_dict)
                    self.ax.plot(
                        x_vals,
                        z_fit,
                        linestyle="--",
                        color=colors[i % len(colors)],
                        alpha=0.7,
                        linewidth=2,
                        # label=f"{self.fit_names[i]} @ Y={y_val:.2f}",
                    )
        else:
            x = self.fit_tab.plot_widget.data_x
            y = self.fit_tab.plot_widget.data_y
            self.ax.scatter(x, y, color="blue", label="Data")

            for i, fit in enumerate(self.stored_fits):
                item = self.fit_list.item(i)
                if not item or item.checkState() != Qt.Checked:
                    continue

                x_values = np.linspace(x.min(), x.max(), 200)
                params = fit["params"]
                p_dict = (
                    params.valuesdict() if hasattr(params, "valuesdict") else params
                )
                parsed_formula = parse_formula(fit["formula"])
                fit_func = eval(
                    "lambda x, " + ", ".join(p_dict.keys()) + ": " + parsed_formula,
                    {"np": np},
                )
                y_fit = fit_func(x_values, **p_dict)

                self.ax.plot(
                    x_values,
                    y_fit,
                    linestyle="--",
                    color=colors[i % len(colors)],
                    linewidth=2,
                    label=self.fit_names[i],
                )

        self.ax.legend()
        self.comparison_plot.draw()

    def create_comparison_table(self):
        """Generate a unified table: parameters + metrics in a single row per fit."""
        if not self.stored_fits:
            return QTableWidget(0, 0)

        # Collect all parameter names
        param_names = set()
        for fit in self.stored_fits:
            p = fit["params"]
            param_dict = p.valuesdict() if hasattr(p, "valuesdict") else p
            param_names.update(param_dict.keys())
        param_names = sorted(param_names)

        metric_names = ["AIC", "BIC", "RMSE", "Chi²", "R²"]
        header_labels = ["Name", "Formula", "Method", *param_names, *metric_names]

        table = QTableWidget(len(self.stored_fits), len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        for i, fit in enumerate(self.stored_fits):
            name = self.fit_names[i] if i < len(self.fit_names) else f"Fit {i + 1}"
            table.setItem(i, 0, QTableWidgetItem(name))
            table.setItem(i, 1, QTableWidgetItem(fit.get("formula", "—")))
            table.setItem(i, 2, QTableWidgetItem(fit.get("method", "—")))

            p = fit["params"]
            if hasattr(p, "valuesdict"):
                values = p.valuesdict()
                errors = {k: p[k].stderr for k in p}
            else:
                values = p
                errors = {}

            for j, param in enumerate(param_names):
                val = values.get(param)
                err = errors.get(param)
                if val is not None:
                    txt = f"{val:.4g}"
                    if err:
                        txt += f" ± {err:.2g}"
                else:
                    txt = "—"
                table.setItem(i, 3 + j, QTableWidgetItem(txt))

            score_values = [
                fit.get("aic"),
                fit.get("bic"),
                fit.get("rmse"),
                fit.get("chi_square"),
                fit.get("r_squared"),
            ]

            for k, score in enumerate(score_values):
                col_idx = 3 + len(param_names) + k
                table.setItem(
                    i,
                    col_idx,
                    QTableWidgetItem(f"{score:.3f}" if score is not None else "—"),
                )

        table.resizeColumnsToContents()
        return table

    def create_fit_list(self):
        """
        Create a list widget to display stored fits.

        Returns:
            QListWidget: The populated list of fits.

        """
        fit_list = QListWidget()

        for i, fit in enumerate(self.stored_fits):
            default_name = f"Fit {i + 1}"
            self.fit_names.append(default_name)
            item = QListWidgetItem(default_name + f": {fit['formula']}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            item.setCheckState(Qt.Checked)
            fit_list.addItem(item)

        fit_list.itemChanged.connect(self.handle_fit_list_change)
        return fit_list

    def handle_fit_list_change(self, item):
        """
        Update names and plots when a fit list item is edited or checked/unchecked.

        Args:
            item (QListWidgetItem): The item that was changed.

        """
        index = self.fit_list.row(item)
        name = item.text().split(":")[0].strip()
        self.fit_names[index] = name
        self.redraw_comparison_plot()
        self.update_parameter_table()
        self.update_comparison_table()

    def update_parameter_table(self):
        """
        Refresh the parameter table after a change in fit selection or name.
        """
        if not self.parameter_table:
            return
        self.dock_comparison.layout().removeWidget(self.parameter_table)
        self.parameter_table.setParent(None)
        self.parameter_table = self.create_parameter_table()
        self.dock_comparison.widget().layout().addWidget(self.parameter_table)

    def update_comparison_table(self):
        """
        Refresh the main comparison table after a change in fit selection or name.
        """
        if not self.comparison_table:
            return
        self.dock_comparison.layout().removeWidget(self.comparison_table)
        self.comparison_table.setParent(None)
        self.comparison_table = self.create_comparison_table()
        self.dock_comparison.widget().layout().addWidget(self.comparison_table)

    def create_parameter_table(self):
        """Generate a table displaying fitted parameters and their uncertainties."""
        # Not sure about this table
        if not self.stored_fits:
            return QTableWidget(0, 0)

        param_names = set()
        for fit in self.stored_fits:
            p = fit["params"]
            param_dict = p.valuesdict() if hasattr(p, "valuesdict") else p
            param_names.update(param_dict.keys())
        param_names = sorted(param_names)

        table = QTableWidget(len(param_names), len(self.stored_fits))
        table.setVerticalHeaderLabels(param_names)
        table.setHorizontalHeaderLabels(self.fit_names)

        for j, fit in enumerate(self.stored_fits):
            p = fit["params"]
            if hasattr(p, "valuesdict"):
                values = p.valuesdict()
                errors = {k: p[k].stderr for k in p}
            else:
                values = p
                errors = {}

            for i, param in enumerate(param_names):
                val = values.get(param)
                err = errors.get(param)
                if val is not None:
                    text = f"{val:.4g}"
                    if err:
                        text += f" ± {err:.2g}"
                else:
                    text = "—"
                table.setItem(i, j, QTableWidgetItem(text))

        table.resizeColumnsToContents()
        return table

    def export_comparison_csv(self):
        """
        Export stored fit comparisons into a CSV file.
        """
        if not self.stored_fits:
            print("No fits to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self.fit_tab,
            "Save Comparison CSV",
            "fit_comparison.csv",
            "CSV Files (*.csv)",
        )
        if not path:
            return

        param_names = set()
        for fit in self.stored_fits:
            p = fit["params"]
            param_dict = p.valuesdict() if hasattr(p, "valuesdict") else p
            param_names.update(param_dict.keys())
        param_names = sorted(param_names)

        with open(path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            header = [
                "Name",
                "Formula",
                "Method",
                "Data Path",
                *param_names,
                "AIC",
                "BIC",
                "RMSE",
                "Chi²",
                "R²",
            ]
            writer.writerow(header)

            for i, fit in enumerate(self.stored_fits):
                name = self.fit_names[i] if i < len(self.fit_names) else f"Fit {i + 1}"
                formula = fit.get("formula", "")
                method = fit.get("method", "")
                data_path = getattr(self.fit_tab, "data_path", "N/A")

                p = fit["params"]
                if hasattr(p, "valuesdict"):
                    values = p.valuesdict()
                    errors = {k: p[k].stderr for k in p}
                else:
                    values = p
                    errors = {}

                param_cells = []
                for key in param_names:
                    val = values.get(key)
                    err = errors.get(key)
                    if val is not None:
                        s = f"{val:.4g}"
                        if err:
                            s += f" ± {err:.2g}"
                    else:
                        s = ""
                    param_cells.append(s)

                scores = [
                    fit.get("aic"),
                    fit.get("bic"),
                    fit.get("rmse"),
                    fit.get("chi_square"),
                    fit.get("r_squared"),
                ]
                score_cells = [f"{s:.4g}" if s is not None else "" for s in scores]

                row = [name, formula, method, data_path, *param_cells, *score_cells]
                writer.writerow(row)

        print(f"Exported comparison to: {path}")

    def reset(self):
        """Clear all stored fits and reset internal state."""
        self.stored_fits.clear()
        self.fit_names.clear()
        self.multi1d_results.clear()

        self.comparison_plot = None
        self.comparison_table = None
        self.dock_comparison = None
        self.fit_list = None
        self.fig = None
        self.ax = None
        self.parameter_table = None
        self.comparison_mode = False
