import logging
from importlib import reload

import pytest

from python_utilities.logging_config import initialize_logger


@pytest.fixture()
def reset_logger():
    logging.shutdown()
    reload(logging)


def test_initialize_logger_valid_value(capsys, reset_logger):
    '''Override default of "INFO" to use "DEBUG".'''
    initialize_logger('DEBUG')

    _, stderr = capsys.readouterr()

    assert 'Threshold set to "DEBUG"' in stderr

    assert logging.root.level == logging.DEBUG


def test_initialize_logger_bad_value(capsys, reset_logger):
    '''Try using a bogus value.'''
    initialize_logger('banana')

    _, stderr = capsys.readouterr()

    msg = 'User attempted to set log level to "banana", which is not a valid log level!'
    assert msg in stderr

    assert logging.root.level == logging.INFO
