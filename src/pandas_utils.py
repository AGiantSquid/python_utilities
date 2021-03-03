'''Useful utility functions for dealing with pandas dataframes.'''
import io
import logging
from functools import partial
from typing import Set

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

LOGGER = logging.getLogger(__file__)


class InvalidSpreadSheet(Exception):
    '''Exception to raise if there is something wrong with the spreadsheet file.'''


def csv_to_df(file: bytes, skip_rows, *args, **kwargs):
    kwargs.pop('sheet_name', None)
    try:
        return pd.read_csv(io.BytesIO(file), skiprows=skip_rows, **kwargs)
    except UnicodeDecodeError:
        return pd.read_csv(io.BytesIO(file), skiprows=skip_rows, encoding='windows_1252', **kwargs)



def excel_to_df(file: bytes, skip_rows, sheet_name, *args, **kwargs):
    return pd.read_excel(file, skiprows=skip_rows, sheet_name=sheet_name, **kwargs)


# map parsing functions to their compatible file types
FUNCTION_FILE_TYPE_MAPPING = {
    csv_to_df: [
        'text/csv',
    ],
    excel_to_df: [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ],
}

# map filetypes to their corresponding parsing functions
FILE_TYPE_FUNCTION_MAPPING = {
  ft: parsing_func
  for parsing_func, file_types in FUNCTION_FILE_TYPE_MAPPING.items()
  for ft in file_types
}


def convert_file_into_df(file: bytes, file_type, skip_rows=None, sheet_name=0, **kwargs):
    '''Return dataframe from file or raise InvalidSpreadSheet.

    Returns first 'sheet' found in excel files, unless a sheet name is given.
    Raise InvalidSpreadsheet on error.'''

    try:
        parsing_func = FILE_TYPE_FUNCTION_MAPPING[file_type]
    except KeyError:
        raise InvalidSpreadSheet(f'{file_type} format currently not support')

    return parsing_func(file, skip_rows, sheet_name, **kwargs)


def coerce_nan_to_none(df: DataFrame) -> DataFrame:
    return df.replace({np.nan: None})


def validate_required_sheet_fields(
        df: DataFrame,
        required_columns: Set[str]):
    '''Raise InvalidSpreadSheet if columns are missing.'''
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise InvalidSpreadSheet(f'Uploaded sheet is missing the following required columns: {missing_columns}')


def convert_date_col_to_str(df: DataFrame, column_name: str) -> DataFrame:
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    df[column_name] = df[column_name].astype(str)
    return df


def df_to_dict(df: DataFrame) -> dict:
    return df.to_dict('records')


def transform_db_response_cell(cell):
    if cell.get('isNull'):
        return 'empty'

    clean = list(cell.values())[0]
    return clean


def db_response_to_df(df):
    return df.apply(transform_db_response_cell)
