from pathlib import Path

import lsdb
import pytest
from hats.io.file_io import read_parquet_file_to_pandas
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


@pytest.fixture
def mock_dp1_frame(test_data_dir):
    """Fixture to load the small_sky catalog."""
    parquet_path = test_data_dir / "mock_dp1_1000" / "dataset" / "Norder=0" / "Dir=0" / "Npix=0.parquet"
    return read_parquet_file_to_pandas(parquet_path)


@pytest.fixture
def mock_dp2_frame(test_data_dir):
    """Fixture to load the mock EDP2 catalog.

    Entirely generated data following the schema of the ``dia_object_lc`` catalog of the
    DP2 release candidate - no real Rubin measurement is in here. In particular the
    ``diaObjectForcedSource`` light curves carry corrected error subcolumns, while
    ``diaSource`` does not, as in EDP2 itself.
    """
    parquet_path = test_data_dir / "mock_dp2_20" / "dataset" / "Norder=0" / "Dir=0" / "Npix=0.parquet"
    return read_parquet_file_to_pandas(parquet_path)


@pytest.fixture
def mock_dp2_object_frame(test_data_dir):
    """Fixture to load the mock EDP2 object catalog.

    Entirely generated data following the schema of the ``object_lc`` catalog of the DP2
    release candidate - no real Rubin measurement is in here. Objects are positioned with
    ``coord_ra``/``coord_dec`` rather than ``ra``/``dec``, and carry ``objectForcedSource``
    light curves with corrected error subcolumns.
    """
    parquet_path = (
        test_data_dir / "mock_dp2_object_20" / "dataset" / "Norder=0" / "Dir=0" / "Npix=0.parquet"
    )
    return read_parquet_file_to_pandas(parquet_path)
