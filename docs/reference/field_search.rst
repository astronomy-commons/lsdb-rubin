Field Search
=============================

Rubin observations are grouped into named fields, listed in the
`DP1 <https://dp1.lsst.io/overview/observations.html#field-centers>`_ and
`DP2 <https://dp2.lsst.io/overview/observations.html#small-fields>`_
observation summaries. These searches let you open a catalog restricted to a
single field by name, without looking its coordinates up:

.. code-block:: python

    import lsdb
    from lsdb_rubin import DP1FieldSearch

    catalog = lsdb.open_catalog(dp1_object_path, search_filter=DP1FieldSearch("ECDFS"))

Or use ``search`` to filter a catalog you have already opened:

.. code-block:: python

    catalog = lsdb.open_catalog(dp1_object_path)
    ecdfs = catalog.search(DP1FieldSearch("ECDFS"))

.. warning::

    **This is implemented as a cone search, not as an exact footprint.**
    Rubin publishes a center for each field, but no boundary: fields differ in
    their visit strategy, and the field is rotated between visits. The search
    returns everything within ``radius_arcsec`` of the center, so it may both
    include sky with little coverage and cut off real data.

The default radius is two degrees for DP1, and 1.75 degrees for DP2. Pass
``radius_arcsec`` to tighten or widen it:

.. code-block:: python

    from lsdb_rubin import DP2FieldSearch

    search = DP2FieldSearch("PRAWN", radius_arcsec=3.0 * 3600.0)

Field names are upper-cased before the lookup, so any case works. The
available names are the keys of the ``FIELDS`` attribute of each class:

.. code-block:: python

    >>> from lsdb_rubin import DP1FieldSearch, DP2FieldSearch
    >>> print(", ".join(DP1FieldSearch.FIELDS))
    47 TUC, LOW ECLIPTIC LATITUDE, FORNAX DSPH, ECDFS, EDFS, LOW GALACTIC LATITUDE, SEAGULL
    >>> print(", ".join(DP2FieldSearch.FIELDS))  # doctest: +NORMALIZE_WHITESPACE
    ABELL 2764, DESI SV3 R1, M49, PRAWN, TRIFID-LAGOON, NEW HORIZONS,
    RUBIN SV 212 -7, RUBIN SV 216 -17, RUBIN SV 225 -40, RUBIN SV 280 -48,
    RUBIN SV 300 -41, RUBIN SV 320 -15, DDF ELAIS S1, DDF XMM LSS, DDF ECDFS,
    DDF EDFS A, DDF EDFS B, DDF COSMOS

.. autoclass:: lsdb_rubin.field_search.DP1FieldSearch
    :members: FIELDS

.. autoclass:: lsdb_rubin.field_search.DP2FieldSearch
    :members: FIELDS

.. autoclass:: lsdb_rubin.field_search.FieldSearch
    :members:
    :special-members: __init__
