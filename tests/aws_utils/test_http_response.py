'''
Test that the http response tools work.
'''
import json

from aws_utils.http_response import handle_exceptions

def test_handle_exceptions():
    @handle_exceptions
    def bad_func():
        return 1/0

    res = bad_func()
    body = json.loads(res.get('body'))
    assert body['code'] == 500
    assert body['message'] == 'unhandled internal error'
