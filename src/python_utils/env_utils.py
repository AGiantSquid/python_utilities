#! /usr/bin/env python3.8

'''
Module for fetching environment variables.
'''
import os
from typing import Optional, Sequence


def getenv_str(variable: str, default: Optional[str] = None) -> str:
    '''Gets string variables from the environment.

    If "default" is set, this function verifies that default is of type string.
    If "default" is not set, throw exception if specified env var not found.
    Returns found value stripping out quotes and spaces.'''

    if default is not None:
        _verify_default_value_type(default, str)

    result = clean_string(os.environ.get(variable))

    if result is None and default is not None:
        return default

    if result is None:
        raise EnvironmentError(
            f'You must set a vaild "{variable}" in the environment.')

    return result


def getenv_int(variable: str, default: Optional[int]) -> int:
    '''Gets integer variables from the environment.

    If "default" is set, this function verifies that default is of type int.
    If "default" is not set, throw exception if specified env var not found.
    Returns found value stripping out quotes and spaces.'''

    if default is not None:
        _verify_default_value_type(default, int)

    str_value = clean_string(os.environ.get(variable))

    if str_value is None and default is not None:
        return default

    if str_value is None:
        raise EnvironmentError(
            f'You must set a vaild "{variable}" in the environment.')

    try:
        result = int(str_value)
    except ValueError:
        raise EnvironmentError(
            f'Invaild value found for evironment variable "{variable}". Expected integer, found: "{str_value}"."')

    return result


def getenv_bool(variable: str, default: Optional[bool]) -> bool:
    '''Gets boolean variables from the environment.

    If "default" is set, this function verifies that default is of type bool.
    If "default" is not set, throw exception if specified env var not found.
    Returns found value coerced to a boolean.'''

    if default is not None:
        _verify_default_value_type(default, bool)

    str_value = clean_string(os.environ.get(variable))

    if str_value is None and default is not None:
        return default

    if str_value is None:
        raise EnvironmentError(
            f'You must set a vaild "{variable}" in the environment.')

    if str_value.lower() in ('1', 'true', 'yes', 'y'):
        return True

    if str_value.lower() in ('0', 'false', 'no', 'n'):
        return False

    raise EnvironmentError(
        f'Invaild value found for evironment variable "{variable}". Expected boolean, found: "{str_value}"."')


def clean_string(value: Optional[str]) -> Optional[str]:
    '''Cleans a string of quote and space characters.
    >>> clean_string("'True'")
    'True'
    >>> clean_string('  "false"  ')
    'false'
    >>> clean_string("Bob's House")
    "Bob's House"
    '''
    return value.strip().strip('"').strip("'") if value else value


def _verify_default_value_type(default, expected_type):
    '''Raise TypeError if user attempts to use a default value that is the wrong type.

    >>> _verify_default_value_type('hey', str)

    >>> _verify_default_value_type(2, str)
    Traceback (most recent call last):
    ...
    TypeError: Default value must be a str! Received value "2" of type: int
    '''
    if not isinstance(default, expected_type):

        # Handle tuples of possible valid types elegantly if at all possible
        expected_type = expected_type[0] if isinstance(expected_type, Sequence) else expected_type

        raise TypeError(
            f'Default value must be a {expected_type.__name__}! ' +
            f'Received value "{default}" of type: {type(default).__name__}'
        )
