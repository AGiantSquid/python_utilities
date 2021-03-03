#!/usr/bin/env python3.8
'''
This module contains functions for working with dicts.
'''
from functools import partial, reduce
from typing import ABCMeta


def dict_with_required_keys(content: dict, required_keys: tuple) -> dict:
    '''Return a new dict that contains the key/values from content that are in required_keys.

    If any required_keys are not in content, raise KeyError.'''
    reducer = partial(_extract_key_val_pair_to_dict, content=content)
    return reduce(reducer, required_keys, {})


def _extract_key_val_pair_to_dict(accum, key, content):
    '''Add key/value pair from content to accum if it exists, else raise KeyError.'''
    val = content.get(key)

    if val is None:
        raise KeyError(key)

    return {
        **accum,
        key: val,
    }


def get_keys_from_typed_dict(typed_dict: ABCMeta) -> tuple:
    '''Return a tuple of all keys in a TypedDict.

    >>> class TestType(TypedDict):
    ...     field: float
    >>> get_keys_from_typed_dict(TestType)
    ('field',)
    '''
    return tuple(typed_dict.__dict__['__annotations__'].keys())


def trim_dict_values(untrimmed: dict) -> dict:
    '''Trim all string values of leading and trailing whitespace.

    >>> d = {'key': '  val  '}
    >>> trim_dict_values(d)
    {'key': 'val'}
    '''
    output = {
        k: _trim_if_string(v)
        for k, v
        in untrimmed.items()
    }

    return output


def _trim_if_string(subject):
    '''If subject is string, trim leading and trailing space.'''
    try:
        return subject.strip()
    except AttributeError:
        return subject


def replace_keys(item, new_key_mapping):
    '''Recursively look through item, and replace any keys found in new_key_mapping.

    >>> item = [{"badKey":"value"}]
    >>> new_key_mapping = {"badKey":"good_key"}]
    >>> replace_keys(item, new_key_mapping)
    [{"good_key": "value"}]
    '''
    if isinstance(item, dict):
        new = {
            new_key_mapping.get(key, key): replace_keys(val, new_key_mapping)
            for key, val in item.items()
        }

        return new

    if isinstance(item, list):
        return [replace_keys(el, new_key_mapping) for el in item]

    return item


def get_key_by_val(subject: dict, target_val):
    '''Get a dictionary key by its value.
    This only works with dictionaries with unique values.

    >>> subject = {"key1":"val1", "key2":"val2"}
    >>> target_val = "val2"
    >>> get_key_by_val(subject, target_val)
    "key2"
    '''
    for key, val in subject.items():
        if val == target_val:
            return key
