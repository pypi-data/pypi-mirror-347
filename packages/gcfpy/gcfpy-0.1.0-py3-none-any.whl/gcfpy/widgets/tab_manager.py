import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
)
from PyQt5.QtWidgets import QScrollArea, QTabWidget, QVBoxLayout, QWidget


class TabManager:
    """Handles tab creation and switching for PlotWidget."""

    def __init__(self, plot_widget):
        """
        Initializes the tab manager.

        Args:
            plot_widget (PlotWidget): The main plot widget instance.

        """
        self.plot_widget = plot_widget
        self.tabs = QTabWidget()

    def add_matplotlib_canvas(self):
        """Adds the main Matplotlib canvas in a new tab."""

        fig_fit, ax_fit = plt.subplots()
        fig_fit.set_size_inches(7, 5, forward=False)

        canvas_fit = FigureCanvas(fig_fit)
        canvas_fit.setMinimumSize(50, 50)
        fit_tab = QWidget()
        fit_layout = QVBoxLayout()
        fit_tab.setLayout(fit_layout)

        self.tabs.addTab(fit_tab, "Data + Fit")
        setattr(self.plot_widget, "data_fit_tab", fit_tab)

        # Attach references back to plot_widget
        self.plot_widget.fig = fig_fit
        self.plot_widget.ax = ax_fit
        self.plot_widget.canvas = canvas_fit

        ax_fit.set_xticks([])
        ax_fit.set_yticks([])
        ax_fit.set_xlabel("X")
        ax_fit.set_ylabel("Y")
        ax_fit.set_title("Waiting for Data...")
        ax_fit.grid(True, linestyle="--", alpha=0.6)
        self.plot_widget.add_matplotlib_toolbar(canvas_fit, fit_layout)
        fit_layout.addWidget(canvas_fit)

    def ensure_tab_exists(self, tab_name, fig_attr, ax_attr, canvas_attr):
        """
        Creates a tab if it does not exist and adds a scrollable
        area for large plots if necessary.
        """
        tab_dict = {
            "Data + Fit": "data_fit_tab",
            "Residuals": "residuals_tab",
            "99% Confidence": "confidence_tab",
            "2D Confidence Contours": "contours_2d_tab",
            "Fit Decomposition": "decompo_tab",
            "MCMC Fit": "mcmc_fit_tab",
            "Corner Plot": "corner_tab",
            "Autocorrelation": "autocorrelation_tab",
            "Walkers": "walkers_tab",
            "2D Scatter": "scatter_2d_tab",
            "2D Surface": "surface_2d_tab",
            "Multi 1D": "multi_1d",
        }

        tab_attr = tab_dict.get(tab_name)
        if tab_attr is None:
            raise ValueError(f"Tab name '{tab_name}' is not defined in tab_dict.")

        existing_tab = getattr(self.plot_widget, tab_attr, None)

        if existing_tab is not None:
            index = self.tabs.indexOf(existing_tab)
            if index != -1:
                self.switch_to_tab(tab_name)
                return
            else:
                setattr(self.plot_widget, tab_attr, None)

        if tab_name == "2D Surface":
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection="3d")
        else:
            fig, ax = plt.subplots(figsize=(10, 8))

        canvas = FigureCanvas(fig)

        new_tab = QWidget()
        new_tab.setMinimumSize(500, 400)
        layout = QVBoxLayout()

        if tab_name == "Corner Plot":
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            container_widget = QWidget()
            container_layout = QVBoxLayout()
            container_layout.addWidget(canvas)
            container_widget.setLayout(container_layout)

            container_widget.setMinimumSize(800, 800)
            scroll_area.setWidget(container_widget)

            layout.addWidget(scroll_area)
        else:
            layout.addWidget(canvas)

        new_tab.setLayout(layout)
        self.tabs.addTab(new_tab, tab_name)

        setattr(self.plot_widget, fig_attr, fig)
        setattr(self.plot_widget, ax_attr, ax)
        setattr(self.plot_widget, canvas_attr, canvas)
        setattr(self.plot_widget, tab_attr, new_tab)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True, linestyle="--", alpha=0.6)
        canvas.draw()

        self.switch_to_tab(tab_name)

    def switch_to_tab(self, tab_name):
        """Switches to the specified tab."""
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == tab_name:
                self.tabs.setCurrentIndex(i)
                return

    def get_tab(self, tab_name):
        """
        Returns the QWidget associated with a given tab name.

        Args:
            tab_name (str): The name used in the tab_dict (e.g. "99% Confidence").

        Returns:
            QWidget or None

        """
        tab_dict = {
            "Data + Fit": "data_fit_tab",
            "Residuals": "residuals_tab",
            "99% Confidence": "confidence_tab",
            "2D Confidence Contours": "contours_2d_tab",
            "Fit Decomposition": "decompo_tab",
            "MCMC Fit": "mcmc_fit_tab",
            "Corner Plot": "corner_tab",
            "Autocorrelation": "autocorrelation_tab",
            "Walkers": "walkers_tab",
            "2D Scatter": "scatter_2d_tab",
            "2D Surface": "surface_2d_tab",
            "Multi 1D": "multi_1d",
        }

        tab_attr = tab_dict.get(tab_name)
        if tab_attr:
            return getattr(self.plot_widget, tab_attr, None)
        return None

    def remove_all_tabs_except(self, keep_names):
        seen = set()
        indices_to_remove = []
        names_to_remove = []

        for i in range(self.tabs.count()):
            name = self.tabs.tabText(i)
            if name in keep_names:
                if name in seen:
                    indices_to_remove.append(i)
                    names_to_remove.append(name)
                else:
                    seen.add(name)
            else:
                indices_to_remove.append(i)
                names_to_remove.append(name)

        for i in reversed(indices_to_remove):
            self.tabs.removeTab(i)

        tab_dict = {
            "Data + Fit": "data_fit_tab",
            "Residuals": "residuals_tab",
            "99% Confidence": "confidence_tab",
            "2D Confidence Contours": "contours_2d_tab",
            "Fit Decomposition": "decompo_tab",
            "MCMC Fit": "mcmc_fit_tab",
            "Corner Plot": "corner_tab",
            "Autocorrelation": "autocorrelation_tab",
            "Walkers": "walkers_tab",
            "2D Scatter": "scatter_2d_tab",
            "2D Surface": "surface_2d_tab",
            "Multi 1D": "multi_1d",
        }

        for name in names_to_remove:
            attr = tab_dict.get(name)
            if attr and hasattr(self.plot_widget, attr):
                delattr(self.plot_widget, attr)
