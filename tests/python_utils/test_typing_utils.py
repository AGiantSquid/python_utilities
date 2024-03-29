#!/usr/bin/env python3.8
'''
Module to verify typing utils work.
'''
from typing import Dict, TypedDict, Union, Optional, List

import pytest

from python_utils.typing_utils import verify_type, is_typed_dict, is_list_with_specified_data_type, is_generic_type


def test_is_typed_dict():
    class TestType(TypedDict):
        field: float

    assert is_typed_dict(TestType) == True

    test_type = TestType(field=2.0)

    assert is_typed_dict(test_type) == False

    assert is_typed_dict(str) == False


def test_is_generic_type():
    test_cases = (
        (str, True),
        (list, True),
        (int, True),
        (dict, True),
        (List[str], False),
        (TypedDict, False),
        (Optional[str], False),
    )

    for tc in test_cases:
        assert is_generic_type(tc[0]) == tc[1]


def test_is_list_with_specified_data_type():
    a = List[str]
    assert is_list_with_specified_data_type(a) == True

    b = list
    assert is_list_with_specified_data_type(b) == False

    c = str
    assert is_list_with_specified_data_type(c) == False


def test_verify_type_basic_types():
    verify_type('hey', str)

    with pytest.raises(TypeError) as e:
        verify_type(1, str)

    assert e.value.args == ("must be str, not int", None)


def test_verify_type_key_error():
    class TestType(TypedDict):
        field: float

    test_type = {
        'wrong_field': 2.0
    }
    with pytest.raises(KeyError) as e:
        verify_type(test_type, TestType, 'body')
    assert str(e.value) == "'field'"


def test_verify_type_type_error():
    class TestType(TypedDict):
        field: float

    test_type = {
        'field': 2
    }
    with pytest.raises(TypeError) as e:
        verify_type(test_type, TestType, 'body')
    assert e.value.args == ('must be float, not int', 'field')


def test_verify_type_nested_error():
    class TestType(TypedDict):
        field: float

    class OtherTestType(TypedDict):
        other_field: TestType

    other_test_type = {
        'other_field': {
            'field': 2
        }
    }

    with pytest.raises(TypeError) as e:
        verify_type(other_test_type, OtherTestType, 'body')
    assert e.value.args == ('must be float, not int', 'field')


def test_verify_inherited_typed_dict_nested_error():
    class TestType(TypedDict):
        field: float

    class OtherTestType(TypedDict):
        other_field: TestType

    class ThirdTestType(OtherTestType):
        '''This inherits from OtherTestType'''

    other_test_type = {
        'other_field': {
            'field': 2
        }
    }

    with pytest.raises(TypeError) as e:
        verify_type(other_test_type, ThirdTestType, 'body')
    assert e.value.args == ('must be float, not int', 'field')


def test_verify_dict_union():
    class TestType(TypedDict):
        field: Union[float, int]

    test_type = {
        'field': 2
    }

    verify_type(test_type, TestType, 'body')


def test_verify_dict_union_error():
    class TestType(TypedDict):
        field: Union[float, int]

    test_type = {
        'field': '2'
    }

    with pytest.raises(TypeError) as e:
        verify_type(test_type, TestType, 'body')
    assert e.value.args == ('must be of the following types: [\'float\', \'int\'], not str', 'field')


def test_verify_dict_optional():
    class TestType(TypedDict):
        field: Optional[float]

    test_type = {
        'field': None
    }

    verify_type(test_type, TestType, 'body')


def test_verify_dict_optional_error():
    class TestType(TypedDict):
        field: Optional[float]

    test_type = {
        'field': '2'
    }

    with pytest.raises(TypeError) as e:
        verify_type(test_type, TestType, 'body')
    assert e.value.args == ('must be of the following types: [\'float\', \'NoneType\'], not str', 'field')


def test_verify_type_nesting():
    class TestType(TypedDict):
        field: float

    class OtherTestType(TypedDict):
        other_field: TestType

    other_test_type = {
        'other_field': {
            'field': 2.0
        }
    }

    verify_type(other_test_type, OtherTestType, 'body')


def test_verify_type_with_list():
    class TestType(TypedDict):
        field: list

    # list of numbers
    test_type = {
        'field': [1,2,3]
    }

    verify_type(test_type, TestType, 'body')

    # list of dict
    test_type = {
        'field': [{
            'key': 2.0
        }]
    }

    verify_type(test_type, TestType, 'body')

    # not list
    test_type = {
        'field': 'string not list'
    }

    with pytest.raises(TypeError) as e:
        verify_type(test_type, TestType, 'body')
    assert e.value.args == ('must be list, not str', 'field')


def test_verify_type_with_list_of_strings():
    class TestType(TypedDict):
        field: List[str]

    # list of strings
    test_type = {
        'field': ['one', 'two', 'three']
    }

    verify_type(test_type, TestType, 'body')

    # list of numbers
    test_type = {
        'field': [1,2,3]
    }

    with pytest.raises(TypeError) as e:
        verify_type(test_type, TestType, 'body')
    assert e.value.args == ('must be str, not int', 'item in field')


def test_verify_type_custom_list():
    class TestType(TypedDict):
        field: float

    class OtherTestType(TypedDict):
        other_field: List[TestType]

    # success case
    other_test_type = {
        'other_field': [{
            'field': 2.0
        }]
    }

    verify_type(other_test_type, OtherTestType, 'body')

    # should error, because 'field' has wrong datatype
    other_test_type = {
        'other_field': [{
            'field': 2
        }]
    }

    with pytest.raises(TypeError) as e:
        verify_type(other_test_type, OtherTestType, 'body')
    assert e.value.args == ('must be float, not int', 'field')


def test_verify_type_optional_nested_error():
    class TestType(TypedDict):
        field: float

    class OtherTestType(TypedDict):
        other_field: Union[TestType, str]

    other_test_type = {
        'other_field': {
            'field': 2
        }
    }

    with pytest.raises(TypeError) as e:
        verify_type(other_test_type, OtherTestType, 'body')
    assert e.value.args == ('must be of the following types: [\'TestType\', \'str\'], not dict', 'other_field')


def test_verify_type_optional_typed_dict():
    class TestType(TypedDict):
        field: float

    class OtherTestType(TypedDict):
        other_field: Union[TestType, str]

    other_test_type = {
        'other_field': 'string'
    }

    verify_type(other_test_type, OtherTestType, 'body')


def test_verify_type_optional_typed_dict_with_typed_dict():
    class TestType(TypedDict):
        field: float

    class OtherTestType(TypedDict):
        other_field: Union[TestType, str]

    other_test_type = {
        'other_field': {
            'field': 2.0
        }
    }
    verify_type(other_test_type, OtherTestType, 'body')


def test_verify_type_optional_typed_dict_with_error():
    class TestType(TypedDict):
        field: float

    class OtherTestType(TypedDict):
        other_field: Union[TestType, str]

    other_test_type = {
        'other_field': 2.3
    }

    with pytest.raises(TypeError) as e:
        verify_type(other_test_type, OtherTestType, 'body')
    assert e.value.args == ('must be of the following types: [\'TestType\', \'str\'], not float', 'other_field')


def test_verify_type_specified_dict():
    DictType = Dict[str, int]

    subject = {
        'str_1': 1
    }
    verify_type(subject, DictType, 'body')


def test_verify_type_specified_dict_error_1():
    DictType = Dict[str, int]

    subject = {
        'str_1': 'oops'
    }

    with pytest.raises(TypeError) as e:
        verify_type(subject, DictType, 'body')
    assert e.value.args == ('must be int, not str', 'oops')


def test_verify_type_specified_dict_error_2():
    DictType = Dict[str, int]

    subject = {
        42: 42
    }

    with pytest.raises(TypeError) as e:
        verify_type(subject, DictType, 'body')
    assert e.value.args == ('must be str, not int', 42)


def test_verify_type_optional_specified_dict():
    class TestType(TypedDict):
        field: Dict[str, dict]

    class OtherTestType(TypedDict):
        other_field: Union[TestType, str]

    other_test_type = {
        'other_field': {
            'field': {
                'dynamic_key': {}
            }
        }
    }
    verify_type(other_test_type, OtherTestType, 'body')


def test_verify_type_optional_specified_dict_with_error():
    class TestType(TypedDict):
        field: Dict[str, dict]

    class OtherTestType(TypedDict):
        other_field: Union[TestType, str]

    other_test_type = {
        'other_field': {
            'field': {
                'dynamic_key': 'wow'
            }
        }
    }
    with pytest.raises(TypeError) as e:
        verify_type(other_test_type, OtherTestType, 'body')
    assert e.value.args == (
        "must be of the following types: ['TestType', 'str'], not dict",
        'other_field',
    )
