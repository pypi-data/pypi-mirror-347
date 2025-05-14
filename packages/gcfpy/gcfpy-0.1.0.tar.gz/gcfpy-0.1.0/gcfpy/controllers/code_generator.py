import re

from .formula_tools import CONSTANTS, extract_parameters, parse_formula


def generate_python_code(formula):
    """
    Generate valid Python code for a fit function based on the given formula.

    Returns:
        str: Python code string defining the fit function.

    """
    parsed_formula = parse_formula(formula)
    if "### ERROR" in parsed_formula:
        raise ValueError("Invalid formula: could not parse.")

    parameters = extract_parameters(formula)
    constants = [
        f"    {key} = {value}" for key, value in CONSTANTS.items() if key in formula
    ]

    independent_vars = []
    if "y=" in formula or "y =" in formula:
        independent_vars.append("x")
    if "z =" in formula or "z=" in formula:
        independent_vars.extend(["x", "y"])
    args_str = ", ".join(independent_vars + parameters)

    code = (
        "import numpy as np\n\n"
        f"def fit_function({args_str}):\n"
        f"{chr(10).join(constants)}\n"
        f"    return {parsed_formula.strip()}\n"
    )
    return code


def save_python_code(formula, file_path):
    """
    Generate and save the Python function to a .py file.

    Args:
        formula (str): The mathematical formula to parse.
        file_path (str): Path to the output .py file.

    Returns:
        None if successful.

    Raises:
        ValueError: If the formula is invalid.
        IOError: If the file could not be saved.

    """
    python_code = generate_python_code(formula)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(python_code)
    except Exception as e:
        raise IOError(f"Could not write file '{file_path}': {e}")


def import_python_function(file_path):
    """
    Import a formula string from a Python file containing a fit_function.

    Returns:
        str: A formula like "y = a*sin(x)"

    Raises:
        ValueError: If no return statement is found.
        IOError: If the file could not be read.

    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        raise IOError(f"Could not read file: {e}")

    inside_function = False
    for line in lines:
        line = line.strip()
        if line.startswith("def fit_function("):
            inside_function = True
        elif inside_function and line.startswith("return "):
            expr = line[len("return ") :].strip()
            expr = re.sub(r"np\.", "", expr)
            return f"y = {expr}"

    raise ValueError("No return statement found in fit_function().")
