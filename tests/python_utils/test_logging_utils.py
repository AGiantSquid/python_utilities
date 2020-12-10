import logging
from importlib import reload

import pytest

from python_utils.logging_utils import initialize_logger, lazy_evaluate_string


@pytest.fixture()
def reset_logger():
    logging.shutdown()
    reload(logging)


def test_initialize_logger_valid_value(capsys, reset_logger):
    '''Override default of "INFO" to use "DEBUG".'''
    initialize_logger('DEBUG')

    captured = capsys.readouterr()

    assert 'Threshold set to "DEBUG"' in captured.err

    assert logging.root.level == logging.DEBUG


def test_initialize_logger_bad_value(capsys, reset_logger):
    '''Try using a bogus value.'''
    initialize_logger('banana')

    captured = capsys.readouterr()

    msg = 'User attempted to set log level to "banana", which is not a valid log level!'
    assert msg in captured.err

    assert logging.root.level == logging.INFO


def test_lazy_evaluate_string(capsys, reset_logger):
    '''Functions wrapped with lazy_evaluate_string should only evaluate when logged.'''
    initialize_logger('INFO')

    # flush captured output
    capsys.readouterr()
    called = False

    @lazy_evaluate_string
    def test_func():
        nonlocal called
        called = True
        return 'result'

    # res is not printed, so test_func is not called
    res = test_func()
    assert called is False

    # logger set to info, so debug not evaluated
    logging.debug('%s', test_func())
    assert called is False

    # verify nothing got printed
    _, stderr = capsys.readouterr()
    assert 'result' not in stderr

    # warning is evaluated, so test_func is called
    logging.warning('%s', test_func())
    assert called is True

    # verify the result from test_func actually gets printed
    _, stderr = capsys.readouterr()
    assert 'result' in stderr
