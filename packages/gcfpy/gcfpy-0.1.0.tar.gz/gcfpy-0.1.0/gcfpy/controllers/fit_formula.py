from PyQt5.QtWidgets import QFileDialog, QMessageBox

from .code_generator import (
    import_python_function,
    save_python_code,
)


class FitFormulaManager:
    """
    Handles logic related to the fit formula text:
    importing, exporting, updating from mode, etc.
    """

    def __init__(self, parent, formula_text_widget):
        """
        Args:
            parent (QWidget): The parent widget (usually FitTab).
            formula_text_widget (QTextEdit): The text widget for the formula.

        """
        self.parent = parent
        self.formula_text = formula_text_widget

    def update_formula_by_mode(self, mode):
        """
        Updates the formula based on the current fitting mode and strategy.

        Args:
            mode (str): "1D" or "2D"
            strategy (str, optional): "Fit per Y" or "Fit surface" (for 2D)

        """
        if mode == "1D":
            formula = "y = a * x + b"
        elif mode == "2D":
            formula = "z=a*x+y*b"
        else:
            formula = ""

        self.formula_text.setPlainText(formula)

    def import_formula(self):
        """
        Load a formula from a .py file and update the formula text widget.
        Also disables manual mode if it was active.
        """

        file_path, _ = QFileDialog.getOpenFileName(
            self.parent, "Import formula", "", "Python Files (*.py)"
        )
        if not file_path:
            return

        formula = import_python_function(file_path)

        if formula.startswith("### ERROR"):
            self.show_error_message_export_import(
                "Failed to import formula.\\n" + formula
            )
            return

        self.formula_text.setPlainText(formula)
        self.parent.fit_options_dialog.update_params_tab(formula)

        # Clean up manual mode if active
        if hasattr(self.parent, "manual_control") and hasattr(
            self.parent.manual_control, "dock_manual"
        ):
            if not self.parent.manual_control.dock_manual.isHidden():
                self.parent.manual_control.toggle_manual_column(False)
                self.parent.manual_control.dock_manual.close()
                self.parent.manual_control.dock_manual.deleteLater()
                del self.parent.manual_control.dock_manual
                self.parent.fit_control.manual_button.setText("Manual")

    def export_formula(self):
        """
        Export the current formula to a .py file.
        """
        formula = self.formula_text.toPlainText()
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent, "Export formula", "", "Python Files (*.py)"
        )
        if not file_path:
            return

        error = save_python_code(formula, file_path)
        if error:
            self.show_error_message_export_import(
                f"Failed to export formula:\\n{error}"
            )

    def show_error_message_export_import(self, message):
        """Display an error dialog with the provided message."""
        box = QMessageBox(self.parent)
        box.setIcon(QMessageBox.Critical)
        box.setWindowTitle("Error")
        box.setText(message)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()
