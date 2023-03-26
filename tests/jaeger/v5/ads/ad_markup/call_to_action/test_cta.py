import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestCTA(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('call to action')
    @allure.description('Verify CTA URLs from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_cta_url(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(str(ad_markup['callToActionDest']).count('http'), equal_to(1))
        assert_that(str(ad_markup['callToActionUrl']).count('http'), equal_to(1))

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('call to action')
    @allure.description('Verify CTA overlay keys from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_cta_overlay(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'cta_overlay' in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(str(ad_markup['cta_overlay']).count('enabled'), equal_to(2))
            assert_that(str(ad_markup['cta_overlay']).count('show_onclick'), equal_to(1))
            assert_that(str(ad_markup['cta_overlay']).count('time_enabled'), equal_to(1))
            assert_that(str(ad_markup['cta_overlay']).count('time_show'), equal_to(1))
            assert_that(str(ad_markup['cta_overlay']).count('click_area'), equal_to(1))