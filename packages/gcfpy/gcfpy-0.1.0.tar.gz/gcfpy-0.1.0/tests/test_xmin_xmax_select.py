import numpy as np
import pandas as pd
import pytest
from gcfpy.app.main_window import MainWindow
from matplotlib.backend_bases import MouseEvent


@pytest.mark.parametrize("method", ["leastsq"])
def test_xmin_xmax_selection_1d(qtbot, tmp_path, method):
    # Prépare des données simples
    x = np.linspace(0, 10, 100)
    y = 2 * x + 1
    df = pd.DataFrame({"X": x, "Y": y})
    csv_path = tmp_path / "test_data.csv"
    df.to_csv(csv_path, index=False)

    # Lance l'application
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()
    fit_tab.load_data_into_tab(df, file_path=str(csv_path))

    # Active le mode Xmin/Xmax
    fit_tab.plot_widget.xmin_xmax.enable_xmin_xmax_selection()
    assert fit_tab.plot_widget.xmin_xmax.xmin_xmax_mode is True

    # Simule deux clics : Xmin = 2, Xmax = 8
    canvas = fit_tab.plot_widget.canvas

    def simulate_click(x_val):
        event = MouseEvent(
            name="button_press_event",
            canvas=canvas,
            x=0,  # coordonnée écran (non utilisée ici)
            y=0,
            button=1,
            key=None,
            step=0,
            dblclick=False,
            guiEvent=None,
        )
        event.xdata = x_val
        event.ydata = 2 * x_val + 1
        return event

    fit_tab.plot_widget.xmin_xmax.on_click_xmin_xmax(simulate_click(2))
    fit_tab.plot_widget.xmin_xmax.on_click_xmin_xmax(simulate_click(8))

    # Vérifie les données sélectionnées
    xminmax = fit_tab.plot_widget.xmin_xmax
    selected_x = fit_tab.plot_widget.selected_x
    selected_y = fit_tab.plot_widget.selected_y

    assert xminmax.xmin_line == 2
    assert xminmax.xmax_line == 8
    assert selected_x is not None and selected_y is not None
    assert np.all((selected_x >= 2) & (selected_x <= 8))
    assert np.all((selected_y >= 2 * 2 + 1) & (selected_y <= 2 * 8 + 1))

    # Reset
    xminmax.reset_xmin_xmax()
    assert fit_tab.plot_widget.selected_x is None
    assert fit_tab.plot_widget.selected_y is None


def simulate_click(canvas, x_val, y_val=0):
    event = MouseEvent(
        name="button_press_event",
        canvas=canvas,
        x=0,
        y=0,
        button=1,
        key=None,
        step=0,
        dblclick=False,
        guiEvent=None,
    )
    event.xdata = x_val
    event.ydata = y_val
    return event


@pytest.mark.parametrize("strategy", ["Fit per Y"])
def test_xmin_xmax_selection_multi1d(qtbot, tmp_path, strategy):
    # Données 2D simples : Z = aX + bY + c
    x = np.tile(np.linspace(0, 10, 50), 5)
    y = np.repeat(np.arange(5), 50)
    z = 2 * x + 3 * y + 5
    df = pd.DataFrame({"X": x, "Y": y, "Z": z})
    csv_path = tmp_path / "test_data.csv"
    df.to_csv(csv_path, index=False)

    # Lance l'application
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.add_fit_tab()
    fit_tab = window.get_current_fit_tab()
    fit_tab.load_data_into_tab(df, file_path=str(csv_path))

    # Change la stratégie
    fit_tab.fit_control.strategy_selector.setCurrentText(strategy)
    assert fit_tab.fit_control.get_current_strategy() == strategy

    # Active la sélection Xmin/Xmax
    xminmax = fit_tab.plot_widget.xmin_xmax
    xminmax.enable_xmin_xmax_selection()
    assert xminmax.xmin_xmax_mode is True

    # Clics simulés sur le canvas multi1d : Xmin = 2.0, Xmax = 8.0
    canvas = fit_tab.plot_widget.canvas_multi1d
    xminmax.on_click_xmin_xmax(simulate_click(canvas, x_val=2.0))
    xminmax.on_click_xmin_xmax(simulate_click(canvas, x_val=8.0))

    # Vérifie les données sélectionnées
    sx = fit_tab.plot_widget.selected_x
    sy = fit_tab.plot_widget.selected_y
    sz = fit_tab.plot_widget.selected_z

    assert sx is not None and len(sx) > 0
    assert sy is not None and len(sy) == len(sx)
    assert sz is not None and len(sz) == len(sx)
    assert np.all((sx >= 2.0) & (sx <= 8.0))
    assert np.all(np.isin(sy, y))  # tous les Y présents doivent être valides

    # Reset
    xminmax.reset_xmin_xmax()
    assert fit_tab.plot_widget.selected_x is None
    assert fit_tab.plot_widget.selected_y is None
