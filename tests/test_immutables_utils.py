#!/usr/bin/env python3
from immutables import Map
import pytest

from immutables_utils import unfreeze, freeze


def test_string_freeze():
    '''leave the string as is'''
    string = 'just livin that string lifeu'
    res = freeze(string)

    assert isinstance(res, str)


def test_basic_dict_freeze():
    '''convert to frozen dict'''
    basic_dict = {'key': 'value'}
    res = freeze(basic_dict)

    assert isinstance(res, Map)


def test_basic_tuple_freeze():
    '''leave as tuple'''
    basic_tuple = (1, 2, 3, 4)
    res = freeze(basic_tuple)

    assert isinstance(res, tuple)


def test_basic_list_freeze():
    '''convert to list'''
    basic_list = [1, 2, 3, 4]
    res = freeze(basic_list)

    assert isinstance(res, tuple)


def test_basic_set_freeze():
    '''convert to list'''
    basic_set = {1, 2, 3, 4}
    res = freeze(basic_set)

    assert isinstance(res, frozenset)


def test_nested_dict_freeze():
    nested_test = {
      'first_key': 'string_value',
      'dictionary_property': {
        'some_key': 'some_value',
        'another_key': [{'nested_key': 'nested_value'}]
      }
    }
    res = freeze(nested_test)

    assert isinstance(res, Map)
    assert isinstance(res['dictionary_property'], Map)
    assert isinstance(res['dictionary_property']['another_key'], tuple)
    assert isinstance(res['dictionary_property']['another_key'][0], Map)


def test_string_unfreeze():
    '''leave the string as is'''
    string = 'just livin that string lifeu'
    res = unfreeze(string)

    assert isinstance(res, str)


def test_basic_dict_unfreeze():
    '''convert to frozen dict'''
    basic_dict = Map({'key': 'value'})
    res = unfreeze(basic_dict)

    assert isinstance(res, dict)


def test_basic_tuple_unfreeze():
    '''convent to list'''
    basic_tuple = (1, 2, 3, 4)
    res = unfreeze(basic_tuple)

    assert isinstance(res, list)


def test_basic_list_unfreeze():
    '''leave as list'''
    basic_list = [1, 2, 3, 4]
    res = unfreeze(basic_list)
    assert isinstance(res, list)


def test_basic_frozenset_unfreeze():
    '''convert to list'''
    basic_frozenset = frozenset({1, 2, 3, 4})
    res = unfreeze(basic_frozenset)

    assert isinstance(res, list)


def test_nested_frozendict_unfreeze():
    nested_test = Map({
      'first_key': 'string_value',
      'dictionary_property': Map({
        'some_key': 'some_value',
        'another_key': tuple([
            Map({'nested_key': 'nested_value'})
        ])
      })
    })
    res = unfreeze(nested_test)

    assert isinstance(res, dict)
    assert isinstance(res['dictionary_property'], dict)
    assert isinstance(res['dictionary_property']['another_key'], list)
    assert isinstance(res['dictionary_property']['another_key'][0], dict)


def test_frozendict_with_tuple_keys():
    nested_test = Map({
      (0, 1): 'string_value',
      (0, 2): 'string_value_2',
    })
    res = unfreeze(nested_test)
    print(res)

    assert isinstance(res, dict)


def test_frozenset_with_tuple():
    nested_test = frozenset({(0, 1), (0, 2)})
    res = unfreeze(nested_test)
    expected_res = {(0, 1), (0, 2)}
    expected_res = [[0, 1], [0, 2]]
    assert res == expected_res


def test_unfreeze():
    map_object = Map({
        'hey': 'there',
        'wow': ('this', 'is', 'a', 'tuple key')
    })
    result = unfreeze(map_object)
    expected_result = {
        'hey': 'there',
        'wow': ['this', 'is', 'a', 'tuple key']
    }
    assert result == expected_result


def test_unfreeze_2():
    '''Frozensets can't properly be converted if they contain items that will be unhashable.'''
    map_object = frozenset({
        Map({
            'testing_facility': (
                frozenset({('lithium', 'm')}),
                frozenset({('hydrogen', 'm'), ('hydrogen', 'g')}),
                frozenset({('lithium', 'g')}),
                frozenset()
            ),
            'elevator': 1
        })
    })

    result = unfreeze(map_object)
    print(result)
    expected_result = [
        {
            'testing_facility': [
                [['lithium', 'm']],
                [['hydrogen', 'g'], ['hydrogen', 'm']],
                [['lithium', 'g']],
                [],
            ],
            'elevator': 1,
        },
    ]
    assert result == expected_result


if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
