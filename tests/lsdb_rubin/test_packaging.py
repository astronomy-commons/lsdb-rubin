import lsdb_rubin


def test_version():
    """Check to see that we can get the package version"""
    assert lsdb_rubin.__version__ is not None
