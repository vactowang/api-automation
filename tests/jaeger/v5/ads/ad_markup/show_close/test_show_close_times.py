import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestShowCloseTimes(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('show close times')
    @allure.description('Verify the show close times from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_show_close_times(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.ads_v5)

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for show close time will not be replaced for MRAID - '
                        'app forceView is false, app is skippable, interstitial placement is not skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_is_skippable_placement_override_app_inter_placement_not_skippable(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50909', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        src_ip=gb_ip,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['templateSettings']['normal_replacements']['CLOSE_BUTTON_DELAY_SECONDS'],
                    is_not(int(ad_markup['showClose'])))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for show close time will not be replaced for MRAID - '
                        'app forceViewIncentivized is false, app is skippable, rewarded placement is not skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_is_skippable_placement_override_app_rewarded_placement_not_skippable(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509080', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        src_ip=gb_ip,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['templateSettings']['normal_replacements']['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'],
                    is_not(int(ad_markup['showCloseIncentivized'])))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for show close time will not be replaced for MRAID - '
                        'app forceViewIncentivized is true not skippable, rewarded placement is skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_is_skippable_placement_override_app_rewarded_placement_skippable(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50919', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        src_ip=gb_ip,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['templateSettings']['normal_replacements']['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'],
                    is_not(int(ad_markup['showCloseIncentivized'])))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for show close time will not be replaced for MRAID - '
                        'app forceView is true not skippable, interstitial placement is skippable')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_is_skippable_placement_override_app_inter_placement_skippable(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509190', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        src_ip=gb_ip,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['templateSettings']['normal_replacements']['CLOSE_BUTTON_DELAY_SECONDS'],
                    is_not(int(ad_markup['showClose'])))

    @allure.feature('close button delay')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-1751 New requirement for close button delay')
    @allure.description('Test for is skippable - skip after time is null and placement is_skippable is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_is_skippable_skip_after_time_is_null(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, '0H90YVC08232', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        src_ip=gb_ip,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['showClose'], equal_to(2))
        assert_that(ad_markup['showCloseIncentivized'], equal_to(2))

    @allure.feature('close button delay')
    @allure.tag('normal')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for show close time will not be replaced for MRAID - '
                        'app forceView is false, app is skippable, interstitial placement is not skippable for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_is_skippable_placement_override_app_inter_placement_not_skippable_e(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50909', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        src_ip=gb_ip,
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['templateSettings']['normal_replacements']['CLOSE_BUTTON_DELAY_SECONDS'],
                    is_not(int(ad_markup['showClose'])))

    @allure.feature('close button delay')
    @allure.tag('normal')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for show close time will not be replaced for MRAID - '
                        'app forceViewIncentivized is false, app is skippable, rewarded placement is not skippable'
                        'for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_is_skippable_placement_override_app_rewarded_placement_not_skippable_e(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509080', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        src_ip=gb_ip,
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['templateSettings']['normal_replacements']['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'],
                    is_not(int(ad_markup['showCloseIncentivized'])))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for show close time will not be replaced for MRAID - '
                        'app forceViewIncentivized is true not skippable, rewarded placement is skippable'
                        'for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_is_skippable_placement_override_app_rewarded_placement_skippable_e(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50919', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        src_ip=au_ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['templateSettings']['normal_replacements']['INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS'],
                    is_not(int(ad_markup['showCloseIncentivized'])))

    @allure.feature('close button delay')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-3814 Add publisher settings(app level & placement level) to programmatic responses')
    @allure.description('Test for show close time will not be replaced for MRAID - '
                        'app forceView is true not skippable, interstitial placement is skippable for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_is_skippable_placement_override_app_inter_placement_skippable_e(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM509190', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.5.3', debug='jaeger',
                                                                        src_ip=au_ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['templateSettings']['normal_replacements']['CLOSE_BUTTON_DELAY_SECONDS'],
                    is_not(int(ad_markup['showClose'])))





