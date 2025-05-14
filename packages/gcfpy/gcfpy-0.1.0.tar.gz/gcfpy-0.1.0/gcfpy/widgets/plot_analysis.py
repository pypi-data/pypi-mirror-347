import itertools

import lmfit
import matplotlib.pyplot as plt
import numpy as np

from gcfpy.controllers.formula_tools import decompose_formula


class PlotAnalysis:
    """
    Handles residuals, fit decomposition, 2D confidence contours, and fit comparison.
    """

    def __init__(self, plot_widget):
        """
        Initializes the analysis plot handler.

        Args:
            plot_widget (PlotWidget): The main plot widget instance.

        """
        self.plot_widget = plot_widget

    def toggle_residuals_plot(self):
        """Displays or hides residuals considering Xmin/Xmax and Multi 1D mode."""
        mode = getattr(
            self.plot_widget.parent.get_current_fit_tab(), "current_mode", "1D"
        )
        fit_tab = self.plot_widget.parent.get_current_fit_tab()

        if mode == "2D":
            strategy = fit_tab.fit_control.get_current_strategy()
        else:
            strategy = None

        self.plot_widget.tab_manager.ensure_tab_exists(
            "Residuals", "fig_res", "ax_res", "canvas_res"
        )
        self.plot_widget.ax_res.clear()

        if mode == "2D" and strategy == "Fit per Y":
            # --- Multi 1D Mode ---
            df = getattr(self.plot_widget.parent.get_current_fit_tab(), "df", None)
            best_fit = self.plot_widget.fit_y
            if df is None or best_fit is None:
                print("Multi 1D: Missing dataframe or fit.")
                return

            x = df["X"].values
            y = df["Y"].values
            z = df["Z"].values
            residuals = z - best_fit

            unique_y = np.unique(y)
            for y_val in unique_y:
                mask = y == y_val
                self.plot_widget.ax_res.scatter(
                    x[mask],
                    residuals[mask],
                    label=f"Y={y_val:.2f}",
                    alpha=0.6,
                    s=10,
                )

            self.plot_widget.ax_res.axhline(
                0, color="black", linestyle="--", linewidth=1
            )
            self.plot_widget.ax_res.set_ylabel("Residuals")
            self.plot_widget.ax_res.set_xlabel("X")
            self.plot_widget.ax_res.legend()
        else:
            # --- 1D classique ---
            if self.plot_widget.fit_y is None:
                print("No fit available, cannot display residuals.")
                return

            x_values, y_values, fit_values = self._get_selected_data()
            residuals = y_values - fit_values

            self.plot_widget.ax_res.scatter(
                x_values,
                residuals,
                color="purple",
                marker="x",
                label="Residuals",
            )
            self.plot_widget.ax_res.axhline(
                0, color="black", linestyle="--", linewidth=1
            )
            self.plot_widget.ax_res.set_ylabel("Residuals")
            self.plot_widget.ax_res.set_xlabel("X")
            self.plot_widget.ax_res.legend()

        self.plot_widget.canvas_res.draw()
        tab = self.plot_widget.tab_manager.get_tab("Residuals")
        if tab is not None:
            self.plot_widget.add_matplotlib_toolbar(
                self.plot_widget.canvas_res, tab.layout()
            )

    def toggle_confidence_band(self):
        """Displays or hides the 3sigma confidence band for 1D and Multi 1D fits."""
        mode = getattr(
            self.plot_widget.parent.get_current_fit_tab(), "current_mode", "1D"
        )
        fit_tab = self.plot_widget.parent.get_current_fit_tab()
        strategy = fit_tab.fit_control.get_current_strategy()

        self.plot_widget.tab_manager.ensure_tab_exists(
            "99% Confidence", "fig_conf", "ax_conf", "canvas_conf"
        )
        ax = self.plot_widget.ax_conf
        ax.clear()

        self.plot_widget.show_confidence = not self.plot_widget.show_confidence

        if mode == "2D" and strategy == "Fit per Y":
            # Multi 1D mode
            df = self.plot_widget.parent.get_current_fit_tab().df
            if df is None or self.plot_widget.fit_y is None:
                print("No fit or data available.")
                return

            x = df["X"].values
            y = df["Y"].values
            z = df["Z"].values
            fit = self.plot_widget.fit_y
            conf = self.plot_widget.confidence_band
            # if fit is None or conf is None:
            #     print("No confidence band for Multi 1D.")
            #     return

            unique_y = np.unique(y)
            for y_val in unique_y:
                mask = y == y_val
                x_vals = x[mask]
                z_vals = z[mask]
                fit_vals = fit[mask]
                lower = (
                    fit_vals - conf[0][mask]
                    if isinstance(conf, tuple)
                    else fit_vals - conf[mask]
                )
                upper = (
                    fit_vals + conf[1][mask]
                    if isinstance(conf, tuple)
                    else fit_vals + conf[mask]
                )

                ax.plot(
                    x_vals,
                    z_vals,
                    "o",
                    color="blue",
                    label=f"Data @Y={y_val:.2f}",
                )
                ax.plot(
                    x_vals,
                    fit_vals,
                    "--",
                    color="red",
                    label=f"Fit @Y={y_val:.2f}",
                )

                if self.plot_widget.show_confidence:
                    ax.fill_between(
                        x_vals,
                        lower,
                        upper,
                        color="red",
                        alpha=0.2,
                    )

        else:
            # Standard 1D fit
            if (
                self.plot_widget.fit_y is None
                or self.plot_widget.confidence_band is None
            ):
                print("No fit or confidence data available.")
                return

            x_values, y_values, fit_values, conf_band = self._get_selected_data(
                include_conf=True
            )

            ax.plot(
                self.plot_widget.data_x,
                self.plot_widget.data_y,
                "o",
                color="blue",
                label="Data",
            )
            ax.plot(x_values, fit_values, "--", color="red", label="Fit")

            if self.plot_widget.show_confidence:
                ax.fill_between(
                    x_values,
                    fit_values - conf_band,
                    fit_values + conf_band,
                    color="red",
                    alpha=0.2,
                    zorder=5,
                )

        # ax.legend()
        self.plot_widget.canvas_conf.draw()

        tab = self.plot_widget.tab_manager.get_tab("99% Confidence")
        if tab is not None:
            self.plot_widget.add_matplotlib_toolbar(
                self.plot_widget.canvas_conf, tab.layout()
            )

    def toggle_fit_decomposition(self):
        """Displays the fit decomposition considering Xmin/Xmax."""
        if self.plot_widget.result is None:
            print("No fit result available.")
            return

        self.plot_widget.tab_manager.ensure_tab_exists(
            "Fit Decomposition", "fig_decomp", "ax_decomp", "canvas_decomp"
        )
        self.plot_widget.ax_decomp.clear()

        x_values, y_values, fit_values = self._get_selected_data()
        fit_tab = self.plot_widget.parent.get_current_fit_tab()

        if not hasattr(fit_tab, "formula_text"):
            print("Cannot access formula_text.")
            return

        formula = fit_tab.formula_text.toPlainText().strip().replace("-", "+-")
        terms = decompose_formula(formula)
        result = self.plot_widget.result

        if isinstance(result, dict):
            param_values = result.get("params", {})
        else:
            param_values = {p: result.params[p].value for p in result.params}

        colors = ["red", "green", "purple", "orange", "brown"]
        y_fit_total = np.zeros_like(x_values, dtype=float)

        for i, term in enumerate(terms):
            try:
                display_term = term
                if "x" not in term:
                    term = f"0*x + ({term})"

                x_values = x_values.astype(float)
                fit_y = eval(term, {"np": np, "x": x_values}, param_values)
                y_fit_total += fit_y

                self.plot_widget.ax_decomp.plot(
                    x_values,
                    fit_y,
                    "--",
                    color=colors[i % len(colors)],
                    label=f"{display_term}",
                )
            except Exception as e:
                print(f"Error evaluating term `{term}`: {e}")

        # data plot
        self.plot_widget.ax_decomp.plot(
            self.plot_widget.data_x,
            self.plot_widget.data_y,
            marker="o",
            linestyle="none",
            color="blue",
            label="Data",
        )

        self.plot_widget.ax_decomp.plot(
            x_values,
            y_fit_total,
            "-",
            color="black",
            linewidth=2,
            label="Total Fit",
        )
        self.plot_widget.ax_decomp.legend()
        self.plot_widget.canvas_decomp.draw()
        tab = self.plot_widget.tab_manager.get_tab("Fit Decomposition")
        if tab is not None:
            self.plot_widget.add_matplotlib_toolbar(
                self.plot_widget.canvas_decomp, tab.layout()
            )

    def plot_conf_interval_2d(self):
        """Displays 2D confidence contours as subplots."""
        self.plot_widget.tab_manager.ensure_tab_exists(
            "2D Confidence Contours", "fig_2d", "ax_2d", "canvas_2d"
        )

        if self.plot_widget.result is None or self.plot_widget.minimizer is None:
            print("No fit result available.")
            return

        param_names = list(self.plot_widget.result.params.keys())
        param_pairs = list(itertools.combinations(param_names, 2))

        if not param_pairs:
            print("Not enough parameters for 2D confidence contour.")
            return

        num_pairs = len(param_pairs)
        num_cols = 2
        num_rows = (num_pairs + num_cols - 1) // num_cols
        if num_pairs == 1:
            fig, axes = plt.subplots(figsize=(7, 5))
            axes = [axes]
        else:
            fig, axes = plt.subplots(num_rows, num_cols, figsize=(7, 5))
            axes = axes.flatten()

        colors = ["#2030b0", "#b02030", "#207070"]
        sigma_levels = [1, 2, 3]

        for i, (param_x, param_y) in enumerate(param_pairs):
            ax = axes[i]
            ci_x, ci_y, prob = lmfit.conf_interval2d(
                self.plot_widget.minimizer,
                self.plot_widget.result,
                param_x,
                param_y,
                nx=10,
                ny=10,
            )
            cnt = ax.contour(ci_x, ci_y, prob, levels=sigma_levels, colors=colors)
            ax.clabel(cnt, inline=True, fmt=r"$\sigma=%.0f$", fontsize=10)
            ax.set_xlabel(param_x)
            ax.set_ylabel(param_y)
        fig.tight_layout()
        self.plot_widget.fig_2d = fig
        self.plot_widget.canvas_2d.figure = fig
        self.plot_widget.canvas_2d.draw()
        tab = self.plot_widget.tab_manager.get_tab("2D Confidence Contours")
        if tab is not None:
            self.plot_widget.add_matplotlib_toolbar(
                self.plot_widget.canvas_2d, tab.layout()
            )

    def _get_selected_data(self, include_conf=False):
        """
        Returns selected or full data, optionally including confidence band.
        Handles Xmin/Xmax selection safely, including for emcee with confidence tuple.

        Returns:
            (x, y, fit[, conf])

        """
        x_all = self.plot_widget.data_x
        y_all = self.plot_widget.data_y
        fit_all = self.plot_widget.fit_y
        conf_all = self.plot_widget.confidence_band
        selected = getattr(self.plot_widget, "selected_x", None)

        # No selection
        if selected is None:
            return (
                (x_all, y_all, fit_all, conf_all)
                if include_conf
                else (x_all, y_all, fit_all)
            )

        # Create mask
        mask = np.isin(x_all, selected)

        # Filter x/y
        x_vals = x_all[mask]
        y_vals = y_all[mask]

        # Only slice fit/conf if same size as data
        fit_vals = (
            fit_all[mask]
            if fit_all is not None and fit_all.shape == x_all.shape
            else fit_all
        )

        if include_conf:
            if conf_all is None:
                conf_vals = None
            elif isinstance(conf_all, tuple) and len(conf_all) == 2:
                lower, upper = conf_all
                conf_vals = (
                    lower[mask] if lower.shape == x_all.shape else lower,
                    upper[mask] if upper.shape == x_all.shape else upper,
                )
            elif isinstance(conf_all, np.ndarray):
                conf_vals = (
                    conf_all[mask] if conf_all.shape == x_all.shape else conf_all
                )
            else:
                conf_vals = conf_all
            return x_vals, y_vals, fit_vals, conf_vals

        return x_vals, y_vals, fit_vals

    def get_param_values(self):
        """
        Returns a dictionary of parameter names and values, regardless of fit method.
        """
        if hasattr(self.plot_widget.result, "params"):  # lmfit
            return {name: self.result.params[name].value for name in self.result.params}
        elif isinstance(self.result, dict) and "params" in self.result:
            return self.result["params"]  # emcee or odr
        return {}
