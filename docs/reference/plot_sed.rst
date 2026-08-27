Plot Broadband SEDs
=============================

Plot an object's per-band measurements against each band's wavelength.

Each band is read straight off the object's own per-band columns - the ones named
``f"{band}_{brightness_field}"``, such as ``u_psfMag`` or ``g_psfFlux`` - and plotted
against that band's wavelength. The matching uncertainty is read from
``f"{band}_{brightness_field}Err"``, when the object has such a column.

If you want additional configuration, you may be better served creating your own plotting
function, as this is intended for quick inspection of individual objects in HATS-formatted
data products.

.. autofunction:: lsdb_rubin.plot_sed.plot_sed

X-axis units
--------------------------------------------------

``x_units`` picks what the x-axis measures. It takes anything ``astropy.units`` reads as a
wavelength (``"nm"``, the default, or ``"angstrom"``, ``"micron"``), a frequency (``"THz"``,
``"GHz"``, ``"Hz"``), an energy (``"eV"``, ``"keV"``), or a wavenumber (``"1/cm"``) - as a
string, or as an ``astropy`` unit object. Whichever you pick, ``band_wavelengths`` and ``band_widths``
are still given in nanometers; this converts them for display only.

.. autodata:: lsdb_rubin.plot_sed.x_axis_quantities

Y-axis units
--------------------------------------------------

``y_units`` picks what the y-axis measures. By default the values are plotted as the catalog
stores them - nanojanskys for a ``flux_field``, AB magnitudes for a ``mag_field``. Pass
``y_units`` and they are converted from there through
`astropy's spectral flux density equivalencies
<https://docs.astropy.org/en/stable/units/equivalencies.html#spectral-flux-and-luminosity-density-units>`_,
at each band's own wavelength: ``"nJy"``, ``"ABmag"``, ``"FLAM"``, or any unit astropy can
reach, such as ``u.erg / u.s / u.cm**2 / u.AA``.

The axis is labelled with what it measures rather than the column it came from, worked out
from the unit's ``physical_type`` - so ``"nJy"`` and ``"FLAM"`` both read as a flux density,
with the units after it saying which, and either magnitude system reads as a magnitude. The
column the measurements were read from titles the legend instead.

.. autodata:: lsdb_rubin.plot_sed.y_axis_quantities
.. autodata:: lsdb_rubin.plot_sed.y_unit_aliases
.. autodata:: lsdb_rubin.plot_sed.flux_column_unit
.. autodata:: lsdb_rubin.plot_sed.mag_column_unit

Scaling and inverting the axes
--------------------------------------------------

Both axes are left linear, and ``plot_sed`` draws on the axes you pass as ``ax`` - or on the
current ones - so you can scale or invert either axis with matplotlib after the call. The
y-axis is automatically inverted whenever what it carries is a magnitude.

Colors, symbols, wavelengths, and band names
--------------------------------------------------

``filter_colors``, ``filter_symbols``, ``band_names``, ``band_wavelengths``, and
``band_widths`` all take the shared band defaults. See :doc:`/reference/bands`.
