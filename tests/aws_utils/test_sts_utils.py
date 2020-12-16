from datetime import datetime, timedelta, date

from aws_utils.sts_utils import (
    get_credentials,
    credentials_generator,
)


def test_credentials_generator():
    called = False

    def mock_get_credentials():
        nonlocal called
        called = True

    cur_time = datetime(2020, 12, 1, 8)
    expires_at = datetime(2020, 12, 1, 8, 2)

    gen = credentials_generator(mock_get_credentials, cur_time, expires_at)

    next(gen)

    assert called is False


def test_credentials_generator_expired():
    called = False

    def mock_get_credentials():
        nonlocal called
        called = True

    cur_time = datetime(2020, 12, 1, 8, 3)
    expires_at = datetime(2020, 12, 1, 8, 2)

    gen = credentials_generator(mock_get_credentials, cur_time, expires_at)

    next(gen)

    assert called


def test_credentials_generator_expired():
    called = 0

    def mock_get_credentials():
        nonlocal called
        called += 1

    cur_time = datetime.now()
    expires_at = cur_time - timedelta(seconds=1)

    gen = credentials_generator(mock_get_credentials, cur_time, expires_at)

    # ask for tokens many times
    next(gen)
    next(gen)
    next(gen)
    next(gen)

    # only call get_new_token_func 1 time
    assert called == 1
