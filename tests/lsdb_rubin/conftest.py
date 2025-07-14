from pathlib import Path

import lsdb
import pytest
from skymap_convert import ConvertedSkymapReader

TEST_DIR = Path(__file__).parent.parent
SKYMAP_DIR_NAME = "skymaps"
SMALL_SKY_DIR_NAME = "small_sky"


@pytest.fixture
def test_data_dir():
    """Fixture to provide the path to the test data directory."""
    return Path(TEST_DIR) / "data"


@pytest.fixture
def lsst_skymap_reader(test_data_dir):
    """Fixture to load the LSST skymap reader from local file."""
    # skymap_path = test_data_dir / SKYMAP_DIR_NAME / "skyMap_lsst_cells_v1_skymaps.pickle"
    # with open(skymap_path, "rb") as f:
    #     lsst_skymap = pickle.load(f)
    # return lsst_skymap
    skymap_reader = ConvertedSkymapReader(preset="lsst_skymap")
    return skymap_reader


@pytest.fixture
def small_sky_catalog(test_data_dir):
    """Fixture to load the small_sky catalog."""
    catalog_path = test_data_dir / SMALL_SKY_DIR_NAME
    return lsdb.read_hats(catalog_path)
