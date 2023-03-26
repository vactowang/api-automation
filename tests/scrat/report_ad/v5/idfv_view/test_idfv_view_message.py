from http import HTTPStatus

import pytest
import allure

from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema, request_payload


@allure.epic('scrat - report ad - v5')
class TestIDFVViewMessage(object):

    @allure.feature('idfv view message')
    @allure.tag('basic', 'smoke', 'R_0.110.0')
    @allure.story('PBJ-2292 Debug info in idfv view message in scrat')
    @allure.description('Verify the non-existing of idfv view message with no idfv from request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_view_message_not_exist_01(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv='')
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug, 'idfv_view_message')

    @allure.feature('idfv view message')
    @allure.tag('basic', 'smoke', 'R_0.110.0')
    @allure.story('PBJ-2292 Debug info in idfv view message in scrat')
    @allure.story('PBJ-3135 Stop producing data to as-view-idfv and as-deliveries-idfv')
    @allure.description('Verify the non-existing of idfv view message with no idfv from request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_view_message_not_exist_02(self, pub_app_id, placement):
        test_idfv = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, idfv=test_idfv)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug, 'idfv_view_message')

    @allure.feature('idfv view message')
    @allure.tag('basic', 'smoke', 'R_0.110.0')
    @allure.story('PBJ-2292 Debug info in idfv view message in scrat')
    @allure.story('PBJ-3135 Stop producing data to as-view-idfv and as-deliveries-idfv')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_view_message_no_device_info(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        test_idfv = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv=test_idfv)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug, 'idfv_view_message')

    @allure.feature('user privacy')
    @allure.tag('gdpr')
    @allure.story('idfv view message gdpr info from debug info')
    @allure.description('Verify idfv view message gdpr info from debug info')
    @allure.story('PBJ-3135 Stop producing data to as-view-idfv and as-deliveries-idfv')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_no_idfv_view_message(self, pub_app_id, placement, consent_status, ip):
        test_idfv = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, idfv=test_idfv, gdpr=consent_status)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', src_ip=ip))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        if new_gdpr_flag:
            if consent_status == 'opted_out':
                assert_keys_not_exist(debug, 'idfv_view_message')
            else:
                assert_keys_not_exist(debug, 'idfv_view_message')
        else:
            assert_keys_not_exist(debug, 'idfv_view_message')

    @allure.feature('idfv view message')
    @allure.tag('normal', 'v0.113.0')
    @allure.story('PBJ-2551 The change of IDFV Kafka topic writing logic')
    @allure.story('PBJ-3135 Stop producing data to as-view-idfv and as-deliveries-idfv')
    @allure.description('Verify the idfv view message when ifa and idfv are not empty, gdpr not protected')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('consent_status', [None, 'opted_in', 'unknown', 'opted_out_by_timeout'])
    def test_non_idfv_view_kafka_writing_logic_1(self, pub_app_id, placement, consent_status):
        test_ifa = gen_device_id()
        test_idfv = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv=test_idfv, gdpr=consent_status)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug, 'idfv_view_message')

    @allure.feature('idfv view message')
    @allure.tag('normal', 'v0.113.0', 'v0.154.0')
    @allure.story('PBJ-2551 The change of IDFV Kafka topic writing logic'
                  'PBJ-4452 Scrat - Treat 0000-0000 as empty IFA')
    @allure.description('Verify the idfv view message when gdpr protected')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_idfv_view_kafka_writing_logic_2(self, pub_app_id, placement, consent_status, device_id):
        test_ifa = device_id
        test_idfv = device_id
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv=test_idfv, gdpr=consent_status)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))


        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug, 'idfv_view_message')

    @allure.feature('idfv view message')
    @allure.tag('normal', 'v0.113.0')
    @allure.story('PBJ-2551 The change of IDFV Kafka topic writing logic')
    @allure.description('Verify the idfv view message when ifa is not empty, but idfv is empty')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_view_kafka_writing_logic_3(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        test_idfv = ''
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv=test_idfv)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug, 'idfv_view_message')

    @allure.feature('idfv view message')
    @allure.tag('normal', 'v0.113.0')
    @allure.story('PBJ-2551 The change of IDFV Kafka topic writing logic')
    @allure.description('Verify the idfv view message when idfv is not empty, but ifa is empty')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_idfv_view_kafka_writing_logic_4(self, pub_app_id, placement, device_id):
        test_ifa = device_id
        test_idfv = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv=test_idfv)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug, 'idfv_view_message')

    @allure.feature('idfv view message')
    @allure.tag('normal', 'v0.113.0')
    @allure.story('PBJ-2551 The change of IDFV Kafka topic writing logic')
    @allure.description('Verify the idfv view message when ifa and idfv are empty')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_idfv_view_kafka_writing_logic_5(self, pub_app_id, placement, device_id):
        test_ifa = device_id
        test_idfv = device_id
        req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=test_ifa, idfv=test_idfv)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug, 'idfv_view_message')