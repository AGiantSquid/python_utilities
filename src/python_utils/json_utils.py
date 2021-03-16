#! /usr/bin/env python3
'''
Module with helpful code for dealing with json.
'''
import json
from decimal import Decimal
from functools import partial


def decimal_default(obj):
    '''Custom default func for json.dumps that will parse Decimal objects.
    See the following for more detail:
    https://stackoverflow.com/questions/16957275/python-to-json-serialization-fails-on-decimal/16957370#16957370
    '''
    if isinstance(obj, Decimal):
        return float(obj)

    obj_type = type(obj).__name__

    raise TypeError(
        f'Object of type "{obj_type}" is not JSON serializable'
    )
