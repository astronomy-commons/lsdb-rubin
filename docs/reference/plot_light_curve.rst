Plot Light Curves
=============================

We provide many customization options for display of multi-band light curves.

If you want additional configuration, you may be better served creating your own plotting
function, as this is intended for quick inspection of individual lightcurves in HATS-formatted
data products.

To see the method and configuration in action, check out the
:doc:`/notebooks/plot_light_curves` notebook.

.. autofunction:: lsdb_rubin.plot_light_curve.plot_light_curve

Colors, symbols, line styles, and band names
--------------------------------------------------

``filter_colors``, ``filter_symbols``, ``filter_linestyles``, and ``band_names`` all take
the shared band defaults. See :doc:`/reference/bands`.
