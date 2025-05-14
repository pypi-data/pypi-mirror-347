from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .formula_tools import extract_parameters


class FitOptionsWindow(QDialog):
    """Handles the configuration of fitting options and parameter settings."""

    def __init__(self, parent=None):
        """
        Initializes the Fit Options Window.

        Args:
            parent: The parent widget.

        """
        super().__init__(parent)
        self.setWindowTitle("Fit Options")
        self.setModal(True)
        self.param_names = []  # Stores the parameter names extracted from the formula
        self.manual_values = {}  # Stores manually set values for parameters
        self.initUI()

    def initUI(self):
        """Initializes the user interface with tabs and layout."""
        layout = QVBoxLayout(self)

        # Tab widget to separate general options and parameter settings
        self.tabs = QTabWidget()
        self.options_tab = QWidget()
        self.params_tab = QWidget()

        # Adding tabs to the interface
        self.tabs.addTab(self.params_tab, "Parameters")
        self.tabs.addTab(self.options_tab, "General Options")

        layout.addWidget(self.tabs)

        # Initialize content for both tabs
        self.init_options_tab()
        self.init_params_tab()

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

        # Update fields based on initial method selection
        self.toggle_tol_fields()

    def init_params_tab(self):
        """Creates the tab for parameter bounds and initial values."""
        self.params_layout = QVBoxLayout(self.params_tab)

        # Retrieve formula from FitTab if available
        formula = (
            self.parent.formula_text.toPlainText().strip()
            if hasattr(self.parent, "formula_text")
            else "y = a*x + b"  # Default formula if unavailable
        )

        # Extract parameter names from the formula
        self.param_names = extract_parameters(formula)

        # Table to configure parameters
        self.params_table = QTableWidget(len(self.param_names), 3)
        self.params_table.setHorizontalHeaderLabels(
            ["Parameter", "Bounds (min, max)", "Initial Value (p0)"]
        )
        self.params_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate the table with parameter settings
        for i, param in enumerate(self.param_names):
            self.params_table.setItem(i, 0, QTableWidgetItem(param))

            bounds_input = QLineEdit("-inf, inf")
            p0_input = QLineEdit("1.0")
            p0_input.setValidator(QDoubleValidator())

            self.params_table.setCellWidget(i, 1, bounds_input)
            self.params_table.setCellWidget(i, 2, p0_input)

        self.params_layout.addWidget(self.params_table)

    def init_options_tab(self):
        """Initializes the general fitting options tab."""
        self.form_layout = QFormLayout()

        self.method_combo = QComboBox()
        self.method_combo.addItems(
            [
                "leastsq",
                "least_squares",
                "nelder",
                "lbfgsb",
                "powell",
                "cg",
                "cobyla",
                "tnc",
                "trust-constr",
                "slsqp",
                "emcee",
                "odr",
            ]
        )
        self.method_combo.setCurrentText("leastsq")
        self.method_combo.currentTextChanged.connect(self.toggle_fit_options)

        # General fit settings (not used for MCMC)
        self.max_nfev_label = QLabel("Max NFEV")
        self.max_nfev_input = QLineEdit("1000")
        self.max_nfev_input.setValidator(QDoubleValidator())

        self.reduce_fcn_label = QLabel("Reduction Function")
        self.reduce_fcn_combo = QComboBox()
        self.reduce_fcn_combo.addItems(
            ["neglogcauchy", "negloglikelihood", "negentropy"]
        )
        self.reduce_fcn_combo.setCurrentText("neglogcauchy")

        # Covariance calculation options
        self.calc_covar_check = QCheckBox("Calculate covariance")
        self.calc_covar_check.setChecked(True)

        self.scale_covar_check = QCheckBox("Scale covariance")
        self.scale_covar_check.setChecked(True)

        # Convergence tolerances (hidden for MCMC)
        self.xtol_label = QLabel("Xtol")
        self.xtol_input = QLineEdit("1.5e-8")
        self.xtol_input.setValidator(QDoubleValidator())

        self.ftol_label = QLabel("Ftol")
        self.ftol_input = QLineEdit("1.5e-8")
        self.ftol_input.setValidator(QDoubleValidator())

        self.gtol_label = QLabel("Gtol")
        self.gtol_input = QLineEdit("1.5e-8")
        self.gtol_input.setValidator(QDoubleValidator())

        self.tol_widgets = [
            (self.xtol_label, self.xtol_input),
            (self.ftol_label, self.ftol_input),
            (self.gtol_label, self.gtol_input),
        ]

        # MCMC-specific options
        self.nwalkers_label = QLabel("N Walkers")
        self.nwalkers_input = QLineEdit("50")
        self.nwalkers_input.setValidator(QDoubleValidator())

        self.steps_label = QLabel("Steps")
        self.steps_input = QLineEdit("1000")
        self.steps_input.setValidator(QDoubleValidator())

        self.burn_label = QLabel("Burn-in")
        self.burn_input = QLineEdit("500")
        self.burn_input.setValidator(QDoubleValidator())

        self.thin_label = QLabel("Thin")
        self.thin_input = QLineEdit("10")
        self.thin_input.setValidator(QDoubleValidator())

        self.is_weighted_check = QCheckBox("Use weights?")
        self.is_weighted_check.setChecked(True)

        # Add widgets to layout
        self.form_layout.addRow("Method", self.method_combo)
        self.form_layout.addRow(self.max_nfev_label, self.max_nfev_input)
        self.form_layout.addRow(self.reduce_fcn_label, self.reduce_fcn_combo)

        for label, widget in self.tol_widgets:
            self.form_layout.addRow(label, widget)

        self.form_layout.addRow(self.calc_covar_check)
        self.form_layout.addRow(self.scale_covar_check)

        # MCMC options (hidden by default)
        self.form_layout.addRow(self.nwalkers_label, self.nwalkers_input)
        self.form_layout.addRow(self.steps_label, self.steps_input)
        self.form_layout.addRow(self.burn_label, self.burn_input)
        self.form_layout.addRow(self.thin_label, self.thin_input)
        self.form_layout.addRow(self.is_weighted_check)

        # Apply layout and update visibility
        self.options_tab.setLayout(self.form_layout)
        self.toggle_fit_options()

    def toggle_fit_options(self):
        """Shows or hides fields based on the selected fitting method."""
        is_emcee = self.method_combo.currentText() == "emcee"
        is_leastsq = self.method_combo.currentText() == "leastsq"

        # Hide options not needed for MCMC
        self.max_nfev_label.setVisible(not is_emcee)
        self.max_nfev_input.setVisible(not is_emcee)
        self.reduce_fcn_label.setVisible(not is_emcee)
        self.reduce_fcn_combo.setVisible(not is_emcee)
        self.calc_covar_check.setVisible(not is_emcee)
        self.scale_covar_check.setVisible(not is_emcee)

        # Show or hide tolerance fields
        for label, widget in self.tol_widgets:
            label.setVisible(is_leastsq)
            widget.setVisible(is_leastsq)

        # Show MCMC options
        self.nwalkers_label.setVisible(is_emcee)
        self.nwalkers_input.setVisible(is_emcee)
        self.steps_label.setVisible(is_emcee)
        self.steps_input.setVisible(is_emcee)
        self.burn_label.setVisible(is_emcee)
        self.burn_input.setVisible(is_emcee)
        self.thin_label.setVisible(is_emcee)
        self.thin_input.setVisible(is_emcee)
        self.is_weighted_check.setVisible(is_emcee)

    def toggle_tol_fields(self):
        """Shows or hides tolerance fields based on the selected method."""
        is_leastsq = self.method_combo.currentText() == "leastsq"
        for label, widget in self.tol_widgets:
            label.setVisible(is_leastsq)
            widget.setVisible(is_leastsq)

    def get_options(self):
        """Returns the selected fit options as a dictionary."""
        options = {"method": self.method_combo.currentText()}

        try:
            if options["method"] == "emcee":
                options.update(
                    {
                        "nwalkers": int(self.nwalkers_input.text() or 50),
                        "steps": int(self.steps_input.text() or 1000),
                        "burn": int(self.burn_input.text() or 500),
                        "thin": int(self.thin_input.text() or 10),
                        "is_weighted": self.is_weighted_check.isChecked(),
                    }
                )
            else:
                options.update(
                    {
                        "max_nfev": int(self.max_nfev_input.text() or 1000),
                        "reduce_fcn": self.reduce_fcn_combo.currentText(),
                        "calc_covar": self.calc_covar_check.isChecked(),
                        "scale_covar": self.scale_covar_check.isChecked(),
                    }
                )

                # Add tolerances only if "leastsq" is selected
                if options["method"] == "leastsq":
                    options.update(
                        {
                            "xtol": float(self.xtol_input.text() or 1.5e-8),
                            "ftol": float(self.ftol_input.text() or 1.5e-8),
                            "gtol": float(self.gtol_input.text() or 1.5e-8),
                        }
                    )
            options["params"] = self.get_params_options()
        except ValueError:
            print("Invalid input in fit options.")
            return None

        return options

    def update_params_tab(self, formula):
        """Updates the parameter list based on the new formula."""
        param_names = extract_parameters(formula)

        if param_names:
            # Clear old content
            self.params_table.clearContents()
            self.params_table.setRowCount(len(param_names))

            # Add new parameters
            for i, param in enumerate(param_names):
                self.params_table.setItem(i, 0, QTableWidgetItem(param))
                bounds_input = QLineEdit("-inf, inf")
                p0_input = QLineEdit("1.0")
                p0_input.setValidator(QDoubleValidator())

                self.params_table.setCellWidget(i, 1, bounds_input)
                self.params_table.setCellWidget(i, 2, p0_input)

    def get_params_options(self):
        """Returns the parameter fit options (bounds and initial values)."""
        params_options = {}

        for i in range(self.params_table.rowCount()):
            param_name = self.params_table.item(i, 0).text()

            bounds_text = self.params_table.cellWidget(i, 1).text().strip()
            try:
                bounds = [float(b) for b in bounds_text.split(",")]
                if len(bounds) != 2:
                    raise ValueError
            except ValueError:
                bounds = [float("-inf"), float("inf")]  # Default values

            # Retrieve initial value (p0)
            try:
                p0_value = float(self.params_table.cellWidget(i, 2).text())
            except ValueError:
                p0_value = 1.0  # Default initial value

            # Store values for this parameter
            params_options[param_name] = {
                "bounds": tuple(bounds),
                "p0": p0_value,
            }

        return params_options
