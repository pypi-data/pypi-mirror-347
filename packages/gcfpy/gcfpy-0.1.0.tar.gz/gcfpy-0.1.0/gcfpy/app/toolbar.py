import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QToolBar


class Toolbar(QToolBar):
    """
    Toolbar for fitting and plotting actions.

    Provides shortcuts for toggling confidence intervals, residuals,
    components, smoothing, weighting, and fit comparison tools.
    """

    def __init__(self, parent):
        """
        Initialize the toolbar with all actions, menus, and connections.

        Args:
            parent (QMainWindow): Main application window or parent widget.

        """
        super().__init__("Fit & Plot Tools", parent)
        self.parent = parent
        self.setMovable(False)
        self._init_paths()
        self._init_actions()
        self._init_menus()
        self._connect_signals()
        self._add_to_toolbar()
        self._set_tooltips()

    def _init_paths(self):
        """
        Initialize the icon directory path.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.icon_dir = os.path.join(base_dir, "icon")

    def _icon(self, name):
        """
        Load an icon from the toolbar's icon directory.

        Args:
            name (str): Filename of the icon.

        Returns:
            QIcon: Loaded icon.

        """
        return QIcon(os.path.join(self.icon_dir, name))

    def _init_actions(self):
        """
        Initialize all toolbar actions (buttons and toggles).

        Sets up:
            - Plot toggles (confidence intervals, residuals, components)
            - Xmin/Xmax selection
            - Smoothing method choices
            - Weighting method choices
            - Fit comparison tools
        """
        # Toggle actions
        self.toggle_confidence_action = QAction(
            self._icon("conf_1d.png"), "99% CI", self
        )
        self.toggle_residuals_action = QAction(
            self._icon("resi.png"), "Residuals", self
        )
        self.toggle_components_action = QAction(
            self._icon("decomp.png"), "Components", self
        )
        self.toggle_confidence_2d_action = QAction(
            self._icon("conf_2d.png"), "2D CI", self
        )

        for action in [
            self.toggle_confidence_action,
            self.toggle_residuals_action,
            self.toggle_components_action,
            self.toggle_confidence_2d_action,
        ]:
            action.setEnabled(False)

        # Xmin/Xmax toggle
        self.set_xmin_xmax_action = QAction("Xmin/Xmax", self)
        self.set_xmin_xmax_action.setCheckable(True)
        self.set_xmin_xmax_action.setEnabled(False)

        # Smoothing dropdown
        self.smooth_gaussian_action = QAction("Gaussian", self)
        self.smooth_moving_avg_action = QAction("Moving Average", self)
        self.smooth_none_action = QAction("None", self)
        for a in (
            self.smooth_gaussian_action,
            self.smooth_moving_avg_action,
            self.smooth_none_action,
        ):
            a.setCheckable(True)
        self.smooth_none_action.setChecked(True)

        # Weighting dropdown
        self.weight_xerr_action = QAction("x error", self)
        self.weight_yerr_action = QAction("y error", self)
        self.weight_xyerr_action = QAction("x and y error", self)
        self.weight_none_action = QAction("None", self)
        for a in (
            self.weight_xerr_action,
            self.weight_yerr_action,
            self.weight_xyerr_action,
            self.weight_none_action,
        ):
            a.setCheckable(True)
        self.weight_none_action.setChecked(True)

        # Comparison
        self.add_fit_action = QAction("Add Fit", self)
        self.add_fit_action.setEnabled(False)

        self.toggle_comparison_action = QAction("Compare", self)
        self.toggle_comparison_action.setCheckable(True)
        self.toggle_comparison_action.setEnabled(False)

    def _init_menus(self):
        """
        Initialize dropdown menus for smoothing and weighting.

        Each menu groups the relevant actions created in _init_actions.
        """
        self.smooth_data_menu = QMenu("Smoothing", self)
        self.smooth_data_menu.addActions(
            [
                self.smooth_gaussian_action,
                self.smooth_moving_avg_action,
                self.smooth_none_action,
            ]
        )

        self.smooth_data_action = QAction("Smoothing", self)
        self.smooth_data_action.setMenu(self.smooth_data_menu)
        self.smooth_data_action.setEnabled(False)

        self.weight_data_menu = QMenu("Weighting", self)
        self.weight_data_menu.addActions(
            [
                self.weight_xerr_action,
                self.weight_yerr_action,
                self.weight_xyerr_action,
                self.weight_none_action,
            ]
        )

        self.weight_data_action = QAction("Weighting", self)
        self.weight_data_action.setMenu(self.weight_data_menu)
        self.weight_data_action.setEnabled(False)

    def _connect_signals(self):
        """
        Connect actions to their corresponding callback methods.

        Maps each toolbar action to its logic or visual update function.
        """

        # Plot toggles
        self.toggle_confidence_action.triggered.connect(self.toggle_confidence)
        self.toggle_residuals_action.triggered.connect(self.toggle_residuals)
        self.toggle_components_action.triggered.connect(self.toggle_components)
        self.toggle_confidence_2d_action.triggered.connect(self.plot_confidence_2d)

        # Xmin/Xmax toggle
        self.set_xmin_xmax_action.triggered.connect(self.toggle_xmin_xmax)

        # Smoothing methods, need to change this part
        self.smooth_gaussian_action.triggered.connect(
            lambda: self._apply_smoothing("savgol")
        )
        self.smooth_moving_avg_action.triggered.connect(
            lambda: self._apply_smoothing("avg")
        )
        self.smooth_none_action.triggered.connect(lambda: self._apply_smoothing("none"))

        # Weighting methods
        self.weight_xerr_action.triggered.connect(
            lambda: self._apply_weighting("x_err")
        )
        self.weight_yerr_action.triggered.connect(
            lambda: self._apply_weighting("y_err")
        )
        self.weight_xyerr_action.triggered.connect(
            lambda: self._apply_weighting("xy_err")
        )
        self.weight_none_action.triggered.connect(lambda: self._apply_weighting("none"))

        # Fit comparison
        self.add_fit_action.triggered.connect(self.add_fit_to_comparison)

        self.toggle_comparison_action.triggered.connect(self._toggle_comparison_mode)

    def _toggle_comparison_mode(self):
        tab = self.parent.get_current_fit_tab()
        manager = tab.comparison_manager
        manager.toggle_comparison_mode(not manager.comparison_mode)

    def _add_to_toolbar(self):
        """
        Add actions and separators to the toolbar layout.

        Organizes the display order of toolbar buttons and dropdowns.
        """
        self.addActions(
            [
                self.toggle_confidence_action,
                self.toggle_residuals_action,
                self.toggle_components_action,
                self.toggle_confidence_2d_action,
            ]
        )
        self.addSeparator()
        self.addAction(self.set_xmin_xmax_action)
        self.addAction(self.smooth_data_action)
        self.addAction(self.weight_data_action)
        self.addSeparator()
        self.addAction(self.add_fit_action)
        self.addAction(self.toggle_comparison_action)

    def _set_tooltips(self):
        """
        Set descriptive tooltips for all toolbar buttons.

        Improves user accessibility and usability.
        """
        self.toggle_confidence_action.setToolTip("Show/hide 99% confidence interval.")
        self.toggle_residuals_action.setToolTip("Show residuals: data - fit.")
        self.toggle_components_action.setToolTip("Show fitted components.")
        self.toggle_confidence_2d_action.setToolTip(
            "Show 2D parameter confidence contours."
        )
        self.set_xmin_xmax_action.setToolTip("Define x-range for fitting.")
        self.smooth_data_action.setToolTip("Apply smoothing to input data.")
        self.weight_data_action.setToolTip("Apply weighting method to data.")
        self.add_fit_action.setToolTip("Add current fit to comparison set.")
        self.toggle_comparison_action.setToolTip("Enable/disable comparison mode.")

    def _apply_smoothing(self, method):
        """
        Apply the selected smoothing method to the current tab's data.

        Args:
            method (str): Smoothing method ('savgol', 'avg', 'none').

        """
        tab = self.get_current_fit_tab()
        if tab:
            tab.smooth_data(method)
        self._update_checkmarks(
            method,
            {
                "savgol": self.smooth_gaussian_action,
                "avg": self.smooth_moving_avg_action,
                "none": self.smooth_none_action,
            },
        )

    def _apply_weighting(self, method):
        """
        Apply the selected weighting method to the current tab's data.

        Args:
            method (str): Weighting method ('x_err', 'y_err', 'xy_err', 'none').

        """
        tab = self.get_current_fit_tab()
        if tab:
            tab.weight_data(method)
        self._update_checkmarks(
            method,
            {
                "x_err": self.weight_xerr_action,
                "y_err": self.weight_yerr_action,
                "xy_err": self.weight_xyerr_action,
                "none": self.weight_none_action,
            },
        )

    def _update_checkmarks(self, selected, action_map):
        """
        Update the checkmark on toolbar dropdowns based on the selected method.

        Args:
            selected (str): Key of the selected method.
            action_map (dict): Mapping from method key to QAction.

        """
        for key, action in action_map.items():
            action.setChecked(key == selected)

    def toggle_xmin_xmax(self):
        """
        Toggle the Xmin/Xmax selection tool based on toolbar button state.
        """
        tab = self.parent.get_current_fit_tab()
        if not tab:
            return
        tool = tab.plot_widget.xmin_xmax_tool
        if self.set_xmin_xmax_action.isChecked():
            tool.enable_xmin_xmax_selection()
        else:
            tool.disable_xmin_xmax_selection()

    def reset_xmin_xmax_button_style(self):
        """
        Uncheck the Xmin/Xmax selection button.
        """
        self.set_xmin_xmax_action.setChecked(False)

    def toggle_confidence(self):
        """
        Toggle the display of the 1D confidence interval on the plot.
        """
        widget = self.get_active_plot_widget()
        if widget:
            widget.analysis_plot.toggle_confidence_band()

    def toggle_residuals(self):
        """
        Toggle the display of residuals (data - fit) on the plot.
        """
        widget = self.get_active_plot_widget()
        if widget:
            widget.analysis_plot.toggle_residuals_plot()

    def toggle_components(self):
        """
        Toggle the display of individual fit components on the plot.
        """
        widget = self.get_active_plot_widget()
        if widget:
            widget.analysis_plot.toggle_fit_decomposition()

    def plot_confidence_2d(self):
        """
        Plot the 2D confidence interval (parameter space) on the active plot.
        """
        widget = self.get_active_plot_widget()
        if widget:
            widget.analysis_plot.plot_conf_interval_2d()

    def add_fit_to_comparison(self):
        """
        Add the current fit result to the comparison manager.
        """
        self.parent.get_current_fit_tab().comparison_manager.store_current_fit()

    def enable_toolbar_options(self, state):
        """
        Enable or disable toolbar options (Xmin/Xmax, smoothing, weighting).

        Args:
            state (bool): True to enable, False to disable.

        """
        self.set_xmin_xmax_action.setEnabled(state)
        self.smooth_data_action.setEnabled(state)
        self.weight_data_action.setEnabled(state)

    def enable_toolbar_plot_options(self, state):
        """
        Enable or disable plot-related toolbar actions (confidence, residuals, etc.).

        Args:
            state (bool): True to enable, False to disable.

        """
        for action in [
            self.toggle_confidence_action,
            self.toggle_residuals_action,
            self.toggle_components_action,
            self.toggle_confidence_2d_action,
        ]:
            action.setEnabled(state)

    def enable_comparison(self, enabled=True):
        """
        Enable or disable fit comparison buttons.

        Args:
            enabled (bool, optional): Default True.

        """
        self.add_fit_action.setEnabled(enabled)
        self.toggle_comparison_action.setEnabled(enabled)

    def get_current_fit_tab(self):
        """
        Return the currently active FitTab.
        """
        return self.parent.get_current_fit_tab()

    def get_active_plot_widget(self):
        """
        Return the PlotWidget of the active tab, if available.
        """
        tab = self.get_current_fit_tab()
        return tab.plot_widget if tab and hasattr(tab, "plot_widget") else None
