import pytest
from lsdb.core.search.region_search import ConeSearch

from lsdb_rubin import DP1FieldSearch, DP2FieldSearch

DEFAULT_RADIUS_ARCSEC = {DP1FieldSearch: 7200.0, DP2FieldSearch: 6300.0}

ALL_SEARCHES = [
    pytest.param(search_class, name, id=f"{search_class.__name__}-{name}")
    for search_class in (DP1FieldSearch, DP2FieldSearch)
    for name in search_class.FIELDS
]


@pytest.mark.parametrize("search_class,field", ALL_SEARCHES)
def test_every_field_is_a_valid_cone(search_class, field):
    """Every hard-coded field center makes a valid cone search with the default radius."""
    search = search_class(field)

    assert isinstance(search, ConeSearch)
    assert search.field == field
    assert 0.0 <= search.ra < 360.0
    assert -90.0 <= search.dec <= 90.0
    assert search.radius_arcsec == DEFAULT_RADIUS_ARCSEC[search_class]
    assert search.fine


def test_field_counts():
    """DP1 has seven fields, DP2 has twelve small fields and six deep drilling fields."""
    assert len(DP1FieldSearch.FIELDS) == 7
    assert len(DP2FieldSearch.FIELDS) == 18


def test_unknown_field_raises():
    """An unknown field name raises, and the message lists the known fields."""
    with pytest.raises(ValueError, match="Unknown field 'ECDF', must be one of: .*ECDFS"):
        DP1FieldSearch("ECDF")

    # DP1 fields are not DP2 fields, even though some of them overlap on the sky.
    with pytest.raises(ValueError, match="47 TUC"):
        DP2FieldSearch("47 Tuc")
