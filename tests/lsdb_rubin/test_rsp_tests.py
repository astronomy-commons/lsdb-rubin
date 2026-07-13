from pathlib import Path

from lsdb_rubin.rsp_tests.critical_functions import critical_functions
from lsdb_rubin.rsp_tests.random_access import random_access


def test_critical_functions():
    critical_functions()


def test_random_access(test_data_dir):
    random_access(test_data_dir / "mock_dp1_1000")
