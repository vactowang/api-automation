import pytest
import allure

from http import HTTPStatus

from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - new')
class TestNewBasic(object):

    @allure.feature('new')
    @allure.tag('basic', 'smoke')
    @allure.story('new')
    @allure.description('Verify all the new endpoints work fine')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('version', ['1', '3', '4', '5'])
    def test_new_basic(self, pub_app_id, version):
        test_ifa = gen_device_id()
        params = {
            "app_id": common_test_app,
            "ifa": test_ifa,
            "match_type": 'fingerprint',
            "country_code": 'US',
            "aaid": test_app_id_ios.replace('\"', '"').split('"')[3],
            "conversion": '1',
            "event_id": test_campaign_ios.split('|')[3]
        }
        r = get(get_new_endpoint_qa(version), params, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(isinstance(response_payload['ts'], str))
        assert_that(response_payload['app_id'], equal_to(params['app_id']))
        assert_that(response_payload['event_id'], equal_to(params['event_id']))
        assert_that(response_payload['ifa'], equal_to(params['ifa']))
        assert_that(response_payload['aaid'], equal_to(params['aaid']))
        assert_that(response_payload['conversion'], equal_to(params['conversion']))
        assert_that(response_payload['match_type'], equal_to(params['match_type']))
        assert_that(response_payload['country_code'], equal_to(params['country_code']))

    @allure.feature('new')
    @allure.tag('basic', 'smoke')
    @allure.story('new')
    @allure.description('Verify that device_ip, device_name, os_version is added to kafka message')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('version', ['1', '3', '4', '5'])
    def test_new_message_device(self, pub_app_id, version):
        test_ifa = gen_device_id()
        params = {
            "app_id": common_test_app,
            "ifa": test_ifa,
            "match_type": 'fingerprint',
            "country_code": 'US',
            "aaid": test_app_id_ios.replace('\"', '"').split('"')[3],
            "conversion": '1',
            "event_id": test_campaign_ios.split('|')[3],
            "device_ip": jp_ip,
            "device_name": "Apple",
            "os_version": "13"
        }
        r = get(get_new_endpoint_qa(version), params, headers=platform_headers(debug='scrat',  sdk_version=None))

        response_payload = r.json()
        ext_message = response_payload['ext']['debug']['message']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(ext_message['vungleType'], equal_to('directAttribution'))
        assert_that(isinstance(response_payload['device_ip'], str))
        assert_that(isinstance(response_payload['device_name'], str))
        assert_that(isinstance(response_payload['os_version'], str))
        assert_that(isinstance(ext_message['device_ip'], str))
        assert_that(isinstance(ext_message['device_name'], str))
        assert_that(isinstance(ext_message['os_version'], str))