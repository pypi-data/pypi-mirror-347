import numpy as np
from scipy.interpolate import griddata


def add_toolbar(name, canvas, plot_widget):
    """
    Add matplotlib toolbar
    """
    tab = plot_widget.tab_manager.get_tab(name)
    if tab is not None:
        plot_widget.add_matplotlib_toolbar(canvas, tab.layout())


def plot_2d_series(ax, canvas, x, y, z, plot_widget):
    """
    Plot Z = f(X) for each unique value of Y on the given Matplotlib axis.
    """
    ax.clear()
    unique_y = np.unique(y)
    for y_val in unique_y:
        mask = y == y_val
        x_subset = x[mask]
        z_subset = z[mask]
        label = f"Y = {y_val:.3g}" if len(unique_y) > 1 else "Z vs X"
        ax.plot(
            x_subset,
            z_subset,
            linestyle="",
            marker="+",
            label=label,
            color="k",
        )

    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    ax.legend()
    canvas.draw()
    if plot_widget:
        add_toolbar("Multi 1D", canvas, plot_widget)


def plot_2d_surface(ax, canvas, x, y, z, plot_widget):
    """
    Plot Z = f(X, Y) as black cross markers instead of a surface.

    Args:
        ax (Axes): A 3D axis (from add_subplot(projection='3d')).
        canvas (FigureCanvas): The canvas to update.

    """
    ax.clear()

    if x.ndim == 2:
        x = x.ravel()
    if y.ndim == 2:
        y = y.ravel()
    if z.ndim == 2:
        z = z.ravel()

    if not (len(x) == len(y) == len(z)):
        raise ValueError("Input arrays must have the same length.")

    ax.scatter(x, y, z, marker="x", color="black")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Z = f(X, Y)")

    canvas.draw()
    if plot_widget:
        add_toolbar("2D Surface", canvas, plot_widget)


def plot_multi1d_data(ax, canvas, x, y, z, plot_widget):
    """
    Plots raw Z = f(X) curves for each fixed Y value.
    """
    ax.clear()
    unique_y = np.unique(y)
    for y_val in unique_y:
        mask = y == y_val
        x_subset = x[mask]
        z_subset = z[mask]
        ax.plot(
            x_subset,
            z_subset,
            marker="+",
            linestyle="",
            color="black",
            markersize=2,
        )
    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    canvas.draw()

    if plot_widget:
        add_toolbar("Multi 1D", canvas, plot_widget)


def plot_multi1d_fit(ax, canvas, fits, plot_widget):
    """
    Plot fitted Z = f(X) curves, one per fixed Y.
    """
    for x, fit_z, y_val in fits:
        ax.plot(x, fit_z, "--", color="red", zorder=5, lw=2)
    canvas.draw()

    if plot_widget:
        add_toolbar("Multi 1D", canvas, plot_widget)


def plot_2d_surface_fit(ax, canvas, x, y, z_data, z_fit, plot_widget=None):
    """
    Plots 3D black cross data and a smooth surface from z_fit on a 3D axis.

    Args:
        ax (Axes3D): A 3D matplotlib axis.
        canvas (FigureCanvas): Matplotlib canvas.
        x (np.ndarray): X data (1D).
        y (np.ndarray): Y data (1D).
        z_data (np.ndarray): Raw Z values (1D).
        z_fit (np.ndarray): Fit Z values (1D, same shape as x, y).
        plot_widget (optional): PlotWidget to add toolbar.

    """
    ax.clear()

    ax.scatter(x, y, z_data, color="black", marker="x", label="Data", zorder=5)

    xi = np.linspace(np.min(x), np.max(x), 100)
    yi = np.linspace(np.min(y), np.max(y), 100)
    X, Y = np.meshgrid(xi, yi)
    Z = griddata((x, y), z_fit, (X, Y), method="cubic")

    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.7, edgecolor="none")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Z = f(X, Y) with Fit")
    canvas.draw()
