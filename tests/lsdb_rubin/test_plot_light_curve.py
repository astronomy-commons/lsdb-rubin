import matplotlib.pyplot as plt
import numpy as np
import pytest

from lsdb_rubin.plot_light_curve import band_names_ugrizy, plot_light_curve


def plotted_errors(ax):
    """Half-lengths of the vertical error bars actually drawn, keyed by band."""
    errors = {}
    for container in ax.containers:
        (bar_lines,) = container.lines[-1]
        errors[container.get_label()] = np.array(
            [(high - low) / 2 for (_, low), (_, high) in bar_lines.get_segments()]
        )
    return errors


def expected_errors(lc, err_field):
    """The values of ``err_field``, keyed by band, for the bands that get plotted."""
    expected = {}
    for band in band_names_ugrizy:
        data = lc.query(f"band == '{band}'")
        if len(data) > 0:
            expected[band] = data[err_field].to_numpy(dtype=float)
    return expected


def assert_plots_errors(lc, err_field, **kwargs):
    """Assert that plot_light_curve draws the error bars taken from ``err_field``."""
    plt.figure()
    plot_light_curve(lc, **kwargs)
    plotted = plotted_errors(plt.gca())
    expected = expected_errors(lc, err_field)

    assert len(expected) > 0
    assert plotted.keys() == expected.keys()
    for band, values in expected.items():
        np.testing.assert_allclose(plotted[band], values, rtol=1e-6)


def test_plot_basic(mock_dp1_frame):
    """Uses all defaults."""
    plt.figure()
    plot_light_curve(mock_dp1_frame.iloc[0]["diaObjectForcedSource"])
    fig = plt.gcf()
    ax = fig.gca()
    legend_els = ax.get_legend_handles_labels()
    assert legend_els[-1] == ["u", "g", "r", "i", "z", "y"]
    assert ax.xaxis.get_label_text() == "MJD"
    assert ax.yaxis.get_label_text() == "psfMag"


def test_plot_y_axis_mag(mock_dp1_frame):
    """Uses a different magnitude column."""
    plt.figure()
    plot_light_curve(mock_dp1_frame.iloc[0]["diaSource"], mag_field="scienceMag")
    fig = plt.gcf()
    ax = fig.gca()
    legend_els = ax.get_legend_handles_labels()
    assert legend_els[-1] == ["u", "g", "r", "i", "z", "y"]
    assert ax.xaxis.get_label_text() == "MJD"

    assert ax.yaxis.get_label_text() == "scienceMag"
    assert ax.yaxis_inverted()


def test_plot_y_axis_flux(mock_dp1_frame):
    """Uses a flux column - the y-axis should be ascending again"""
    plt.figure()
    plot_light_curve(mock_dp1_frame.iloc[0]["diaSource"], flux_field="psfFlux")
    fig = plt.gcf()
    ax = fig.gca()
    legend_els = ax.get_legend_handles_labels()
    assert legend_els[-1] == ["u", "g", "r", "i", "z", "y"]

    assert ax.xaxis.get_label_text() == "MJD"
    left_tick = ax.xaxis.get_majorticklabels()[0]._x
    right_tick = ax.xaxis.get_majorticklabels()[-1]._x
    assert left_tick < right_tick
    assert 60_000 < left_tick < 70_000

    assert ax.yaxis.get_label_text() == "psfFlux"
    bottom_tick = ax.yaxis.get_majorticklabels()[0]._y
    top_tick = ax.yaxis.get_majorticklabels()[-1]._y
    assert bottom_tick < top_tick
    assert not ax.yaxis_inverted()


def test_plot_5band(mock_dp1_frame):
    """This light curve only has data in 5 bands."""
    plt.figure()
    plot_light_curve(mock_dp1_frame.query("diaObjectId == 4629141259356225276").iloc[0]["diaSource"])
    fig = plt.gcf()
    ax = fig.gca()
    legend_els = ax.get_legend_handles_labels()
    assert legend_els[-1] == ["u", "g", "i", "z", "y"]
    assert ax.xaxis.get_label_text() == "MJD"
    assert ax.yaxis.get_label_text() == "psfMag"


def test_plot_x_axis_period(mock_dp1_frame):
    """Set a period for phase-folded light curve. The x-axis will just be [0, 1]"""
    plt.figure()
    plot_light_curve(mock_dp1_frame.iloc[0]["diaSource"], period=3.5)
    fig = plt.gcf()
    ax = fig.gca()
    legend_els = ax.get_legend_handles_labels()
    assert legend_els[-1] == ["u", "g", "r", "i", "z", "y"]
    assert ax.xaxis.get_label_text() == "phase"
    left_tick = ax.xaxis.get_majorticklabels()[0]._x
    right_tick = ax.xaxis.get_majorticklabels()[-1]._x
    assert left_tick == 0
    assert right_tick == 1

    assert ax.yaxis.get_label_text() == "psfMag"
    assert ax.yaxis_inverted()


def test_plot_x_axis_period_doubled(mock_dp1_frame):
    """Set a period for phase-folded light curve, but show two periods. The x-axis will just be [0, 2]"""
    plt.figure()
    plot_light_curve(mock_dp1_frame.iloc[0]["diaSource"], period=3.5, num_periods=2)
    fig = plt.gcf()
    ax = fig.gca()
    legend_els = ax.get_legend_handles_labels()
    assert legend_els[-1] == ["u", "g", "r", "i", "z", "y"]
    assert ax.xaxis.get_label_text() == "phase"
    left_tick = ax.xaxis.get_majorticklabels()[0]._x
    right_tick = ax.xaxis.get_majorticklabels()[-1]._x
    assert left_tick == 0
    assert right_tick == 2

    assert ax.yaxis.get_label_text() == "psfMag"
    assert ax.yaxis_inverted()


def test_plot_corrected_err_mag(mock_dp2_frame):
    """Corrected magnitude errors are plotted when we ask for them."""
    lc = mock_dp2_frame.iloc[0]["diaObjectForcedSource"]
    assert not np.allclose(lc["psfMagErr"], lc["psfMagErr_corrected"])

    assert_plots_errors(lc, "psfMagErr_corrected", corrected_err=True)


def test_plot_corrected_err_flux(mock_dp2_frame):
    """The corrected error field is derived from the flux field name, too."""
    lc = mock_dp2_frame.iloc[0]["diaObjectForcedSource"]

    assert_plots_errors(lc, "psfFluxErr_corrected", flux_field="psfFlux", corrected_err=True)


def test_plot_corrected_err_diff_flux(mock_dp2_frame):
    """Difference-image fluxes have their own corrected error field."""
    lc = mock_dp2_frame.iloc[0]["diaObjectForcedSource"]

    assert_plots_errors(lc, "psfDiffFluxErr_corrected", flux_field="psfDiffFlux", corrected_err=True)


def test_plot_original_err_by_default(mock_dp2_frame):
    """We plot the original errors unless corrected ones are asked for, even in DP2 data."""
    lc = mock_dp2_frame.iloc[0]["diaObjectForcedSource"]
    assert "psfMagErr_corrected" in lc.columns

    assert_plots_errors(lc, "psfMagErr")
    assert_plots_errors(lc, "psfMagErr", corrected_err=False)


def test_plot_corrected_err_missing(mock_dp2_frame):
    """diaSource has no corrected errors, in the mock as in EDP2, so we fail loudly."""
    lc = mock_dp2_frame.iloc[0]["diaSource"]
    assert "psfMagErr_corrected" not in lc.columns

    plt.figure()
    with pytest.raises(ValueError, match="psfMagErr_corrected"):
        plot_light_curve(lc, corrected_err=True)


def test_plot_corrected_err_missing_for_brightness_field(mock_dp2_frame):
    """Only some brightness fields have a corrected counterpart, scienceMag is not one."""
    lc = mock_dp2_frame.iloc[0]["diaSource"]
    assert "scienceMagErr" in lc.columns

    plt.figure()
    with pytest.raises(ValueError, match="scienceMagErr_corrected"):
        plot_light_curve(lc, mag_field="scienceMag", corrected_err=True)
