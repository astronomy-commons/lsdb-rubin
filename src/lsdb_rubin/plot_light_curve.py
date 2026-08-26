import matplotlib.pyplot as plt
import nested_pandas as npd

from lsdb_rubin.bands import (
    band_names_ugrizy,
    plot_filter_colors_white_background,
    plot_linestyles_none,
    plot_symbols,
)


def plot_light_curve(
    lc: npd.NestedFrame,
    *,
    title="LSST light curve",
    mag_field="psfMag",
    flux_field=None,
    corrected_err=False,
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
    """Convenience method to plot a single light curve's magnitude.

    Note: The y-axis is upside-down since magnitude is bananas.

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
        corrected_err (bool, optional): Whether to use the corrected error field,
            ``f"{brightness_field}Err_corrected"``, instead of the original
            ``f"{brightness_field}Err"``. Corrected errors are added to the nested
            forced-source columns of the Rubin EDP2 HATS catalogs (``psfFluxErr_corrected``,
            ``psfDiffFluxErr_corrected`` and ``psfMagErr_corrected``) by a model that
            rescales the errors of non-variable objects to a reduced chi-squared close to
            unity.
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

    Raises:
        ValueError: If ``corrected_err`` is True but ``lc`` has no corrected error column
            for the requested brightness field.
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
    if corrected_err:
        corrected_err_field = f"{brightness_err_field}_corrected"
        if corrected_err_field not in lc.columns:
            raise ValueError(
                f"Light curve has no {corrected_err_field!r} column. Corrected errors are only "
                f"available for some of the nested forced-source columns of the Rubin EDP2 catalogs. "
                f"Pass corrected_err=False to plot {brightness_err_field!r} instead."
            )
        brightness_err_field = corrected_err_field

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
