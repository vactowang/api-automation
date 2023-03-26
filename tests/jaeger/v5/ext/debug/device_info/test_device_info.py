import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestDeviceInfo(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('device info')
    @allure.description('Verify device info from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_info_basic(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device_info']['id'], equal_to(test_ifa))
        assert_that(debug['device_info']['source'], equal_to('IFA'))

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('device info')
    @allure.description('Verify device info from debug info in test mode')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_info_in_test_mode(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device_info']['id'], equal_to(test_mode_device_id))
        assert_that(debug['device_info']['source'], equal_to('IFA'))

    @allure.feature('user privacy')
    @allure.tag('smoke', 'test_mode', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify device info from debug with non eu country ip and not match GDPR external consent')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_device_info_gdpr_non_eu_country(self, pub_app_id, consent_status):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_that(debug['device_info']['id'], not equal_to(test_mode_device_id))
                assert_that(debug['device_info']['source'], equal_to_ignoring_case('GDPR'))
            else:
                assert_that(debug['device_info']['id'], equal_to(test_mode_device_id))
                assert_that(debug['device_info']['source'], equal_to_ignoring_case('IFA'))
        else:
            assert_that(debug['device_info']['id'], equal_to(test_mode_device_id))
            assert_that(debug['device_info']['source'], equal_to_ignoring_case('IFA'))

    @allure.feature('user privacy')
    @allure.tag('smoke', 'test_mode')
    @allure.story('GDPR')
    @allure.description('Verify device info from debug when GDPR off')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_info_gdpr_opted_in(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr='opted_in',
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device_info']['id'], equal_to(test_mode_device_id))
        assert_that(debug['device_info']['source'], equal_to_ignoring_case('IFA'))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('GDPR')
    @allure.description('Verify device info from debug in GDPR status')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_info_gdpr_opted_out(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr='opted_out', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device_info']['id'], not equal_to(test_ifa))
        assert_that(debug['device_info']['source'], equal_to('GDPR'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0', 'test_mode')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify device info from debug not in GDPR status in case of Legitimate Interest is true')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_device_info_gdpr_legitimate_interest_true(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device_info']['id'], equal_to(test_mode_device_id))
        assert_that(debug['device_info']['source'], equal_to('IFA'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify device info from debug in GDPR status in case of Legitimate Interest is false')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_device_info_gdpr_legitimate_interest_false(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if ip == non_eu_country_ip or consent_status is None:
            assert_that(debug['device_info']['id'], equal_to(test_ifa))
            assert_that(debug['device_info']['source'], equal_to('IFA'))
        else:
            assert_that(debug['device_info']['id'], not equal_to(test_ifa))
            assert_that(debug['device_info']['source'], equal_to('GDPR'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify device info from debug in GDPR status in case of pre v6 flag is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_device_info_gdpr_pre_v6_true(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version='Vungle/5.9.9',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if ip == eu_country_ip:
                if consent_status == 'opted_in':
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to(test_ifa))
                else:
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(test_ifa))
            elif consent_status == 'opted_out':
                assert_that(debug['device_info']['source'], equal_to('GDPR'))
                assert_that(debug['device_info']['id'], not equal_to(test_ifa))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(test_ifa))
        else:
            if ip == eu_country_ip:
                assert_that(debug['device_info']['source'], equal_to('GDPR'))
                assert_that(debug['device_info']['id'], not equal_to(test_ifa))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(test_ifa))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify device info from debug in GDPR status in case of pre v6 flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_device_info_gdpr_pre_v6_false(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version='Vungle/5.9.9',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_that(debug['device_info']['source'], equal_to('GDPR'))
                assert_that(debug['device_info']['id'], not equal_to(test_ifa))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(test_ifa))
        else:
            assert_that(debug['device_info']['source'], equal_to('IFA'))
            assert_that(debug['device_info']['id'], equal_to(test_ifa))

    @allure.feature('user privacy')
    @allure.tag('normal', 'kiloo')
    @allure.story('GDPR kiloo')
    @allure.description('Test for Kiloo consent status override')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['58fa97228fac7a64660001d3'])
    def test_kiloo_consent_status_for_jaeger_1(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-KILOO', gdpr='unknown', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip))

        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device_info['id'], not equal_to(test_ifa))
        assert_that(device_info['source'], equal_to('GDPR'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify the status of GDPR external consents opted out, and legitimate interest is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_gdpr_external_consents_opted_out_legitimate_interest_true(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=gdpr_external_consents_opted_out_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                assert_that(debug['device_info']['source'], equal_to('GDPR'))
                assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
            else:
                if ip == eu_country_ip:
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_out_device_id))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify the status of GDPR external consents opted in, and legitimate interest is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_gdpr_external_consents_opted_in_legitimate_interest_true(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=gdpr_external_consents_opted_in_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_in_device_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify the status of GDPR external consents opted out, and legitimate interest is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_gdpr_external_consents_opted_out_legitimate_interest_false(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status,
                                            ifa=gdpr_external_consents_opted_out_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                assert_that(debug['device_info']['source'], equal_to('GDPR'))
                assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
            else:
                if ip == eu_country_ip:
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_out_device_id))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.127.0')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify the status of GDPR external consents opted in, and legitimate interest is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_gdpr_external_consents_opted_in_legitimate_interest_false(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status,
                                            ifa=gdpr_external_consents_opted_in_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                if ip == eu_country_ip:
                    if consent_status in ('opted_out', 'unknown', 'opted_out_by_timeout'):
                        assert_that(debug['device_info']['source'], equal_to('GDPR'))
                        assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_in_device_id))
                    else:
                        assert_that(debug['device_info']['source'], equal_to('IFA'))
                        assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
                else:
                    if consent_status == 'opted_out':
                        assert_that(debug['device_info']['source'], equal_to('GDPR'))
                        assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_in_device_id))
                    else:
                        assert_that(debug['device_info']['source'], equal_to('IFA'))
                        assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('GDPR')
    @allure.description('Verify the status of GDPR for Android device')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_gdpr_android(self, pub_app_id, consent_status, ip):
        '''
        "legitimate_interest": true for this account
        '''
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, gdpr=consent_status,
                                                android_id=test_id, ifa='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version='VungleDroid/6.4.0'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(test_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('ISU'))
                    assert_that(debug['device_info']['id'], equal_to(test_id))
            else:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(test_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('ISU'))
                    assert_that(debug['device_info']['id'], equal_to(test_id))
        else:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(test_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('ISU'))
                    assert_that(debug['device_info']['id'], equal_to(test_id))
            else:
                assert_that(debug['device_info']['source'], equal_to('ISU'))
                assert_that(debug['device_info']['id'], equal_to(test_id))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('GDPR')
    @allure.description('Verify the status of GDPR for Windows device')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_gdpr_windows(self, pub_app_id, consent_status, ip):
        '''
        "legitimate_interest": true for this account
        '''
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_windows(pub_app_id, windows_common_test_placement, gdpr=consent_status,
                                                ifa=test_id, ashwid=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            debug='jaeger', src_ip=ip, sdk_version='VungleWindows/6.4.0 (Windows 10; native)',
            rtb_selector=meister_rtb_ids
        ))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to_ignoring_case(test_id))
            else:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to_ignoring_case(test_id))
        else:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to_ignoring_case(test_id))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to_ignoring_case(test_id))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.138.0')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify the the device src on ashwid for Windows device')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_gdpr_windows_ashwid(self, pub_app_id, consent_status, ip):
        '''
        "legitimate_interest": true for this account
        '''
        test_id = gen_device_id()
        req = request_payload.jaeger_v5_windows(pub_app_id, windows_common_test_placement, gdpr=consent_status,
                                                ifa='', ashwid=test_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            debug='jaeger', src_ip=ip, sdk_version='VungleWindows/6.4.0 (Windows 10; native)',
            rtb_selector=meister_rtb_ids
        ))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('ASHWID'))
                    assert_that(debug['device_info']['id'], equal_to_ignoring_case(test_id))
            else:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('ASHWID'))
                    assert_that(debug['device_info']['id'], equal_to_ignoring_case(test_id))
        else:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('ASHWID'))
                    assert_that(debug['device_info']['id'], equal_to_ignoring_case(test_id))
            else:
                assert_that(debug['device_info']['source'], equal_to('ASHWID'))
                assert_that(debug['device_info']['id'], equal_to_ignoring_case(test_id))

    # ------------------------------------------ null device id ---------------------------------------------------

    @allure.feature('user privacy')
    @allure.tag('normal', 'test_mode', 'R_1.138.0')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug with non eu country ip and not match GDPR external consent, '
                        'null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    def test_device_info_gdpr_non_eu_country_null_device_id(self, pub_app_id, consent_status, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement_t, gdpr=consent_status, ifa='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        if sdk_v != 'Vungle/6.3.9':
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['id'], not equal_to(''))
                    assert_that(debug['device_info']['source'], equal_to_ignoring_case('GDPR_FP'))
                else:
                    assert_that(debug['device_info']['id'], not equal_to(''))
                    assert_that(debug['device_info']['source'], equal_to_ignoring_case('Vungle_FP'))
            else:
                assert_that(debug['device_info']['id'], not equal_to(''))
                assert_that(debug['device_info']['source'], equal_to_ignoring_case('Vungle_FP'))
        else:
            assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(86401))
            assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('malformed payload'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.138.0')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug when GDPR off, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    def test_device_info_gdpr_opted_in_null_device_id(self, pub_app_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement_t, gdpr='opted_in', ifa='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                                                        sdk_version=sdk_v))

        response_payload = r.json()
        if sdk_v != 'Vungle/6.3.9':
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(debug['device_info']['id'], not equal_to(''))
            assert_that(debug['device_info']['source'], equal_to_ignoring_case('Vungle_FP'))
        else:
            assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(86401))
            assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('malformed payload'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.138.0')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug in GDPR status, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    def test_device_info_gdpr_opted_out_null_device_id(self, pub_app_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement_t, gdpr='opted_out', ifa='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                                                        sdk_version=sdk_v))

        response_payload = r.json()
        if sdk_v != 'Vungle/6.3.9':
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(debug['device_info']['id'], not equal_to(''))
            assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
        else:
            assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(86401))
            assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('malformed payload'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.138.0')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug not in GDPR status in case of Legitimate Interest is true,'
                        'null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    def test_device_info_gdpr_legitimate_interest_true_null_device_id(self, pub_app_id, consent_status, ip, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement_t, gdpr=consent_status,
                                            ifa='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version=sdk_v))

        response_payload = r.json()
        if sdk_v != 'Vungle/6.3.9':
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(debug['device_info']['id'], not equal_to(''))
            assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
        else:
            assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(86401))
            assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('malformed payload'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.138.0')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug in GDPR status in case of Legitimate Interest is false,'
                        'null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    def test_device_info_gdpr_legitimate_interest_false_null_device_id(self, pub_app_id, consent_status, ip, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version=sdk_v))

        response_payload = r.json()
        if sdk_v != 'Vungle/6.3.9':
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if ip == non_eu_country_ip or consent_status is None:
                assert_that(debug['device_info']['id'], not equal_to(''))
                assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
            else:
                assert_that(debug['device_info']['id'], not equal_to(''))
                assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
        else:
            assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(86401))
            assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('malformed payload'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.138.0')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug in GDPR status in case of pre v6 flag is true, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_device_info_gdpr_pre_v6_true_null_device_id(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement_t, gdpr=consent_status, ifa='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version='Vungle/5.9.9'))

        response_payload = r.json()
        assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(86401))
        assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('malformed payload'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.138.0')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug in GDPR status in case of pre v6 flag is false, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_device_info_gdpr_pre_v6_false_null_device_id(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version='Vungle/5.9.9'))

        response_payload = r.json()
        assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(86401))
        assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('malformed payload'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.138.0', 'kiloo')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Test for Kiloo consent status override, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['58fa97228fac7a64660001d3'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    def test_kiloo_consent_status_for_jaeger_null_device_id(self, pub_app_id, sdk_v):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-KILOO', gdpr='unknown', ifa='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                                                        sdk_version=sdk_v))

        response_payload = r.json()
        if sdk_v != 'Vungle/6.3.9':
            device_info = response_payload['ext']['debug']['auction_result']['device_info']

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(device_info['id'], not equal_to(test_ifa))
            assert_that(device_info['source'], equal_to('Vungle_FP'))
        else:
            assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(86401))
            assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('malformed payload'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.138.0')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify the status of GDPR for Android device, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('sdk_v', ['VungleDroid/6.4.0', 'VungleDroid/6.3.9'])
    def test_gdpr_android_null_device_id(self, pub_app_id, consent_status, ip, sdk_v):
        '''
        "legitimate_interest": true for this account
        '''
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement, gdpr=consent_status,
                                                android_id='', ifa='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            if sdk_v != 'VungleDroid/6.3.9':
                debug = response_payload['ext']['debug']['auction_result']
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                if new_gdpr_flag:
                    if ip == eu_country_ip:
                        if consent_status == 'opted_out':
                            assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                            assert_that(debug['device_info']['id'], not equal_to(''))
                        else:
                            assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                            assert_that(debug['device_info']['id'], not equal_to(''))
                    else:
                        if consent_status == 'opted_out':
                            assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                            assert_that(debug['device_info']['id'], not equal_to(''))
                        else:
                            assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                            assert_that(debug['device_info']['id'], not equal_to(''))
                else:
                    if ip == eu_country_ip:
                        if consent_status == 'opted_out':
                            assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                            assert_that(debug['device_info']['id'], not equal_to(''))
                        else:
                            assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                            assert_that(debug['device_info']['id'], not equal_to(''))
                    else:
                        assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                        assert_that(debug['device_info']['id'], not equal_to(''))
            else:
                assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(86401))
                assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('malformed payload'))

    @allure.feature('user privacy')
    @allure.tag('normal', 'R_1.138.0')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify the status of GDPR for Windows device, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('sdk_v', ['VungleWindows/6.4.0 (Windows 10; native)',
                                       'VungleWindows/6.3.9 (Windows 10; native)'])
    def test_gdpr_windows_null_device_id(self, pub_app_id, consent_status, ip, sdk_v):
        '''
        "legitimate_interest": true for this account
        '''
        req = request_payload.jaeger_v5_windows(pub_app_id, windows_common_test_placement, gdpr=consent_status,
                                                ifa='', ashwid='')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip, sdk_version=sdk_v,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        if sdk_v != 'VungleWindows/6.3.9 (Windows 10; native)':
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                if ip == eu_country_ip:
                    if consent_status == 'opted_out':
                        assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                        assert_that(debug['device_info']['id'], not equal_to(''))
                    else:
                        assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                        assert_that(debug['device_info']['id'], not equal_to(''))
                else:
                    if consent_status == 'opted_out':
                        assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                        assert_that(debug['device_info']['id'], not equal_to(''))
                    else:
                        assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                        assert_that(debug['device_info']['id'], not equal_to(''))
            else:
                if ip == eu_country_ip:
                    if consent_status == 'opted_out':
                        assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                        assert_that(debug['device_info']['id'], not equal_to(''))
                    else:
                        assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                        assert_that(debug['device_info']['id'], not equal_to(''))
                else:
                    assert_that(debug['device_info']['source'], equal_to('Vungle_FP'))
                    assert_that(debug['device_info']['id'], not equal_to(''))
        else:
            assert_that(response_payload['ads'][0]['ad_markup']['sleep'], equal_to(86401))
            assert_that(response_payload['ads'][0]['ad_markup']['info'], equal_to('malformed payload'))

    # ------------------------------------------- block opted out --------------------------------------------------

    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify block opted out with non eu country ip and not match GDPR external consent')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    # def test_device_info_gdpr_non_eu_country_block_optedout(self, pub_app_id, consent_status):
    #     test_ifa = gen_device_id()
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
    #                                         ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=jp_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     if new_gdpr_flag:
    #         if consent_status == 'opted_out':
    #             ad_markup = response_payload['ads'][0]['ad_markup']
    #             assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #             assert_that('sleep' in ad_markup)
    #         else:
    #             debug = response_payload['ext']['debug']['auction_result']
    #             assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #             assert_that(debug['device_info']['id'], equal_to(test_ifa))
    #             assert_that(debug['device_info']['source'], equal_to_ignoring_case('IFA'))
    #     else:
    #         debug = response_payload['ext']['debug']['auction_result']
    #         assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #         assert_that(debug['device_info']['id'], equal_to(test_ifa))
    #         assert_that(debug['device_info']['source'], equal_to_ignoring_case('IFA'))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify block opted out with non eu country ip and not match GDPR external consent, '
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_device_info_gdpr_non_eu_country_block_optedout_1(self, pub_app_id, consent_status):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                debug = response_payload['ext']['debug']['auction_result']
                assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                assert_that(debug['device_info']['id'], not equal_to(test_ifa))
                assert_that(debug['device_info']['source'], equal_to_ignoring_case('GDPR'))
            else:
                debug = response_payload['ext']['debug']['auction_result']
                assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                assert_that(debug['device_info']['id'], equal_to(test_ifa))
                assert_that(debug['device_info']['source'], equal_to_ignoring_case('IFA'))
        else:
            debug = response_payload['ext']['debug']['auction_result']
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(debug['device_info']['id'], equal_to(test_ifa))
            assert_that(debug['device_info']['source'], equal_to_ignoring_case('IFA'))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify block opted out from debug when GDPR off, block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_info_gdpr_opted_in_block_optedout_1(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr='opted_in',
                                            ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device_info']['id'], equal_to(test_ifa))
        assert_that(debug['device_info']['source'], equal_to_ignoring_case('IFA'))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify block opted out from debug when GDPR off')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_info_gdpr_opted_in_block_optedout(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr='opted_in',
                                            ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device_info']['id'], equal_to(test_ifa))
        assert_that(debug['device_info']['source'], equal_to_ignoring_case('IFA'))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify block opted out from debug in GDPR status, block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_device_info_gdpr_opted_out_block_optedout(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr='opted_out', ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device_info']['id'], not equal_to(test_ifa))
        assert_that(debug['device_info']['source'], equal_to('GDPR'))

    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify block opted out from debug in GDPR status')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # def test_device_info_gdpr_opted_out_block_optedout_1(self, pub_app_id):
    #     test_ifa = gen_device_id(digital=36)
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr='opted_out', ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=eu_country_ip,
    #                                                                     rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     assert_that('sleep' in ad_markup)

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify block opted out from debug not in GDPR status in case of Legitimate Interest is true, '
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_device_info_gdpr_legitimate_interest_true_block_optedout(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device_info']['id'], equal_to(test_ifa))
        assert_that(debug['device_info']['source'], equal_to('IFA'))

    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify block opted out from debug not in GDPR status in case of Legitimate Interest is true')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    # @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    # def test_device_info_gdpr_legitimate_interest_true_block_optedout_1(self, pub_app_id, consent_status, ip):
    #     test_ifa = gen_device_id()
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
    #                                         ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
    #                                                                     rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']['auction_result']
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_that(debug['device_info']['id'], equal_to(test_ifa))
    #     assert_that(debug['device_info']['source'], equal_to('IFA'))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify block opted out from debug in GDPR status in case of Legitimate Interest is false,'
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_device_info_gdpr_legitimate_interest_false_block_optedout(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if ip == jp_ip or consent_status is None:
            assert_that(debug['device_info']['id'], equal_to(test_ifa))
            assert_that(debug['device_info']['source'], equal_to('IFA'))
        else:
            assert_that(debug['device_info']['id'], not equal_to(test_ifa))
            assert_that(debug['device_info']['source'], equal_to('GDPR'))

    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify block opted out from debug in GDPR status in case of Legitimate Interest is false')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    # @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    # @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    # def test_device_info_gdpr_legitimate_interest_false_block_optedout_1(self, pub_app_id, consent_status, ip):
    #     test_ifa = gen_device_id(digital=36)
    #     req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
    #                                                                     rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     if ip == jp_ip or consent_status is None:
    #         debug = response_payload['ext']['debug']['auction_result']
    #         assert_response_status_code(r.status_code, HTTPStatus.OK)
    #         assert_that(debug['device_info']['id'], equal_to(test_ifa))
    #         assert_that(debug['device_info']['source'], equal_to('IFA'))
    #     else:
    #         ad_markup = response_payload['ads'][0]['ad_markup']
    #         assert_that('sleep' in ad_markup)

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify block opted out from debug in GDPR status in case of pre v6 flag is true,'
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_device_info_gdpr_pre_v6_true_block_optedout(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version='Vungle/5.9.9',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if ip == eu_country_ip:
                if consent_status == 'opted_in':
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to(test_ifa))
                else:
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(test_ifa))
            elif consent_status == 'opted_out':
                assert_that(debug['device_info']['source'], equal_to('GDPR'))
                assert_that(debug['device_info']['id'], not equal_to(test_ifa))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(test_ifa))
        else:
            if ip == eu_country_ip:
                assert_that(debug['device_info']['source'], equal_to('GDPR'))
                assert_that(debug['device_info']['id'], not equal_to(test_ifa))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(test_ifa))

    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify block opted out from debug in GDPR status in case of pre v6 flag is true')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    # @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    # def test_device_info_gdpr_pre_v6_true_block_optedout_1(self, pub_app_id, consent_status, ip):
    #     test_ifa = gen_device_id(digital=36)
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status, ifa=test_ifa)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
    #                                                                     sdk_version='Vungle/5.9.9',
    #                                                                     rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     if new_gdpr_flag:
    #         if ip == eu_country_ip:
    #             if consent_status == 'opted_in':
    #                 debug = response_payload['ext']['debug']['auction_result']
    #                 assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #                 assert_that(debug['device_info']['source'], equal_to('IFA'))
    #                 assert_that(debug['device_info']['id'], equal_to(test_ifa))
    #             else:
    #                 ad_markup = response_payload['ads'][0]['ad_markup']
    #
    #         elif consent_status == 'opted_out':
    #             ad_markup = response_payload['ads'][0]['ad_markup']
    #
    #         else:
    #             debug = response_payload['ext']['debug']['auction_result']
    #             assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #             assert_that(debug['device_info']['source'], equal_to('IFA'))
    #             assert_that(debug['device_info']['id'], equal_to(test_ifa))
    #     else:
    #         if ip == eu_country_ip:
    #             ad_markup = response_payload['ads'][0]['ad_markup']
    #
    #         else:
    #             debug = response_payload['ext']['debug']['auction_result']
    #             assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #             assert_that(debug['device_info']['source'], equal_to('IFA'))
    #             assert_that(debug['device_info']['id'], equal_to(test_ifa))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify block opted out from debug in GDPR status in case of pre v6 flag is false,'
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_device_info_gdpr_pre_v6_false_block_optedout(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version='Vungle/5.9.9',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        debug = response_payload['ext']['debug']['auction_result']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_that(debug['device_info']['source'], equal_to('GDPR'))
                assert_that(debug['device_info']['id'], not equal_to(test_ifa))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(test_ifa))
        else:
            assert_that(debug['device_info']['source'], equal_to('IFA'))
            assert_that(debug['device_info']['id'], equal_to(test_ifa))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify block opted out from debug in GDPR status in case of pre v6 flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_device_info_gdpr_pre_v6_false_block_optedout_1(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        sdk_version='Vungle/5.9.9',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                ad_markup = response_payload['ads'][0]['ad_markup']
                assert_that('sleep' in ad_markup)
            else:
                debug = response_payload['ext']['debug']['auction_result']
                assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(test_ifa))
        else:
            debug = response_payload['ext']['debug']['auction_result']
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(debug['device_info']['source'], equal_to('IFA'))
            assert_that(debug['device_info']['id'], equal_to(test_ifa))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify the status of GDPR external consents opted out, and legitimate interest is true,'
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_gdpr_external_consents_opted_out_legitimate_interest_true_block_optedout(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=gdpr_external_consents_opted_out_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                assert_that(debug['device_info']['source'], equal_to('GDPR'))
                assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
            else:
                if ip == eu_country_ip:
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_out_device_id))

    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify the status of GDPR external consents opted out, and legitimate interest is true')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    # @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    # def test_gdpr_external_consents_opted_out_legitimate_interest_true_block_optedout_1(self, pub_app_id, consent_status, ip):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
    #                                         ifa=gdpr_external_consents_opted_out_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
    #                                                                     rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
    #         return
    #     else:
    #         if new_gdpr_flag:
    #             ad_markup = response_payload['ads'][0]['ad_markup']
    #             assert_that('sleep' in ad_markup)
    #         else:
    #             if ip == eu_country_ip:
    #                 ad_markup = response_payload['ads'][0]['ad_markup']
    #             else:
    #                 assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #                 debug = response_payload['ext']['debug']['auction_result']
    #                 assert_that(debug['device_info']['source'], equal_to('IFA'))
    #                 assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_out_device_id))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify the status of GDPR external consents opted in, and legitimate interest is true,'
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_gdpr_external_consents_opted_in_legitimate_interest_true_block_optedout(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                            ifa=gdpr_external_consents_opted_in_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                if consent_status == 'opted_out':
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_in_device_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))

    # @allure.feature('rtb blocks opted out')
    # @allure.tag('normal', 'R_1.141.0')
    # @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    # @allure.description('Verify the status of GDPR external consents opted in, and legitimate interest is true')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    # @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    # def test_gdpr_external_consents_opted_in_legitimate_interest_true_block_optedout_1(self, pub_app_id, consent_status, ip):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
    #                                         ifa=gdpr_external_consents_opted_in_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
    #                                                                     rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
    #         return
    #     else:
    #         if new_gdpr_flag:
    #             if consent_status == 'opted_out':
    #                 ad_markup = response_payload['ads'][0]['ad_markup']
    #                 assert_that('sleep' in ad_markup)
    #             else:
    #                 debug = response_payload['ext']['debug']['auction_result']
    #                 assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #                 assert_that(debug['device_info']['source'], equal_to('IFA'))
    #                 assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
    #         else:
    #             debug = response_payload['ext']['debug']['auction_result']
    #             assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #             assert_that(debug['device_info']['source'], equal_to('IFA'))
    #             assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify the status of GDPR external consents opted out, and legitimate interest is false,'
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_gdpr_external_consents_opted_out_legitimate_interest_false_block_optedout(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status,
                                            ifa=gdpr_external_consents_opted_out_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                assert_that(debug['device_info']['source'], equal_to('GDPR'))
                assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
            else:
                if ip == eu_country_ip:
                    assert_that(debug['device_info']['source'], equal_to('GDPR'))
                    assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
                else:
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_out_device_id))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify the status of GDPR external consents opted out, and legitimate interest is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_gdpr_external_consents_opted_out_legitimate_interest_false_block_optedout_1(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status,
                                            ifa=gdpr_external_consents_opted_out_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            if new_gdpr_flag:
                ad_markup = response_payload['ads'][0]['ad_markup']
            else:
                if ip == eu_country_ip:
                    ad_markup = response_payload['ads'][0]['ad_markup']
                else:
                    debug = response_payload['ext']['debug']['auction_result']
                    assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                    assert_that(debug['device_info']['source'], equal_to('IFA'))
                    assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_out_device_id))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify the status of GDPR external consents opted in, and legitimate interest is false,'
                        'block_consent_optout flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_gdpr_external_consents_opted_in_legitimate_interest_false_block_optedout(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status,
                                            ifa=gdpr_external_consents_opted_in_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            debug = response_payload['ext']['debug']['auction_result']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                if ip == eu_country_ip:
                    if consent_status in ('opted_out', 'unknown', 'opted_out_by_timeout'):
                        assert_that(debug['device_info']['source'], equal_to('GDPR'))
                        assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_in_device_id))
                    else:
                        assert_that(debug['device_info']['source'], equal_to('IFA'))
                        assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
                else:
                    if consent_status == 'opted_out':
                        assert_that(debug['device_info']['source'], equal_to('GDPR'))
                        assert_that(debug['device_info']['id'], not equal_to(gdpr_external_consents_opted_in_device_id))
                    else:
                        assert_that(debug['device_info']['source'], equal_to('IFA'))
                        assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
            else:
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))

    @allure.feature('rtb blocks opted out')
    @allure.tag('normal', 'R_1.141.0')
    @allure.story('PBJ-2048 Test filterout rtbconnection when request has consent(GDPA/CCPA) opted out')
    @allure.description('Verify the status of GDPR external consents opted in, and legitimate interest is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, jp_ip])
    def test_gdpr_external_consents_opted_in_legitimate_interest_false_block_optedout_1(self, pub_app_id, consent_status, ip):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status,
                                            ifa=gdpr_external_consents_opted_in_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ip,
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_block_optedout))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        ad_markup = response_payload['ads'][0]['ad_markup']
        if ('sleep' in ad_markup) and (ad_markup['info'] == 'publisher device exceeded placement daily delivery limit'):
            return
        else:
            if new_gdpr_flag:
                if ip == eu_country_ip:
                    if consent_status in ('opted_out', 'unknown', 'opted_out_by_timeout'):
                        ad_markup = response_payload['ads'][0]['ad_markup']
                        assert_that('sleep' in ad_markup)
                    else:
                        debug = response_payload['ext']['debug']['auction_result']
                        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                        assert_that(debug['device_info']['source'], equal_to('IFA'))
                        assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
                else:
                    if consent_status == 'opted_out':
                        ad_markup = response_payload['ads'][0]['ad_markup']
                        assert_that('sleep' in ad_markup)
                    else:
                        debug = response_payload['ext']['debug']['auction_result']
                        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                        assert_that(debug['device_info']['source'], equal_to('IFA'))
                        assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
            else:
                debug = response_payload['ext']['debug']['auction_result']
                assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                assert_that(debug['device_info']['source'], equal_to('IFA'))
                assert_that(debug['device_info']['id'], equal_to(gdpr_external_consents_opted_in_device_id))