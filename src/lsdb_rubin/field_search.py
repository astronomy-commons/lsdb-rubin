from __future__ import annotations

from lsdb.core.search.region_search import ConeSearch


class FieldSearch(ConeSearch):
    """Filter a catalog by a cone about a Rubin field center.

    Parameters
    ----------
    field : str
        Name of the field, one of the keys of :attr:`FIELDS`. Upper-cased
        before the lookup, so the case does not matter. The error message of an
        unknown name also lists the valid ones.
    radius_arcsec : float
        Cone radius in arcseconds.
    fine : bool
        True if points are to be filtered, False if only partitions should be
        filtered.

    Attributes
    ----------
    FIELDS : dict[str, tuple[float, float]]
        Field name to ``(ra, dec)`` center in degrees, ICRS.
    field : str
        The name of the selected field, upper-cased.

    Raises
    ------
    ValueError
        If ``field`` is not a known field of this data release.

    References
    ----------
    Field centers are transcribed from the Rubin data release documentation:

    - DP1 fields: https://dp1.lsst.io/overview/observations.html#field-centers
    - DP2 small fields: https://dp2.lsst.io/overview/observations.html#small-fields
    - DP2 deep drilling fields:
      https://dp2.lsst.io/overview/observations.html#deep-drilling-fields
    """

    FIELDS: dict[str, tuple[float, float]] = {}

    def __init__(self, field: str, *, radius_arcsec: float, fine: bool):
        field = field.upper()
        if field not in self.FIELDS:
            raise ValueError(f"Unknown field {field!r}, must be one of: {', '.join(self.FIELDS)}")
        ra, dec = self.FIELDS[field]
        super().__init__(ra, dec, radius_arcsec, fine=fine)
        self.field = field


class DP1FieldSearch(FieldSearch):
    """Filter a catalog to one of the seven Rubin DP1 fields.

    Parameters
    ----------
    field : str
        Name of the field, one of the keys of :attr:`FIELDS`. Upper-cased
        before the lookup, so the case does not matter. The error message of an
        unknown name also lists the valid ones.
    radius_arcsec : float (default 7200.0)
        Cone radius in arcseconds, two degrees by default, since it covers
        every DP1 field.
    fine : bool (default True)
        True if points are to be filtered, False if only partitions should be
        filtered.

    Examples
    --------
    >>> import lsdb
    >>> from lsdb_rubin import DP1FieldSearch

    The available field names are the keys of :attr:`FIELDS`:

    >>> print(", ".join(DP1FieldSearch.FIELDS))
    47 TUC, LOW ECLIPTIC LATITUDE, FORNAX DSPH, ECDFS, EDFS, LOW GALACTIC LATITUDE, SEAGULL

    >>> search = DP1FieldSearch("ECDFS")
    >>> search.ra, search.dec, search.radius_arcsec
    (53.13, -28.1, 7200.0)

    Pass it to :func:`lsdb.open_catalog` to filter as the catalog is opened, or
    to :meth:`lsdb.catalog.Catalog.search` to filter one you already have:

    >>> catalog = lsdb.open_catalog(DP1_COLLECTION_PATH, search_filter=search)  # doctest: +SKIP
    >>> catalog = lsdb.open_catalog(DP1_COLLECTION_PATH).search(search)  # doctest: +SKIP
    """

    def __init__(self, field: str, *, radius_arcsec: float = 7200.0, fine: bool = True):
        super().__init__(field, radius_arcsec=radius_arcsec, fine=fine)

    # Table 1. Keys are shortened; the full names from that table follow in comments.
    FIELDS = {
        "47 TUC": (6.02, -72.08),  # 47 Tuc Globular Cluster
        "LOW ECLIPTIC LATITUDE": (37.86, 6.98),  # Low Ecliptic Latitude Field
        "FORNAX DSPH": (40.00, -34.45),  # Fornax Dwarf Spheroidal Galaxy
        "ECDFS": (53.13, -28.10),  # Extended Chandra Deep Field South (ECDFS)
        "EDFS": (59.10, -48.73),  # Euclid Deep Field South (EDFS)
        "LOW GALACTIC LATITUDE": (95.00, -25.00),  # Low Galactic Latitude Field
        "SEAGULL": (106.23, -10.51),  # Seagull Nebula
    }
    """The seven DP1 field centers, RA and Dec in degrees."""


class DP2FieldSearch(FieldSearch):
    """Filter a catalog to one of the eighteen Rubin DP2 fields.

    Covers both the small field survey areas and the deep drilling fields.

    Parameters
    ----------
    field : str
        Name of the field, one of the keys of :attr:`FIELDS`. Upper-cased
        before the lookup, so the case does not matter. The error message of an
        unknown name also lists the valid ones.
    radius_arcsec : float (default 6300.0)
        Cone radius in arcseconds, 1.75 degrees by default (half of
        the diameter of the LSSTCam field of view). Please note that
        "small fields" have different shapes, and you may need to adjust this
        value.
    fine : bool (default True)
        True if points are to be filtered, False if only partitions should be
        filtered.

    Examples
    --------
    >>> import lsdb
    >>> from lsdb_rubin import DP2FieldSearch

    The available field names are the keys of :attr:`FIELDS`:

    >>> print(", ".join(DP2FieldSearch.FIELDS))  # doctest: +NORMALIZE_WHITESPACE
    ABELL 2764, DESI SV3 R1, M49, PRAWN, TRIFID-LAGOON, NEW HORIZONS,
    RUBIN SV 212 -7, RUBIN SV 216 -17, RUBIN SV 225 -40, RUBIN SV 280 -48,
    RUBIN SV 300 -41, RUBIN SV 320 -15, DDF ELAIS S1, DDF XMM LSS, DDF ECDFS,
    DDF EDFS A, DDF EDFS B, DDF COSMOS

    >>> search = DP2FieldSearch("DDF COSMOS")
    >>> search.ra, search.dec, search.radius_arcsec
    (150.1, 2.1, 6300.0)

    Pass it to :func:`lsdb.open_catalog` to filter as the catalog is opened, or
    to :meth:`lsdb.catalog.Catalog.search` to filter one you already have:

    >>> catalog = lsdb.open_catalog(DP2_COLLECTION_PATH, search_filter=search)  # doctest: +SKIP
    >>> catalog = lsdb.open_catalog(DP2_COLLECTION_PATH).search(search)  # doctest: +SKIP
    """

    def __init__(self, field: str, *, radius_arcsec: float = 6300.0, fine: bool = True):
        super().__init__(field, radius_arcsec=radius_arcsec, fine=fine)

    # Table 1 (small fields) and Table 2 (deep drilling fields).
    FIELDS = {
        # Small field survey areas
        "ABELL 2764": (5.5, -49.0),
        "DESI SV3 R1": (180.5, -0.3),
        "M49": (186.3, 6.9),
        "PRAWN": (253.5, -41.0),
        "TRIFID-LAGOON": (271.7, -23.9),
        "NEW HORIZONS": (289.4, -20.2),
        "RUBIN SV 212 -7": (211.7, -7.0),
        "RUBIN SV 216 -17": (216.1, -16.7),
        "RUBIN SV 225 -40": (225.0, -39.5),
        "RUBIN SV 280 -48": (280.1, -48.0),
        "RUBIN SV 300 -41": (300.3, -41.0),
        "RUBIN SV 320 -15": (320.2, -15.1),
        # Deep drilling fields
        "DDF ELAIS S1": (9.5, -44.0),
        "DDF XMM LSS": (35.6, -4.8),
        "DDF ECDFS": (53.0, -28.1),
        "DDF EDFS A": (59.2, -49.2),
        "DDF EDFS B": (63.2, -47.8),
        "DDF COSMOS": (150.1, 2.1),
    }
    """The twelve DP2 small field and six deep drilling field centers, in degrees."""
