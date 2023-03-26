import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.protobuf_common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - sdk error logging')
class TestSDKErrorLoggingBasic(object):

    @allure.feature('sdk error logging')
    @allure.tag('basic', 'smoke')
    @allure.story('sdk error logging')
    @allure.description('Verify the sdk error logging endpoint work fine')
    @allure.severity('smoke')
    def test_sdk_error_logging_basic(self):
        req = request_payload.sdk_error_logging()
        pb_message = generate_pb2_message(json_message=json.dumps(req))
        pb_serialized = pb_serialize_to_string(pb_message)
        r = post_gzip(sdk_error_logging_endpoint_qa, data=pb_serialized, headers=platform_headers(app_id=common_test_app))
        response_payload = r[0].json()
        assert_response_status_code(r[0].status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk error logging')
    @allure.tag('basic', 'smoke')
    @allure.story('sdk error logging')
    @allure.description('Verify the sdk error logging endpoint work fine')
    @allure.severity('smoke')
    def test_sdk_error_logging_basic_android(self):
        req = request_payload.sdk_error_logging()
        pb_message = generate_pb2_message(json_message=json.dumps(req))
        pb_serialized = pb_serialize_to_string(pb_message)
        r = post_gzip(sdk_error_logging_endpoint_qa, data=pb_serialized, headers=platform_headers(app_id=android_common_test_app))
        response_payload = r[0].json()
        assert_response_status_code(r[0].status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))