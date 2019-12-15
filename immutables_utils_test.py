import immutables
import immutables_utils


def test_string_freeze():
    "leave the string as is"
    string = "just livin that string lifeu"
    res = immutables_utils.freeze(string)

    assert isinstance(res, str)


def test_basic_dict_freeze():
    "convert to frozen dict"
    basic_dict = {"key": "value"}
    res = immutables_utils.freeze(basic_dict)

    assert isinstance(res, immutables.Map)


def test_basic_tuple_freeze():
    "leave as tuple"
    basic_tuple = (1,2,3,4)
    res = immutables_utils.freeze(basic_tuple)

    assert isinstance(res, tuple)


def test_basic_list_freeze():
    "convert to list"
    basic_list = [1,2,3,4]
    res = immutables_utils.freeze(basic_list)

    assert isinstance(res, tuple)


def test_basic_set_freeze():
    "convert to list"
    basic_set = {1,2,3,4}
    res = immutables_utils.freeze(basic_set)

    assert isinstance(res, frozenset)


def test_nested_dict_freeze():
    nested_test = {
      "first_key": "string_value",
      "dictionary_property": {
        "some_key": "some_value",
        "another_key": [{"nested_key": "nested_value"}]
      }
    }
    res = immutables_utils.freeze(nested_test)

    assert isinstance(res, immutables.Map)
    assert isinstance(res["dictionary_property"], immutables.Map)
    assert isinstance(res["dictionary_property"]["another_key"], tuple)
    assert isinstance(res["dictionary_property"]["another_key"][0], immutables.Map)



def test_string_unfreeze():
    "leave the string as is"
    string = "just livin that string lifeu"
    res = immutables_utils.unfreeze(string)

    assert isinstance(res, str)


def test_basic_dict_unfreeze():
    "convert to frozen dict"
    basic_dict = immutables.Map({"key": "value"})
    res = immutables_utils.unfreeze(basic_dict)

    assert isinstance(res, dict)



def test_basic_tuple_unfreeze():
    "convent to list"
    basic_tuple = (1,2,3,4)
    res = immutables_utils.unfreeze(basic_tuple)

    assert isinstance(res, list)



def test_basic_list_unfreeze():
    "leave as list"
    basic_list = [1,2,3,4]
    res = immutables_utils.unfreeze(basic_list)
    assert isinstance(res, list)


def test_basic_frozenset_unfreeze():
    "convert to set"
    basic_frozenset = frozenset({1,2,3,4})
    res = immutables_utils.unfreeze(basic_frozenset)

    print(res)
    assert isinstance(res, set)



def test_nested_frozendict_unfreeze():
    nested_test = immutables.Map({
      "first_key": "string_value",
      "dictionary_property": immutables.Map({
        "some_key": "some_value",
        "another_key": tuple([
            immutables.Map({"nested_key": "nested_value"})
        ])
      })
    })
    res = immutables_utils.unfreeze(nested_test)

    assert isinstance(res, dict)
    assert isinstance(res["dictionary_property"], dict)
    assert isinstance(res["dictionary_property"]["another_key"], list)
    assert isinstance(res["dictionary_property"]["another_key"][0], dict)


def test_frozendict_with_tuple_keys():
    nested_test = immutables.Map({
      (0,1): "string_value",
      (0,2): "string_value_2",
    })
    res = immutables_utils.unfreeze(nested_test)
    print(res)

    assert isinstance(res, dict)



def test_frozenset_with_tuple():
    nested_test = frozenset({(0,1), (0,2)})
    res = immutables_utils.unfreeze(nested_test)
    expected_res = {(0,1), (0,2)}
    expected_res = [[0,1], [0,2]]
    assert res == expected_res


if __name__ == "__main__":
    # test_string_freeze()
    # test_basic_dict_freeze()
    # test_basic_tuple_freeze()
    # test_basic_list_freeze()
    # test_basic_set_freeze()
    # test_nested_dict_freeze()
    # test_string_unfreeze()
    # test_basic_dict_unfreeze()
    # test_basic_tuple_unfreeze()
    # test_basic_list_unfreeze()
    # test_basic_frozenset_unfreeze()
    # test_nested_frozendict_unfreeze()
    # test_frozendict_with_tuple_keys()
    test_frozenset_with_tuple()
    pass