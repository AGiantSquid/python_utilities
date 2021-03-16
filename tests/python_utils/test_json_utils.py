'''
Test functions from json_utils module
'''
import json
from decimal import Decimal

import pytest

from python_utils.json_utils import decimal_default


def test_default_raises():
    '''The builtin json decoder should raise an exception for a Decimal.'''
    item = {'x': Decimal('5.5')}

    with pytest.raises(TypeError) as err:
        json.dumps(item)

    assert 'Object of type Decimal is not JSON serializable' in str(err.value)


def test_decimal_default():
    '''Data should serialize without error with decimal_default supplied to json.dumps method.'''
    item = {'x': Decimal('5.5')}

    result = json.dumps(item, default=decimal_default)

    assert result == '{"x": 5.5}'
