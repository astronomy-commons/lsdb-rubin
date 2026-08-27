Plot Broadband SEDs
=============================

Plot an object's per-band measurements against each band's effective wavelength.

Each band is read straight off the object's own per-band columns - the ones named
``f"{band}_{brightness_field}"``, such as ``u_psfMag`` or ``g_psfFlux`` - and plotted
against that band's effective wavelength. The matching uncertainty is read from
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

Frequency, energy, and wavenumber all run the opposite way to wavelength, so the bands plot
right to left, with ``u`` at the high end. Follow the call with ``plt.gca().invert_xaxis()``
if you would rather keep them in ``ugrizy`` order.

.. autodata:: lsdb_rubin.plot_sed.x_axis_quantities

Colors, symbols, wavelengths, and band names
--------------------------------------------------

``filter_colors``, ``filter_symbols``, ``band_names``, ``band_wavelengths``, and
``band_widths`` all take the shared band defaults. See :doc:`/reference/bands`.
