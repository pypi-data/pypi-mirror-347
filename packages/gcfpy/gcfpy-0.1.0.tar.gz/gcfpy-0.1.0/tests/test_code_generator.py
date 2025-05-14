import os
import tempfile

import pytest
from gcfpy.controllers.code_generator import (
    generate_python_code,
    import_python_function,
    save_python_code,
)


def test_generate_python_code_y_equals_expr():
    formula = "y = a * x + b"
    code = generate_python_code(formula)
    assert "def fit_function(x, a, b):" in code
    assert "return a * x + b" in code


def test_generate_python_code_z_equals_expr():
    formula = "z = a * x + b * y + c"
    code = generate_python_code(formula)
    assert "def fit_function(x, y, a, b, c):" in code
    assert "return a * x + b * y + c" in code


def test_generate_python_code_invalid_formula():
    with pytest.raises(ValueError):
        generate_python_code("invalid_formula")


def test_save_python_code_creates_file():
    formula = "y = a * x + b"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp_path = tmp.name
    save_python_code(formula, tmp_path)
    with open(tmp_path, "r", encoding="utf-8") as f:
        content = f.read()
    os.remove(tmp_path)
    assert "def fit_function(x, a, b):" in content


def test_save_python_code_ioerror(monkeypatch):
    monkeypatch.setattr(
        "builtins.open",
        lambda *args, **kwargs: (_ for _ in ()).throw(OSError("IO error")),
    )
    with pytest.raises(OSError):
        save_python_code("y = a * x", "bad_path.py")


def test_import_python_function_extracts_return():
    content = """
import numpy as np

def fit_function(x, a, b):
    return np.sin(a * x + b)
"""
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".py", mode="w", encoding="utf-8"
    ) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    formula = import_python_function(tmp_path)
    os.remove(tmp_path)
    assert formula == "y = sin(a * x + b)"


def test_import_python_function_missing_return():
    content = """
def fit_function(x, a):
    pass
"""
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".py", mode="w", encoding="utf-8"
    ) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    with pytest.raises(ValueError):
        import_python_function(tmp_path)
    os.remove(tmp_path)


def test_import_python_function_ioerror(monkeypatch):
    monkeypatch.setattr(
        "builtins.open",
        lambda *args, **kwargs: (_ for _ in ()).throw(OSError("read error")),
    )
    with pytest.raises(OSError):
        import_python_function("nonexistent.py")
