
<img src="https://cdn2.webdamdb.com/1280_2yYofV7cPVE1.png?1607019137" height="200"> [![LINCC Frameworks](https://github.com/astronomy-commons/lsdb/blob/main/docs/lincc-logo.png)](https://lsstdiscoveryalliance.org/programs/lincc-frameworks/)

# LSDB Rubin

[![Template](https://img.shields.io/badge/Template-LINCC%20Frameworks%20Python%20Project%20Template-brightgreen)](https://lincc-ppt.readthedocs.io/en/latest/)

[![PyPI](https://img.shields.io/pypi/v/lsdb_rubin?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/lsdb_rubin/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/astronomy-commons/lsdb_rubin/smoke-test.yml)](https://github.com/astronomy-commons/lsdb_rubin/actions/workflows/smoke-test.yml)
[![Codecov](https://codecov.io/gh/astronomy-commons/lsdb_rubin/branch/main/graph/badge.svg)](https://codecov.io/gh/astronomy-commons/lsdb_rubin)
[![Read The Docs](https://img.shields.io/readthedocs/lsdb-rubin)](https://lsdb-rubin.readthedocs.io/)

Suite of utilities for interacting with Rubin LSST data within LSDB.

## Quickstart
To install, clone the repository (ideally, within a virtual environment): 
```python
git clone https://github.com/astronomy-commons/lsdb-rubin.git
cd lsdb-rubin
pip install .
```

### LSST tract/patch search
Use LSDB to search catalogs by LSST tract and/or patch.
```python
import lsdb
import skymap_convert
from lsdb_rubin import tract_patch_search

gaia = lsdb.read_hats("https://data.lsdb.io/hats/gaia_dr3/gaia")
lsst_skymap = skymap_convert.ConvertedSkymapReader(preset="lsst_skymap")

tract_index = 10_000
lsdb.catalog.Catalog.tract_patch_search = tract_patch_search
gaia.tract_patch_search(skymap_reader=lsst_skymap, tract=tract_index)
```
See the [demo notebook](https://github.com/astronomy-commons/lsdb-rubin/blob/main/docs/notebooks/tract_patch_search.ipynb) for more.

### Plot a LSST light curve
LSST light curves can be tricky to plot, so we've provided an easy method for a single light curve.

```python
import lsdb
from lsdb_rubin.plot_light_curve import plot_light_curve

dia_object = lsdb.open_catalog("<your-path-to>/lsdb-rubin/tests/data/mock_dp1_1000")
dia_object = dia_object.compute()

plot_light_curve(dia_object.iloc[0]["diaObjectForcedSource"])
```
See the [demo notebook](https://github.com/astronomy-commons/lsdb-rubin/blob/main/docs/notebooks/plot_light_curves.ipynb) for more.
