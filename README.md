
<img src="https://cdn2.webdamdb.com/1280_2yYofV7cPVE1.png?1607019137" height="200"> [![LINCC Frameworks](https://github.com/astronomy-commons/lsdb/blob/main/docs/lincc-logo.png)](https://lsstdiscoveryalliance.org/programs/lincc-frameworks/)

# LSDB Rubin

[![Template](https://img.shields.io/badge/Template-LINCC%20Frameworks%20Python%20Project%20Template-brightgreen)](https://lincc-ppt.readthedocs.io/en/latest/)

[![PyPI](https://img.shields.io/pypi/v/lsdb_rubin?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/lsdb_rubin/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/astronomy-commons/lsdb_rubin/smoke-test.yml)](https://github.com/astronomy-commons/lsdb_rubin/actions/workflows/smoke-test.yml)
[![Codecov](https://codecov.io/gh/astronomy-commons/lsdb_rubin/branch/main/graph/badge.svg)](https://codecov.io/gh/astronomy-commons/lsdb_rubin)
[![Read The Docs](https://img.shields.io/readthedocs/lsdb-rubin)](https://lsdb-rubin.readthedocs.io/)

Suite of utilities for interacting with Rubin LSST data within LSDB.

## Dev Guide - Getting Started

Before installing any dependencies or writing code, it's a great idea to create a
virtual environment. LINCC-Frameworks engineers primarily use `conda` to manage virtual
environments. If you have conda installed locally, you can run the following to
create and activate a new environment.

```
>> conda create -n <env_name> python=3.11
>> conda activate <env_name>
```

Once you have created a new environment, you can install this project for local
development using the following commands:

```
>> ./.setup_dev.sh
>> conda install pandoc
```

Notes:
1. `./.setup_dev.sh` will initialize pre-commit for this local repository, so
   that a set of tests will be run prior to completing a local commit. For more
   information, see the Python Project Template documentation on 
   [pre-commit](https://lincc-ppt.readthedocs.io/en/latest/practices/precommit.html)
