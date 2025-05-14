import ast
import json
import os

from sympy import Add, expand, symbols, sympify


def load_math_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "..", "utils", "math_config.json")
    with open(config_path, "r") as file:
        config = json.load(file)
    return config


math_config = load_math_config()

CONSTANTS = math_config["constants"]
MATH_FUNCTION_MAP = math_config["function_map"]
MATH_FUNCTIONS = set(MATH_FUNCTION_MAP.keys())


class MathTransformer(ast.NodeTransformer):
    """
    AST transformer that prefixes math functions with np. and allows known constants.
    """

    def visit_Name(self, node):
        if node.id in MATH_FUNCTIONS:
            return ast.copy_location(
                ast.Attribute(
                    value=ast.Name(id="np", ctx=ast.Load()),
                    attr=node.id,
                    ctx=node.ctx,
                ),
                node,
            )
        elif node.id in CONSTANTS:
            return ast.copy_location(ast.Name(id=node.id, ctx=ast.Load()), node)
        return node


def parse_formula(formula):
    """
    Converts a math formula into valid Python/NumPy syntax using AST.

    Args:
        formula (str): A string like "y = a * sin(x) + b".

    Returns:
        str: A Python expression like "a * np.sin(x) + b".

    """
    try:
        rhs = formula.split("=")[1].strip()
        rhs = rhs.replace("^", "**")
        tree = ast.parse(rhs, mode="eval")
        tree = MathTransformer().visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
    except Exception as e:
        return f"### ERROR: Invalid formula - {e}"


def extract_parameters(formula):
    """
    Extracts symbolic parameters from the formula, excluding known symbols.

    Args:
        formula (str): A string like "y = a * sin(x) + b".

    Returns:
        list[str]: List of variable names like ["a", "b"].

    """
    try:
        expr = formula.split("=")[1].strip() if "=" in formula else formula
        sym_expr = sympify(expr)
        return sorted(
            str(sym)
            for sym in sym_expr.free_symbols
            if str(sym) not in {"x", "y", "np"} | MATH_FUNCTIONS | CONSTANTS.keys()
        )
    except Exception:
        return []


def decompose_formula(formula):
    """
    Splits a formula into separate NumPy-compatible components.

    Args:
        formula (str): A formula string like "y = a * sin(x) + b".

    Returns:
        list[str]: List of decomposed terms as strings.

    """
    try:
        x = symbols("x")
        expr = sympify(formula.split("=")[1].strip().replace("^", "**"))
        terms = Add.make_args(expand(expr))

        dependent = []
        independent = []

        for term in terms:
            term_str = str(term)
            for sympy_func, np_func in MATH_FUNCTION_MAP.items():
                term_str = term_str.replace(sympy_func, np_func)

            if term.has(x):
                dependent.append(term_str)
            else:
                independent.append(term_str)

        if independent:
            const_term = " + ".join(independent)
            dependent.append(f"0*x + ({const_term})")

        return dependent

    except Exception as e:
        return [f"### ERROR: Invalid formula - {e}"]
