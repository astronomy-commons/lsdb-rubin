import lsdb
from pathlib import Path
import lsdb
import numpy as np
import pandas as pd
import sys


def random_access(catalog_path, verbose=False):
    """Run the contents of the `HATS Data Preview 1 on RSP` notebook.
    Any deviation from expected values will result in assertion failures.

    See https://github.com/lsst-sitcom/linccf/blob/main/RSP/random_access.ipynb"""
    if catalog_path is None:
        catalog_path = Path(__file__).parent.parent.parent.parent / "tests" / "data" / "mock_dp1_1000"

    ### Cell 1
    object_collection = lsdb.open_catalog(catalog_path)

    ### Cell 2
    pixel_statistics = object_collection.per_pixel_statistics()
    counts = pd.to_numeric(pixel_statistics["diaObjectId: row_count"], errors="coerce")
    pixel_counts = counts.groupby(level=0).sum()

    ### Cell 3
    partition_indices = []
    for percentile in [10, 50, 90]:
        q = np.percentile(pixel_counts, percentile)
        if verbose:
            print(f"Percentile: {percentile}, Quartile: {q}")
        index = int(np.argmin(np.abs(pixel_counts - q)))
        closest_value = pixel_counts.iloc[index]
        if verbose:
            print(f"Closest value: {closest_value}, partition index: {index}")
        partition_indices.append(index)

    ### Cell 4
    for index in partition_indices:
        if verbose:
            print(f"Sampling partition {index} of size {pixel_counts.iloc[index]}")
        object_collection.sample(index, n=100, seed=10)


if __name__ == "__main__":
    catalog_path = None
    if len(sys.argv) == 2:
        catalog_path = Path(sys.argv[1])

    random_access(catalog_path)
