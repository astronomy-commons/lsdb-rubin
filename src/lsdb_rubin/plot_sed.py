import astropy.units as u
import matplotlib.pyplot as plt
import pandas as pd

from lsdb_rubin.bands import (
    band_names_ugrizy,
    band_wavelengths_ugrizy,
    band_widths_ugrizy,
    plot_filter_colors_white_background,
    plot_symbols,
)


def plot_sed(
    obj: pd.Series,
    title="LSST broadband SED",
    mag_field="psfMag",
    flux_field=None,
    band_names=None,
    band_wavelengths=None,
    band_widths=None,
    x_units="nm",
    filter_colors=None,
    filter_symbols=None,
    plot_kwargs=None,
    legend_kwargs=None,
    ax=None,
):
    """Convenience method to plot a single object's broadband SED.

    Each band is read straight off the object's own per-band columns - the ones named
    ``f"{band}_{brightness_field}"``, such as ``u_psfMag`` or ``g_psfFlux`` - and plotted
    against that band's wavelength, with a horizontal bar spanning the band's throughput
    FWHM. The matching uncertainty is read from ``f"{band}_{brightness_field}Err"``,
    when the object has such a column.

    Bands the object has no column for, or whose value is null, are left out - so an
    object measured only in ``griz`` is plotted as four points.

    Note: The y-axis is upside-down when plotting magnitudes, since magnitude is bananas.

    If you want additional configuration, you may be better served creating your own
    plotting function, as this is intended for quick inspection of individual objects in
    HATS-formatted data products.

    Args:
        obj (pd.Series): A single row of an object catalog, e.g. ``catalog.compute().iloc[0]``.
        title (str, optional): Title for the plot. Defaults to "LSST broadband SED".
        mag_field (str, optional): Name of the per-band magnitude, without its band prefix.
            Defaults to "psfMag". If using magnitude, the y-axis will be inverted.
        flux_field (str, optional): Name of the per-band flux, without its band prefix.
            If None, uses mag_field instead. Defaults to None.
        band_names (list, optional): List of band names to plot, in plotting order. These
            are the column prefixes, not the values of any ``band`` column.
            Defaults to None (uses ugrizy).
        band_wavelengths (dict, optional): Mapping of band name to wavelength,
            in nanometers. Defaults to band_wavelengths_ugrizy.
        band_widths (dict, optional): Mapping of band name to throughput FWHM, in
            nanometers, drawn as a horizontal bar through each point spanning half a
            width either side of the band's wavelength. Bands missing from the
            mapping are drawn without a bar. Defaults to band_widths_ugrizy; pass an
            empty dict for bare points.
        x_units (str or astropy.units.UnitBase, optional): Units for the x-axis. Anything
            astropy reads as a wavelength ("nm", "angstrom", "micron"), a frequency
            ("THz", "GHz"), an energy ("eV", "keV"), or a wavenumber ("1/cm"). Defaults
            to "nm".
        filter_colors (dict, optional): Mapping of band names to colors.
            Defaults to plot_filter_colors_white_background.
        filter_symbols (dict, optional): Mapping of band names to marker symbols.
            Defaults to plot_filter_symbols.
        plot_kwargs (dict, optional): Additional keyword arguments for Axes.errorbar(). Defaults to None.
        legend_kwargs (dict, optional): Keyword arguments for Axes.legend(). Defaults to None.
        ax (matplotlib.axes.Axes, optional): Axes to draw on. Defaults to the current axes,
            creating a figure to hold them when no figure is open yet.

    Returns:
        matplotlib.axes.Axes: The axes the SED was drawn on.
    """
    if band_names is None:
        band_names = band_names_ugrizy
    if band_wavelengths is None:
        band_wavelengths = band_wavelengths_ugrizy
    if band_widths is None:
        band_widths = band_widths_ugrizy
    if filter_colors is None:
        filter_colors = plot_filter_colors_white_background
    if filter_symbols is None:
        filter_symbols = plot_symbols
    if plot_kwargs is None:
        plot_kwargs = {}
    if legend_kwargs is None:
        legend_kwargs = {}
    if ax is None:
        ax = plt.gca()

    x_unit, x_label = _x_axis(x_units)

    is_mag = flux_field is None
    brightness_field = flux_field or mag_field

    for band in band_names:
        brightness, uncertainty = _band_measurement(obj, band, brightness_field)
        if brightness is None:
            continue
        x_position, x_error = _band_x_extent(band, band_wavelengths, band_widths, x_unit)

        ax.errorbar(
            x_position,
            brightness,
            yerr=uncertainty,
            xerr=x_error,
            label=band,
            fmt=filter_symbols[band],
            color=filter_colors[band],
            **plot_kwargs,
        )

    if is_mag:
        ax.invert_yaxis()

    ax.set_xlabel(x_label)
    ax.set_ylabel(brightness_field)
    ax.set_title(title)
    ax.legend(**legend_kwargs)

    return ax


x_axis_quantities = {
    "length": "wavelength",
    "frequency": "frequency",
    "energy": "energy",
    "wavenumber": "wavenumber",
}
"""The physical quantities :func:`plot_sed` will plot a band against, mapped to the axis
label each one draws. Any astropy unit of one of these is a usable ``x_units``, since
they are the quantities ``astropy.units.spectral()`` converts a wavelength into."""


def _x_axis(x_units):
    """Resolve the requested x-axis units into an astropy unit and its axis label."""
    unit = u.Unit(x_units)
    for physical_type, quantity in x_axis_quantities.items():
        if unit.physical_type == physical_type:
            return unit, f"{quantity} ({unit.to_string('unicode')})"
    raise ValueError(
        f"Cannot plot an SED against {unit}, which measures {unit.physical_type}; "
        f"x_units must be a unit of {' or '.join(sorted(x_axis_quantities))}"
    )


def _to_x_units(wavelength, unit):
    """Convert a wavelength in nanometers - or a list of them - into the x-axis units."""
    return (wavelength * u.nm).to_value(unit, equivalencies=u.spectral())


def _band_measurement(obj, band, brightness_field):
    """One band's measurement and its uncertainty, as ``(brightness, uncertainty)``.

    The brightness is None when the object has no column for this band, or a null one -
    those bands are left out of the plot entirely. The uncertainty is None when the
    catalog carries no matching ``Err`` column, and that band is drawn as a bare point.
    """
    column = f"{band}_{brightness_field}"
    if column not in obj or pd.isna(obj[column]):
        return None, None
    uncertainty = obj.get(f"{column}Err")
    if uncertainty is None or pd.isna(uncertainty):
        return float(obj[column]), None
    return float(obj[column]), float(uncertainty)


def _band_x_extent(band, band_wavelengths, band_widths, unit):
    """Where a band sits on the x-axis, as ``(position, half-bars to either side)``.

    A band with no width in ``band_widths`` gets no bar. The bar is converted from the
    band's edges rather than scaled from its width, because frequency and energy are
    reciprocals of wavelength - a band symmetric in wavelength is lopsided in those.
    """
    if band not in band_wavelengths:
        raise KeyError(f"No wavelength for band {band!r}; check `band_wavelengths`")
    wavelength = band_wavelengths[band]
    position = _to_x_units(wavelength, unit)
    width = band_widths.get(band)
    if width is None:
        return position, None
    half_width = float(width) / 2
    lower, upper = sorted(_to_x_units([wavelength - half_width, wavelength + half_width], unit))
    return position, [[position - lower], [upper - position]]
