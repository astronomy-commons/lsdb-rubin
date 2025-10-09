Plot Light Curves
=============================

We provide many customization options for display of multi-band light curves.

If you want additional configuration, you may be better served creating your own plotting
function, as this is intended for quick inspection of individual lightcurves in HATS-formatted
data products.

To see the method and configuration in action, check out the
:doc:`/notebooks/plot_light_curves` notebook.

.. autofunction:: lsdb_rubin.plot_light_curve.plot_light_curve

Color palattes (``filter_colors``)
-----------------------------------------

A color palatte will be used to distinguish multi-band data, and is expected
to be a dictionary, where keys are band names, and values are the color, as 
accepted by matplotlib.

.. autodata:: lsdb_rubin.plot_light_curve.plot_filter_colors_white_background
.. autodata:: lsdb_rubin.plot_light_curve.plot_filter_colors_black_background
.. autodata:: lsdb_rubin.plot_light_curve.plot_filter_colors_rainbow

Symbols (``filter_symbols``)
-----------------------------------------

Symbols will be used to distinguish multi-band data, and is expected
to be a dictionary, where keys are band names, and values are the symbol
marker, as accepted by matplotlib.

.. autodata:: lsdb_rubin.plot_light_curve.plot_symbols
.. autodata:: lsdb_rubin.plot_light_curve.plot_filter_symbols

Line Styles (``filter_linestyles``)
-----------------------------------------

.. autodata:: lsdb_rubin.plot_light_curve.plot_linestyles_none
.. autodata:: lsdb_rubin.plot_light_curve.plot_linestyles

Band Names (``band_names``)
-----------------------------------------

.. autodata:: lsdb_rubin.plot_light_curve.band_names_ugrizy
.. autodata:: lsdb_rubin.plot_light_curve.band_names_lsst_ugrizy
