import astropy.units as units
import matplotlib.pyplot as plt
import pandas as pd
import pytest

from lsdb_rubin.plot_sed import band_wavelengths_ugrizy, plot_sed


def measured_bands(obj, brightness_field="psfMag"):
    """The bands this object actually has a measurement in, in ugrizy order."""
    return [band for band in "ugrizy" if not pd.isna(obj[f"{band}_{brightness_field}"])]


def test_plot_returns_the_axes_it_drew_on(mock_dp2_object_frame, figure):
    """The axes handed back are the ones that were already current, not a new figure's."""
    returned = plot_sed(mock_dp2_object_frame.iloc[0])

    assert returned.get_figure() is figure


def test_plot_on_given_axes(mock_dp2_object_frame, figure):
    """An explicit `ax` is drawn on, whichever axes happen to be current."""
    ax, other_axes = figure.subplots(1, 2)
    plt.sca(other_axes)

    returned = plot_sed(mock_dp2_object_frame.iloc[0], ax=ax)

    assert returned is ax
    assert len(ax.lines) > 0
    assert len(other_axes.lines) == 0


def test_plot_basic(mock_dp2_object_frame):
    """Uses all defaults - title, axis labels and legend."""
    obj = mock_dp2_object_frame.iloc[0]
    ax = plot_sed(obj)

    assert ax.get_title() == "LSST broadband SED"
    assert ax.xaxis.get_label_text() == "wavelength (nm)"
    assert ax.yaxis.get_label_text() == "magnitude (mag(AB))"
    assert ax.get_legend_handles_labels()[-1] == list("ugizy")


def test_plot_missing_error_column(mock_dp2_object_frame):
    """A measurement with no matching Err column is still plotted, as a bare point."""
    obj = mock_dp2_object_frame.iloc[0]

    # psfMagErr exists, so the points have error bars.
    with_errors = plot_sed(obj)
    assert len(with_errors.lines) > 0
    assert all(container.has_yerr for container in with_errors.containers)

    # kronRad has no kronRadErr alongside it.
    _, ax = plt.subplots()
    assert "kronRadErr" not in obj.index
    without_errors = plot_sed(obj, mag_field="kronRad", ax=ax)
    assert len(without_errors.lines) > 0
    assert not any(container.has_yerr for container in without_errors.containers)


def test_plot_filter_colors_and_symbols(mock_dp2_object_frame):
    """Per-band colors and symbols reach the artists, one point per band."""
    obj = mock_dp2_object_frame.iloc[0]
    ax = plot_sed(
        obj,
        filter_colors=dict.fromkeys("ugrizy", "#123456"),
        filter_symbols=dict.fromkeys("ugrizy", "D"),
    )

    # One line artist per band, each holding a single point.
    assert len(ax.lines) == len(measured_bands(obj))
    for line in ax.lines:
        assert len(line.get_xdata()) == 1
        assert line.get_marker() == "D"
        assert line.get_color() == "#123456"


def test_plot_kwargs_reach_the_artists(mock_dp2_object_frame):
    """Anything in plot_kwargs is handed to errorbar as it is."""
    ax = plot_sed(mock_dp2_object_frame.iloc[0], plot_kwargs={"markersize": 11, "alpha": 0.25})

    assert len(ax.lines) > 0
    for line in ax.lines:
        assert line.get_markersize() == 11
        assert line.get_alpha() == 0.25


@pytest.mark.parametrize(
    ("kwargs", "title"),
    [
        ({}, "psfMag"),
        ({"y_units": "nJy"}, "psfMag"),
        ({"flux_field": "psfFlux", "y_units": "ABmag"}, "psfFlux"),
        ({"legend_kwargs": {"title": "bands"}}, "bands"),
    ],
)
def test_plot_legend_names_the_column(mock_dp2_object_frame, kwargs, title):
    """The legend is titled with the column read, whatever units the axis ends up in."""
    ax = plot_sed(mock_dp2_object_frame.iloc[0], **kwargs)

    assert ax.get_legend().get_title().get_text() == title


def test_plot_unknown_band(mock_dp2_object_frame):
    """A measured band with no wavelength is an error, not a silent skip."""
    with pytest.raises(KeyError, match="No wavelength for band"):
        plot_sed(mock_dp2_object_frame.iloc[0], band_names=["u", "g"], band_wavelengths={"u": 367.0})


def test_plot_band_widths(mock_dp2_object_frame):
    """Each band gets a horizontal bar spanning its throughput FWHM."""
    obj = mock_dp2_object_frame.iloc[0]
    widths = {"u": 100.0, "g": 50.0}
    ax = plot_sed(obj, band_widths=widths, band_names=["u", "g"])

    assert [container.has_xerr for container in ax.containers] == [True, True]
    # The bar spans half a width either side of the band's wavelength.
    for container, band in zip(ax.containers, ["u", "g"], strict=True):
        center = band_wavelengths_ugrizy[band]
        half = widths[band] / 2
        bar = container[2][0].get_segments()[0]
        assert bar[:, 0].tolist() == [center - half, center + half]


def test_plot_missing_band_width(mock_dp2_object_frame):
    """A band with no width in the mapping is drawn without a bar."""
    obj = mock_dp2_object_frame.iloc[0]
    ax = plot_sed(obj, band_widths={})

    assert len(ax.containers) == len(measured_bands(obj))
    assert not any(container.has_xerr for container in ax.containers)


def test_plot_x_axis(mock_dp2_object_frame):
    """Each band's point sits at that band's wavelength, in nanometers by default."""
    obj = mock_dp2_object_frame.iloc[0]
    assert measured_bands(obj) == list("ugizy")

    ax = plot_sed(obj)

    # Object 0 has no r-band measurement.
    plotted_xdata = [line.get_xdata()[0] for line in ax.lines]
    assert plotted_xdata == [band_wavelengths_ugrizy[band] for band in "ugizy"]


@pytest.mark.parametrize(
    ("x_units", "label"),
    [
        ("angstrom", "wavelength (Å)"),
        ("THz", "frequency (THz)"),
        ("Hz", "frequency (Hz)"),
        ("eV", "energy (eV)"),
        ("1/cm", "wavenumber (cm⁻¹)"),
    ],
)
def test_plot_x_axis_label(mock_dp2_object_frame, x_units, label):
    """Every quantity astropy's spectral() can reach names its own axis."""
    ax = plot_sed(mock_dp2_object_frame.iloc[0], x_units=x_units)
    assert ax.xaxis.get_label_text() == label


def test_plot_x_units_accepts_unit_objects(mock_dp2_object_frame):
    """An astropy unit is as good as the string that names it."""
    from_string = plot_sed(mock_dp2_object_frame.iloc[0], x_units="micron")
    plt.figure()
    from_unit = plot_sed(mock_dp2_object_frame.iloc[0], x_units=units.micron)
    assert from_unit.xaxis.get_label_text() == from_string.xaxis.get_label_text()
    for one, other in zip(from_string.lines, from_unit.lines, strict=True):
        assert one.get_xdata()[0] == other.get_xdata()[0]


def test_plot_x_units_wrong_quantity(mock_dp2_object_frame):
    """A unit that is not on the spectral axis at all is an error."""
    with pytest.raises(ValueError, match="Cannot plot an SED against Jy"):
        plot_sed(mock_dp2_object_frame.iloc[0], x_units="Jy")


@pytest.mark.parametrize(
    ("kwargs", "brightness_field", "label", "inverted"),
    [
        ({}, "psfMag", "magnitude (mag(AB))", True),
        ({"flux_field": "psfFlux"}, "psfFlux", "flux density (nJy)", False),
        ({"mag_field": "kronRad"}, "kronRad", "magnitude (mag(AB))", True),
    ],
)
def test_plot_y_axis(mock_dp2_object_frame, kwargs, brightness_field, label, inverted):
    """The y-axis reads its column untouched, and is labeled in the column's own units."""
    obj = mock_dp2_object_frame.iloc[0]
    ax = plot_sed(obj, **kwargs)

    assert ax.yaxis.get_label_text() == label
    for line, band in zip(ax.lines, measured_bands(obj, brightness_field), strict=True):
        assert line.get_ydata()[0] == pytest.approx(obj[f"{band}_{brightness_field}"])
    assert ax.yaxis_inverted() == inverted


def test_plot_y_units_from_magnitudes(mock_dp2_object_frame):
    """Magnitudes convert to a flux density, and the axis stops being upside-down."""
    obj = mock_dp2_object_frame.iloc[0]
    ax = plot_sed(obj, y_units="nJy")

    assert not ax.yaxis_inverted()
    for line, band in zip(ax.lines, measured_bands(obj), strict=True):
        expected = (obj[f"{band}_psfMag"] * units.ABmag).to_value(units.nJy)
        assert line.get_ydata()[0] == pytest.approx(expected)


def test_plot_y_units_from_fluxes(mock_dp2_object_frame):
    """Fluxes convert to magnitudes, and the axis is inverted for them."""
    obj = mock_dp2_object_frame.iloc[0]
    ax = plot_sed(obj, flux_field="psfFlux", y_units="ABmag")

    assert ax.yaxis_inverted()
    for line, band in zip(ax.lines, measured_bands(obj, "psfFlux"), strict=True):
        expected = (obj[f"{band}_psfFlux"] * units.nJy).to_value(units.ABmag)
        assert line.get_ydata()[0] == pytest.approx(expected)


def test_plot_y_units_missing_error_column(mock_dp2_object_frame):
    """A column with no Err beside it converts just the same, and stays a bare point."""
    obj = mock_dp2_object_frame.iloc[0]
    assert "kronRadErr" not in obj.index

    ax = plot_sed(obj, mag_field="kronRad", y_units="nJy")

    assert not any(container.has_yerr for container in ax.containers)
    for line, band in zip(ax.lines, measured_bands(obj, "kronRad"), strict=True):
        expected = (obj[f"{band}_kronRad"] * units.ABmag).to_value(units.nJy)
        assert line.get_ydata()[0] == pytest.approx(expected)


def test_plot_y_units_uses_each_band_wavelength(mock_dp2_object_frame):
    """A flux density per wavelength is converted at the band's own wavelength."""
    obj = mock_dp2_object_frame.iloc[0]
    flam = units.erg / (units.s * units.cm**2 * units.AA)
    ax = plot_sed(obj, y_units="FLAM")

    for line, band in zip(ax.lines, measured_bands(obj), strict=True):
        equivalency = units.spectral_density(band_wavelengths_ugrizy[band] * units.nm)
        expected = (obj[f"{band}_psfMag"] * units.ABmag).to_value(flam, equivalency)
        assert line.get_ydata()[0] == pytest.approx(expected)


def test_plot_y_units_accepts_unit_objects(mock_dp2_object_frame):
    """The "FLAM" shorthand and the unit it names give the same plot."""
    from_alias = plot_sed(mock_dp2_object_frame.iloc[0], y_units="FLAM")
    plt.figure()
    from_unit = plot_sed(mock_dp2_object_frame.iloc[0], y_units=units.erg / units.s / units.cm**2 / units.AA)

    assert from_alias.yaxis.get_label_text() == from_unit.yaxis.get_label_text()
    for one, other in zip(from_alias.lines, from_unit.lines, strict=True):
        assert one.get_ydata()[0] == other.get_ydata()[0]


@pytest.mark.parametrize(
    ("y_units", "label"),
    [
        ("nJy", "flux density (nJy)"),
        ("FNU", "flux density (erg Hz⁻¹ s⁻¹ cm⁻²)"),
        ("FLAM", "flux density (erg Å⁻¹ s⁻¹ cm⁻²)"),
        ("PHOTLAM", "photon flux density (ph Å⁻¹ s⁻¹ cm⁻²)"),
        ("ABmag", "magnitude (mag(AB))"),
        ("STmag", "magnitude (mag(ST))"),
        (units.erg / (units.s * units.cm**2), "energy flux (erg s⁻¹ cm⁻²)"),
    ],
)
def test_plot_y_axis_label(mock_dp2_object_frame, y_units, label):
    """The label names what the axis measures."""
    ax = plot_sed(mock_dp2_object_frame.iloc[0], y_units=y_units)

    assert ax.yaxis.get_label_text() == label


def test_plot_y_units_wrong_quantity(mock_dp2_object_frame):
    """A unit no flux density converts into is an error, raised before anything is drawn."""
    figure = plt.gcf()
    with pytest.raises(ValueError, match="which is read as mag\\(AB\\)"):
        plot_sed(mock_dp2_object_frame.iloc[0], y_units="deg")
    assert len(figure.gca().lines) == 0


def test_plot_y_units_unparseable(mock_dp2_object_frame):
    """A unit astropy cannot even read is an error from astropy itself."""
    with pytest.raises(ValueError, match="did not parse as unit"):
        plot_sed(mock_dp2_object_frame.iloc[0], y_units="nJyy")
