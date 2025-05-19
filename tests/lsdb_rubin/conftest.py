from pathlib import Path

import lsdb
import pickle
import pytest

DATA_DIR_NAME = "data"
TEST_DIR = Path(__file__).parent
SKYMAP_DIR_NAME = "skymaps"
SMALL_SKY_DIR_NAME = "small_sky"


@pytest.fixture
def test_data_dir():
    return Path(TEST_DIR) / DATA_DIR_NAME


@pytest.fixture
def lsst_skymap(test_data_dir):
    """Fixture to load the LSST skymap from local file."""
    skymap_path = test_data_dir / SKYMAP_DIR_NAME / "skyMap_lsst_cells_v1_skymaps.pickle"
    with open(skymap_path, "rb") as f:
        skymap = pickle.load(f)
    return skymap


@pytest.fixture
def small_sky_catalog(test_data_dir):
    """Fixture to load the small_sky catalog."""
    catalog_path = test_data_dir / SMALL_SKY_DIR_NAME
    return lsdb.read_hats(catalog_path)
