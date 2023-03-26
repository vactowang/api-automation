import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - sdk logging')
class TestSDKLoggingBasic(object):

    @allure.feature('sdk logging')
    @allure.tag('basic', 'smoke')
    @allure.story('sdk logging')
    @allure.description('Verify the sdk logging endpoint work fine')
    @allure.severity('smoke')
    def test_sdk_logging_basic(self):
        req = request_payload.sdk_logging()
        r = post(sdk_logging_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))