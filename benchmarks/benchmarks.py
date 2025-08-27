from lsdb_rubin.rsp_tests.critical_functions import critical_functions
from lsdb_rubin.rsp_tests.random_access import random_access


def time_critical_functions():
    """Run the contents of the `Test of LSDB Critical functions` notebook,
    reporting the total runtime. Any deviation from expected values will
    cause the benchmark test to fail.

    See https://github.com/lsst-sitcom/linccf/blob/main/RSP/critical_fs.ipynb"""
    critical_functions()


def time_random_access():
    """Run the contents of the `HATS Data Preview 1 on RSP` notebook,
    reporting the total runtime. Any deviation from expected values will
    cause the benchmark test to fail.

    See https://github.com/lsst-sitcom/linccf/blob/main/RSP/random_access.ipynb"""
    random_access(None)
