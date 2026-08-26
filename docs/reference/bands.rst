LSST Bands
=============================

Names, effective wavelengths, and display defaults for the LSST passbands. These are
shared by every plotting method in this package - pass them via the ``filter_colors``,
``filter_symbols``, ``filter_linestyles``, ``band_names``, and ``band_wavelengths``
arguments.

Color palettes (``filter_colors``)
-----------------------------------------

A color palette will be used to distinguish multi-band data, and is expected
to be a dictionary, where keys are band names, and values are the color, as
accepted by matplotlib.

.. autodata:: lsdb_rubin.bands.plot_filter_colors_white_background
.. autodata:: lsdb_rubin.bands.plot_filter_colors_black_background
.. autodata:: lsdb_rubin.bands.plot_filter_colors_rainbow

Symbols (``filter_symbols``)
-----------------------------------------

Symbols will be used to distinguish multi-band data, and is expected
to be a dictionary, where keys are band names, and values are the symbol
marker, as accepted by matplotlib.

.. autodata:: lsdb_rubin.plot_light_curve.plot_symbols
.. autodata:: lsdb_rubin.plot_light_curve.plot_filter_symbols

Line Styles (``filter_linestyles``)
-----------------------------------------

Used by :doc:`/reference/plot_light_curve`. Note that an SED plots a single point per
band, with no segment between points, so it takes no line styles.

.. autodata:: lsdb_rubin.bands.plot_linestyles_none
.. autodata:: lsdb_rubin.bands.plot_linestyles

Band Names (``band_names``)
-----------------------------------------

.. autodata:: lsdb_rubin.bands.band_names_ugrizy
.. autodata:: lsdb_rubin.plot_light_curve.band_names_lsst_ugrizy

Effective wavelengths (``band_wavelengths``)
---------------------------------------------

The x-axis position of each band in :doc:`/reference/plot_sed`, expected to be a
dictionary where keys are band names and values are the effective wavelength in
nanometers.

.. autodata:: lsdb_rubin.bands.band_wavelengths_ugrizy

Effective widths (``band_widths``)
---------------------------------------------

The horizontal bar drawn through each band's point in :doc:`/reference/plot_sed`,
expected to be a dictionary where keys are band names and values are the effective
width in nanometers.

.. autodata:: lsdb_rubin.bands.band_widths_ugrizy
