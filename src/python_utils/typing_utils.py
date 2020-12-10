#!/usr/bin/env python3.8
'''
Module with functions to help with typing assertions.
'''
from typing import (
    _TypedDictMeta,
    ABCMeta,
    get_args,
    get_origin,
    get_type_hints,
    Optional,
    TypedDict,
    Union,
)

import sys
sys.setrecursionlimit(10**2)

def is_typed_dict(x: ABCMeta):
    '''Return true if x is a class that inherits from TypedDict.'''
    return x.__class__ == _TypedDictMeta


def is_generic_type(x):
    '''Return true if x is a generic type, like str, int, or dict.'''
    # complex types from the typing module do not allow isinstance() to be called on them
    try:
        isinstance('demostring', x)
        return True
    except TypeError as err:
        return False


def is_list_with_specified_data_type(subject):
    '''Return True if x is type List, with a specified data type.

    >>> a = List[str]
    >>> is_list_with_specified_data_type(a)
    True
    '''
    # get_origin is "list" when you specify List[type]
    # get_args returns the type as a tuple (if type specified)
    return get_origin(subject) == list and len(get_args(subject))


def verify_type(subject, expected_type: ABCMeta, label: Optional[str]=None):
    '''Raise error if subject is not of expected type.

    This function overcomes the limitations of builtin isinstance()
    which can only verify basic types. verify_type can verify complex
    types like Lists with type specified, Unions of multiple types,
    and TypedDicts with fields. This function will recurse through
    datastructures to validate the nested data types.

    >>> class TestType(TypedDict):
    ...     field: float

    >>> verify_type(TestType(wrong_field=2.0), TestType)
    Traceback (most recent call last):
    ...
    KeyError: 'field'

    >>> verify_type(TestType(field='invalid'), TestType)
    Traceback (most recent call last):
    ...
    TypeError: "field" must be <class 'float'>, not <class 'str'>
    '''

    if is_generic_type(expected_type):
        if not isinstance(subject, expected_type):
            raise _get_type_error(subject, (expected_type,), label)
        else:
            return

    if is_typed_dict(expected_type):
        return _verify_typed_dict(subject, expected_type, label)


    if is_list_with_specified_data_type(expected_type):
        # List can only receive one type, so get first element from args
        list_element_data_type = get_args(expected_type)[0]
        if not isinstance(subject, list):
            raise _get_type_error(subject, (list,), label)
        else:
            for el in subject:
                verify_type(el, list_element_data_type, f'item in {label}')
        return

    # some vals are allowed to be multiple types, so check multiple
    # for example, a type of Optional[dict] can be a dict or None,
    # which is the Union of 'NoneType' and 'dict'
    if get_origin(expected_type) == Union:
        possible_types = get_args(expected_type)
    else:
        possible_types = (expected_type,)

    check_multiple_types(subject, possible_types, label)


def _get_type_error(subject, possible_types, label):
    '''Helper func for verify_type() to raise proper type error.'''
    if len(possible_types) > 1:
        allowed_types = f'of the following types: {[_.__name__ for _ in possible_types]}'
    else:
        allowed_types = possible_types[0].__name__

    error_msg = f'must be {allowed_types}, not {type(subject).__name__}'.strip()

    return TypeError(error_msg, label)


def _verify_typed_dict(subject, expected_type: ABCMeta, label: Optional[str]=None):
    '''Check that subject has the proper keys/values for a typed_dict.

    Raise KeyError if subject does not have all the specified keys.
    Raise TypeError if subject is not a dict, or if any values are of wrong type.
    '''
    if not isinstance(subject, dict):
        raise _get_type_error(subject, (expected_type,), label)

    typed_dict_fields = get_type_hints(expected_type)

    for key, key_type in typed_dict_fields.items():
        if key not in subject:
            raise KeyError(key)

        val = subject.get(key)

        verify_type(val, key_type, key)


def check_multiple_types(subject, possible_types, label):
    '''Raise exception if subject is none of the possible types.'''
    found_exception = None

    for p_type in possible_types:
        try:
            verify_type(subject, p_type, label)
            return
        except TypeError as err:
            found_exception = err
        except KeyError as err:
            found_exception = err

    if found_exception is not None:
        raise _get_type_error(subject, possible_types, label)
