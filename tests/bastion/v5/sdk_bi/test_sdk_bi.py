import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestSDKBiBastion(object):

    @allure.feature('sdk bi')
    @allure.tag('smoke', 'v0.98.0', 'test_mode')
    @allure.story('PBJ-2305 Bastion sdk_bi support')
    @allure.description('Verify the sdk bi endpoint')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sdk_bi_support(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload['endpoints'], 'sdk_bi')
        assert_that('/api/v5/sdk_bi' in response_payload['endpoints']['sdk_bi'])