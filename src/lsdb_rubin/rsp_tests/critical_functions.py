import tempfile
from pathlib import Path

import lsdb


def critical_functions():
    """Run the contents of the `Test of LSDB Critical functions` notebook.
    Any deviation from expected values will result in assertion failures.

    See https://github.com/lsst-sitcom/linccf/blob/main/RSP/critical_fs.ipynb"""
    ### Cell 1
    tmp_path = tempfile.TemporaryDirectory()
    tmp_dir = Path(tmp_path.name)

    ### Cell 2
    region = lsdb.ConeSearch(ra=53.13, dec=-28.10, radius_arcsec=20)
    expected_pixels = [lsdb.HealpixPixel(7, 143742)]

    gen_catalog_1 = lsdb.generate_catalog(100, 5, seed=53, search_region=region)
    assert gen_catalog_1.get_healpix_pixels() == expected_pixels
    gen_catalog_1.to_hats(tmp_dir / "catalog_1", catalog_name="catalog_1", overwrite=True)

    gen_catalog_2 = lsdb.generate_catalog(100, 5, seed=28, search_region=region)
    assert gen_catalog_2.get_healpix_pixels() == expected_pixels
    gen_catalog_2_computed = gen_catalog_2.compute()

    ### Cell 3
    catalog_1 = lsdb.open_catalog(tmp_dir / "catalog_1")
    catalog_2 = lsdb.from_dataframe(gen_catalog_2_computed)

    ### Cell 4
    crossmatch_result = lsdb.crossmatch(catalog_1, gen_catalog_2)
    assert len(crossmatch_result.compute()) > 0

    ### Cell 5
    def sum_id(df):
        import pandas as pd

        return pd.DataFrame([{"sum": df["id"].sum()}])

    unrealized = catalog_1.map_partitions(sum_id)
    assert unrealized.compute()["sum"][0] == 52752

    unrealized = catalog_2.map_partitions(sum_id)
    assert unrealized.compute()["sum"][0] == 56349

    ### Cell 6
    tmp_path.cleanup()


if __name__ == "__main__":
    critical_functions()
