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
class TestDeviceDetails(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request device')
    @allure.description('Verify app device details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_details(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['ifa'], equal_to(test_ifa))
        assert_that(device['geo']['country'], equal_to('FRA'))
        assert_that(device['ip'], equal_to(eu_country_ip))
        assert_that(device['os'], equal_to_ignoring_case('iOS'))
        assert_that(device['osv'], equal_to('13'))

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request device')
    @allure.description('Verify app device ext details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_ext_details(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['ext']['vungle']['isu'], equal_to(test_ifa))
        assert_that(device['ext']['vungle']['id'], equal_to(test_ifa))
        assert_that(device['ext']['vungle']['id_source'], equal_to_ignoring_case('IFA'))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('GDPR')
    @allure.description('Verify device ext from debug in GDPR opted out')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_ext_gdpr_opted_out(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', gdpr='opted_out', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['ext']['vungle']['isu'], not equal_to(test_ifa))
        assert_that(device['ext']['vungle']['id'], not equal_to(test_ifa))
        assert_that(device['ext']['vungle']['id_source'], equal_to('GDPR'))

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0', 'test_mode')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the device geo field for openrtb25x changes')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_geo_openrtb25x(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['geo']['ipservice'], equal_to(3))

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the no ipservice field in device geo when geo info in ads request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_device_geo_no_ipservice_openrtb25x(self, pub_app_id):
        test_android_id = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_android(
            pub_app_id, android_common_test_placement, android_id=test_android_id, geo=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(device['geo'], 'ipservice')

    @allure.feature('wurfl support')
    @allure.tag('normal', 'R_1.131.0')
    @allure.story('PBJ-1724 Support wurfl in Jaeger')
    @allure.description('Verify that the valid Android ua string in ads request with iOS device')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_valid_ua_ios(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        test_ua = 'Mozilla/5.0 (Linux; Android 7.0; SM-T819 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Version/4.0 Chrome/83.0.4103.101 Safari/537.36,SM-G965N,Samsung,4'
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, make='Apple',
                                            model='iPhone11,8', ua=test_ua)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['ua'], equal_to(test_ua))
        if wurfl_flag:
            assert_that(device['devicetype'], equal_to(5))
            assert_that(device['make'], equal_to('Samsung'))
            assert_that(device['model'], equal_to('SM-T819'))
        else:
            assert_that(device['devicetype'], equal_to(1))
            assert_that(device['make'], equal_to('Apple'))
            assert_that(device['model'], equal_to('iPhone11,8'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'R_1.131.0', 'test_mode')
    @allure.story('PBJ-1724 Support wurfl in Jaeger')
    @allure.description('Verify that the valid Android ua string in ads request with iOS device in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_valid_ua_ios_test_mode(self, pub_app_id):
        test_ua = 'Mozilla/5.0 (Linux; Android 7.0; SM-T819 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Version/4.0 Chrome/83.0.4103.101 Safari/537.36,SM-G965N,Samsung,4'
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id, make='Apple',
                                            model='iPhone11,8', ua=test_ua)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['ua'], equal_to(test_ua))
        if wurfl_flag:
            assert_that(device['devicetype'], equal_to(5))
            assert_that(device['make'], equal_to('Samsung'))
            assert_that(device['model'], equal_to('SM-T819'))
        else:
            assert_that(device['devicetype'], equal_to(1))
            assert_that(device['make'], equal_to('Apple'))
            assert_that(device['model'], equal_to('iPhone11,8'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'R_1.131.0')
    @allure.story('PBJ-1724 Support wurfl in Jaeger')
    @allure.description('Verify that the valid ua string in ads request with Android device')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_valid_ua_android(self, pub_app_id):
        test_android_id = gen_device_id(digital=36)
        test_ua = 'Mozilla/5.0 (Linux; Android 7.0; SM-T819 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Version/4.0 Chrome/83.0.4103.101 Safari/537.36,SM-G965N,Samsung,4'
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, android_id=test_android_id,
                                                model='q10', make='cool', ua=test_ua)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['ua'], equal_to(test_ua))
        if wurfl_flag:
            assert_that(device['devicetype'], equal_to(5))
            assert_that(device['make'], equal_to('Samsung'))
            assert_that(device['model'], equal_to('SM-T819'))
        else:
            assert_that(device['devicetype'], equal_to(1))
            assert_that(device['make'], equal_to('cool'))
            assert_that(device['model'], equal_to('q10'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'R_1.131.0')
    @allure.story('PBJ-1724 Support wurfl in Jaeger')
    @allure.description('Verify that the invalid ua string in ads request with iOS device')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_invalid_ua_ios(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        test_ua = 'test_ua'
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, make='Apple',
                                            model='iPhone11,8', ua=test_ua)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['ua'], equal_to(test_ua))
        assert_that(device['devicetype'], equal_to(1))
        assert_that(device['make'], equal_to('Apple'))
        assert_that(device['model'], equal_to('iPhone11,8'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'R_1.131.0', 'test_mode')
    @allure.story('PBJ-1724 Support wurfl in Jaeger')
    @allure.description('Verify that the invalid ua string in ads request with iOS device in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_invalid_ua_ios_test_mode(self, pub_app_id):
        test_ua = 'test_ua'
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id, make='Apple',
                                            model='iPhone11,8', ua=test_ua)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['ua'], equal_to(test_ua))
        assert_that(device['devicetype'], equal_to(1))
        assert_that(device['make'], equal_to('Apple'))
        assert_that(device['model'], equal_to('iPhone11,8'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'R_1.131.0')
    @allure.story('PBJ-1724 Support wurfl in Jaeger')
    @allure.description('Verify that the invalid ua string in ads request with Android device')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_invalid_ua_android(self, pub_app_id):
        test_android_id = gen_device_id(digital=36)
        test_ua = 'test_ua'
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, android_id=test_android_id,
                                                make='cool', model='q10', ua=test_ua)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['ua'], equal_to(test_ua))
        assert_that(device['devicetype'], equal_to(1))
        assert_that(device['make'], equal_to('cool'))
        assert_that(device['model'], equal_to('q10'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv is hardcode to OSAPI when model is using WURFL for edsps')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_default_value_of_the_hwv_ios_01(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id, make='Apple',
                                            model='iPhone11,8')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('XR'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv is hardcode to OSAPI when device_detect_strategies=WURFL for edsps')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_value_of_the_hwv_ios_set_to_wurfl_01(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_wurfl.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_wurfl.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id, make='Apple',
                                            model='iPhone11,8')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('XR'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv is hardcode to OSAPI when device_detect_strategies=OSAPI for edsps')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_value_of_the_hwv_ios_set_to_OSAPI_01(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_OSAPI.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_OSAPI.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id, make='Apple',
                                            model='iPhone14,2')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('13 Pro'))

    @allure.feature('wurfl support')
    @allure.tag('normal')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv is hardcode to OSAPI when model is using WURFL for non test mode '
                        'edsps')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_default_value_of_the_hwv_02(self, pub_app_id):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid_1.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid_1.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_programmatic_mrec_placement, ifa=gen_device_id(),
                                            make='Apple',
                                            model='iPhone11,8')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('XR'))


    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv mapping to model when model is using OSAPI for edsps on windows')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    def test_default_value_of_the_hwv_windows_01(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_windows(pub_app_id, windows_common_test_placement, ashwid=test_mode_device_id,
                                                make='ASUSTeK COMPUTER INC.',
                                                model='GL752VW')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='VungleWindows/6.5.3 (Windows 10; native)',
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('GL752VW'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv mapping to marketingName when model is using wurfl'
                        ' for edsps on windows')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    def test_default_value_of_the_hwv_wurfl_windows_01(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_wurfl.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_wurfl.split(',')[1]
        req = request_payload.jaeger_v5_windows(pub_app_id, windows_common_test_placement, ashwid=test_mode_device_id,
                                                make='ASUSTeK COMPUTER INC.',
                                                model='GL752VW')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='VungleWindows/6.5.3 (Windows 10; native)',
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('Edge'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv mapping to model when using OSAPI'
                        ' for edsps on windows')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    def test_default_value_of_the_hwv_OSAPI_windows_01(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_OSAPI.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_OSAPI.split(',')[1]
        req = request_payload.jaeger_v5_windows(pub_app_id, windows_common_test_placement, ashwid=test_mode_device_id,
                                                make='ASUSTeK COMPUTER INC.',
                                                model='GL752VW')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='VungleWindows/6.5.3 (Windows 10; native)',
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('GL752VW'))



    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv mapping to marketing name when model is using default value for '
                        'edsps on android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_default_value_of_the_hwv_android_01(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=test_mode_device_id,
                                                make='Coolpad',
                                                model='8190Q')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('Xuan Ying 90'))


    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv mapping to marketing name when device_detect_strategies=WURFL for '
                        'edsps on android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_default_value_of_the_hwv_android_02(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_wurfl.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_wurfl.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=test_mode_device_id,
                                                make='Coolpad',
                                                model='8190Q')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('Xuan Ying 90'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv mapping to marketing name when device_detect_strategies=OSAPI for '
                        'edsps on android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_default_value_of_the_hwv_android_03(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_OSAPI.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_OSAPI.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=test_mode_device_id,
                                                make='Coolpad',
                                                model='8190Q')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('8190Q'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv mapping to marketing name when model is using WURFL for '
                        'edsps on amazon')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    def test_default_value_of_the_hwv_Amazon_01(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement,
                                               ifa=test_mode_device_id,
                                               make='samsung',
                                               model='SM-G973U1')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('Galaxy S10'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv mapping to marketing name when using WURFL for '
                        'edsps on amazon')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    def test_default_value_of_the_hwv_Amazon_02(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_wurfl.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_wurfl.split(',')[1]
        req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement,
                                               ifa=test_mode_device_id,
                                               make='samsung',
                                               model='SM-G973U1')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('Galaxy S10'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv mapping to marketing name when using OSAPI for '
                        'edsps on amazon')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    def test_default_value_of_the_hwv_Amazon_03(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_OSAPI.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_OSAPI.split(',')[1]
        req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement,
                                               ifa=test_mode_device_id,
                                               make='samsung',
                                               model='SM-G973U1')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device['hwv'], equal_to('SM-G973U1'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv when mixed rtb attend auction for '
                        'edsps on windows')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    def test_default_value_of_the_hwv_special_case_for_windows(self, pub_app_id):

        if env == 'ci':
            rtb = ext_test_mode_kraken_mixedRTB_wurfl_ci
            rtb1 = ext_test_mode_kraken_mixedRTB_wurfl_ci.split(',')[0]
            rtb2 = ext_test_mode_kraken_mixedRTB_wurfl_ci.split(',')[1]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_mixedRTB_wurfl
            rtb1 = ext_test_mode_kraken_mixedRTB_wurfl.split(',')[0]
            rtb2 = ext_test_mode_kraken_mixedRTB_wurfl.split(',')[1]
        req = request_payload.jaeger_v5_windows(windows_common_test_app, windows_common_test_placement,
                                                ashwid=test_mode_device_id,
                                                make='ASUSTeK COMPUTER INC.',
                                                model='GL752VW')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='VungleWindows/6.5.3 (Windows 10; native)',
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request_rtb1 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb1)
        bid_request_rtb2 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb2)
        device1 = bid_request_rtb1['device']
        device2 = bid_request_rtb2['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device1['make'], equal_to('ASUSTeK COMPUTER INC.'))
        assert_that(device1['model'], equal_to('GL752VW'))
        assert_that(device1['hwv'], equal_to('GL752VW'))
        assert_that(device2['make'], equal_to('Microsoft'))
        assert_that(device2['model'], equal_to('Edge'))
        assert_that(device2['hwv'], equal_to('Edge'))

    @allure.feature('wurfl support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3478 Implement device_detect_strategies for external DSPs')
    @allure.description('Verify that value of hwv when mixed rtb attend auction for '
                        'edsps on ios')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_default_value_of_the_hwv_special_case_for_ios(self, pub_app_id):
        test_idfv = '00000000-0000-0000-0000-000000000000'
        if env == 'ci':
            rtb = ext_test_mode_kraken_mixedRTB_wurfl_ci
            rtb1 = ext_test_mode_kraken_mixedRTB_wurfl_ci.split(',')[0]
            rtb2 = ext_test_mode_kraken_mixedRTB_wurfl_ci.split(',')[1]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_mixedRTB_wurfl
            rtb1 = ext_test_mode_kraken_mixedRTB_wurfl.split(',')[0]
            rtb2 = ext_test_mode_kraken_mixedRTB_wurfl.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            make='Apple',
                                            model='iPhone11,8', idfv=test_idfv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request_rtb1 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb1)
        bid_request_rtb2 = get_bid_request_obj_from_jaeger_explain(response_payload, rtb2)
        device1 = bid_request_rtb1['device']
        device2 = bid_request_rtb2['device']
        assert_keys_exist(device2, 'ext')
        assert_that(device2['ext']['idfv'], equal_to(test_idfv))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.139.0')
    @allure.story('PBJ-2003 HBP partner name in message record')
    @allure.description('Verify the mediation name from bid request device info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_ext_mediation(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.8.0;Mopub',
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to('Vungle/6.8.0;Mopub'))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'test_mode', 'R_1.139.0')
    @allure.story('PBJ-2003 HBP partner name in message record')
    @allure.description('Verify the mediation name from bid request device info in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_ext_mediation_test_mode(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.8.0;Mopub',
                                          rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to('Vungle/6.8.0;Mopub'))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.147.0')
    @allure.story('PBJ-2191 Parse Plugin name & Adapter Version for Saygames & ohayoo')
    @allure.description('Verify the plugin name and adapter version from bid request device info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0;vunglehbs/3.0.0', 'Vungle/6.8.0;vunglehbs/4.0.0'])
    def test_device_ext_plugin_name_adapter_ver(self, pub_app_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to(sdk_v))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.147.0', 'test_mode')
    @allure.story('PBJ-2191 Parse Plugin name & Adapter Version for Saygames & ohayoo')
    @allure.description('Verify the plugin name and adapter version from bid request device info in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0;vunglehbs/3.0.0', 'Vungle/6.8.0;vunglehbs/4.0.0'])
    def test_device_ext_plugin_name_adapter_ver_test_mode(self, pub_app_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to(sdk_v))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.152.0')
    @allure.story('PBJ-2333 Parse Plugin name & Adapter Version for Aequus')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0;vunglehbs/5.0.0'])
    def test_device_ext_plugin_name_adapter_ver_1(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to(sdk_v))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.152.0', 'test_mode')
    @allure.story('PBJ-2333 Parse Plugin name & Adapter Version for Aequus')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0;vunglehbs/5.0.0'])
    def test_device_ext_plugin_name_adapter_ver_test_mode_1(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to(sdk_v))


    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.153.0')
    @allure.story('PBJ-2333 Parse Plugin name & Adapter Version for charboost')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0;vunglehbs/6.0.0'])
    def test_device_ext_plugin_name_adapter_ver_2(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to(sdk_v))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.153.0', 'test_mode')
    @allure.story('PBJ-2333 Parse Plugin name & Adapter Version for charboost')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0;vunglehbs/6.0.0'])
    def test_device_ext_plugin_name_adapter_ver_test_mode_2(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to(sdk_v))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.165.0')
    @allure.story('PBJ-2784 HBP new endpoint for Fyber & TopOn')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0;vunglehbs/7.0.0'])
    def test_device_ext_plugin_name_adapter_ver_3(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to(sdk_v))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.165.0', 'test_mode')
    @allure.story('PBJ-2784 HBP new endpoint for Fyber & TopOn')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0;vunglehbs/7.0.0'])
    def test_device_ext_plugin_name_adapter_ver_test_mode_3(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to(sdk_v))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-3033 Add plugin name with vunglehbs map for rovio& admost in jaeger&scrat')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0;vunglehbs/9.0.0', 'Vungle/6.9.0;vunglehbs/10.0.0'])
    def test_device_ext_plugin_name_adapter_ver_4(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to(sdk_v))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.170.0', 'test_mode')
    @allure.story('PBJ-3033 Add plugin name with vunglehbs map for rovio& admost in jaeger&scrat')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0;vunglehbs/9.0.0', 'Vungle/6.9.0;vunglehbs/10.0.0'])
    def test_device_ext_plugin_name_adapter_ver_test_mode_4(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['device']['ext']['vungle']['vungleua'], equal_to(sdk_v))

    @allure.feature('bid request device')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2256 Set LMT to FALSE when IFA is present with non-zero value')
    @allure.description('Verify the lmt should be 0 with vaild IFA')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('lmt', [0, 1])
    def test_lmt_with_vaild_ifa(self, pub_app_id, placement, lmt):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), lmt=lmt)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=gb_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['lmt'], equal_to(0))

    @allure.feature('bid request device')
    @allure.tag('normal', 'R_1.149.0', 'test_mode')
    @allure.story('PBJ-2256 Set LMT to FALSE when IFA is present with non-zero value')
    @allure.description('Verify the lmt should be 0 with vaild IFA in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('lmt', [0, 1])
    def test_lmt_with_vaild_ifa_test_mode(self, pub_app_id, placement, lmt):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, lmt=lmt)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=gb_ip, rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['lmt'], equal_to(0))

    @allure.feature('bid request device')
    @allure.tag('normal', 'R_1.149.0')
    @allure.story('PBJ-2256 Set LMT to FALSE when IFA is present with non-zero value')
    @allure.description('Verify the lmt should keep the original value with invaild IFA')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ifa', ['00000000-0000-0000-0000-000000000000', ''])
    @pytest.mark.parametrize('lmt', [0, 1])
    def test_lmt_with_invaild_ifa(self, pub_app_id, placement, ifa, lmt):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=ifa, lmt=lmt)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['lmt'], equal_to(lmt))

    # ------------------------------------------ support ipv6 ---------------------------------------------------

    @allure.feature('support ipv6')
    @allure.tag('smoke')
    @allure.story('PBJ-3258 RTB::Feature request to support ipv6 format')
    @allure.description("Verify there is ipv6 field from bid request for non test mode XRTB")
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_ipv6_for_XRTB(self, pub_app_id, placement, hb):
        rtb = ext1_non_test_mode_kraken_rtb_ids_vast
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ipv6_example_01, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(device, 'ipv6')
        assert_keys_not_exist(device, 'ip')
        assert_that(device['ipv6'], equal_to(ipv6_example_01))

    @allure.feature('support ipv6')
    @allure.tag('smoke')
    @allure.story('PBJ-3258 RTB::Feature request to support ipv6 format')
    @allure.description("Verify there is ipv6 field from bid request for test mode XRTB")
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_ipv6_for_test_mode_XRTB(self, pub_app_id, placement, hb):
        rtb = ext1_test_mode_kraken_rtb_ids_vast
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ipv6_example_01,
                                                                        rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(device, 'ipv6')
        assert_keys_not_exist(device, 'ip')
        assert_that(device['ipv6'], equal_to(ipv6_example_01))

    @allure.feature('support ipv6')
    @allure.tag('smoke')
    @allure.story('PBJ-3258 RTB::Feature request to support ipv6 format')
    @allure.description("Verify there are ipv6 and ip fields from bid request for meister")
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_ipv6_for_meister(self, pub_app_id, placement, hb):
        rtb = meister_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ipv6_example_01,
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(device, 'ipv6')
        assert_keys_exist(device, 'ip')
        assert_that(device['ipv6'], equal_to(ipv6_example_01))
        assert_that(device['ip'], equal_to(ipv6_example_01))

    @allure.feature('support ipv6')
    @allure.tag('smoke')
    @allure.story('PBJ-3258 RTB::Feature request to support ipv6 format')
    @allure.description("Verify there is ip field from bid request for non test mode XRTB")
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_ipv4_for_XRTB(self, pub_app_id, placement, hb):
        rtb = ext1_non_test_mode_kraken_rtb_ids_vast
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_not_exist(device, 'ipv6')
        assert_that(device['ip'], equal_to(au_ip))

    @allure.feature('support ipv6')
    @allure.tag('smoke')
    @allure.story('PBJ-3258 RTB::Feature request to support ipv6 format')
    @allure.description("Verify there is ip field from bid request for test mode XRTB")
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_ipv4_for_test_mode_XRTB(self, pub_app_id, placement, hb):
        rtb = ext1_test_mode_kraken_rtb_ids_vast
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(device, 'ip')
        assert_keys_not_exist(device, 'ipv6')
        assert_that(device['ip'], equal_to(au_ip))

    @allure.feature('support ipv6')
    @allure.tag('smoke')
    @allure.story('PBJ-3258 RTB::Feature request to support ipv6 format')
    @allure.description("Verify there is ip field from bid request for meister")
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_ipv6_for_meister(self, pub_app_id, placement, hb):
        rtb = meister_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(device, 'ip')
        assert_keys_not_exist(device, 'ipv6')
        assert_that(device['ip'], equal_to(au_ip))

    @allure.feature('support ipv6')
    @allure.tag('smoke')
    @allure.story('PBJ-3258 RTB::Feature request to support ipv6 format')
    @allure.description("Verify there is ipv6 field from bid request for non test mode XRTB")
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_ipv6_for_XRTB_android(self, pub_app_id, placement, hb):
        test_ifa = gen_device_id(digital=36)
        rtb = ext1_non_test_mode_kraken_rtb_ids_vast
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_ifa, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ipv6_example_01,
                                                                        rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(device, 'ipv6')
        assert_keys_not_exist(device, 'ip')
        assert_that(device['ipv6'], equal_to(ipv6_example_01))

    @allure.feature('support ipv6')
    @allure.tag('smoke')
    @allure.story('PBJ-3258 RTB::Feature request to support ipv6 format')
    @allure.description("Verify there is ip field from bid request for test mode XRTB android")
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_ipv4_for_test_mode_XRTB_android(self, pub_app_id, placement, hb):
        rtb = ext1_test_mode_kraken_rtb_ids_vast
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(device, 'ip')
        assert_keys_not_exist(device, 'ipv6')
        assert_that(device['ip'], equal_to(au_ip))

    @allure.feature('support ipv6')
    @allure.tag('smoke')
    @allure.story('PBJ-3258 RTB::Feature request to support ipv6 format')
    @allure.description("Verify there are ipv6 and ip fields from bid request for meister android")
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_ipv6_for_meister_android(self, pub_app_id, placement, hb):
        rtb = meister_rtb_ids
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ipv6_example_01,
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(device, 'ipv6')
        assert_keys_exist(device, 'ip')
        assert_that(device['ipv6'], equal_to(ipv6_example_01))
        assert_that(device['ip'], equal_to(ipv6_example_01))

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-3210 Update ios Make & model specific for meister in bidrequest')
    @allure.description("Verify the ios Make & model specific have updated")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_specific_the_make_and_model(self, pub_app_id, placement, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=meister_rtb_ids))
        request_make = req['device']['make']
        request_model = req['device']['model']
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        bid_request_make = device['make']
        bid_request_model = device['model']
        assert_that(request_make, equal_to(bid_request_make))
        assert_that(request_model, equal_to(bid_request_model))

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-3210 Update ios Make & model specific for meister in bidrequest')
    @allure.description("Verify the ios Make & model specific have updated for kraken")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_specific_the_make_and_model_2(self, pub_app_id, placement, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))
        request_make = req['device']['make']
        request_model = req['device']['model']
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        bid_request_make = device['make']
        bid_request_model = device['model']
        assert_that(request_make, equal_to(bid_request_make))
        assert_that(request_model, equal_to(bid_request_model))

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-3210 Update ios Make & model specific for meister in bidrequest')
    @allure.description("Verify the ios Make & model specific have updated for non test mode idsp")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_specific_the_make_and_model_3(self, pub_app_id, placement, hb):
        idfv = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))
        request_make = req['device']['make']
        request_model = req['device']['model']
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        bid_request_make = device['make']
        bid_request_model = device['model']
        assert_that(request_make, equal_to(bid_request_make))
        assert_that(request_model, equal_to(bid_request_model))

    @allure.feature('device info')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3472 Update Apple\'s mobile device codes types For new apple devices')
    @allure.description("Verify the new app devices has updated for non test mode edsp")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('new_app_devices', new_app_devices)
    def test_new_app_devices_updated_non_test_mode(self, pub_app_id, placement, new_app_devices):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ua='Mozilla/5.0',
                                            model=new_app_devices["model"])
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_keys_exist(device, 'hwv')
        assert_that(device['hwv'], equal_to(new_app_devices['make']))

    @allure.feature('device info')
    @allure.tag('normal', 'test_mode', 'v1.186.0')
    @allure.story('PBJ-3472 Update Apple\'s mobile device codes types For new apple devices')
    @allure.description("Verify the new app devices has updated for test mode edsp")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('new_app_devices', new_app_devices)
    def test_new_app_devices_updated_test_mode(self, pub_app_id, placement, new_app_devices):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ua='Mozilla/5.0',
                                            model=new_app_devices["model"], ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_keys_exist(device, 'hwv')
        assert_that(device['hwv'], equal_to(new_app_devices['make']))

    @allure.feature('device info')
    @allure.tag('normal', 'test_mode', 'v1.186.0')
    @allure.story('PBJ-3472 Update Apple\'s mobile device codes types For new apple devices')
    @allure.description("Verify the new app devices has not updated for idsp")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('new_app_devices', new_app_devices)
    def test_new_app_devices_not_updated_idsp(self, pub_app_id, placement, new_app_devices):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ua='Mozilla/5.0',
                                            model=new_app_devices["model"], ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_keys_not_exist(device, 'hwv')

    @allure.feature('device info')
    @allure.tag('normal', 'v1.249.0')
    @allure.story('PBJ-4966 Bid Request modification experiment.')
    @allure.description("Verify osv mapping if it enters the DevOSV bucket of the experiment for eDSP")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['15.6.0'])
    def test_dev_osv_exp_1(self, pub_app_id, placement, osv):
        '''
            Mapping rule in the exp:
            "15.6.0": "15"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=kr_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_that(device['osv'], equal_to('15'))

    @allure.feature('device info')
    @allure.tag('normal', 'v1.249.0', 'test_mode')
    @allure.story('PBJ-4966 Bid Request modification experiment.')
    @allure.description("Verify osv will not be modified if it enters the DevOSV bucket of the experiment for iDSP")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['15.6.0'])
    def test_dev_osv_exp_2(self, pub_app_id, placement, osv):
        '''
            Mapping rule in the exp:
            "15.6.0": "15"
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=kr_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_that(device['osv'], equal_to('15.6.0'))

    @allure.feature('device info')
    @allure.tag('normal', 'v1.249.0')
    @allure.story('PBJ-4966 Bid Request modification experiment.')
    @allure.description("Verify osv mapping if it does not enter the DevOSV bucket of the experiment for eDSP")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['15.6.0'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_dev_osv_exp_3(self, pub_app_id, placement, osv, rtb):
        '''
            Mapping rule in the exp:
            "15.6.0": "15"

            AU won't enter the exp
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_that(device['osv'], equal_to('15.6.0'))

    @allure.feature('device info')
    @allure.tag('normal', 'v1.249.0')
    @allure.story('PBJ-4966 Bid Request modification experiment.')
    @allure.description("Verify osv mapping if it does not enter the experiment due to rtb black list")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['15.6.0'])
    def test_dev_osv_exp_4(self, pub_app_id, placement, osv):
        '''
            Mapping rule in the exp:
            "15.6.0": "15"

            ext_non_test_mode_kraken_rtb_ids_vast_1 in rtb_blacklist of the exp
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=kr_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_1))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_that(device['osv'], equal_to('15.6.0'))

    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.249.0')
    # @allure.story('PBJ-4966 Bid Request modification experiment.')
    # @allure.description("Verify no osv mapping if it enters the Control bucket of the experiment for eDSP")
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('osv', ['15.6.0'])
    # @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast,
    #                                  ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    # def test_dev_osv_exp_5(self, pub_app_id, placement, osv, rtb):
    #     '''
    #         Mapping rule in the exp:
    #         "15.6.0": "15"
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip, rtb_selector=rtb))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['osv'], equal_to('15.6.0'))
    #
    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.249.0', 'test_mode')
    # @allure.story('PBJ-4966 Bid Request modification experiment.')
    # @allure.description("Verify no osv mapping if it enters the Control bucket of the experiment for iDSP")
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('osv', ['15.6.0'])
    # def test_dev_osv_exp_6(self, pub_app_id, placement, osv):
    #     '''
    #         Mapping rule in the exp:
    #         "15.6.0": "15"
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip,
    #                                       rtb_selector=test_mode_kraken_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['osv'], equal_to('15.6.0'))

    @allure.feature('device info')
    @allure.tag('normal', 'v1.249.0')
    @allure.story('PBJ-4966 Bid Request modification experiment.')
    @allure.description("Verify osv mapping if it enters the DevOSV bucket of the experiment for eDSP, but no matching "
                        "from the dev os version list")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['13.99.0'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_dev_osv_exp_7(self, pub_app_id, placement, osv, rtb):
        '''
            '13.99.0' not in dev_os_version list
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=kr_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_that(device['osv'], equal_to('13.99.0'))

    @allure.feature('device info')
    @allure.tag('normal', 'v1.249.0', 'test_mode')
    @allure.story('PBJ-4966 Bid Request modification experiment.')
    @allure.description("Verify osv mapping if it enters the DevOSV bucket of the experiment for iDSP but no matching "
                        "from the dev os version list")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['13.99.0'])
    def test_dev_osv_exp_8(self, pub_app_id, placement, osv):
        '''
            '13.99.0' not in dev_os_version list
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=kr_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_that(device['osv'], equal_to('13.99.0'))

    @allure.feature('device info')
    @allure.tag('normal', 'v1.249.0')
    @allure.story('PBJ-4966 Bid Request modification experiment.')
    @allure.description("Verify that Android will enter the experiment for eDSP but device osv will not be"
                        " modified")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('osv', ['15.6.0'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_dev_osv_exp_9(self, pub_app_id, placement, osv, rtb):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=kr_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_that(device['osv'], equal_to('15.6.0'))

    @allure.feature('device info')
    @allure.tag('normal', 'v1.249.0', 'test_mode')
    @allure.story('PBJ-4966 Bid Request modification experiment.')
    @allure.description("Verify that Android will enter the experiment for iDSP but device osv will not be modified")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('osv', ['15.6.0'])
    def test_dev_osv_exp_10(self, pub_app_id, placement, osv):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=kr_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        device = bid_request['device']
        assert_that(device['osv'], equal_to('15.6.0'))

    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.258.0')
    # @allure.story('PBJ-5246 [Implementation] Bid Request modification experiment - round 4')
    # @allure.description("Verify model mapping if it enters the DevModel bucket of the experiment for eDSP")
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('model', ['iPhone 8.0'])
    # def test_dev_osv_exp_11(self, pub_app_id, placement, model):
    #     '''
    #         Mapping rule in the exp:
    #         "iPhone 8.0": "iPhone 8"
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), model=model)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['model'], equal_to('iPhone 8'))
    #
    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.258.0', 'test_mode')
    # @allure.story('PBJ-5246 [Implementation] Bid Request modification experiment - round 4')
    # @allure.description("Verify model will not be modified if it enters the DevModel bucket of the experiment for iDSP")
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('model', ['iPhone 8.0'])
    # def test_dev_osv_exp_12(self, pub_app_id, placement, model):
    #     '''
    #         Mapping rule in the exp:
    #         "iPhone 8.0": "iPhone 8"
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, model=model)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip,
    #                                       rtb_selector=test_mode_kraken_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['model'], equal_to('iPhone 8.0'))
    #
    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.258.0')
    # @allure.story('PBJ-5246 [Implementation] Bid Request modification experiment - round 4')
    # @allure.description("Verify model mapping if it does not enter the DevModel bucket of the experiment for eDSP")
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('model', ['iPhone 8.0'])
    # @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast,
    #                                  ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    # def test_dev_osv_exp_13(self, pub_app_id, placement, model, rtb):
    #     '''
    #         Mapping rule in the exp:
    #         "iPhone 8.0": "iPhone 8"
    #
    #         AU won't enter the exp
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), model=model)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['model'], equal_to('iPhone'))
    #
    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.258.0')
    # @allure.story('PBJ-5246 [Implementation] Bid Request modification experiment - round 4')
    # @allure.description("Verify model mapping if it does not enter the experiment due to rtb black list")
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('model', ['iPhone 8.0'])
    # def test_dev_osv_exp_14(self, pub_app_id, placement, model):
    #     '''
    #         Mapping rule in the exp:
    #         "iPhone 8.0": "iPhone 8"
    #
    #         ext_non_test_mode_kraken_rtb_ids_vast_1 in rtb_blacklist of the exp
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), model=model)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_1))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['model'], equal_to('iPhone'))
    #
    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.258.0')
    # @allure.story('PBJ-5246 [Implementation] Bid Request modification experiment - round 4')
    # @allure.description("Verify no model mapping if it enters the Control bucket of the experiment for eDSP")
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('model', ['iPhone 8.0'])
    # @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast,
    #                                  ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    # def test_dev_osv_exp_15(self, pub_app_id, placement, model, rtb):
    #     '''
    #         Mapping rule in the exp:
    #         "iPhone 8.0": "iPhone 8"
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), model=model)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip, rtb_selector=rtb))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['model'], equal_to('iPhone 8.0'))
    #
    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.258.0', 'test_mode')
    # @allure.story('PBJ-5246 [Implementation] Bid Request modification experiment - round 4')
    # @allure.description("Verify no model mapping if it enters the Control bucket of the experiment for iDSP")
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('model', ['iPhone 8.0'])
    # def test_dev_osv_exp_16(self, pub_app_id, placement, model):
    #     '''
    #         Mapping rule in the exp:
    #         "iPhone 8.0": "iPhone 8"
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, model=model)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip,
    #                                       rtb_selector=test_mode_kraken_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['model'], equal_to('iPhone 8.0'))
    #
    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.258.0')
    # @allure.story('PBJ-5246 [Implementation] Bid Request modification experiment - round 4')
    # @allure.description("Verify model mapping if it enters the DevModel bucket of the experiment for eDSP, but no "
    #                     "matching from the dev os version list")
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('model', ['iPhone 0'])
    # @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast,
    #                                  ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    # def test_dev_osv_exp_17(self, pub_app_id, placement, model, rtb):
    #     '''
    #         'iPhone 0' not in dev_os_version list
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), model=model)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip, rtb_selector=rtb))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['model'], equal_to('iPhone 0'))
    #
    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.258.0', 'test_mode')
    # @allure.story('PBJ-5246 [Implementation] Bid Request modification experiment - round 4')
    # @allure.description("Verify model mapping if it enters the DevModel bucket of the experiment for iDSP but no "
    #                     "matching from the dev os version list")
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('model', ['iPhone 0'])
    # def test_dev_osv_exp_18(self, pub_app_id, placement, model):
    #     '''
    #         'iPhone 0' not in dev_os_version list
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, model=model)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip,
    #                                       rtb_selector=test_mode_kraken_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['model'], equal_to('iPhone 0'))
    #
    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.258.0')
    # @allure.story('PBJ-5246 [Implementation] Bid Request modification experiment - round 4')
    # @allure.description("Verify that Android will enter the experiment for eDSP and device model will be modified")
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('placement', [android_common_test_placement])
    # @pytest.mark.parametrize('model', ['Sumsung S11'])
    # @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast,
    #                                  ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    # def test_dev_osv_exp_19(self, pub_app_id, placement, model, rtb):
    #     '''
    #         Mapping rule in the exp:
    #         "Sumsung S11": "S11"
    #     '''
    #     req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id(), model=model)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip, rtb_selector=rtb))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['model'], equal_to('S11'))
    #
    # @allure.feature('device info')
    # @allure.tag('normal', 'v1.258.0', 'test_mode')
    # @allure.story('PBJ-5246 [Implementation] Bid Request modification experiment - round 4')
    # @allure.description("Verify that Android will enter the experiment for iDSP but device model will not be modified")
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('placement', [android_common_test_placement])
    # @pytest.mark.parametrize('model', ['Sumsung S11'])
    # def test_dev_osv_exp_20(self, pub_app_id, placement, model):
    #     '''
    #         Mapping rule in the exp:
    #         "Sumsung S11": "S11"
    #     '''
    #     req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=test_mode_device_id, model=model)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=kr_ip,
    #                                       rtb_selector=test_mode_kraken_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     device = bid_request['device']
    #     assert_that(device['model'], equal_to('Sumsung S11'))