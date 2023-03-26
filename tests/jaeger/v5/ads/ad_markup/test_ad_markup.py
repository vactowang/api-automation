import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_hbp_with_real_time_token, decode_real_time_adunit, \
    get_bid_request_obj_from_jaeger_explain, get_bid_response_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema
from datetime import datetime


@allure.epic('jaeger v5')
class TestAdMarkup(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('ad markup')
    @allure.description('Verify ad markup expiry from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_markup_expiry(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that('expiry' in ad_markup)

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('ad markup')
    @allure.description('Verify ad markup ad_market_id from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_markup_ad_market_id(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that('ad_market_id' in ad_markup)

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('ad markup')
    @allure.description('Verify ad markup retryCount from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_markup_retry_count(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that('retryCount' in ad_markup)

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('ad markup')
    @allure.description('Verify ad markup asyncThreshold from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_markup_async_threshold(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that('asyncThreshold' in ad_markup)

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('ad markup')
    @allure.description('Verify ad markup video_object_id from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_markup_video_object_id(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that('video_object_id' in ad_markup)

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('ad markup')
    @allure.description('Verify ad markup requires_sideloading from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_markup_requires_sideloading(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that('requires_sideloading' in ad_markup)

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('ad markup')
    @allure.description('Verify ad markup data science cache from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_markup_data_science_cache(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that('data_science_cache' in ad_markup)

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode')
    @allure.story('rtb connection selector')
    @allure.description('Test for selecting non test mode rtbConnection in case of test mode turned on')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_select_non_test_mode_rtb(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(21603))
        assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('no eligible RTB connections'))

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode')
    @allure.story('rtb connection selector')
    @allure.description('Test for selecting test mode rtbConnection in case of test mode turned off')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_select_test_mode_rtb_test_mode_off(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(21603))
        assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('no eligible RTB connections'))

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode', 'manual')
    @allure.story('GDPR')
    @allure.description('Verify test mode not works in case of GDPR opted_out')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_gdpr_opted_out_test_mode_not_works(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', gdpr='opted_out', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(21603))
        assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('no eligible RTB connections'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'R_1.124.0')
    @allure.story('PBJ-1453 Programmatic MREC support')
    @allure.description('Verify for the programmatic mrec support on non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_programmatic_mrec_support_non_test_mode(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_programmatic_mrec_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip, sdk_version='Vungle/6.5.3',
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['adType'], equal_to('vungle_mraid'))
        assert_that(ad_markup['template_type'], equal_to('mrec'))
        assert_that(ad_markup['templateId'], equal_to('5e93dfc72e4ace6b7a77f7a5'))
        assert_that('/template-rtb/programmaticBanner' in ad_markup['templateURL'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.124.0')
    @allure.story('PBJ-1453 Programmatic MREC support')
    @allure.description('Verify for the programmatic mrec support on test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_programmatic_mrec_support_test_mode(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_programmatic_mrec_placement,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger',
                                          src_ip=fr_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['adType'], equal_to('vungle_mraid'))
        assert_that(ad_markup['template_type'], equal_to('mrec'))
        assert_that(ad_markup['templateId'], equal_to('5e93dfc72e4ace6b7a77f7a5'))
        assert_that('/template-rtb/programmaticBanner' in ad_markup['templateURL'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'R_1.124.0')
    @allure.story('PBJ-1465 Jaeger only serve programmatic MREC for SDK 6.5.2 and higher')
    @allure.description('Verify that programmatic MERC will be served for SDK >= 6.5.2')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.5.2', 'Vungle/6.5.3'])
    def test_programmatic_mrec_sdk_filter_0(self, pub_app_id, sdk_ver):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_programmatic_mrec_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip, sdk_version=sdk_ver,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['adType'], equal_to('vungle_mraid'))
        assert_that(ad_markup['template_type'], equal_to('mrec'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'R_1.124.0')
    @allure.story('PBJ-1465 Jaeger only serve programmatic MREC for SDK 6.5.2 and higher')
    @allure.description('Verify that programmatic MERC will not be served for SDK < 6.5.2')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.5.1', 'Vungle/6.3.2', 'Vungle/5.1.2', 'Vungle/5.0.0'])
    def test_programmatic_mrec_sdk_filter_1(self, pub_app_id, sdk_ver):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_programmatic_mrec_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip, sdk_version=sdk_ver,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(21603))
        assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('no eligible RTB connections'))

    @allure.feature('image mrec support')
    @allure.tag('normal', 'R_1.125.0')
    @allure.story('PBJ-1548 Verify template type when ads returns an image_mrec ad.')
    @allure.description('Verify the template type for image mrec ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_template_type_for_image_mrec_non_test_mode(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_image_mrec_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=non_test_mode_kraken_int1_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['template_type'], equal_to('mrec'))

    @allure.feature('image mrec support')
    @allure.tag('normal', 'R_1.135.0', 'test_mode')
    @allure.story('PBJ-197 Kraken image mrec support')
    @allure.description('Verify the test mode image mrec support for iOS')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_image_mrec_support_in_test_mode_ios(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_image_mrec_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['template_type'], equal_to('mrec'))

    @allure.feature('image mrec support')
    @allure.tag('normal', 'R_1.135.0', 'test_mode')
    @allure.story('PBJ-197 Kraken image mrec support')
    @allure.description('Verify the test mode image mrec support for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_image_mrec_support_in_test_mode_android(self, pub_app_id):
        req = request_payload.jaeger_v5_android(pub_app_id, android_image_mrec_test_placement,
                                                android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids,
                                                                        sdk_version='VungleDroid/6.5.3'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['template_type'], equal_to('mrec'))

    @allure.feature('image mrec support')
    @allure.tag('normal', 'R_1.135.0', 'test_mode')
    @allure.story('PBJ-197 Kraken image mrec support')
    @allure.description('Verify the test mode image mrec support for windows')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    def test_image_mrec_support_in_test_mode_windows(self, pub_app_id):
        req = request_payload.jaeger_v5_windows(pub_app_id, windows_image_mrec_test_placement,
                                                ashwid=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version='VungleWindows/6.5.3 (Windows 10; native)'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['template_type'], equal_to('mrec'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1784 Only serves Programmatic Banner/MREC for iOS 10 and above if the device on iOS platform')
    @allure.description('Verify that programmatic banner will be served for iOS >= 10 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('os_version', ['10', '10.0', '10.1'])
    def test_programmatic_banner_ios_10(self, pub_app_id, os_version):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True,
                                            os_version=os_version)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.132.0')
    @allure.story('PBJ-1784 Only serves Programmatic Banner/MREC for iOS 10 and above if the device on iOS platform')
    @allure.description('Verify that programmatic banner will not be served for iOS < 10 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('os_version', ['9.8', '9.9'])
    def test_programmatic_banner_ios_10_1(self, pub_app_id, os_version):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True,
                                            os_version=os_version)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_mraid, debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['sleep'], equal_to(121))
        assert_that(ad_markup['info'], equal_to('incompatible sdk with MRAID'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1784 Only serves Programmatic Banner/MREC for iOS 10 and above if the device on iOS platform')
    @allure.description('Verify that programmatic banner will be served for iOS >= 10 in non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('os_version', ['10', '10.0', '10.1'])
    def test_programmatic_banner_ios_10_2(self, pub_app_id, os_version):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_ifa, banner=True,
                                            os_version=os_version)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid_1,
                                          debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('programmatic support')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1784 Only serves Programmatic Banner/MREC for iOS 10 and above if the device on iOS platform')
    @allure.description('Verify that programmatic banner will not be served for iOS < 10 in non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('os_version', ['9.8', '9.9'])
    def test_programmatic_banner_ios_10_3(self, pub_app_id, os_version):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_ifa, banner=True,
                                            os_version=os_version)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['sleep'], equal_to(121))
        assert_that(ad_markup['info'], equal_to('incompatible sdk with MRAID'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1784 Only serves Programmatic Banner/MREC for iOS 10 and above if the device on iOS platform')
    @allure.description('Verify that programmatic mrec will be served for iOS >= 10 in non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [mrec_test_app])
    @pytest.mark.parametrize('os_version', ['10', '10.0', '10.1'])
    def test_programmatic_mrec_ios_10(self, pub_app_id, os_version):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, programmatic_mrec_placement, ifa=test_ifa,
                                            os_version=os_version)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version='Vungle/6.5.3',
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'R_1.132.0')
    @allure.story('PBJ-1784 Only serves Programmatic Banner/MREC for iOS 10 and above if the device on iOS platform')
    @allure.description('Verify that programmatic mrec will not be served for iOS < 10 in non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [mrec_test_app])
    @pytest.mark.parametrize('os_version', ['9.8', '9.9'])
    def test_programmatic_mrec_ios_10_1(self, pub_app_id, os_version):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, programmatic_mrec_placement, ifa=test_ifa,
                                            os_version=os_version)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version='Vungle/6.5.3',
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['sleep'], equal_to(121))
        assert_that(ad_markup['info'], equal_to('incompatible sdk with MRAID'))

    @allure.feature('rtb connection')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2229 App exclusion targeting at RTB Connection')
    @allure.description('Verify that both allowed and exclusion list is empty')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [rtb_exclusion_test_app])
    @pytest.mark.parametrize('placement', [rtb_exclusion_test_placement])
    def _test_rtb_exclusion_1(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_2))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('rtb connection')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2229 App exclusion targeting at RTB Connection')
    @allure.description('Verify that the pub app only on allowed list, and exclusion list is empty')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [rtb_exclusion_test_app])
    @pytest.mark.parametrize('placement', [rtb_exclusion_test_placement])
    def test_rtb_exclusion_2(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('rtb connection')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2229 App exclusion targeting at RTB Connection')
    @allure.description('Verify that the pub app only on exclusion list, and allowed list is empty')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [rtb_exclusion_test_app])
    @pytest.mark.parametrize('placement', [rtb_exclusion_test_placement])
    def test_rtb_exclusion_2(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_3))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['sleep'], equal_to(21603))
        assert_that(ad_markup['info'], equal_to('no eligible RTB connections'))

    @allure.feature('rtb connection')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2229 App exclusion targeting at RTB Connection')
    @allure.description('Verify that the pub app on exclusion list but not on allowed list, invalid scenario')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [rtb_exclusion_test_app])
    @pytest.mark.parametrize('placement', [rtb_exclusion_test_placement])
    def test_rtb_exclusion_4(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['sleep'], equal_to(21603))
        assert_that(ad_markup['info'], equal_to('no eligible RTB connections'))

    @allure.feature('rtb connection')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2229 App exclusion targeting at RTB Connection')
    @allure.description('Verify that the pub app only on allowed list, invalid scenario')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_exclusion_5(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('rtb connection')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2229 App exclusion targeting at RTB Connection')
    @allure.description('Verify that the pub app on both allowed and exclusion list, invalid scenario')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_exclusion_6(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('rtb connection')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2229 App exclusion targeting at RTB Connection')
    @allure.description('Verify that the pub app not on both exclusion and allowed list, invalid scenario')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_rtb_exclusion_7(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('rtb connection')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2229 App exclusion targeting at RTB Connection')
    @allure.description('Verify that the pub app not on allowed list, and exclusion list is empty')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_rtb_exclusion_8(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['sleep'], equal_to(21603))
        assert_that(ad_markup['info'], equal_to('no eligible RTB connections'))

    @allure.feature('rtb connection')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2229 App exclusion targeting at RTB Connection')
    @allure.description('Verify that the pub app on exclusion list of Meister rtb')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [rtb_exclusion_test_app])
    @pytest.mark.parametrize('placement', [rtb_exclusion_test_placement])
    def test_rtb_exclusion_9(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=gb_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['sleep'], equal_to(21603))
        assert_that(ad_markup['info'], equal_to('no eligible RTB connections'))

    @allure.feature('basic')
    @allure.tag('smoke', 'R_1.149.0')
    @allure.story('PBJ-2240 Adding timestamp for ads delivery')
    @allure.description('Verify the timestamp field from the ad unit')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    def test_timestamp_field_1(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=gb_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'timestamp')

    @allure.feature('basic')
    @allure.tag('smoke', 'R_1.149.0', 'test_mode')
    @allure.story('PBJ-2240 Adding timestamp for ads delivery')
    @allure.description('Verify the timestamp field from the ad unit')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_timestamp_field_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=gb_ip, rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'timestamp')

    # @allure.feature('ip blocking')
    # @allure.tag('normal', 'R_1.154.0')
    # @allure.story('PBJ-2446 Jaeger IP blocking')
    # @allure.description('Verify the Jaeger request will be blocked from the IP address which in block list')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_ip_blocking_1(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=blocked_ip, rtb_selector=meister_qa_rtbconnection_ids))
    #
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     assert_that(ad_markup['sleep'], equal_to(86423))
    #     assert_that(ad_markup['info'], equal_to('no serve'))
    #
    # @allure.feature('ip blocking')
    # @allure.tag('normal', 'R_1.154.0')
    # @allure.story('PBJ-2446 Jaeger IP blocking')
    # @allure.description('Verify the Jaeger request will be blocked from the IP address which in block list test mode')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_ip_blocking_2(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=blocked_ip, rtb_selector=kraken_rtbconnection_ids))
    #
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     assert_that(ad_markup['sleep'], equal_to(86423))
    #     assert_that(ad_markup['info'], equal_to('no serve'))
    #
    # @allure.feature('ip blocking')
    # @allure.tag('normal', 'R_1.154.0')
    # @allure.story('PBJ-2446 Jaeger IP blocking')
    # @allure.description('Verify the Jaeger request will not be blocked from the IP from the same sub mark '
    #                     'with the blacked one')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_ip_blocking_3(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=fr_ip, rtb_selector=meister_qa_rtbconnection_ids))
    #
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-3867 Block Adomain on RTB level'
                  'PBJ-4007 Jaeger should send RTB account \'s adomain backlist through badv field of bid request.')
    @allure.description('Verify block the adomain which set in account mongodb for ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_blocking_edsp_ios_01(self, pub_app_id, placement):
        """
        account setting:

        adDomainBlacklist:{"glu.com", "testabc.com"}
        """
        override_bid_adomain = 'glu.com,testabc.com'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_block_adomain,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              ext_non_test_mode_kraken_rtb_block_adomain)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_keys_exist(badv, override_bid_adomain.split(',')[0])
        assert_keys_exist(badv, override_bid_adomain.split(',')[1])


    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-3867 Block Adomain on RTB level'
                  'PBJ-4007 Jaeger should send RTB account \'s adomain backlist through badv field of bid request.')
    @allure.description('Verify block the adomain which set in account mongodb for ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_blocking_edsp_ios_02(self, pub_app_id, placement):
        """
              account setting:

              adDomainBlacklist:{"glu.com", "testabc.com"}
              """
        override_bid_adomain = "testabc.com"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_block_adomain,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              ext_non_test_mode_kraken_rtb_block_adomain)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_keys_exist(badv, override_bid_adomain)

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-3867 Block Adomain on RTB level'
                  'PBJ-4007 Jaeger should send RTB account \'s adomain backlist through badv field of bid request.')
    @allure.description('Verify block the adomain which set in account mongodb for windows platform')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    def test_adomain_blocking_edsp_windows(self, pub_app_id, placement):
        """
              account setting:

              adDomainBlacklist:{"glu.com", "testabc.com"}
        """
        override_bid_adomain = "glu.com"
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_block_adomain,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              ext_non_test_mode_kraken_rtb_block_adomain)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_keys_exist(badv, override_bid_adomain)

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-3867 Block Adomain on RTB level'
                  'PBJ-4007 Jaeger should send RTB account \'s adomain backlist through badv field of bid request.')
    @allure.description('Verify block the adomain which set in account mongodb for android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('placement', [android_common_coppa_placememt])
    def test_adomain_block_edsp_android(self, pub_app_id, placement):
        """
                   account setting:

                   adDomainBlacklist:{"glu.com", "testabc.com"}
        """
        override_bid_adomain = "glu.com"
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_block_adomain,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              ext_non_test_mode_kraken_rtb_block_adomain)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_keys_exist(badv, override_bid_adomain)

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4012 Jaeger support ADomain on RTB Account Level & Global Level.')
    @allure.description('Verify block the adomain which set in realtime mongodb(global level) for ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_block_global_ios(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video", "glu.com", "com.mopub.video"],
                "windows":[]
                }
        """
        override_bid_adomain = "com.mopub.video"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=non_test_mode_kraken_rtb_ids_no_adomain_block,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              non_test_mode_kraken_rtb_ids_no_adomain_block)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        assert_keys_exist(badv, override_bid_adomain)
        assert_that(['charm00.com', 'com.mopub.video', 'com.murka.scatterslots', 'domain2.com', 'domain3.com',
                     'domain4.com', 'glu.com', 'hhijb.com', 'osityh.com'],
                    equal_to(badv))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4012 Jaeger support ADomain on RTB Account Level & Global Level.')
    @allure.description('Verify block the adomain which set in realtime mongodb(global level) for ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_block_global_test_mode_ios(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video"],
                "windows":[]
                }
        """
        override_bid_adomain = "com.mopub.video"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=test_mode_kraken_rtb_ids_no_adomain_block,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              test_mode_kraken_rtb_ids_no_adomain_block)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        assert_keys_exist(badv, override_bid_adomain)
        assert_that(['charm00.com', 'com.mopub.video', 'com.murka.scatterslots', 'domain2.com', 'domain3.com',
                     'domain4.com', 'glu.com', 'hhijb.com', 'osityh.com'], equal_to(badv))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4012 Jaeger support ADomain on RTB Account Level & Global Level.')
    @allure.description('Verify block the adomain which set in realtime mongodb(global level) for ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_block_global_ios_edsp(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video"],
                "windows":[]
                }
        """
        override_bid_adomain = "com.murka.scatterslots"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector='62398afb7240231f0711cf2f',
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, '62398afb7240231f0711cf2f')
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        assert_keys_exist(badv, override_bid_adomain)
        assert_that(['charm00.com', 'com.mopub.video', 'com.murka.scatterslots', 'domain2.com', 'domain3.com',
                     'domain4.com', 'glu.com', 'hhijb.com', 'osityh.com'],
                    equal_to(badv))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4012 Jaeger support ADomain on RTB Account Level & Global Level.')
    @allure.description('Verify block the adomain which set in realtime mongodb(global level) for ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_block_global_ios_test_mode_edsp(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video"],
                "windows":[]
                }
        """
        override_bid_adomain = "com.murka.scatterslots"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector='623998777240231f0711cf32',
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, '623998777240231f0711cf32')
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        assert_keys_exist(badv, override_bid_adomain)
        assert_that(['charm00.com', 'com.mopub.video', 'com.murka.scatterslots', 'domain2.com', 'domain3.com',
                     'domain4.com', 'glu.com', 'hhijb.com', 'osityh.com'],
                    equal_to(badv))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4012 Jaeger support ADomain on RTB Account Level & Global Level.')
    @allure.description('Verify block the adomain which set in realtime mongodb(global level) for android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_adomain_block_global_android(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video"],
                "windows":[]
                }
        """
        override_bid_adomain = "com.murka.scatterslots"
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector='62398afb7240231f0711cf2f',
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, '62398afb7240231f0711cf2f')
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        assert_keys_exist(badv, override_bid_adomain)
        assert_that(['charm00.com', 'com.murka.scatterslots', 'domain3.com', 'domain4.com', 'hhijb.com', 'osityh.com'],
                    equal_to(badv))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4012 Jaeger support ADomain on RTB Account Level & Global Level.')
    @allure.description('Verify will not block for adomain not in list via android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_will_not_block_for_adomain_not_in_list_android(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video"],
                "windows":[]
                }
        """
        override_bid_adomain = "com.murka.scatterslot"
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'sleep')
        assert_that(['charm00.com', 'com.murka.scatterslots', 'domain3.com', 'domain4.com', 'glu.com', 'hhijb.com',
                     'osityh.com', 'testabc.com'], equal_to(badv))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4012 Jaeger support ADomain on RTB Account Level & Global Level.')
    @allure.description('Verify will not block for adomain not in list via amazon platform')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    def test_will_not_block_for_adomain_not_in_list_amazon(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video"],
                "windows":[]
                }
        """
        override_bid_adomain = "com.murka.scatterslots"
        req = request_payload.jaeger_v5_amazon(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_test_mode_kraken_rtb_ids_vast)
        badv = bid_request['badv']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(['charm00.com', 'glu.com', 'hhijb.com', 'osityh.com', 'testabc.com'], equal_to(badv))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4012 Jaeger support ADomain on RTB Account Level & Global Level.')
    @allure.description('Verify will not block for adomain not in list via windows platform')
    @pytest.mark.parametrize('pub_app_id', ['5b8d17307ad5a86fc53c7c8a'])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    def test_will_not_block_for_adomain_not_in_list_windows(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video"],
                "windows":[]
                }
        """
        override_bid_adomain = "com.murka.scatterslots"
        req = request_payload.jaeger_v5_windows(pub_app_id, 'DEFAULT-4642078', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip, rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version='VungleWindows/6.4.0 (Windows 10; native)',
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, test_mode_kraken_rtb_ids)
        badv = bid_request['badv']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(['charm00.com', 'glu.com', 'hhijb.com', 'osityh.com', 'testabc.com'], equal_to(badv))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4012 Jaeger support ADomain on RTB Account Level & Global Level.')
    @allure.description('Verify adomain block for mixed level via ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_block_for_mixed_level(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video", "glu.com", "com.mopub.video"],
                "windows":[]
                }
           rtb account setting:

           adDomainBlacklist:{
                "glu.com", "testabc.com"
           }

          application setting:

          adDomainBlacklist:{
                "domain2.com", "domain3.com", "Glu.com"
           }


        """
        override_bid_adomain = "com.mopub.video"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(['charm00.com', 'com.mopub.video', 'com.murka.scatterslots', 'domain2.com', 'domain3.com',
                     'domain4.com', 'glu.com', 'hhijb.com', 'osityh.com', 'testabc.com'],
                    equal_to(badv))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4039 aDomain Blocking - casing.')
    @allure.description('Verify adomain block for mixed level for case-insensitive via ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_block_for_mixed_level_case_insensitive_01(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video", "glu.com", "com.mopub.video"],
                "windows":[]
                }
           rtb account setting:

           adDomainBlacklist:{
                "glu.com", "testabc.com"
           }

          application setting:

          adDomainBlacklist:{
                "domain2.com", "domain3.com", "Glu.com"
           }


        """
        override_bid_adomain = "com.Mopub.video"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4039 aDomain Blocking - casing.')
    @allure.description('Verify adomain block for mixed level for case-insensitive via ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_block_for_mixed_level_case_insensitive_02(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video", "glu.com", "com.mopub.video"],
                "windows":[]
                }
           rtb account setting:

           adDomainBlacklist:{
                "glu.com", "testabc.com"
           }

          application setting:

          adDomainBlacklist:{
                "domain2.com", "domain3.com", "Glu.com"
           }


        """
        override_bid_adomain = "Glu.com"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))

    @allure.feature('Block Adomain')
    @allure.tag('normal')
    @allure.story('PBJ-4039 aDomain Blocking - casing.')
    @allure.description('Verify adomain block for mixed level for case-insensitive via ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_block_for_mixed_level_case_insensitive_03(self, pub_app_id, placement):
        """
           realtime setting:

           ad_domain_blacklist:{
                "amazon":[],
                "android":["com.murka.Scatterslots"],
                "ios": ["com.murka.Scatterslots", "com.Mopub.video", "glu.com", "com.mopub.video"],
                "windows":[]
                }
           rtb account setting:

           adDomainBlacklist:{
                "glu.com", "testabc.com"
           }

          application setting:

          adDomainBlacklist:{
                "domain2.com", "domain3.com", "Glu.com"
           }


        """
        override_bid_adomain = "TESTabc.com,domain.com"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))

    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4013 Block CRID on RTB Account level')
    @allure.description('Verify block the CRID which set in rtb account mongodb for ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_edsp_ios_01(self, pub_app_id, placement):
        """
       account setting:

       adCrIDBlacklist:['574351a9740cf4426b30d030']
        """
        override_crid = '574351a9740cf4426b30d030'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_block_crid,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], 'impression auctioned but unsold')

    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4013 Block CRID on RTB Account level')
    @allure.description('Verify block the CRID which set in rtb account mongodb for ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_edsp_ios_02(self, pub_app_id, placement):
        """
       account setting:

       adCrIDBlacklist:['574351a9740cf4426b30d030', '574351a9740cf4426b30d034']
        """
        override_crid = '574351a9740cf4426b30d034'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_block_crid,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], 'impression auctioned but unsold')

    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4013 Block CRID on RTB Account level')
    @allure.description('Verify block the CRID which set in rtb account mongodb for android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_block_crid_edsp_android(self, pub_app_id, placement):
        """
        account setting:

        adCrIDBlacklist:['574351a9740cf4426b30d030']
        """
        override_crid = '574351a9740cf4426b30d030'
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_block_crid,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], 'impression auctioned but unsold')

    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4013 Block CRID on RTB Account level')
    @allure.description('Verify block the CRID which set in rtb account mongodb for amazon platform')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    def test_block_crid_edsp_amazon(self, pub_app_id, placement):
        """
        account setting:

        adCrIDBlacklist:['574351a9740cf4426b30d030']
        """
        override_crid = '574351a9740cf4426b30d030'
        req = request_payload.jaeger_v5_amazon(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_block_crid,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], 'impression auctioned but unsold')

    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4013 Block CRID on RTB Account level')
    @allure.description('Verify block the CRID which set in rtb account mongodb for windows platform')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    def test_block_crid_edsp_windows(self, pub_app_id, placement):
        """
        account setting:

        adCrIDBlacklist:['574351a9740cf4426b30d030']
        """
        override_crid = '574351a9740cf4426b30d030'
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_block_crid,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], 'impression auctioned but unsold')

    @allure.feature('Block CRID')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4166 Block the creative ID for a specific publisher app')
    @allure.description('Verify block the CRID which setting in appliction')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('crid', ['310310', 'testabcabc'])
    def test_block_crid_on_app_01(self, pub_app_id, placement, crid):
        """
        app setting:

        adCrIDBlacklist:['310310','testabcabc']
        """
        override_crid = crid
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], 'impression auctioned but unsold')

    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4166 Block the creative ID for a specific publisher app')
    @allure.description('Verify block the CRID which setting in appliction')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('crid', ['310310', 'testabcabc'])
    def test_block_crid_on_app_02(self, pub_app_id, placement, crid):
        """
        app setting:

        adCrIDBlacklist:['310310','testabcabc']
        """
        override_crid = crid
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], 'impression auctioned but unsold')

    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4166 Block the creative ID for a specific publisher app')
    @allure.description('Verify jaeger will not block the CRID which setting in appliction for edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('crid', ['310310', 'testabcabc'])
    def test_will_not_block_crid_on_app_e(self, pub_app_id, placement, crid):
        """
        app setting:

        adCrIDBlacklist:['310310','testabcabc']
        """
        override_crid = crid
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4166 Block the creative ID for a specific publisher app')
    @allure.description(
        'Verify jaeger will block the CRID which both setting in appliction and in rtb account for idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('crid', ['310310', '574351a9740cf4426b30d030'])
    def test_will_block_crid_for_mixed_dimensinon(self, pub_app_id, placement, crid):
        """
        app setting:

        adCrIDBlacklist:['310310','testabcabc']

        rtb account setting:
         adCrIDBlacklist:['574351a9740cf4426b30d030','574351a9740cf4426b30d034']
        """
        override_crid = crid
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids_no_adomain_block, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], 'impression auctioned but unsold')

    @allure.feature('Block Ads')
    @allure.tag('normal')
    @allure.story('PBJ-4255 (Wooga) Block ads in certain countries')
    @allure.description('Verify Ads should be served for other countries for '
                        'Wooga (account ID: 561e8d936b8d90f61a00059f)')
    @pytest.mark.parametrize('pub_app_id', ['6285f9081f830de563bea707'])
    @pytest.mark.parametrize('placement', ['DEFAULT02021_10'])
    @pytest.mark.parametrize('src_ip', [au_ip, fr_ip])
    def test_ads_serve_for_other_countries(self, pub_app_id, placement, src_ip):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids_no_adomain_block, src_ip=src_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('Block Ads')
    @allure.tag('normal')
    @allure.story('PBJ-4255 (Wooga) Block ads in certain countries')
    @allure.description('Verify Ads shouldn\'t be served in Cuba, North Korea, Syria, Lebanon and Iran for '
                        'Wooga (account ID: 561e8d936b8d90f61a00059f)')
    @pytest.mark.parametrize('pub_apps', block_specify_country)
    @pytest.mark.parametrize('src_ip', [cu_ip, kp_ip, sy_ip, lb_ip, ir_ip])
    def test_ads_not_serve_for_specific_countries(self, pub_apps, src_ip):

        req = request_payload.jaeger_v5_ios(pub_apps['pub_app'], pub_apps['placement'],
                                            ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids_no_adomain_block, src_ip=src_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('Block Ads')
    @allure.tag('normal')
    @allure.story('PBJ-4308 (Playtika) Block ads in a few countries')
    @allure.description('Verify Ads shouldn\'t be served in Cuba, North Korea, Syria, Lebanon and Iran for '
                        'Wooga (account ID: 561e8d936b8d90f61a00059f)')
    @pytest.mark.parametrize('pub_apps', block_specify_country_android)
    @pytest.mark.parametrize('src_ip', [cu_ip, kp_ip, sy_ip, lb_ip, ir_ip])
    def test_ads_not_serve_for_specific_countries_02(self, pub_apps, src_ip):

        req = request_payload.jaeger_v5_android(pub_apps['pub_app'], pub_apps['placement'], ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids_no_adomain_block, src_ip=src_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('expiry experiment')
    @allure.tag('normal', 'v1.155.0', 'v1.169.0')
    @allure.story('PBJ-2553 Expiry experiment,  PBJ-3003 New round expiry experiment')
    @allure.description('Verify the pub app which not on list will not enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', ['HJKM6GM5090810'])
    def test_expiry_experiment_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, greater_than(3))
        assert_that((expiry - now).days, less_than_or_equal_to(7))

    @allure.feature('expiry experiment')
    @allure.tag('normal', 'v1.155.0', 'v1.169.0')
    @allure.story('PBJ-2553 Expiry experiment, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the not specific placement but app in list will enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_expiry_experiment_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(3))

    @allure.feature('expiry experiment')
    @allure.tag('normal', 'v1.155.0', 'v1.169.0')
    @allure.story('PBJ-2553 Expiry experiment, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the specific placement and app will enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_expiry_experiment_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(3))

    @allure.feature('expiry experiment')
    @allure.tag('normal', 'v1.155.0', 'v1.169.0')
    @allure.story('PBJ-2553 Expiry experiment, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the specific placement but app not in list will enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', ['HJKM6GM509080'])
    def test_expiry_experiment_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(3))

    @allure.feature('expiry experiment')
    @allure.tag('normal', 'v1.157.0', 'v1.169.0')
    @allure.story('PBJ-2606 Verify expiry time configurable in experiment, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expiry time follows the setting in ext')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_expiry_experiment_5(self, pub_app_id, placement):
        '''
            "ext": {
                "hours": 24
            }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(1))

    @allure.feature('expiry experiment')
    @allure.tag('normal', 'v1.157.0', 'v1.169.0')
    @allure.story('PBJ-2606 Verify expiry time configurable in experiment, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the placement which is matched with more than 1 experiment will not enter experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50918'])
    def test_expiry_experiment_6(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids, src_ip=au_ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(7))

    @allure.feature('block traffic')
    @allure.tag('normal', 'v1.156.0')
    @allure.story('PBJ-2565 Jaeger block traffic for specific account for windows SDK <6.5')
    @allure.description('Verify the Jaeger block traffic for specific account for windows SDK < 6.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5797949864c72d066f000097'])
    @pytest.mark.parametrize('placement', ['MAHDEFA10231'])
    @pytest.mark.parametrize('sdk_v', ['VungleWindows/6.4.9 (Windows 10; native)'])
    def test_block_traffic_windows_1(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=meister_rtb_ids, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(ad_markup['info'], equal_to('publisher inactive'))
        assert_that(ad_markup['sleep'], equal_to(86400))

    @allure.feature('block traffic')
    @allure.tag('normal', 'v1.156.0')
    @allure.story('PBJ-2565 Jaeger block traffic for specific account for windows SDK <6.5')
    @allure.description('Verify the Jaeger wont block traffic for specific account for windows SDK >= 6.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5797949864c72d066f000097'])
    @pytest.mark.parametrize('placement', ['MAHDEFA10231'])
    @pytest.mark.parametrize('sdk_v', ['VungleWindows/6.5.0 (Windows 10; native)',
                                       'VungleWindows/6.5.1 (Windows 10; native)'])
    def test_block_traffic_windows_2(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=meister_rtb_ids, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('publisher inactive'))
            assert_that(ad_markup['sleep'], not equal_to(86400))

    @allure.feature('block adv')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2685 Block advertising apps through domain (account&app)')
    @allure.description('Verify the domain on app black list can not be served by Jaeger')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b7'])
    @pytest.mark.parametrize('placement', ['DEFAULT02027'])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1, ext_test_mode_kraken_rtb_ids_vast])
    def test_block_adv_1(self, pub_app_id, placement, rtb):
        '''
        Account setting:
            adDomainBlacklist": ["domain3.com", "domain4.com"]

        App setting:
            "adDomainBlacklist": ["domain1.com"]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('block adv')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2685 Block advertising apps through domain (account&app)')
    @allure.description('Verify the domain on account black list can not be served by Jaeger')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b8'])
    @pytest.mark.parametrize('placement', ['DEFAULT02028'])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1, ext_test_mode_kraken_rtb_ids_vast])
    def test_block_adv_2(self, pub_app_id, placement, rtb):
        '''
        Account setting:
            adDomainBlacklist": ["domain1.com", "domain4.com"]

        App setting:
            "adDomainBlacklist": ["domain2.com", "domain3.com"]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('block adv')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2685 Block advertising apps through domain (account&app)')
    @allure.description('Verify the domain not on account black list can be served by Jaeger')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1, ext_test_mode_kraken_rtb_ids_vast])
    def test_block_adv_3(self, pub_app_id, placement, rtb):
        '''
        Account setting:
            adDomainBlacklist": ["domain3.com", "domain4.com"]

        App setting:
            "adDomainBlacklist": ["domain2.com", "domain3.com"]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.163.0', 'v1.169.0')
    @allure.story('PBJ-2774 Expiry time of internal ad for HB traffic, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expriy time is 1day for internal HB traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_expiry_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(1))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.163.0', 'v1.169.0', 'test_mode')
    @allure.story('PBJ-2774 Expiry time of internal ad for HB traffic, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expriy time is 1day for internal HB traffic in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_expiry_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(1))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.163.0', 'v1.169.0')
    @allure.story('PBJ-2774 Expiry time of internal ad for HB traffic, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expriy time will not affect external HB traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_expiry_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).seconds / 3600, less_than_or_equal_to(1))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.163.0', 'test_mode', 'v1.169.0')
    @allure.story('PBJ-2774 Expiry time of internal ad for HB traffic, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expriy time will not affect external HB traffic in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_expiry_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).seconds / 3600, less_than_or_equal_to(1))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.163.0', 'v1.169.0')
    @allure.story('PBJ-2774 Expiry time of internal ad for HB traffic, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expiry experiment not works for internal HB traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_hb_expiry_5(self, pub_app_id, placement):
        '''
            The expiry setting in experiment is 24h
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(1))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.163.0', 'test_mode', 'v1.169.0')
    @allure.story('PBJ-2774 Expiry time of internal ad for HB traffic, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expiry experiment not works for internal HB traffic in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_hb_expiry_6(self, pub_app_id, placement):
        '''
            The expiry setting in experiment is 24h
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(1))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.163.0', 'v1.169.0')
    @allure.story('PBJ-2774 Expiry time of internal ad for HB traffic, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expiry experiment not works for external HB traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_hb_expiry_7(self, pub_app_id, placement):
        '''
            The expiry setting in experiment is 24h
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).seconds / 3600, less_than_or_equal_to(1))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.163.0', 'test_mode', 'v1.169.0')
    @allure.story('PBJ-2774 Expiry time of internal ad for HB traffic, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expiry experiment not works for external HB traffic in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_hb_expiry_8(self, pub_app_id, placement):
        '''
            The expiry setting in experiment is 24h
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).seconds / 3600, less_than_or_equal_to(1))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.163.0', 'v1.169.0')
    @allure.story('PBJ-2774 Expiry time of internal ad for HB traffic, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expriy time does not work for internal non-HB traffic w/ or w/o HB placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, 'HJKM6GM50919'])
    def test_hb_expiry_9(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(7))
        assert_that((expiry - now).days, greater_than(1))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.163.0', 'v1.169.0')
    @allure.story('PBJ-2774 Expiry time of internal ad for HB traffic, PBJ-3003 New round expiry experiment')
    @allure.description('Verify the expriy time 1 day only consider about the traffic is HB or not')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_hb_expiry_10(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(1))

    @allure.feature('ddl')
    @allure.tag('normal', 'v1.164.0')
    @allure.story('PBJ-2772 Jaeger should not update placement DDL if no config')
    @allure.description('Verify that there is no DDL config on both app and placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ifa', [gen_device_id(), '', '00000000-0000-0000-0000-000000000000', '0000-0000', '-'])
    def test_ddl_config_1(self, pub_app_id, placement, ifa):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=ifa, header_bidding=True)
        post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))
        post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        if 'info' in ad_markup:
            assert_that(ad_markup['info'].count('daily delivery limit'), equal_to(0))

    @allure.feature('ddl')
    @allure.tag('normal', 'v1.164.0')
    @allure.story('PBJ-2772 Jaeger should not update placement DDL if no config'
                  'PBJ-3429 Sort out Jaeger Sleepcode')
    @allure.description('Verify that there is DDL config on both app and placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_ddl_config_2(self, pub_app_id, placement):
        '''
            app: 1, placement: 2
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        if 'info' in ad_markup:
            assert_that(ad_markup['info'].count('daily delivery limit'), equal_to(0))

        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(ad_markup['sleep'], equal_to(3603))
        assert_that(ad_markup['info'].count('daily delivery limit'), equal_to(1))

    # @allure.feature('ddl')
    # @allure.tag('normal', 'v1.164.0')
    # @allure.story('PBJ-2772 Jaeger should not update placement DDL if no config')
    # @allure.description('Verify that there is DDL config on both app and placement with empty device id')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    # @pytest.mark.parametrize('placement', [common_test_placement_1])
    # @pytest.mark.parametrize('ifa', ['', '00000000-0000-0000-0000-000000000000'])
    # def test_ddl_config_3(self, pub_app_id, placement, ifa):
    #     '''
    #         app: 1, placement: 2
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=ifa, header_bidding=True)
    #     post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_qa_rtbconnection_ids))
    #     post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_qa_rtbconnection_ids))
    #
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_qa_rtbconnection_ids))
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     if 'info' in ad_markup:
    #         assert_that(ad_markup['info'].count('daily delivery limit'), equal_to(0))

    @allure.feature('ddl')
    @allure.tag('normal', 'v1.164.0')
    @allure.story('PBJ-2772 Jaeger should not update placement DDL if no config'
                  'PBJ-3429 Sort out Jaeger Sleepcode')
    @allure.description('Verify that there is DDL config on only app level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', ['HJKM6GM509080'])
    def test_ddl_config_4(self, pub_app_id, placement):
        '''
            app: 1
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        if 'info' in ad_markup:
            assert_that(ad_markup['info'].count('daily delivery limit'), equal_to(0))

        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(ad_markup['sleep'], equal_to(3603))
        assert_that(ad_markup['info'].count('daily delivery limit'), equal_to(1))

    # @allure.feature('ddl')
    # @allure.tag('normal', 'v1.164.0')
    # @allure.story('PBJ-2772 Jaeger should not update placement DDL if no config')
    # @allure.description('Verify that there is DDL config on only app level with empty device id')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    # @pytest.mark.parametrize('placement', ['HJKM6GM509080'])
    # @pytest.mark.parametrize('ifa', ['', '00000000-0000-0000-0000-000000000000'])
    # def test_ddl_config_5(self, pub_app_id, placement, ifa):
    #     '''
    #         app: 1
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=ifa, header_bidding=True)
    #     post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_qa_rtbconnection_ids))
    #
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_qa_rtbconnection_ids))
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     if 'info' in ad_markup:
    #         assert_that(ad_markup['info'].count('daily delivery limit'), equal_to(0))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.169.0')
    @allure.story('PBJ-3003 New round expiry experiment')
    @allure.description('Verify the experiment does not impact the external HB traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_ext_expiry_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).seconds, less_than_or_equal_to(3600))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.169.0')
    @allure.story('PBJ-3003 New round expiry experiment')
    @allure.description('Verify the experiment does not impact the external HB traffic in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_ext_expiry_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).seconds, less_than_or_equal_to(3600))

    @allure.feature('hb expiry')
    @allure.tag('normal', 'v1.169.0')
    @allure.story('PBJ-3003 New round expiry experiment')
    @allure.description('Verify the experiment does not impact the external HB traffic which does not enter exp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    def test_hb_ext_expiry_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).seconds, less_than_or_equal_to(3600))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-3038 storeID information in Programmatic banner/Mrec Ads')
    @allure.description('Verify ad markup ad_market_id from ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_ad_markup_ad_market_id_programmatic_banner(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_that(ad_markup['ad_market_id'], equal_to(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle']))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.170.0', 'test_mode')
    @allure.story('PBJ-3038 storeID information in Programmatic banner/Mrec Ads')
    @allure.description('Verify ad markup ad_market_id from ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_ad_markup_ad_market_id_programmatic_banner_test_mode(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_that(ad_markup['ad_market_id'], equal_to(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle']))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-3038 storeID information in Programmatic banner/Mrec Ads')
    @allure.description('Verify ad markup ad_market_id from ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    def test_ad_markup_ad_market_id_programmatic_mrec(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_that(ad_markup['ad_market_id'], equal_to(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle']))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.170.0', 'test_mode')
    @allure.story('PBJ-3038 storeID information in Programmatic banner/Mrec Ads')
    @allure.description('Verify ad markup ad_market_id from ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    def test_ad_markup_ad_market_id_programmatic_mrec_test_mode(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_that(ad_markup['ad_market_id'], equal_to(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle']))

    @allure.feature('rtb meister support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3088 Send bid request to HBP specific Meister')
    @allure.description('Verify that the hb traffic can call the RTB Meister via the specific rtb connection')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_meister_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=hb_meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'info' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('unaccounted serving error'))

    @allure.feature('rtb meister support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3088 Send bid request to HBP specific Meister')
    @allure.description('Verify that the hb traffic can not call the legacy Meister via the specific rtb connection')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_meister_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=legacy_meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(21603))
        assert_that(ad_markup['info'], equal_to('no eligible RTB connections'))

    @allure.feature('rtb meister support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3088 Send bid request to HBP specific Meister')
    @allure.description('Verify that the non-hb traffic will not be impact with legacy Meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_meister_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=legacy_meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'info' in ad_markup:
            assert_that(ad_markup['sleep'], not equal_to(21603))
            assert_that(ad_markup['info'], not equal_to('no eligible RTB connections'))

    @allure.feature('rtb meister support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3088 Send bid request to HBP specific Meister')
    @allure.description('Verify that the non-hb traffic can not call the RTB Meister via the specific rtb connection')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_meister_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=hb_meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(21603))
        assert_that(ad_markup['info'], equal_to('no eligible RTB connections'))

    @allure.feature('rtb meister support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3088 Send bid request to HBP specific Meister')
    @allure.description('Verify that both hb and non-hb traffic will not be impact with eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_rtb_meister_5(self, pub_app_id, placement, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'info' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('unaccounted serving error'))

    @allure.feature('legacy ad')
    @allure.tag('normal', 'v1.172.0', 'v1.177.0')
    @allure.story('PBJ-3128 Filter out Legacy ads on 6.4+ SDK,'
                  'PBJ-3316 Filter out Legacy ads on 6.4+ on the iOS platform')
    @allure.description('Verify that Jaeger will filter out legacy ad when SDK >= 6.4.0 for iOS')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_legacy])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.4.0', 'Vungle/6.4.1'])
    def test_filter_out_legacy_1(self, pub_app_id, placement, sdk_ver):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_ver, src_ip=au_ip,
                                          rtb_selector=meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('legacy ad')
    @allure.tag('normal', 'v1.172.0', 'v1.177.0')
    @allure.story('PBJ-3128 Filter out Legacy ads on 6.4+ SDK,'
                  'PBJ-3316 Filter out Legacy ads on 6.4+ on the iOS platform')
    @allure.description('Verify that Jaeger will not filter out legacy ad when SDK < 6.4.0 for iOS')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_legacy])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.3.9'])
    def test_filter_out_legacy_2(self, pub_app_id, placement, sdk_ver):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_ver, src_ip=au_ip,
                                          rtb_selector=meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('legacy ad')
    @allure.tag('normal', 'v1.172.0', 'v1.177.0')
    @allure.story('PBJ-3128 Filter out Legacy ads on 6.4+ SDK,'
                  'PBJ-3316 Filter out Legacy ads on 6.4+ on the iOS platform')
    @allure.description('Verify that Jaeger will not filter out legacy ad when SDK >= 6.4.0 for Android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement_legacy])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.4.0', 'Vungle/6.4.1'])
    def test_filter_out_legacy_3(self, pub_app_id, placement, sdk_ver):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_ver, src_ip=au_ip,
                                          rtb_selector=meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('legacy ad')
    @allure.story('PBJ-3128 Filter out Legacy ads on 6.4+ SDK,'
                  'PBJ-3316 Filter out Legacy ads on 6.4+ on the iOS platform')
    @allure.description('Verify that Jaeger will not filter out legacy ad when SDK < 6.4.0 for Android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement_legacy])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.3.9'])
    def test_filter_out_legacy_4(self, pub_app_id, placement, sdk_ver):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_ver, src_ip=au_ip,
                                          rtb_selector=meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('legacy ad')
    @allure.story('PBJ-3128 Filter out Legacy ads on 6.4+ SDK,'
                  'PBJ-3316 Filter out Legacy ads on 6.4+ on the iOS platform')
    @allure.description('Verify that Jaeger will not filter out legacy ad when SDK >= 6.4.0 for Windows')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement_legacy])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.4.0', 'Vungle/6.4.1'])
    def test_filter_out_legacy_5(self, pub_app_id, placement, sdk_ver):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ashwid=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_ver, src_ip=au_ip,
                                          rtb_selector=meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('legacy ad')
    @allure.story('PBJ-3128 Filter out Legacy ads on 6.4+ SDK,'
                  'PBJ-3316 Filter out Legacy ads on 6.4+ on the iOS platform')
    @allure.description('Verify that Jaeger will not filter out legacy ad when SDK < 6.4.0 for Windows')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement_legacy])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.3.9'])
    def test_filter_out_legacy_6(self, pub_app_id, placement, sdk_ver):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ashwid=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_ver, src_ip=au_ip,
                                          rtb_selector=meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('click coordinate')
    @allure.tag('normal', 'v1.173.0', 'test_mode')
    @allure.story('PBJ-3150 Click coordinate reporting in Jaeger')
    @allure.description('Verify the click coordinates flag for non-tencent eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_click_coordinates_flag_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_that(ad_markup['click_coordinates_enabled'], equal_to(True))

    @allure.feature('click coordinate')
    @allure.tag('normal', 'v1.173.0', 'test_mode')
    @allure.story('PBJ-3150 Click coordinate reporting in Jaeger')
    @allure.description('Verify the click coordinates flag for tencent eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_click_coordinates_flag_2(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(rtb_selector=ext_test_mode_kraken_vast_rtb_ids_tencent,
                                              sdk_version=test_default_real_time_sdk_version))

            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            assert_that(ad_markup['click_coordinates_enabled'], equal_to(True))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.173.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify that the SDK version will not impact hb traffic calls the RTB Meister via the '
                        'real-time Meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.1', 'Vungle/6.9.2'])
    def test_rtb_meister_sdk_version_1(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=hb_meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'info' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('unaccounted serving error'))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.173.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify that the SDK version will not impact non-hb traffic calls the legacy Meister via the '
                        'legacy Meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.1', 'Vungle/6.9.2'])
    def test_rtb_meister_sdk_version_2(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=legacy_meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'info' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('unaccounted serving error'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.176.0')
    @allure.story('PBJ-3194 Check sdk version for Native placement in Ads request')
    @allure.description('Verify that Jaeger should not serve for native type if SDK < 6.11.0 via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_sdk_version_ctl_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=test_default_multi_cache_sdk_version,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(122))
        assert_that(ad_markup['info'], equal_to('incompatible sdk with ad type'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.176.0', 'test_mode')
    @allure.story('PBJ-3194 Check sdk version for Native placement in Ads request')
    @allure.description('Verify that Jaeger should not serve for native type if SDK < 6.11.0 via iDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_sdk_version_ctl_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=test_default_multi_cache_sdk_version,
                                          rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(122))
        assert_that(ad_markup['info'], equal_to('incompatible sdk with ad type'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.176.0')
    @allure.story('PBJ-3194 Check sdk version for Native placement in Ads request')
    @allure.description('Verify that Jaeger should not serve for native type if SDK < 6.11.0 via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_sdk_version_ctl_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=test_default_multi_cache_sdk_version,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(122))
        assert_that(ad_markup['info'], equal_to('incompatible sdk with ad type'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.176.0', 'test_mode')
    @allure.story('PBJ-3194 Check sdk version for Native placement in Ads request')
    @allure.description('Verify that Jaeger should not serve for native type if SDK < 6.11.0 via eDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_sdk_version_ctl_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=test_default_multi_cache_sdk_version,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(122))
        assert_that(ad_markup['info'], equal_to('incompatible sdk with ad type'))

    @allure.feature('gzip support')
    @allure.tag('normal', 'v1.177.0', 'test_mode')
    @allure.story('PBJ-3121 RTB :: Gzip Bid Requests')
    @allure.description('Verify Jaeger serves normally via gzip enabled rtb connection in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_gzip, ext_test_mode_kraken_rtb_ids_vast_gzip])
    def test_gzip_enabled_rtb_test_mode(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that('info' not in ad_markup)

    @allure.feature('gzip support')
    @allure.tag('normal', 'v1.177.0')
    @allure.story('PBJ-3121 RTB :: Gzip Bid Requests')
    @allure.description('Verify Jaeger serves normally via gzip enabled rtb connection in non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [non_test_mode_kraken_rtb_ids_gzip, ext_non_test_mode_kraken_rtb_ids_vast_gzip])
    def test_gzip_enabled_rtb(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that('info' not in ad_markup)


    @allure.feature('gzip support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3925 Cache gzip encoded bytes at bidWorkProducer in advance')
    @allure.description('Verify Jaeger serve normally and bid requests are the same '
                        'for the same setting enabled gzip in test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [test_mode_same_setting_rtb_ids_gzip])
    def test_gzip_enabled_rtb_2(self, pub_app_id, placement, rtb):
        rtb_id1 = rtb.split(',')[0]
        rtb_id2 = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        bid_request1 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_id1)
        bid_request2 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_id2)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request1, equal_to(bid_request2))

    @allure.feature('gzip support')
    @allure.tag('normal')
    @allure.story('PBJ-3925 Cache gzip encoded bytes at bidWorkProducer in advance')
    @allure.description('Verify Jaeger serve normally and bid requests are the same '
                        'for the same setting enabled gzip in non test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [non_test_mode_same_setting_rtb_ids_gzip])
    def test_gzip_enabled_rtb_3(self, pub_app_id, placement, rtb):
        rtb_id1 = rtb.split(',')[0]
        rtb_id2 = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        bid_request1 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_id1)
        bid_request2 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_id2)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request1, equal_to(bid_request2))

    @allure.feature('gzip support')
    @allure.tag('normal')
    @allure.story('PBJ-3925 Cache gzip encoded bytes at bidWorkProducer in advance')
    @allure.description('Verify Jaeger serve normally and bid requests are the same '
                        'for the same setting enabled gzip in non test mode edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_same_setting_rtb_ids_vast_gzip])
    def test_gzip_enabled_rtb_edsp_non_test_mode(self, pub_app_id, placement, rtb):
        rtb_id1 = rtb.split(',')[0]
        rtb_id2 = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        bid_request1 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_id1)
        bid_request2 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_id2)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request1, equal_to(bid_request2))

    @allure.feature('gzip support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3925 Cache gzip encoded bytes at bidWorkProducer in advance')
    @allure.description('Verify Jaeger serve normally and bid requests are the same '
                        'for the same setting enabled gzip in test mode edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_test_mode_kraken_same_setting_rtb_ids_vast_gzip])
    def test_gzip_enabled_rtb_edsp_test_mode(self, pub_app_id, placement, rtb):
        rtb_id1 = rtb.split(',')[0]
        rtb_id2 = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        bid_request1 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_id1)
        bid_request2 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_id2)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request1, equal_to(bid_request2))

    @allure.feature('gzip support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3925 Cache gzip encoded bytes at bidWorkProducer in advance')
    @allure.description('Verify Jaeger serve normally and bid requests are different '
                        'for the different setting enabled gzip')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [mixed_non_test_rtbs_gzip])
    def test_gzip_enabled_rtb_edsp_test_mode(self, pub_app_id, placement, rtb):
        rtb_id1 = rtb.split(',')[0]
        rtb_id2 = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        bid_request1 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_id1)
        bid_request2 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_id2)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request1, not equal_to(bid_request2))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from ad_markup via sdv version >= 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_ad_markup(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'deeplinkUrl')
        assert_that(isinstance(ad_markup['deeplinkUrl'], str))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from ad_markup via sdv version >= 6.11.0'
                        ' and test mode eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_ad_markup_test_mode(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'deeplinkUrl')
        assert_that(isinstance(ad_markup['deeplinkUrl'], str))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from ad markup via sdv version < 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_no_deeplink_in_ad_markup_test_mode(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'deeplinkUrl')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from ad markup via sdv version < 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_no_deeplink_in_ad_markup(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'deeplinkUrl')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from ad markup via sdv version >= 6.11.0'
                        ' and iDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_no_deeplink_in_ad_markup_iDSP(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=hb_meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'deeplinkUrl')

    # ------------------------------------------- deeplink for android --------------------------------------------------
    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from ad_markup via sdv version >= 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_ad_markup_android(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'deeplinkUrl')
        assert_that(isinstance(ad_markup['deeplinkUrl'], str))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from ad_markup via sdv version >= 6.11.0'
                        ' and test mode eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_ad_markup_test_mode_android(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb,
                                                android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'deeplinkUrl')
        assert_that(isinstance(ad_markup['deeplinkUrl'], str))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from ad markup via sdv version < 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_no_deeplink_in_ad_markup_test_mode_android(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb,
                                                android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'deeplinkUrl')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from ad markup via sdv version < 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_no_deeplink_in_ad_markup_android(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'deeplinkUrl')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from ad markup via sdv version >= 6.11.0'
                        ' and iDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_no_deeplink_in_ad_markup_android_iDSP(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=hb_meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'deeplinkUrl')

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3333 Cannot fill AdMarketID from SKAdNetwork information')
    @allure.description('Verify the ad_market_id will be filled by itunesitem from skadn if no bundle in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_ad_market_id_fill_fix_1(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = ext2_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                              override_bid_response_any='seatbid.0.bid.0.bundle@\"\"'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            ad_market_id = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']['skadn']['itunesitem']
            assert_that(ad_markup['ad_market_id'], equal_to(ad_market_id))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3333 Cannot fill AdMarketID from SKAdNetwork information')
    @allure.description('Verify the ad_market_id will be filled by itunesitem from skadn if no bundle in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    def test_ad_market_id_fill_fix_2(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = ext2_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                              override_bid_response_any='seatbid.0.bid.0.bundle@\"\"'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            ad_market_id = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']['skadn']['itunesitem']
            assert_that(ad_markup['ad_market_id'], equal_to(ad_market_id))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'smoke')
    @allure.story('PBJ-3676 Update Jaeger to fix iOS 15 black screen issues for programmatic ads')
    @allure.description('Verify programmatic ads can work well for mrec placement'
                        ' on iOS 15 when v_ios>=15 and sdk_v<6.10.3 ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    @pytest.mark.parametrize('osv', ['15', '15.1'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_ios_15_fix_01(self, pub_app_id, placement, osv, sdk_v):
        if env == 'qa' or env == 'regression':
            rtb = ext2_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
            r = post(ads_v5_endpoint_qa_real_adbuilder, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, sdk_version=sdk_v))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            template_settings = ad_markup['templateSettings']
            assert_keys_exist(template_settings, 'cacheable_replacements')
            assert_keys_exist(template_settings['cacheable_replacements'], 'IOS15_REPLACEMENTS')
            assert_keys_exist(template_settings['cacheable_replacements'], 'IOS15_TOKEN_MAP')
            assert_keys_exist(template_settings['cacheable_replacements'], 'VUNGLE_MRAID')
            assert_that('https://' in template_settings['cacheable_replacements']['IOS15_REPLACEMENTS']['url'])
            assert_that('https://' in template_settings['cacheable_replacements']['IOS15_TOKEN_MAP']['url'])
            assert_that('https://' in template_settings['cacheable_replacements']['VUNGLE_MRAID']['url'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'smoke', 'test_mode')
    @allure.story('PBJ-3676 Update Jaeger to fix iOS 15 black screen issues for programmatic ads')
    @allure.description('Verify programmatic ads can work well for mrec placement'
                        ' on iOS 15 when v_ios>=15 and sdk_v<6.10.3 ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_video_mrec_placement])
    @pytest.mark.parametrize('osv', ['15', '15.1'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_ios_15_fix_test_mode_02(self, pub_app_id, placement, osv, sdk_v):
        if env == 'qa' or env == 'regression':
            rtb = ext1_test_mode_kraken_rtb_ids_vast.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
            r = post(ads_v5_endpoint_qa_real_adbuilder, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, sdk_version=sdk_v))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            template_settings = ad_markup['templateSettings']
            assert_keys_exist(template_settings, 'cacheable_replacements')
            assert_keys_exist(template_settings['cacheable_replacements'], 'IOS15_REPLACEMENTS')
            assert_keys_exist(template_settings['cacheable_replacements'], 'IOS15_TOKEN_MAP')
            assert_keys_exist(template_settings['cacheable_replacements'], 'VUNGLE_MRAID')
            assert_that('https://' in template_settings['cacheable_replacements']['IOS15_REPLACEMENTS']['url'])
            assert_that('https://' in template_settings['cacheable_replacements']['IOS15_TOKEN_MAP']['url'])
            assert_that('https://' in template_settings['cacheable_replacements']['VUNGLE_MRAID']['url'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'smoke')
    @allure.story('PBJ-3676 Update Jaeger to fix iOS 15 black screen issues for programmatic ads')
    @allure.description('Verify programmatic ads can work well for mrec placement'
                        ' on iOS 15 when v_ios>=15 and sdk_v<6.10.3 ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('osv', ['15', '15.1'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_ios_15_fix_03(self, pub_app_id, placement, osv, sdk_v):
        if env == 'qa' or env == 'regression':
            rtb = ext2_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv, banner=True)
            r = post(ads_v5_endpoint_qa_real_adbuilder, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, sdk_version=sdk_v))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            template_settings = ad_markup['templateSettings']
            assert_keys_exist(template_settings, 'cacheable_replacements')
            assert_keys_exist(template_settings['cacheable_replacements'], 'IOS15_REPLACEMENTS')
            assert_keys_exist(template_settings['cacheable_replacements'], 'IOS15_TOKEN_MAP')
            assert_keys_exist(template_settings['cacheable_replacements'], 'VUNGLE_MRAID')
            assert_that('https://' in template_settings['cacheable_replacements']['IOS15_REPLACEMENTS']['url'])
            assert_that('https://' in template_settings['cacheable_replacements']['IOS15_TOKEN_MAP']['url'])
            assert_that('https://' in template_settings['cacheable_replacements']['VUNGLE_MRAID']['url'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'smoke')
    @allure.story('PBJ-3676 Update Jaeger to fix iOS 15 black screen issues for programmatic ads')
    @allure.description('Verify programmatic ads can work well for mrec placement'
                        ' on iOS 15 when v_ios>=15 and sdk_v<6.10.3 ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['15', '15.1'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_ios_15_fix_04(self, pub_app_id, placement, osv, sdk_v):
        if env == 'qa' or env == 'regression':
            rtb = ext2_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
            r = post(ads_v5_endpoint_qa_real_adbuilder, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, sdk_version=sdk_v))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            template_settings = ad_markup['templateSettings']
            assert_keys_exist(template_settings, 'cacheable_replacements')
            assert_keys_exist(template_settings['cacheable_replacements'], 'IOS15_REPLACEMENTS')
            assert_keys_exist(template_settings['cacheable_replacements'], 'IOS15_TOKEN_MAP')
            assert_keys_exist(template_settings['cacheable_replacements'], 'VUNGLE_MRAID')
            assert_that('https://' in template_settings['cacheable_replacements']['IOS15_REPLACEMENTS']['url'])
            assert_that('https://' in template_settings['cacheable_replacements']['IOS15_TOKEN_MAP']['url'])
            assert_that('https://' in template_settings['cacheable_replacements']['VUNGLE_MRAID']['url'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'smoke')
    @allure.story('PBJ-3676 Update Jaeger to fix iOS 15 black screen issues for programmatic ads')
    @allure.description('Verify programmatic ads can work well for mrec placement'
                        ' on iOS 15 when v_ios>=15 and sdk_v<6.10.3 ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['15', '15.1'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_ios_15_fix_05(self, pub_app_id, placement, osv, sdk_v):
        if env == 'qa' or env == 'regression':
            rtb = meister_rtb_ids
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
            r = post(ads_v5_endpoint_qa_real_adbuilder, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, sdk_version=sdk_v))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            template_settings = ad_markup['templateSettings']
            assert_keys_exist(template_settings, 'cacheable_replacements')
            assert_keys_exist(template_settings['cacheable_replacements'], 'IOS15_REPLACEMENTS')
            assert_keys_exist(template_settings['cacheable_replacements'], 'IOS15_TOKEN_MAP')
            assert_keys_exist(template_settings['cacheable_replacements'], 'VUNGLE_MRAID')
            assert_that('https://' in template_settings['cacheable_replacements']['IOS15_REPLACEMENTS']['url'])
            assert_that('https://' in template_settings['cacheable_replacements']['IOS15_TOKEN_MAP']['url'])
            assert_that('https://' in template_settings['cacheable_replacements']['VUNGLE_MRAID']['url'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'smoke')
    @allure.story('PBJ-3676 Update Jaeger to fix iOS 15 black screen issues for programmatic ads')
    @allure.description('Verify the three js file will not be added in cacheable_replacements for mrec placement'
                        ' on iOS 15 when v_ios>=15 and sdk_v>=6.10.3 ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['15', '15.1'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_ios_15_fix_06(self, pub_app_id, placement, osv, sdk_v):
        if env == 'qa' or env == 'regression':
            rtb = meister_rtb_ids
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
            r = post(ads_v5_endpoint_qa_real_adbuilder, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, sdk_version=sdk_v))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            template_settings = ad_markup['templateSettings']
            assert_keys_exist(template_settings, 'cacheable_replacements')
            assert_keys_not_exist(template_settings['cacheable_replacements'], 'IOS15_REPLACEMENTS')
            assert_keys_not_exist(template_settings['cacheable_replacements'], 'IOS15_TOKEN_MAP')
            assert_keys_not_exist(template_settings['cacheable_replacements'], 'VUNGLE_MRAID')

    @allure.feature('programmatic support')
    @allure.tag('normal', 'smoke')
    @allure.story('PBJ-3676 Update Jaeger to fix iOS 15 black screen issues for programmatic ads')
    @allure.description('Verify the three js file will not be added in cacheable_replacements for mrec placement'
                        ' on iOS 15 when v_ios<15 and sdk_v<6.10.3 ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['14.1', ])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_ios_15_fix_07(self, pub_app_id, placement, osv, sdk_v):
        if env == 'qa' or env == 'regression':
            rtb = meister_rtb_ids
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
            r = post(ads_v5_endpoint_qa_real_adbuilder, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, sdk_version=sdk_v))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            template_settings = ad_markup['templateSettings']
            assert_keys_exist(template_settings, 'cacheable_replacements')
            assert_keys_not_exist(template_settings['cacheable_replacements'], 'IOS15_REPLACEMENTS')
            assert_keys_not_exist(template_settings['cacheable_replacements'], 'IOS15_TOKEN_MAP')
            assert_keys_not_exist(template_settings['cacheable_replacements'], 'VUNGLE_MRAID')

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.181.0')
    @allure.story('PBJ-3415 Assign the correct impression type for Native')
    @allure.description('Verify the template type should be native for native placement via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_template_type_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=us_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['template_type'], equal_to('native'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.181.0')
    @allure.story('PBJ-3415 Assign the correct impression type for Native')
    @allure.description('Verify the template type should be native for native placement via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_template_type_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['template_type'], equal_to('native'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.181.0')
    @allure.story('PBJ-3415 Assign the correct impression type for Native')
    @allure.description('Verify the template type should be native for native placement via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', ['NATIVE_PLACEMENT_01-7689948'])
    def test_native_placement_template_type_android_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, debug="jaeger"))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['template_type'], equal_to('native'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.181.0', 'test_mode')
    @allure.story('PBJ-3415 Assign the correct impression type for Native')
    @allure.description('Verify the template type should be native for native placement via iDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_template_type_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=us_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['template_type'], equal_to('native'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.181.0', 'test_mode')
    @allure.story('PBJ-3415 Assign the correct impression type for Native')
    @allure.description('Verify the template type should be native for native placement via eDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_template_type_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['template_type'], equal_to('native'))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-5098 The macros in native response should be replaced correctly.')
    @allure.description('Verify that macros should be replaced')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_macros_replaced(self, pub_app_id, placement):
        adm = '{\\\"native\\\":{\\\"assets\\\":[{\\\"id\\\":1,\\\"required\\\":1,\\\"img\\\":{\\\"url\\\":\\\"https:\\\/\\\/cdn-f.adsmoloco.com\\\/L4pnIkwXfKNhe7zn\\\/creative\\\/1200x628_static__bopeqsszogt0g1jz.png\\\",\\\"h\\\":628,\\\"w\\\":1200}},{\\\"id\\\":4,\\\"data\\\":{\\\"value\\\":\\\"BAIXE AGORA\\\",\\\"label\\\":\\\"\\\"}},{\\\"id\\\":5,\\\"required\\\":1,\\\"img\\\":{\\\"url\\\":\\\"https:\\\/\\\/cdn-f.adsmoloco.com\\\/L4pnIkwXfKNhe7zn\\\/creative\\\/google_play_512x_em4epma4xjbrcvt7.png\\\",\\\"h\\\":512,\\\"w\\\":512}},{\\\"id\\\":6,\\\"required\\\":1,\\\"title\\\":{\\\"text\\\":\\\"365 Scores\\\"}},{\\\"id\\\":7,\\\"data\\\":{\\\"value\\\":\\\"N\\u00E3o perca termpo: baixe o app 365scores agora e comece a contar seus ganhos!\\\",\\\"label\\\":\\\"\\\"}},{\\\"id\\\":8,\\\"data\\\":{\\\"value\\\":\\\"4.6\\\",\\\"label\\\":\\\"\\\"}},{\\\"id\\\":9,\\\"img\\\":{\\\"url\\\":\\\"https:\\\/\\\/cdn-f.adsmoloco.com\\\/L4pnIkwXfKNhe7zn\\\/creative\\\/google_play_512x_em4epma4xjbrcvt7.png\\\",\\\"h\\\":120,\\\"w\\\":120}},{\\\"id\\\":11,\\\"data\\\":{\\\"value\\\":\\\"365Scores LTD\\\",\\\"label\\\":\\\"\\\"}}],\\\"link\\\":{\\\"url\\\":\\\"https:\\\/\\\/tr-us.adsmoloco.com\\\/rtb\\\/click?exchange=VUNGLE\\\\u0026imp_id=63a36ff8263492264d41497c\\\\u0026info=ChAZwvqxNL9H5q-737UEUD1DEPjfjZ0GGhQIARoQsyWshK-rR6G8U3d-CfCwLyABKgAyAA\\\\u0026campaign_name=d9g8CbN5Zzd3aLHX\\\\u0026dcr=\\\",\\\"clicktrackers\\\":null},\\\"imptrackers\\\":[\\\"https:\\\/\\\/tr-us.adsmoloco.com\\\/rtb\\\/imp?exchange=VUNGLE\\\\u0026info=ChAZwvqxNL9H5q-737UEUD1DEPjfjZ0GGhQIARoQsyWshK-rR6G8U3d-CfCwLyABKgAyAA\\\\u0026campaign_name=d9g8CbN5Zzd3aLHX\\\\u0026imp_id=63a36ff8263492264d41497c\\\\u0026price=${AUCTION_PRICE}\\\",\\\"https:\\\/\\\/tr-us.adsmoloco.com\\\/rtb\\\/imp_fwd?exchange=VUNGLE\\\\u0026info=ChAZwvqxNL9H5q-737UEUD1DEPjfjZ0GGhQIARoQsyWshK-rR6G8U3d-CfCwLyABKgAyAA\\\\u0026price=${AUCTION_PRICE}\\\\u0026auctionid=${AUCTION_ID}\\\"],\\\"privacy\\\":\\\"https:\\\/\\\/cdn-f.adsmoloco.com\\\/moloco-cdn\\\/privacy.html\\\"}}'
        over_ride_bid_reposne = 'seatbid.0.bid.0.adm@"%s"' % adm
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, debug='jaeger',
                                          override_bid_response_any=over_ride_bid_reposne))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['template_type'], equal_to('native'))
        checkpoint0 = ad_markup['tpat']['checkpoint.0']
        urls = checkpoint0[0]
        for url in urls:
            if "https://tr-us.adsmoloco" in url:
                assert_that("${AUCTION_PRICE}" not in url)


    @allure.feature('native placement')
    @allure.tag('normal', 'v1.181.0', 'test_mode')
    @allure.story('PBJ-3415 Assign the correct impression type for Native')
    @allure.description('Verify the native type placement request will only invite native impression supported RTBs ')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_rtb_filter_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_multi_cache_sdk_version,
                                          rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(122))
        assert_that(ad_markup['info'], equal_to('incompatible sdk with ad type'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.181.0', 'test_mode')
    @allure.story('PBJ-3415 Assign the correct impression type for Native')
    @allure.description('Verify the native type placement request will only invite native impression supported RTBs ')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_rtb_filter_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=test_default_multi_cache_sdk_version,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(122))
        assert_that(ad_markup['info'], equal_to('incompatible sdk with ad type'))

    @allure.feature('sleep code')
    @allure.tag('normal', 'v1.182.0')
    @allure.story('PBJ-3426 Refactor BlacklistwhitelistInfoProvider, move the logic to dal package')
    @allure.description('Verify the placement level ad tag blacklist setting is conflict with pub app level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026c1'])
    @pytest.mark.parametrize('placement', ['DEFAULT02031'])
    def test_ad_tag_blacklist_conflict(self, pub_app_id, placement):
        '''
        Pub app level setting:

            "adTagWhitelist" : [
                "bbb"
            ]

        Placement level setting:

            "adTagBlacklist" : [
                "bbb"
            ]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['info'], equal_to('placement not found'))
        assert_that(ad_markup['sleep'], equal_to(902))

    @allure.feature('sleep code')
    @allure.tag('normal', 'v1.182.0')
    @allure.story('PBJ-3426 Refactor BlacklistwhitelistInfoProvider, move the logic to dal package')
    @allure.description('Verify the pub level ad blacklist setting is conflict with account level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026c2'])
    @pytest.mark.parametrize('placement', ['DEFAULT02032'])
    def test_ad_blacklist_conflict_1(self, pub_app_id, placement):
        '''
        Pub app level setting:

            "adWhitelist": [{
                "$oid": "513a1d5e5cac775f65000047"
            }]

        Account level setting:

            "adBlacklist": [{
                "$oid": "513a1d5e5cac775f65000047"
            }]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['info'], equal_to('publisher not found'))
        assert_that(ad_markup['sleep'], equal_to(901))

    @allure.feature('sleep code')
    @allure.tag('normal', 'v1.182.0')
    @allure.story('PBJ-3426 Refactor BlacklistwhitelistInfoProvider, move the logic to dal package')
    @allure.description('Verify the pub level ad blacklist setting is conflict with account level setting,'
                        'and the placement level ad tag blacklist setting is conflict with pub app level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026c2'])
    @pytest.mark.parametrize('placement', ['DEFAULT020321'])
    def test_ad_blacklist_conflict_2(self, pub_app_id, placement):
        '''
        Pub app level setting:

            "adWhitelist": [{
                "$oid": "513a1d5e5cac775f65000047"
            }],
            "adTagWhitelist" : [
                "bbb"
            ]

        Account level setting:

            "adBlacklist": [{
                "$oid": "513a1d5e5cac775f65000047"
            }]

        Placement level setting:

            "adTagBlacklist" : [
                "bbb"
            ]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['info'], equal_to('publisher not found'))
        assert_that(ad_markup['sleep'], equal_to(901))

    # @allure.feature('sleep code')
    # @allure.tag('normal')
    # @allure.story('PBJ-3429 Sort out Jaeger Sleepcode')
    # @allure.description('Verify incompatible admarkup sleep code')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_sleep_code_incompatible_admarkup(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid))
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_that(ad_markup['sleep'], equal_to(53))
    #     assert_that(ad_markup['info'], equal_to('incompatible admarkup'))

    @allure.feature('vungle mraid')
    @allure.tag('normal', 'v1.184.0')
    @allure.story('PBJ-3411 Block Vungle MRAID Ads for specific apps when devices are in low power mode')
    @allure.description('Verify it will not serve when devices are in low power mode for the specific applications'
                        ' connecting meister')
    @pytest.mark.parametrize('apps', block_low_power_mode_apps)
    def test_block_vungle_mraid_01(self, apps):
        req = request_payload.jaeger_v5_ios(apps[0], apps[1], ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(1813))
        assert_that(ad_markup['info'], equal_to('publisher battery saver mode not support'))

    @allure.feature('vungle mraid')
    @allure.tag('normal', 'v1.184.0')
    @allure.story('PBJ-3411 Block Vungle MRAID Ads for specific apps when devices are in low power mode')
    @allure.description('Verify it will not serve when devices are in low power mode for specific applications '
                        'connecting eDSP')
    @pytest.mark.parametrize('apps', block_low_power_mode_apps)
    def test_block_vungle_mraid_edsp_01(self, apps):
        req = request_payload.jaeger_v5_ios(apps[0], apps[1], ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(1813))
        assert_that(ad_markup['info'], equal_to('publisher battery saver mode not support'))

    @allure.feature('vungle mraid')
    @allure.tag('normal', 'v1.184.0', 'test_mode')
    @allure.story('PBJ-3411 Block Vungle MRAID Ads for specific apps when devices are in low power mode')
    @allure.description('Verify it will not serve when devices are in low power mode for specific applications '
                        'connecting test mode eDSP')
    @pytest.mark.parametrize('apps', block_low_power_mode_apps)
    def test_block_vungle_mraid_edsp_02(self, apps):
        req = request_payload.jaeger_v5_ios(apps[0], apps[1], ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_mraid))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(1813))
        assert_that(ad_markup['info'], equal_to('publisher battery saver mode not support'))

    @allure.feature('vungle mraid')
    @allure.tag('normal', 'v1.184.0')
    @allure.story('PBJ-3411 Block Vungle MRAID Ads for specific apps when devices are in low power mode')
    @allure.description('Verify it will not serve when devices are in low power mode for specific applications'
                        'connecting non test mode kraken')
    @pytest.mark.parametrize('apps', block_low_power_mode_apps)
    def test_block_vungle_mraid_02(self, apps):
        req = request_payload.jaeger_v5_ios(apps[0], apps[1], ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(1813))
        assert_that(ad_markup['info'], equal_to('publisher battery saver mode not support'))

    @allure.feature('vungle mraid')
    @allure.tag('normal', 'v1.184.0', 'test_mode')
    @allure.story('PBJ-3411 Block Vungle MRAID Ads for specific apps when devices are in low power mode')
    @allure.description('Verify it will not serve when devices are in low power mode for specific applications'
                        'connecting test mode kraken')
    @pytest.mark.parametrize('apps', block_low_power_mode_apps)
    def test_block_vungle_mraid_03(self, apps):
        req = request_payload.jaeger_v5_ios(apps[0], apps[1], ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(1813))
        assert_that(ad_markup['info'], equal_to('publisher battery saver mode not support'))

    @allure.feature('vungle mraid')
    @allure.tag('normal', 'v1.184.0')
    @allure.story('PBJ-3411 Block Vungle MRAID Ads for specific apps when devices are in low power mode')
    @allure.description('Verify it will not serve when devices are not in low power mode for specific applications'
                        'connecting meister')
    @pytest.mark.parametrize('apps', block_low_power_mode_apps)
    def test_block_vungle_mraid_04(self, apps):
        req = request_payload.jaeger_v5_ios(apps[0], apps[1], ifa=gen_device_id(), battery_saver_enabled=0)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        if "sleep" in ad_markup:
            assert_that(ad_markup['sleep'], not equal_to(1813))
            assert_that(ad_markup['info'] is not 'publisher battery saver mode not support')

    @allure.feature('vungle mraid')
    @allure.tag('normal', 'v1.184.0')
    @allure.story('PBJ-3411 Block Vungle MRAID Ads for specific apps when devices are in low power mode')
    @allure.description('Verify it will not serve when devices are not in low power mode for specific applications'
                        'connecting non test mode kraken')
    @pytest.mark.parametrize('apps', block_low_power_mode_apps)
    def test_block_vungle_mraid_05(self, apps):
        req = request_payload.jaeger_v5_ios(apps[0], apps[1], ifa=gen_device_id(), battery_saver_enabled=0)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        if "sleep" in ad_markup:
            assert_that(ad_markup['sleep'], not equal_to(1813))
            assert_that(ad_markup['info'] is not 'publisher battery saver mode not support')

    @allure.feature('vungle mraid')
    @allure.tag('normal', 'v1.184.0', 'test_mode')
    @allure.story('PBJ-3411 Block Vungle MRAID Ads for specific apps when devices are in low power mode')
    @allure.description('Verify it will not serve when devices are not in low power mode for specific applications'
                        'connecting test mode kraken')
    @pytest.mark.parametrize('apps', block_low_power_mode_apps)
    def test_block_vungle_mraid_06(self, apps):
        req = request_payload.jaeger_v5_ios(apps[0], apps[1], ifa=test_mode_device_id, battery_saver_enabled=0)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        if "sleep" in ad_markup:
            assert_that(ad_markup['sleep'], not equal_to(1813))
            assert_that(ad_markup['info'] is not 'publisher battery saver mode not support')

    # @allure.feature('ios15 block apps')
    # @allure.tag('normal', 'v1.186.1', 'test_mode')
    # @allure.story('PBJ-3490 Stop serving ads to iOS 15 on the following apps with these criteria')
    # @allure.description('Verify jaeger will not serve for some apps on ios 15')
    # @pytest.mark.parametrize('apps', block_ios_15_apps)
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    # def test_block_apps_with_ios15_1(self, apps, sdk_v):
    #     req = request_payload.jaeger_v5_ios(apps['pub_app'], apps['placement'], ifa=test_mode_device_id,
    #                                         os_version='15')
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids, sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_that(ad_markup['sleep'], equal_to(86405))
    #     assert_that(ad_markup['info'], equal_to('block app because of SDK incompatible with OS'))
    #
    # @allure.feature('ios15 block apps')
    # @allure.tag('normal', 'v1.186.1')
    # @allure.story('PBJ-3490 Stop serving ads to iOS 15 on the following apps with these criteria')
    # @allure.description('Verify jaeger will not serve for some apps on ios 15 for non test mode edsp')
    # @pytest.mark.parametrize('apps', block_ios_15_apps)
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    # def test_block_apps_with_ios15_2(self, apps, sdk_v):
    #     req = request_payload.jaeger_v5_ios(apps['pub_app'], apps['placement'], ifa=gen_device_id(),
    #                                         os_version='15')
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_that(ad_markup['sleep'], equal_to(86405))
    #     assert_that(ad_markup['info'], equal_to('block app because of SDK incompatible with OS'))
    #
    # @allure.feature('ios15 block apps')
    # @allure.tag('normal', 'v1.186.1')
    # @allure.story('PBJ-3490 Stop serving ads to iOS 15 on the following apps with these criteria')
    # @allure.description('Verify jaeger will  serve for some apps on ios 15 but sdk version is not 6.10.1 or 6.10.2')
    # @pytest.mark.parametrize('apps', block_ios_15_apps)
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.1'])
    # def test_block_apps_with_ios15_3(self, apps, sdk_v):
    #     req = request_payload.jaeger_v5_ios(apps['pub_app'], apps['placement'], ifa=gen_device_id(),
    #                                         os_version='15')
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     if 'sleep' in ad_markup:
    #         assert_that(ad_markup['sleep'], is_not(86405))
    #
    # @allure.feature('ios15 block apps')
    # @allure.tag('normal', 'v1.186.1')
    # @allure.story('PBJ-3490 Stop serving ads to iOS 15 on the following apps with these criteria')
    # @allure.description('Verify jaeger will serve for some apps os version is not 15 '
    #                     'but sdk version is 6.10.1 or 6.10.2')
    # @pytest.mark.parametrize('apps', block_ios_15_apps)
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    # def test_block_apps_with_ios15_4(self, apps, sdk_v):
    #     req = request_payload.jaeger_v5_ios(apps['pub_app'], apps['placement'], ifa=gen_device_id(),
    #                                         os_version='13')
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     if 'sleep' in ad_markup:
    #         assert_that(ad_markup['sleep'], is_not(86405))

    # @allure.feature('ios15 block apps')
    # @allure.tag('normal', 'v1.193.0', 'test_mode')
    # @allure.story('PBJ-3611 Add the following SayGames app IDs to the filtering list on iOS15')
    # @allure.description('Verify Jaeger will not serve for the app in the provided saygames app list '
    #                     'for all SDK version on iOS 15 in test mode')
    # @pytest.mark.parametrize('pub_app_id', [block_ios_15_all_version_test_app])
    # @pytest.mark.parametrize('placement', [block_ios_15_all_version_test_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3'])
    # def test_block_apps_with_ios15_5(self, pub_app_id, placement, sdk_v):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version='15')
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids, sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_that(ad_markup['sleep'], equal_to(86405))
    #     assert_that(ad_markup['info'], equal_to('block app because of SDK incompatible with OS'))

    # @allure.feature('ios15 block apps')
    # @allure.tag('normal', 'v1.193.0')
    # @allure.story('PBJ-3611 Add the following SayGames app IDs to the filtering list on iOS15')
    # @allure.description('Verify Jaeger will not serve for the app in the provided saygames app list '
    #                     'for all SDK version on iOS 15')
    # @pytest.mark.parametrize('pub_app_id', [block_ios_15_all_version_test_app])
    # @pytest.mark.parametrize('placement', [block_ios_15_all_version_test_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3'])
    # def test_block_apps_with_ios15_6(self, pub_app_id, placement, sdk_v):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version='15')
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids, sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_that(ad_markup['sleep'], equal_to(86405))
    #     assert_that(ad_markup['info'], equal_to('block app because of SDK incompatible with OS'))

    @allure.feature('ios15 block apps')
    @allure.tag('normal', 'v1.193.0', 'test_mode')
    @allure.story('PBJ-3611 Add the following SayGames app IDs to the filtering list on iOS15')
    @allure.description('Verify Jaeger will serve for the app in the provided saygames app list '
                        'for all SDK version if iOS version is not 15 in test mode')
    @pytest.mark.parametrize('pub_app_id', [block_ios_15_all_version_test_app])
    @pytest.mark.parametrize('placement', [block_ios_15_all_version_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3'])
    def test_block_apps_with_ios15_7(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version='14')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids, sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' in ad_markup:
            assert_that(ad_markup['sleep'], is_not(86405))

    @allure.feature('ios15 block apps')
    @allure.tag('normal', 'v1.193.0')
    @allure.story('PBJ-3611 Add the following SayGames app IDs to the filtering list on iOS15')
    @allure.description('Verify Jaeger will serve for the app in the provided saygames app list '
                        'for all SDK version if iOS version is not 15')
    @pytest.mark.parametrize('pub_app_id', [block_ios_15_all_version_test_app])
    @pytest.mark.parametrize('placement', [block_ios_15_all_version_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3'])
    def test_block_apps_with_ios15_8(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version='14')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids, sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' in ad_markup:
            assert_that(ad_markup['sleep'], is_not(86405))

    # @allure.feature('ios15 block apps')
    # @allure.tag('normal', 'v1.193.0', 'test_mode')
    # @allure.story('PBJ-3611 Add the following SayGames app IDs to the filtering list on iOS15')
    # @allure.description('Verify Jaeger will not serve for the app in both the provided saygames app list and the block '
    #                     'app list for all SDK version on iOS 15 in test mode')
    # @pytest.mark.parametrize('pub_app_id', [block_ios_15_conflict_test_app])
    # @pytest.mark.parametrize('placement', [block_ios_15_conflict_test_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.3'])
    # def test_block_apps_with_ios15_9(self, pub_app_id, placement, sdk_v):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version='15')
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids, sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_that(ad_markup['sleep'], equal_to(86405))
    #     assert_that(ad_markup['info'], equal_to('block app because of SDK incompatible with OS'))

    # @allure.feature('ios15 block apps')
    # @allure.tag('normal', 'v1.193.0')
    # @allure.story('PBJ-3611 Add the following SayGames app IDs to the filtering list on iOS15')
    # @allure.description('Verify Jaeger will not serve for the app in both the provided saygames app list and the block '
    #                     'app list for all SDK version on iOS 15')
    # @pytest.mark.parametrize('pub_app_id', [block_ios_15_conflict_test_app])
    # @pytest.mark.parametrize('placement', [block_ios_15_conflict_test_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.3'])
    # def test_block_apps_with_ios15_10(self, pub_app_id, placement, sdk_v):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version='15')
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids, sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_that(ad_markup['sleep'], equal_to(86405))
    #     assert_that(ad_markup['info'], equal_to('block app because of SDK incompatible with OS'))

    @allure.feature('ios15 block apps')
    @allure.tag('normal', 'v1.193.0', 'test_mode')
    @allure.story('PBJ-3611 Add the following SayGames app IDs to the filtering list on iOS15')
    @allure.description('Verify Jaeger will serve for the app in both the provided saygames app list and the block '
                        'app list for all SDK version is not iOS 15 in test mode')
    @pytest.mark.parametrize('pub_app_id', [block_ios_15_conflict_test_app])
    @pytest.mark.parametrize('placement', [block_ios_15_conflict_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3'])
    def test_block_apps_with_ios15_11(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version='14')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids, sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' in ad_markup:
            assert_that(ad_markup['sleep'], is_not(86405))

    @allure.feature('ios15 block apps')
    @allure.tag('normal', 'v1.193.0')
    @allure.story('PBJ-3611 Add the following SayGames app IDs to the filtering list on iOS15')
    @allure.description('Verify Jaeger will serve for the app in both the provided saygames app list and the block '
                        'app list for all SDK version is not iOS 15')
    @pytest.mark.parametrize('pub_app_id', [block_ios_15_conflict_test_app])
    @pytest.mark.parametrize('placement', [block_ios_15_conflict_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.10.3'])
    def test_block_apps_with_ios15_12(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version='14')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids, sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' in ad_markup:
            assert_that(ad_markup['sleep'], is_not(86405))

    @allure.feature('sleep code')
    @allure.tag('normal')
    @allure.story('PBJ-3429 Sort out Jaeger Sleepcode')
    @allure.description('Verify the sleep code of SleepCodeDeviceNotWifi')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026c3'])  # connection type only wifi
    @pytest.mark.parametrize('placement', ['DEFAULT02021c3'])
    def test_new_sleep_code_302(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), device_connection_type='4g')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(302))
        assert_that(ad_markup['info'], equal_to('device not on WiFi'))

    @allure.feature('basic')
    @allure.story('PBJ-3578 All invalid AdSize of banner are output as fullscreen to log.')
    @allure.description('Verify jaeger will not serve for ad size is null')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_banner_placement])
    def test_ad_size_is_null(self, pub_app_id, placement):
        """

             Banner size: ''
        """
        rtb = test_mode_kraken_rtb_ids_banner_xapi
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            banner=True, banner_type=" ")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(86401))
        assert_that(ad_markup['info'], equal_to('malformed payload'))

    @allure.feature('basic')
    @allure.story('PBJ-3578 All invalid AdSize of banner are output as fullscreen to log.')
    @allure.description('Verify jaeger will not serve for ad size is invalid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_banner_placement])
    def test_ad_size_is_invalid(self, pub_app_id, placement):
        """

             Banner size: 'aas'
        """
        rtb = test_mode_kraken_rtb_ids_banner_xapi
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            banner=True, banner_type="aas")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['sleep'], equal_to(86401))
        assert_that(ad_markup['info'], equal_to('malformed payload'))

    @allure.feature('kraken support')
    @allure.tag('normal', 'test_mode', 'v1.193.0')
    @allure.severity('normal')
    @allure.story('PBJ-3576 The internal Kraken can not serve if the bid request imp contains both banner and video')
    @allure.description('Verify the internal Kraken can pass ad with third party playable placement '
                        'on the matched h and w in meta file for iOS')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_01])
    @pytest.mark.parametrize('ad_size', [default_ios_test_ad_size])
    def test_kraken_meta_update_1(self, pub_app_id, placement, ad_size):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            h=ad_size['h'], w=ad_size['w'])
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('impression auctioned but unsold'))

    @allure.feature('kraken support')
    @allure.tag('normal', 'test_mode', 'v1.193.0')
    @allure.severity('normal')
    @allure.story('PBJ-3576 The internal Kraken can not serve if the bid request imp contains both banner and video')
    @allure.description('Verify the internal Kraken can only return mraid video with third party playable placement '
                        'on the non-matched h and w in meta file for iOS')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_01])
    @pytest.mark.parametrize('ad_size', [default_android_test_ad_size,
                                         default_windows_test_ad_size,
                                         {"h": 1000, "w": 500}])
    def test_kraken_meta_update_2(self, pub_app_id, placement, ad_size):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            h=ad_size['h'], w=ad_size['w'])
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('impression auctioned but unsold'))

    @allure.feature('kraken support')
    @allure.tag('normal', 'test_mode', 'v1.193.0')
    @allure.severity('normal')
    @allure.story('PBJ-3576 The internal Kraken can not serve if the bid request imp contains both banner and video')
    @allure.description('Verify the internal Kraken can pass ad with non third party playable placement '
                        'on the non-matched h and w in meta file for iOS')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ad_size', [default_android_test_ad_size,
                                         default_windows_test_ad_size,
                                         {"h": 1000, "w": 500}])
    def test_kraken_meta_update_3(self, pub_app_id, placement, ad_size):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            h=ad_size['h'], w=ad_size['w'])
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('impression auctioned but unsold'))

    @allure.feature('kraken support')
    @allure.tag('normal', 'test_mode', 'v1.193.0')
    @allure.severity('normal')
    @allure.story('PBJ-3576 The internal Kraken can not serve if the bid request imp contains both banner and video')
    @allure.description('Verify the internal Kraken can pass ad with third party playable placement '
                        'on the matched h and w in meta file for Android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_third_party_placement])
    @pytest.mark.parametrize('ad_size', [default_android_test_ad_size])
    def test_kraken_meta_update_4(self, pub_app_id, placement, ad_size):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                header_bidding=True, h=ad_size['h'], w=ad_size['w'])
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('impression auctioned but unsold'))

    @allure.feature('kraken support')
    @allure.tag('normal', 'test_mode', 'v1.193.0')
    @allure.severity('normal')
    @allure.story('PBJ-3576 The internal Kraken can not serve if the bid request imp contains both banner and video')
    @allure.description('Verify the internal Kraken can  pass ad with third party playable placement '
                        'on the non-matched h and w in meta file for Android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_third_party_placement])
    @pytest.mark.parametrize('ad_size', [default_ios_test_ad_size,
                                         default_windows_test_ad_size,
                                         {"h": 1000, "w": 500}])
    def test_kraken_meta_update_5(self, pub_app_id, placement, ad_size):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                header_bidding=True, h=ad_size['h'], w=ad_size['w'])
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('impression auctioned but unsold'))

    @allure.feature('kraken support')
    @allure.tag('normal', 'test_mode', 'v1.193.0')
    @allure.severity('normal')
    @allure.story('PBJ-3576 The internal Kraken can not serve if the bid request imp contains both banner and video')
    @allure.description('Verify the internal Kraken can pass ad with non third party playable placement '
                        'on the non-matched h and w in meta file for Android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('ad_size', [default_ios_test_ad_size,
                                         default_windows_test_ad_size,
                                         {"h": 1000, "w": 500}])
    def test_kraken_meta_update_6(self, pub_app_id, placement, ad_size):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                header_bidding=True, h=ad_size['h'], w=ad_size['w'])
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('impression auctioned but unsold'))

    @allure.feature('kraken support')
    @allure.tag('normal', 'test_mode', 'v1.193.0')
    @allure.severity('normal')
    @allure.story('PBJ-3576 The internal Kraken can not serve if the bid request imp contains both banner and video')
    @allure.description('Verify the internal Kraken can pass ad with third party playable placement '
                        'on the matched h and w in meta file for Windows')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_third_party_placement])
    @pytest.mark.parametrize('ad_size', [default_windows_test_ad_size])
    def test_kraken_meta_update_7(self, pub_app_id, placement, ad_size):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ashwid=test_mode_device_id, header_bidding=True,
                                                h=ad_size['h'], w=ad_size['w'])
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('impression auctioned but unsold'))

    @allure.feature('kraken support')
    @allure.tag('normal', 'test_mode', 'v1.193.0')
    @allure.severity('normal')
    @allure.story('PBJ-3576 The internal Kraken can not serve if the bid request imp contains both banner and video')
    @allure.description('Verify the internal Kraken can pass ad with third party playable placement '
                        'on the non-matched h and w in meta file for Windows')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_third_party_placement])
    @pytest.mark.parametrize('ad_size', [default_ios_test_ad_size,
                                         default_android_test_ad_size,
                                         {"h": 1000, "w": 500}])
    def test_kraken_meta_update_8(self, pub_app_id, placement, ad_size):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ashwid=test_mode_device_id, header_bidding=True,
                                                h=ad_size['h'], w=ad_size['w'])
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('impression auctioned but unsold'))

    @allure.feature('kraken support')
    @allure.tag('normal', 'test_mode', 'v1.193.0')
    @allure.severity('normal')
    @allure.story('PBJ-3576 The internal Kraken can not serve if the bid request imp contains both banner and video')
    @allure.description('Verify the internal Kraken can pass ad with non third party playable placement '
                        'on the non-matched h and w in meta file for Windows')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    @pytest.mark.parametrize('ad_size', [default_ios_test_ad_size,
                                         default_android_test_ad_size,
                                         {"h": 1000, "w": 500}])
    def test_kraken_meta_update_9(self, pub_app_id, placement, ad_size):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ashwid=test_mode_device_id, header_bidding=True,
                                                h=ad_size['h'], w=ad_size['w'])
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], not equal_to('impression auctioned but unsold'))

    @allure.feature('test ads')
    @allure.tag('normal')
    @allure.severity('normal')
    @allure.story('PBJ-3791 add test devices status to allow the user enable/disable the test devices')
    @allure.description('Verify jaeger return test ads for all test devices when enable the test device')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_enable_test_devices(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False,
                                            )
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        campaign = ad_markup['campaign']
        assert_that('test-ads' in campaign)

    @allure.feature('test ads')
    @allure.tag('normal')
    @allure.severity('normal')
    @allure.story('PBJ-3791 add test devices status to allow the user enable/disable the test devices')
    @allure.description('Verify jaeger not return test ads for test devices when disable the test device')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_3])
    @pytest.mark.parametrize('placement', [common_test_placement_3])
    def test_disable_test_devices_for_test_mode(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False,
                                            )
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that('sleep' in ad_markup)

    @allure.feature('test ads')
    @allure.tag('normal')
    @allure.severity('normal')
    @allure.story('PBJ-3791 add test devices status to allow the user enable/disable the test devices')
    @allure.description('Verify jaeger server for meister when disable the test device')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_3])
    @pytest.mark.parametrize('placement', [common_test_placement_3])
    def test_disable_test_devices_for_meister(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False,
                                            )
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that('sleep' not in ad_markup)

    @allure.feature('test ads')
    @allure.tag('normal')
    @allure.severity('normal')
    @allure.story('PBJ-3791 add test devices status to allow the user enable/disable the test devices')
    @allure.description('Verify jaeger return test ads for test mode app when disable the test device')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_4])
    @pytest.mark.parametrize('placement', [common_test_placement_4])
    def test_disable_test_devices_for_test_mode_01(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False,
                                            )
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        campaign = ad_markup['campaign']
        assert_that('test-ads' in campaign)

    @allure.feature('test ads')
    @allure.tag('normal')
    @allure.severity('normal')
    @allure.story('PBJ-3791 add test devices status to allow the user enable/disable the test devices')
    @allure.description('Verify jaeger return test ads for test mode app when enable the test device')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_5])
    @pytest.mark.parametrize('placement', [common_test_placement_5])
    def test_enable_test_devices_for_test_mode_01(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False,
                                            )
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        campaign = ad_markup['campaign']
        assert_that('test-ads' in campaign)

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation')
    @allure.description('Verify jaeger will server when rtb setting match bid request for eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_01(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": true,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":true,
            "ccpa": true,
            "coppa": true,
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), gdpr='opted_out',
                                            ccpa='opted_out'
                                            )
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_01,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['regs']['coppa'], equal_to(1))
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to("1-Y-"))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation')
    @allure.description('Verify filter out rtb when allow platform android is false for eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_prefiltering_rtb_match_02(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": true,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":true,
            "ccpa": true,
            "coppa": true,
        }
        """
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id(), gdpr='opted_out',
                                                ccpa='opted_out'
                                                )
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_01,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'info')
        assert_that(ad_markup['info'], 'no eligible RTB connections')

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation')
    @allure.description('Verify that allow_regulation_optout will not affect optedin traffic for eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_03(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": true,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":true,
            "ccpa": true,
            "coppa": true,
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), gdpr='opted_in',
                                            ccpa='opted_in'
                                            )
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_01,
                                          debug='jaeger'))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['regs']['coppa'], equal_to(1))
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to("1-N-"))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation')
    @allure.description('Verify jaeger serve when  allow regulation optout  for all privacy'
                        'in bid request for eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_04(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": true,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":true,
            "ccpa": true,
            "coppa": true,
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), gdpr='opted_in',
                                            )
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_01,
                                          debug='jaeger'))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['regs']['coppa'], equal_to(1))
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to("1---"))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation')
    @allure.description('Verify filter out rtb when rtb allow platform for ios is false for eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_05(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": false,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":true,
            "ccpa": true,
            "coppa": true,
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), gdpr='opted_out',
                                            ccpa='opted_out'
                                            )
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_02,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'info')
        assert_that(ad_markup['info'], 'no eligible RTB connections')

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation')
    @allure.description('Verify filter out rtb when rtb allow regulation optout of gdpr if false'
                        'for eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_06(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": true,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":false,
            "ccpa": true,
            "coppa": true,
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), gdpr='opted_out',
                                            ccpa='opted_in'
                                            )
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_03,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'info')
        assert_that(ad_markup['info'], 'no eligible RTB connections')

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation')
    @allure.description(
        'Verify jaeger will not server when rtb setting match bid request but lmt is not match for eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_07(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": true,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":true,
            "ccpa": true,
            "coppa": true,
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa='00000000-0000-0000-0000-000000000000',
                                            gdpr='opted_out', ccpa='opted_out'
                                            , lmt=1)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_01,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'info')

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation')
    @allure.description('Verify jaeger will  server when rtb setting match bid request and lmt is  match for eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_8(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": true,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":true,
            "ccpa": true,
            "coppa": true,
        }
        "block_consent_optout": false
        "allow_lat": false
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), gdpr='opted_out',
                                            ccpa='opted_out'
                                            )
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_04,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['device']['lmt'], equal_to(0))
        assert_that(bid_request['regs']['coppa'], equal_to(1))
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to("1-Y-"))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation'
                  'PBJ-3861 Jaeger - Add log for RTB connection filters if it fail')
    @allure.description(
        'Verify jaeger will not server when rtb setting match bid request but lmt is not match for eDSP'
        'Verify the log for RTB connection filter failed is added')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_9(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": true,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":true,
            "ccpa": true,
            "coppa": true,
        }
        "block_consent_optout": false
        "allow_lat": false
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa='00000000-0000-0000-0000-000000000000',
                                            gdpr='opted_out', ccpa='opted_out'
                                            , lmt=1)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_04,

                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        debug = response_payload['ext']['debug']
        assert_keys_exist(ad_markup, 'info')
        assert_that(ad_markup['info'], 'no eligible RTB connections')
        assert_keys_exist(debug, 'rtb_failed_filters')

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation')
    @allure.description('Verify jaeger will server when rtb setting match bid request but lmt is match for eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_10(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": true,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":true,
            "ccpa": true,
            "coppa": true,
        }
        "block_consent_optout": false
        "allow_lat": true
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa='00000000-0000-0000-0000-000000000000',
                                            gdpr='opted_out', ccpa='opted_out'
                                            , lmt=1)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_05,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['device']['lmt'], equal_to(1))
        assert_that(bid_request['regs']['coppa'], equal_to(1))
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to("1-Y-"))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3816 PreFiltering Implementation')
    @allure.description(
        'Verify the value of allow_lat will not influence traffic when lmt=0 in bid request for eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_11(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_platform": {
            "ios": true,
            "android": false,
            "windows": true,
            "amazon": true
        }
        "allow_regulation_optout":{
            "gdpr":true,
            "ccpa": true,
            "coppa": true,
        }
        "block_consent_optout": false
        "allow_lat": true
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), gdpr='opted_out',
                                            ccpa='opted_out'
                                            )
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_05,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify request with banner size "300x50", "320x50" for banner placement '
                        'will pass to downstreams')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('banner_size', ["banner", "banner_short"])
    def test_prefiltering_rtb_match_ad_size_01(self, pub_app_id, placement, banner_size):
        """
        rtb setting in DB
        "allow_banner_size":{
                "300x50":true,
                "320x50":true,
                "728x90":false,
                "300x250":true (this only for mrec)
              }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner_type=banner_size,
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_06,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify request with banner size "728x90" for banner placement will not pass to downstreams')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('banner_size', ["banner_leaderboard"])
    def test_prefiltering_rtb_match_ad_size_02(self, pub_app_id, placement, banner_size):
        """
        rtb setting in DB
        "allow_banner_size":{
                "300x50":true,
                "320x50":true,
                "728x90":false,
                "300x250":true (this only for mrec)
              }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True,
                                            banner_type=banner_size)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_06,
                                          debug='jaeger'))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['info'], 'no eligible RTB connections')
        assert_keys_exist(debug, 'rtb_failed_filters')
        assert_that(debug['rtb_failed_filters'][ext1_non_test_mode_kraken_rtb_prefiltering_06],
                    equal_to('adSizeFilter'))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify request with mrec placement will pass to downstreams')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement, common_test_video_mrec_placement])
    def test_prefiltering_rtb_match_ad_size_03(self, pub_app_id, placement):
        """
        rtb setting in DB
        "allow_banner_size":{
                "300x50":true,
                "320x50":true,
                "728x90":false,
                "300x250":true (this only for mrec)
              }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_06,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify will filter out traffic in case of bid floor>db country level setting.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_bid_floor_01(self, pub_app_id, placement):
        """
        rtb setting in DB
       "block_bid_floor":{
                "global":2.3,
                "by_country":{
                    "JP":2.4,
                    "DE":4
                    }
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_07,
                                          debug='jaeger'))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['info'], 'no eligible RTB connections')
        assert_keys_exist(debug, 'rtb_failed_filters')
        assert_that(debug['rtb_failed_filters'][ext1_non_test_mode_kraken_rtb_prefiltering_07],
                    equal_to('bidFloorFilter'))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify will pass the traffic in case of bid floor< db country level setting.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_prefiltering_rtb_match_bid_floor_02(self, pub_app_id, placement):
        """
        rtb setting in DB
       "block_bid_floor":{
                "global":2.3,
                "by_country":{
                    "JP":2.4,
                    "DE":4
                    }
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True,
                                            banner_type='banner')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_07,
                                          debug='jaeger'))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['info'], 'no eligible RTB connections')
        assert_keys_exist(debug, 'rtb_failed_filters')
        assert_that(debug['rtb_failed_filters'][ext1_non_test_mode_kraken_rtb_prefiltering_07],
                    equal_to('bidFloorFilter'))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify will deny the traffic in case of bid floor > db global level setting.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_bid_floor_03(self, pub_app_id, placement):
        """
        rtb setting in DB
       "block_bid_floor":{
                "global":2.3,
                "by_country":{
                    "JP":2.4,
                    "DE":4
                    }
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_07,
                                          debug='jaeger'))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['info'], 'no eligible RTB connections')
        assert_keys_exist(debug, 'rtb_failed_filters')
        assert_that(debug['rtb_failed_filters'][ext1_non_test_mode_kraken_rtb_prefiltering_07],
                    equal_to('bidFloorFilter'))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify will pass the traffic in case of bid floor < db global level setting.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_bid_floor_04(self, pub_app_id, placement):
        """
        rtb setting in DB
       "block_bid_floor":{
                "global":2.3,
                "by_country":{
                    "JP":2.4,
                    "DE":4
                    }
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_07,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify will deny the traffic in case of bid floor = country level setting for gdpr traffic.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_bid_floor_05(self, pub_app_id, placement):
        """
        rtb setting in DB
       "block_bid_floor":{
                "global":2.3,
                "by_country":{
                    "JP":2.4,
                    "DE":4
                    }
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), gdpr='opted_out')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=de_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_07,
                                          debug='jaeger'))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['info'], 'no eligible RTB connections')
        assert_keys_exist(debug, 'rtb_failed_filters')
        assert_that(debug['rtb_failed_filters'][ext1_non_test_mode_kraken_rtb_prefiltering_07],
                    equal_to('bidFloorFilter'))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify will pass the traffic in case of bid floor < global level setting for gdpr traffic.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_prefiltering_rtb_match_bid_floor_06(self, pub_app_id, placement):
        """
        rtb setting in DB
       "block_bid_floor":{
                "global":2.3,
                "by_country":{
                    "JP":2.4,
                    "DE":4
                    }
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), gdpr='opted_out')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=it_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_07,
                                          debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description(
        'Verify will deny the traffic in case of, bid floor < country level setting, 728x90=false for banner.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_prefiltering_rtb_match_mixed_08(self, pub_app_id, placement):
        """
        rtb setting in DB
       "allow_banner_size":{
              "300x50":true,
              "728x90":false,
              "300x250":false(this only for mrec)
            }
        "block_bid_floor":{
          "by_country":{
            "US":1.1,
            "AU": 30
          }
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True,
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=us_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_08,
                                          debug='jaeger'))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['info'], 'no eligible RTB connections')
        assert_keys_exist(debug, 'rtb_failed_filters')
        assert_that(debug['rtb_failed_filters'][ext1_non_test_mode_kraken_rtb_prefiltering_08],
                    equal_to('adSizeFilter'))

    @allure.feature('PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description(
        'Verify will deny the traffic in case of, bid floor < country level setting, 300x50=true for banner.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_prefiltering_rtb_match_mixed_09(self, pub_app_id, placement):
        """
        rtb setting in DB
       "allow_banner_size":{
              "300x50":true,
              "728x90":false,
              "300x250":false(this only for mrec)
            }
        "block_bid_floor":{
          "by_country":{
            "US":1.1,
            "AU": 30
          }
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True,
                                            banner_type='banner_short',
                                            header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_prefiltering_08,
                                          debug='jaeger'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['info'], 'no eligible RTB connections')
        assert_keys_exist(debug, 'rtb_failed_filters')
        assert_that(debug['rtb_failed_filters'][ext1_non_test_mode_kraken_rtb_prefiltering_08],
                    equal_to('bidFloorFilter'))

    @allure.feature('no specify rtb')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify will not cause error for no specify rtb id for pre-filtering feature')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.3.2', 'Vungle/6.10.0', 'Vungle/6.11.0'])
    def test_no_specify_rtb_id_for_prefiltering_test_mode(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')

    @allure.feature('no specify rtb')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify will not cause error for no specify rtb id for pre-filtering feature')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.3.2', 'Vungle/6.10.0', 'Vungle/6.11.0'])
    def test_no_specify_rtb_id_for_prefiltering(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')

    @allure.feature('max duration')
    @allure.tag('normal', 'v1.204.0')
    @allure.severity('normal')
    @allure.story('PBJ-3940 Rollic - EDSP Not Adhering to Maximum "Ad Duration" within Vungle Dashboard'
                  'PBJ-4040 Rollic Video Duration Enforcement')
    @allure.description('Verify jaeger will not serve in case of the ad duration > max duration of app settup for '
                        'the Rollic Games')
    @pytest.mark.parametrize('pub_app_id', ['5c093376ee91e5216654a748'])
    @pytest.mark.parametrize('placement', ['DEFAULT-9905484'])
    def test_max_duration_filter_out_1(self, pub_app_id, placement):
        """
            App level setting: maxVideoLength = 45
            Ad duration: 46
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], equal_to('invalid VAST'))

    @allure.feature('max duration')
    @allure.tag('normal', 'v1.204.0')
    @allure.severity('normal')
    @allure.story('PBJ-3940 Rollic - EDSP Not Adhering to Maximum "Ad Duration" within Vungle Dashboard'
                  'PBJ-4040 Rollic Video Duration Enforcement')
    @allure.description('Verify jaeger will serve in case of the ad duration <= max duration of app settup for '
                        'the Rollic Games')
    @pytest.mark.parametrize('pub_app_id', ['5c13a451a8854a4206ff8ef7'])
    @pytest.mark.parametrize('placement', ['DEFAULT-6248310'])
    def test_max_duration_filter_out_2(self, pub_app_id, placement):
        """
            App level setting: maxVideoLength = 46
            Ad duration: 46
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('max duration')
    @allure.tag('normal', 'v1.204.0')
    @allure.severity('normal')
    @allure.story('PBJ-3940 Rollic - EDSP Not Adhering to Maximum "Ad Duration" within Vungle Dashboard'
                  'PBJ-4040 Rollic Video Duration Enforcement')
    @allure.description(
        'Verify jaeger will serve and log warning in case of the ad duration > max duration of app settup + 5s for '
        'the non Rollic Games')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b9'])
    @pytest.mark.parametrize('placement', ['DEFAULT02029'])
    def test_max_duration_filter_out_3(self, pub_app_id, placement):
        """
            App level setting: maxVideoLength = 40
            Ad duration: 46
        """

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('ppid')
    @allure.tag('normal')
    @allure.story('PBJ-3932 Support for App Store Custom Product Pages')
    @allure.description('Verify "custom_pord_page_id" field exists in ad response for test mode kraken on ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_custon_pord_page_id_1(self, pub_app_id, placement):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version='Vungle/6.11.0'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        callToActionDest = ad_markup['callToActionDest']
        ppid = callToActionDest[callToActionDest.find('ppid=') + 5:]
        assert_keys_exist(ad_markup, 'custom_prod_page_id')
        assert_that(ad_markup['custom_prod_page_id'], equal_to(ppid))

    @allure.feature('ppid')
    @allure.tag('normal')
    @allure.story('PBJ-3932 Support for App Store Custom Product Pages')
    @allure.description(
        'Verify "custom_pord_page_id" field exists in ad response for non test mode kraken on ios platform ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    def test_custon_pord_page_id_2(self, pub_app_id, placement):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version='Vungle/6.11.0'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        callToActionDest = ad_markup['callToActionDest']
        ppid = callToActionDest[callToActionDest.find('ppid=') + 5:]
        assert_keys_exist(ad_markup, 'custom_prod_page_id')
        assert_that(ad_markup['custom_prod_page_id'], equal_to(ppid))

    @allure.feature('ppid')
    @allure.tag('normal')
    @allure.story('PBJ-3932 Support for App Store Custom Product Pages')
    @allure.description(
        'Verify "custom_pord_page_id" field exists in ad response for test mode edsp on ios platform ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_custon_pord_page_id_3(self, pub_app_id, placement):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False,
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.11.0'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = response_payload['ads'][0]['ad_markup']['templateSettings']['normal_replacements']
        CTA_BUTTON_URL = normal_replacements['CTA_BUTTON_URL']
        ppid = CTA_BUTTON_URL[CTA_BUTTON_URL.find('ppid=') + 5:]
        assert_keys_exist(ad_markup, 'custom_prod_page_id')
        assert_that(ad_markup['custom_prod_page_id'], equal_to(ppid))

    @allure.feature('ppid')
    @allure.tag('normal', 'v1.237.0')
    @allure.story('PBJ-4683 Support CPP(custom product page) for eDSP partners')
    @allure.description('Verify ppid read from bid_response.ext.skadn.cpp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_custom_pord_page_id_e_01(self, pub_app_id, placement, rtb):
        override_bid_response_cpp = 'seatbid.0.bid.0.ext.skadn.cpp@"external_cpp_01"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb,
                                          sdk_version='Vungle/6.11.0',
                                          override_bid_response_any=override_bid_response_cpp,
                                          debug='jaeger'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'custom_prod_page_id')
        assert_that(ad_markup['custom_prod_page_id'], equal_to("external_cpp_01"))

    @allure.feature('ppid')
    @allure.tag('normal', 'v1.237.0')
    @allure.story('PBJ-4683 Support CPP(custom product page) for eDSP partners')
    @allure.description('Verify ppid read from bid_response.ext.skadn.cpp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_custom_pord_page_id_e_02(self, pub_app_id, placement, rtb):
        override_bid_response_cpp = 'seatbid.0.bid.0.ext.skadn.cpp@"external_cpp_banner"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb,
                                          sdk_version='Vungle/6.11.0',
                                          override_bid_response_any=override_bid_response_cpp,
                                          debug='jaeger'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'custom_prod_page_id')
        assert_that(ad_markup['custom_prod_page_id'], equal_to("external_cpp_banner"))

    @allure.feature('ppid')
    @allure.tag('normal', 'v1.237.0')
    @allure.story('PBJ-4683 Support CPP(custom product page) for eDSP partners')
    @allure.description('Verify ppid read from bid_response.ext.skadn.cpp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_playable_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_custom_pord_page_id_e_03(self, pub_app_id, placement, rtb):
        override_bid_response_cpp = 'seatbid.0.bid.0.ext.skadn.cpp@"external_cpp_playable"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb,
                                          sdk_version='Vungle/6.11.0',
                                          override_bid_response_any=override_bid_response_cpp,
                                          debug='jaeger'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'custom_prod_page_id')
        assert_that(ad_markup['custom_prod_page_id'], equal_to("external_cpp_playable"))

    @allure.feature('ppid')
    @allure.tag('normal', 'v1.237.0')
    @allure.story('PBJ-4683 Support CPP(custom product page) for eDSP partners')
    @allure.description('Verify ppid read from bid_response.ext.skadn.cpp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_custom_pord_page_id_e_04(self, pub_app_id, placement, rtb):
        override_bid_response_cpp = 'seatbid.0.bid.0.ext.skadn.cpp@"external_cpp_native"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=us_ip, rtb_selector=rtb,
                                          sdk_version='Vungle/6.11.0',
                                          override_bid_response_any=override_bid_response_cpp,
                                          debug='jaeger'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'custom_prod_page_id')
        assert_that(ad_markup['custom_prod_page_id'], equal_to("external_cpp_native"))

    @allure.feature('ppid')
    @allure.tag('normal', 'v1.237.0')
    @allure.story('PBJ-4683 Support CPP(custom product page) for eDSP partners')
    @allure.description('Verify ppid read from bid_response.ext.skadn.cpp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    def test_custom_pord_page_id_e_05(self, pub_app_id, placement):
        override_bid_response_cpp = 'seatbid.0.bid.0.ext.skadn.cpp@""'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.11.0',
                                          override_bid_response_any=override_bid_response_cpp,
                                          debug='jaeger'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'custom_prod_page_id')

    @allure.feature('ppid')
    @allure.tag('normal', 'test_mode', 'v1.237.0')
    @allure.story('PBJ-4683 Support CPP(custom product page) for eDSP partners')
    @allure.description('Verify ppid read from bid_response.ext.skadn.cpp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_test_mode_kraken_rtb_ids_vast, test_mode_kraken_rtb_ids])
    def test_custom_pord_page_id_e_06(self, pub_app_id, placement, rtb):
        override_bid_response_cpp = 'seatbid.0.bid.0.ext.skadn.cpp@"external_cpp_test_mode"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=us_ip, rtb_selector=rtb,
                                          sdk_version='Vungle/6.11.0',
                                          override_bid_response_any=override_bid_response_cpp,
                                          debug='jaeger'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'custom_prod_page_id')
        assert_that(ad_markup['custom_prod_page_id'], equal_to("external_cpp_test_mode"))

    @allure.feature('ad markup')
    @allure.tag('normal')
    @allure.story('PBJ-3974 Add APP_STORE_ID token for programmatic VAST responses')
    @allure.description('Verify APP_STORE_ID is added in token')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_app_store_id_added_in_token(self, pub_app_id, placement):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, 'APP_STORE_ID')
        assert_that(normal_replacements['APP_STORE_ID'], equal_to('1490962424'))

    @allure.feature('expiry experiment')
    @allure.tag('normal', 'v1.121.0')
    @allure.story('PBJ-3950 Investigate Ad Cached Expired from 7 day -> 3 day')
    @allure.description('Verify the expiry time is 3 days for the non-hb traffic if placement in exp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_expiry_experiment_non_hb_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(3))

    @allure.feature('expiry experiment')
    @allure.tag('normal', 'v1.121.0', 'test_mode')
    @allure.story('PBJ-3950 Investigate Ad Cached Expired from 7 day -> 3 day')
    @allure.description('Verify the expiry time is 3 days for the non-hb traffic if placement in exp in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_expiry_experiment_non_hb_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(3))

    @allure.feature('expiry experiment')
    @allure.tag('normal', 'v1.121.0')
    @allure.story('PBJ-3950 Investigate Ad Cached Expired from 7 day -> 3 day')
    @allure.description('Verify the exp does not impact the placement that not enter exp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['AREYOUS82690'])
    def test_expiry_experiment_non_hb_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(1))

    @allure.feature('expiry experiment')
    @allure.tag('normal', 'v1.121.0', 'test_mode')
    @allure.story('PBJ-3950 Investigate Ad Cached Expired from 7 day -> 3 day')
    @allure.description('Verify the exp does not impact the placement that not enter exp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['AREYOUS82690'])
    def test_expiry_experiment_non_hb_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        expiry = datetime.fromtimestamp(ad_markup['expiry'])
        now = datetime.now()
        assert_that((expiry - now).days, less_than_or_equal_to(7))

    @allure.feature('ad markup')
    @allure.tag('normal')
    @allure.story('PBJ-4259 Fix Kraken bid.id')
    @allure.description('Verify bidresponse.bid.id in bid response = bidrequest.id ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_bid_id_e(self, pub_app_id, placement):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        bid_response = get_bid_response_obj_from_jaeger_explain(response_payload,
                                                                ext_non_test_mode_kraken_rtb_ids_vast)
        bid_id = bid_response['id']
        seat_id = bid_response['seatbid'][0]['bid'][0]['id']
        assert_that(bid_id, equal_to(seat_id))

    @allure.feature('ad markup')
    @allure.tag('normal')
    @allure.story('PBJ-4259 Fix Kraken bid.id')
    @allure.description('Verify bidresponse.bid.id in bid response = bidrequest.id ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_bid_id_i(self, pub_app_id, placement):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_int1_rtb_ids,
                                          debug='jaeger'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        bid_response = get_bid_response_obj_from_jaeger_explain(response_payload, non_test_mode_kraken_int1_rtb_ids)
        bid_id = bid_response['id']
        seat_id = bid_response['seatbid'][0]['bid'][0]['id']
        assert_that(bid_id, equal_to(seat_id))

    @allure.feature('ad markup')
    @allure.tag('normal')
    @allure.story('PBJ-4194 Add adSource in ads response for SDK 6.12+ to indicate the ad is from iDSP or eDSP')
    @allure.description('Verify adSource is added in ads response for idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0', 'Vungle/6.12.1'])
    def test_ad_source_i_01(self, pub_app_id, placement, sdk_v):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_int1_rtb_ids,
                                          debug='jaeger', sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'adSource')
        assert_that(ad_markup['adSource'], equal_to('idsp'))

    @allure.feature('ad markup')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4194 Add adSource in ads response for SDK 6.12+ to indicate the ad is from iDSP or eDSP')
    @allure.description('Verify adSource is added in ads response for idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0', 'Vungle/6.12.1'])
    def test_ad_source_i_t(self, pub_app_id, placement, sdk_v):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids,
                                          debug='jaeger', sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'adSource')
        assert_that(ad_markup['adSource'], equal_to('idsp'))

    @allure.feature('ad markup')
    @allure.tag('normal')
    @allure.story('PBJ-4194 Add adSource in ads response for SDK 6.12+ to indicate the ad is from iDSP or eDSP')
    @allure.description('Verify adSource is added in ads response for edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0', 'Vungle/6.12.1'])
    def test_ad_source_e_01(self, pub_app_id, placement, sdk_v):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger', sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'adSource')
        assert_that(ad_markup['adSource'], equal_to('edsp'))

    @allure.feature('ad markup')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4194 Add adSource in ads response for SDK 6.12+ to indicate the ad is from iDSP or eDSP')
    @allure.description('Verify adSource is added in ads response for edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0', 'Vungle/6.12.1'])
    def test_ad_source_e_t(self, pub_app_id, placement, sdk_v):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_mraid,
                                          debug='jaeger', sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'adSource')
        assert_that(ad_markup['adSource'], equal_to('edsp'))

    @allure.feature('ad markup')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4194 Add adSource in ads response for SDK 6.12+ to indicate the ad is from iDSP or eDSP')
    @allure.description('Verify no adSource in ads response below 6.12')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.6'])
    def test_no_ad_source_e_t(self, pub_app_id, placement, sdk_v):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_mraid,
                                          debug='jaeger', sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'adSource')

    @allure.feature('ad markup')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4194 Add adSource in ads response for SDK 6.12+ to indicate the ad is from iDSP or eDSP')
    @allure.description('Verify adSource is added in ads response for edsp via android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0', 'Vungle/6.12.1'])
    def test_ad_source_android(self, pub_app_id, placement, sdk_v):

        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_mraid,
                                          debug='jaeger', sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'adSource')
        assert_that(ad_markup['adSource'], equal_to('edsp'))

    @allure.feature('ad markup')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4497 Blocking RU + Ukraine traffic in King app')
    @allure.description('Verify this account will be blocked via RU adn Ukraine traffic')
    @pytest.mark.parametrize('pub_app_id', ['62df85659fa3e5efd7bf3f0e'])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [ru_ip, ua_ip])
    def test_block_country_for_king_app_1(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=ip, rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('sleep' in response_payload['ads'][0]['ad_markup'])

    @allure.feature('ad markup')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4497 Blocking RU + Ukraine traffic in King app')
    @allure.description('Verify this account will not be blocked via the other country traffic')
    @pytest.mark.parametrize('pub_app_id', ['62df85659fa3e5efd7bf3f0e'])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [au_ip])
    def test_block_country_for_king_app_2(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=ip, rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('sleep' not in response_payload['ads'][0]['ad_markup'])

    @allure.feature('block ads')
    @allure.tag('normal', 'v1.237.0', 'v1.240.0')
    @allure.story('PBJ-4728 (Playrix) Block ads in certain countries'
                  'PBJ-4811 (Playrix) Block ads in Belarus')
    @allure.description('Verify block ads for Russia & Ukraine for playrix')
    @pytest.mark.parametrize('pub_app_id', ['5767da97de4dacbc140000e7'])
    @pytest.mark.parametrize('placement', ['FD_IOS_DOUBLE-0549036'])
    @pytest.mark.parametrize('ip', [ru_ip, ua_ip, by_ip])
    def test_block_country_for_playrix_1(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(response_payload['ads'][0]['ad_markup'], 'sleep')

    @allure.feature('block ads')
    @allure.tag('normal', 'v1.237.0')
    @allure.story('PBJ-4728 (Playrix) Block ads in certain countries')
    @allure.description('Verify jaeger will serve ads for other counties for playrix')
    @pytest.mark.parametrize('pub_app_id', ['5767da97de4dacbc140000e7'])
    @pytest.mark.parametrize('placement', ['FD_IOS_DOUBLE-0549036'])
    @pytest.mark.parametrize('ip', [au_ip])
    def test_block_country_for_playrix_2(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(response_payload['ads'][0]['ad_markup'], 'sleep')

    @allure.feature('Block IPs')
    @allure.tag('normal', 'v1.260.0')
    @allure.story('PBJ-5070 Block Fraudulent IPs for Chartboost Connections'
                  'PBJ-5171 Additional Chartboost IPs to be Blocked'
                  'PBJ-5220 Make eDSP IP block configuration into MongoDB RBTConnetion Collection')
    @allure.description('Verify Fraudulent ips will be blocked for the specified rtb account'
                        'Verify that ip will be blocked based on config')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_block_ip_01])
    @pytest.mark.parametrize('block_ips', [fr_ip, "200.0.61.1", "200.0.61.16", "161.0.70.45", "161.0.70.0"])
    def test_block_chartboot_ips_01(self, pub_app_id, placement, rtb_ids, block_ips):
        """
        config in DB
        rtb account:
        block blocked_ips:["37.164.162.171"](FR_ip)
        blocked_sub_nets: ["200.0.61","161.0.70"]
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=block_ips, rtb_selector=rtb_ids,
                                          sdk_version=test_default_real_time_sdk_version,
                                           debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'sleep')
        debug = response_payload['ext']['debug']
        assert_that(debug['rtb_failed_filters'][ext1_non_test_mode_kraken_block_ip_01], equal_to('ipFilter'))


    @allure.feature('Block IPs')
    @allure.tag('normal', 'v1.260.0')
    @allure.story('PBJ-5070 Block Fraudulent IPs for Chartboost Connections'
                  'PBJ-5171 Additional Chartboost IPs to be Blocked'
                  'PBJ-5220 Make eDSP IP block configuration into MongoDB RBTConnetion Collection')
    @allure.description('Verify ips will not be blocked for other rtb account')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_ids', [ext_test_mode_kraken_rtb_ids_OSAPI])
    @pytest.mark.parametrize('block_ips', [fr_ip, "200.0.61.1", "200.0.61.16", "161.0.70.45", "161.0.70.0"])
    def test_block_chartboot_ips_02(self, pub_app_id, placement, rtb_ids, block_ips):
        """
              config in DB
              rtb  account:
              block blocked_ips:[]
              blocked_sub_nets: []
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=block_ips, rtb_selector=rtb_ids,
                                          sdk_version=test_default_real_time_sdk_version,
                                           ))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(ad_markup, 'sleep')


    @allure.feature('Block IPs')
    @allure.tag('normal', 'v1.260.0')
    @allure.story('PBJ-5070 Block Fraudulent IPs for Chartboost Connections'
                  'PBJ-5171 Additional Chartboost IPs to be Blocked'
                  'PBJ-5220 Make eDSP IP block configuration into MongoDB RBTConnetion Collection')
    @allure.description('Verify ips will not be blocked for other ips')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_block_ip_01])
    @pytest.mark.parametrize('block_ips', [au_ip])
    def test_block_chartboot_ips_03(self, pub_app_id, placement, rtb_ids, block_ips):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=block_ips, rtb_selector=rtb_ids,
                                          sdk_version=test_default_real_time_sdk_version,
                                           ))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(ad_markup, 'sleep')



    @allure.feature('real eDSP crid')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP to SDK')
    @allure.description('Verify pass real crid of edsp for non HB traffic via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_real_edsp_crid_t(self, pub_app_id, placement, sdk_v):
        """
        rtb_account_id: 5cd92b2661a35300113a8487
        """
        override_bidreponse_any = 'seatbid.0.bid.0.cid@"emilycid"|||seatbid.0.bid.0.crid@"emilycrid"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_mraid,
                                          debug='jaeger', sdk_version=sdk_v,
                                          override_bid_response_any=override_bidreponse_any))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        campaign = ad_markup['campaign']
        campaign_components = campaign.split('|')
        assert_that(campaign_components[0], equal_to('5cd92b2661a35300113a8487_emilycid'))
        assert_that(campaign_components[1], equal_to('5cd92b2661a35300113a8487_emilycrid'))
        # Verify transaction: winning_bid.cid=emilycid, winning_bid.crid=emilycrid

    @allure.feature('real eDSP crid')
    @allure.tag('normal')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP to SDK')
    @allure.description('Verify pass real crid of edsp for non HB traffic via non test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_real_edsp_crid_n_t(self, pub_app_id, placement, sdk_v):
        """

        rtb_account_id: 5cd92b2661a35300113a8487
        """
        override_bidreponse_any = 'seatbid.0.bid.0.cid@"emilycid"|||seatbid.0.bid.0.crid@"emilycrid"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger', sdk_version=sdk_v,
                                          override_bid_response_any=override_bidreponse_any))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        campaign = ad_markup['campaign']
        campaign_components = campaign.split('|')
        assert_that(campaign_components[0], equal_to('5cd92b2661a35300113a8487_emilycid'))
        assert_that(campaign_components[1], equal_to('5cd92b2661a35300113a8487_emilycrid'))
        # Verify transaction: winning_bid.cid=emilycid, winning_bid.crid=emilycrid

    @allure.feature('real eDSP crid')
    @allure.tag('normal')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP to SDK')
    @allure.description('Verify pass default crid of edsp for non HB traffic when edsp response null cid and crid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_real_edsp_crid_and_cid_null(self, pub_app_id, placement, sdk_v):
        """

              rtb_account_id: 5cd92b2661a35300113a8487
              default cid: 591007e887faec9f44000018
              default crid: 574351a9740cf4426b30d030
        """
        override_bid_response_any = 'seatbid.0.bid.0.cid@""|||seatbid.0.bid.0.crid@""'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger', sdk_version=sdk_v,
                                          override_bid_response_any=override_bid_response_any))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        campaign = ad_markup['campaign']
        campaign_components = campaign.split('|')
        assert_that(campaign_components[0], equal_to('5cd92b2661a35300113a8487_591007e887faec9f44000018'))
        assert_that(campaign_components[1], equal_to('5cd92b2661a35300113a8487_574351a9740cf4426b30d030'))
        # Verify transaction: no cid&crid

    @allure.feature('real eDSP crid')
    @allure.tag('normal')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP to SDK')
    @allure.description(
        'Verify pass default crid of edsp for non HB traffic when edsp response empty string cid and crid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_real_edsp_crid_and_cid_empty_str(self, pub_app_id, placement, sdk_v):
        """

              rtb_account_id: 5cd92b2661a35300113a8487
              default cid: 591007e887faec9f44000018
              default crid: 574351a9740cf4426b30d030
        """
        override_bid_response_any = 'seatbid.0.bid.0.cid@" "|||seatbid.0.bid.0.crid@" "'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger', sdk_version=sdk_v,
                                          override_bid_response_any=override_bid_response_any))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        campaign = ad_markup['campaign']
        campaign_components = campaign.split('|')
        assert_that(campaign_components[0], equal_to('5cd92b2661a35300113a8487_591007e887faec9f44000018'))
        assert_that(campaign_components[1], equal_to('5cd92b2661a35300113a8487_574351a9740cf4426b30d030'))
        # Verify transaction:  cid&crid =" "

    @allure.feature('real eDSP crid')
    @allure.tag('normal')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP to SDK')
    @allure.description('Verify the campaign in ads response will not be impacted for iDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_real_edsp_crid_meister(self, pub_app_id, placement, sdk_v):
        """
              cid: 5eb9877e136f432531e6f285
              crid: 5eb9a49a5ddc02539da7c732
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          debug='jaeger', sdk_version=sdk_v,
                                          ))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        campaign = ad_markup['campaign']
        campaign_components = campaign.split('|')
        assert_that("_" not in campaign_components[0])
        assert_that("_" not in campaign_components[1])

    @allure.feature('real eDSP crid')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP to SDK')
    @allure.description('Verify pass real crid of edsp for  HB traffic via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_real_edsp_crid_t_hb(self, pub_app_id, placement, sdk_v):
        """

        rtb_account_id: 5cd92b2661a35300113a8487
        """
        override_bidreponse_any = 'seatbid.0.bid.0.cid@"emilycid"|||seatbid.0.bid.0.crid@"emilycrid"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_mraid,
                                          debug='jaeger', sdk_version=sdk_v,
                                          override_bid_response_any=override_bidreponse_any))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_token = ad_markup['bid_token']
        dynamo_key = bid_token.split('|')[2]
        campaign = ad_markup['campaign']
        campaign_components = campaign.split('|')
        assert_that(campaign_components[0], equal_to('5cd92b2661a35300113a8487_emilycid'))
        assert_that(campaign_components[1], equal_to('5cd92b2661a35300113a8487_emilycrid'))
        # check crid and cid in dynamo DB
        checker = post(hbp_checker_qa % (dynamo_key, "bidinfo"), json="")
        checker_response = checker.json()[0]
        assert_that(checker_response['adv_cid'], equal_to('emilycid'))
        assert_that(checker_response['adv_crid'], equal_to('emilycrid'))

        # Verify transaction: winning_bid.cid=emilycid, winning_bid.crid=emilycrid

    @allure.feature('real eDSP crid')
    @allure.tag('normal')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP to SDK')
    @allure.description('Verify pass real crid of edsp for HB traffic via non test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_real_edsp_crid_n_t_hb(self, pub_app_id, placement, sdk_v):
        """

        rtb_account_id: 5cd92b2661a35300113a8487
        """
        override_bidreponse_any = 'seatbid.0.bid.0.cid@"emilycid"|||seatbid.0.bid.0.crid@"emilycrid"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger', sdk_version=sdk_v,
                                          override_bid_response_any=override_bidreponse_any))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        campaign = ad_markup['campaign']
        bid_token = ad_markup['bid_token']
        dynamo_key = bid_token.split('|')[2]
        campaign_components = campaign.split('|')
        assert_that(campaign_components[0], equal_to('5cd92b2661a35300113a8487_emilycid'))
        assert_that(campaign_components[1], equal_to('5cd92b2661a35300113a8487_emilycrid'))
        # check crid and cid in dynamo DB
        checker = post(hbp_checker_qa % (dynamo_key, "bidinfo"), json="")
        checker_response = checker.json()[0]
        assert_that(checker_response['adv_cid'], equal_to('emilycid'))
        assert_that(checker_response['adv_crid'], equal_to('emilycrid'))
        # Verify transaction: winning_bid.cid=emilycid, winning_bid.crid=emilycrid

    @allure.feature('real eDSP crid')
    @allure.tag('normal')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP to SDK')
    @allure.description('Verify pass default crid of edsp for HB traffic when edsp response null cid and crid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_real_edsp_crid_and_cid_null_hb(self, pub_app_id, placement, sdk_v):
        """

              rtb_account_id: 5cd92b2661a35300113a8487
              default cid: 591007e887faec9f44000018
              default crid: 574351a9740cf4426b30d030
        """
        override_bid_response_any = 'seatbid.0.bid.0.cid@""|||seatbid.0.bid.0.crid@""'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger', sdk_version=sdk_v,
                                          override_bid_response_any=override_bid_response_any))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_token = ad_markup['bid_token']
        dynamo_key = bid_token.split('|')[2]
        campaign = ad_markup['campaign']
        campaign_components = campaign.split('|')
        assert_that(campaign_components[0], equal_to('5cd92b2661a35300113a8487_591007e887faec9f44000018'))
        assert_that(campaign_components[1], equal_to('5cd92b2661a35300113a8487_574351a9740cf4426b30d030'))
        # check crid and cid in dynamo DB
        checker = post(hbp_checker_qa % (dynamo_key, "bidinfo"), json="")
        checker_response = checker.json()[0]
        assert_that(checker_response['adv_cid'], equal_to(''))
        assert_that(checker_response['adv_crid'], equal_to(''))

    @allure.feature('google api integration')
    @allure.tag('normal')
    @allure.description('Verify retry successfully process')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_admob_google_integration_creative_review_process_retry_01(self, pub_app_id, placement):
        pass
        '''
        Steps:
        1. Send admob head bidding request to jaeger auction. after it passed all bid filters,
           a. Validate 'send message to topic ex-jaeger-admob-creatives-20220818'.
           b. Validate 'record cr-rev-mk.<murmur3sum32 of ([rtbAccountID]_[creativeID]> with ttl 10min in redis.'
        2. Then check mock server has been submit the creative to google api to review.   
        3. Then go to s3 '(​​vungle2-ssp-dev/admobreview/creatives' to check whether the creative id recorded here.
        4. Cron job runs once every 30 minutes, to get the crid from s3 creative folder, then send it to 'adquality-admob-submitreview-list'.
           Validate 'adquality-admob-submitreview-list' has the creative ids.
        5. Admobreviewservice get the review result throug consumer 'adquality-admob-submitreview-list'.
           set the response result = [],
           a. Validate the crid will store in s3 creative  with retry:true flag.
           b. Waitting for the next process. Then set the result to 'APPROVED'.
           c. Validate the process finish.
             
        '''

    @allure.feature('google api integration')
    @allure.tag('normal')
    @allure.description('Verify retry failed process')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_admob_google_integration_creative_review_process_retry_02(self, pub_app_id, placement):
        pass
        '''
        Steps:
        1. Send admob head bidding request to jaeger auction. after it passed all bid filters,
           a. Validate 'send message to topic ex-jaeger-admob-creatives-20220818'.
           b. Validate 'record cr-rev-mk.<murmur3sum32 of ([rtbAccountID]_[creativeID]> with ttl 10min in redis.'
        2. Then check mock server has been submit the creative to google api to review.   
        3. Then go to s3 '(​​vungle2-ssp-dev/admobreview/creatives' to check whether the creativeid id recorded here.
        4. Cron job runs once every 30 minutes, to get the crid from s3 creative folder, then send it to 'adquality-admob-submitreview-list'.
           Validate 'adquality-admob-submitreview-list' has the creative ids.
        5. Admobreviewservice get the review result throug consumer 'adquality-admob-submitreview-list'.
           set the response result = [],
           a. Validate the crid will store in s3 creative  with retry:true flag.
           b. Waitting for the next process. Then set the result to 'STATUS_UNSPECIFIED'.
           c. Validate the process finish. the crid will record to s3 failed folder.
        '''

    @allure.feature('google api integration')
    @allure.tag('normal')
    @allure.description('Verify disapproved process')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_admob_google_integration_creative_review_process_disapproved_01(self, pub_app_id, placement):
        pass
        '''
        Steps:
        1. Send admob head bidding request to jaeger auction. after it passed all bid filters,
           a. Validate 'send message to topic ex-jaeger-admob-creatives-20220818'.
           b. Validate 'record cr-rev-mk.<murmur3sum32 of ([rtbAccountID]_[creativeID]> with ttl 10min in redis.'
        2. Then check mock server has been submit the creative to google api to review.   
        3. Then go to s3 '(​​vungle2-ssp-dev/admobreview/creatives' to check whether the creativeid id recorded here.
        4. Cron job runs once every 30 minutes, to get the crid from s3 creative folder, then send it to 'adquality-admob-submitreview-list'.
           Validate 'adquality-admob-submitreview-list' has the creative ids.
        5. Admobreviewservice get the review result throug consumer 'adquality-admob-submitreview-list'.
           set the response result = global/china/russia=DISAPPROVED,
           a. Validate the crid will not exist in s3 creative again.
           b. Validate in redis will exist three keys as below:
             cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.CN, with the TTL=168 hours, value=0  
             cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.RUA, with the TTL=168 hours, value=0  
             cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.ALL, with the TTL=168 hours, value=0  
        6. Send admob request again, jaeger will not auction.     
        '''

    @allure.feature('google api integration')
    @allure.tag('normal')
    @allure.description('Verify approved process')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_admob_google_integration_creative_review_process_approved_01(self, pub_app_id, placement):
        pass
        '''
        Steps:
        1. Send admob head bidding request to jaeger auction. after it passed all bid filters,
           a. Validate 'send message to topic ex-jaeger-admob-creatives-20220818'.
           b. Validate 'record cr-rev-mk.<murmur3sum32 of ([rtbAccountID]_[creativeID]> with ttl 10min in redis.'
        2. Then check mock server has been submit the creative to google api to review.   
        3. Then go to s3 '(​​vungle2-ssp-dev/admobreview/creatives' to check whether the creativeid id recorded here.
        4. Cron job runs once every 30 minutes, to get the crid from s3 creative folder, then send it to 'adquality-admob-submitreview-list'.
           Validate 'adquality-admob-submitreview-list' has the creative ids.
        5. Admobreviewservice get the review result throug consumer 'adquality-admob-submitreview-list'.
           set the response result = global/china/russia=APPROVED,
           a. Validate the crid will not exist in s3 creative again.
           b. Validate no keys exist in redis.
        6. Send admob request again, jaeger auction.     
        '''

    @allure.feature('google api integration')
    @allure.tag('normal')
    @allure.description('Verify PENDING_REVIEW process')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_admob_google_integration_creative_review_process_pending_review_01(self, pub_app_id, placement):
        pass
        '''
        Steps:
        1. Send admob head bidding request to jaeger auction. after it passed all bid filters,
           a. Validate 'send message to topic ex-jaeger-admob-creatives-20220818'.
           b. Validate 'record cr-rev-mk.<murmur3sum32 of ([rtbAccountID]_[creativeID]> with ttl 10min in redis.'
        2. Then check mock server has been submit the creative to google api to review.   
        3. Then go to s3 '(​​vungle2-ssp-dev/admobreview/creatives' to check whether the creativeid id recorded here.
        4. Cron job runs once every 30 minutes, to get the crid from s3 creative folder, then send it to 'adquality-admob-submitreview-list'.
           Validate 'adquality-admob-submitreview-list' has the creative ids.
        5. Admobreviewservice get the review result throug consumer 'adquality-admob-submitreview-list'.
           set the response result = global/china/russia=PENDING_REVIEW,
           a. Validate the crid will not exist in s3 creative again.
           b. Validate no keys exist in redis.
        6. Send admob request again, jaeger auction.     
        '''

    @allure.feature('google api integration')
    @allure.tag('normal')
    @allure.description('Verify mixed status process')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_admob_google_integration_creative_review_process_mixed_status_01(self, pub_app_id, placement):
        pass
        '''
        Steps:
        1. Send admob head bidding request to jaeger auction. after it passed all bid filters,
           a. Validate 'send message to topic ex-jaeger-admob-creatives-20220818'.
           b. Validate 'record cr-rev-mk.<murmur3sum32 of ([rtbAccountID]_[creativeID]> with ttl 10min in redis.'
        2. Then check mock server has been submit the creative to google api to review.   
        3. Then go to s3 '(​​vungle2-ssp-dev/admobreview/creatives' to check whether the creativeid id recorded here.
        4. Cron job runs once every 30 minutes, to get the crid from s3 creative folder, then send it to 'adquality-admob-submitreview-list'.
           Validate 'adquality-admob-submitreview-list' has the creative ids.
        5. Admobreviewservice get the review result throug consumer 'adquality-admob-submitreview-list'.
           set the response result = global/china/russia=APPROVED/PENDING_REVIEW/DISAPPROVED,
           a. Validate the crid will not exist in s3 creative again.
           b. Validate russia keys exist in redis:
              cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.RUA, with the TTL=168 hours, value=0  
        6. Send admob request with russia ip, jaeger will not auction.     
           Send admob request with other ips, jaeger not auction.      
        '''

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.238.0')
    @allure.story('PBJ-4782 Need to use helm env to read programmatic fullscreen template URL.')
    @allure.description('Verify for the programmatic video template URL')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_vungle_mraid_third_party_placement])
    def test_programmatic_template_01(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that('/template-rtb/programmaticFullscreen-v4' in ad_markup['templateURL'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.238.0')
    @allure.story('PBJ-4782 Need to use helm env to read programmatic fullscreen template URL.')
    @allure.description('Verify for the programmatic banner template URL')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_programmatic_template_02(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that('/template-rtb/programmaticBanner-v1' in ad_markup['templateURL'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'v1.238.0')
    @allure.story('PBJ-4782 Need to use helm env to read programmatic fullscreen template URL.')
    @allure.description('Verify for the programmatic mrec template URL')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    def test_programmatic_template_03(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that('/template-rtb/programmaticBanner-v1' in ad_markup['templateURL'])

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify 50 percent traffic of AU will serve successfully')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_throttle_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_placement_throttle_01(self, pub_app_id, placement, header_bidding, rtb_ids):
        """

        "is_throttling_enabled":true
        "default_throttling": 5000
        geo{
            "au": 5000
            "us"  10000
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36),
                                            header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], equal_to('request is rejected by filter'))
        else:
            assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify 100 percent traffic of US will serve successfully')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_throttle_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_placement_throttle_02(self, pub_app_id, placement, header_bidding, rtb_ids):
        """

        "is_throttling_enabled":true
        "default_throttling": 5000
        geo{
            "au": 5000
            "us"  10000
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36),
                                            header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify 50 percent traffic of gb will serve successfully')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_throttle_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_placement_throttle_03(self, pub_app_id, placement, header_bidding, rtb_ids):
        """

        "is_throttling_enabled":true
        "default_throttling": 5000
        geo{
            "au": 5000
            "us"  10000
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36),
                                            header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=gb_ip,
                                          rtb_selector=rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' in ad_markup:
            assert_that(ad_markup['info'], equal_to('request is rejected by filter'))
        else:
            assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('placement throttle')
    @allure.tag('normal', 'test mode')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify placement throttle will not impact test mode traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_throttle_placement])
    @pytest.mark.parametrize('ip', [au_ip, us_ip, gb_ip])
    @pytest.mark.parametrize('rtb_ids', [ext_test_mode_kraken_rtb_ids_vast, test_mode_kraken_rtb_ids])
    def test_placement_throttle_test_mode(self, pub_app_id, placement, rtb_ids, ip):
        """

        "is_throttling_enabled":true
        "default_throttling": 5000
        geo{
            "au": 5000
            "us"  10000
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip,
                                          rtb_selector=rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify is_throttling_enabled = false will not take throttle effect')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_throttle_placement_false])
    @pytest.mark.parametrize('ip', [au_ip, us_ip, gb_ip])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_placement_throttle_false(self, pub_app_id, placement, rtb_ids, ip):
        """

        "is_throttling_enabled":false
        "default_throttling": 5000
        geo{
            "au": 5000
            "us"  10000
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip,
                                          rtb_selector=rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify is_throttling_enabled = true w/o throttle percentage setting will not'
                        ' take throttle effect')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [au_ip, us_ip, gb_ip])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_placement_throttle_flag_true_but_no_setting_01(self, pub_app_id, placement, rtb_ids, ip):
        """
        "is_throttling_enabled":true
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip,
                                          rtb_selector=rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify no is_throttling_enabled flag wil not take throttle effect')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('ip', [au_ip, us_ip, gb_ip])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids])
    def test_placement_no_throttle_flag(self, pub_app_id, placement, rtb_ids, ip):
        """
        default_throttling: 5000
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip,
                                          rtb_selector=rtb_ids))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')


    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify 50 percent traffic of AU will serve successfully')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_throttle])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('ip', [au_ip])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_placement_throttle_01(self, pub_app_id, placement, sdk_v, partner, ip, rtb_ids):
        """
            "is_throttling_enabled":true
            "default_throttling": 5000
            geo{
                "au": 5000
                "us"  10000
            }
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb_ids, ip=ip
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if 'nbr' in response_payload:
                assert_keys_exist(response_payload['ext'], 'err_msg')
                assert_that('rejected by filter: RESULT_REQUEST_THROTTLED' in response_payload['ext']['err_msg'])
            else:
                assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify 100 percent traffic of US will serve successfully')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_throttle])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('ip', [us_ip])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_placement_throttle_02(self, pub_app_id, placement, sdk_v, partner, ip, rtb_ids):
        """
            "is_throttling_enabled":true
            "default_throttling": 5000
            geo{
                "au": 5000
                "us"  10000
            }
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb_ids, ip=ip
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify 50 percent traffic of gb will serve successfully')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_throttle])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('ip', [gb_ip])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_placement_throttle_03(self, pub_app_id, placement, sdk_v, partner, ip, rtb_ids):
        """
            "is_throttling_enabled":true
            "default_throttling": 5000
            geo{
                "au": 5000
                "us"  10000
            }
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb_ids, ip=ip
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if 'nbr' in response_payload:
                assert_keys_exist(response_payload['ext'], 'err_msg')
                assert_that('rejected by filter: RESULT_REQUEST_THROTTLED' in response_payload['ext']['err_msg'])
            else:
                assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('placement throttle')
    @allure.tag('normal', 'test mode')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify placement throttle will not impact test mode traffic')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_throttle])
    @pytest.mark.parametrize('rtb_ids', [ext_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('ip', [au_ip, us_ip, gb_ip])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_placement_throttle_test_mode(self, pub_app_id, placement, sdk_v, partner, ip, rtb_ids):
        """
            "is_throttling_enabled":true
            "default_throttling": 5000
            geo{
                "au": 5000
                "us"  10000
            }
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb_ids, ip=ip, is_test=1,
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify is_throttling_enabled = false will not take throttle effect')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_throttle_false])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('ip', [au_ip, us_ip, gb_ip])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_placement_throttle_false(self, pub_app_id, placement, sdk_v, partner, ip, rtb_ids):
        """
            "is_throttling_enabled":false
            "default_throttling": 5000
            geo{
                "au": 5000
                "us"  10000
            }
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb_ids, ip=ip, is_test=0
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify is_throttling_enabled = false will not take throttle effect')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('ip', [au_ip, us_ip, gb_ip])
    @pytest.mark.parametrize('partner', ['max'])
    def test_placement_throttle_flag_true_but_no_setting(self, pub_app_id, placement, sdk_v, partner, ip, rtb_ids):
        """
            "is_throttling_enabled":true
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb_ids, ip=ip, is_test=0
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify traffic of AU will not serve successfully')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement_throttle])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('ip', [au_ip])
    @pytest.mark.parametrize('partner', ['max'])
    def test_placement_throttle_for_hybrird(self, pub_app_id, placement, sdk_v, partner, ip, rtb_ids):
        """
            "is_throttling_enabled":true
            "default_throttling": 5000
            geo{
                "au": 0
                "us"  10000
            }
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb_ids, ip=ip, is_test=0
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload['ext'], 'err_msg')
            assert_that('rejected by filter: RESULT_REQUEST_THROTTLED' in response_payload['ext']['err_msg'])

    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify traffic of us will serve successfully')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement_throttle])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('ip', [us_ip])
    @pytest.mark.parametrize('partner', ['max'])
    def test_placement_throttle_for_hybrird_01(self, pub_app_id, placement, sdk_v, partner, ip, rtb_ids):
        """
            "is_throttling_enabled":true
            "default_throttling": 5000
            geo{
                "au": 0
                "us"  10000
            }
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb_ids, ip=ip, is_test=0
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('RTA')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4877 RTA - Support getting time difference from loadAd to playAd')
    @allure.description('Verify tracking url in ad response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_tracking_url(self, pub_app_id, placement, rtb_ids,):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=rtb_ids, sdk_version=test_default_real_time_sdk_version))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        notification = ad_markup['notification']
        for tracking_url in notification:
            if 'load_ad' in tracking_url:
                assert_that(True)
                return
        assert_that(False)

    @allure.feature('basic')
    @allure.tag('normal', 'v1.252.0')
    @allure.story('PBJ-4938 Header Bidding flag enhancement from reused placements')
    @allure.description('Verify that jaeger will no serve for appbidding placement when sdk <=6.6')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.0', 'Vungle/6.5.9', 'Vungle/6.4.9'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_no_serve_for_appbidding_placement(self, pub_app_id, placement, rtb_ids, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('request is rejected by header bidding sdk version control'))

    @allure.feature('basic')
    @allure.tag('normal', 'v1.252.0')
    @allure.story('PBJ-4938 Header Bidding flag enhancement from reused placements')
    @allure.description('Verify that jaeger will serve for appbidding placement when sdk >6.6')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.1', 'Vungle/6.7.9'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_appbidding_placement(self, pub_app_id, placement, rtb_ids, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('no serve')
    @allure.tag('normal')
    @allure.story('PBJ-5071 SDK 6.7 Traffic block for specific App on Windows')
    @allure.description('Verify jaeger not serve for sdk<=6.7.0 for windows app(57979405fb0fb7fc6e0000a2)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_specify_block_app])
    @pytest.mark.parametrize('placement', [windows_common_specify_block_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.7.0', 'Vungle/6.6.9'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_block_app_on_specify_app_01(self, pub_app_id, placement, rtb_ids, sdk_v):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('no serve')
    @allure.tag('normal')
    @allure.story('PBJ-5071 SDK 6.7 Traffic block for specific App on Windows')
    @allure.description('Verify jaeger serve for sdk>6.7.0 for windows app(57979405fb0fb7fc6e0000a2)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_specify_block_app])
    @pytest.mark.parametrize('placement', [windows_common_specify_block_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.7.1', 'Vungle/6.8.9'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_block_app_on_specify_app_02(self, pub_app_id, placement, rtb_ids, sdk_v):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')


    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-5179 [Kraken] One service for idsp & edsp')
    @allure.description('Kraken serve as one service')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_default_int])
    def test_kranken_serve_as_idsp_t(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp_ext = bid_request['imp'][0]['ext']
        assert_keys_exist(imp_ext, 'vungle')


    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-5179 [Kraken] One service for idsp & edsp')
    @allure.description('Kraken serve as one service')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [non_test_mode_kraken_default_int])
    def test_kranken_serve_as_idsp_nt(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp_ext = bid_request['imp'][0]['ext']
        assert_keys_exist(imp_ext, 'vungle')



    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-5179 [Kraken] One service for idsp & edsp')
    @allure.description('Kraken serve as one service')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_default_ext])
    def test_kranken_serve_as_edsp_t(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp_ext = bid_request['imp'][0]['ext']
        assert_keys_not_exist(imp_ext, 'vungle')



    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-5179 [Kraken] One service for idsp & edsp')
    @allure.description('Kraken serve as one service')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [non_test_mode_kraken_default_ext])
    def test_kranken_serve_as_edsp_nt(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp_ext = bid_request['imp'][0]['ext']
        assert_keys_not_exist(imp_ext, 'vungle')


    @allure.feature('block')
    @allure.tag('basic', 'v1.257.0')
    @allure.story('PBJ-5258 Do not send rewarded video traffic to InMobi')
    @allure.description('Verify that jaeger will block rtb account id (60d191906f59f30017a17639) for rewarded placement'
                        )
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_default_InMobi])
    @pytest.mark.parametrize('hb', [True, False])
    def test_block_rewarded_for_inmobi_nt(self, pub_app_id, placement, rtb, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        ext_debug = response_payload['ext']['debug']
        assert_that(ext_debug['rtb_failed_filters'][rtb], equal_to('placementTypeFilter'))


    @allure.feature('block')
    @allure.tag('basic', 'v1.257.0')
    @allure.story('PBJ-5258 Do not send rewarded video traffic to InMobi')
    @allure.description('Verify that jaeger does not block rtb account id (60d191906f59f30017a17639) for other placements'
                        )
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_default_InMobi])
    @pytest.mark.parametrize('hb', [True, False])
    def test_dont_block_other_placements_inmobi(self, pub_app_id, placement, rtb, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')



    @allure.feature('block')
    @allure.tag('basic')
    @allure.story('PBJ-5258 Do not send rewarded video traffic to InMobi')
    @allure.description('Verify that jaeger will block rtb account id (60d191906f59f30017a17639) for rewarded placement'
                        )
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement_rewarded])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_default_InMobi])
    @pytest.mark.parametrize('hb', [True, False])
    def test_block_rewarded_for_inmobi_android(self, pub_app_id, placement, rtb, hb):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        ext_debug = response_payload['ext']['debug']
        assert_that(ext_debug['rtb_failed_filters'][rtb], equal_to('placementTypeFilter'))

