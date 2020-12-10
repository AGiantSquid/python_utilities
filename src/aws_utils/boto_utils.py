#!/usr/bin/env python3.8
'''
Utils to help writing and reading from the db.
'''
import logging
from typing import Dict, List, TypedDict

from python_utils.logging_utils import lazy_evaluate_string

logger = logging.getLogger(__file__)


PYTHON_BOTO_DATA_MAPPING = {
    int: 'longValue',
    str: 'stringValue',
    bool: 'booleanValue',
    float: 'doubleValue',
}


class BotoParameter(TypedDict):
    '''Dict for parameter used by boto in sql statement execution.'''
    name: str
    value: Dict


BotoParameterSet = List[BotoParameter]


def convert_to_parameter_sets(unformatted_parameters: List[dict]) -> List[BotoParameterSet]:
    '''Convert a list of dicts of sql parameters into the format used by boto3'''
    return [convert_to_parameter_set(_) for _ in unformatted_parameters]


def convert_to_parameter_set(unformatted_parameters: dict) -> BotoParameterSet:
    '''Convert a dict of sql parameters into the format used by boto3

    >>> unformatted_params = {'number': 2}
    >>> convert_to_parameter_set(unformatted_params)
    [{'name': 'number', 'value': {'longValue': 2}}]
    '''

    return [
        convert_to_parameter(key, val) for key, val in unformatted_parameters.items()
    ]


def convert_to_parameter(key: str, val) -> BotoParameter:
    '''Convert python data type to boto sql parameter.'''
    if val is None:
        value = {'isNull': True}
    else:
        value = {PYTHON_BOTO_DATA_MAPPING[type(val)]: val}

    return {
        'name': key,
        'value': value,
    }


@lazy_evaluate_string
def lazy_log_sql_statements(sql: str, parameterSets: List[BotoParameterSet]) -> str:
    '''Interpolate and concatenate parameters into sql in a lazy fashion.

    This function will not actually do anything until it is printed.'''
    sql_stmnts = interpolate_batch_sql(sql, parameterSets)
    return '\n'.join(sql_stmnts)


def interpolate_batch_sql(sql: str, parameterSets: List[BotoParameterSet]) -> List[str]:
    '''Output sql statements for batch_execute_statement function.'''
    return [interpolate_sql_statement(sql, _) for _ in parameterSets]


def interpolate_sql_statement(sql, params: BotoParameterSet) -> str:
    '''Return sql statement with params interpolated.

    >>> sql = "SELECT * FROM table_name WHERE f_name = :f_name and dept = :dept ;"
    >>> params = [
    ...     {'name': 'f_name', 'value': {'stringValue': 'Bob'}},
    ...     {'name': 'dept', 'value': {'longValue': 123}}
    ... ]
    >>> interpolate_sql_statement(sql, params)
    "SELECT * FROM table_name WHERE f_name = 'Bob' and dept = 123 ;"
    '''
    new_sql = sql
    for param in params:
        new_sql = new_sql.replace(
            f":{param['name']}",
            convert_param_to_string(param['value'])
        )
    return new_sql


def convert_param_to_string(param_val) -> str:
    '''Convert boto query parameter to a string for interpolation.

    >>> param_val = {'longValue': 2}
    >>> convert_param_to_string(param_val)
    '2'
    >>> param_val ={'stringValue': 'Bob'}
    >>> convert_param_to_string(param_val)
    "'Bob'"
    '''
    data_type, value = list(param_val.items())[0]

    if data_type == 'stringValue':
        return f"'{value}'"

    return str(value)
