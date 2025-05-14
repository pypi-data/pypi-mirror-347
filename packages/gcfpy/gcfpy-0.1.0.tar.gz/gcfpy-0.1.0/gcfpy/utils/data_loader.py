import os

import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class DataLoader:
    """
    Handles data loading from CSV files into the application.
    """

    def __init__(self, parent):
        """
        Initializes the DataLoader.

        Args:
            parent: The parent widget (typically MainWindow).

        """
        self.parent = parent
        self.df = None

    def load_data(self, file_path=None):
        """
        Opens a file dialog to load a CSV file, or uses a given file path.

        Returns:
            tuple: (DataFrame, file_path) if successful, else (None, None)

        """
        if file_path is None:
            file_path, _ = QFileDialog.getOpenFileName(
                self.parent,
                "Load Data File ueuieuueuç",
                "",
                "CSV Files (*.csv);;HDF5 Files (*.h5 *.hdf5);;All Files (*)",
            )

        if not file_path:
            return None, None

        if file_path.lower().endswith(".csv"):
            df = self.read_csv(file_path)
        else:
            print(f"Unsupported file format: {file_path}")
            return None, None
        if df is not None:
            self.df = df
            self._update_toolbar_on_load()
            return df, file_path

        return None, None

    def read_csv(self, file_path):
        """
        Reads a CSV file and validates its format.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            pd.DataFrame or None: Validated dataframe or None if error.

        """
        try:
            df = pd.read_csv(file_path)

            if not {"X", "Y"}.issubset(df.columns):
                self._show_error("CSV must contain columns 'X' and 'Y'.")
                return None

            if df["X"].isnull().any() or df["Y"].isnull().any():
                self._show_error("CSV contains missing values in 'X' or 'Y'.")
                return None

            return df

        except Exception as e:
            self._show_error(f"Failed to load CSV file: {e}")
            return None

    def _update_toolbar_on_load(self):
        """
        Updates the toolbar and plot widgets after successful data load.
        """
        fit_tab = self.parent.get_current_fit_tab()

        # Reset fit comparison
        if hasattr(fit_tab, "comparison_manager"):
            fit_tab.comparison_manager.toggle_comparison_mode(False)
            fit_tab.comparison_manager.reset()

        # Reset xmin/xmax tool
        if hasattr(fit_tab.plot_widget, "xmin_xmax_tool"):
            fit_tab.plot_widget.xmin_xmax_tool.reset_xmin_xmax()

        # Safely update toolbar state
        toolbar = self.parent.toolbar
        if hasattr(toolbar, "set_xmin_xmax_action"):
            toolbar.set_xmin_xmax_action.setChecked(False)
        toolbar.enable_toolbar_options(True)
        toolbar.enable_toolbar_plot_options(False)
        toolbar.enable_comparison(False)

    def _show_error(self, message):
        """
        Displays an error message in a dialog.

        Args:
            message (str): The error message.

        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def get_previous_file(self):
        """
        Loads the last used file path if recorded.

        Returns:
            str or None: File path if found, else None.

        """
        if self.prev_data_file and os.path.exists(self.prev_data_file):
            try:
                with open(self.prev_data_file, "r") as f:
                    return f.read().strip()
            except Exception as e:
                print(f"[Error] Failed to read previous file: {e}")

        return None
