# Curve Graphical Curve Fitting

A Python-based graphical interface for fitting experimental data, built on top of `lmfit`, `emcee`, `scipy` and `PyQt5`. It allows interactive visualization, model customization, and multi-method fit analysis (1D and 2D).

---

## Features

* **Multi-tab GUI**: manage several fit sessions in parallel
* **Custom model editor**: write formulas directly, with auto-detected parameters
* **Fitting methods**:

  * Least-squares (`lmfit`)
  * MCMC sampling (`emcee`)
  * Orthogonal Distance Regression (`scipy.odr`)
* **Data types supported**:

  * 1D fit (`y = f(x)`) with optional error bars
  * 2D fit (`z = f(x, y)`) with surface visualization
* **Advanced visualization tools**:

  * Residual plots and confidence intervals
  * 2D surface fit & scatter overlays
  * Component breakdown (for additive models)
  * MCMC diagnostics: chains, corner plots, autocorrelation
* **Fit comparison manager**: store, label and compare multiple models per dataset
* **Data & results export/import** (CSV)

Other tools such as [PyModelFit](https://pythonhosted.org/PyModelFit/gui.html), [curvefitgui](https://pypi.org/project/curvefitgui/), or more general platforms like [Veusz](https://veusz.github.io/) also provide GUI-based fitting capabilities.

---

## Installing

```bash
git clone https://github.com/gcfpy/gcfpy
cd gcfpy
pip install -e .
```

---

## Launch the Application

```bash
gcfpy
```
or
```bash
python -m gcfpy.app.main_window
```
---

## Documentation

Read the [docs](https://gcfpy.github.io/gcfpy/).

It is possible to build the doc locally :
```bash
mkdocs serve
```
The full documentation is written in Markdown using **MkDocs** with the Material theme.

---
## Contributions

We appreciate and welcome contributions. Small improvements or fixes are always appreciated.