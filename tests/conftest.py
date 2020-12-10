#!/usr/bin/env python3.8
'''
This is a configuration file for pytest that runs before and after the unit tests.
'''
import sys
from pathlib import Path

import pytest

PROJECT_SRC_DIR = Path(__file__).absolute().parents[1]


# def pre_test_setup():
#     '''Add project src dir to path, add src dir as python_utilities module.'''
#     print(PROJECT_SRC_DIR)
#     if str(PROJECT_SRC_DIR) not in sys.path:
#         sys.path.append(str(PROJECT_SRC_DIR))

#     # treat src directory as "python_utilities" module
#     if 'python_utilities' not in sys.modules:
#         import src
#         sys.modules['python_utilities'] = src


# def post_test_cleanup():
#     '''Remove project src dir from path, remove python_utilities module reference.'''
#     while str(PROJECT_SRC_DIR) in sys.path:
#         sys.path.remove(str(PROJECT_SRC_DIR))

#     if 'python_utilities' in sys.modules:
#         del sys.modules['python_utilities']

# pre_test_setup()


# @pytest.fixture(scope="module", autouse=True)
# def wrapper():
#     '''Modify the env to allow tests to run, and cleanup when tests are done.'''
#     pre_test_setup()
#     yield
#     post_test_cleanup()
