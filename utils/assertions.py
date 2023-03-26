import jsonschema
from hamcrest import *


def assert_response_status_code(http_code, expected_status_code):
    assert_that(http_code, equal_to(expected_status_code), 
                'Verify the status code should be equal to %s' % expected_status_code)


def assert_response_headers(response_headers):

    content_type = 'application/json'
    assert_that(response_headers['content-type'], equal_to(content_type),
                'Verify content-type in the response headers should be equal to %s' % content_type)

    content_encoding = 'gzip'
    assert_that(response_headers['content-encoding'], equal_to('gzip'),
                'Verify content-encoding in the response headers should be equal to %s' % content_encoding)


def assert_valid_schema(response_json, schema):
    assert_that(jsonschema.validate(response_json, schema), none(), 
                'Verify the json response should follow the schema')


def assert_keys_exist(obj_json, key):
    if key in obj_json:
        pass
    else:
        raise AssertionError


def assert_keys_not_exist(obj_json, key):
    if key not in obj_json:
        pass
    else:
        raise AssertionError


def assert_response_status_code_in(http_code, *status_code):
    assert_that(http_code, any_of(*status_code),
                'Verify the status code should be in to %s' % (str(status_code)))

