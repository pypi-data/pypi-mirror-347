import emcee
import lmfit
import numpy as np
from PyQt5.QtWidgets import QMessageBox
from scipy.odr import ODR, Model, RealData
from scipy.optimize import approx_fprime

from .code_generator import generate_python_code
from .formula_tools import extract_parameters


class FitProcessor:
    """Handles the fit logic separately from the UI."""

    def __init__(self, fit_options_dialog):
        """
        Initializes the FitProcessor.

        Args:
            fit_options_dialog: Dialog containing fit options.

        """
        self.fit_options_dialog = fit_options_dialog

    def generate_fit_function(self, formula):
        """
        Generates and secures the fit function.

        Args:
            formula (str): The mathematical formula for fitting.

        Returns:
            function: The compiled fit function, or None if an error occurs.

        """
        function_code = generate_python_code(formula)
        if not function_code:
            print("Error: No function code generated.")
            return None

        local_scope = {}
        try:
            exec(function_code, {"lmfit": lmfit, "np": np}, local_scope)
            return local_scope.get("fit_function", None)
        except Exception as e:
            print(f"Error in function generation: {e}")
            return None

    def prepare_parameters(self, formula):
        """
        Prepares lmfit.Parameters based on the formula and user-defined options.

        Args:
            formula (str): The mathematical formula for fitting.

        Returns:
            lmfit.Parameters: Configured parameters for the fitting process.

        """
        param_options = self.fit_options_dialog.get_params_options()
        param_names = extract_parameters(formula)
        params = lmfit.Parameters()

        try:
            for param in param_names:
                p0 = param_options[param]["p0"]
                min_bound, max_bound = param_options[param]["bounds"]
                params.add(param, value=p0, min=min_bound, max=max_bound)
        except KeyError as e:
            print(f"Missing parameter setting: {e}")
            return None

        return params

    def process_fit(self, formula, x_data, y_data, weights=None, weighting_method=None):
        """
        Dispatches the 1D fit depending on the method (lmfit, odr, emcee).
        """
        fit_function = self.generate_fit_function(formula)
        if fit_function is None:
            raise ValueError("Invalid formula: cannot generate fit function.")

        fit_options = self.fit_options_dialog.get_options()
        method = fit_options.get("method", "leastsq")  # default is lmfit

        if method == "odr":
            return self._process_odr(
                formula,
                fit_function,
                ["x"],
                x_data,
                y_data,
                x_err=None,
                y_err=None,
            )
        elif method == "emcee":
            fit_options = self.fit_options_dialog.get_options()
            param_info = fit_options.get("params", {})
            return self._run_emcee(
                fit_function,
                param_info,
                x_data,
                y_data,
                weights if weights is not None else np.ones_like(y_data),
                fit_options,
                mode="1d",
            )
        else:
            return self._process_lmfit(
                formula,
                fit_function,
                ["x"],
                x_data,
                y_data,
                weights,
                weighting_method,
            )

    def process_fit_per_y(
        self,
        formula,
        x_data,
        y_data,
        z_data,
        weights=None,
        weighting_method=None,
    ):
        """
        Fit 2D model Z = f(X, Y_fixed).
        """
        fit_function = self.generate_fit_function(formula)
        if fit_function is None:
            raise ValueError("Invalid formula: cannot generate fit function.")
        return self._process_lmfit(
            formula,
            fit_function,
            ["x", "y"],
            (x_data, y_data),
            z_data,
            weights,
            weighting_method,
        )

    def process_fit_surface(
        self,
        formula,
        fit_function,
        x_data,
        y_data,
        z_data,
        weights=None,
        weighting_method=None,
    ):
        """
        Fit 2D surface model Z = f(X, Y) using pre-generated fit_function.
        """
        return self._process_lmfit(
            formula,
            fit_function,
            ["x", "y"],
            (x_data, y_data),
            z_data,
            weights,
            weighting_method,
        )

    def _process_lmfit(
        self,
        formula,
        fit_function,
        independent_vars,
        x_data,
        y_data,
        weights,
        weighting_method,
    ):
        """
        Internal method to perform lmfit fit.
        """
        if weighting_method in ("x_err", "xy_err"):
            QMessageBox.warning(
                None,
                "Weighting Warning",
                "'x_err' weighting is not supported by lmfit and will be ignored.\n"
                "Only 'y_err' is used.",
            )
            weights = None

        fit_options = self.fit_options_dialog.get_options()
        params = self.prepare_parameters(formula)
        if params is None:
            raise ValueError("Error preparing lmfit parameters.")

        model = lmfit.Model(
            fit_function,
            independent_vars=independent_vars,
            nan_policy="omit",
            missing="raise",
            eval_env={"np": np},
        )

        fit_kwargs = {
            "method": fit_options.get("method", "leastsq"),
            "calc_covar": fit_options.get("calc_covar", True),
            "scale_covar": fit_options.get("scale_covar", True),
        }

        # Adapt x_data to the fit argument format
        if isinstance(x_data, tuple):
            fit_args = dict(zip(independent_vars, x_data))
        else:
            fit_args = {independent_vars[0]: x_data}

        result = model.fit(y_data, params, weights=weights, **fit_args, **fit_kwargs)
        best_fit = result.best_fit
        minimizer = result

        try:
            confidence_band = result.eval_uncertainty(sigma=3)
        except Exception:
            confidence_band = None

        return result, minimizer, best_fit, confidence_band

    def _run_emcee(
        self,
        fit_function,
        param_info,
        inputs,
        targets,
        sigma,
        fit_options,
        mode="1d",
    ):
        """
        Internal method to perform MCMC fitting using emcee.

        Args:
            fit_function (callable): Function to fit.
            param_info (dict): Parameters info (p0, bounds).
            inputs (tuple or np.ndarray): Input data (x,) or (x, y).
            targets (np.ndarray): Target data (y or z).
            sigma (np.ndarray): Errors.
            fit_options (dict): MCMC fit options.
            mode (str): '1d', 'per_y', or 'surface'.

        Returns:
            result (dict), sampler (emcee.EnsembleSampler), best_fit (np.ndarray),
             confidence_band (tuple)

        """

        param_names = list(param_info.keys())
        p0_values = [param_info[k]["p0"] for k in param_names]
        param_bounds = [param_info[k]["bounds"] for k in param_names]

        ndim = len(p0_values)
        nwalkers = fit_options.get("nwalkers", 50)
        nsteps = fit_options.get("steps", 1000)
        burn = fit_options.get("burn", 200)
        thin = fit_options.get("thin", 10)

        def log_prior(theta):
            for val, (low, high) in zip(theta, param_bounds):
                if not (low < val < high):
                    return -np.inf
            return 0.0

        def log_likelihood(theta, *args):
            try:
                if mode == "1d":
                    x, y, yerr = args
                    model = fit_function(x, *theta)
                    return -0.5 * np.sum(((y - model) / yerr) ** 2)
                else:
                    x, y, z, sigma = args
                    model = fit_function(x, y, *theta)
                    return -0.5 * np.sum(((z - model) / sigma) ** 2)
            except Exception:
                return -np.inf

        def log_prob(theta, *args):
            lp = log_prior(theta)
            if not np.isfinite(lp):
                return -np.inf
            return lp + log_likelihood(theta, *args)

        # Prepare inputs for log_prob
        if mode == "1d":
            args = (inputs, targets, sigma)
        else:
            args = (*inputs, targets, sigma)

        p0 = np.array(p0_values) + 1e-4 * np.random.randn(nwalkers, ndim)
        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob, args=args)
        sampler.run_mcmc(p0, nsteps, progress=True)

        flat_samples = sampler.get_chain(discard=burn, thin=thin, flat=True)
        med_params = np.median(flat_samples, axis=0)
        std_params = np.std(flat_samples, axis=0)

        if mode == "1d":
            inputs_plot = (inputs,)
            best_fit = fit_function(inputs, *med_params)

        elif mode == "per_y":
            inputs_plot = inputs
            best_fit = fit_function(*inputs, *med_params)

        elif mode == "surface":
            inputs_plot = inputs
            best_fit = fit_function(inputs[0], inputs[1], *med_params)

        else:
            raise ValueError(f"Unsupported mode: {mode}")

        n_draws = min(500, len(flat_samples))
        draw_indices = np.random.choice(len(flat_samples), size=n_draws, replace=False)

        preds = np.array(
            [fit_function(*inputs_plot, *theta) for theta in flat_samples[draw_indices]]
        )
        lower = np.percentile(preds, 0.15, axis=0)
        upper = np.percentile(preds, 99.85, axis=0)
        confidence_band = (lower, upper)

        if mode == "1d":
            best_fit = fit_function(inputs, *med_params)
        elif mode in ("per_y", "surface"):
            best_fit = fit_function(*inputs, *med_params)
        residuals = targets - best_fit
        ss_res = np.sum(residuals**2)
        n = len(targets)
        k = ndim
        reduced_chi2 = ss_res / (n - k) if n > k else np.nan
        aic = n * np.log(ss_res / n) + 2 * k
        bic = n * np.log(ss_res / n) + k * np.log(n)

        result = {
            "method": "emcee",
            "params": dict(zip(param_names, med_params)),
            "stderr": dict(zip(param_names, std_params)),
            "samples": flat_samples,
            "chain": sampler.get_chain(),
            "residuals": residuals,
            "nfev": nsteps * nwalkers,
            "sum_square": ss_res,
            "aic": aic,
            "bic": bic,
            "reduced_chi2": reduced_chi2,
            "fit_stats": {
                "n_points": n,
                "n_params": k,
                "nfev": nsteps * nwalkers,
                "sum_sq": ss_res,
                "reduced_chi2": reduced_chi2,
                "aic": aic,
                "bic": bic,
            },
        }

        return result, sampler, best_fit, confidence_band

    def process_emcee(
        self,
        formula,
        fit_function,
        x_data,
        y_data,
        y_err=None,
        fit_options=None,
        weighting_method=None,
    ):
        if y_err is None:
            y_err = np.ones_like(y_data)

        if fit_options is None:
            fit_options = self.fit_options_dialog.get_options()

        param_info = fit_options.get("params", {})

        return self._run_emcee(
            fit_function,
            param_info,
            x_data,
            y_data,
            y_err,
            fit_options,
            mode="1d",
        )

    def process_fit_per_y_emcee(
        self,
        formula,
        x_data,
        y_data,
        z_data,
        weights=None,
        weighting_method=None,
    ):
        if weights is None:
            weights = np.ones_like(z_data)

        fit_function = self.generate_fit_function(formula)
        if fit_function is None:
            raise ValueError("Invalid formula: cannot generate fit function.")

        fit_options = self.fit_options_dialog.get_options()
        param_info = fit_options.get("params", {})

        return self._run_emcee(
            fit_function,
            param_info,
            (x_data, y_data),
            z_data,
            weights,
            fit_options,
            mode="per_y",
        )

    def process_fit_surface_emcee(
        self,
        formula,
        fit_function,
        x_data,
        y_data,
        z_data,
        weights=None,
        weighting_method=None,
    ):
        if weights is None:
            weights = np.ones_like(z_data)

        fit_options = self.fit_options_dialog.get_options()
        param_info = fit_options.get("params", {})

        return self._run_emcee(
            fit_function,
            param_info,
            (x_data, y_data),
            z_data,
            weights,
            fit_options,
            mode="surface",
        )

    def process_fit_odr(self, formula, x_data, y_data, x_err=None, y_err=None):
        """
        Fit 1D model Y = f(X) using ODR.
        """
        fit_function = self.generate_fit_function(formula)
        if fit_function is None:
            raise ValueError("Invalid formula: cannot generate fit function.")
        return self._process_odr(
            formula,
            fit_function,
            ["x"],
            x_data,
            y_data,
            x_err,
            y_err,
        )

    def process_fit_per_y_odr(
        self, formula, x_data, y_data, z_data, x_err=None, y_err=None
    ):
        """
        Fit 2D model Z = f(X, Y_fixed) using ODR.
        """
        fit_function = self.generate_fit_function(formula)
        if fit_function is None:
            raise ValueError("Invalid formula: cannot generate fit function.")
        return self._process_odr(
            formula,
            fit_function,
            ["x", "y"],
            (x_data, y_data),
            z_data,
            x_err,
            y_err,
        )

    def process_fit_surface_odr(
        self,
        formula,
        fit_function,
        x_data,
        y_data,
        z_data,
        x_err=None,
        y_err=None,
    ):
        """
        Fit 2D surface model Z = f(X, Y) using ODR (with provided fit_function).
        """
        return self._process_odr(
            formula,
            fit_function,
            ["x", "y"],
            (x_data, y_data),
            z_data,
            x_err,
            y_err,
        )

    def _process_odr(
        self,
        formula,
        fit_function,
        independent_vars,
        x_data,
        y_data,
        x_err=None,
        y_err=None,
    ):
        """
        Internal method to perform ODR fit.
        """
        fit_options = self.fit_options_dialog.get_options()
        param_info = fit_options.get("params", {})
        param_names = list(param_info.keys())
        p0_values = [param_info[k]["p0"] for k in param_names]

        # Prepare the function for ODR
        def odr_func(beta, inputs):
            if isinstance(inputs, np.ndarray):
                if inputs.ndim == 2:
                    return fit_function(inputs[0], inputs[1], *beta)
                else:
                    return fit_function(inputs, *beta)
            elif isinstance(inputs, (list, tuple)):
                if len(inputs) == 2:
                    return fit_function(inputs[0], inputs[1], *beta)
                else:
                    return fit_function(inputs[0], *beta)
            else:
                return fit_function(inputs, *beta)

        model = Model(odr_func)

        # Prepare RealData
        if isinstance(x_data, tuple):
            x_input = np.vstack(x_data)
        else:
            x_input = x_data

        realdata = RealData(x_input, y_data, sx=x_err, sy=y_err)
        odr = ODR(realdata, model, beta0=p0_values)
        output = odr.run()

        beta = output.beta
        cov_beta = output.cov_beta

        if isinstance(x_data, tuple):
            best_fit = fit_function(x_data[0], x_data[1], *beta)
        else:
            best_fit = fit_function(x_data, *beta)

        def compute_jacobian(x0, beta_vals, epsilon=1e-8):
            def wrapped(p):
                if isinstance(x0, tuple):
                    return fit_function(x0[0], x0[1], *p)
                else:
                    return fit_function(x0, *p)

            return approx_fprime(beta_vals, wrapped, epsilon)

        std_devs = []
        if isinstance(x_data, tuple):
            for xi, yi in zip(x_data[0], x_data[1]):
                J = compute_jacobian((xi, yi), beta)
                var = np.dot(J, np.dot(cov_beta, J.T))
                std_devs.append(np.sqrt(var))
        else:
            for xi in x_data:
                J = compute_jacobian(xi, beta)
                var = np.dot(J, np.dot(cov_beta, J.T))
                std_devs.append(np.sqrt(var))
        confidence_band = np.array(std_devs)

        residuals = y_data - best_fit
        ss_res = np.sum(residuals**2)
        n = len(y_data)
        k = len(beta)
        reduced_chi2 = ss_res / (n - k) if n > k else np.nan
        aic = n * np.log(ss_res / n) + 2 * k
        bic = n * np.log(ss_res / n) + k * np.log(n)

        result = {
            "method": "odr",
            "params": dict(zip(param_names, beta)),
            "stderr": dict(zip(param_names, output.sd_beta)),
            "covariance": cov_beta,
            "residuals": residuals,
            "nfev": output.info,
            "sum_square": ss_res,
            "aic": aic,
            "bic": bic,
            "reduced_chi2": reduced_chi2,
            "fit_stats": {
                "n_points": n,
                "n_params": k,
                "nfev": output.info,
                "sum_sq": ss_res,
                "reduced_chi2": reduced_chi2,
                "aic": aic,
                "bic": bic,
            },
        }
        return result, output, best_fit, confidence_band

    def extract_param_names(self, formula):
        """
        Extract parameter names from a formula string.

        Args:
            formula (str): Mathematical formula as string.

        Returns:
            list[str]: List of parameter names.

        """
        return extract_parameters(formula)

    def get_fit_report(self, result):
        """
        Returns a formatted fit report.

        Args:
            result: lmfit result object.

        Returns:
            str: Fit report.

        """
        return lmfit.fit_report(result, show_correl=True)

    def reset_fit(self, plot_widget, main_window):
        """
        Resets all fit results and plots depending on the current mode.

        Args:
            plot_widget: Main plot widget containing axes and results.
            main_window: Reference to the main application window.

        """
        # Clear stored results
        plot_widget.result = None
        plot_widget.minimizer = None
        plot_widget.fit_y = None
        plot_widget.confidence_band = None
        plot_widget.weights = None
        plot_widget.components = {}

        # Restore original plots if needed
        tab = plot_widget.parent.get_current_fit_tab()
        mode = getattr(tab, "current_mode", None)
        strategy = (
            tab.fit_control.get_current_strategy()
            if hasattr(tab, "fit_control")
            else None
        )

        if mode == "2D" and strategy == "Fit per Y":
            if hasattr(plot_widget.parent, "stored_fits_per_y"):
                plot_widget.parent.stored_fits_per_y.clear()
            if hasattr(tab, "df"):
                df = tab.df
                from gcfpy.widgets.plot2d import plot_multi1d_data

                plot_widget.tab_manager.ensure_tab_exists(
                    "Multi 1D", "fig_multi1d", "ax_multi1d", "canvas_multi1d"
                )
                plot_multi1d_data(
                    plot_widget.ax_multi1d,
                    plot_widget.canvas_multi1d,
                    df["X"].values,
                    df["Y"].values,
                    df["Z"].values,
                    plot_widget,
                )

        elif mode == "2D" and strategy == "Fit surface":
            if hasattr(plot_widget, "ax_surface"):
                plot_widget.ax_surface.clear()
                plot_widget.canvas_surface.draw()

        elif mode == "1D":
            if hasattr(plot_widget, "ax"):
                plot_widget.ax.clear()
                plot_widget.canvas.draw()

        if hasattr(tab, "results_text"):
            tab.results_text.clear()
        # Reset selection and UI
        if hasattr(plot_widget.xmin_xmax_tool, "disable_xmin_xmax_selection"):
            plot_widget.xmin_xmax_tool.disable_xmin_xmax_selection()
            main_window.toolbar.reset_xmin_xmax_button_style()

        main_window.toolbar.enable_toolbar_options(True)
        main_window.enable_toolbar_buttons(False)
        main_window.toolbar.enable_comparison(False)
