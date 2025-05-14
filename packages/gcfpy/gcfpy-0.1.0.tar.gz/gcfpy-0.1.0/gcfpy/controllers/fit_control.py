import lmfit
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gcfpy.utils import ConfigManager
from gcfpy.widgets.base_dock import BaseDockWidget
from gcfpy.widgets.plot2d import (
    plot_2d_surface_fit,
    plot_multi1d_data,
    plot_multi1d_fit,
)

from .fit_processor import FitProcessor


class FitControl:
    """
    FitControl panel for launching curve fits.

    Manages the UI controls to run, reset, and configure fits in 1D and 2D,
    dispatches the fitting logic to the appropriate processor,
    and updates the toolbar and result display accordingly.
    """

    def __init__(self, parent, main_window):
        """
        Initialize the FitControl dock and associated logic.

        Args:
            parent (FitTab): The parent FitTab instance.
            main_window (MainWindow): The main application window.

        """
        self.parent = parent
        self.main_window = main_window
        self.fit_report = None

        self.fit_processor = FitProcessor(self.parent.fit_options_dialog)
        self._init_ui()

    def _init_ui(self):
        """Initialize the Fit Control dock and layout."""
        self._create_dock()
        self._create_buttons()
        self._create_strategy_selector()
        self._assemble_layout()

    def _create_dock(self):
        """Create the main dock widget."""
        self.config = ConfigManager()
        max_width = self.config.get("fit_control", "max_width", 400)
        max_height = self.config.get("fit_control", "max_height", 140)

        self.dock_fit = BaseDockWidget("Fit Control", self.parent)
        self.dock_fit.setMaximumSize(max_width, max_height)
        self.dock_fit.setHidden(True)
        self.parent.addDockWidget(Qt.BottomDockWidgetArea, self.dock_fit)

    def _create_buttons(self):
        """Create and connect the Run, Reset, and Manual fit buttons."""
        self.run_fit_button = QPushButton("Run Fit")
        self.reset_fit_button = QPushButton("Reset Fit")
        self.manual_button = QPushButton("Manual")

        self.run_fit_button.clicked.connect(self.run_fit)
        self.reset_fit_button.clicked.connect(self.reset_fit)
        self.manual_button.clicked.connect(
            self.parent.manual_control.toggle_manual_dock
        )

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.run_fit_button)
        self.button_layout.addWidget(self.reset_fit_button)
        self.button_layout.addWidget(self.manual_button)

    def _create_strategy_selector(self):
        """Create the strategy selector for 2D fit modes."""
        self.strategy_label = QLabel("Fit strategy:")
        self.strategy_label.setToolTip(
            "Choose how to fit the 2D data (by Y slices or as surface)."
        )
        self.strategy_selector = QComboBox()
        self.strategy_selector.addItems(["Fit surface", "Fit per Y"])
        self.strategy_selector.currentTextChanged.connect(self._on_strategy_change)

        self.strategy_label.setVisible(False)
        self.strategy_selector.setVisible(False)

        self.strategy_layout = QHBoxLayout()
        self.strategy_layout.addWidget(self.strategy_label)
        self.strategy_layout.addWidget(self.strategy_selector)
        self.strategy_layout.setContentsMargins(5, 0, 5, 0)

    def _assemble_layout(self):
        """Assemble all UI components into the final layout."""
        self.fit_layout = QVBoxLayout()
        self.fit_layout.addLayout(self.button_layout)
        self.fit_layout.addLayout(self.strategy_layout)

        fit_widget = QWidget()
        fit_widget.setLayout(self.fit_layout)
        self.dock_fit.setWidget(fit_widget)

    def _get_selected_or_full_data(self, cols):
        """
        Return selected data if available, otherwise full data from parent.df.

        Args:
            cols (list of str): columns to retrieve, e.g. ["X", "Y"], ["X", "Y", "Z"]

        Returns:
            tuple of np.ndarray: values of the requested columns.

        """
        if "Z" in cols:
            return tuple(self.parent.df[col].values for col in cols)
        else:
            selected = [
                getattr(self.parent.plot_widget, f"selected_{col.lower()}", None)
                for col in cols
            ]
            if all(s is not None for s in selected):
                return tuple(selected)
            else:
                return tuple(self.parent.df[col].values for col in cols)

    def display_fit_results(self):
        """Ensure the fit dock is visible after fitting."""
        self.dock_fit.setVisible(True)

    def reset_fit(self):
        """Reset any existing fit and restore the original plot."""
        self.fit_processor.reset_fit(self.parent.plot_widget, self.main_window)

    def run_fit(self):
        """Execute the fit using the selected method."""
        method = self.parent.fit_options_dialog.get_options().get("method", "leastsq")
        strategy = self.strategy_selector.currentText()

        if self.parent.current_mode == "2D" and strategy.startswith("Fit per Y"):
            self._run_fit_per_y(method)
        elif self.parent.current_mode == "2D" and strategy.startswith("Fit surface"):
            self._run_fit_surface(method)
        else:
            self._run_fit_process(method)  # for standard 1D

    def get_formula_or_warn(self):
        """Extract the formula text or show a warning if missing."""
        formula = self.parent.formula_text.toPlainText().strip()
        if not formula:
            QMessageBox.warning(self.parent, "Error", "No fitting formula provided.")
            return None
        return formula

    def _generate_fit_report(self, result, method):
        """Generate the fit report based on the method used."""
        if method == "emcee":
            return self._format_emcee_report(result)
        elif method == "odr":
            return self._format_odr_report(result)
        else:
            return lmfit.fit_report(result, show_correl=True)

    def _handle_fit_result(
        self,
        result,
        minimizer,
        best_fit,
        confidence_band,
        method,
        strategy="1D",
    ):
        """
        Store result, update UI, and manage toolbar depending on the method.

        Args:
            result: Fit result.
            minimizer: Fitting engine instance.
            best_fit: Fitted Y or Z values.
            confidence_band: Confidence intervals.
            method: Fit method ("lmfit", "odr", "emcee").
            strategy : "1D", "multi 1D", "2D"

        """
        self.parent.plot_widget.store_fit_result(
            result, minimizer, confidence_band, best_fit
        )
        self.fit_report = self._generate_fit_report(result, method)
        self.parent.update_results_text(self.fit_report)
        self.display_fit_results()

        self.main_window.toolbar.enable_toolbar_options(False)
        self.main_window.toolbar.enable_comparison(True)

        if method == "emcee":
            self.main_window.enable_toolbar_buttons(False)
            self.parent.plot_widget.mcmc_plot.show_mcmc_results(result, confidence_band)
        elif strategy == "2D":
            self.main_window.enable_toolbar_buttons(False)
        elif strategy == "multi 1D":
            self.main_window.enable_toolbar_buttons(True)
            self.main_window.toolbar.toggle_components_action.setEnabled(False)
            if method == "odr":
                self.main_window.toolbar.toggle_confidence_2d_action.setEnabled(False)
        else:
            self.main_window.enable_toolbar_buttons(True)
            if method == "odr":
                self.main_window.toolbar.toggle_confidence_2d_action.setEnabled(False)

    def _run_fit_process(self, method):
        """
        Performs a 1D fit Y = f(X) using lmfit, odr, or emcee.
        """
        x, y = self._get_selected_or_full_data(["X", "Y"])
        if x is None or y is None:
            QMessageBox.warning(self.parent, "Error", "No data available for fitting.")
            return

        formula = self.get_formula_or_warn()
        if formula is None:
            return

        weights = getattr(self.parent.plot_widget, "weights", None)
        wm = self.parent.plot_widget.weighting_method

        try:
            result, minimizer, best_fit, confidence_band = (
                self.fit_processor.process_fit(formula, x, y, weights, wm)
            )
        except (ValueError, RuntimeError) as e:
            QMessageBox.warning(self.parent, "Error", str(e))
            return

        if best_fit is not None:
            self.parent.plot_widget.plot_fit(x, best_fit)

        self._handle_fit_result(
            result, minimizer, best_fit, confidence_band, method, strategy="1D"
        )

    def _run_fit_surface(self, method):
        """
        Performs a 2D surface fit Z = f(X, Y) using lmfit, odr, or emcee.
        """
        x, y, z = self._get_selected_or_full_data(["X", "Y", "Z"])
        if x is None or y is None or z is None:
            QMessageBox.warning(
                self.parent,
                "Error",
                "Missing X, Y or Z data for 2D surface fit.",
            )
            return

        formula = self.get_formula_or_warn()
        if formula is None:
            return

        weights = getattr(self.parent.plot_widget, "weights", None)
        fit_function = self.fit_processor.generate_fit_function(formula)

        if method == "odr":
            result, minimizer, best_fit, confidence_band = (
                self.fit_processor.process_fit_surface_odr(
                    formula, fit_function, x, y, z, weights
                )
            )
        elif method == "emcee":
            result, minimizer, best_fit, confidence_band = (
                self.fit_processor.process_fit_surface_emcee(
                    formula, fit_function, x, y, z, weights
                )
            )
        else:
            result, minimizer, best_fit, confidence_band = (
                self.fit_processor.process_fit_surface(
                    formula, fit_function, x, y, z, weights
                )
            )

        self.parent.plot_widget.tab_manager.ensure_tab_exists(
            "2D Surface", "fig_surface", "ax_surface", "canvas_surface"
        )
        plot_2d_surface_fit(
            self.parent.plot_widget.ax_surface,
            self.parent.plot_widget.canvas_surface,
            x,
            y,
            z,
            best_fit,
            self.parent.plot_widget,
        )

        self._handle_fit_result(
            result, minimizer, best_fit, confidence_band, method, strategy="2D"
        )

    def _run_fit_per_y(self, method):
        """
        Performs a global multi-1D fit Z = f(X, Y_fixed) across all Y slices.
        """
        x, y, z = self._get_selected_or_full_data(["X", "Y", "Z"])
        if x is None or y is None or z is None:
            QMessageBox.warning(self.parent, "Error", "No data available for fitting.")
            return

        formula = self.get_formula_or_warn()
        if formula is None:
            return

        weights = getattr(self.parent.plot_widget, "weights", None)
        wm = self.parent.plot_widget.weighting_method

        if method == "odr":
            result, minimizer, best_fit, confidence_band = (
                self.fit_processor.process_fit_per_y_odr(formula, x, y, z, weights, wm)
            )
        elif method == "emcee":
            result, minimizer, best_fit, confidence_band = (
                self.fit_processor.process_fit_per_y_emcee(
                    formula, x, y, z, weights, wm
                )
            )
        else:
            result, minimizer, best_fit, confidence_band = (
                self.fit_processor.process_fit_per_y(formula, x, y, z, weights, wm)
            )

        fits = [(x[y == val], best_fit[y == val], val) for val in np.unique(y)]

        self.parent.plot_widget.tab_manager.ensure_tab_exists(
            "Multi 1D", "fig_multi1d", "ax_multi1d", "canvas_multi1d"
        )
        plot_multi1d_data(
            self.parent.plot_widget.ax_multi1d,
            self.parent.plot_widget.canvas_multi1d,
            x,
            y,
            z,
            self.parent.plot_widget,
        )
        plot_multi1d_fit(
            self.parent.plot_widget.ax_multi1d,
            self.parent.plot_widget.canvas_multi1d,
            fits,
            self.parent.plot_widget,
        )

        self._handle_fit_result(
            result, minimizer, best_fit, confidence_band, method, strategy="multi 1D"
        )

    def _format_emcee_report(self, result):
        """
        Generate a textual summary report for emcee fit results.

        Args:
            result (dict): Result dictionary returned by process_emcee().

        Returns:
            str: Formatted summary report.

        """
        lines = []
        lines.append("[[Fit Statistics]]")
        lines.append("    # fitting method   = MCMC (emcee)")
        lines.append(f"    # chain shape      = {result['chain'].shape}")
        lines.append(f"    # total samples    = {len(result['samples'])}")
        lines.append("")

        lines.append("[[Variables (median ± std)]]")

        param_names = list(result["params"].keys())
        samples = result["samples"]
        param_stats = {}

        for i, name in enumerate(param_names):
            values = samples[:, i]
            median = np.median(values)
            std = np.std(values)
            param_stats[name] = (median, std)

            rel_err = abs(std / median) * 100 if median != 0 else np.nan
            lines.append(f"    {name}: {median:.6g} +/- {std:.2g} ({rel_err:.2f}%)")

        lines.append("")

        # Optional: Correlations
        if len(param_names) > 1:
            lines.append("[[Correlations]] (Pearson, sample-based)")
            for i in range(len(param_names)):
                for j in range(i + 1, len(param_names)):
                    xi = samples[:, i]
                    xj = samples[:, j]
                    corr = np.corrcoef(xi, xj)[0, 1]
                    if abs(corr) > 0.1:
                        lines.append(
                            f"    C({param_names[i]}, {param_names[j]}) = {corr:.4f}"
                        )

        return "\n".join(lines)

    def _format_odr_report(self, result):
        """
        Generate a textual summary report of ODR fit results,
        mimicking the style of lmfit's fit_report.

        Args:
            result (dict): Result dictionary returned by process_odr().

        Returns:
            str: Formatted summary report.

        """
        lines = []
        lines.append("[[Fit Statistics]]")
        lines.append("    # fitting method   = ODR")
        lines.append(f"    # data points      = {result['fit_stats']['n_points']}")
        lines.append(f"    # variables        = {result['fit_stats']['n_params']}")
        lines.append(f"    sum squared error = {result['fit_stats']['sum_sq']:.6g}")
        lines.append(
            f"    reduced chi-square = {result['fit_stats']['reduced_chi2']:.6g}"
        )
        lines.append(f"    Akaike info crit   = {result['fit_stats']['aic']:.6g}")
        lines.append(f"    Bayesian info crit = {result['fit_stats']['bic']:.6g}")
        lines.append("")

        lines.append("[[Variables]]")
        for name in result["params"]:
            value = result["params"][name]
            stderr = result["stderr"].get(name, np.nan)
            rel_err = abs(stderr / value) * 100 if value != 0 else np.nan
            lines.append(f"    {name}: {value:.6g} +/- {stderr:.2g} ({rel_err:.2f}%)")
        lines.append("")

        # Optional: Display correlation matrix if cov available
        if "covariance" in result and result["covariance"] is not None:
            cov = result["covariance"]
            param_names = list(result["params"].keys())
            lines.append("[[Correlations]] (unreported correlations are < 0.100)")
            for i in range(len(param_names)):
                for j in range(i + 1, len(param_names)):
                    corr = cov[i, j] / (np.sqrt(cov[i, i] * cov[j, j]) + 1e-12)
                    if abs(corr) >= 0.1:
                        lines.append(
                            f"    C({param_names[i]}, {param_names[j]}) = {corr:.4f}"
                        )

        return "\n".join(lines)

    def update_strategy_selector(self, visible):
        """
        Show or hide the strategy selection dropdown for 2D fitting.

        Args:
            visible (bool): Whether to show or hide the selector.

        """
        self.strategy_label.setVisible(visible)
        self.strategy_selector.setVisible(visible)

    def get_current_strategy(self):
        """
        Return the selected 2D fit strategy.

        Returns:
            str: "Fit per Y" or "Fit surface"

        """
        return self.strategy_selector.currentText()

    def _on_strategy_change(self, strategy):
        """
        Triggered when the 2D fitting strategy changes.
        Updates plot visibility and re-displays data accordingly.

        Args:
            strategy (str): Selected strategy, e.g., "Fit per Y" or "Fit surface".

        """

        if self.parent.current_mode != "2D":
            return

        self.parent.plot_widget.update_plot_visibility("2D", strategy)

        df = self.parent.df
        if df is not None and all(col in df.columns for col in ("X", "Y", "Z")):
            x, y, z = df["X"].values, df["Y"].values, df["Z"].values
            self.parent.plot_widget.plot_2d_series(x, y, z, strategy)
