from unittest.mock import MagicMock, patch

import pytest
from gcfpy.controllers.fit_formula import FitFormulaManager
from gcfpy.controllers.formula_tools import parse_formula
from PyQt5.QtWidgets import QTextEdit


def test_simple_linear_formula():
    formula = "y = a * x + b"
    expression = parse_formula(formula)
    assert isinstance(expression, str)
    assert "a" in expression and "x" in expression and "b" in expression


def test_complex_math_expression():
    formula = "y = a * sin(b * x + c) + d * log(abs(x)) + e * exp(-x**2)"
    expression = parse_formula(formula)
    assert isinstance(expression, str)
    assert all(
        symbol in expression
        for symbol in ["a", "b", "x", "c", "d", "e", "log", "exp", "sin"]
    )


def test_2d_surface_formula():
    formula = "z = a * x**2 + b * y + c * sin(x*y) + d"
    expression = parse_formula(formula)
    assert isinstance(expression, str)
    assert all(symbol in expression for symbol in ["x", "y", "a", "b", "c", "d", "sin"])


@pytest.fixture
def mock_parent():
    parent = MagicMock()
    parent.fit_options_dialog.update_params_tab = MagicMock()
    parent.fit_control.manual_button.setText = MagicMock()
    parent.manual_control.dock_manual.isHidden.return_value = False
    return parent


@pytest.fixture
def formula_text():
    return QTextEdit()


def test_update_formula_by_mode(formula_text, mock_parent):
    manager = FitFormulaManager(mock_parent, formula_text)
    manager.update_formula_by_mode("1D")
    assert formula_text.toPlainText() == "y = a * x + b"

    manager.update_formula_by_mode("2D")
    assert formula_text.toPlainText() == "z = a * x + y"

    manager.update_formula_by_mode("unknown")
    assert formula_text.toPlainText() == ""


@patch("gcfpy.controllers.fit_formula.import_python_function")
@patch("gcfpy.controllers.fit_formula.QFileDialog.getOpenFileName")
def test_import_formula_success(
    mock_get_open, mock_import_func, formula_text, mock_parent
):
    manager = FitFormulaManager(mock_parent, formula_text)
    mock_get_open.return_value = ("fake.py", "")
    mock_import_func.return_value = "y = a * x + b"

    manager.import_formula()

    assert formula_text.toPlainText() == "y = a * x + b"
    mock_parent.fit_options_dialog.update_params_tab.assert_called_once()
    mock_parent.fit_control.manual_button.setText.assert_called_once_with("Manual")


@patch("gcfpy.controllers.fit_formula.import_python_function")
@patch("gcfpy.controllers.fit_formula.QFileDialog.getOpenFileName")
@patch("gcfpy.controllers.fit_formula.QMessageBox")
def test_import_formula_error(
    mock_msgbox, mock_get_open, mock_import_func, formula_text, mock_parent
):
    manager = FitFormulaManager(mock_parent, formula_text)
    mock_get_open.return_value = ("invalid.py", "")
    mock_import_func.return_value = "### ERROR something went wrong"

    manager.import_formula()

    assert formula_text.toPlainText() == ""
    mock_msgbox.return_value.exec_.assert_called_once()


@patch("gcfpy.controllers.fit_formula.save_python_code")
@patch("gcfpy.controllers.fit_formula.QFileDialog.getSaveFileName")
def test_export_formula_success(
    mock_get_save, mock_save_code, formula_text, mock_parent
):
    formula_text.setPlainText("y = a * x + b")
    manager = FitFormulaManager(mock_parent, formula_text)
    mock_get_save.return_value = ("output.py", "")
    mock_save_code.return_value = ""

    manager.export_formula()
    mock_save_code.assert_called_once_with("y = a * x + b", "output.py")


@patch("gcfpy.controllers.fit_formula.save_python_code")
@patch("gcfpy.controllers.fit_formula.QFileDialog.getSaveFileName")
@patch("gcfpy.controllers.fit_formula.QMessageBox")
def test_export_formula_error(
    mock_msgbox, mock_get_save, mock_save_code, formula_text, mock_parent
):
    formula_text.setPlainText("y = a * x + b")
    manager = FitFormulaManager(mock_parent, formula_text)
    mock_get_save.return_value = ("bad.py", "")
    mock_save_code.return_value = "Permission denied"

    manager.export_formula()
    mock_msgbox.return_value.exec_.assert_called_once()
