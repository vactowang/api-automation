import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_hbp_with_real_time_token
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestAdType(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('ad type')
    @allure.description('Verify ad type from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_type(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids, debug='jaeger'))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(ad_markup['adType'] in ['vungle_local', 'vungle_mraid'])

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0', 'R_1.130.0')
    @allure.story('PBJ-1335 VAST ad type transform to MRAID, PBJ-1723 Modify the scope for converting vast to mraid')
    @allure.description('Verify the ad type convent to mraid for programmatic vast ad (iOS>=10, SDK>=5.1.0)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('os_ver', ['10', '10.1', '12.9'])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/5.1.0', 'Vungle/5.1.1', 'Vungle/6.3.3'])
    def test_for_ad_type_vast_convert_mraid(self, pub_app_id, placement, os_ver, sdk_ver):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, os_version=os_ver, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['adType'], equal_to('vungle_mraid'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0', 'R_1.130.0')
    @allure.story('PBJ-1335 VAST ad type transform to MRAID, PBJ-1723 Modify the scope for converting vast to mraid')
    @allure.description('Verify the ad type does not convent to mraid for programmatic vast ad (iOS<10)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_for_ad_type_vast_not_convert_mraid_1(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, os_version='9.9', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb, sdk_version='Vungle/5.1.0'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['adType'], equal_to('vungle_local'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0', 'R_1.130.0')
    @allure.story('PBJ-1335 VAST ad type transform to MRAID, PBJ-1723 Modify the scope for converting vast to mraid')
    @allure.description('Verify the ad type does not convent to mraid for programmatic vast ad (SDK<5.1.0)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('os_ver', ['10', '12.9'])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/5.0.9', 'Vungle/5.0', 'Vungle/4.9.9'])
    def test_for_ad_type_vast_not_convert_mraid_2(self, pub_app_id, placement, os_ver, sdk_ver):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, os_version=os_ver, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['adType'], equal_to('vungle_local'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.122.0', 'R_1.130.0')
    @allure.story('PBJ-1335 VAST ad type transform to MRAID, PBJ-1723 Modify the scope for converting vast to mraid')
    @allure.description('Verify the ad type does not convent to mraid for programmatic vast ad (iOS<10, SDK<5.1.0)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('os_ver', ['9.9'])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/5.0.9', 'Vungle/5.0', 'Vungle/4.9.9'])
    def test_for_ad_type_vast_not_convert_mraid_3(self, pub_app_id, placement, os_ver, sdk_ver):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, os_version=os_ver, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['adType'], equal_to('vungle_local'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'legacy')
    @allure.story('PBJ-4862 No TPAT click for Windows& Amazon on Legacy')
    @allure.description('Verify :postroll_click, checkpoint.75, checkpoint.100 are added for tpat url for vunlge local')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('os_ver', ['10', '12.9'])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/5.0.9', 'Vungle/5.0', 'Vungle/4.9.9'])
    def test_tpat_for_vungle_local_01(self, pub_app_id, placement, os_ver, sdk_ver):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, os_version=os_ver, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        tpat_play_percentage = ad_markup['tpat']['play_percentage'][0]
        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_exist(ad_markup['tpat'], 'postroll_click')
            assert_that(tpat_play_percentage['checkpoint'] in [0, 1, 0.75])

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode')
    @allure.story('external support')
    @allure.description('Verify the ad type of programmatic banner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_for_ad_type_of_programmatic_banner(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, banner=True, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' not in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['adType'], equal_to('vungle_mraid'))

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode')
    @allure.story('external support')
    @allure.description('Verify the ad type of programmatic VAST')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_for_ad_type_of_programmatic_vast(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['adType'], equal_to('vungle_mraid'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.135.0')
    @allure.story('PBJ-1912 Converting Android VAST to MRAID ad format for some specific sdk versions')
    @allure.description('Verify the ad type convent to mraid for programmatic vast ad Android SDK >= 5.1.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sdk_ver', ['VungleDroid/5.1.0', 'VungleDroid/5.1.1'])
    def test_for_ad_type_vast_convert_mraid_android(self, pub_app_id, sdk_ver, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['adType'], equal_to('vungle_mraid'))

    @allure.feature('programmatic support')
    @allure.tag('normal', 'test_mode', 'R_1.135.0')
    @allure.story('PBJ-1912 Converting Android VAST to MRAID ad format for some specific sdk versions')
    @allure.description('Verify the ad type convent to mraid for programmatic vast ad Android SDK < 5.1.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sdk_ver', ['VungleDroid/5.0.9'])
    def test_for_ad_type_vast_not_convert_mraid_android(self, pub_app_id, sdk_ver, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['adType'], equal_to('vungle_local'))

    @allure.feature('programmatic support')
    @allure.tag('normal')
    @allure.story('PBJ-4764 Convert Amazon VAST to MRAID ad format')
    @allure.description('Verify the ad type convent to mraid for programmatic vast SDK >= 6.12.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.12.0', 'Vungle/6.12.1'])
    def test_for_ad_type_vast_convert_mraid_amazon(self, pub_app_id, sdk_ver, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_amazon(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['adType'], equal_to('vungle_mraid'))

    @allure.feature('programmatic support')
    @allure.tag('normal')
    @allure.story('PBJ-4764 Convert Amazon VAST to MRAID ad format')
    @allure.description('Verify the ad type does not convent to mraid for programmatic vast SDK < 6.12.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_for_ad_type_vast_convert_mraid_amazon_01(self, pub_app_id, sdk_ver, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_amazon(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(ad_markup['adType'], equal_to('vungle_local'))

    @allure.feature('programmatic support')
    @allure.tag('normal')
    @allure.story('PBJ-5005 Hardcode showClose flag in Jaeger to always be false')
    @allure.description('Verify showclose Flag should be 0 on windows')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/4.9.9'])
    @pytest.mark.parametrize('rtb_ids', [ext_test_mode_kraken_rtb_ids_vast, test_mode_kraken_rtb_ids])
    def test_showClose_flag_windows(self, pub_app_id, sdk_ver, placement, rtb_ids):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ashwid=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['showClose'], equal_to(0))
        assert_that(ad_markup['showCloseIncentivized'], equal_to(0))

    @allure.feature('programmatic support')
    @allure.tag('normal')
    @allure.story('PBJ-5005 Hardcode showClose flag in Jaeger to always be false')
    @allure.description('Verify showclose Flag should not be 0 on other platforms')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/4.9.9'])
    @pytest.mark.parametrize('rtb_ids', [ext_test_mode_kraken_rtb_ids_vast])
    def test_showClose_flag_ios(self, pub_app_id, sdk_ver, placement, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['showClose'], not equal_to(0))
        assert_that(ad_markup['showCloseIncentivized'], not equal_to(0))

    # Below cases are for grabing test cases from prod, and specified kraken will serve with these ads, if the below
    # cases are failed. please check whether the ads exist in S3(date is looking back 3
    # days)

    @allure.feature('Support SDK Test')
    @allure.tag('normal')
    @allure.story('PBJ-4957 Support SDK Test - Grab online ads to feed into Kraken to make it return more ads')
    @allure.description(
        "Verify that internal RTB which endpoint is the specified kraken will serve with grabed online ads")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [int_grab_online_rtb])
    def test_grab_online_ads_ios(self, pub_app_id, sdk_ver, placement, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')
        callToActionDest = ad_markup['callToActionDest']
        assert_that('apple.com' in callToActionDest)

    @allure.feature('Support SDK Test')
    @allure.tag('normal')
    @allure.story('PBJ-4957 Support SDK Test - Grab online ads to feed into Kraken to make it return more ads')
    @allure.description(
        "Verify that internal RTB which endpoint is the specified kraken will serve with grabed online ads")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [int_grab_online_rtb])
    def test_grab_online_ads_android(self, pub_app_id, sdk_ver, placement, rtb_ids):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')
        callToActionDest = ad_markup['callToActionDest']
        assert_that('google.com' or 'android' in callToActionDest )

    @allure.feature('Support SDK Test')
    @allure.tag('normal')
    @allure.story('PBJ-4957 Support SDK Test - Grab online ads to feed into Kraken to make it return more ads')
    @allure.description(
        "Verify that internal RTB which endpoint is the specified kraken will serve with grabed online ads")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [int_grab_online_rtb])
    def test_grab_online_ads_windows(self, pub_app_id, sdk_ver, placement, rtb_ids):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')
        callToActionDest = ad_markup['callToActionDest']
        assert_that('ms-windows-store' in callToActionDest)

    @allure.feature('Support SDK Test')
    @allure.tag('normal')
    @allure.story('PBJ-4957 Support SDK Test - Grab online ads to feed into Kraken to make it return more ads')
    @allure.description(
        "Verify that internal RTB which endpoint is the specified kraken will serve with grabed online ads")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('rtb_ids', [int_grab_online_rtb])
    def test_grab_online_ads_banner(self, pub_app_id, sdk_ver, placement, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True,
                                            banner_type='banner_leaderboard')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')
        template_type = ad_markup['template_type']
        assert_that(template_type, equal_to('banner'))

    # @allure.feature('Support SDK Test')
    # @allure.tag('normal')
    # @allure.story('PBJ-4957 Support SDK Test - Grab online ads to feed into Kraken to make it return more ads')
    # @allure.description(
    #     "Verify that internal RTB which endpoint is the specified kraken will serve with grabed online ads")
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_native_placement])
    # @pytest.mark.parametrize('sdk_ver', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('rtb_ids', [int_grab_online_rtb])
    # def test_grab_online_ads_native(self, pub_app_id, sdk_ver, placement, rtb_ids):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids, sdk_version=sdk_ver))
    #
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_keys_not_exist(ad_markup, 'sleep')
    #     template_type = ad_markup['template_type']
    #     assert_that(template_type, equal_to('native'))

    @allure.feature('Support SDK Test')
    @allure.tag('normal')
    @allure.story('PBJ-4957 Support SDK Test - Grab online ads to feed into Kraken to make it return more ads')
    @allure.description(
        "Verify that ext RTB which endpoint is the specified kraken will serve with grabed online ads")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_ver', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('rtb_ids', [default_onlinefeeder_ext])
    def test_grab_online_ads_ext(self, pub_app_id, sdk_ver, placement, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('Support SDK Test')
    @allure.tag('normal')
    @allure.story('PBJ-4957 Support SDK Test - Grab online ads to feed into Kraken to make it return more ads')
    @allure.description(
        "Verify that internal RTB which endpoint is the specified kraken will serve with grabed online ads")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('rtb_ids', [default_onlinefeeder_ext])
    def test_grab_online_ads_real_time(self, pub_app_id, placement, sdk_v, partner, rtb_ids):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, coppa=True, rtb=rtb_ids)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            bid_response = info['hbp_response']
            assert_keys_exist(bid_response, 'seatbid')

    # @allure.feature('Support SDK Test')
    # @allure.tag('normal')
    # @allure.story('PBJ-4957 Support SDK Test - Grab online ads to feed into Kraken to make it return more ads')
    # @allure.description("Verify that no ads in S3 folder")
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('placement', [android_common_test_placement])
    # @pytest.mark.parametrize('sdk_ver', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('rtb_ids', [ext_grab_online_rtb])
    # def test_grab_online_ads_ext_no_ads_in_s3(self, pub_app_id, sdk_ver, placement, rtb_ids):
    #     req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids, sdk_version=sdk_ver))
    #
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_keys_exist(ad_markup, 'sleep')