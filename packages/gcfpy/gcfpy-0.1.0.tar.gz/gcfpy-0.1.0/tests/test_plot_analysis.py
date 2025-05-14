from unittest.mock import MagicMock

import numpy as np
import pytest
from gcfpy.widgets.plot_analysis import PlotAnalysis


class DummyPlotWidget:
    def __init__(self):
        self.data_x = np.linspace(0, 10, 10)
        self.data_y = np.sin(self.data_x)
        self.fit_y = np.cos(self.data_x)
        self.confidence_band = 0.1 * np.ones_like(self.data_x)
        self.result = MagicMock()
        self.minimizer = MagicMock()
        self.parent = MagicMock()
        self.canvas_res = MagicMock()
        self.canvas_conf = MagicMock()
        self.canvas_decomp = MagicMock()
        self.canvas_2d = MagicMock()
        self.fig_2d = MagicMock()
        self.ax_res = MagicMock()
        self.ax_conf = MagicMock()
        self.ax_decomp = MagicMock()
        self.tab_manager = MagicMock()
        self.tab_manager.get_tab.return_value = MagicMock()
        self.tab_manager.get_tab.return_value.layout = MagicMock()
        self.tab_manager.ensure_tab_exists = MagicMock()
        self.add_matplotlib_toolbar = MagicMock()
        self.show_confidence = False


@pytest.fixture
def analysis():
    dummy_widget = DummyPlotWidget()
    return PlotAnalysis(dummy_widget)


def test_get_selected_data_full(analysis):
    x, y, fit = analysis._get_selected_data()
    assert isinstance(x, np.ndarray)
    assert isinstance(y, np.ndarray)
    assert isinstance(fit, np.ndarray)


def test_get_selected_data_with_conf(analysis):
    x, y, fit, conf = analysis._get_selected_data(include_conf=True)
    assert isinstance(conf, np.ndarray)


def test_toggle_fit_decomposition_no_result():
    widget = DummyPlotWidget()
    widget.result = None
    plot_analysis = PlotAnalysis(widget)
    plot_analysis.toggle_fit_decomposition()  # should not raise


def test_toggle_residuals_plot_no_fit():
    widget = DummyPlotWidget()
    widget.fit_y = None
    plot_analysis = PlotAnalysis(widget)
    plot_analysis.toggle_residuals_plot()  # should not raise


def test_toggle_confidence_band_no_fit():
    widget = DummyPlotWidget()
    widget.fit_y = None
    plot_analysis = PlotAnalysis(widget)
    plot_analysis.toggle_confidence_band()  # should not raise


def test_plot_conf_interval_2d_not_enough_params():
    widget = DummyPlotWidget()
    widget.result.params = {"a": MagicMock()}
    plot_analysis = PlotAnalysis(widget)
    plot_analysis.plot_widget.result = widget.result
    plot_analysis.plot_widget.minimizer = MagicMock()
    plot_analysis.plot_conf_interval_2d()  # should not raise
