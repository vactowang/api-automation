import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - sdk bi')
class TestSDKBiBasic(object):

    @allure.feature('sdk bi')
    @allure.tag('basic', 'smoke')
    @allure.story('sdk bi')
    @allure.description('Verify the sdk bi endpoint work fine')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sdk_bi_basic(self, pub_app_id):
        req = request_payload.sdk_bi_ios(pub_app_id, target='campaign', id='5f08238f4fd1310016fd4d09',
                                         event_id='5ffc151e6f779b000114ad2f')
        r = post(sdk_bi_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))