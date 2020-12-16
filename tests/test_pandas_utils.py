import pytest

from pandas_utils import validate_required_sheet_fields, InvalidSpreadSheet

def test_validate_required_sheet_fields():
    # does contain required field, no exception raised
    class Sheet:
        def __init__(self, columns):
            self.columns = columns

    mock_sheet = Sheet(columns=['SSO', 'Effective Date', 'Access Granted'])
    validate_required_sheet_fields(mock_sheet, {'SSO', 'Effective Date', 'Access Granted'})

    mock_sheet_bad = Sheet(columns=[])
    # does not contain required field, raises BadRequest
    with pytest.raises(InvalidSpreadSheet) as err:
        validate_required_sheet_fields(mock_sheet_bad, {'SSO', 'Effective Date', 'Access Granted'})

    assert 'Uploaded sheet is missing the following required columns:' in str(err.value)
