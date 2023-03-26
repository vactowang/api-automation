import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - load ad')
class TestScratLoadAd(object):

    @allure.feature('sdk load ad')
    @allure.tag('smoke', 'v0.124.0')
    @allure.story('PBJ-3044 Implement DDL strategy for real-time bidding')
    @allure.description('Verify the hbp load ad endpoint work fine with no param')
    @allure.severity('smoke')
    def test_scrat_load_ad_basic_1(self):
        req = request_payload.hbp_load_ad()
        r = get(scrat_sdk_notification_endpoint_qa, params=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('Request invalid: cannot get extInfo param.'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk load ad')
    @allure.tag('smoke', 'v0.124.0')
    @allure.story('PBJ-3044 Implement DDL strategy for real-time bidding')
    @allure.description('Verify the hbp impression endpoint work fine with empty ext param')
    @allure.severity('smoke')
    def test_scrat_load_ad_basic_2(self):
        req = request_payload.hbp_load_ad(ext='')
        r = get(scrat_sdk_notification_endpoint_qa, params=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('Request invalid: cannot get extInfo param.'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk load ad')
    @allure.tag('smoke', 'v0.124.0')
    @allure.story('PBJ-3044 Implement DDL strategy for real-time bidding')
    @allure.description('Verify the hbp impression endpoint work fine with invalid ext param')
    @allure.severity('smoke')
    def test_scrat_load_ad_basic_3(self):
        req = request_payload.hbp_load_ad(ext='123456')
        r = get(scrat_sdk_notification_endpoint_qa, params=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('Request invalid: decode notification info failed' in response_payload['msg'])
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk load ad')
    @allure.tag('smoke', 'v0.124.0')
    @allure.story('PBJ-3044 Implement DDL strategy for real-time bidding')
    @allure.description('Verify the hbp impression endpoint work fine with ext param')
    @allure.severity('smoke')
    def test_scrat_load_ad_basic_4(self):
        req = request_payload.hbp_load_ad(ext=test_sdk_notification_ext_param)
        r = get(scrat_sdk_notification_endpoint_qa, params=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))



    # @allure.feature('RTA')
    # @allure.tag('normal')
    # @allure.story('PBJ-4877 RTA - Support getting time difference from loadAd to playAd')
    # @allure.description('Verify scrat will log the message to kafka topic "as-tpat"')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    # def test_scrat_invoke_tracking_url_for_precache(self, pub_app_id, placement, rtb_ids):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36), header_bidding=True)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=us_ip,
    #                                       rtb_selector=rtb_ids))
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     notification = ad_markup['notification']
    #     tracking_url = notification[0]
    #     assert_that("load_ad" in tracking_url)
    #     r = get(tracking_url.replace("https://events.api.vungle.com", scrat_notification_host),
    #             headers=platform_headers(debug='scrat'))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_that(response_payload['msg'], equal_to('ok'))
    #     assert_that(response_payload['code'], equal_to(200))