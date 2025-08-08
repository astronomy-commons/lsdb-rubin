import matplotlib.pyplot as plt
from lsdb_rubin.plot_light_curve import plot_light_curve


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
