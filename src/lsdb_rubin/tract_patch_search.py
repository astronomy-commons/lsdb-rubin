import math

import nested_pandas as npd
from lsdb.core.search.abstract_search import AbstractSearch
from lsdb.core.search.polygon_search import polygon_filter
from lsdb.types import HCCatalogTypeVar


def tract_patch_search(
    self,
    skymap,
    tract: int,
    patch: int | None = None,
    fine: bool = True,
    use_inner: bool = False,
):
    """Perform a tract/patch search to filter the catalog.

    This method filters points within the given tract and patch, and filters
    partitions in the catalog that overlap with the specified tract and patch.

    A `skymap` is required to perform this search. A `skymap` is a spatial
    indexing structure that divides the sky into tracts and patches, allowing
    efficient spatial queries.

    Args:
        self (Catalog): The catalog to be filtered.
        skymap (lsst.skymap.BaseSkyMap): The skymap specifying tracts and patches
            within the sky.
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
    return self.search(TractPatchSearch(skymap, tract, patch, fine, use_inner))


class TractPatchSearch(AbstractSearch):
    """Perform a spatial search to filter the catalog based on tract and patch.

    This class filters points within the given tract and patch, and filters
    partitions in the catalog that overlap with the specified tract and patch.

    A `skymap` is required to perform this search. A `skymap` is a spatial
    indexing structure that divides the sky into tracts and patches, enabling
    efficient spatial queries.

    Attributes:
        skymap (lsst.skymap.BaseSkyMap): The skymap specifying tracts and patches.
        tract (int): The tract ID within the skymap.
        patch (int | None): The patch ID within the skymap. If None, the entire
            tract is used.
        fine (bool): If True, filters points within the tract/patch. If False,
            only filters partitions.
        use_inner (bool): If True, use the inner polygon for the search.
            If False, use the outer polygon. Defaults to False.
    """

    def __init__(
        self, skymap, tract: int, patch: int | None = None, fine: bool = True, use_inner: bool = False
    ):
        super().__init__(fine)
        self.skymap = skymap
        self.tract = tract
        self.patch = patch
        self.use_inner = use_inner

        self.tract_info = self.skymap.generateTract(self.tract)
        if self.patch is not None:
            self.patch_info = self.tract_info.getPatchInfo(self.patch)

    def filter_hc_catalog(self, hc_structure: HCCatalogTypeVar):
        """Filters the catalog pixels according to given tract/patch"""

        # Get the vertices of either the tract or the patch.
        if self.patch is not None:
            sphere_point_vertices = self.patch_info.getInnerSkyPolygon().getVertices()
            ra_dec_vertices = []
            for vertex in sphere_point_vertices:
                x, y, z = vertex.x(), vertex.y(), vertex.z()
                ra = math.degrees(math.atan2(y, x)) % 360  # RA in degrees
                dec = math.degrees(math.asin(z))  # Dec in degrees
                ra_dec_vertices.append((ra, dec))
        else:
            vertex_coords = self.tract_info._vertexCoordList
            ra_dec_vertices = [
                (vertex_coord.getLongitude().asDegrees(), vertex_coord.getLatitude().asDegrees())
                for vertex_coord in vertex_coords
            ]

        # Pass the vertices to the filter_by_polygon method.
        return hc_structure.filter_by_polygon(ra_dec_vertices)

    def search_points(self, frame: npd.NestedFrame, metadata) -> npd.NestedFrame:
        """Determine the search results within a data frame.

        Args:
            frame (npd.NestedFrame): The data frame to search.
            metadata (hats.catalog.TableProperties): Metadata for the data frame.

        Returns:
            npd.NestedFrame: The filtered data frame.
        """
        # Get boundaries of search area.
        if self.patch is not None:
            search_polygon = (
                self.patch_info.inner_sky_polygon if self.use_inner else self.patch_info.outer_sky_polygon
            )
        else:
            search_polygon = (
                self.tract_info.inner_sky_region if self.use_inner else self.tract_info.outer_sky_polygon
            )

        # Search the frame using the polygon filter.
        return polygon_filter(
            frame,
            search_polygon,
            metadata,
        )
