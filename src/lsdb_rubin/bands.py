"""Names, effective wavelengths, and display defaults for the LSST passbands.

These are shared by every plotting method in this package - see :doc:`/reference/bands`.
"""

plot_filter_colors_rainbow = {
    "u": "#0c71ff",  # Blue
    "g": "#49be61",  # Green
    "r": "#ff0000",  # Red
    "i": "#ffc200",  # Orange/Yellow
    "z": "#f341a2",  # Pink/Magenta
    "y": "#990099",  # Purple
}
"""Bright color palette."""

## https://rtn-045.lsst.io/#colorblind-friendly-plots
plot_filter_colors_white_background = {
    "u": "#1600ea",
    "g": "#31de1f",
    "r": "#b52626",
    "i": "#370201",
    "z": "#ba52ff",
    "y": "#61a2b3",
}
"""Rubin color palette for use on a white background.

This is the default, when you have no specified a per-band color palette
via the ``filter_colors`` argument.

See https://rtn-045.lsst.io/#colorblind-friendly-plots"""

plot_filter_colors_black_background = {
    "u": "#3eb7ff",
    "g": "#30c39f",
    "r": "#ff7e00",
    "i": "#2af5ff",
    "z": "#a7f9c1",
    "y": "#fdc900",
}
"""Rubin color palette for use on a black background.

See https://rtn-045.lsst.io/#colorblind-friendly-plots"""

plot_filter_symbols = {
    "u": "o",  # Circle
    "g": "^",  # Triangle up
    "r": "s",  # Square
    "i": "D",  # Diamond
    "z": "v",  # Triangle down
    "y": "X",  # X
}
"""Alternative symbols to use for individual data points, varying by filter.
See https://rtn-045.lsst.io/#colorblind-friendly-plots"""

plot_symbols = {"u": "o", "g": "^", "r": "v", "i": "s", "z": "*", "y": "p"}
"""Symbols to use for individual data points, varying by filter.

See https://rtn-045.lsst.io/#colorblind-friendly-plots

This is the default, when you have not specified a per-band color palette
via the ``filter_symbols`` argument."""

plot_linestyles_none = {
    "u": None,
    "g": None,
    "r": None,
    "i": None,
    "z": None,
    "y": None,
}
"""Do not use filter-varying line styles. All lines are solid.

This is the default, when you have no specified a per-band color palette
via the ``filter_linestyles`` argument."""

plot_linestyles = {
    "u": "--",
    "g": (0, (3, 1, 1, 1)),
    "r": "-.",
    "i": "-",
    "z": (0, (3, 1, 1, 1, 1, 1)),
    "y": ":",
}
"""Alternative filter-varying line styles.

These can be useful to show different line styles for each filter in a plot."""

band_names_ugrizy = ["u", "g", "r", "i", "z", "y"]
"""Names of passbands that will appear in the ``band`` nested column.

This is the default, when you have no specified a per-band color palette
via the ``band_names`` argument.
"""

band_names_lsst_ugrizy = ["LSST_u", "LSST_g", "LSST_r", "LSST_i", "LSST_z", "LSST_y"]
"""Alternative names of passbands that could appear in the ``band`` nested column."""

band_wavelengths_ugrizy = {
    "u": 372.4,
    "g": 480.7,
    "r": 622.1,
    "i": 755.9,
    "z": 868.0,
    "y": 975.3,
}
"""Effective wavelength (in nanometers) of each LSST passband (throughputs v1.9).

This is the default, when you have not specified a per-band mapping via the
``band_wavelengths`` argument.

See https://lsstcam.lsst.io"""

band_widths_ugrizy = {
    "u": 46.4,
    "g": 148.6,
    "r": 140.0,
    "i": 128.7,
    "z": 104.1,
    "y": 86.4,
}
"""Full width at half maximum (in nanometers) of each LSST passband (throughputs v1.9).

Drawn by :doc:`/reference/plot_sed` as a horizontal bar through each point, spanning
half a width either side of the effective wavelength. Note that the passbands are not
quite symmetric about their effective wavelength - most visibly in ``y``, whose bar
runs about 7nm redder than its true half-power points - so read the bar as the rough
extent of the band, not as its exact edges.

This is the default, when you have not specified a per-band mapping via the
``band_widths`` argument. Pass ``band_widths={}`` to draw bare points instead.

See https://lsstcam.lsst.io"""
