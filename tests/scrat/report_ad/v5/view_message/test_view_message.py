import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('scrat - report ad - v5')
class TestViewMessage(object):

    @allure.feature('view message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad view message from debug info')
    @allure.description('Verify view message basic from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_view_message_basic(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(isinstance(debug['view_message']['timestamp'], str))
        assert_that(isinstance(debug['view_message']['viewed_timestamp'], int))
        assert_that(debug['view_message']['os'], equal_to('iOS'))

    @allure.feature('view message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad view message from debug info')
    @allure.description('Verify is_external_dsp from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_view_message_is_external_dsp(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['view_message']['is_external_dsp'], equal_to(False))

    @allure.feature('view message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad view message from debug info')
    @allure.description('Verify view message campaign info from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_view_message_campaign_info(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['view_message']['campaign_id'], equal_to(test_campaign_ios.split('|')[0]))
        assert_that(debug['view_message']['creative_id'], equal_to(test_campaign_ios.split('|')[1]))

    @allure.feature('view message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad view message from debug info')
    @allure.description('Verify view message app info from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_view_message_app_info(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['view_message']['store_id'], equal_to(test_app_id_ios.replace('\"', '"').split('"')[3]))

    @allure.feature('user privacy')
    @allure.tag('gdpr')
    @allure.story('view message gdpr info from debug info')
    @allure.description('Verify view message gdpr info from debug info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_view_message_device_id_not_null(self, pub_app_id, consent_status, ip):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, gdpr=consent_status, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_that(debug['view_message']['device_id'], not equal_to(test_ifa))
                assert_that(debug['view_message']['device_id_source'], equal_to('GDPR'))
                assert_that(debug['view_message']['ifa'], equal_to(''))
                assert_that(debug['view_message']['isu'], not equal_to(test_ifa))
            else:
                assert_that(debug['view_message']['device_id'], equal_to(test_ifa))
                assert_that(debug['view_message']['device_id_source'], equal_to('IFA'))
                assert_that(debug['view_message']['ifa'], equal_to(test_ifa))
                assert_that(debug['view_message']['isu'], equal_to(test_ifa))
        else:
            if ip == eu_country_ip and consent_status == 'opted_out':
                assert_that(debug['view_message']['device_id'], not equal_to(test_ifa))
                assert_that(debug['view_message']['device_id_source'], equal_to('GDPR'))
                assert_that(debug['view_message']['ifa'], equal_to(''))
                assert_that(debug['view_message']['isu'], not equal_to(test_ifa))
            else:
                assert_that(debug['view_message']['device_id'], equal_to(test_ifa))
                assert_that(debug['view_message']['device_id_source'], equal_to('IFA'))
                assert_that(debug['view_message']['ifa'], equal_to(test_ifa))
                assert_that(debug['view_message']['isu'], equal_to(test_ifa))

    @allure.feature('user privacy')
    @allure.tag('gdpr')
    @allure.story('PBJ-1981 Add hashed device id to null device')
    @allure.description('Verify the device id info in view message from debug info when device id is null')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_view_message_device_id_null(self, pub_app_id, consent_status, ip, device_id):

        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=device_id, gdpr=consent_status,
                                               app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))


        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_that(debug['view_message']['device_id'], not equal_to(''))
                assert_that(debug['view_message']['device_id_source'], equal_to('Vungle_FP'))
                assert_that(debug['view_message']['ifa'], equal_to(''))
                assert_that(debug['view_message']['isu'], not equal_to(''))
            else:
                assert_that(debug['view_message']['device_id'], not equal_to(''))
                assert_that(debug['view_message']['device_id_source'], equal_to('Vungle_FP'))
                assert_that(debug['view_message']['ifa'], equal_to(''))
                assert_that(debug['view_message']['isu'], not equal_to(''))
        else:
            if ip == eu_country_ip and consent_status == 'opted_out':
                assert_that(debug['view_message']['device_id'], not equal_to(''))
                assert_that(debug['view_message']['device_id_source'], equal_to('Vungle_FP'))
                assert_that(debug['view_message']['ifa'], equal_to(''))
                assert_that(debug['view_message']['isu'], not equal_to(''))
            else:
                assert_that(debug['view_message']['device_id'], not equal_to(''))
                assert_that(debug['view_message']['device_id_source'], equal_to('Vungle_FP'))
                assert_that(debug['view_message']['ifa'], equal_to(''))
                assert_that(debug['view_message']['isu'], not equal_to(''))

    @allure.feature('idfv message')
    @allure.tag('normal', 'v0.115.0')
    @allure.story('PBJ-2635 IDFV field in as-views topic')
    @allure.description('Verify the idfv field from as view message')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-'])
    def test_view_message_idfv_1(self, pub_app_id, placement, device_id):
        test_ifa = device_id
        test_idfv = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv=test_idfv, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['view_message']['device_id_source'], equal_to('IDFV'))
        assert_that(debug['view_message']['idfv'], equal_to(test_idfv))

    @allure.feature('idfv message')
    @allure.tag('normal', 'v0.115.0')
    @allure.story('PBJ-2635 IDFV field in as-views topic')
    @allure.description('Verify the idfv field from as view message')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-'])
    def test_view_message_idfv_2(self, pub_app_id, placement, device_id):
        test_ifa = device_id
        test_idfv = ''
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv=test_idfv, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['view_message']['device_id_source'], equal_to('Vungle_FP'))
        assert_keys_not_exist(debug['view_message'], 'idfv')