import matplotlib.pyplot as plt
import nested_pandas as npd

plot_filter_colors_rainbow = {
    "u": "#0c71ff",  # Blue
    "g": "#49be61",  # Green
    "r": "#ff0000",  # Red
    "i": "#ffc200",  # Orange/Yellow
    "z": "#f341a2",  # Pink/Magenta
    "y": "#990099",  # Purple
}

## https://rtn-045.lsst.io/#colorblind-friendly-plots
plot_filter_colors_white_background = {
    "u": "#1600ea",
    "g": "#31de1f",
    "r": "#b52626",
    "i": "#370201",
    "z": "#ba52ff",
    "y": "#61a2b3",
}
plot_filter_colors_black_background = {
    "u": "#3eb7ff",
    "g": "#30c39f",
    "r": "#ff7e00",
    "i": "#2af5ff",
    "z": "#a7f9c1",
    "y": "#fdc900",
}

plot_filter_symbols = {
    "u": "o",  # Circle
    "g": "^",  # Triangle up
    "r": "s",  # Square
    "i": "D",  # Diamond
    "z": "v",  # Triangle down
    "y": "X",  # X
}

plot_symbols = {"u": "o", "g": "^", "r": "v", "i": "s", "z": "*", "y": "p"}
plot_linestyles_none = {
    "u": None,
    "g": None,
    "r": None,
    "i": None,
    "z": None,
    "y": None,
}

plot_linestyles = {
    "u": "--",
    "g": (0, (3, 1, 1, 1)),
    "r": "-.",
    "i": "-",
    "z": (0, (3, 1, 1, 1, 1, 1)),
    "y": ":",
}

band_names_ugrizy = ["u", "g", "r", "i", "z", "y"]
band_names_lsst_ugrizy = ["LSST_u", "LSST_g", "LSST_r", "LSST_i", "LSST_z", "LSST_y"]


def plot_light_curve(
    lc: npd.NestedFrame,
    title="LSST light curve",
    mag_field="psfMag",
    flux_field=None,
    legend_kwargs=None,
    band_names=None,
    plot_kwargs=None,
    filter_colors=None,
    filter_symbols=None,
    filter_linestyles=None,
    period=None,
    num_periods=1,
    period_mjd0=None,
):
    """Convenience method to plot a single light curve's magnitude. The y-axis is
    upside-down since magnitude is bananas.

    If you want additional configuration, you may be better served creating your own plotting
    function, as this is intended for quick inspection of individual lightcurves in HATS-formatted
    data products.

    Args:
        lc (npd.NestedFrame): Light curve data a single nested dataframe.
        title (str, optional): Title for the plot. Defaults to "LSST light curve".
        mag_field (str, optional): Field name for magnitude values. Defaults to "psfMag".
            If using magnitude, the y-axis will be inverted.
        flux_field (str, optional): Field name for flux values.
            If None, uses mag_field instead. Defaults to None.
        legend_kwargs (dict, optional): Keyword arguments for plt.legend(). Defaults to None.
        band_names (list, optional): List of band names to plot. Defaults to None (uses ugrizy).
        plot_kwargs (dict, optional): Additional keyword arguments for plt.errorbar(). Defaults to None.
        filter_colors (dict, optional): Mapping of band names to colors.
            Defaults to plot_filter_colors_white_background.
        filter_symbols (dict, optional): Mapping of band names to marker symbols.
            Defaults to plot_symbols.
        filter_linestyles (dict, optional): Mapping of band names to line styles.
            Defaults to plot_linestyles_none.
        period (float, optional): If provided, folds the time axis by this period (in days).
            Defaults to None.
        num_periods (int): Used to plot multiple full periods. Defaults to 1 (single period).
        period_mjd0 (float, optional): The time of the start of the phase-folded light curve.
            If not provided, we use the earliest ``midpointMjdTai`` value.

    Returns:
        None
    """
    # Let's first set values to defaults if they're not specified in kwargs.
    if plot_kwargs is None:
        plot_kwargs = {}
    if filter_colors is None:
        filter_colors = plot_filter_colors_white_background
    if filter_symbols is None:
        filter_symbols = plot_symbols
    if filter_linestyles is None:
        filter_linestyles = plot_linestyles_none

    if legend_kwargs is None:
        legend_kwargs = {}
    if band_names is None:
        band_names = band_names_ugrizy

    is_mag = flux_field is None
    brightness_field = flux_field or mag_field
    brightness_err_field = f"{brightness_field}Err"
    if period_mjd0 is None:
        period_mjd0 = lc["midpointMjdTai"].min()

    # Actually do the plot
    for band in band_names:
        data = lc.query(f"band == '{band}'")
        if len(data) == 0:
            continue
        x_axis = data["midpointMjdTai"]
        if period is not None:
            x_axis = (x_axis - period_mjd0) / period % num_periods
        plt.errorbar(
            x_axis,
            data[brightness_field],
            yerr=data[brightness_err_field],
            label=band,
            linestyle=filter_linestyles[band],
            fmt=filter_symbols[band],
            color=filter_colors[band],
            **plot_kwargs,
        )

    if is_mag:
        plt.gca().invert_yaxis()

    if period is None:
        plt.xlabel("MJD")
    else:
        plt.xlabel("phase")
        plt.xlim([0, num_periods])
        title = title + f" (period = {period} d)"

    plt.ylabel(brightness_field)
    plt.title(title)
    plt.legend(**legend_kwargs)
