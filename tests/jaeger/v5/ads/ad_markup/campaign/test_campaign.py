import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestCampaign(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('campaign')
    @allure.description('Verify campaign string from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement_id', [common_test_placement_10])
    def test_campaign(self, pub_app_id, placement_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(ad_markup['campaign'].count('|'), equal_to(3))

    @allure.feature('test mode')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('campaign')
    @allure.description('Verify campaign string from ads response in test mode')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_campaign_in_test_mode(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(ad_markup['campaign'].count('|'), equal_to(3))

    @allure.feature('test mode flag')
    @allure.tag('normal', 'R_1.140.0')
    @allure.story('PBJ-2031 Scrat test mode flag')
    @allure.description('Verify the campaign string has no change in non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement_id', [common_test_placement_10])
    def test_test_mode_flag_non_test_mode(self, pub_app_id, placement_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(ad_markup['campaign'].split('|')[2], not equal_to('test-ads'))

    @allure.feature('test mode flag')
    @allure.tag('normal', 'test_mode', 'R_1.140.0')
    @allure.story('PBJ-2031 Scrat test mode flag')
    @allure.description('Verify the 3rd part of campaign string is test-ads in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_test_mode_flag(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(ad_markup['campaign'].split('|')[2], equal_to('test-ads'))