from unittest.mock import MagicMock

from gcfpy.controllers.fit_processor import FitProcessor


def test_generate_fit_function_and_prepare_parameters():
    # formule de test
    formula = "y = A * exp(-B * x)"

    # fake fit_options_dialog
    mock_dialog = MagicMock()
    mock_dialog.get_params_options.return_value = {
        "A": {"p0": 2.5, "bounds": (0, 10)},
        "B": {"p0": 0.4, "bounds": (0, 5)},
    }

    processor = FitProcessor(fit_options_dialog=mock_dialog)

    # génère la fonction Python
    fit_func = processor.generate_fit_function(formula)
    assert callable(fit_func)

    # génère les paramètres pour lmfit
    params = processor.prepare_parameters(formula)
    assert "A" in params and "B" in params
    assert params["A"].value == 2.5
    assert params["A"].min == 0
    assert params["A"].max == 10
