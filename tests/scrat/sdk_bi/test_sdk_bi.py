import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - sdk bi')
class TestSDKBiScrat(object):

    @allure.feature('sdk bi')
    @allure.tag('normal', 'v0.98.0', 'test_mode')
    @allure.story('PBJ-2306 Scrat sdk_bi support')
    @allure.description('Verify the sdk bi normal request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('target', ['campaign', 'creative'])
    def test_sdk_bi_request(self, pub_app_id, target):
        req = request_payload.sdk_bi_ios(pub_app_id, target=target, id='5f08238f4fd1310016fd4d09',
                                         event_id='5ffc151e6f779b000114ad2f')
        r = post(sdk_bi_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk bi')
    @allure.tag('normal', 'v0.98.0', 'test_mode')
    @allure.story('PBJ-2306 Scrat sdk_bi support')
    @allure.description('Verify the sdk bi request with invalid id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('target', ['campaign', 'creative'])
    def test_sdk_bi_request_1(self, pub_app_id, target):
        req = request_payload.sdk_bi_ios(pub_app_id, target=target, id='abcedfg', event_id='5ffc151e6f779b000114ad2f')
        r = post(sdk_bi_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk bi')
    @allure.tag('normal', 'v0.98.0', 'test_mode')
    @allure.story('PBJ-2306 Scrat sdk_bi support')
    @allure.description('Verify the sdk bi request with invalid event id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('target', ['campaign', 'creative'])
    def test_sdk_bi_request_2(self, pub_app_id, target):
        req = request_payload.sdk_bi_ios(pub_app_id, target=target, id='5f08238f4fd1310016fd4d09', event_id='abcdefg')
        r = post(sdk_bi_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk bi')
    @allure.tag('normal', 'v0.98.0', 'test_mode')
    @allure.story('PBJ-2306 Scrat sdk_bi support')
    @allure.description('Verify the sdk bi request with empty cache bust fields')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sdk_bi_request_3(self, pub_app_id):
        req = request_payload.sdk_bi_ios(pub_app_id)
        r = post(sdk_bi_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk bi')
    @allure.tag('normal', 'v0.98.0', 'test_mode')
    @allure.story('PBJ-2306 Scrat sdk_bi support')
    @allure.description('Verify the sdk bi request with empty cache bust obj')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sdk_bi_request_4(self, pub_app_id):
        req = request_payload.sdk_bi_ios(pub_app_id, cache_bust=None)
        r = post(sdk_bi_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))