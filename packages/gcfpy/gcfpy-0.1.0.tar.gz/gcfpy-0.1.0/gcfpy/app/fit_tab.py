import pandas as pd
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from gcfpy.controllers import (
    FitComparisonManager,
    FitControl,
    FitFormulaManager,
    FitOptionsWindow,
    ManualControl,
    smooth_data,
    weight_data,
)
from gcfpy.utils import ConfigManager, DataLoader
from gcfpy.widgets import BaseDockWidget


class FitTab(QMainWindow):
    """
    Fit tab for the curve fitting application.

    Handles data loading, plotting, formula input, fit controls,
    and dock widget setup for a single fitting session.
    """

    fit_counter = 0

    def __init__(self, main_window, plot_widget):
        """Initialize a new Fit tab instance."""
        super().__init__()
        self.main_window = main_window

        FitTab.fit_counter += 1
        self.fit_id = FitTab.fit_counter
        self.setWindowTitle(f"Fit {self.fit_id}")

        # Core widgets and managers
        self.plot_widget = plot_widget
        self.data_loader = DataLoader(self)
        self.manual_control = ManualControl(self)
        self.fit_options_dialog = FitOptionsWindow(self)
        self.fit_control = FitControl(self, self.main_window)
        self.comparison_manager = FitComparisonManager(self)
        self.formula_text = QTextEdit("y = a * x + b")
        self.formula_manager = FitFormulaManager(self, self.formula_text)

        self.fit_options = self.fit_options_dialog.get_options()

        self.config = ConfigManager()
        dock_width = self.config.get("fit_tab", "dock_formula_width", 200)
        dock_height = self.config.get("fit_tab", "dock_formula_height", 467)
        formula_text_max_height = self.config.get("fit_tab", "formula_text_height", 100)
        self.dock_formula = BaseDockWidget("Fit Formula", self)
        self.formula_text.setMaximumHeight(formula_text_max_height)
        self.formula_text.textChanged.connect(self.update_fit_options_params)
        self.dock_formula.setFixedSize(QSize(dock_width, dock_height))

        self.fit_control.dock_fit.setVisible(False)

        self.initUI()

    def initUI(self):
        """Create and configure all initial dock gcfpy.widgets."""
        self.view_actions = {}

        self.init_plot_dock()
        self.init_formula_dock()
        self.init_xy_dock()
        self.init_results_dock()

    def init_plot_dock(self):
        """Initialize the plot dock widget."""
        self.dock_plot = BaseDockWidget("Data Plot", self)
        self.dock_plot.setWidget(self.plot_widget)

        width = self.config.get("fit_tab", "dock_plot_width", 800)
        height = self.config.get("fit_tab", "dock_plot_height", 550)
        self.dock_plot.setFixedSize(width, height)

        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_plot)

    def init_formula_dock(self):
        """Initialize the formula input dock and connect to formula manager."""
        layout = QVBoxLayout()
        layout.addWidget(self.formula_text)

        self.import_formula_button = QPushButton("Import Formula")
        self.export_formula_button = QPushButton("Export Formula to Python")
        self.fit_options_button = QPushButton("Fit Options")

        self.import_formula_button.clicked.connect(self.formula_manager.import_formula)
        self.export_formula_button.clicked.connect(self.formula_manager.export_formula)
        self.fit_options_button.clicked.connect(self.open_fit_options)

        layout.addWidget(self.import_formula_button)
        layout.addWidget(self.export_formula_button)
        layout.addWidget(self.fit_options_button)

        container = QWidget()
        container.setLayout(layout)
        self.dock_formula.setWidget(container)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_formula)

    def init_xy_dock(self):
        """Initialize the data display dock (X/Y table)."""
        self.dock_xy = BaseDockWidget("X/Y Data", self)

        self.xy_table = self.create_xy_table()
        self.xy_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.xy_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.xy_table)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(scroll_area)
        layout.setContentsMargins(0, 0, 0, 0)

        self.dock_xy.setWidget(container)
        self.dock_xy.setHidden(True)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_xy)

    def init_results_dock(self):
        """Initialize the results dock to display fit reports."""
        self.dock_results = BaseDockWidget("Fit Results", self)
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)

        self.dock_results.setWidget(self.results_text)
        self.dock_results.setHidden(True)

        min_width = self.config.get("fit_tab", "results_min_width", 400)
        min_height = self.config.get("fit_tab", "results_min_height", 100)
        max_height = self.config.get("fit_tab", "results_max_height", 150)

        self.dock_results.setMinimumSize(QSize(min_width, min_height))
        self.dock_results.setMaximumHeight(max_height)

        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_results)

    def create_xy_table(self):
        """Create the table widget used to display X and Y data."""
        table = QTableWidget(2, 5)
        table.setVerticalHeaderLabels(["X", "Y"])
        table.setHorizontalHeaderLabels([str(i + 1) for i in range(5)])

        width = self.config.get("fit_tab", "xy_table_min_width", 300)
        height = self.config.get("fit_tab", "xy_table_min_height", 200)
        table.setMinimumSize(width, height)

        return table

    def show_error_message(self, message):
        """Display an error dialog with the provided message."""
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Critical)
        box.setWindowTitle("Error")
        box.setText(message)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()

    def show_fit_results(self):
        """Make the fit dock and results label visible."""
        self.fit_control.dock_fit.setVisible(True)
        self.fit_control.results_label.setVisible(True)

    def get_fit_name(self):
        """Return a unique name for this fit tab."""
        return f"Fit {self.fit_id}"

    def load_data_into_tab(self, df, file_path):
        """
        Load the given DataFrame into the XY table and plot widget.
        Detects whether data is 1D or 2D, and prepares the interface accordingly.
        """
        # Check and clean manual dock if active

        if hasattr(self, "manual_control"):
            manual = self.manual_control
            if not manual.dock_manual.isHidden():
                manual.toggle_manual_dock()
                if not isinstance(df, pd.DataFrame):
                    return

        self.df = df
        self.data_path = file_path

        columns = set(df.columns)
        base_cols_2d = {"X", "Y", "Z"}
        error_cols = {"X_err", "Y_err", "Z_err"}

        if {"X", "Y"}.issubset(columns) and "Z" not in columns:
            self.current_mode = "1D"
        elif base_cols_2d.issubset(columns):
            self.current_mode = "2D"
        else:
            QMessageBox.warning(
                self,
                "Invalid data",
                "Data must contain 'X' and 'Y' or 'X', 'Y', 'Z'.",
            )
            return

        for col in base_cols_2d.intersection(columns):
            if not pd.api.types.is_numeric_dtype(df[col]):
                QMessageBox.warning(
                    self, "Invalid column", f"Column '{col}' must be numeric."
                )
                return

        known_cols = base_cols_2d.union(error_cols)
        extra_cols = columns - known_cols
        if extra_cols:
            print(f"Ignored extra columns: {extra_cols}")

        self._cleanup_manual_control()

        self.dock_xy.setVisible(True)
        self.fit_control.dock_fit.setVisible(True)
        self.dock_results.setVisible(False)
        self.main_window.toolbar.toggle_comparison_action.setEnabled(False)

        if self.current_mode == "1D":
            self._load_1d_data(df)
            self.fit_control.update_strategy_selector(visible=False)
            self.plot_widget.update_plot_visibility("1D")
            self.formula_manager.update_formula_by_mode("1D")

        elif self.current_mode == "2D":
            self._load_2d_data(df)
            self.fit_control.update_strategy_selector(visible=True)
            strategy = self.fit_control.get_current_strategy()
            self.plot_widget.update_plot_visibility("2D", strategy)
            self.formula_manager.update_formula_by_mode("2D")

        if not self._validate_formula_against_data():
            return

    def _cleanup_manual_control(self):
        """Close and remove the manual control dock if active."""
        if hasattr(self, "manual_control") and hasattr(
            self.manual_control, "dock_manual"
        ):
            if not self.manual_control.dock_manual.isHidden():
                self.manual_control.toggle_manual_column(False)
                self.manual_control.dock_manual.close()
                self.manual_control.dock_manual.deleteLater()
                del self.manual_control.dock_manual
                self.manual_control = None
                self.fit_control.manual_button.setText("Manual")

    def open_fit_options(self):
        """Open the fit options dialog and store selected options if confirmed."""
        if self.fit_options_dialog.exec_():
            self.fit_options = self.fit_options_dialog.get_options()

    def update_fit_options_params(self):
        """Update the parameter list in FitOptionsWindow from current formula."""
        self.fit_options_dialog.update_params_tab(self.formula_text.toPlainText())

    def smooth_data(self, method):
        """Apply smoothing method and update the plotted data."""
        if self.plot_widget.data_x is None or self.plot_widget.data_y is None:
            return

        y_smooth = smooth_data(self.plot_widget.data_y, method)
        if y_smooth is not None:
            df = pd.DataFrame({"X": self.plot_widget.data_x, "Y": y_smooth})
            self.plot_widget.plot_data(df)

    def weight_data(self, method):
        """Apply weighting to the data before fitting.

        Args:
            method (str): One of 'x_err', 'y_err', 'xy_err', or 'none'.

        """
        pw = self.plot_widget

        if pw.data_x is None or pw.data_y is None:
            return

        x_err = getattr(pw, "x_err", None)
        y_err = getattr(pw, "y_err", None)

        pw.weights, pw.sx_sy, pw.sigma = weight_data(
            pw.data_x, pw.data_y, x_err, y_err, method
        )
        pw.weighting_method = method

    def update_results_text(self, fit_report):
        """Update the results dock with the given fit report."""
        self.results_text.setText(fit_report)
        self.dock_results.setVisible(True)

    def clear_data(self):
        """Clear all data and reset the plot."""
        self.df = None
        self.plot_widget.data_x = None
        self.plot_widget.data_y = None
        self.plot_widget.fit_y = None
        self.plot_widget.original_y = None
        self.plot_widget.result = None
        self.plot_widget.confidence_band = None
        self.plot_widget.components = {}

        self.dock_xy.setVisible(False)
        self.fit_control.dock_fit.setVisible(False)

        self.plot_widget.ax.clear()
        self.plot_widget.ax.set_title("No Data")
        self.plot_widget.canvas.draw()

    def _load_1d_data(self, df):
        """
        Initialize the table and plot for 1D data (X, Y ± errors).
        """
        has_xerr = "X_err" in df.columns
        has_yerr = "Y_err" in df.columns

        rows = ["X", "Y"]
        if has_xerr:
            rows.append("X_err")
        if has_yerr:
            rows.append("Y_err")

        self.xy_table.setRowCount(len(rows))
        self.xy_table.setColumnCount(len(df))
        self.xy_table.setVerticalHeaderLabels(rows)
        self.xy_table.horizontalHeader().setVisible(False)

        for col in range(len(df)):
            self.xy_table.setItem(0, col, QTableWidgetItem(f"{df['X'].iloc[col]:.3e}"))
            self.xy_table.setItem(1, col, QTableWidgetItem(f"{df['Y'].iloc[col]:.3e}"))
            row_idx = 2

            if has_xerr:
                self.xy_table.setItem(
                    row_idx,
                    col,
                    QTableWidgetItem(f"{df['X_err'].iloc[col]:.3e}"),
                )
                row_idx += 1
            if has_yerr:
                self.xy_table.setItem(
                    row_idx,
                    col,
                    QTableWidgetItem(f"{df['Y_err'].iloc[col]:.3e}"),
                )

            self.xy_table.setColumnWidth(col, 70)

        # Direct plot
        self.plot_widget.plot_data(df)

    def _load_2d_data(self, df):
        """
        Load and display 2D data (X, Y, Z) in both the table and the plot.
        """
        self.xy_table.clear()
        self.xy_table.setRowCount(3)
        self.xy_table.setColumnCount(len(df))
        self.xy_table.setVerticalHeaderLabels(["X", "Y", "Z"])
        self.xy_table.horizontalHeader().setVisible(False)

        for col in range(len(df)):
            self.xy_table.setItem(0, col, QTableWidgetItem(f"{df['X'].iloc[col]:.3e}"))
            self.xy_table.setItem(1, col, QTableWidgetItem(f"{df['Y'].iloc[col]:.3e}"))
            self.xy_table.setItem(2, col, QTableWidgetItem(f"{df['Z'].iloc[col]:.3e}"))
            self.xy_table.setColumnWidth(col, 70)

        x = df["X"].values
        y = df["Y"].values
        z = df["Z"].values

        strategy = self.fit_control.get_current_strategy().lower()
        self.plot_widget.plot_2d_series(x, y, z, strategy)

    def _validate_formula_against_data(self):
        """
        Checks that the formula is compatible with the data columns (1D or 2D).
        Displays an error message and returns False if this is not the case.
        """
        formula = self.formula_text.toPlainText().strip().lower().replace(" ", "")
        is_2d = self.current_mode == "2D"
        expected_start = "z=" if is_2d else "y="
        required_vars = {"x", "y"} if is_2d else {"x"}

        if not formula.startswith(expected_start):
            error_msg = f"Formula must start with '{expected_start}'"
            error_msg += f" for {self.current_mode} data. {formula}"
            self.show_error_message(error_msg)
            return False

        missing_vars = [v for v in required_vars if v not in formula]
        if missing_vars:
            self.show_error_message(
                f"Formula is missing required variable(s): {', '.join(missing_vars)}"
            )
            return False

        return True
