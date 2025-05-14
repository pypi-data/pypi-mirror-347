import copy
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QTabBar,
    QTabWidget,
)

from gcfpy.app.fit_tab import FitTab
from gcfpy.app.toolbar import Toolbar
from gcfpy.utils import (
    ConfigManager,
    DataLoader,
    load_previous_file,
    save_previous_file,
)
from gcfpy.widgets import PlotWidget


class MainWindow(QMainWindow):
    """
    Main application window for the curve fitting GUI.

    Handles initialization of the interface and central tab system,
    loads configuration, and manages user-level interactions.
    """

    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        self.setWindowTitle("Graphical Curve Fitting")
        self.setWindowFlags(self.windowFlags())
        self.config = ConfigManager()
        width = self.config.get("window", "width", 1200)
        height = self.config.get("window", "height", 800)
        self.setFixedSize(width, height)  # Not sure
        self._init_interface()

    def _init_interface(self):
        """Set up menu bar, toolbar, and tab system."""
        self.toolbar = Toolbar(self)
        self.addToolBar(self.toolbar)

        # Menu bar and menus
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        fits_menu = menu_bar.addMenu("Fits")
        self.view_menu = menu_bar.addMenu("View")

        self._init_file_menu(file_menu)
        self._init_fits_menu(fits_menu)

        # Tabs setup
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabs.tabCloseRequested.connect(self.close_fit_tab)
        self.setCentralWidget(self.tabs)

        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # Saves dock toolbar in each tab
        self.view_actions_per_tab = {}
        self.dock_visibility_per_tab = {}
        self.toolbar_states_per_tab = {}
        self.tabs.tabBarClicked.connect(self._snapshot_dock_states_before_switch)

        self.tabs.currentChanged.connect(self._update_view_menu_for_current_tab)
        self.add_fit_tab()

    def _init_file_menu(self, file_menu):
        """
        Initialize the 'File' menu with actions for loading, exporting,
        and exiting the application.
        """
        load_action = QAction("Load Data", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_data_from_menu)

        unload_action = QAction("Unload Data", self)
        unload_action.setShortcut("Ctrl+W")
        unload_action.triggered.connect(self.unload_data)

        load_prev_action = QAction("Load Previous Data", self)
        load_prev_action.setShortcut("Ctrl+Shift+O")
        load_prev_action.triggered.connect(self.load_previous_data)

        export_action = QAction("Export Data", self)
        export_action.setShortcut("Ctrl+S")
        export_action.triggered.connect(self.export_data)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addActions(
            [
                load_action,
                unload_action,
                load_prev_action,
                export_action,
                exit_action,
            ]
        )

    def _init_fits_menu(self, fits_menu):
        """
        Initialize the 'Fits' menu with actions for
        managing fit tabs and dock visibility.
        """
        new_fit_action = QAction("New Fit Window", self)
        new_fit_action.triggered.connect(self.add_fit_tab)

        close_fit_action = QAction("Close Fit Window", self)
        close_fit_action.triggered.connect(
            lambda: self.close_fit_tab(self.tabs.currentIndex())
        )

        fits_menu.addActions(
            [
                new_fit_action,
                close_fit_action,
            ]
        )

        # Stores toggle actions for individual dock widgets per fit tab
        self.dock_actions = {}

    def _init_view_menu(self, view_menu, tab):
        """
        Create and link the View menu actions to the visibility
        of each dock in the given tab.
        """
        dock_map = {
            "Fit Formula": tab.dock_formula,
            "Data Plot": tab.dock_plot,
            "X/Y Table": tab.dock_xy,
            "Fit Results": tab.dock_results,
            "Fit Panel": tab.fit_control.dock_fit,
            "Manual control": tab.manual_control.dock_manual,
        }

        actions = {}
        for name, dock in dock_map.items():
            action = QAction(name, self)
            action.setCheckable(True)
            action.setChecked(not dock.isHidden())
            action.toggled.connect(dock.setVisible)
            dock.visibilityChanged.connect(action.setChecked)
            view_menu.addAction(action)
            actions[name] = (action, dock)
        restore_action = QAction("Restore Default View", self)
        restore_action.triggered.connect(self.restore_default_view)
        view_menu.addAction(restore_action)

        self.view_actions_per_tab[tab] = actions

    def _update_view_menu_for_current_tab(self):
        """
        Update the View menu to reflect the current tab s dock states.
        Dock visibility is restored from the snapshot made before tab switch.
        """
        new_tab = self.get_current_fit_tab()
        if not new_tab:
            return

        self.view_menu.clear()

        if new_tab not in self.view_actions_per_tab:
            self._init_view_menu(self.view_menu, new_tab)

        # dock_visibility_per_tab[tab] = {dock_name: visible_bool}
        visibility = self.dock_visibility_per_tab.get(new_tab, {})
        for name, (action, dock) in self.view_actions_per_tab[new_tab].items():
            if name in visibility:
                dock.setVisible(visibility[name])
            self.view_menu.addAction(action)

        restore_action = QAction("Restore Default View", self)
        restore_action.setShortcut("Ctrl+R")
        restore_action.triggered.connect(self.restore_default_view)
        self.view_menu.addAction(restore_action)

        # reload toolbar
        self._restore_toolbar_state(new_tab)

    def add_fit_tab(self):
        """Create and activate a new Fit tab with its own plot and docks."""

        # Hack for save previous tab
        # Save current tab state before switching (toolbar and dock visibility)
        try:
            self._init_view_menu(self.view_menu, self.get_current_fit_tab())
            self._snapshot_dock_states_before_switch(self.get_current_fit_tab())
        except Exception:
            pass

        # Create new plot and tab
        plot_widget = PlotWidget(self)
        new_tab = FitTab(self, plot_widget)
        self.tabs.addTab(new_tab, new_tab.get_fit_name())
        self.tabs.setCurrentWidget(new_tab)

        # Restore toolbar state for the new tab
        self._restore_toolbar_state(new_tab)

    def get_current_fit_tab(self):
        """Return the current tab if it is a valid FitTab."""
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, FitTab):
            return current_tab
        return None

    def close_fit_tab(self, index):
        """Close a specific FitTab by index."""
        if 0 <= index < self.tabs.count():
            self.tabs.removeTab(index)

    def load_data_from_menu(self):
        """Load data via dialog and send it to the current FitTab."""
        data_loader = DataLoader(self)
        df, file_path = data_loader.load_data()

        if df is not None:
            self._inject_data_into_tab(df, file_path, "Data")
            save_previous_file(file_path)

    def load_previous_data(self):
        """Load the most recent data file from history."""
        prev_file = load_previous_file()
        if prev_file and os.path.exists(prev_file):
            data_loader = DataLoader(self)
            df, _ = data_loader.load_data(prev_file)

            if df is not None:
                self._inject_data_into_tab(df, prev_file, "Previous data")
        else:
            self.show_status("No previous data file found.")

    def _inject_data_into_tab(self, df, file_path, label):
        """Inject the DataFrame into the current tab and update the status."""
        current_tab = self.get_current_fit_tab()
        if current_tab:
            current_tab.load_data_into_tab(df, file_path)
            self.show_status(f"{label} loaded from {file_path}")

    def rename_tab(self, index):
        """Allow renaming of a tab via inline editing."""
        tab_bar = self.tabs.tabBar()
        tab_name_edit = QLineEdit(self.tabs.tabText(index))
        tab_name_edit.setFrame(False)
        tab_name_edit.setAlignment(Qt.AlignCenter)
        tab_bar.setTabButton(index, QTabBar.LeftSide, tab_name_edit)
        tab_name_edit.setFocus()

        def save_name():
            name = tab_name_edit.text().strip() or self.tabs.tabText(index)
            self.tabs.setTabText(index, name)
            tab_bar.setTabButton(index, QTabBar.LeftSide, None)
            tab_name_edit.deleteLater()

        tab_name_edit.editingFinished.connect(save_name)
        tab_name_edit.focusOutEvent = lambda event: save_name()

    def duplicate_tab(self, index):
        """Duplicate a FitTab, including data, formula, and fit options."""
        original_tab = self.tabs.widget(index)
        if not isinstance(original_tab, FitTab):
            return

        new_plot_widget = PlotWidget(self)
        new_tab = FitTab(self, new_plot_widget)

        # Copy data
        if hasattr(original_tab, "df") and original_tab.df is not None:
            new_tab.df = original_tab.df.copy()
            new_tab.load_data_into_tab(new_tab.df, "Duplicated Data")

        new_tab.formula_text.setText(original_tab.formula_text.toPlainText())

        new_tab.fit_options = copy.deepcopy(
            original_tab.fit_options
        )  # I don't remember if i need a deepcopy

        # Pb if we duplicate 2d or multi 1d
        if hasattr(new_tab, "df") and new_tab.df is not None:
            new_tab.plot_widget.plot_data(new_tab.df)

        self.tabs.addTab(new_tab, f"{self.tabs.tabText(index)} (Copy)")
        self.tabs.setCurrentWidget(new_tab)
        self.show_status(f"Duplicated tab: {self.tabs.tabText(index)}")

    def enable_toolbar_buttons(self, enabled):
        """Enable or disable toolbar buttons after a fit."""
        self.toolbar.toggle_confidence_action.setEnabled(enabled)
        self.toolbar.toggle_residuals_action.setEnabled(enabled)
        self.toolbar.toggle_components_action.setEnabled(enabled)
        self.toolbar.toggle_confidence_2d_action.setEnabled(enabled)

    def unload_data(self):
        """Clear all data from the currently active FitTab."""
        current_tab = self.get_current_fit_tab()
        if current_tab:
            current_tab.clear_data()
            QMessageBox.information(self, "Data cleared", "All data has been removed.")
            self.show_status("Data cleared")

    def export_data(self):
        """Export the current data as a CSV file."""
        current_tab = self.get_current_fit_tab()
        if current_tab and hasattr(current_tab, "df") and current_tab.df is not None:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Export data",
                "",
                "CSV Files (*.csv);;All Files (*)",
            )
            if file_name:
                try:
                    current_tab.df.to_csv(file_name, index=False)
                    QMessageBox.information(
                        self,
                        "Export successful",
                        f"Data was saved to:\n{file_name}",
                    )
                except Exception as e:
                    QMessageBox.warning(
                        self,
                        "Export failed",
                        f"An error occurred while exporting:\n{e}",
                    )
        else:
            QMessageBox.warning(
                self,
                "No data available",
                "There is no data to export from this tab.",
            )

    def restore_default_view(self):
        """
        Restore visibility and check state for all dock widgets of the current tab.
        """
        current_tab = self.get_current_fit_tab()
        if not current_tab or current_tab not in self.view_actions_per_tab:
            return

        for name, (action, dock) in self.view_actions_per_tab[current_tab].items():
            dock.show()
            action.setChecked(True)

        self.show_status("View restored to default")

    def show_status(self, message: str, timeout: int = 4000):
        """
        Display a temporary message in the status bar.

        Args:
            message (str): The message to display.
            timeout (int): Time in ms the message is visible. 0 means permanent.

        """
        self.status_bar.showMessage(message, timeout)

    def _snapshot_dock_states_before_switch(self, index):
        """
        Save the current tab's dock visibility state just before switching tabs.
        This prevents Qt's internal hiding of docks from polluting our state tracking.
        Same thing for the toolbar
        """
        current_tab = self.get_current_fit_tab()
        if not current_tab or current_tab not in self.view_actions_per_tab:
            return

        self.dock_visibility_per_tab[current_tab] = {}
        for name, (_, dock) in self.view_actions_per_tab[current_tab].items():
            is_visible = dock.isVisible()
            self.dock_visibility_per_tab[current_tab][name] = is_visible

        self._snapshot_toolbar_state(current_tab)

    def _snapshot_toolbar_state(self, tab):
        """Save toolbar button states (enabled/visible) for a given tab."""
        self.toolbar_states_per_tab[tab] = {
            "confidence": self.toolbar.toggle_confidence_action.isEnabled(),
            "residuals": self.toolbar.toggle_residuals_action.isEnabled(),
            "components": self.toolbar.toggle_components_action.isEnabled(),
            "confidence_2d": self.toolbar.toggle_confidence_2d_action.isEnabled(),
            "Xmin/Xmax": self.toolbar.set_xmin_xmax_action.isEnabled(),
            "Smoothing": self.toolbar.smooth_data_menu.isEnabled(),
            "Weighting": self.toolbar.weight_data_menu.isEnabled(),
            "Add Fit": self.toolbar.add_fit_action.isEnabled(),
            "Compare": self.toolbar.toggle_comparison_action.isEnabled(),
        }

    def _restore_toolbar_state(self, tab):
        """Restore toolbar button states for a given tab."""
        state = self.toolbar_states_per_tab.get(tab)
        if not state:
            # Disable all relevant toolbar buttons if no state available
            self.enable_toolbar_buttons(False)
            self.toolbar.set_xmin_xmax_action.setEnabled(False)
            self.toolbar.smooth_data_action.setEnabled(False)
            self.toolbar.weight_data_action.setEnabled(False)
            self.toolbar.add_fit_action.setEnabled(False)
            self.toolbar.toggle_comparison_action.setEnabled(False)
            return

        # Restore each toolbar button based on saved state
        self.toolbar.toggle_confidence_action.setEnabled(state.get("confidence", False))
        self.toolbar.toggle_residuals_action.setEnabled(state.get("residuals", False))
        self.toolbar.toggle_components_action.setEnabled(state.get("components", False))
        self.toolbar.toggle_confidence_2d_action.setEnabled(
            state.get("confidence_2d", False)
        )
        self.toolbar.set_xmin_xmax_action.setEnabled(state.get("Xmin/Xmax", False))
        self.toolbar.smooth_data_menu.setEnabled(state.get("Smoothing", False))
        self.toolbar.weight_data_menu.setEnabled(state.get("Weighting", False))
        self.toolbar.add_fit_action.setEnabled(state.get("Add Fit", False))
        self.toolbar.toggle_comparison_action.setEnabled(state.get("Compare", False))


def main():
    import os

    dir_path = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.dirname(dir_path)
    icon_path = os.path.join(dir_path, "icon", "test.png")
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()
    window.show()
    window.raise_()
    window.activateWindow()
    frame_geom = window.frameGeometry()
    screen_center = QApplication.desktop().availableGeometry().center()
    frame_geom.moveCenter(screen_center)
    window.move(frame_geom.topLeft())
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
