import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *



@allure.epic('jaeger v5')
class TestSupportHtmlEndcard(object):

    # @allure.feature('html end card')
    # @allure.tag('normal')
    # @allure.story('PBJ-3067 toggle to support playable endcard by HTMLResource')
    # @allure.description('Verify support playable endcard by HTMLResource for test mode via edsp'
    #                     '(this is temporary case just for validate the function)')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_test_mode_support_html_endcard(self, pub_app_id, placement):
    #     """
    #         "allow_html_endcard": true
    #     """
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast, debug='jaeger'))
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     normal_replacements = ad_markup['templateSettings']['normal_replacements']
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_that('EC_HTML' in normal_replacements)
    #     EC_HTML = normal_replacements['EC_HTML']
    #     assert_that(base64.b64decode(EC_HTML), is_not(None))

    # @allure.feature('html end card')
    # @allure.tag('normal')
    # @allure.story('PBJ-3067 toggle to support playable endcard by HTMLResource')
    # @allure.description('Verify support playable endcard by HTMLResource for non test mode'
    #                     '(this is temporary case just for validate the function)')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_non_test_mode_support_html_endcard(self, pub_app_id, placement):
    #     """
    #
    #         "allow_html_endcard": true
    #     """
    #     test_ifa = gen_device_id()
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     normal_replacements = ad_markup['templateSettings']['normal_replacements']
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_that('EC_HTML' in normal_replacements)
    #     EC_HTML = normal_replacements['EC_HTML']
    #     assert_that(base64.b64decode(EC_HTML), is_not(None))

    @allure.feature('html end card')
    @allure.tag('normal')
    @allure.story('PBJ-3067 toggle to support playable endcard by HTMLResource')
    @allure.description('Verify not support playable endcard by HTMLResource for test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_not_support_html_endcard(self, pub_app_id, placement):
        """
            "allow_html_endcard": false
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast_no_html_ec))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('EC_HTML' not in normal_replacements)


    # @allure.feature('html end card')
    # @allure.tag('normal')
    # @allure.story('PBJ-3067 toggle to support playable endcard by HTMLResource')
    # @allure.description('Verify support playable endcard by HTMLResource for test mode via android'
    #                     '(this is temporary case just for validate the function)')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('placement', [android_common_test_placement])
    # def test_test_mode_support_html_endcard_android(self, pub_app_id, placement):
    #     """
    #         "allow_html_endcard": true
    #     """
    #     req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast, debug='jaeger'))
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     normal_replacements = ad_markup['templateSettings']['normal_replacements']
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_that('EC_HTML' in normal_replacements)
    #     EC_HTML = normal_replacements['EC_HTML']
    #     assert_that(base64.b64decode(EC_HTML), is_not(None))
    #
    # @allure.feature('html end card')
    # @allure.tag('normal')
    # @allure.story('PBJ-3067 toggle to support playable endcard by HTMLResource')
    # @allure.description('Verify support playable endcard by HTMLResource for non test mode on android'
    #                     '(this is temporary case just for validate the function)')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('placement', [android_common_test_placement])
    # def test_non_test_mode_support_html_endcard_android(self, pub_app_id, placement):
    #     """
    #
    #         "allow_html_endcard": true
    #     """
    #     test_ifa = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     normal_replacements = ad_markup['templateSettings']['normal_replacements']
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_that('EC_HTML' in normal_replacements)
    #     EC_HTML = normal_replacements['EC_HTML']
    #     assert_that(base64.b64decode(EC_HTML), is_not(None))

    @allure.feature('html end card')
    @allure.tag('normal')
    @allure.story('PBJ-3067 toggle to support playable endcard by HTMLResource')
    @allure.description('Verify not support playable endcard by HTMLResource for test mode on android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_not_support_html_endcard_android(self, pub_app_id, placement):
        """
            "allow_html_endcard": false
        """
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast_no_html_ec))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('EC_HTML' not in normal_replacements)


