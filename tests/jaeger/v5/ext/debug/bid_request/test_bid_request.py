from collections import Counter

import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain, get_device_info
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestBidRequest(object):

    @allure.feature('basic')
    @allure.tag('test_mode', 'smoke', 'basic')
    @allure.story('bid request test mode')
    @allure.description('Test for enable test mode by device id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_enable_test_mode_by_device_id(self, pub_app_id):
        rtb = test_mode_kraken_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('test_mode', 'smoke')
    @allure.story('test mode device support')
    @allure.description('Test for enable test mode by test mode pub app - windows device')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5b8d17307ad5a86fc53c7c8a'])
    def test_for_enable_test_mode_by_pub_app(self, pub_app_id):
        rtb = test_mode_kraken_rtb_ids
        req = request_payload.jaeger_v5_windows(pub_app_id, 'DEFAULT-4642078', ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version='VungleWindows/6.4.0 (Windows 10; native)', debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('test_mode', 'smoke')
    @allure.story('test mode device support')
    @allure.description('Test for test mode amazon device support')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5bebe77a598bee2c619dca28'])
    def test_for_test_mode_amazon(self, pub_app_id):
        rtb = test_mode_kraken_rtb_ids
        req = request_payload.jaeger_v5_amazon(pub_app_id, 'DEFAULT-8228620', ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='VungleDroid/6.3.2', debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('test_mode', 'smoke')
    @allure.story('test mode ad type support')
    @allure.description('Test for test mode mrec support')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_test_mode_mrec(self, pub_app_id):
        rtb = test_mode_kraken_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, 'MREC-TEST-01', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.4.0', debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('test_mode', 'smoke')
    @allure.story('test mode ad type support')
    @allure.description('Test for test mode banner support')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_test_mode_banner(self, pub_app_id):
        rtb = test_mode_kraken_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['test'], equal_to(1))

    @allure.feature('user privacy')
    @allure.tag('smoke', 'test_mode', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify gdpr status from debug with non eu country ip but user consent in request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_gdpr_non_eu_country_after_v6(self, pub_app_id, consent_status):
        rtb = test_mode_kraken_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if consent_status in (None, 'unknown', 'opted_out_by_timeout'):
                assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))
            else:
                assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
        else:
            assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))

    @allure.feature('user privacy')
    @allure.tag('smoke', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify gdpr status from debug with eu country ip but user consent in request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_gdpr_eu_country_after_v6(self, pub_app_id, consent_status):
        rtb = meister_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if consent_status is None:
            assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))
        else:
            assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify gdpr status from debug with non eu country in case of pre v6')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_gdpr_non_eu_country_pre_v6(self, pub_app_id, consent_status):
        rtb = meister_rtb_ids
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=non_eu_country_ip, sdk_version='Vungle/5.9.9',
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_in':
                assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
                assert_that(bid_request['user']['ext']['consent'], equal_to(1))
            elif consent_status == 'opted_out':
                assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
                assert_that(bid_request['user']['ext']['consent'], equal_to(0))
            else:
                assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))
        else:
            assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify gdpr status from debug with eu country in case of pre v6 flag is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_gdpr_eu_country_pre_v6_true(self, pub_app_id, consent_status):
        rtb = meister_rtb_ids
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, sdk_version='Vungle/5.9.9',
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_in':
                assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
                assert_that(bid_request['user']['ext']['consent'], equal_to(1))
            else:
                assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
                assert_that(bid_request['user']['ext']['consent'], equal_to(0))
        else:
            assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
            assert_that(bid_request['user']['ext']['consent'], equal_to(0))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify gdpr status from debug with eu country in case of pre v6 flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_gdpr_eu_country_pre_v6_false(self, pub_app_id, consent_status):
        rtb = meister_rtb_ids
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, sdk_version='Vungle/5.9.9',
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
        assert_that(bid_request['user']['ext']['consent'], equal_to(1))

    @allure.feature('user privacy')
    @allure.tag('smoke', 'test_mode')
    @allure.story('GDPR')
    @allure.description('Verify consent status opted in from debug in GDPR status')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_gdpr_opted_in(self, pub_app_id):
        rtb = test_mode_kraken_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr='opted_in', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                                                        rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
        assert_that(bid_request['user']['ext']['consent'], equal_to(1))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('GDPR')
    @allure.description('Verify consent status opted out from debug in GDPR status')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_gdpr_opted_out(self, pub_app_id):
        rtb = meister_rtb_ids
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr='opted_out', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                                                        rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['user']['ext']['consent'], equal_to(0))
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))

    @allure.feature('user privacy')
    @allure.tag('smoke', 'test_mode')
    @allure.story('GDPR')
    @allure.description('Verify consent status from debug not in GDPR status in case of Legitimate Interest is true')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    def test_gdpr_legitimate_interest_true(self, pub_app_id, consent_status):
        rtb = test_mode_kraken_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        if consent_status is None:
            assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))
        else:
            assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))
            assert_that(bid_request['user']['ext']['consent'], equal_to(1))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('GDPR')
    @allure.description('Verify consent status from debug in GDPR status in case of Legitimate Interest is false')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    def test_gdpr_legitimate_interest_false(self, pub_app_id, consent_status):
        rtb = meister_rtb_ids
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if consent_status is None:
            assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))
        else:
            assert_that(bid_request['user']['ext']['consent'], equal_to(0))
            assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3712 RTB :: Change user.ext.consent to string')
    @allure.description(
        'Verify consent support string when "supported_extension_type":"ConsentString" in rtbconnection')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    def test_supported_consent_to_string(self, pub_app_id, consent_status):
        rtb = ext_non_test_mode_kraken_rtb_consentString
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        if consent_status is None:
            # PBJ-4874 Deprecate
            assert_that(bid_request['user']['ext']['consent'], equal_to(0))
        else:
            # PBJ-4874 Deprecate
            assert_that(bid_request['user']['ext']['consent'], equal_to(1))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3712 RTB :: Change user.ext.consent to string')
    @allure.description(
        'Verify consent support string when "supported_extension_type":"ConsentString" in rtbconnection on test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    def test_supported_consent_to_string_test_mode(self, pub_app_id, consent_status):
        rtb = ext_test_mode_kraken_rtb_consentString
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # PBJ-4874 Deprecate
        if consent_status is None:
            assert_that(bid_request['user']['ext']['consent'], equal_to(0))
        else:
            assert_that(bid_request['user']['ext']['consent'], equal_to(1))

    @allure.feature('user privacy')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify consent support string for rtb support extension type=default_consentstring')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    def test_supported_default_consent_to_string(self, pub_app_id, placement, consent_status):
        rtb = ext1_non_kraken_test_mode_default_consentstring
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, gdpr=consent_status,
                                            ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        if consent_status is None:
            assert_that(bid_request['user']['ext']['consent'], equal_to("0"))
        else:
            assert_that(bid_request['user']['ext']['consent'], equal_to("1"))



    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3862 Do not pass Appset ID in GDPR traffic if consent is not given')
    @allure.description('Verify the AppSet ID is filter for consent = 0  via edsp for android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_filter_out_appset_id_edsp_android(self, pub_app_id):
        test_ifa = gen_device_id()
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, gdpr='opted_out',
                                                app_set_id=test_ifa, android_id='')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['device']['ext'], 'app_set_id')
        device_info = get_device_info(r.json())
        assert_that(device_info['source'], 'Vungle_FP')


    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3862 Do not pass Appset ID in GDPR traffic if consent is not given')
    @allure.description('Verify the AppSet ID is filter for consent = 0  via idsp for android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_filter_out_appset_id_idsp_android(self, pub_app_id):
        test_ifa = gen_device_id()
        rtb = non_test_mode_kraken_rtb_ids
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, gdpr='opted_out',
                                                app_set_id=test_ifa, android_id='')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['device']['ext']['vungle'], 'app_set_id')
        assert_that(bid_request['device']['ext']['vungle']['id_source'], 'Vungle_FP')


    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3862 Do not pass Appset ID in GDPR traffic if consent is not given')
    @allure.description('Verify the AppSet ID is filter for consent = 0  via edsp for android')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    def test_filter_out_appset_id_edsp_amazon(self, pub_app_id):
        test_ifa = test_mode_device_id
        rtb = ext_test_mode_kraken_rtb_ids_vast
        req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement, gdpr='opted_out',
                                               app_set_id=test_ifa, ifa='')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['device']['ext'], 'app_set_id')
        device_info = get_device_info(r.json())
        assert_that(device_info['source'], 'Vungle_FP')


    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3862 Do not pass Appset ID in GDPR traffic if consent is not given')
    @allure.description('Verify the AppSet ID is filter for consent = 0  via idsp for android')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    def test_filter_out_appset_id_idsp_amazon(self, pub_app_id):
        test_ifa = test_mode_device_id
        rtb = test_mode_kraken_rtb_ids
        req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement, gdpr='opted_out',
                                               app_set_id=test_ifa, ifa='')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['device']['ext']['vungle'], 'app_set_id')
        assert_that(bid_request['device']['ext']['vungle']['id_source'], 'Vungle_FP')



    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('CCPA support')
    @allure.description('Verify us_privacy in case of CCPA status opted out')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('ccpa_status', ['opted_out'])
    @pytest.mark.parametrize('ip', [ca_us_ip, eu_country_ip])
    def test_ccpa_status_opted_out(self, pub_app_id, ccpa_status, ip):
        rtb = meister_rtb_ids
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ccpa=ccpa_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-Y-'))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('CCPA support')
    @allure.description('Verify us_privacy in case of CCPA status opted out by location')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ccpa_status_opted_out_flag_1(self, pub_app_id):
        '''
        Account level setting:
        "is_ccpa_opt_out": true
        '''
        rtb = meister_rtb_ids
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-Y-'))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('CCPA support')
    @allure.description('Verify us_privacy in case of CCPA status opted in by location')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_ccpa_status_opted_in_flag_1(self, pub_app_id):
        '''
        Account level setting:
        "is_ccpa_opt_out": false
        '''
        rtb = meister_rtb_ids
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-N-'))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('CCPA support')
    @allure.description('Verify us_privacy in case of CCPA status repect the external consent')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('ccpa_status', ['opted_in'])
    def test_ccpa_status_opted_out_respect_external_consent(self, pub_app_id, ccpa_status):
        rtb = meister_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ccpa=ccpa_status,
                                            ifa=ccpa_external_consents_opted_out_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-Y-'))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('CCPA support')
    @allure.description('Verify us_privacy in case of CCPA status opted in or in other value')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('ccpa_status', ['opted_in', 'test'])
    def test_ccpa_status_opted_in(self, pub_app_id, ccpa_status):
        rtb = meister_rtb_ids
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ccpa=ccpa_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-N-'))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('CCPA support')
    @allure.description('Verify us_privacy in case of CCPA status not exist')
    @allure.severity('smoke')
    @pytest.mark.parametrize('data', [{"app": common_test_app, "placement": common_test_placement},
                                      {"app": "5c003b9a3933314cf38ff7f3", "placement": "DEFAULT-5045327"}])
    def test_ccpa_status_not_exist(self, data):
        rtb = meister_rtb_ids
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(data['app'], data['placement'], ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1---'))

    @allure.feature('coppa support')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1466 COPPA at the placement level setting')
    @allure.description('Verify coppa field with placement level true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_coppa_placement_level_t(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": true

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('coppa support')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1466 COPPA at the placement level setting')
    @allure.description('Verify coppa field with placement level false but app level true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_coppa_placement_level_f_app_t(self, pub_app_id):
        """
        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'AREYOUS82690', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('coppa support')
    @allure.tag('normal', 'test mode')
    @allure.story('PBJ-3557 Treat UK traffic as COPPA traffic for all apps under Rovio account')
    @allure.description('Verify coppa field with placement level true for app under Rovio account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c0525848c30ee3a6ca2bcc6'])
    @pytest.mark.parametrize('placement', ['DEFAULT-5757423'])
    def test_coppa_placement_level_for_Rovio(self, pub_app_id, placement):
        """

        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": true

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1,
                                                                        src_ip=gb_ip))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('coppa support')
    @allure.tag('normal', 'test mode')
    @allure.story('PBJ-3557 Treat UK traffic as COPPA traffic for all apps under Rovio account')
    @allure.description('Verify coppa field with placement level false and ip is GB for app under Rovio account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c0525848c30ee3a6ca2bcc6'])
    @pytest.mark.parametrize('placement', ['REWARD_VIDEO-4062180'])
    def test_coppa_placement_level_for_Rovio_02(self, pub_app_id, placement):
        """

        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1,
                                                                        src_ip=gb_ip))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('coppa support')
    @allure.tag('normal', 'test mode')
    @allure.story('PBJ-3557 Treat UK traffic as COPPA traffic for all apps under Rovio account')
    @allure.description('Verify coppa field with placement level false and ip is not gb for app under Rovio account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c0525848c30ee3a6ca2bcc6'])
    @pytest.mark.parametrize('placement', ['REWARD_VIDEO-4062180'])
    def test_coppa_placement_level_for_Rovio_03(self, pub_app_id, placement):
        """

        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1,
                                                                        src_ip=jp_ip))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('coppa support')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-3557 Treat UK traffic as COPPA traffic for all apps under Rovio account')
    @allure.description('Verify coppa field with app level false and ip is gb for app under Rovio account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5a13d15693d318b46c0087e9'])
    def test_coppa_placement_level_for_Rovio_04(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'REWARDV84499', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1, src_ip=gb_ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('coppa support')
    @allure.tag('normal', 'test mode')
    @allure.story('PBJ-3557 Treat UK traffic as COPPA traffic for all apps under Rovio account')
    @allure.description('Verify coppa field with app level false and ip is not gb for app under Rovio account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5a13d15693d318b46c0087e9'])
    def test_coppa_placement_level_for_Rovio_05(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'REWARDV84499', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1, src_ip=au_ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3557 Treat UK traffic as COPPA traffic for all apps under Rovio account')
    @allure.description('Verify coppa field with app level false and ip is gb for app under Rovio account')
    @pytest.mark.parametrize('pub_app_id', ['5a13d15693d318b46c0087e9'])
    def test_coppa_placement_level_for_Rovio_06(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'REWARDV84499', coppa=False,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1,
                                                                        src_ip=gb_ip))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3557 Treat UK traffic as COPPA traffic for all apps under Rovio account')
    @allure.description('Verify coppa field with app level false and ip is not gb for app under Rovio account')
    @pytest.mark.parametrize('pub_app_id', ['5a13d15693d318b46c0087e9'])
    def test_coppa_placement_level_for_Rovio_07(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'REWARDV84499', coppa=False,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1,
                                                                        src_ip=au_ip))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3557 Treat UK traffic as COPPA traffic for all apps under Rovio account')
    @allure.description('Verify coppa field with app level true and request false and ip is gb for '
                        'app under Rovio account')
    @pytest.mark.parametrize('pub_app_id', ['5c0525848c30ee3a6ca2bcc6'])
    def test_coppa_placement_level_for_Rovio_08(self, pub_app_id):
        """

              App level setting:
              "isCoppaCompliant": true

              Placement level setting:
              "is_coppa": true

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5757423', coppa=False,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1,
                                                                        src_ip=gb_ip))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3557 Treat UK traffic as COPPA traffic for all apps under Rovio account')
    @allure.description('Verify coppa field with app level true and request false and ip is not gb for '
                        'app under Rovio account')
    @pytest.mark.parametrize('pub_app_id', ['5c0525848c30ee3a6ca2bcc6'])
    def test_coppa_placement_level_for_Rovio_09(self, pub_app_id):
        """

              App level setting:
              "isCoppaCompliant": true

              Placement level setting:
              "is_coppa": true

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5757423', coppa=False,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1,
                                                                        src_ip=au_ip))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('coppa support')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1466 COPPA at the placement level setting')
    @allure.description('Verify coppa field with app level true and no placement level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_coppa_app_level(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": true

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50918', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('coppa support')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1466 COPPA at the placement level setting')
    @allure.description('Verify no coppa field with app level false and no placement level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_no_coppa(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('coppa support')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1466 COPPA at the placement level setting')
    @allure.description('Verify coppa field with app level false and placement level true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_coppa_app_f_placement_t(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": true

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'COPPA-TEST', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads and in pub dash is both true')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_coppa_setting_in_dash(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": true

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement,
                                            ifa=test_mode_device_id, coppa=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads and in pub dash is both true for meister')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_coppa_setting_in_dash_meister(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": true

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement,
                                            ifa=gen_device_id(), coppa=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads and in pub dash is both true for edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_coppa_setting_in_dash_edsp(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": true

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement,
                                            ifa=gen_device_id(), coppa=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                                                        rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is true but in pub dash is false')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_coppa_setting_in_dash_01(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'COPPA-TEST_01', coppa=True,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is true but in pub dash is false for meister')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_coppa_setting_in_dash_meister_01(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'COPPA-TEST_01', coppa=True,
                                            ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is true but in pub dash is false for edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_coppa_setting_in_dash_edsp_01(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'COPPA-TEST_01', coppa=True,
                                            ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                                                        rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is false and in pub dash is false')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_coppa_setting_in_dash_02(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'COPPA-TEST_01', coppa=False,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is False and in pub dash is false for meister')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_coppa_setting_in_dash_meister_02(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'COPPA-TEST_01', coppa=False,
                                            ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is False and in pub dash is false for edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_coppa_setting_in_dash_edsp_02(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": false

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'COPPA-TEST_01', coppa=False,
                                            ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                                                        rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is true and in pub dash is false')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_coppa_setting_in_dash_03(self, pub_app_id):
        """

        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": true

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement,
                                            ifa=test_mode_device_id, coppa=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is true and in pub dash is false for meister')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_coppa_setting_in_dash_meister_03(self, pub_app_id):
        '''

        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": true

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement,
                                            ifa=gen_device_id(), coppa=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is true and in pub dash is false for edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_coppa_setting_in_dash_edsp_03(self, pub_app_id):
        '''

        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": true

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement,
                                            ifa=gen_device_id(), coppa=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                                                        rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is true and in pub dash is false on android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_coppa_setting_in_dash_on_android(self, pub_app_id):
        '''

        App level setting:
        "isCoppaCompliant": false
        '''
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=test_mode_device_id, coppa=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is false and in pub dash is false on android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_coppa_setting_in_dash_on_android_01(self, pub_app_id):
        '''

        App level setting:
        "isCoppaCompliant": false
        '''
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=test_mode_device_id, coppa=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is true and in pub dash is true on android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_coppa_setting_in_dash_on_android_02(self, pub_app_id):
        '''

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": true

        '''
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                android_id=test_mode_device_id, coppa=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3498 [COPPA] jaeger process coppa flag from ads endpoint')
    @allure.description('Verify coppa value set in ads is false and in pub dash is true on android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_coppa_setting_in_dash_on_android_03(self, pub_app_id):
        '''

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": true

        '''
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                android_id=test_mode_device_id, coppa=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    # # -------------------------below cases are for disable_ad_id_if_coppa=False-----------------------------------------
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # def test_zero_out_gaid_for_android_01_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     test_id = ''
    #     ifa = ''
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
    #                                             android_id=test_id, ifa=ifa)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
    #                                                                     src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_not_exist(bid_request['regs'], 'coppa')
    #     assert_keys_not_exist(bid_request, 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_keys_exist(device_ext_vungle, 'isu')
    #     assert_that(device_ext_vungle['isu'], is_not(test_id))
    #     assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # def test_zero_out_gaid_for_android_02_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     test_id = ''
    #     ifa = ''
    #     req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                             android_id=test_id, ifa=ifa)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_that(bid_request['regs']['coppa'], equal_to(1))
    #     assert_keys_not_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_keys_exist(device_ext_vungle, 'isu')
    #     assert_that(device_ext_vungle['isu'], is_not(test_id))
    #     assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #
    #
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # def test_zero_out_gaid_for_android_03_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
    #                                             android_id=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_not_exist(bid_request['regs'], 'coppa')
    #     assert_keys_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_keys_exist(device_ext_vungle, 'isu')
    #     assert_that(device_ext_vungle['isu'], test_id)
    #     assert_that(device_ext_vungle['id_source'], equal_to('IFA'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # def test_zero_out_gaid_for_android_04_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                             android_id=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_that(bid_request['regs']['coppa'], equal_to(1))
    #     assert_keys_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_keys_exist(device_ext_vungle, 'isu')
    #     assert_that(device_ext_vungle['isu'], test_id)
    #     assert_that(device_ext_vungle['id_source'], equal_to('IFA'))
    #
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_07_false(self, pub_app_id, sdk_v):
    #     """
    #
    #    App level setting:
    #    "isCoppaCompliant": false
    #    """
    #     test_id = ''
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=False,
    #                                              android_id=test_id, ifa='')
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_not_exist(bid_request['regs'], 'coppa')
    #     assert_keys_not_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_keys_exist(device_ext_vungle, 'isu')
    #     assert_that(device_ext_vungle, is_not(test_id))
    #     assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_08_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     test_id = ''
    #     req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                             android_id="", ifa="")
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_exist(bid_request['regs'], 'coppa')
    #     assert_keys_not_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_keys_exist(device_ext_vungle, 'isu')
    #     assert_that(device_ext_vungle, is_not(test_id))
    #     assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify non zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_09_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     test_device_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
    #                                             android_id=test_device_id, coppa=False)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_not_exist(bid_request['regs'], 'coppa')
    #     assert_keys_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['isu'], equal_to(test_device_id))
    #     assert_that(device_ext_vungle['id_source'], equal_to("IFA"))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_10_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     test_device_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                             android_id=test_device_id, coppa=False)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_not_exist(bid_request['regs'], 'coppa')
    #     assert_keys_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['isu'], equal_to(test_device_id))
    #     assert_that(device_ext_vungle['id_source'], equal_to('IFA'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_11_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     test_device_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
    #                                             android_id=test_device_id, coppa=True)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_exist(bid_request['regs'], 'coppa')
    #     assert_keys_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['isu'], equal_to(test_device_id))
    #     assert_that(device_ext_vungle['id_source'], equal_to('IFA'))
    #
    #
    #
    # # -------------------------below cases are for disable_ad_id_if_coppa=False and GDPR exists------------------------
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    # def test_zero_out_gaid_with_gdpr_for_android_01_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     test_id = ''
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
    #                                             android_id=test_id, ifa='', gdpr=consent_status)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
    #                                                                     src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_not_exist(bid_request['regs'], 'coppa')
    #     assert_keys_not_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #     assert_that(device_ext_vungle['isu'], is_not(test_id))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    # def test_zero_out_gaid_with_gdpr_for_android_02_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     test_id = ''
    #     req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                             android_id=test_id, ifa='', gdpr=consent_status)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_that(bid_request['regs']['coppa'], equal_to(1))
    #     assert_keys_not_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['isu'], is_not(test_id))
    #     assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #
    #
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    # def test_zero_out_gaid_with_gdpr_for_android_03_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
    #                                             android_id=test_id, gdpr=consent_status)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['isu'], is_not(test_id))
    #     assert_that(device_ext_vungle['id_source'], equal_to('GDPR'))
    #
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    # def test_zero_out_gaid_with_gdpr_for_android_04_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                             android_id=test_id, gdpr=consent_status)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_that(bid_request['regs']['coppa'], equal_to(1))
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['id_source'], equal_to('GDPR'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_zero_out_gaid_with_gdpr_for_android_07_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #
    #    App level setting:
    #    "isCoppaCompliant": false
    #    """
    #     test_id = ''
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=False,
    #                                             android_id=test_id, ifa="", gdpr=consent_status)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_not_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_zero_out_gaid_with_gdpr_for_android_08_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa', gdpr=consent_status,
    #                                             android_id="", ifa="")
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify non zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_zero_out_gaid_with_gdpr_for_android_09_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, gdpr=consent_status,
    #                                             android_id=gen_device_id(), coppa=False)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_not_exist(bid_request['regs'], 'coppa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['id_source'], equal_to('GDPR'))
    #
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_zero_out_gaid_with_gdpr_for_android_10_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa', gdpr=consent_status,
    #                                             android_id=gen_device_id(), coppa=False)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_not_exist(bid_request['regs'], 'coppa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['id_source'], equal_to('GDPR'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_zero_out_gaid_with_gdpr_for_android_11_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
    #                                             android_id=gen_device_id(), coppa=True, gdpr=consent_status)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                                                     rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_exist(bid_request['regs'], 'coppa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['id_source'], equal_to('GDPR'))

    # -------------------------below cases are for disable_ad_id_if_coppa=True------------------------------------------

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_for_android_01_true(self, pub_app_id, sdk_v):
        """

        App level setting:
        "isCoppaCompliant": false
        """
        test_id = ''
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=test_id, ifa="")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                                                        src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_not_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request, 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['isu'], is_not(test_id))
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_for_android_02_true(self, pub_app_id, sdk_v):
        """
        Placement level setting:
        "is_coppa": true
        """
        test_id = ''
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                android_id=test_id, ifa="")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(bid_request['regs']['coppa'], equal_to(1))
        assert_keys_not_exist(bid_request['device'], 'ifa')
        assert_that(device_ext_vungle['isu'], is_not(test_id))
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_for_android_05_true(self, pub_app_id, sdk_v):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, ifa=test_id,
                                                android_id=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip, sdk_version=sdk_v,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_not_exist(bid_request['regs'], 'coppa')
        assert_keys_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['isu'], equal_to(test_id))
        assert_that(device_ext_vungle['id_source'], equal_to('IFA'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_zero_out_gaid_for_app_set_id_05_true(self, pub_app_id, sdk_v, header_bidding):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, ifa=test_id,
                                                app_set_id=test_id, android_id='', header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip, sdk_version=sdk_v,
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
        assert_keys_not_exist(bid_request['regs'], 'coppa')
        assert_keys_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['app_set_id'], equal_to(test_id))
        assert_that(device_ext_vungle['id_source'], equal_to('IFA'))



    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # @pytest.mark.parametrize('header_bidding', [True, False])
    # def test_zero_out_gaid_for_app_set_id_05_false(self, pub_app_id, sdk_v, header_bidding):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, ifa='',
    #                                             app_set_id=test_id, android_id='', header_bidding=header_bidding)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip, sdk_version=sdk_v,
    #                                                                     rtb_selector=meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
    #     assert_keys_not_exist(bid_request['regs'], 'coppa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_keys_exist(device_ext_vungle['id_source'], 'AppSetID')
    #     assert_that(device_ext_vungle['app_set_id'], equal_to(test_id))




    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('empty_device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-'])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_zero_out_gaid_for_app_set_id_05_false_01(self, pub_app_id, sdk_v, empty_device_id, header_bidding):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, ifa='',
                                                app_set_id=empty_device_id, android_id='', header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip, sdk_version=sdk_v,
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
        assert_keys_not_exist(bid_request['regs'], 'coppa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_keys_exist(device_ext_vungle['id_source'], 'Vungle_FP')




    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_for_android_06_true(self, pub_app_id, sdk_v):
        """
           Placement level setting:
           "is_coppa": true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                android_id=gen_device_id(), ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip, sdk_version=sdk_v,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))


    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_for_app_set_id_06_true(self, pub_app_id, sdk_v):
        """
           Placement level setting:
           "is_coppa": true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa', android_id='',
                                                app_set_id=gen_device_id(), ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip, sdk_version=sdk_v,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))



    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    def test_zero_out_gaid_for_android_07_true(self, pub_app_id, sdk_v):
        """

       App level setting:
       "isCoppaCompliant": false
       """
        test_id = ''
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=False,
                                                android_id=test_id, ifa="")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_not_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))


    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    def test_zero_out_gaid_for_android_08_true(self, pub_app_id, sdk_v):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    def test_zero_out_gaid_for_app_set_id_08_true(self, pub_app_id, sdk_v):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa', android_id='',
                                                app_set_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))



    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'v1.226.0')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag'
                  'PBJ-4399 Jaeger - Treat 0000-0000 as empty IFA')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('empty_device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-'])
    def test_zero_out_gaid_for_android_12_true(self, pub_app_id, sdk_v, empty_device_id):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                ifa=empty_device_id,
                                                android_id=empty_device_id, coppa=True,
                                                )
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=jp_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('empty_device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-'])
    def test_zero_out_gaid_for_android_12_1_true(self, pub_app_id, sdk_v, empty_device_id):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                ifa=empty_device_id,
                                                android_id=empty_device_id, coppa=True,
                                                )
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=jp_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    # ----------- below test cases are for coppa_preference=2 (means prefer api's value) and sdk_v>=6.10.4--------------

    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_preference2_on_android_1(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
       """

        test_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=coppa,
                                                android_id=test_id, ifa="")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        if coppa:
            assert_keys_exist(bid_request['regs'], 'coppa')
            assert_keys_not_exist(bid_request['device'], 'ifa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
        else:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('ISU'))

    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 and '
                        'send zero ifa on android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    @pytest.mark.parametrize('empty_device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-'])
    def test_coppa_preference2_on_zero_ifa_android_1(self, pub_app_id, sdk_v, coppa, empty_device_id):
        """
        App level setting:
        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
       """

        test_id = empty_device_id
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=coppa,
                                                android_id=test_id, ifa="")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        if coppa:
            assert_keys_exist(bid_request['regs'], 'coppa')
            assert_keys_not_exist(bid_request['device'], 'ifa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
        else:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))


    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_preference2_on_android_2(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": true
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
       """

        test_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_coppa_placememt, coppa=coppa,
                                                android_id=test_id, ifa="")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        if coppa is False:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('ISU'))

        else:
            assert_keys_exist(bid_request['regs'], 'coppa')
            assert_keys_not_exist(bid_request['device'], 'ifa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on amazon platform')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    @pytest.mark.parametrize('empty_device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-'])
    def test_coppa_preference2_on_amazon_1(self, pub_app_id, sdk_v, coppa, empty_device_id):
        """
        App level setting:
        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
       """
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        test_id = empty_device_id
        req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement, coppa=coppa,
                                               ifa=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        bid_response_device_info = response_payload['ext']['debug']['auction_result']['device_info']
        if coppa:
            assert_keys_exist(bid_request['regs'], 'coppa')
            assert_that(bid_response_device_info['source'], equal_to('Vungle_FP'))
        else:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            device = bid_request['device']
            assert_that(device['ifa'], equal_to(test_id))


    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 and '
                        'zero ifa on amazon platform')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_preference2_zero_ifa_on_amazon_1(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
       """
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        test_id = test_mode_device_id
        req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement, coppa=coppa,
                                               ifa=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        bid_response_device_info = response_payload['ext']['debug']['auction_result']['device_info']
        if coppa:
            assert_keys_exist(bid_request['regs'], 'coppa')
            assert_that(bid_response_device_info['source'], equal_to('IFA'))
        else:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            device = bid_request['device']
            assert_that(device['ifa'], equal_to(test_id))



    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_preference2_on_ios_1(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": true
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
       """
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, coppa=coppa,
                                            ifa=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
        if coppa is False:
            assert_keys_not_exist(bid_request['regs'], 'coppa')

        else:
            assert_keys_exist(bid_request['regs'], 'coppa')

    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_preference2_on_ios_2(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
       """
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', coppa=coppa,
                                            ifa=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
        if coppa is True:
            assert_keys_exist(bid_request['regs'], 'coppa')

        else:
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on windows platform')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_preference2_on_windows_1(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
       """
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_windows(pub_app_id, windows_common_test_placement, coppa=coppa,
                                                ashwid=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
        if coppa is True:
            assert_keys_exist(bid_request['regs'], 'coppa')

        else:
            assert_keys_not_exist(bid_request['regs'], 'coppa')

    # ----------- below test cases are for coppa_preference=1 (means dashboard+api value) and sdk_v>=6.10.4-------------
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on android platform')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_preference1_on_android_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=coppa,
    #                                             android_id=test_id, ifa="")
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                       rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     if coppa:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #         assert_keys_not_exist(bid_request['device'], 'ifa')
    #         device_ext_vungle = bid_request['device']['ext']['vungle']
    #         assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')
    #         device_ext_vungle = bid_request['device']['ext']['vungle']
    #         assert_that(device_ext_vungle['id_source'], equal_to('ISU'))
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 and '
    #                     'send zero ifa on android platform')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_preference1_on_zero_ifa_android_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #
    #     test_id = '00000000-0000-0000-0000-000000000000'
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=coppa,
    #                                             android_id=test_id, ifa="")
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                       rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     if coppa:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #         assert_keys_not_exist(bid_request['device'], 'ifa')
    #         device_ext_vungle = bid_request['device']['ext']['vungle']
    #         assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')
    #         device_ext_vungle = bid_request['device']['ext']['vungle']
    #         assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on android platform')
    # @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_preference1_on_android_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": true
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
    #    """
    #
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_coppa_placememt, coppa=coppa,
    #                                             android_id=test_id, ifa="")
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                       rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_exist(bid_request['regs'], 'coppa')
    #     assert_keys_not_exist(bid_request['device'], 'ifa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on amazon platform')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_preference1_zero_ifa_on_amazon_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #     if env == 'ci':
    #         rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
    #     elif env == 'qa' or env == 'regression':
    #         rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
    #     test_id = '00000000-0000-0000-0000-000000000000'
    #     req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement, coppa=coppa,
    #                                            ifa=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
    #                                       rtb_selector=rtb))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #     bid_response_device_info = response_payload['ext']['debug']['auction_result']['device_info']
    #     if coppa:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #         assert_that(bid_response_device_info['source'], equal_to('Vungle_FP'))
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')
    #         device = bid_request['device']
    #         assert_that(device['ifa'], equal_to(test_id))
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 and '
    #                     'zero ifa on amazon platform')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_preference1_on_amazon_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #     if env == 'ci':
    #         rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
    #     elif env == 'qa' or env == 'regression':
    #         rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
    #     test_id = test_mode_device_id
    #     req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement, coppa=coppa,
    #                                            ifa=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
    #                                       rtb_selector=rtb))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #     bid_response_device_info = response_payload['ext']['debug']['auction_result']['device_info']
    #     if coppa:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #         assert_that(bid_response_device_info['source'], equal_to('IFA'))
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')
    #         device = bid_request['device']
    #         assert_that(device['ifa'], equal_to(test_id))
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on ios platform')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_preference1_on_ios_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": true
    #     case:
    #     coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
    #    """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, coppa=coppa,
    #                                         ifa=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
    #                                       rtb_selector=meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
    #     assert_keys_exist(bid_request['regs'], 'coppa')
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on ios platform')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_preference1_on_ios_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', coppa=coppa,
    #                                         ifa=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
    #                                       rtb_selector=meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
    #     if coppa is True:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on windows platform')
    # @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_preference1_on_windows_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_windows(pub_app_id, windows_common_test_placement, coppa=coppa,
    #                                             ashwid=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
    #                                       rtb_selector=meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
    #     if coppa is True:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')

    # ----------- below test cases are for no legal_config in DB and sdk_v>=6.10.4-------------

    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
    #               'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on android platform')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_no_config_android_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     no legal config; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=coppa,
    #                                             android_id=test_id, ifa="")
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                       rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     if coppa:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #         device_ext_vungle = bid_request['device']['ext']['vungle']
    #         assert_that(device_ext_vungle['id_source'], equal_to('ISU'))
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')
    #         device_ext_vungle = bid_request['device']['ext']['vungle']
    #         assert_that(device_ext_vungle['id_source'], equal_to('ISU'))
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
    #               'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 and '
    #                     'send zero ifa on android platform')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_no_config_on_zero_ifa_android_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     no legal config; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #
    #     test_id = '00000000-0000-0000-0000-000000000000'
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=coppa,
    #                                             android_id=test_id, ifa="")
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                       rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     if coppa:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #         assert_keys_not_exist(bid_request['device'], 'ifa')
    #         device_ext_vungle = bid_request['device']['ext']['vungle']
    #         assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')
    #         device_ext_vungle = bid_request['device']['ext']['vungle']
    #         assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
    #               'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on android platform')
    # @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_no_config_on_android_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": true
    #     case:
    #     no legal cofig; is_coppa(api):% coppa; is_coppa(dashboard):true;
    #    """
    #
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_android(pub_app_id, android_common_coppa_placememt, coppa=coppa,
    #                                             android_id=test_id, ifa="")
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
    #                                       rtb_selector=win_notification_meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_keys_exist(bid_request['regs'], 'coppa')
    #     device_ext_vungle = bid_request['device']['ext']['vungle']
    #     assert_that(device_ext_vungle['id_source'], equal_to('ISU'))
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
    #               'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on amazon platform')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_no_config_zero_ifa_on_amazon_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     no legal config; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #     if env == 'ci':
    #         rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
    #     elif env == 'qa' or env == 'regression':
    #         rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
    #     test_id = '00000000-0000-0000-0000-000000000000'
    #     req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement, coppa=coppa,
    #                                            ifa=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
    #                                       rtb_selector=rtb))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #     bid_response_device_info = response_payload['ext']['debug']['auction_result']['device_info']
    #     if coppa:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #         assert_that(bid_response_device_info['source'], equal_to('Vungle_FP'))
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')
    #         device = bid_request['device']
    #         assert_that(device['ifa'], equal_to(test_id))
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
    #               'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 and '
    #                     'zero ifa on amazon platform')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_no_config_on_amazon_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     no legal config; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #     if env == 'ci':
    #         rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
    #     elif env == 'qa' or env == 'regression':
    #         rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
    #     test_id = test_mode_device_id
    #     req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement, coppa=coppa,
    #                                            ifa=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
    #                                       rtb_selector=rtb))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #     bid_response_device_info = response_payload['ext']['debug']['auction_result']['device_info']
    #     if coppa:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #         assert_that(bid_response_device_info['source'], equal_to('IFA'))
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')
    #         device = bid_request['device']
    #         assert_that(device['ifa'], equal_to(test_id))
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
    #               'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on ios platform')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_no_config_on_ios_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": true
    #     case:
    #     no legal config; is_coppa(api):% coppa; is_coppa(dashboard):true;
    #    """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, coppa=coppa,
    #                                         ifa=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
    #                                       rtb_selector=meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
    #     assert_keys_exist(bid_request['regs'], 'coppa')
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
    #               'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on ios platform')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_no_config_on_ios_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     no legal config; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', coppa=coppa,
    #                                         ifa=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
    #                                       rtb_selector=meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
    #     if coppa is True:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')
    #
    # @allure.feature('coppa 6.11.X')
    # @allure.tag('normal')
    # @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
    #               'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    # @allure.description('Verify coppa_preference is work well for jaeger when sdk >=6.10.4 on windows platform')
    # @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", False, True])
    # def test_coppa_no_config_on_windows_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     case:
    #     no legal config; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #    """
    #     test_id = gen_device_id()
    #     req = request_payload.jaeger_v5_windows(pub_app_id, windows_common_test_placement, coppa=coppa,
    #                                             ashwid=test_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
    #                                       rtb_selector=meister_rtb_ids))
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
    #     if coppa is True:
    #         assert_keys_exist(bid_request['regs'], 'coppa')
    #
    #     else:
    #         assert_keys_not_exist(bid_request['regs'], 'coppa')



    # ------------------------------------------below cases are for sdk < 6.10.4 ---------------------------------------

    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk < 6.10.4 on android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_android_6103_01(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": false
        case:
        "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
       """

        test_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=coppa,
                                                android_id=test_id, ifa="")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        if coppa:
            assert_keys_exist(bid_request['regs'], 'coppa')
            assert_keys_not_exist(bid_request['device'], 'ifa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
        else:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('ISU'))

    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk < 6.10.4 on android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_android_6103_zero_ifa(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": false
        case:
        "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
       """

        test_id = '00000000-0000-0000-0000-000000000000'
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=coppa,
                                                android_id=test_id, ifa="")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        if coppa:
            assert_keys_exist(bid_request['regs'], 'coppa')
            assert_keys_not_exist(bid_request['device'], 'ifa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))
        else:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))


    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk < 6.10.4 on android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_android_6103_2(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": true
        case:
        "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
       """

        test_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_coppa_placememt, coppa=coppa,
                                                android_id=test_id, ifa="")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        if coppa == False:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('ISU'))
        else:
            assert_keys_exist(bid_request['regs'], 'coppa')
            assert_keys_not_exist(bid_request['device'], 'ifa')
            device_ext_vungle = bid_request['device']['ext']['vungle']
            assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))


    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk < 6.10.4 on amazon platform')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_amazon_6103(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": true
        case:
        "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
       """

        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        test_id = test_mode_device_id
        req = request_payload.jaeger_v5_amazon(pub_app_id, amazon_common_test_placement, coppa=coppa,
                                               ifa=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        bid_response_device_info = response_payload['ext']['debug']['auction_result']['device_info']
        if coppa:
            assert_keys_exist(bid_request['regs'], 'coppa')
            assert_that(bid_response_device_info['source'], equal_to('IFA'))
        else:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            device = bid_request['device']
            assert_that(device['ifa'], equal_to(test_id))



    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk < 6.10.4 on ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_on_ios_1(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": true
        case:
        "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
       """
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, coppa=coppa,
                                            ifa=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
        if coppa is False:
            assert_keys_not_exist(bid_request['regs'], 'coppa')

        else:
            assert_keys_exist(bid_request['regs'], 'coppa')



    @allure.feature('coppa 6.11.X')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +'
                  'PBJ-3879 [Jaeger][COPPA] compliance with COPPA behavior for 6.10.4 android & 6.11.0 +')
    @allure.description('Verify coppa_preference is work well for jaeger when sdk < 6.10.4 on windows platform')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('coppa', ["", False, True])
    def test_coppa_on_windows_1(self, pub_app_id, sdk_v, coppa):
        """
        App level setting:
        "isCoppaCompliant": false
        case:
       "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
       """
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_windows(pub_app_id, windows_common_test_placement, coppa=coppa,
                                                ashwid=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
        if coppa is True:
            assert_keys_exist(bid_request['regs'], 'coppa')

        else:
            assert_keys_not_exist(bid_request['regs'], 'coppa')



    # --------------------below cases are for disable_ad_id_if_coppa=True and GDPR exists---------------------------

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story(
        'PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3'
                        'and GDPR exists')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_zero_out_gaid_with_gdpr_for_android_01_true(self, pub_app_id, sdk_v, consent_status):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id="", ifa="", gdpr=consent_status)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                                                        src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_keys_not_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request, 'ifa')
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story(
        'PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_zero_out_gaid_with_gdpr_for_android_02_true(self, pub_app_id, sdk_v, consent_status):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                android_id="", ifa="", gdpr=consent_status)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                          rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              win_notification_meister_rtb_ids)
        assert_that(bid_request['regs']['coppa'], equal_to(1))
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_with_gdpr_for_android_05_true(self, pub_app_id, sdk_v, consent_status):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=gen_device_id(), gdpr=consent_status)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip, sdk_version=sdk_v,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_not_exist(bid_request['regs'], 'coppa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_keys_exist(device_ext_vungle, 'isu')
        assert_that(device_ext_vungle['id_source'], equal_to('GDPR'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story(
        'PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_zero_out_gaid_with_gdpr_for_android_06_true(self, pub_app_id, sdk_v, consent_status):
        """
           Placement level setting:
           "is_coppa": true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                android_id=gen_device_id(), gdpr=consent_status,
                                                )
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip, sdk_version=sdk_v,
                                          rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              win_notification_meister_rtb_ids)
        assert_keys_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    def test_zero_out_gaid_with_gdpr_for_android_07_true(self, pub_app_id, sdk_v, consent_status):
        """

       App level setting:
       "isCoppaCompliant": false
       """
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, coppa=False,
                                                android_id="", ifa="", gdpr=consent_status)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
        assert_keys_not_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story(
        'PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_zero_out_gaid_with_gdpr_for_android_08_true(self, pub_app_id, sdk_v, consent_status):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                android_id="", ifa="", gdpr=consent_status)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=fr_ip,
                                          rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              win_notification_meister_rtb_ids)
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story(
        'PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_zero_out_gaid_with_gdpr_for_android_12_true(self, pub_app_id, sdk_v, consent_status):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                ifa='00000000-0000-0000-0000-000000000000',
                                                android_id='00000000-0000-0000-0000-000000000000', coppa=True,
                                                gdpr=consent_status)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=jp_ip,
                                          rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              win_notification_meister_rtb_ids)
        assert_keys_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story(
        'PBJ-3574 [COPPA][jaeger]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_zero_out_gaid_with_gdpr_for_android_12_1_true(self, pub_app_id, sdk_v, consent_status):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.jaeger_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                ifa='00000000-0000-0000-0000-000000000000',
                                                android_id='00000000-0000-0000-0000-000000000000', coppa=True,
                                                gdpr=consent_status)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=jp_ip,
                                          rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              win_notification_meister_rtb_ids)
        assert_keys_exist(bid_request['regs'], 'coppa')
        assert_keys_not_exist(bid_request['device'], 'ifa')
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_that(device_ext_vungle['id_source'], equal_to('Vungle_FP'))

    @allure.feature('disable account')
    @allure.tag('normal', 'R_1.124.0')
    @allure.story('PBJ-1520 do not serve the ad request for the archived accounts')
    @allure.description('Verify Jaeger does not serve for the app of deleted account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5d4be99434c2bc00181da7f4'])
    @pytest.mark.parametrize('placement', ['DEFAULT-94243124'])
    def test_jaeger_not_serve_for_deleted_account(self, pub_app_id, placement):
        '''
        account id: 603f51273f32a974dcad4946
        "is_deleted" = true
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(ad_markup['sleep'], equal_to(901))
        assert_that(ad_markup['info'], equal_to('publisher not found'))

    @allure.feature('disable account')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1520 do not serve the ad request for the archived accounts')
    @allure.description('Verify Jaeger serves for the app of non deleted account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_jaeger_serves_for_non_deleted_account_1(self, pub_app_id):
        '''
        account id: 597565c6c5511a1b62000990
        "is_deleted" = false
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if 'sleep' in ad_markup:
            assert_that(ad_markup['sleep'], not equal_to(901))
            assert_that(ad_markup['info'], not equal_to('publisher not found'))

    @allure.feature('disable account')
    @allure.tag('normal', 'R_1.124.0')
    @allure.story('PBJ-1520 do not serve the ad request for the archived accounts')
    @allure.description('Verify Jaeger serves for the app of non deleted account (no is_deleted setting)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    def test_jaeger_serves_for_non_deleted_account_2(self, pub_app_id):
        '''
        account id: 5b5b55bd4d46a60c8063f18c
        no "is_deleted" setting in account
        '''
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_windows(pub_app_id, win_notification_meister_rtb_ids, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if 'sleep' in ad_markup:
            assert_that(ad_markup['sleep'], not equal_to(901))
            assert_that(ad_markup['info'], not equal_to('publisher not found'))

    #
    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify rtb blocks in case of CCPA status opted out via non test mode ext vast kraken')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('ccpa_status', ['opted_out'])
    # @pytest.mark.parametrize('ip', [ca_ip, jp_ip])
    # def test_ccpa_status_opted_out_block_opted_out(self, pub_app_id, ccpa_status, ip):
    #     test_ifa = gen_device_id(digital=36)
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ccpa=ccpa_status, ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_that('sleep' in ad_markup)

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify rtb blocks in case of CCPA status opted out via non test mode ext vast kraken,'
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('ccpa_status', ['opted_out'])
    @pytest.mark.parametrize('ip', [ca_us_ip, jp_ip])
    def test_ccpa_status_opted_out_block_opted_out_1(self, pub_app_id, ccpa_status, ip):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ccpa=ccpa_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-Y-'))

    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify rtb doen not block in case of CCPA status opted in or in other value via '
    #                     'non test mode kraken')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('ccpa_status', ['opted_in', 'test'])
    # def test_ccpa_status_opted_in_block_opted_out(self, pub_app_id, ccpa_status):
    #     test_ifa = gen_device_id(digital=36)
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ccpa=ccpa_status, ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=jp_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-N-'))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify rtb doen not block in case of CCPA status opted in or in other value via '
                        'non test mode kraken, block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('ccpa_status', ['opted_in', 'test'])
    def test_ccpa_status_opted_in_block_opted_out_1(self, pub_app_id, ccpa_status):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ccpa=ccpa_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-N-'))

    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify rtb blocks in case of CCPA status opted out via non test mode ext vast kraken')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # def test_ccpa_status_opted_out_flag_block_opted_out_2(self, pub_app_id):
    #     '''
    #         Account level setting:
    #         "is_ccpa_opt_out": true
    #     '''
    #     test_ifa = gen_device_id(digital=36)
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=ca_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_that('sleep' in ad_markup)

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify rtb blocks in case of CCPA status opted out via non test mode ext vast kraken,'
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ccpa_status_opted_out_flag_block_opted_out_1(self, pub_app_id):
        '''
            Account level setting:
            "is_ccpa_opt_out": true
        '''
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-Y-'))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify rtb blocks in case of CCPA status opted in via non test mode ext vast kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_ccpa_status_opted_in_flag_block_opted_out_2(self, pub_app_id):
        '''
            Account level setting:
            "is_ccpa_opt_out": false
        '''
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-N-'))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify rtb blocks in case of CCPA status opted in via non test mode ext vast kraken,'
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_ccpa_status_opted_in_flag_block_opted_out_1(self, pub_app_id):
        '''
            Account level setting:
            "is_ccpa_opt_out": false
        '''
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-N-'))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify us_privacy in case of CCPA status repect the external consent')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('ccpa_status', ['opted_in'])
    def test_ccpa_status_opted_out_respect_external_consent_block_opted_out(self, pub_app_id, ccpa_status):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ccpa=ccpa_status,
                                            ifa=ccpa_external_consents_opted_out_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that('sleep' in ad_markup)

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify us_privacy in case of CCPA status repect the external consent, '
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('ccpa_status', ['opted_in'])
    def test_ccpa_status_opted_out_respect_external_consent_block_opted_out_1(self, pub_app_id, ccpa_status):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ccpa=ccpa_status,
                                            ifa=ccpa_external_consents_opted_out_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            response_payload = r.json()
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-Y-'))

    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify rtb doen not block in case of CCPA status not exist via non test mode kraken')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('data', [{"app": common_test_app, "placement": common_test_placement},
    #                                   {"app": "5c003b9a3933314cf38ff7f3", "placement": "DEFAULT-5045327"}])
    # def test_ccpa_status_not_exist_block_opted_out(self, data):
    #     test_ifa = gen_device_id(digital=36)
    #     req = request_payload.jaeger_v5_ios(data['app'], data['placement'], ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=jp_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1---'))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify rtb doen not block in case of CCPA status not exist via non test mode kraken, '
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('data', [{"app": common_test_app, "placement": common_test_placement},
                                      {"app": "5c003b9a3933314cf38ff7f3", "placement": "DEFAULT-5045327"}])
    def test_ccpa_status_not_exist_block_opted_out_1(self, data):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(data['app'], data['placement'], ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1---'))

    # @allure.feature('bcat list')
    # @allure.tag('normal', 'R_1.151.0')
    # @allure.story('PBJ-2315 Remove IAB14-1 Dating from Bcat')
    # @allure.description('Verify that there is no IAB14-1 from bcat list')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_bcat_list(self, pub_app_id, placement):
    #     test_ifa = gen_device_id(digital=36)
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_that('IAB14-1' not in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal', 'v1.158.0')
    # @allure.story('PBJ-2618 Remove IAB11 for xRTB stackadapt in bid request')
    # @allure.description('Verify for removing IAB11 for eDSP')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_removing_edsp_1(self, pub_app_id, placement):
    #     rtb = ext_non_test_mode_kraken_rtb_ids_vast_no_iab11
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=jp_ip, rtb_selector=rtb))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #     assert_that('IAB11' not in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal', 'v1.158.0')
    # @allure.story('PBJ-2618 Remove IAB11 for xRTB stackadapt in bid request')
    # @allure.description('Verify for not removing IAB11 for eDSP')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_removing_edsp_2(self, pub_app_id, placement):
    #     rtb = ext_non_test_mode_kraken_rtb_ids_vast
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=jp_ip, rtb_selector=rtb))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #     assert_that('IAB11' in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal', 'v1.158.0', 'test_mode')
    # @allure.story('PBJ-2618 Remove IAB11 for xRTB stackadapt in bid request')
    # @allure.description('Verify for removing IAB11 for eDSP in test mode')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_removing_edsp_1_test_mode(self, pub_app_id, placement):
    #     rtb = ext_test_mode_kraken_rtb_ids_vast_no_iab11
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #     assert_that('IAB11' not in bid_request['bcat'])

    @allure.feature('bcat list')
    @allure.tag('normal', 'v1.164.0', 'test_mode')
    @allure.story('PBJ-2766 Remove IAB7-44 from Bcat')
    @allure.description('Verify for removing IAB7-44 for idsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_removing_bcat_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that('IAB7-44' not in bid_request['bcat'])

    @allure.feature('bcat list')
    @allure.tag('normal', 'v1.164.0', 'test_mode')
    @allure.story('PBJ-2766 Remove IAB7-44 from Bcat')
    @allure.description('Verify for removing IAB7-44 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_removing_bcat_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that('IAB7-44' not in bid_request['bcat'])

    @allure.feature('bcat list')
    @allure.tag('normal', 'v1.164.0', 'test_mode')
    @allure.story('PBJ-2766 Remove IAB7-44 from Bcat')
    @allure.description('Verify for removing IAB7-44 for edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_removing_bcat_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that('IAB7-44' not in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal', 'v1.158.0', 'test_mode')
    # @allure.story('PBJ-2618 Remove IAB11 for xRTB stackadapt in bid request')
    # @allure.description('Verify for not removing IAB11 for eDSP in test mode')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_removing_edsp_2_test_mode(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     assert_keys_not_exist(response_payload['ext']['debug']['auction_result']['bid_requests'], 'NoIAB11')
    #
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that('IAB11' in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal', 'v1.158.0', 'test_mode')
    # @allure.story('PBJ-2618 Remove IAB11 for xRTB stackadapt in bid request')
    # @allure.description('Verify the supported_extension_type will not work for iDSP')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_removing_idsp_1(self, pub_app_id, placement):
    #     '''
    #         Setup for the test iDSP rtb: "supported_extension_type": "NoIAB11"
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     assert_keys_not_exist(response_payload['ext']['debug']['auction_result']['bid_requests'], 'NoIAB11')
    #
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that('IAB11' in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal', 'v1.158.0', 'test_mode')
    # @allure.story('PBJ-2618 Remove IAB11 for xRTB stackadapt in bid request')
    # @allure.description('Verify if no supported_extension_type setting for iDSP')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_removing_idsp_2(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     assert_keys_not_exist(response_payload['ext']['debug']['auction_result']['bid_requests'], 'NoIAB11')
    #
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that('IAB11' in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal')
    # @allure.story('PBJ-3642 bCAT Test - 5 Apps')
    # @allure.description('Verify bcat field be merged of the specified for meister')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_apps', bCAT_beta_apps)
    # def test_merged_bcat_meister(self, pub_apps):
    #     req = request_payload.jaeger_v5_ios(pub_apps['pub_app'], pub_apps['placement'], ifa=gen_device_id(),
    #                                         battery_saver_enabled=0)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', rtb_selector=win_notification_meister_rtb_ids))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_that(len(bid_request['bcat']), equal_to(len(pub_apps['merged_iab'])))
    #     all(bid_request['bcat'].count(i) == pub_apps['merged_iab'].count(i) for i in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal')
    # @allure.story('PBJ-3642 bCAT Test - 5 Apps')
    # @allure.description('Verify bcat field be merged of the specified for eDSP in non test mode')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_apps', bCAT_beta_apps)
    # def test_merged_bcat_non_test_mode_edsp(self, pub_apps):
    #     req = request_payload.jaeger_v5_ios(pub_apps['pub_app'], pub_apps['placement'], ifa=gen_device_id(),
    #                                         battery_saver_enabled=0)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=fr_ip,
    #                                       rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext1_non_test_mode_kraken_rtb_ids_vast)
    #     assert_that(len(bid_request['bcat']), equal_to(len(pub_apps['merged_iab'])))
    #     all(bid_request['bcat'].count(i) == pub_apps['merged_iab'].count(i) for i in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal')
    # @allure.story('PBJ-3642 bCAT Test - 5 Apps')
    # @allure.description('Verify bcat field be merged of the specified for windows')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_apps', bCAT_beta_windows_apps)
    # def test_merged_bcat_windows_meister(self, pub_apps):
    #     req = request_payload.jaeger_v5_windows(pub_apps['pub_app'], pub_apps['placement'], ashwid=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', rtb_selector=win_notification_meister_rtb_ids,
    #                                       sdk_version='VungleWindows/6.5.3 (Windows 10; native)'))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, win_notification_meister_rtb_ids)
    #     assert_that(len(bid_request['bcat']), equal_to(len(pub_apps['merged_iab'])))
    #     all(bid_request['bcat'].count(i) == pub_apps['merged_iab'].count(i) for i in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal')
    # @allure.story('PBJ-3760 Badoo Mobile - bCAT Blocks')
    # @allure.description('Verify bcat field be merged of the specified for android')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_apps', bCAT_block_android_apps)
    # def test_merged_bcat_android(self, pub_apps):
    #     if env == 'ci':
    #         rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
    #     elif env == 'qa' or env == 'regression':
    #         rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
    #     req = request_payload.jaeger_v5_android(pub_apps['pub_app'], pub_apps['placement'], android_id=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', rtb_selector=rtb,
    #                                       src_ip=fr_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #     assert_that(len(bid_request['bcat']), equal_to(len(pub_apps['merged_iab'])))
    #     all(bid_request['bcat'].count(i) == pub_apps['merged_iab'].count(i) for i in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal')
    # @allure.story('PBJ-3760 Badoo Mobile - bCAT Blocks')
    # @allure.description('Verify bcat field be merged of the specified for iOS')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_apps', bCAT_block_ios_apps)
    # def test_merged_bcat_ios(self, pub_apps):
    #     if env == 'ci':
    #         rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
    #     elif env == 'qa' or env == 'regression':
    #         rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
    #     req = request_payload.jaeger_v5_ios(pub_apps['pub_app'], pub_apps['placement'], ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', rtb_selector=rtb,
    #                                       src_ip=fr_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #     assert_that(len(bid_request['bcat']), equal_to(len(pub_apps['merged_iab'])))
    #     all(bid_request['bcat'].count(i) == pub_apps['merged_iab'].count(i) for i in bid_request['bcat'])


    @allure.feature('bcat list')
    @allure.tag('normal')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard')
    @allure.description('Verify bcat field based on dashboard setting in case of no config in app&pub')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [gdpr_gdpr_delegate_t_legitimate_interest_f_app])
    @pytest.mark.parametrize('placement', ['DEFAULT09128'])
    def test_bcat_setting_on_dashboard_01(self, pub_app_id, placement):
        '''

        without 'ad_cat_blocklist' field in application and application account
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        assert_keys_not_exist(bid_request, 'bcat')

    @allure.feature('bcat list')
    @allure.tag('normal')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard')
    @allure.description('Verify bcat field based on dashboard setting in case of ad_cat_blocklist is null in app&pub')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', ['COPPA-TEST'])
    def test_bcat_setting_on_dashboard_02(self, pub_app_id, placement):
        '''

        'ad_cat_blocklist:[]' field in application and application account
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        assert_keys_not_exist(bid_request, 'bcat')



    @allure.feature('bcat list')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard'
                  'PBJ-4742 PBJ-4742 Exchange and Accelerate don\'t respect ad categories block')
    @allure.description('Verify bcat field based on dashboard setting in case of ad_cat_blocklist in account is [V1-1] '
                        'app is no field'
                        'Verify will not block bcat in the response if account level:filter_out_bcat=false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_bcat_setting_on_dashboard_03(self, pub_app_id, placement):
        '''
        account config
        'ad_cat_blocklist:['V1-1']'

         account:
        "filter_out_bcat": false

        app config
        no ad_cat_blocklist field
        '''
        override_bcat = 'seatbid.0.bid.0.cat.0@"IAB8-5"'
        expected_bcats=['IAB8-5', 'IAB8-18']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=fr_ip, override_bid_response_any=override_bcat))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        assert_keys_exist(bid_request, 'bcat')
        assert_that(len(bid_request['bcat']), equal_to(len(expected_bcats)))
        all(bid_request['bcat'].count(i) == expected_bcats.count(i) for i in bid_request['bcat'])
        # PBJ-4742 validation
        assert_keys_not_exist(ad_markup, 'sleep')
        # verify that will log to metrics "ssp_jaeger_bcat_violation_count"


    @allure.feature('bcat list')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard'
                  'PBJ-4742 PBJ-4742 Exchange and Accelerate don\'t respect ad categories block')
    @allure.description('Verify bcat field based on dashboard setting in case of ad_cat_blocklist in account is [V1-1,V1-2] '
                        'app is no field'
                        'Verify will hard block bcat in the response if account level:filter_out_bcat=true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [mrec_test_app])
    @pytest.mark.parametrize('placement', [programmatic_mrec_placement])
    def test_bcat_setting_on_dashboard_04(self, pub_app_id, placement):
        """
        account config
        'ad_cat_blocklist:['V1-1', 'V1-2']'
        'filter_out_bcat': true

        app config
        no ad_cat_blocklist field
        """
        override_bcat= 'seatbid.0.bid.0.cat.0@"IAB8-5"'
        expected_bcats = ['IAB8-5', 'IAB8-18', 'IAB25', 'IAB17-5', 'IAB17-20']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=fr_ip, override_bid_response_any=override_bcat))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        assert_keys_exist(bid_request, 'bcat')
        assert_that(len(bid_request['bcat']), equal_to(len(expected_bcats)))
        all(bid_request['bcat'].count(i) == expected_bcats.count(i) for i in bid_request['bcat'])
        # PBJ-4742 validation
        assert_keys_exist(ad_markup, 'sleep')


    @allure.feature('bcat list')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard'
                  'PBJ-4742 PBJ-4742 Exchange and Accelerate don\'t respect ad categories block')
    @allure.description('Verify bcat field based on dashboard setting in case of ad_cat_blocklist exist in account & app '
                        'Verify will hard bolck bcat id app level: filter_out_bcat is true'
                        )
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_bcat_setting_on_dashboard_05(self, pub_app_id, placement):
        '''
        account config
        'ad_cat_blocklist:['V1-1']'

        app config
        'ad_cat_blocklist:['V1-3']'
        'filter_out_bcat'" true

        '''
        override_bcat = 'seatbid.0.bid.0.cat.0@"IAB8-5"'
        expected_bcats = ['IAB8-5', 'IAB8-18', 'IAB13-2']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=fr_ip, override_bid_response_any=override_bcat))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        assert_keys_exist(bid_request, 'bcat')
        assert_that(len(bid_request['bcat']), equal_to(len(expected_bcats)))
        all(bid_request['bcat'].count(i) == expected_bcats.count(i) for i in bid_request['bcat'])
        # PBJ-4742 validation
        assert_keys_exist(ad_markup, 'sleep')



    @allure.feature('bcat list')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard'
                  'PBJ-4742 Exchange and Accelerate don\'t respect ad categories block')
    @allure.description('Verify bcat field based on dashboard setting in case of ad_cat_blocklist not exist in account but in app '
                        'Verify will not block bcat in the response if account level:filter_out_bcat=null')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('placement', [android_common_coppa_placememt])
    def test_bcat_setting_on_dashboard_06(self, pub_app_id, placement):
        '''
        account config
        no field
        filter_out_bcat = nullR
        app config
        'ad_cat_blocklist:['V1-1']'
        '''
        override_bcat = 'seatbid.0.bid.0.cat.0@"IAB8-5"'
        expected_bcats = ['IAB8-5','IAB8-18']
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=fr_ip, override_bid_response_any=override_bcat))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        assert_that(len(bid_request['bcat']), equal_to(len(expected_bcats)))
        all(bid_request['bcat'].count(i) == expected_bcats.count(i) for i in bid_request['bcat'])
        # PBJ-4742 validation
        assert_keys_not_exist(ad_markup, 'sleep')
        # verify that will log to metrics "ssp_jaeger_bcat_violation_count"


    @allure.feature('bcat list')
    @allure.tag('normal')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard')
    @allure.description('Verify bcat field based on dashboard setting in case of ad_cat_blocklist not exist in account but in app '
                        )
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_bcat_app])
    @pytest.mark.parametrize('placement', [android_common_bcat_placement])
    def test_bcat_setting_on_dashboard_07(self, pub_app_id, placement):
        '''
        account config
        no field

        app config
        'ad_cat_blocklist:['V1-1','V1-2']'
        '''
        expected_bcats = ['IAB17-5', 'IAB17-20', 'IAB8-18', 'IAB8-5', 'IAB25']
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        assert_keys_exist(bid_request, 'bcat')
        assert_that(len(bid_request['bcat']), equal_to(len(expected_bcats)))
        all(bid_request['bcat'].count(i) == expected_bcats.count(i) for i in bid_request['bcat'])


    @allure.feature('bcat list')
    @allure.tag('normal')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard')
    @allure.description('Verify bcat field based on dashboard setting in case of ad_cat_blocklist both exist in account and app '
                        'for non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids, meister_rtb_ids])
    def test_bcat_setting_on_dashboard_08(self, pub_app_id, placement, rtb_ids):
        '''
        account config
       'ad_cat_blocklist:['V1-1']'

        app config
        'ad_cat_blocklist:['V1-1','V1-2','V1-9']'
        '''
        expected_bcats = ['IAB25', 'IAB17-5', 'IAB17-20', 'IAB7-39', 'IAB14-3', 'IAB18-2', 'IAB9-9', 'IAB8-5', 'IAB8-18']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids,
                                          src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        assert_keys_exist(bid_request, 'bcat')
        assert_that(len(bid_request['bcat']), equal_to(len(expected_bcats)))
        all(bid_request['bcat'].count(i) == expected_bcats.count(i) for i in bid_request['bcat'])


    @allure.feature('bcat list')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard')
    @allure.description('Verify bcat field based on dashboard setting in case of ad_cat_blocklist both exist in account and app '
                        'for test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    @pytest.mark.parametrize('rtb_ids', [ext_test_mode_kraken_rtb_ids_mraid, test_mode_kraken_rtb_ids])
    def test_bcat_setting_on_dashboard_09(self, pub_app_id, placement, rtb_ids):
        '''
        account config
       'ad_cat_blocklist:['V1-1']'

        app config
        'ad_cat_blocklist:['V1-1','V1-2','V1-9']'
        '''
        expected_bcats = ['IAB25', 'IAB17-5', 'IAB17-20', 'IAB7-39', 'IAB14-3', 'IAB18-2', 'IAB9-9', 'IAB8-5', 'IAB8-18']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb_ids,
                                          src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        assert_keys_exist(bid_request, 'bcat')
        assert_that(len(bid_request['bcat']), equal_to(len(expected_bcats)))
        all(bid_request['bcat'].count(i) == expected_bcats.count(i) for i in bid_request['bcat'])


    @allure.feature('bcat list')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard')
    @allure.description('Verify bcat field based on dashboard setting in case of ad_cat_blocklist both exist in account and app '
                        'for amazon')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    def test_bcat_setting_on_dashboard_10(self, pub_app_id, placement):
        '''
        account config


        app config
        'ad_cat_blocklist:['V2-9']'
        '''
        expected_bcats = ['IAB17-18']
        req = request_payload.jaeger_v5_amazon(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, test_mode_kraken_rtb_ids)
        assert_keys_exist(bid_request, 'bcat')
        assert_that(len(bid_request['bcat']), equal_to(len(expected_bcats)))
        all(bid_request['bcat'].count(i) == expected_bcats.count(i) for i in bid_request['bcat'])




    @allure.feature('block adv')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2685 Block advertising apps through domain (account&app)')
    @allure.description('Verify the domain on app black list can not be served by Jaeger')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b7'])
    @pytest.mark.parametrize('placement', ['DEFAULT02027'])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1, ext_test_mode_kraken_rtb_ids_vast])
    def test_block_adv_domain_1(self, pub_app_id, placement, rtb):
        '''
        Account setting:
            adDomainBlacklist": ["domain3.com", "domain4.com"]
        App setting:
            "adDomainBlacklist": ["domain1.com"]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        if rtb == test_mode_kraken_rtb_ids_1:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        else:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # update check points for PBJ-4007
        assert_that(bid_request['badv'],
                    equal_to(['charm00.com', 'com.mopub.video', 'com.murka.scatterslots', 'domain1.com', 'domain3.com',
                               'domain4.com', 'glu.com', 'hhijb.com', 'osityh.com', 'testabc.com']))

    @allure.feature('block adv')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2685 Block advertising apps through domain (account&app)')
    @allure.description('Verify the domain on account black list can not be served by Jaeger')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b8'])
    @pytest.mark.parametrize('placement', ['DEFAULT02028'])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1, ext_test_mode_kraken_rtb_ids_vast])
    def test_block_adv_domain_2(self, pub_app_id, placement, rtb):
        '''
        Account setting:
            adDomainBlacklist": ["domain1.com", "domain4.com"]

        App setting:
            "adDomainBlacklist": ["domain2.com", "domain3.com"]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        if rtb == test_mode_kraken_rtb_ids_1:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, test_mode_kraken_rtb_ids_1)
        else:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_test_mode_kraken_rtb_ids_vast)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # update check points for PBJ-4007
        assert_that(bid_request['badv'],
                    equal_to(['charm00.com', 'com.mopub.video', 'com.murka.scatterslots', 'domain1.com', 'domain2.com',
                              'domain3.com', 'domain4.com', 'glu.com', 'hhijb.com', 'osityh.com', 'testabc.com']))


    @allure.feature('block adv')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2685 Block advertising apps through domain (account&app)')
    @allure.description('Verify the domain not on account black list can be served by Jaeger')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1, ext_test_mode_kraken_rtb_ids_vast])
    def test_block_adv_domain_3(self, pub_app_id, placement, rtb):
        '''
        Account setting:
            adDomainBlacklist": ["domain3.com", "domain4.com"]

        App setting:
            "adDomainBlacklist": ["domain2.com", "domain3.com"]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        if rtb == test_mode_kraken_rtb_ids_1:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        else:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # add check points for 4007
        assert_that(bid_request['badv'],
                    equal_to(['charm00.com', 'com.mopub.video', 'com.murka.scatterslots', 'domain2.com', 'domain3.com',
                              'domain4.com', 'glu.com', 'hhijb.com', 'osityh.com', 'testabc.com']))


    @allure.feature('block ads')
    @allure.tag('normal' , 'v1.245.0')
    @allure.story('PBJ-4875 Jaeger - Support pub level country block by MongoDB')
    @allure.description('Verify country on account level setting can not be served by Jaeger')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('placement', [android_common_coppa_placememt])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_block_adomain])
    @pytest.mark.parametrize('ip', [de_ip, lb_ip])
    def test_block_ads_on_pub_account_01(self, pub_app_id, placement, rtb, ip):
        """
        Account setting:
            ad_serving_country_blocklist": ["de", "ir", "lb"]
        """
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb, src_ip=ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('publisher inactive'))


    @allure.feature('block ads')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4875 Jaeger - Support pub level country block by MongoDB')
    @allure.description('Verify country not set on account level blocklist can be served by Jaeger')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('placement', [android_common_coppa_placememt])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_block_adomain])
    @pytest.mark.parametrize('ip', [au_ip])
    def test_block_ads_on_pub_account_02(self, pub_app_id, placement, rtb, ip):
        """
        Account setting:
            ad_serving_country_blocklist": ["de", "ir", "lb"]
        """
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb, src_ip=ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')


    @allure.feature('first price auction')
    @allure.tag('normal', 'v1.164.0')
    @allure.story('PBJ-2767 First price auction strategy and features')
    @allure.description('Verify that all country except China use 1st price auction which match the old exp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [ca_us_ip])
    def test_first_price_auction_1(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip, rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['at'], equal_to(1))

    @allure.feature('first price auction')
    @allure.tag('normal', 'v1.164.0')
    @allure.story('PBJ-2767 First price auction strategy and features')
    @allure.description('Verify that all country except China still use 1st price auction which not match the old exp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [gb_ip])
    def test_first_price_auction_2(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip, rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['at'], equal_to(1))

    @allure.feature('first price auction')
    @allure.tag('normal', 'v1.164.0', 'test_mode')
    @allure.story('PBJ-2767 First price auction strategy and features')
    @allure.description('Verify that all country except China use 1st price auction in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [ca_us_ip, gb_ip])
    def test_first_price_auction_3(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip, rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['at'], equal_to(1))

    @allure.feature('first price auction')
    @allure.tag('normal', 'v1.164.0')
    @allure.story('PBJ-2767 First price auction strategy and features')
    @allure.description('Verify that all country except China use 1st price auction with edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [jp_ip, au_ip])
    def test_first_price_auction_4(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['at'], equal_to(1))

    @allure.feature('first price auction')
    @allure.tag('normal', 'v1.164.0', 'v1.226.0')
    @allure.story('PBJ-2767 First price auction strategy and features'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that China uses 2nd price auction which match the old exp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [cn_ip])
    def test_first_price_auction_5(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip, rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['at'], equal_to(1))

    @allure.feature('first price auction')
    @allure.tag('normal', 'v1.164.0', 'test_mode', 'v1.226.0')
    @allure.story('PBJ-2767 First price auction strategy and features'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that China uses 2nd price auction in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [cn_ip])
    def test_first_price_auction_6(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip, rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['at'], equal_to(1))

    @allure.feature('first price auction')
    @allure.tag('normal', 'v1.164.0', 'test_mode', 'v1.226.0')
    @allure.story('PBJ-2767 First price auction strategy and features'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that China uses 2nd price auction with edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [cn_ip])
    def test_first_price_auction_7(self, pub_app_id, placement, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['at'], equal_to(1))


    @allure.feature('auction type experiment')
    @allure.tag('normal', 'test_mode', 'v1.223.0')
    @allure.story('PBJ-4216 Experiment 1st Price Auction for China Traffic')
    @allure.description('Verify CN traffic will follow 1st action price rule if enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('ip', [cn_ip])
    @pytest.mark.parametrize('rtb_ids', [ext_test_mode_kraken_rtb_ids_vast, test_mode_kraken_rtb_ids])
    def test_cn_auction_type_experiment_01(self, pub_app_id, placement, ip, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['at'], is_in([1, 2]))
        # Also verify transaction & delivery messages.

    @allure.feature('auction type experiment')
    @allure.tag('normal', 'v1.223.0')
    @allure.story('PBJ-4216 Experiment 1st Price Auction for China Traffic')
    @allure.description('Verify CN traffic will follow 1st action price rule if enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('ip', [cn_ip])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids])
    def test_cn_auction_type_experiment_02(self, pub_app_id, placement, ip, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['at'], is_in([1, 2]))
        # Also verify transaction & delivery messages.


    @allure.feature('auction type experiment')
    @allure.tag('normal', 'v1.223.0')
    @allure.story('PBJ-4216 Experiment 1st Price Auction for China Traffic')
    @allure.description('Verify other countries traffic does not enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('ip', [au_ip, eu_country_ip])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids])
    def test_cn_auction_type_experiment_03(self, pub_app_id, placement, ip, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['at'], equal_to(1))
        # Also verify no experiment info in transaction & delivery messages.



    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.')
    @allure.description('Verify only video object from bid request for previous placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_not_support_fullscreen_previous_placements_edsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        imp = bid_request['imp']
        assert_keys_not_exist(imp[0], 'banner')
        assert_keys_exist(imp[0], 'video')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.')
    @allure.description('Verify banner + video object from bid request for Interstitial&rewarded placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement',
                             [common_test_third_party_placement_crtype_01, common_test_third_party_placement_crtype_02])
    def test_fullscreen_support_placements_edsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        imp = bid_request['imp']
        assert_keys_exist(imp[0], 'banner')
        assert_that(imp[0]['banner']['api'][0], equal_to(5))
        assert_that(imp[0]['banner']['pos'], equal_to(7))
        assert_that(imp[0]['banner']['vcm'], equal_to(1))
        assert_keys_exist(imp[0], 'video')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.')
    @allure.description('Verify only  video object from bid request for no third party playable '
                        'Interstitial&rewarded placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement',
                             ['EMILY_INST_NO_THIRD_PARTY_PLAYABLE-6451276',
                              'EMILY_REWARDED_NO_THIRD_PARTY_PLAYABLE-5097310'])
    def test_fullscreen_support_placements_for_no_third_party_playable_edsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast_playable))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        imp = bid_request['imp']
        assert_keys_not_exist(imp[0], 'banner')
        assert_keys_exist(imp[0], 'video')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.')
    @allure.description('Verify only  video object from bid request for third party playable '
                        'Interstitial&rewarded placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement',
                             ['EMILY_INST_NO_THIRD_PARTY-6661709', 'EMILY_REWARDED_NO_THIRD_PARTY-0652232'])
    def test_fullscreen_support_placements_for_no_third_party_edsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_mraid))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        imp = bid_request['imp']
        assert_keys_not_exist(imp[0], 'banner')
        assert_keys_exist(imp[0], 'video')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.')
    @allure.description('Verify only banner object from bid request for banner placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_03])
    def test_fullscreen_support_banner_placements_edsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                            header_bidding=True, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast_playable))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        imp = bid_request['imp']
        assert_keys_exist(imp[0], 'banner')
        assert_keys_not_exist(imp[0], 'video')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.')
    @allure.description('Verify only banner object from bid request for mrec placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_04])
    def test_fullscreen_support_mrec_placements_edsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast_playable))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        imp = bid_request['imp']
        assert_keys_exist(imp[0], 'banner')
        assert_keys_not_exist(imp[0], 'video')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.')
    @allure.description('Verify only banner object from bid request for banner placement via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_03])
    def test_fullscreen_support_banner_placements_test_mode_edsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=test_mode_device_id,
                                            header_bidding=True, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_mraid))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        imp = bid_request['imp']
        assert_keys_exist(imp[0], 'banner')
        assert_keys_not_exist(imp[0], 'video')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.')
    @allure.description('Verify only banner object from bid request for mrec placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_04])
    def test_fullscreen_support_mrec_placements_test_mode_edsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=test_mode_device_id,
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_mraid))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        imp = bid_request['imp']
        assert_keys_exist(imp[0], 'banner')
        assert_keys_not_exist(imp[0], 'video')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.')
    @allure.description('Verify banner + video object from bid request for Interstitial&rewarded via non test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement',
                             [common_test_third_party_placement_crtype_01,
                              common_test_third_party_placement_crtype_02])
    def test_fullscreen_support_placements_non_test_mode_edsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        imp = bid_request['imp']
        assert_keys_exist(imp[0], 'banner')
        assert_that(imp[0]['banner']['api'][0], equal_to(5))
        assert_that(imp[0]['banner']['pos'], equal_to(7))
        assert_that(imp[0]['banner']['vcm'], equal_to(1))
        assert_keys_exist(imp[0], 'video')

    @allure.feature('Android 12 Privacy')
    @allure.tag('normal', 'test_mode', 'v1.192.0')
    @allure.story('PBJ-3595 [Android 12 Privacy] Read app_set_id from ads request & send to DSP')
    @allure.description('Verify app_set_id field is added in bid resquest for test mode idsp on android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_app_set_id_for_test_mode_idsp(self, pub_app_id):
        app_set_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=test_mode_device_id, app_set_id=app_set_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, test_mode_kraken_rtb_ids_1)
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_keys_exist(device_ext_vungle, 'app_set_id')
        assert_that(device_ext_vungle['app_set_id'], equal_to(app_set_id))

    @allure.feature('Android 12 Privacy')
    @allure.tag('normal', 'test_mode', 'v1.192.0')
    @allure.story('PBJ-3595 [Android 12 Privacy] Read app_set_id from ads request & send to DSP')
    @allure.description('Verify app_set_id field is added in bid resquest for test mode idsp on android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_app_set_id_for_test_mode_idsp(self, pub_app_id):
        app_set_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=test_mode_device_id, app_set_id=app_set_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, test_mode_kraken_rtb_ids_1)
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_keys_exist(device_ext_vungle, 'app_set_id')
        assert_that(device_ext_vungle['app_set_id'], equal_to(app_set_id))

    @allure.feature('Android 12 Privacy')
    @allure.tag('normal', 'v1.192.0')
    @allure.story('PBJ-3595 [Android 12 Privacy] Read app_set_id from ads request & send to DSP')
    @allure.description('Verify app_set_id field is added in bid resquest for non test mode idsp android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_app_set_id_for_non_test_mode_idsp(self, pub_app_id):
        app_set_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=app_set_id, app_set_id=app_set_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                                                        rtb_selector=non_test_mode_kraken_rtb_ids))
        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, non_test_mode_kraken_rtb_ids)
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_keys_exist(device_ext_vungle, 'app_set_id')
        assert_that(device_ext_vungle['app_set_id'], equal_to(app_set_id))

    @allure.feature('Android 12 Privacy')
    @allure.tag('normal', 'v1.192.0')
    @allure.story('PBJ-3595 [Android 12 Privacy] Read app_set_id from ads request & send to DSP')
    @allure.description('Verify app_set_id field is added in bid resquest for meister android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_app_set_id_for_meister(self, pub_app_id):
        app_set_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=app_set_id, app_set_id=app_set_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, meister_rtb_ids)
        device_ext_vungle = bid_request['device']['ext']['vungle']
        assert_keys_exist(device_ext_vungle, 'app_set_id')
        assert_that(device_ext_vungle['app_set_id'], equal_to(app_set_id))

    @allure.feature('Android 12 Privacy')
    @allure.tag('normal', 'v1.192.0')
    @allure.story('PBJ-3595 [Android 12 Privacy] Read app_set_id from ads request & send to DSP')
    @allure.description('Verify app_set_id field is added in bid resquest for test mode edsp android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_app_set_id_for_test_mode_eDSP(self, pub_app_id):
        app_set_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=test_mode_device_id, app_set_id=app_set_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_test_mode_kraken_rtb_ids_vast)
        device_ext = bid_request['device']['ext']
        assert_keys_exist(device_ext, 'app_set_id')
        assert_that(device_ext['app_set_id'], equal_to(app_set_id))

    @allure.feature('Android 12 Privacy')
    @allure.tag('normal', 'v1.192.0')
    @allure.story('PBJ-3595 [Android 12 Privacy] Read app_set_id from ads request & send to DSP')
    @allure.description('Verify app_set_id field is added in bid resquest for non test mode edsp android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_app_set_id_for_non_test_mode_eDSP(self, pub_app_id):
        app_set_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=app_set_id, app_set_id=app_set_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        device_ext = bid_request['device']['ext']
        assert_keys_exist(device_ext, 'app_set_id')
        assert_that(device_ext['app_set_id'], equal_to(app_set_id))

    @allure.feature('Android 12 Privacy')
    @allure.tag('normal', 'v1.192.0')
    @allure.story('PBJ-3507 [Android 12 privacy] Process DDL with AppSetID')
    @allure.description('Verify process DDL with AppSetID')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_process_ddl_with_AppSetId(self, pub_app_id):
        """

        placement: daily_delivery_limit:1

        """
        app_set_id = gen_device_id()

        req = request_payload.jaeger_v5_android(pub_app_id, android_common_ddl_placement,
                                                android_id='', app_set_id=app_set_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                                                        rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                                                            rtb_selector=win_notification_meister_rtb_ids))
            ad_markup = r.json()['ads'][0]['ad_markup']
            assert_keys_exist(ad_markup, 'sleep')
            assert_that(ad_markup['info'], equal_to('publisher/placement in device exceeded daily delivery limit'))

    @allure.feature('Refactor bidder')
    @allure.tag('normal')
    @allure.story('PBJ-2864 Refactor bidder package')
    @allure.description('Verify the value of instl in bid request for banner placement for mixed rtbids')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_add_mixed_rtb_ids_auction_1(self, pub_app_id):
        device_id = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_banner_placement,
                                            ifa=device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=mixed_non_test_mode_edsp))
        rtb_insti_null = mixed_non_test_mode_edsp.split(',')[0]
        rtb_insti_false = mixed_non_test_mode_edsp.split(',')[1]
        rtb_insti_true = mixed_non_test_mode_edsp.split(',')[2]
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_insti_null)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_insti_false)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_insti_true)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('Refactor bidder')
    @allure.tag('normal')
    @allure.story('PBJ-2864 Refactor bidder package')
    @allure.description('Verify jaeger serve request correctly with playable placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_add_mixed_rtb_ids_auction_2(self, pub_app_id):
        device_id = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_third_party_placement_crtype_02,
                                            ifa=device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=mixed_non_test_mode_edsp_with_playable))
        rtb_no_playable = mixed_non_test_mode_edsp_with_playable.split(',')[0]
        rtb_playable = mixed_non_test_mode_edsp_with_playable.split(',')[1]
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_no_playable)
        assert_keys_exist(bid_request['imp'][0], 'video')
        assert_keys_not_exist(bid_request['imp'][0], 'banner')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_playable)
        assert_keys_exist(bid_request['imp'][0], 'video')
        assert_keys_exist(bid_request['imp'][0], 'banner')

    @allure.feature('Refactor bidder')
    @allure.tag('normal')
    @allure.story('PBJ-2864 Refactor bidder package')
    @allure.description('Verify jaeger serve request correctly for non playable placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_add_mixed_rtb_ids_auction_3(self, pub_app_id):
        device_id = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement,
                                            ifa=device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=mixed_non_test_mode_edsp_with_playable))
        rtb_no_playable = mixed_non_test_mode_edsp_with_playable.split(',')[0]
        rtb_playable = mixed_non_test_mode_edsp_with_playable.split(',')[1]
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_no_playable)
        assert_keys_exist(bid_request['imp'][0], 'video')
        assert_keys_not_exist(bid_request['imp'][0], 'banner')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_playable)
        assert_keys_exist(bid_request['imp'][0], 'video')
        assert_keys_not_exist(bid_request['imp'][0], 'banner')

    @allure.feature('Refactor bidder')
    @allure.tag('normal')
    @allure.story('PBJ-2864 Refactor bidder package')
    @allure.description('Verify jaeger serve request correctly for internal, external and liftoff attend auction')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_add_mixed_rtb_ids_auction_4(self, pub_app_id):
        device_id = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement,
                                            ifa=device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=mixed_non_test_mode_rtb_ids))
        rtb_internal = mixed_non_test_mode_rtb_ids.split(',')[0]
        rtb_external = mixed_non_test_mode_rtb_ids.split(',')[1]
        rtb_liftoff = mixed_non_test_mode_rtb_ids.split(',')[2]
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_internal)
        assert_keys_exist(bid_request['device']['ext'], 'vungle')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_external)
        assert_keys_not_exist(bid_request['device']['ext'], 'vungle')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_liftoff)
        assert_keys_exist(bid_request['device']['ext'], 'vungle')

    @allure.feature('Refactor bidder')
    @allure.tag('normal')
    @allure.story('PBJ-2864 Refactor bidder package')
    @allure.description('Verify banner.imp.ext.rp for XAPI and other eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_add_mixed_rtb_ids_auction_5(self, pub_app_id):
        device_id = test_mode_device_id
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_banner_placement,
                                            ifa=device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=mixed_test_mode_rtb_banner))
        rtb_ext = mixed_test_mode_rtb_banner.split(',')[0]
        rtb_xapi = mixed_test_mode_rtb_banner.split(',')[1]
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ext)
        assert_keys_not_exist(bid_request['imp'][0]['banner'], 'ext')
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_xapi)
        assert_keys_exist(bid_request['imp'][0]['banner']['ext'], 'rp')

    @allure.feature('xapi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-2809 Create HTTP authentication header for XAPI integration')
    @allure.description('Verify the auth token from the bid request header for XAPI eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_xapi_auth_header_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_xapi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request_header = get_bid_request_obj_from_jaeger_explain(response_payload, content='Header')
        assert_keys_exist(bid_request_header, 'Authorization')

    @allure.feature('xapi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-2809 Create HTTP authentication header for XAPI integration')
    @allure.description('Verify the auth token from the bid request header for XAPI eDSP via hb traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_xapi_auth_header_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_xapi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request_header = get_bid_request_obj_from_jaeger_explain(response_payload, content='Header')
        assert_keys_exist(bid_request_header, 'Authorization')

    @allure.feature('xapi suuport')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-2809 Create HTTP authentication header for XAPI integration')
    @allure.description('Verify the auth token from the bid request header for XAPI eDSP with programmatic banner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_xapi_auth_header_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_banner_xapi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request_header = get_bid_request_obj_from_jaeger_explain(response_payload, content='Header')
        assert_keys_exist(bid_request_header, 'Authorization')

    @allure.feature('xapi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-2809 Create HTTP authentication header for XAPI integration')
    @allure.description('Verify there is no auth token from the bid request header for non-XAPI eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_xapi_auth_header_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request_header = get_bid_request_obj_from_jaeger_explain(response_payload, content='Header')
        assert_keys_not_exist(bid_request_header, 'Authorization')

    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4103 Max Duration Testing'
                  'PBJ-4280 Max Duration - High Priority Publishers')
    @allure.description('Test max duration and skipafter in case of skipable is true for interstial placement enter experiment'
                        'Legacy Video Max Duration Experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_apps', max_duration_apps_skippable_true)
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_max_duration_01(self, pub_apps, rtb_ids):
        '''
             db setting: placement level
             is_skippable: true


             application level:
             maxVideoLength: 46
        '''

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_android(pub_apps['pub_app'], pub_apps['placement'], ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        maxDuration = bid_request['imp'][0]['video']['maxduration']
        video = bid_request['imp'][0]['video']
        assert_that(maxDuration, equal_to(120))
        assert_that(video['skip'], equal_to(1))
        assert_keys_exist(video, 'skipafter')
        assert_that(video['skipafter'], equal_to(5))

    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4103 Max Duration Testing'
                  'PBJ-4280 Max Duration - High Priority Publishers')
    @allure.description('Test max duration and skipafter in case of skipable is true with duration'
                        ' for interstial placement enter exp \'Legacy Video Max Duration Experiment\'')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_apps', max_duration_apps_skippable_true_with_duration)
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_max_duration_02(self, pub_apps, rtb_ids):
        '''
        db setting: placement level
        is_skippable: true
        skip_after: 10


        application level:
        maxVideoLength: 46
        '''

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_android(pub_apps['pub_app'], pub_apps['placement'], ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        maxDuration = bid_request['imp'][0]['video']['maxduration']
        video = bid_request['imp'][0]['video']
        assert_that(maxDuration, equal_to(120))
        assert_that(video['skip'], equal_to(1))
        assert_keys_exist(video, 'skipafter')
        assert_that(video['skipafter'], equal_to(10))

    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4103 Max Duration Testing'
                  'PBJ-4280 Max Duration - High Priority Publishers')
    @allure.description('Test max duration and skipafter in case of skipable is false for interstial placement does not'
                        'enter the experiment ')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_apps', max_duration_apps_skippable_false)
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_max_duration_03(self, pub_apps, rtb_ids):
        '''
             db setting: placement level
             is_skippable: false


             application level:
             maxVideoLength: 46
        '''

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_android(pub_apps['pub_app'], pub_apps['placement'], ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_keys_not_exist(video, 'skip')
        assert_that(video['maxduration'], equal_to(46))

    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4103 Max Duration Testing'
                  'PBJ-4280 Max Duration - High Priority Publishers')
    @allure.description('Test max duration and skipafter in case of skipable is true for rewarded placement '
                        'not enter experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_apps', max_duration_rewarded_apps)
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_max_duration_04(self, pub_apps, rtb_ids):
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_apps['pub_app'], pub_apps['placement'], ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        maxDuration = bid_request['imp'][0]['video']['maxduration']
        video = bid_request['imp'][0]['video']
        if 'skip' in video:
            assert_that(video['skip'], equal_to(1))
        if 'skipafter' in video:
            assert_that(video['skipafter'], equal_to(10))
        assert_that(maxDuration, equal_to(32))

    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4103 Max Duration Testing'
                  'PBJ-4280 Max Duration - High Priority Publishers')
    @allure.description('Test max duration and skipafter all type of placements not in max duration experiment list')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50916IMA1'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_max_duration_05(self, pub_app, placement, rtb_ids):
        '''

        app setting:
        maxVideoLength: 46

        placement setting:
        is_skippable: true
        skip_after: 6
        '''

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_that(video['maxduration'], equal_to(46))
        assert_that(video['skip'], equal_to(1))
        assert_that(video['skipafter'], equal_to(6))

    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4103 Max Duration Testing'
                  'PBJ-4280 Max Duration - High Priority Publishers')
    @allure.description('Test max duration and skipafter all type of placements not in max duration experiment list')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_max_duration_06(self, pub_app, placement, rtb_ids):
        '''

        app setting:
        maxVideoLength: 46

        placement setting:
        is_skippable: false
        '''

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_that(video['maxduration'], equal_to(46))

    @allure.feature('max duration')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4103 Max Duration Testing')
    @allure.description('Test max duration and skipafter in case of skipable is true for interstial placement '
                        'via test mode enter the experiment \'Legacy Video Max Duration Experiment\'')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_apps', max_duration_apps)
    @pytest.mark.parametrize('rtb_ids', [ext_test_mode_kraken_rtb_ids_mraid])
    def test_max_duration_071(self, pub_apps, rtb_ids):
        '''
             db setting: placement level
             is_skippable: true


             application level:
             maxVideoLength: 32
        '''

        test_ifa = test_mode_device_id
        req = request_payload.jaeger_v5_ios(pub_apps['pub_app'], pub_apps['placement'], ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        maxDuration = bid_request['imp'][0]['video']['maxduration']
        video = bid_request['imp'][0]['video']
        assert_that(maxDuration, equal_to(120))
        assert_that(video['skip'], equal_to(1))
        assert_keys_exist(video, 'skipafter')
        assert_that(video['skipafter'], equal_to(5))

    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4280 Max Duration - High Priority Publishers')
    @allure.description('Test pub app enther the experiment \'Video Max Duration Experiment\' '
                        'via test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [max_duration_app_exp1])
    @pytest.mark.parametrize('placement_id', [max_duration_placement_exp1])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_max_duration_exp1_01(self, pub_app, placement_id, rtb_ids):
        '''
             db setting: placement level
             is_skippable: true


             application level:
             maxVideoLength: 32
        '''

        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        maxDuration = bid_request['imp'][0]['video']['maxduration']
        video = bid_request['imp'][0]['video']
        assert_that(maxDuration in [32, 120])
        assert_that(video['skip'], equal_to(1))
        if maxDuration == 120:
            assert_keys_exist(video, 'skipafter')
            assert_that(video['skipafter'], equal_to(5))
        else:
            assert_keys_not_exist(video, 'skipafter')

    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4103 Max Duration Testing')
    @allure.description('Test max duration and skipafter in case of skipable is false for interstial placement will '
                        'not enter'
                        'experiment \'Video Max Duration Experiment\'')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [max_duration_app_skipable_false_exp1])
    @pytest.mark.parametrize('placement_id', [max_duration_placement_skipable_exp1])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_max_duration_exp1_02(self, pub_app, placement_id, rtb_ids):
        '''
             db setting: placement level
             is_skippable: false


             application level:
             maxVideoLength: 46
        '''

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_android(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_keys_not_exist(video, 'skip')
        assert_that(video['maxduration'], equal_to(46))

    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4103 Max Duration Testing')
    @allure.description('Test max duration and skipafter in case of skipable is true with duration'
                        ' for interstial placement will enter experiment \'Video Max Duration Experiment\'')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [max_duration_apps_skippable_true_with_duration_exp1])
    @pytest.mark.parametrize('placement_id', [max_duration_placement_skippable_true_with_duration_exp1])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_max_duration_exp1_03(self, pub_app, placement_id, rtb_ids):
        '''
           db setting: placement level
           is_skippable: true
           skip_after: 10


           application level:
           maxVideoLength: 46
        '''

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_android(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        maxDuration = bid_request['imp'][0]['video']['maxduration']
        video = bid_request['imp'][0]['video']
        assert_that(maxDuration in [46, 120])
        assert_that(video['skip'], equal_to(1))
        assert_keys_exist(video, 'skipafter')
        assert_that(video['skipafter'], equal_to(10))


    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4103 Max Duration Testing')
    @allure.description('Test max duration and skipafter in case of skipable is true without duration'
                        ' for interstial placement will enter experiment \'Video Max Duration Experiment\'')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [max_duration_app_skippable_true_exp1])
    @pytest.mark.parametrize('placement_id', [max_duration_placement_skippable_true_exp1])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_max_duration_exp1_04(self, pub_app, placement_id, rtb_ids):
        '''
           db setting: placement level
           is_skippable: true


           application level:
           maxVideoLength: 46
        '''

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_android(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        maxDuration = bid_request['imp'][0]['video']['maxduration']
        video = bid_request['imp'][0]['video']
        assert_that(maxDuration in [46, 120])
        if maxDuration == 120:
            assert_that(video['skip'], equal_to(1))
            assert_keys_exist(video, 'skipafter')
            assert_that(video['skipafter'], equal_to(5))
        elif maxDuration == 46:
            assert_keys_not_exist(video, 'skipafter')



    @allure.feature('max duration')
    @allure.tag('normal')
    @allure.story('PBJ-4103 Max Duration Testing')
    @allure.description('Test max duration and skipafter in case of skipable is true without duration'
                        ' for rewarded placement does not enter experiment \'Video Max Duration Experiment\'')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [max_duration_app_rewarded_exp1])
    @pytest.mark.parametrize('placement_id', [max_duration_placement_rewarded_exp1])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_max_duration_exp1_05(self, pub_app, placement_id, rtb_ids):
        '''
           db setting: placement level
           is_skippable: true


           application level:
           maxVideoLength: 46
        '''

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_android(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        maxDuration = bid_request['imp'][0]['video']['maxduration']
        assert_that(maxDuration, equal_to(46))



    @allure.feature('skip after')
    @allure.tag('normal')
    @allure.story('PBJ-4580 Send Skipafter to DSP partners')
    @allure.description('Test app level: skip=true and close_button_delay!="" & placement level: skip=true and '
                        'close_button_delay!=""')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_skipafter_to_dsp_01(self, pub_app, placement_id, rtb_ids):
        """
           app level setting:
                forceView:false
                "adExperience": {
                    "multi_ec_close_button_delay": 11,
                    "multi_video_close_button_delay": 10,
                    "single_close_button_delay": 12
                }
           placement level setting:
                is_skippable: true
                "multi_ec_close_button_delay": 16,
                "multi_video_close_button_delay": 15,
                "single_close_button_delay": 17
        """

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_that(video['skip'], equal_to(1))
        assert_keys_exist(video, 'skipafter')
        assert_that(video['skipafter'], equal_to(15))



    @allure.feature('skip after')
    @allure.tag('normal')
    @allure.story('PBJ-4580 Send Skipafter to DSP partners')
    @allure.description('Test app level: skip=true and close_button_delay!="" & placement level: skip=true and '
                        'close_button_delay=""')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement_instl2])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_skipafter_to_dsp_02(self, pub_app, placement_id, rtb_ids):
        """
           app level setting:
                forceView:false
                "adExperience": {
                    "multi_ec_close_button_delay": 11,
                    "multi_video_close_button_delay": 10,
                    "single_close_button_delay": 12
                }
           placement level setting:
                is_skippable: true
                "multi_ec_close_button_delay": null,
                "multi_video_close_button_delay": null,
                "single_close_button_delay": null
        """

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_that(video['skip'], equal_to(1))
        assert_keys_exist(video, 'skipafter')
        assert_that(video['skipafter'], equal_to(10))


    @allure.feature('skip after')
    @allure.tag('normal')
    @allure.story('PBJ-4580 Send Skipafter to DSP partners')
    @allure.description('Test app level: skip=true and close_button_delay!="" & placement level: skip=false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement_instl3])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_skipafter_to_dsp_03(self, pub_app, placement_id, rtb_ids):
        """
           app level setting:
                forceView:false
                "adExperience": {
                    "multi_ec_close_button_delay": 11,
                    "multi_video_close_button_delay": 10,
                    "single_close_button_delay": 12
                }
           placement level setting:
                is_skippable: false,
                is_incentivized: false
        """

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_keys_not_exist(video, 'skip')
        assert_keys_not_exist(video, 'skipafter')


    @allure.feature('skip after')
    @allure.tag('normal')
    @allure.story('PBJ-4580 Send Skipafter to DSP partners')
    @allure.description('Test app level: forceView=true  & placement level: skip=true and '
                        'close_button_delay=1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1_instl])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_skipafter_to_dsp_04(self, pub_app, placement_id, rtb_ids):
        """
           app level setting:
                forceView:true
                # "adExperience": {
                #     "multi_ec_close_button_delay": 11,
                #     "multi_video_close_button_delay": 10,
                #     "single_close_button_delay": 12
                # }
           placement level setting:
                is_skippable: true
                "multi_ec_close_button_delay": 2,
                "multi_video_close_button_delay": 1,
                "single_close_button_delay": 3
        """

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_that(video['skip'], equal_to(1))
        assert_keys_exist(video, 'skipafter')
        assert_that(video['skipafter'], equal_to(1))



    @allure.feature('skip after')
    @allure.tag('normal')
    @allure.story('PBJ-4580 Send Skipafter to DSP partners')
    @allure.description('Test app level: forceView:true & placement level: skip=true and '
                        'close_button_delay=""')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1_instl1])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_skipafter_to_dsp_05(self, pub_app, placement_id, rtb_ids):
        """
           app level setting:
                forceView:true
                # "adExperience": {
                #     "multi_ec_close_button_delay": 11,
                #     "multi_video_close_button_delay": 10,
                #     "single_close_button_delay": 12
                # }
           placement level setting:
                is_skippable: true
                "multi_video_close_button_delay": null,

        """

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_that(video['skip'], equal_to(1))
        assert_keys_exist(video, 'skipafter')
        assert_that(video['skipafter'], equal_to(9999))


    @allure.feature('skip after')
    @allure.tag('normal')
    @allure.story('PBJ-4580 Send Skipafter to DSP partners')
    @allure.description('Test app level: forceView:true  & placement level: skip=false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1_instl2])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_skipafter_to_dsp_06(self, pub_app, placement_id, rtb_ids):
        """
           app level setting:
                forceView:false
                "adExperience": {
                    "multi_ec_close_button_delay": 11,
                    "multi_video_close_button_delay": 10,
                    "single_close_button_delay": 12
                }
           placement level setting:
                is_skippable: false
        """

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_keys_not_exist(video, 'skip')
        assert_keys_not_exist(video, 'skipafter')



    @allure.feature('skip after')
    @allure.tag('normal')
    @allure.story('PBJ-4580 Send Skipafter to DSP partners')
    @allure.description('Test skip field not exist: placement: is_skippable=null, is_incentivized=false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement_instl4])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_skip_field_01(self, pub_app, placement_id, rtb_ids):
        """
           app level setting:
                forceView:false
                forceViewIncentivized: true
                "adExperience": {
                    "multi_ec_close_button_delay": 11,
                    "multi_video_close_button_delay": 10,
                    "single_close_button_delay": 12
                }
           placement level setting:

                is_incentivized: true
        """

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_keys_not_exist(video, 'skip')


    @allure.feature('skip after')
    @allure.tag('normal')
    @allure.story('PBJ-4580 Send Skipafter to DSP partners')
    @allure.description('Test skip field  exist: placement is_incentivized = false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement_instl5])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids,
                                         ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_skip_field_02(self, pub_app, placement_id, rtb_ids):
        """
           app level setting:
                forceView:false
                forceViewIncentivized: true
                "adExperience": {
                    "multi_ec_close_button_delay": 11,
                    "multi_video_close_button_delay": 10,
                    "single_close_button_delay": 12
                }
           placement level setting:

                is_incentivized: false
        """

        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app, placement_id, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        video = bid_request['imp'][0]['video']
        assert_keys_exist(video, 'skip')
        assert_keys_exist(video, 'skipafter')
        assert_that(video['skipafter'], equal_to(10))

    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify hb flag is added for rtb support extension type=default_hb via edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_refactor_supported_extension_default_hb_01(self, pub_app_id, placement, header_bidding):
        """
        rtb_setting:
         "supported_extension_type": "default_hb"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext1_non_kraken_test_mode_default_hb,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        source_ext = bid_request['source']['ext']
        assert_keys_exist(source_ext, 'header_bidding')
        if header_bidding:
            assert_that(source_ext['header_bidding'], equal_to(1))
        else:
            assert_that(source_ext['header_bidding'], equal_to(0))

    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify hb flag does not add for rtb support extension type=default_hb via idsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [False])
    def test_refactor_supported_extension_default_hb_02(self, pub_app_id, placement, header_bidding):
        """

        rtb_setting:
         "supported_extension_type": "default_hb"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_int1_rtb_ids,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        source_ext = bid_request['source']['ext']
        assert_keys_not_exist(source_ext, 'header_bidding')

    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing'
                  'PBJ-4857 [SPO] Auction ID shows original one on duplicate Bid Requests')
    @allure.description('Verify bidrequest_id  for rtb support extension type=default_dup via edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_refactor_supported_extension_default_dup_01(self, pub_app_id, placement):
        """
          rtb_setting:
           "supported_extension_type": "default_dup"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext2_non_kraken_test_mode_default_dup,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        bid_request_id = bid_request['id']
        assert_that("___" in bid_request_id)
        bid_request_id_suffix = int(bid_request_id.split('___')[1])
        assert_that(isinstance(bid_request_id_suffix, int))
        # Validated that kraken-ext1-apiqa-kraken will receive loss notification with dup auction id
        # such as: Got notifications: /lurl?min=&event_id=6363a5ebef11790106511b93___2787"}

    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify the feature will not impact idsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_refactor_supported_extension_default_dup_i(self, pub_app_id, placement):
        """

         rtb_setting:
          "supported_extension_type": "vungle_dup"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids_vungle_dup,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        bid_request_id = bid_request['id']
        assert_that("___" not in bid_request_id)

    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify bidrequest_id  for rtb support extension type=liftoff_dup via liftoff')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_refactor_supported_extension_default_dup_liftoff(self, pub_app_id, placement):
        """

           rtb_setting:
            "supported_extension_type": "liftoff_dup"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=liftoff_rtbids_liftoff_dup,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        bid_request_id = bid_request['id']
        assert_that("___" in bid_request_id)
        bid_request_id_suffix = int(bid_request_id.split('___')[1])
        assert_that(isinstance(bid_request_id_suffix, int))

    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify bidrequest_id  for rtb support extension type=liftoff_DUP via liftoff')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_refactor_supported_extension_default_dup_liftoff_01(self, pub_app_id, placement):
        """
        rtb_setting:
         "supported_extension_type": "liftoff_dup=123"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=liftoff_rtbids_liftoff_specify_dup,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        bid_request_id = bid_request['id']
        assert_that('___' in bid_request_id)
        bid_request_id_suffix = bid_request_id.split('___')[1]
        assert_that(bid_request_id_suffix, equal_to('123'))



    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify bidrequest_id  for same rtb muti dup')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_refactor_supported_extension_default_dup_for_3_liftoff_rtb(self, pub_app_id, placement):
        """

        rtb_setting:
         "634d125e98c5395c9f094d6d":"supported_extension_type": "liftoff_DUP"
         "634cc7a998c5395c9f094d63":"supported_extension_type": "liftoff_dup"
         "615464e663244e95d2626a4f":"supported_extension_type": "liftoff"
        """
        rtb_ids = '634d125e98c5395c9f094d6d,634cc7a998c5395c9f094d63,615464e663244e95d2626a4f'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request1 = get_bid_request_obj_from_jaeger_explain(response_payload,'634d125e98c5395c9f094d6d')
        bid_request_id1 = bid_request1['id']
        bid_request2 = get_bid_request_obj_from_jaeger_explain(response_payload, '634cc7a998c5395c9f094d63')
        bid_request_id2 = bid_request2['id']
        bid_request3 = get_bid_request_obj_from_jaeger_explain(response_payload, '615464e663244e95d2626a4f')
        bid_request_id3 = bid_request3['id']
        assert_that("___" in bid_request_id1)
        assert_that("___" in bid_request_id2)
        assert_that("___" in bid_request_id3)
        assert_that(bid_request_id1, not equal_to(bid_request_id2))




    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify bidrequest_id  for different rtb muti dup')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_refactor_supported_extension_default_dup_for_different_rtb(self, pub_app_id, placement):
        """

        rtb_setting:
         "60a277a5b3bbef2c0884d8bc":
         "634cc68f98c5395c9f094d5f":"supported_extension_type": "default_dup"
         "634cc7a998c5395c9f094d63":"supported_extension_type": "liftoff_dup"
         "615464e663244e95d2626a4f":"supported_extension_type": "liftoff"
        """
        rtb_ids = '60a277a5b3bbef2c0884d8bc,634cc68f98c5395c9f094d5f,634cc7a998c5395c9f094d63,615464e663244e95d2626a4f'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request1 = get_bid_request_obj_from_jaeger_explain(response_payload, '60a277a5b3bbef2c0884d8bc')
        bid_request_id1 = bid_request1['id']
        bid_request2 = get_bid_request_obj_from_jaeger_explain(response_payload, '634cc68f98c5395c9f094d5f')
        bid_request_id2 = bid_request2['id']
        bid_request3 = get_bid_request_obj_from_jaeger_explain(response_payload, '634cc7a998c5395c9f094d63')
        bid_request_id3 = bid_request3['id']
        bid_request4 = get_bid_request_obj_from_jaeger_explain(response_payload, '615464e663244e95d2626a4f')
        bid_request_id4 = bid_request4['id']
        assert_that("___" not in bid_request_id1)
        assert_that("___" in bid_request_id2)
        assert_that("___" in bid_request_id3)
        assert_that("___" in bid_request_id4)
        assert_that(bid_request_id2, not equal_to(bid_request_id3))


    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify bidrequest_id  for rtb support extension type=default_dup_hb')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_refactor_supported_extension_mutiple_catgory_01(self, pub_app_id, placement, header_bidding):
        """

        rtb_setting:
         "supported_extension_type": "default_dup_hb"
         or
         "supported_extension_type": "default_hb_dup"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext1_non_kraken_test_mode_mutiple_category,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          ))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        bid_request_id = bid_request['id']
        assert_that("___" in bid_request_id)
        bid_request_id_suffix = int(bid_request_id.split('___')[1])
        assert_that(isinstance(bid_request_id_suffix, int))

        source_ext = bid_request['source']['ext']
        assert_keys_exist(source_ext, 'header_bidding')
        if header_bidding:
            assert_that(source_ext['header_bidding'], equal_to(1))
        else:
            assert_that(source_ext['header_bidding'], equal_to(0))

    @allure.feature('HB flag')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4831 HB Flag: Expose "passing HB flag to DSP partners" through dashboard')
    @allure.description('Verify hb flag enabled and also in support extension type')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_hb_flag_01(self, pub_app_id, placement, header_bidding):
        """
        rtb_setting:
         "supported_extension_type": "default_hb"
         "allow_hb_flag": true
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext1_non_kraken_test_mode_default_hb,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        source_ext = bid_request['source']['ext']
        assert_keys_exist(source_ext, 'header_bidding')
        if header_bidding:
            assert_that(source_ext['header_bidding'], equal_to(1))
        else:
            assert_that(source_ext['header_bidding'], equal_to(0))


    @allure.feature('HB flag')
    @allure.tag('normal' , 'v1.245.0')
    @allure.story('PBJ-4831 HB Flag: Expose "passing HB flag to DSP partners" through dashboard')
    @allure.description('Verify hb flag enabled and does not exist support extension type')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_hb_flag_02(self, pub_app_id, placement, header_bidding):
        """
        rtb_setting:
         "allow_hb_flag": true
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext1_non_kraken_test_mode_default_consentstring,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        source_ext = bid_request['source']['ext']
        assert_keys_exist(source_ext, 'header_bidding')
        if header_bidding:
            assert_that(source_ext['header_bidding'], equal_to(1))
        else:
            assert_that(source_ext['header_bidding'], equal_to(0))


    @allure.feature('HB flag')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4831 HB Flag: Expose "passing HB flag to DSP partners" through dashboard')
    @allure.description('Verify hb flag false and also exist support extension type="default_hb"')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_hb_flag_03(self, pub_app_id, placement, header_bidding):
        """
        rtb_setting:
         "allow_hb_flag": false
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext1_non_kraken_test_mode_mutiple_category,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        source_ext = bid_request['source']['ext']
        assert_keys_exist(source_ext, 'header_bidding')
        if header_bidding:
            assert_that(source_ext['header_bidding'], equal_to(1))
        else:
            assert_that(source_ext['header_bidding'], equal_to(0))



    @allure.feature('HB flag')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4831 HB Flag: Expose "passing HB flag to DSP partners" through dashboard')
    @allure.description('Verify hb flag false and does not exist support extension type="default_hb"')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_hb_flag_04(self, pub_app_id, placement, header_bidding):
        """
        rtb_setting:
         "allow_hb_flag": false
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_consentString,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        source_ext = bid_request['source']['ext']
        assert_keys_not_exist(source_ext, 'header_bidding')



    @allure.feature('HB flag')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4831 HB Flag: Expose "passing HB flag to DSP partners" through dashboard')
    @allure.description('Verify unset hb flag and does not exist support extension type="default_hb"')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_hb_flag_05(self, pub_app_id, placement, header_bidding):
        """
        rtb_setting:
         unset allow_hb_flag
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_aarki,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        source_ext = bid_request['source']['ext']
        assert_keys_not_exist(source_ext, 'header_bidding')


    @allure.feature('HB flag')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4831 HB Flag: Expose "passing HB flag to DSP partners" through dashboard')
    @allure.description('Verify unset hb flag and exist support extension type="default_hb"')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_hb_flag_06(self, pub_app_id, placement, header_bidding):
        """
        rtb_setting:
         unset allow_hb_flag
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_mutiple_category,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        source_ext = bid_request['source']['ext']
        assert_keys_exist(source_ext, 'header_bidding')
        if header_bidding:
            assert_that(source_ext['header_bidding'], equal_to(1))
        else:
            assert_that(source_ext['header_bidding'], equal_to(0))


    @allure.feature('support extension type')
    @allure.tag('normal' ,'v1.245.0')
    @allure.story('PBJ-4816 [SPO] Allow VX sends more than one duplicate Bid Requests to Accelerate')
    @allure.description('Verify user can specified the suffix of duplication request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_specified_the_suffix_default_dup_01(self, pub_app_id, placement):
        """
          rtb_setting:
           "supported_extension_type": "default_dup=specifyDefalut"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext2_non_kraken_test_mode_spec_default_dup,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        bid_request_id = bid_request['id']
        assert_that("___" in bid_request_id)
        bid_request_id_suffix = bid_request_id.split('___')[1]
        assert_that(bid_request_id_suffix, equal_to("specifydefalut"))
        source_ext = bid_request['source']['ext']
        assert_keys_not_exist(source_ext, 'header_bidding')


    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4816 [SPO] Allow VX sends more than one duplicate Bid Requests to Accelerate')
    @allure.description('Verify user can specified the suffix of duplication request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_specified_the_suffix_liftoff_dup_02(self, pub_app_id, placement):
        """
          rtb_setting:
           "supported_extension_type": "liftoff_dup=123"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=liftoff_rtbids_liftoff_specify_dup,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        bid_request_id = bid_request['id']
        assert_that("___" in bid_request_id)
        bid_request_id_suffix = bid_request_id.split('___')[1]
        assert_that(bid_request_id_suffix, equal_to("123"))
        source_ext = bid_request['source']['ext']
        assert_keys_not_exist(source_ext, 'header_bidding')


    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4816 [SPO] Allow VX sends more than one duplicate Bid Requests to Accelerate')
    @allure.description('Verify user can specified the suffix of duplication request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_specified_the_default_mutiple_category(self, pub_app_id, placement, header_bidding):
        """
          rtb_setting:
           "supported_extension_type": "default_dup=specifyDefalut_hb"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext2_non_kraken_test_mode_spec_default_mutiple_category,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        bid_request_id = bid_request['id']
        assert_that("___" in bid_request_id)
        bid_request_id_suffix = bid_request_id.split('___')[1]
        assert_that(bid_request_id_suffix, equal_to("specifydefalut"))

        source_ext = bid_request['source']['ext']
        assert_keys_exist(source_ext, 'header_bidding')
        if header_bidding:
            assert_that(source_ext['header_bidding'], equal_to(1))
        else:
            assert_that(source_ext['header_bidding'], equal_to(0))



    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4816 [SPO] Allow VX sends more than one duplicate Bid Requests to Accelerate')
    @allure.description('Verify user can specified the suffix of duplication request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_specified_the_liftoff_mutiple_category(self, pub_app_id, placement, header_bidding):
        """
          rtb_setting:
           "supported_extension_type": "liftoff_dup=123_hb"
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=liftoff_rtbids_liftoff_specify_mutiple_category,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        bid_request_id = bid_request['id']
        assert_that("___" in bid_request_id)
        bid_request_id_suffix = bid_request_id.split('___')[1]
        assert_that(bid_request_id_suffix, equal_to("123"))

        source_ext = bid_request['source']['ext']
        assert_keys_exist(source_ext, 'header_bidding')
        if header_bidding:
            assert_that(source_ext['header_bidding'], equal_to(1))
        else:
            assert_that(source_ext['header_bidding'], equal_to(0))



    @allure.feature('support extension type')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4816 [SPO] Allow VX sends more than one duplicate Bid Requests to Accelerate')
    @allure.description('Verify user can specified the suffix of duplication request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_notification_dup_id_is_specified(self, pub_app_id, placement):
        """
          rtb_setting:

           rtb1:636dea4131cc74fcc2717bdc ("supported_extension_type": "default_dup=specifyDefalut")
           rtb2:636def3b31cc74fcc2717be0 ("supported_extension_type": "liftoff_dup=123")
        """
        lurl = 'http://kraken-lo1-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?mbtw=${MIN_BID_TO_WIN}&exbtw=${EX_MIN_BID_TO_WIN}&exbtwv=${EX_MIN_BID_TO_WIN_V}&event_id=${AUCTION_ID}'
        over_ride_lurl = 'seatbid.0.bid.0.lurl@"%s"' % lurl
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector="636dea4131cc74fcc2717bdc,636def3b31cc74fcc2717be0",
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          override_bid_response_any=over_ride_lurl))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        bid_request_id = bid_request['id']
        assert_that("___" in bid_request_id)
        bid_request_id_suffix = bid_request_id.split('___')[1]
        assert_that(bid_request_id_suffix in ["specifydefalut", "123"])
        # Validated that kraken-lo1-apiqa-kraken will receive loss notification with the specified dup auction id
        # such as: Got notifications: /lurl?mbtw=&exbtw=&exbtwv=&event_id=636dfa4e878a7c4899408561___123"}



    @allure.feature('support extension type')
    @allure.tag('normal')
    @allure.story('PBJ-4953 [SPO] Way to flag multi-bidding traffic on LO control group')
    @allure.description('Verify liftoff RTB will add "___ctl" suffix if another liftoff rtb specify with _dup')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_dup_id_for_liftoff_01(self, pub_app_id, placement):
        """
          rtb_setting:

           rtb1:6114dfcd09ef564172e38113 ("supported_extension_type": "liftoff")
           rtb2:636def3b31cc74fcc2717be0 ("supported_extension_type": "liftoff_dup=123")
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector="6114dfcd09ef564172e38113,636def3b31cc74fcc2717be0",
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          ))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request1 = get_bid_request_obj_from_jaeger_explain(response_payload, '6114dfcd09ef564172e38113')
        bid_request_id1 = bid_request1['id']
        assert_that("___ctl" in bid_request_id1)

        bid_request2 = get_bid_request_obj_from_jaeger_explain(response_payload, '636def3b31cc74fcc2717be0')
        bid_request_id2 = bid_request2['id']
        assert_that("___123" in bid_request_id2)



    @allure.feature('support extension type')
    @allure.tag('normal')
    @allure.story('PBJ-4953 [SPO] Way to flag multi-bidding traffic on LO control group')
    @allure.description('Verify one liftoff RTB does not add suffix "___ctl" without specifying _dup')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_dup_id_for_liftoff_02(self, pub_app_id, placement):
        """
          rtb_setting:

           rtb1:6114dfcd09ef564172e38113 ("supported_extension_type": "liftoff")
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector="6114dfcd09ef564172e38113",
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          ))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request1 = get_bid_request_obj_from_jaeger_explain(response_payload, '6114dfcd09ef564172e38113')
        bid_request_id1 = bid_request1['id']
        assert_that("___" not in bid_request_id1)


    @allure.feature('support extension type')
    @allure.tag('normal')
    @allure.story('PBJ-4953 [SPO] Way to flag multi-bidding traffic on LO control group')
    @allure.description('Verify liftoff RTB does not add suffix "___ctl" in case of 2 rtb auction(one is liftoff, '
                        'another is one edsp with specifing _dup)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_dup_id_for_liftoff_03(self, pub_app_id, placement):
        """
          rtb_setting:

           rtb1:6114dfcd09ef564172e38113 ("supported_extension_type": "liftoff")
           rtb2:636dea4131cc74fcc2717bdc ("supported_extension_type": "default_dup=specifyDefalut")
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector="6114dfcd09ef564172e38113,636dea4131cc74fcc2717bdc",
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          ))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request1 = get_bid_request_obj_from_jaeger_explain(response_payload, '6114dfcd09ef564172e38113')
        bid_request_id1 = bid_request1['id']
        assert_that("___" not in bid_request_id1)
        bid_request2 = get_bid_request_obj_from_jaeger_explain(response_payload, '636dea4131cc74fcc2717bdc')
        bid_request_id2 = bid_request2['id']
        assert_that("___specifydefalut" in bid_request_id2)