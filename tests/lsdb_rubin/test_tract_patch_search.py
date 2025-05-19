from lsdb.catalog import Catalog
from lsdb_rubin.tract_patch_search import tract_patch_search

Catalog.tract_patch_search = tract_patch_search


def test_tract_patch_search_tract_outer(lsst_skymap, small_sky_catalog):
    """Test the tract_patch_search function with the small_sky catalog."""
    tract = 792
    result = small_sky_catalog.tract_patch_search(
        skymap=lsst_skymap,
        tract=tract,
        fine=True,
        use_inner=False,
    )

    # Verify the result is a catalog and contains expected data
    assert result is not None
    assert result.hc_structure is not None
    assert result.compute().shape[0] > 0  # Ensure some rows are returned


def test_tract_patch_search_tract_inner(lsst_skymap, small_sky_catalog):
    """Test the tract_patch_search function with the small_sky catalog."""
    tract = 792
    result = small_sky_catalog.tract_patch_search(
        skymap=lsst_skymap,
        tract=tract,
        fine=True,
        use_inner=True,
    )

    # Verify the result is a catalog and contains expected data
    assert result is not None
    assert result.hc_structure is not None
    assert result.compute().shape[0] > 0  # Ensure some rows are returned


def test_tract_patch_search_tract_empty(lsst_skymap, small_sky_catalog):
    """Test the tract_patch_search function with the small_sky catalog."""
    tract = 0
    result = small_sky_catalog.tract_patch_search(
        skymap=lsst_skymap,
        tract=tract,
        fine=True,
        use_inner=False,
    )

    # Verify the result is length 0, as the tract does not overlap with any data
    assert len(result.compute()) == 0


def test_tract_patch_search_patch_outer(lsst_skymap, small_sky_catalog):
    """Test the tract_patch_search function with the small_sky catalog."""
    tract = 792
    patch = 62
    result = small_sky_catalog.tract_patch_search(
        skymap=lsst_skymap,
        tract=tract,
        patch=patch,
        fine=True,
        use_inner=False,
    )

    # Verify the result is a catalog and contains expected data
    assert result is not None
    assert result.hc_structure is not None
    assert result.compute().shape[0] > 0  # Ensure some rows are returned


def test_tract_patch_search_patch_inner(lsst_skymap, small_sky_catalog):
    """Test the tract_patch_search function with the small_sky catalog."""
    tract = 792
    patch = 62
    result = small_sky_catalog.tract_patch_search(
        skymap=lsst_skymap,
        tract=tract,
        patch=patch,
        fine=True,
        use_inner=True,
    )

    # Verify the result is a catalog and contains expected data
    assert result is not None
    assert result.hc_structure is not None
    assert result.compute().shape[0] > 0  # Ensure some rows are returned


def test_tract_patch_search_patch_empty(lsst_skymap, small_sky_catalog):
    """Test the tract_patch_search function with the small_sky catalog."""
    tract = 0
    patch = 0
    result = small_sky_catalog.tract_patch_search(
        skymap=lsst_skymap,
        tract=tract,
        patch=patch,
        fine=True,
        use_inner=True,
    )

    # Verify the result is length 0, as the patch does not overlap with any data
    assert len(result.compute()) == 0
