from PyQt5.QtWidgets import QDockWidget


class BaseDockWidget(QDockWidget):
    """
    A reusable dock widget that hides itself instead of being closed
    when the user clicks the close button (X).
    """

    def closeEvent(self, event):
        self.hide()
        event.ignore()
