import corner
import matplotlib.pyplot as plt
import numpy as np


class MCMCPlot:
    """Handles all MCMC-related plots (corner plot, autocorrelation, walkers)."""

    def __init__(self, plot_widget):
        """
        Initializes the MCMCPlot handler.

        Args:
            plot_widget (PlotWidget): The main plot widget instance.

        """
        self.plot_widget = plot_widget
        self.mcmc_chains = None
        self.mcmc_params = None

    def plot_autocorrelation(self):
        """Autocorrelation for each parameter."""
        if self.mcmc_chains is None:
            return

        max_lag = min(100, len(self.mcmc_chains))
        ax = self.plot_widget.ax_auto
        ax.clear()

        for i, name in enumerate(self.mcmc_params):
            chain = self.mcmc_chains[:, i]
            autocorr = np.correlate(
                chain - chain.mean(), chain - chain.mean(), mode="full"
            )
            autocorr = autocorr[autocorr.size // 2 :]
            autocorr /= autocorr[0] if autocorr[0] != 0 else 1
            ax.plot(autocorr[:max_lag], label=name)

        ax.set_title("Autocorrelation")
        ax.legend()
        tab = self.plot_widget.tab_manager.get_tab("Autocorrelation")

        if tab is not None:
            self.plot_widget.add_matplotlib_toolbar(
                self.plot_widget.canvas_auto, tab.layout()
            )
        self.plot_widget.canvas_auto.draw()

    def plot_corner_plot(self):
        """Corner plot showing parameter distributions and correlations."""
        if self.mcmc_chains is None:
            return

        fig = corner.corner(self.mcmc_chains, labels=self.mcmc_params)
        self.plot_widget.fig_corner.clf()
        self.plot_widget.fig_corner = fig
        self.plot_widget.canvas_corner.figure = fig
        self.plot_widget.canvas_corner.draw()
        tab = self.plot_widget.tab_manager.get_tab("Corner Plot")
        if tab is not None:
            self.plot_widget.add_matplotlib_toolbar(
                self.plot_widget.canvas_corner, tab.layout()
            )

    def plot_walkers(self):
        """
        Walker subplots for each parameter (1 subplot per parameter, 1 line per walker).
        """
        if self.mcmc_chains_walkers is None:
            return

        chains = self.mcmc_chains_walkers  # shape: (n_steps, n_walkers, n_params)
        n_steps, n_walkers, n_params = chains.shape

        fig, axes = plt.subplots(n_params, 1, figsize=(8, 1.5 * n_params), sharex=True)
        if n_params == 1:
            axes = [axes]

        for i, ax in enumerate(axes):
            for walker in chains[:, :, i].T:  # loop over all walkers
                ax.plot(walker, alpha=0.2, color="black")
            ax.set_ylabel(self.mcmc_params[i])

        axes[-1].set_xlabel("Step")

        self.plot_widget.canvas_walkers.figure = fig
        self.plot_widget.canvas_walkers.draw()

        tab = self.plot_widget.tab_manager.get_tab("Walkers")
        if tab is not None:
            self.plot_widget.add_matplotlib_toolbar(
                self.plot_widget.canvas_walkers, tab.layout()
            )

    def show_mcmc_results(self, result, confidence_band):
        """
        Displays MCMC results for emcee fit, including plots of corner, walkers,
        autocorrelation, and the fit with confidence bands.
        """
        self.mcmc_chains = result["samples"]
        self.mcmc_chains_walkers = result["chain"]
        self.mcmc_params = list(result["params"].keys())

        self.plot_widget.tab_manager.ensure_tab_exists(
            "Corner Plot", "fig_corner", "ax_corner", "canvas_corner"
        )
        self.plot_widget.tab_manager.ensure_tab_exists(
            "Walkers", "fig_walkers", "ax_walkers", "canvas_walkers"
        )
        self.plot_widget.tab_manager.ensure_tab_exists(
            "Autocorrelation", "fig_auto", "ax_auto", "canvas_auto"
        )

        self.plot_corner_plot()
        self.plot_autocorrelation()
        self.plot_walkers()

        fit_tab = self.plot_widget.parent.get_current_fit_tab()
        mode = fit_tab.current_mode
        strategy = fit_tab.fit_control.get_current_strategy()

        formula = fit_tab.formula_text.toPlainText()
        fit_function = fit_tab.fit_control.fit_processor.generate_fit_function(formula)
        median_params = list(result["params"].values())

        if mode == "2D" and strategy == "Fit surface":
            df = fit_tab.df
            x = df["X"].values
            y = df["Y"].values
            z = df["Z"].values
            best_fit = fit_function(x, y, *median_params)

            self.plot_widget.tab_manager.ensure_tab_exists(
                "2D Surface", "fig_surface", "ax_surface", "canvas_surface"
            )
            from gcfpy.widgets.plot2d import plot_2d_surface_fit

            plot_2d_surface_fit(
                self.plot_widget.ax_surface,
                self.plot_widget.canvas_surface,
                x,
                y,
                z,
                best_fit,
                self.plot_widget,
            )

            self.plot_widget.tab_manager.switch_to_tab("2D Surface")
            tab = self.plot_widget.tab_manager.get_tab("2D Surface")
            if tab is not None:
                self.plot_widget.add_matplotlib_toolbar(
                    self.plot_widget.canvas_surface, tab.layout()
                )

        elif mode == "2D" and strategy == "Fit per Y":
            self.plot_widget.tab_manager.ensure_tab_exists(
                "MCMC Fit", "fig_mcmc_fit", "ax_mcmc_fit", "canvas_mcmc_fit"
            )
            df = fit_tab.df
            x = df["X"].values
            y = df["Y"].values
            z = df["Z"].values
            best_fit = fit_function(x, y, *median_params)
            lower, upper = confidence_band
            unique_y = np.unique(y)

            ax = self.plot_widget.ax_mcmc_fit
            ax.clear()

            for y_val in unique_y:
                mask = y == y_val
                x_ = x[mask]
                z_ = z[mask]
                fit_ = best_fit[mask]
                low_ = lower[mask]
                up_ = upper[mask]

                sort_idx = np.argsort(x_)
                x_sorted = x_[sort_idx]
                z_sorted = z_[sort_idx]
                fit_sorted = fit_[sort_idx]
                low_sorted = low_[sort_idx]
                up_sorted = up_[sort_idx]

                ax.plot(
                    x_sorted,
                    z_sorted,
                    "o",
                    color="blue",
                    label=f"Z @Y={y_val:.2f}",
                )
                ax.plot(
                    x_sorted,
                    fit_sorted,
                    color="red",
                    label=f"Fit @Y={y_val:.2f}",
                )
                ax.fill_between(
                    x_sorted, low_sorted, up_sorted, color="gray", alpha=0.3
                )

            self.plot_widget.canvas_mcmc_fit.draw()
            tab = self.plot_widget.tab_manager.get_tab("MCMC Fit")
            if tab is not None:
                self.plot_widget.add_matplotlib_toolbar(
                    self.plot_widget.canvas_mcmc_fit, tab.layout()
                )

        else:
            self.plot_widget.tab_manager.ensure_tab_exists(
                "MCMC Fit", "fig_mcmc_fit", "ax_mcmc_fit", "canvas_mcmc_fit"
            )
            x = self.plot_widget.data_x
            y = self.plot_widget.data_y
            best_fit = fit_function(x, *median_params)
            lower, upper = confidence_band if confidence_band else (best_fit, best_fit)

            if (
                hasattr(self.plot_widget, "selected_x")
                and self.plot_widget.selected_x is not None
            ):
                mask = np.isin(x, self.plot_widget.selected_x)
                x = x[mask]
                y = y[mask]
                best_fit = best_fit[mask]

            ax = self.plot_widget.ax_mcmc_fit
            ax.clear()
            ax.plot(x, y, "o", color="blue", label="Data")
            ax.plot(x, best_fit, color="red", linewidth=2, label="Best Fit")
            ax.fill_between(x, lower, upper, color="gray", alpha=0.4, label="99% CI")
            self.plot_widget.canvas_mcmc_fit.draw()

            tab = self.plot_widget.tab_manager.get_tab("MCMC Fit")
            if tab is not None:
                self.plot_widget.add_matplotlib_toolbar(
                    self.plot_widget.canvas_mcmc_fit, tab.layout()
                )
