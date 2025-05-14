import numpy as np
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar,
)
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from gcfpy.widgets.mcmc_plot import MCMCPlot
from gcfpy.widgets.plot2d import (
    plot_2d_series,
    plot_2d_surface,
    plot_multi1d_data,
    plot_multi1d_fit,
)
from gcfpy.widgets.plot_analysis import PlotAnalysis
from gcfpy.widgets.tab_manager import TabManager
from gcfpy.widgets.xmin_xmax import PlotXminXmax


class PlotWidget(QWidget):
    """
    Manages the main plotting interface, handling data visualization, fit plots,
    confidence bands, residuals, and interactive selections.
    """

    def __init__(self, parent=None):
        """
        Initializes the plotting widget.

        Args:
            parent (QWidget, optional): The parent widget.

        """
        super().__init__(parent)
        self.parent = parent

        self.data_x = None
        self.data_y = None
        self.x_err = None
        self.y_err = None
        self.fit_y = None
        self.weighting_method = None
        self.original_y = None
        self.confidence_band = None
        self.result = None
        self.components = {}

        self.show_confidence = False
        self.show_residuals = False
        self.show_components = False

        self.xmin_xmax_tool = PlotXminXmax(self)
        self.mcmc_plot = MCMCPlot(self)
        self.analysis_plot = PlotAnalysis(self)
        self.tab_manager = TabManager(self)

        self.cursor_event = None

        self.mcmc_chains = None
        self.mcmc_params = None

        self.initUI()

        self.tab_manager.add_matplotlib_canvas()

    def initUI(self):
        """Initializes the user interface by setting up the layout and tab manager."""
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tab_manager.tabs)

    def plot_data(self, df):
        """
        Plots the raw data.

        Args:
            df (pandas.DataFrame): Dataframe containing X and Y values.

        """
        if hasattr(self.parent, "manual_control") and self.parent.manual_control:
            if not self.parent.manual_control.dock_manual.isHidden():
                print("[DEBUG] Manual dock is open, closing it.")
                self.parent.manual_control.toggle_manual_dock()

        self.tab_manager.ensure_tab_exists("Data + Fit", "fig", "ax", "canvas")
        self.tab_manager.switch_to_tab("Data + Fit")
        if df is None or df.empty:
            return

        self.data_x = df["X"].values
        self.data_y = df["Y"].values
        self.x_err = df["X_err"].values if "X_err" in df else None
        self.y_err = df["Y_err"].values if "Y_err" in df else None
        if self.original_y is None:
            self.original_y = self.data_y.copy()

        self.ax.clear()
        if self.y_err is not None or self.x_err is not None:
            self.ax.errorbar(
                self.data_x,
                self.data_y,
                yerr=self.y_err,
                xerr=self.x_err,
                fmt="o",
                color="blue",
                label="Data",
            )
        else:
            self.ax.plot(
                self.data_x,
                self.data_y,
                marker="o",
                linestyle="-",
                color="blue",
                label="Data",
            )

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.legend()
        self.fig.tight_layout()
        self.canvas.draw()

    def plot_fit(self, fit_x, fit_y):
        """
        Plots the fitted curve along with the raw data.

        Args:
            fit_x (numpy.ndarray): X values of the fitted curve.
            fit_y (numpy.ndarray): Y values of the fitted curve.

        """
        if fit_y is None:
            print("Error: No fit has been performed.")
            return
        self.tab_manager.switch_to_tab("Data + Fit")
        self.ax.clear()
        if self.y_err is not None or self.x_err is not None:
            self.ax.errorbar(
                self.data_x,
                self.data_y,
                yerr=self.y_err,
                xerr=self.x_err,
                fmt="o",
                color="blue",
                label="Data",
            )
        else:
            self.ax.plot(
                self.data_x,
                self.data_y,
                marker="o",
                linestyle="-",
                color="blue",
                label="Data",
            )

        self.ax.plot(fit_x, fit_y, linestyle="--", color="red", label="Fit")

        if self.show_components and self.components:
            for name, comp_y in self.components.items():
                self.ax.plot(self.data_x, comp_y, linestyle="--", label=name)

        self.ax.legend()
        self.fig.tight_layout()
        self.canvas.draw()

    def store_fit_result(
        self,
        result,
        minimizer,
        confidence_band,
        best_fit,
        mcmc_chains=None,
        mcmc_params=None,
    ):
        """
        Stores the fit results and associated confidence intervals.

        Args:
            result (lmfit.MinimizerResult): The result object from the fit.
            minimizer (lmfit.Minimizer): The optimizer used for fitting.
            confidence_band (numpy.ndarray): The computed confidence band.
            best_fit (numpy.ndarray): The fitted Y values.
            mcmc_chains (numpy.ndarray, optional): MCMC sample chains.
            mcmc_params (list, optional): Names of the fitted parameters.

        """
        self.result = result
        self.minimizer = minimizer
        self.confidence_band = confidence_band
        self.mcmc_chains = mcmc_chains
        self.mcmc_params = mcmc_params

        current_tab = self.parent.get_current_fit_tab()
        is_emcee = current_tab.fit_options_dialog.get_options()["method"] == "emcee"

        if is_emcee:
            # self.mcmc_plot.plot_mcmc_results()
            return

        if best_fit is not None:
            self.fit_y = best_fit
        else:
            print("Warning: No best fit calculated.")
            return

    def plot_manual_fit(self, fit_function, param_values):
        """
        Displays the updated fit curve with manually adjusted parameters.

        Args:
            fit_function (callable): The function representing the model.
            param_values (dict): The parameter values to use.

        """
        if self.data_x is None or self.data_y is None:
            print("No data loaded, cannot display manual fit.")
            return

        y_manual = fit_function(self.data_x, **param_values)

        self.ax.clear()
        self.ax.plot(self.data_x, self.data_y, "o", color="blue", label="Data")
        self.ax.plot(self.data_x, y_manual, "--", color="green", label="Manual Fit")

        self.ax.legend()
        self.canvas.draw()

    def plot_manual_fit_per_y(self, fit_function, param_values):
        """
        Plots the manually adjusted fit curves Z = f(X) for each fixed Y.
        """
        if self.parent.get_current_fit_tab().df is None:
            print("Missing data for manual fit.")
            return

        df = self.parent.get_current_fit_tab().df
        x = df["X"].values
        y = df["Y"].values

        try:
            z_manual = fit_function(x, y, **param_values)
        except Exception as e:
            print(f"[Manual Fit Error] {e}")
            return

        self.tab_manager.ensure_tab_exists(
            "Multi 1D", "fig_multi1d", "ax_multi1d", "canvas_multi1d"
        )

        ax = self.ax_multi1d
        ax.clear()

        plot_multi1d_data(ax, self.canvas_multi1d, x, y, df["Z"].values, self)

        fits = []
        for y_val in np.unique(y):
            mask = y == y_val
            fits.append((x[mask], z_manual[mask], y_val))
        plot_multi1d_fit(ax, self.canvas_multi1d, fits, self)

    def add_matplotlib_toolbar(self, canvas, layout):
        """
        Adds a Matplotlib toolbar for interactive navigation.

        Args:
            canvas (FigureCanvas): The Matplotlib canvas.
            layout (QVBoxLayout): The layout to add the toolbar to.

        """
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, NavigationToolbar):
                return

        toolbar = NavigationToolbar(canvas, self)
        layout.addWidget(toolbar)

    def plot_2d_series(self, x, y, z, strategy):
        """
        Show both 2D scatter and 3D surface for Z = f(X, Y).
        """

        if "surface" in strategy:
            self.tab_manager.ensure_tab_exists(
                "2D Surface", "fig_surface", "ax_surface", "canvas_surface"
            )
            self.tab_manager.switch_to_tab("2D Surface")
            plot_2d_surface(self.ax_surface, self.canvas_surface, x, y, z, self)
        else:
            self.tab_manager.ensure_tab_exists(
                "Multi 1D", "fig_multi1d", "ax_multi1d", "canvas_multi1d"
            )
            plot_2d_series(self.ax_multi1d, self.canvas_multi1d, x, y, z, self)

    def update_plot_visibility(self, mode, strategy=None):
        """
        Show/hide relevant plots based on current fit mode and strategy.

        Args:
            mode (str): "1D" or "2D"
            strategy (str or None): "Fit per Y" or "Fit surface" (only for 2D)

        """
        if mode == "1D":
            required_tabs = ["Data + Fit"]
            self.tab_manager.remove_all_tabs_except(required_tabs)
            self.tab_manager.switch_to_tab("Data + Fit")

        elif mode == "2D":
            required_tabs = ["Multi 1D"]
            if strategy == "Fit surface":
                required_tabs = ["2D Scatter"]
                required_tabs.append("2D Surface")
            self.tab_manager.remove_all_tabs_except(required_tabs)
            self.tab_manager.switch_to_tab(required_tabs[0])
