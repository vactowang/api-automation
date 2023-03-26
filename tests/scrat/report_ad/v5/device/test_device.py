import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('scrat - report ad - v5')
class TestReportAdDevice(object):

    @allure.feature('device')
    @allure.tag('basic', 'smoke')
    @allure.story('device from debug info')
    @allure.description('Verify device from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_device_basic(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['device']['id'], equal_to(test_ifa))
        assert_that(debug['device']['id_source'], equal_to('IFA'))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify device info from debug with non eu country ip and not match GDPR external consent')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_report_ad_device_gdpr_non_eu_country_1(self, pub_app_id, consent_status):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status, ifa=test_ifa,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_that(debug['device']['id'], not equal_to(test_ifa))
                assert_that(debug['device']['id_source'], equal_to_ignoring_case('GDPR'))
            else:
                assert_that(debug['device']['id'], equal_to(test_ifa))
                assert_that(debug['device']['id_source'], equal_to_ignoring_case('IFA'))
        else:
            assert_that(debug['device']['id'], equal_to(test_ifa))
            assert_that(debug['device']['id_source'], equal_to_ignoring_case('IFA'))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('GDPR')
    @allure.description('Verify device info from debug when GDPR off')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_device_gdpr_opted_in_1(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, gdpr='opted_in', ifa=test_ifa,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=eu_country_ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device']['id'], equal_to(test_ifa))
        assert_that(debug['device']['id_source'], equal_to_ignoring_case('IFA'))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('GDPR')
    @allure.description('Verify device info from debug in GDPR status')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_device_gdpr_opted_out_1(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, gdpr='opted_out', ifa=test_ifa,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=eu_country_ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device']['id'], not equal_to(test_ifa))
        assert_that(debug['device']['id_source'], equal_to('GDPR'))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify device info from debug not in GDPR status in case of Legitimate Interest is true')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_report_ad_device_gdpr_legitimate_interest_true_1(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status, ifa=test_ifa,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(debug['device']['id'], equal_to(test_ifa))
        assert_that(debug['device']['id_source'], equal_to('IFA'))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify device info from debug in GDPR status in case of Legitimate Interest is false')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_report_ad_device_gdpr_legitimate_interest_false_1(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id(digital=36)
        test_app_id = gen_test_app_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=test_ifa,
                                               app_id=test_app_id)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if ip == non_eu_country_ip or consent_status is None:
            assert_that(debug['device']['id'], equal_to(test_ifa))
            assert_that(debug['device']['id_source'], equal_to('IFA'))
        else:
            assert_that(debug['device']['id'], not equal_to(test_ifa))
            assert_that(debug['device']['id_source'], equal_to('GDPR'))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify device info from debug in GDPR status in case of pre v6 flag is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_report_ad_device_gdpr_pre_v6_true_1(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status, ifa=test_ifa,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=ip, sdk_version='Vungle/5.9.9'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if ip == eu_country_ip:
                if consent_status == 'opted_in':
                    assert_that(debug['device']['id_source'], equal_to('IFA'))
                    assert_that(debug['device']['id'], equal_to(test_ifa))
                else:
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to(test_ifa))
            elif consent_status == 'opted_out':
                assert_that(debug['device']['id_source'], equal_to('GDPR'))
                assert_that(debug['device']['id'], not equal_to(test_ifa))
            else:
                assert_that(debug['device']['id_source'], equal_to('IFA'))
                assert_that(debug['device']['id'], equal_to(test_ifa))
        else:
            if ip == eu_country_ip:
                assert_that(debug['device']['id_source'], equal_to('GDPR'))
                assert_that(debug['device']['id'], not equal_to(test_ifa))
            else:
                assert_that(debug['device']['id_source'], equal_to('IFA'))
                assert_that(debug['device']['id'], equal_to(test_ifa))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify device info from debug in GDPR status in case of pre v6 flag is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_report_ad_device_gdpr_pre_v6_false_1(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.report_ad_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=test_ifa,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=ip, sdk_version='Vungle/5.9.9'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_that(debug['device']['id_source'], equal_to('GDPR'))
                assert_that(debug['device']['id'], not equal_to(test_ifa))
            else:
                assert_that(debug['device']['id_source'], equal_to('IFA'))
                assert_that(debug['device']['id'], equal_to(test_ifa))
        else:
            assert_that(debug['device']['id_source'], equal_to('IFA'))
            assert_that(debug['device']['id'], equal_to(test_ifa))

    @allure.feature('user privacy')
    @allure.tag('normal', 'kiloo')
    @allure.story('GDPR kiloo')
    @allure.description('Test for Kiloo consent status override')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['58fa97228fac7a64660001d3'])
    def test_report_ad_kiloo_consent_status_for_jaeger_1(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.report_ad_v5_ios(pub_app_id, 'DEFAULT-KILOO', gdpr='unknown', ifa=test_ifa,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=eu_country_ip))

        response_payload = r.json()
        device_info = response_payload['ext']['debug']['device']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(device_info['id'], not equal_to(test_ifa))
        assert_that(device_info['id_source'], equal_to('GDPR'))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify the status of GDPR external consents opted out, and legitimate interest is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_scrat_gdpr_external_consents_opted_out_legitimate_interest_true_1(self, pub_app_id, consent_status, ip):
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                               ifa=gdpr_external_consents_opted_out_device_id,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            assert_that(debug['device']['id_source'], equal_to('GDPR'))
            assert_that(debug['device']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
        else:
            if ip == eu_country_ip:
                assert_that(debug['device']['id_source'], equal_to('GDPR'))
                assert_that(debug['device']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
            else:
                assert_that(debug['device']['id_source'], equal_to('IFA'))
                assert_that(debug['device']['id'], equal_to(gdpr_external_consents_opted_out_device_id))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify the status of GDPR external consents opted in, and legitimate interest is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_scrat_gdpr_external_consents_opted_in_legitimate_interest_true_1(self, pub_app_id, consent_status, ip):
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, gdpr=consent_status,
                                               ifa=gdpr_external_consents_opted_in_device_id,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_that(debug['device']['id_source'], equal_to('GDPR'))
                assert_that(debug['device']['id'], not equal_to(gdpr_external_consents_opted_in_device_id))
            else:
                assert_that(debug['device']['id_source'], equal_to('IFA'))
                assert_that(debug['device']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
        else:
            assert_that(debug['device']['id_source'], equal_to('IFA'))
            assert_that(debug['device']['id'], equal_to(gdpr_external_consents_opted_in_device_id))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify the status of GDPR external consents opted out, and legitimate interest is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_scrat_gdpr_external_consents_opted_out_legitimate_interest_false_1(self, pub_app_id, consent_status, ip):
        req = request_payload.report_ad_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status,
                                               ifa=gdpr_external_consents_opted_out_device_id,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            assert_that(debug['device']['id_source'], equal_to('GDPR'))
            assert_that(debug['device']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
        else:
            if ip == eu_country_ip:
                assert_that(debug['device']['id_source'], equal_to('GDPR'))
                assert_that(debug['device']['id'], not equal_to(gdpr_external_consents_opted_out_device_id))
            else:
                assert_that(debug['device']['id_source'], equal_to('IFA'))
                assert_that(debug['device']['id'], equal_to(gdpr_external_consents_opted_out_device_id))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1606 Respect GDPR consent signal from publishers')
    @allure.description('Verify the status of GDPR external consents opted in, and legitimate interest is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_scrat_gdpr_external_consents_opted_in_legitimate_interest_false_1(self, pub_app_id, consent_status, ip):
        req = request_payload.report_ad_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status,
                                               ifa=gdpr_external_consents_opted_in_device_id,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if ip == eu_country_ip:
                if consent_status in ('opted_out', 'unknown', 'opted_out_by_timeout'):
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to(gdpr_external_consents_opted_in_device_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('IFA'))
                    assert_that(debug['device']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
            else:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to(gdpr_external_consents_opted_in_device_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('IFA'))
                    assert_that(debug['device']['id'], equal_to(gdpr_external_consents_opted_in_device_id))
        else:
            assert_that(debug['device']['id_source'], equal_to('IFA'))
            assert_that(debug['device']['id'], equal_to(gdpr_external_consents_opted_in_device_id))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('GDPR')
    @allure.description('Verify the status of GDPR for Android device')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_scrat_gdpr_android_1(self, pub_app_id, consent_status, ip):
        '''
        "legitimate_interest": true for this account
        '''
        test_id = gen_device_id()
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement, gdpr=consent_status,
                                                   android_id=test_id, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=ip, sdk_version='VungleDroid/6.4.0'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to(test_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('ISU'))
                    assert_that(debug['device']['id'], equal_to(test_id))
            else:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to(test_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('ISU'))
                    assert_that(debug['device']['id'], equal_to(test_id))
        else:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to(test_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('ISU'))
                    assert_that(debug['device']['id'], equal_to(test_id))
            else:
                assert_that(debug['device']['id_source'], equal_to('ISU'))
                assert_that(debug['device']['id'], equal_to(test_id))

    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('GDPR')
    @allure.description('Verify the status of GDPR for Windows device')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_scrat_gdpr_windows_1(self, pub_app_id, consent_status, ip):
        '''
        "legitimate_interest": true for this account
        '''
        test_id = gen_device_id()
        req = request_payload.report_ad_v5_windows(pub_app_id, windows_common_test_placement, gdpr=consent_status,
                                                   ifa=test_id, ashwid=test_id, app_id=gen_test_app_id('windows'))
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(
            debug='scrat', src_ip=ip, sdk_version='VungleWindows/6.4.0 (Windows 10; native)'
        ))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('IFA'))
                    assert_that(debug['device']['id'], equal_to_ignoring_case(test_id))
            else:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('IFA'))
                    assert_that(debug['device']['id'], equal_to_ignoring_case(test_id))
        else:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('IFA'))
                    assert_that(debug['device']['id'], equal_to_ignoring_case(test_id))
            else:
                assert_that(debug['device']['id_source'], equal_to('IFA'))
                assert_that(debug['device']['id'], equal_to_ignoring_case(test_id))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify the the device src on ashwid for Windows device')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_scrat_gdpr_windows_ashwid_1(self, pub_app_id, consent_status, ip, device_id):
        '''
        "legitimate_interest": true for this account
        '''
        test_id = gen_device_id()
        req = request_payload.report_ad_v5_windows(pub_app_id, windows_common_test_placement, gdpr=consent_status,
                                                   ifa=device_id, ashwid=test_id, app_id=gen_test_app_id('windows'))
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(
            debug='scrat', src_ip=ip, sdk_version='VungleWindows/6.4.0 (Windows 10; native)'
        ))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if new_gdpr_flag:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('ASHWID'))
                    assert_that(debug['device']['id'], equal_to_ignoring_case(test_id))
            else:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('ASHWID'))
                    assert_that(debug['device']['id'], equal_to_ignoring_case(test_id))
        else:
            if ip == eu_country_ip:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id_source'], equal_to('GDPR'))
                    assert_that(debug['device']['id'], not equal_to_ignoring_case(test_id))
                else:
                    assert_that(debug['device']['id_source'], equal_to('ASHWID'))
                    assert_that(debug['device']['id'], equal_to_ignoring_case(test_id))
            else:
                assert_that(debug['device']['id_source'], equal_to('ASHWID'))
                assert_that(debug['device']['id'], equal_to_ignoring_case(test_id))

    # ------------------------------------------ null device id ---------------------------------------------------

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug with non eu country ip and not match GDPR external consent, '
                        'null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_report_ad_device_gdpr_non_eu_country_null_device_id(self, pub_app_id, consent_status, sdk_v, device_id):
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement_t, gdpr=consent_status, ifa=device_id,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', sdk_version=sdk_v))

        if sdk_v != 'Vungle/6.3.9':
            response_payload = r.json()
            debug = response_payload['ext']['debug']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                if consent_status == 'opted_out':
                    assert_that(debug['device']['id'], not equal_to(''))
                    assert_that(debug['device']['id_source'], equal_to_ignoring_case('Vungle_FP'))
                else:
                    assert_that(debug['device']['id'], not equal_to(''))
                    assert_that(debug['device']['id_source'], equal_to_ignoring_case('Vungle_FP'))
            else:
                assert_that(debug['device']['id'], not equal_to(''))
                assert_that(debug['device']['id_source'], equal_to_ignoring_case('Vungle_FP'))
        else:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(r.content, equal_to(b''))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug when GDPR off, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_report_ad_device_gdpr_opted_in_null_device_id(self, pub_app_id, sdk_v, device_id):
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement_t, gdpr='opted_in', ifa=device_id,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=eu_country_ip, sdk_version=sdk_v))

        if sdk_v != 'Vungle/6.3.9':
            response_payload = r.json()
            debug = response_payload['ext']['debug']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(debug['device']['id'], not equal_to(''))
            assert_that(debug['device']['id_source'], equal_to_ignoring_case('Vungle_FP'))
        else:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(r.content, equal_to(b''))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug in GDPR status, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_report_ad_device_gdpr_opted_out_null_device_id(self, pub_app_id, sdk_v, device_id):
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement_t, gdpr='opted_out', ifa=device_id,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=eu_country_ip, sdk_version=sdk_v))

        if sdk_v != 'Vungle/6.3.9':
            response_payload = r.json()
            debug = response_payload['ext']['debug']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(debug['device']['id'], not equal_to(''))
            assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
        else:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(r.content, equal_to(b''))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug not in GDPR status in case of Legitimate Interest is true,'
                        'null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_report_ad_device_gdpr_legitimate_interest_true_null_device_id(self, pub_app_id, consent_status, ip, sdk_v, 
                                                                           device_id):
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement_t, gdpr=consent_status,
                                               ifa=device_id, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=ip, sdk_version=sdk_v))

        if sdk_v != 'Vungle/6.3.9':
            response_payload = r.json()
            debug = response_payload['ext']['debug']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(debug['device']['id'], not equal_to(''))
            assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
        else:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(r.content, equal_to(b''))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug in GDPR status in case of Legitimate Interest is false,'
                        'null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_report_ad_device_gdpr_legitimate_interest_false_null_device_id(self, pub_app_id, consent_status, ip,
                                                                            sdk_v, device_id):
        req = request_payload.report_ad_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=device_id,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=ip, sdk_version=sdk_v))

        if sdk_v != 'Vungle/6.3.9':
            response_payload = r.json()
            debug = response_payload['ext']['debug']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if ip == non_eu_country_ip or consent_status is None:
                assert_that(debug['device']['id'], not equal_to(''))
                assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
            else:
                assert_that(debug['device']['id'], not equal_to(''))
                assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
        else:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(r.content, equal_to(b''))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug in GDPR status in case of pre v6 flag is true, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_t])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_report_ad_device_gdpr_pre_v6_true_null_device_id(self, pub_app_id, consent_status, ip, device_id):
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement_t, gdpr=consent_status, ifa=device_id)
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=ip, sdk_version='Vungle/5.9.9'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(r.content, equal_to(b''))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify device info from debug in GDPR status in case of pre v6 flag is false, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_report_ad_device_gdpr_pre_v6_false_null_device_id(self, pub_app_id, consent_status, ip, device_id):
        req = request_payload.report_ad_v5_ios(pub_app_id, 'DEFAULT-5045327', gdpr=consent_status, ifa=device_id)
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=ip, sdk_version='Vungle/5.9.9'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(r.content, equal_to(b''))

    @allure.feature('user privacy')
    @allure.tag('normal', 'kiloo')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Test for Kiloo consent status override, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['58fa97228fac7a64660001d3'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.0', 'Vungle/6.3.9'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_scrat_kiloo_consent_status_for_jaeger_null_device_id(self, pub_app_id, sdk_v, device_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.report_ad_v5_ios(pub_app_id, 'DEFAULT-KILOO', gdpr='unknown', ifa=device_id,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=eu_country_ip, sdk_version=sdk_v))

        if sdk_v != 'Vungle/6.3.9':
            response_payload = r.json()
            device_info = response_payload['ext']['debug']['device']

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(device_info['id'], not equal_to(test_ifa))
            assert_that(device_info['id_source'], equal_to('Vungle_FP'))
        else:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(r.content, equal_to(b''))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify the status of GDPR for Android device, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('sdk_v', ['VungleDroid/6.4.0', 'VungleDroid/6.3.9'])
    def test_scrat_gdpr_android_null_device_id(self, pub_app_id, consent_status, ip, sdk_v):
        '''
        "legitimate_interest": true for this account
        '''
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement, gdpr=consent_status,
                                                   android_id='', app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=ip, sdk_version=sdk_v))

        if sdk_v != 'VungleDroid/6.3.9':
            response_payload = r.json()
            debug = response_payload['ext']['debug']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                if ip == eu_country_ip:
                    if consent_status == 'opted_out':
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
                    else:
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
                else:
                    if consent_status == 'opted_out':
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
                    else:
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
            else:
                if ip == eu_country_ip:
                    if consent_status == 'opted_out':
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
                    else:
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
                else:
                    assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                    assert_that(debug['device']['id'], not equal_to(''))
        else:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(r.content, equal_to(b''))

    @allure.feature('user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify the status of GDPR for Windows device, null device id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('sdk_v', ['VungleWindows/6.4.0 (Windows 10; native)',
                                       'VungleWindows/6.3.9 (Windows 10; native)'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_scrat_gdpr_windows_null_device_id(self, pub_app_id, consent_status, ip, sdk_v, device_id):
        '''
        "legitimate_interest": true for this account
        '''
        req = request_payload.report_ad_v5_windows(pub_app_id, windows_common_test_placement, gdpr=consent_status,
                                                   ifa=device_id, ashwid='', app_id=gen_test_app_id('windows'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', src_ip=ip, sdk_version=sdk_v))

        if sdk_v != 'VungleWindows/6.3.9 (Windows 10; native)':
            response_payload = r.json()
            debug = response_payload['ext']['debug']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            if new_gdpr_flag:
                if ip == eu_country_ip:
                    if consent_status == 'opted_out':
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
                    else:
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
                else:
                    if consent_status == 'opted_out':
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
                    else:
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
            else:
                if ip == eu_country_ip:
                    if consent_status == 'opted_out':
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
                    else:
                        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                        assert_that(debug['device']['id'], not equal_to(''))
                else:
                    assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
                    assert_that(debug['device']['id'], not equal_to(''))
        else:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(r.content, equal_to(b''))

    # -------------------------below cases are for disable_ad_id_if_coppa=True------------------------------------------

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_for_android_01_true(self, pub_app_id, sdk_v, device_id):
        """

        App level setting:
        "isCoppaCompliant": false
        """
        ifa = device_id
        test_id = ''
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
                                                   android_id=test_id, ifa=ifa, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        if device_id == '':
            assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_for_android_02_true(self, pub_app_id, sdk_v, device_id):
        """
        Placement level setting:
        "is_coppa": true
        """

        ifa = device_id
        test_id = ''
        req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                   android_id=test_id, ifa=ifa, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_zero_out_gaid_for_android_05_true(self, pub_app_id, sdk_v):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        ifa = test_id = gen_device_id()
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement, ifa=ifa,
                                                   android_id=test_id, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['report_ad_message']['ifa'], equal_to(ifa))
        assert_that(debug['device']['id_source'], equal_to('IFA'))


    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_zero_out_gaid_for_android_05_true_app_set_id(self, pub_app_id, sdk_v):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        ifa = test_id = gen_device_id()
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement, ifa=ifa,
                                                   app_set_id=test_id, android_id='', app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['report_ad_message']['ifa'], equal_to(ifa))
        assert_that(debug['device']['id_source'], equal_to('IFA'))




    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_zero_out_gaid_for_android_06_true(self, pub_app_id, sdk_v):
        """
           Placement level setting:
           "is_coppa": true
        """
        ifa = test_id = gen_device_id()
        req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                   android_id=gen_device_id(), ifa=ifa, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))


    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_zero_out_gaid_for_android_06_true_app_set_id(self, pub_app_id, sdk_v):
        """
           Placement level setting:
           "is_coppa": true
        """
        ifa = test_id = gen_device_id()
        req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                   app_set_id=test_id, ifa=ifa, android_id='', app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))



    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_for_android_07_true(self, pub_app_id, sdk_v, device_id):
        """

       App level setting:
       "isCoppaCompliant": false
       """
        ifa = device_id
        test_id = ''
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement, coppa=False,
                                                   android_id=test_id, ifa=ifa, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        if device_id == '':
            assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_for_android_08_true(self, pub_app_id, sdk_v, device_id):
        """
        Placement level setting:
        "is_coppa": true
        """
        ifa = device_id
        test_id = ''
        req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT_REWARDED-3605411', android_id=test_id, ifa=ifa,
                                                   coppa=False, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        if device_id == '':
            assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_for_android_12_true(self, pub_app_id, sdk_v, device_id):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
                                                   android_id='', ifa=device_id, coppa=True,
                                                   app_id=gen_test_app_id('android')
                                                   )
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_for_android_12_1_true(self, pub_app_id, sdk_v, device_id):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                   android_id='', ifa=device_id, coppa=True,
                                                   app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    # --------------------below cases are for disable_ad_id_if_coppa=True and GDPR exists---------------------------

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3'
                        'and GDPR exists')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_01_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
                                                   android_id='', ifa=device_id, gdpr=consent_status,
                                                   app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        if device_id == '':
            assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_02_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                   android_id='', ifa=device_id, gdpr=consent_status,
                                                   app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
        ifa = test_id = gen_device_id()
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
                                                   android_id=test_id, ifa=ifa, gdpr=consent_status, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['id_source'], equal_to('GDPR'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
        ifa = test_id = gen_device_id()
        req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                   android_id=test_id, ifa=ifa, gdpr=consent_status,
                                                   app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_07_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """

       App level setting:
       "isCoppaCompliant": false
       """
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement, coppa=False,
                                                   android_id='', ifa=device_id, gdpr=consent_status,
                                                   app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        if device_id == '':
            assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_08_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                   android_id='', ifa=device_id, gdpr=consent_status,
                                                   app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_12_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
                                                   android_id='', ifa=device_id, coppa=True,
                                                   gdpr=consent_status, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_12_1_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                   android_id='', ifa=device_id, coppa=True,
                                                   gdpr=consent_status, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_request_with_app_set_id(self, pub_app_id, sdk_v, consent_status):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                                   android_id='', ifa='', app_set_id=gen_device_id(),
                                                   coppa=True,
                                                   gdpr=consent_status, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Scrat support app_set_id')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_request_with_app_set_id_01(self, pub_app_id, sdk_v, header_bidding):
        """
        Placement level setting:
        "is_coppa": false
        """
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
                                                   android_id='', ifa='', app_set_id=gen_device_id(),
                                                   coppa=False, header_bidding=header_bidding, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('AppSetID'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Scrat support app_set_id')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_request_with_app_set_id_02(self, pub_app_id, sdk_v, header_bidding):
        """
        Placement level setting:
        "is_coppa": false
        """
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
                                                   android_id='', ifa='', app_set_id=gen_device_id(),
                                                   coppa=True, header_bidding=header_bidding, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Scrat support app_set_id')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_request_with_app_set_id_03(self, pub_app_id, sdk_v, device_id, header_bidding):
        """
        Placement level setting:
        "is_coppa": false
        """
        req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
                                                   android_id='', ifa='', app_set_id=device_id,
                                                   coppa=False, header_bidding=header_bidding, app_id=gen_test_app_id('android'))
        r = post(get_report_ad_endpoint_qa('5'), json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_keys_not_exist(debug['report_ad_message'], 'ifa')
        assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))

    # -------------------------below cases are for disable_ad_id_if_coppa=False-----------------------------------------

    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
    #                                                android_id=test_id, ifa=ifa)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_not_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                                android_id=test_id, ifa=ifa)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_not_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # def test_zero_out_gaid_for_android_03_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
    #                                                android_id=test_id, ifa=ifa)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['report_ad_message']['ifa'], equal_to(ifa))
    #     assert_that(debug['device']['id_source'], equal_to('IFA'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # def test_zero_out_gaid_for_android_04_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                                android_id=gen_device_id(), ifa=ifa)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['report_ad_message']['ifa'], equal_to(ifa))
    #     assert_that(debug['device']['id_source'], equal_to('IFA'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement, coppa=False,
    #                                                android_id=test_id, ifa='')
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_not_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_08_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                                android_id='', ifa=device_id, coppa=False)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_not_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify non zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_09_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     ifa = test_device_id = gen_device_id()
    #     req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
    #                                                android_id=test_device_id, ifa=ifa, coppa=False)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['report_ad_message']['ifa'], ifa)
    #     assert_that(debug['device']['id_source'], equal_to('IFA'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_10_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     ifa = test_device_id = gen_device_id()
    #     req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                                android_id=test_device_id, ifa=ifa, coppa=False)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['report_ad_message']['ifa'], ifa)
    #     assert_that(debug['device']['id_source'], equal_to('IFA'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_11_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     ifa = test_device_id = gen_device_id()
    #     req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
    #                                                android_id=test_device_id, ifa=ifa, coppa=True)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['report_ad_message']['ifa'], ifa)
    #     assert_that(debug['device']['id_source'], equal_to('IFA'))

    # -------------------------below cases are for disable_ad_id_if_coppa=False and GDPR exists------------------------

    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
    #                                                android_id=test_id, ifa='', gdpr=consent_status)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_not_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                                android_id=test_id, ifa='', gdpr=consent_status)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_not_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
    #                                                android_id=test_id, ifa=ifa, gdpr=consent_status)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['id_source'], equal_to('GDPR'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                                android_id=test_id, ifa=ifa, gdpr=consent_status)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['id_source'], equal_to('GDPR'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement, coppa=False,
    #                                                android_id=test_id, ifa="", gdpr=consent_status)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_not_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa', gdpr=consent_status,
    #                                                android_id='', ifa=device_id, coppa=False)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_keys_not_exist(debug['report_ad_message'], 'ifa')
    #     assert_that(debug['device']['id_source'], equal_to('Vungle_FP'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement, gdpr=consent_status,
    #                                                android_id=test_id, ifa=ifa, coppa=False)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['id_source'], equal_to('GDPR'))
    #
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.report_ad_v5_android(pub_app_id, 'DEFAULT95027_coppa', gdpr=consent_status,
    #                                                android_id=test_id, ifa=ifa, coppa=False)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['id_source'], equal_to('GDPR'))
    #
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
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
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.report_ad_v5_android(pub_app_id, android_common_test_placement,
    #                                                android_id=test_id, ifa=ifa, coppa=True, gdpr=consent_status)
    #     r = post(get_report_ad_endpoint_qa('5'), json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['id_source'], equal_to('GDPR'))
