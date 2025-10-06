from typing import TYPE_CHECKING

from lsdb.core.search.abstract_search import AbstractSearch
from lsdb.core.search.region_search import box_filter
from lsdb.types import HCCatalogTypeVar

if TYPE_CHECKING:
    import nested_pandas as npd


def tract_patch_search(
    self,
    skymap_reader,
    tract: int,
    patch: int | None = None,
    fine: bool = True,
):
    """Perform a tract/patch search to filter the catalog.

    This method filters points within the given tract and patch, and filters
    partitions in the catalog that overlap with the specified tract and patch.

    A `skymap_reader` is required to perform this search. A `skymap_reader`
    is an instance of `skymap_convert.ConvertedSkymapReader` that provides
    access to the vertices of tracts and patches in the sky.

    Args:
        self (Catalog): The catalog to be filtered.
        skymap_reader (lsdb_rubin.skymap_convert.ConvertedSkymapReader): The skymap reader
            specifying tracts and patches within the sky.
        tract (int): The tract ID within the given skymap.
        patch (int): The patch ID within the given skymap. If None, the entire
            tract is used.
        fine (bool): True if points are to be filtered, False if only partitions
            should be filtered. Defaults to True.
        use_inner (bool): If True, use the inner polygon for the search.
            If False, use the outer polygon. Defaults to False.

    Returns:
        A new Catalog containing the points filtered to those within the tract
        and patch, and the partitions that overlap the tract and patch.
    """
    return self.search(TractPatchSearch(skymap_reader, tract, patch, fine))


class TractPatchSearch(AbstractSearch):
    """Perform a spatial search to filter the catalog based on tract and patch.

    This class filters points within the given tract and patch, and filters
    partitions in the catalog that overlap with the specified tract and patch.

    A `skymap_reader` is required to perform this search. A `skymap_reader`
    is an instance of `skymap_convert.ConvertedSkymapReader` that provides
    access to the vertices of tracts and patches in the sky.

    Attributes:
        skymap_reader (skymap_convert.ConvertedSkymapReader): The skymap reader specifying vertices of tracts
            and patches.
        tract (int): The tract ID within the skymap.
        patch (int | None): The patch ID within the skymap. If None, the entire
            tract is used.
        fine (bool): If True, filters points within the tract/patch. If False,
            only filters partitions.
    """

    def __init__(self, skymap_reader, tract: int, patch: int | None = None, fine: bool = True):
        super().__init__(fine)
        self.skymap_reader = skymap_reader
        self.tract = tract
        self.patch = patch

    def filter_hc_catalog(self, hc_structure: HCCatalogTypeVar):
        """Filters the catalog pixels according to given tract/patch"""

        # Get the vertices of either the tract or the patch.
        if self.patch is not None:
            ra_dec_vertices = self.skymap_reader.get_patch_vertices(self.tract, self.patch)
        else:
            ra_dec_vertices = self.skymap_reader.get_tract_vertices(self.tract)

        # Get the ra and dec ranges from the vertices.
        ra_values = [v[0] for v in ra_dec_vertices]
        dec_values = [v[1] for v in ra_dec_vertices]
        ra_range = (min(ra_values), max(ra_values))
        dec_range = (min(dec_values), max(dec_values))

        # Pass the vertices to the filter_by_box method.
        return hc_structure.filter_by_box(ra_range, dec_range)

    def search_points(self, frame: "npd.NestedFrame", metadata) -> "npd.NestedFrame":
        """Determine the search results within a data frame.

        Args:
            frame (npd.NestedFrame): The data frame to search.
            metadata (hats.catalog.TableProperties): Metadata for the data frame.

        Returns:
            npd.NestedFrame: The filtered data frame.
        """
        # Get boundaries of search area.
        if self.patch is not None:
            search_vertices = self.skymap_reader.get_patch_vertices(self.tract, self.patch)
        else:
            search_vertices = self.skymap_reader.get_tract_vertices(self.tract)

        # Get ra and dec ranges from the vertices.
        ra_values = [v[0] for v in search_vertices]
        dec_values = [v[1] for v in search_vertices]

        # Search the frame using the polygon filter.
        return box_filter(
            frame,
            ra=(min(ra_values), max(ra_values)),
            dec=(min(dec_values), max(dec_values)),
            metadata=metadata,
        )
