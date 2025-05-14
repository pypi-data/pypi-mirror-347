from gcfpy.controllers.fit_options import FitOptionsWindow


def test_fit_options_window_launch(qtbot):
    """Check that FitOptionsWindow can be instantiated and shown."""
    window = FitOptionsWindow()
    qtbot.addWidget(window)
    window.show()
    assert window.isVisible()
