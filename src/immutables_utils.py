"""Convert (possibly nested) data structures into immutable data structures.

The "freeze" function recursively turns dictionaries into
immutable Map objects, lists into tuples,
and sets into frozensets.

Can also be used to turn JSON data into a hashable value.

>>> nested_test = {
...   "first_key": "string_value",
...   "dictionary_property": {
...     "some_key": "some_value",
...     "another_key": [{"nested_key": "nested_value"}]
...   }
... }
>>> frozen = freeze(nested_test)
>>> frozen["new_key"] = "new_value"
Traceback (most recent call last):
    ...
TypeError: 'immutables._map.Map' object does not support item assignment
>>> frozen["dictionary_property"]["some_key"] = "updated_value"
Traceback (most recent call last):
    ...
TypeError: 'immutables._map.Map' object does not support item assignment
"""
import logging
import pprint

from immutables import Map


logging.basicConfig(level=logging.DEBUG)

pp = pprint.PrettyPrinter(indent=2, width=80).pprint
logger = logging.getLogger(__name__)


def freeze(obj):
    """Convert data structure into an immutable data structure.

    >>> list_test = [1, 2, 3]
    >>> freeze(list_test)
    (1, 2, 3)
    >>> set_test = {1, 2, 3}
    >>> freeze(set_test)
    frozenset({1, 2, 3})
    """

    try:
        # See if the object is hashable
        hash(obj)
        return obj
    except TypeError:
        pass

    try:
        # Try to see if this is a mapping
        try:
            obj[tuple(obj)]
        except KeyError:
            is_mapping = True
        else:
            is_mapping = False
    except (TypeError, IndexError):
        is_mapping = False

    if is_mapping:
        frz = {key: freeze(value) for key, value in obj.items()}
        return Map(frz)

    # See if the object is a set like
    # or sequence like object
    try:
        obj[0]
        cls = tuple
    except TypeError:
        cls = frozenset
    except IndexError:
        cls = tuple

    try:
        iter(obj)
        is_iterable = True
    except TypeError:
        is_iterable = False

    if is_iterable:
        return cls(freeze(i) for i in obj)

    msg = 'Unsupported type: %r' % type(obj).__name__
    raise TypeError(msg)


def unfreeze(obj):
    """Convert all map objects to dicts.
    NOTE: Cannot reliably turn frozensets into sets,
    as the objects in the set may become unhashable after unfreezing
    All frozen sets are converted to lists.

    >>> map_object = Map({
    ...     "key": Map({"nested_key": "nested_value"})
    ... })
    >>> unfreeze(map_object)
    {'key': {'nested_key': 'nested_value'}}
    """
    def sorted_list(iterable):
        """Use a sorted list instead of a set."""
        return sorted(list(iterable))

    # print('movinwg')
    # print(type(obj).__name__)
    if type(obj).__name__ in ('str', 'int', 'float', 'bool'):
        # print(obj)
        return obj

    # print('sweet')
    try:
        #Try to see if this is a mapping
        try:
            obj[tuple(obj)]
        except KeyError:
            is_mapping = True
            logger.debug('is_mapping')
        else:
            is_mapping = False
    except (TypeError, IndexError):
        is_mapping = False

    if is_mapping:
        for key in obj.keys():
            if type(key).__name__ in ('tuple', 'immutables.Map'):
                logger.info('Input has hashable type "%s" used as a key. This will remain frozen, as dict keys must be hashable.', type(key).__name__)
        return {key: unfreeze(value) for key, value in obj.items()}

    try:
        obj[0]
        cls = list
    except TypeError:
        cls = sorted_list # set (someday figure out how to make a set like object that con convert back to frozenset)
    except IndexError:
        cls = list

    try:
        iter(obj)
        is_iterable = True
    except TypeError:
        is_iterable = False

    if is_iterable:
        try:
            return cls(unfreeze(i) for i in obj)
        except TypeError:
            return list(unfreeze(i) for i in obj)

    return obj


def print_map(map_object):
    '''Pretty print map.

    Pretty printing necessitates unfreezing as PrettyPrint module can't deal with Maps'''
    dict_obj = unfreeze(map_object)
    pp(dict_obj)


if __name__ == "__main__":
    import doctest
    doctest.testmod(raise_on_error=False, verbose=True)
