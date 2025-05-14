import numpy as np
from matplotlib.widgets import Cursor


class PlotXminXmax:
    """Handles the Xmin/Xmax selection for filtering data in PlotWidget."""

    def __init__(self, plot_widget):
        """
        Initializes the Xmin/Xmax selection tool.

        Args:
            plot_widget (PlotWidget): The main plot widget instance.

        """
        self.plot_widget = plot_widget
        self.plot_widget.xmin_xmax = self  # Direct reference
        self.xmin_xmax_mode = False
        self.xmin_line = None
        self.xmax_line = None
        self.selection_patch = None
        self.selected_indices = None
        self.cursor_event = None
        self.xmin_line = None
        self.xmax_line = None

    def enable_xmin_xmax_selection(self):
        """Activates Xmin/Xmax selection mode."""
        if self.xmin_xmax_mode:
            self.disable_xmin_xmax_selection()
            return

        mode = getattr(
            self.plot_widget.parent.get_current_fit_tab(), "current_mode", "1D"
        )

        fit_tab = self.plot_widget.parent.get_current_fit_tab()
        strategy = fit_tab.fit_control.get_current_strategy()

        if mode == "2D" and strategy == "Fit per Y":
            df = self.plot_widget.parent.get_current_fit_tab().df
            if df is None or "X" not in df or "Z" not in df:
                print("Error: Missing X/Z columns for multi 1D selection.")
                return

            self.plot_widget.ax_multi1d.clear()
            self.plot_widget.ax_multi1d.scatter(
                df["X"], df["Z"], color="blue", label="Data"
            )

            self.cursor = Cursor(
                self.plot_widget.ax_multi1d,
                useblit=True,
                color="black",
                linewidth=1,
            )
            self.cursor_event = self.plot_widget.canvas_multi1d.mpl_connect(
                "button_press_event", self.on_click_xmin_xmax
            )
            self.plot_widget.canvas_multi1d.draw()

        else:
            if self.plot_widget.data_x is None or self.plot_widget.data_y is None:
                print("Error: No data available for Xmin/Xmax selection.")
                return

            self.plot_widget.ax.clear()
            self.plot_widget.ax.scatter(
                self.plot_widget.data_x,
                self.plot_widget.data_y,
                color="blue",
                label="Data",
            )

            self.cursor = Cursor(
                self.plot_widget.ax, useblit=True, color="black", linewidth=1
            )
            self.cursor_event = self.plot_widget.canvas.mpl_connect(
                "button_press_event", self.on_click_xmin_xmax
            )
            self.plot_widget.canvas.draw()

        self.xmin_xmax_mode = True
        self.selected_indices = None

    def disable_xmin_xmax_selection(self):
        """Deactivates Xmin/Xmax selection and restores the plot."""
        self.xmin_xmax_mode = False
        self.xmin_line = None
        self.xmax_line = None
        self.selection_patch = None
        self.selected_indices = None
        self.plot_widget.selected_x = None
        self.plot_widget.selected_y = None

        # Disable cursor
        if hasattr(self, "cursor") and self.cursor is not None:
            if self.cursor_event is not None:
                self.plot_widget.canvas.mpl_disconnect(self.cursor_event)
            self.cursor = None

        self.plot_widget.ax.clear()
        self.plot_widget.ax.scatter(
            self.plot_widget.data_x,
            self.plot_widget.data_y,
            color="blue",
            label="Data",
        )
        self.plot_widget.ax.legend()

        self.plot_widget.canvas.draw()

    def on_click_xmin_xmax(self, event):
        """Handles click events to set Xmin/Xmax."""
        if not self.xmin_xmax_mode or event.xdata is None:
            return

        mode = getattr(
            self.plot_widget.parent.get_current_fit_tab(), "current_mode", "1D"
        )
        fit_tab = self.plot_widget.parent.get_current_fit_tab()
        strategy = fit_tab.fit_control.get_current_strategy()

        if self.xmin_line is None:
            # First click sets Xmin
            self.xmin_line = event.xdata
            if mode == "2D" and strategy == "Fit per Y":
                self.plot_widget.ax_multi1d.axvline(
                    self.xmin_line, color="black", linestyle="--", linewidth=1
                )
                self.plot_widget.canvas_multi1d.draw()
            else:
                self.plot_widget.ax.axvline(
                    self.xmin_line, color="black", linestyle="--", linewidth=1
                )
                self.plot_widget.canvas.draw()

        elif self.xmax_line is None:
            # Second click sets Xmax
            self.xmax_line = event.xdata
            if self.xmax_line < self.xmin_line:
                self.xmin_line, self.xmax_line = self.xmax_line, self.xmin_line

            if mode == "2D" and strategy == "Fit per Y":
                self.plot_widget.ax_multi1d.axvline(
                    self.xmax_line, color="black", linestyle="--", linewidth=1
                )
                self.plot_widget.canvas_multi1d.draw()
            else:
                self.plot_widget.ax.axvline(
                    self.xmax_line, color="black", linestyle="--", linewidth=1
                )
                self.plot_widget.canvas.draw()

            self.apply_xmin_xmax_selection()

    def apply_xmin_xmax_selection(self):
        """Filters data points between Xmin and Xmax."""
        if self.xmin_line is None or self.xmax_line is None:
            return
        mode = getattr(
            self.plot_widget.parent.get_current_fit_tab(), "current_mode", "1D"
        )

        fit_tab = self.plot_widget.parent.get_current_fit_tab()
        strategy = fit_tab.fit_control.get_current_strategy()

        if mode == "2D" and strategy == "Fit per Y":
            # Multi 1D
            df = self.plot_widget.parent.get_current_fit_tab().df
            x_all = df["X"].values
            y_all = df["Y"].values
            z_all = df["Z"].values
            unique_y = np.unique(y_all)

            selected_x, selected_y, selected_z = [], [], []
            for y_val in unique_y:
                mask_y = y_all == y_val
                x = x_all[mask_y]
                z = z_all[mask_y]
                mask_x = (x >= self.xmin_line) & (x <= self.xmax_line)
                if np.any(mask_x):
                    selected_x.extend(x[mask_x])
                    selected_y.extend([y_val] * np.sum(mask_x))
                    selected_z.extend(z[mask_x])

            if not selected_x:
                print("Warning: No points selected. Resetting selection.")
                self.reset_xmin_xmax()
                return

            self.plot_widget.selected_x = np.array(selected_x)
            self.plot_widget.selected_y = np.array(selected_y)
            self.plot_widget.selected_z = np.array(selected_z)
            print(
                f"{len(self.plot_widget.selected_x)}"
                + "points selected for multi-1D fitting."
            )

            # Update plot (Multi 1D = fig_multi1d)
            self.plot_widget.ax_multi1d.clear()
            self.plot_widget.ax_multi1d.scatter(
                x_all,
                z_all,
                color="red",
                marker="x",
                alpha=0.3,
                label="Excluded",
            )
            self.plot_widget.ax_multi1d.scatter(
                self.plot_widget.selected_x,
                self.plot_widget.selected_z,
                color="blue",
                label="Selected",
            )
            self.plot_widget.ax_multi1d.axvspan(
                self.xmin_line, self.xmax_line, color="black", alpha=0.2
            )
            self.plot_widget.ax_multi1d.legend()
            self.plot_widget.canvas_multi1d.draw()
            return

        self.selected_indices = np.where(
            (self.plot_widget.data_x >= self.xmin_line)
            & (self.plot_widget.data_x <= self.xmax_line)
        )[0]

        if len(self.selected_indices) == 0:
            print("Warning: No points selected. Resetting selection.")
            self.reset_xmin_xmax()
            return

        if self.plot_widget.fit_y is not None:
            self.plot_widget.selected_fit_y = self.plot_widget.fit_y[
                self.selected_indices
            ]
            self.plot_widget.selected_confidence_band = (
                self.plot_widget.confidence_band[self.selected_indices]
            )
        else:
            self.plot_widget.selected_fit_y = None
            self.plot_widget.selected_confidence_band = None

        self.plot_widget.selected_x = self.plot_widget.data_x[self.selected_indices]
        self.plot_widget.selected_y = self.plot_widget.data_y[self.selected_indices]

        print(f"{len(self.plot_widget.selected_x)} points selected for fitting.")

        # Update plot
        self.plot_widget.ax.clear()
        self.plot_widget.ax.scatter(
            self.plot_widget.data_x,
            self.plot_widget.data_y,
            color="red",
            marker="x",
            alpha=0.5,
            label="Excluded",
        )
        self.plot_widget.ax.scatter(
            self.plot_widget.selected_x,
            self.plot_widget.selected_y,
            color="blue",
            label="Selected",
        )

        self.selection_patch = self.plot_widget.ax.axvspan(
            self.xmin_line, self.xmax_line, color="black", alpha=0.2
        )

        self.plot_widget.ax.legend()
        self.plot_widget.canvas.draw()

    def reset_xmin_xmax(self):
        """Resets the Xmin/Xmax selection and restores the original data view."""
        self.xmin_line = None
        self.xmax_line = None
        self.selected_indices = None
        self.plot_widget.selected_x = None
        self.plot_widget.selected_y = None
        self.plot_widget.selected_fit_y = None

        self.plot_widget.ax.clear()
        self.plot_widget.ax.scatter(
            self.plot_widget.data_x,
            self.plot_widget.data_y,
            color="blue",
            label="Data",
        )

        self.plot_widget.ax.legend()
        self.plot_widget.canvas.draw()

        if hasattr(self, "cursor") and self.cursor is not None:
            try:
                self.plot_widget.canvas.mpl_disconnect(self.cursor)
            except Exception:
                pass

            self.cursor = None
