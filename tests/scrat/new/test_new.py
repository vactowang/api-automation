import pytest
import allure

from http import HTTPStatus

from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - new')
class TestNew(object):

    @allure.feature('install')
    @allure.tag('normal')
    @allure.story('PBJ-4919 Removed unused Kafka Message in Scrat')
    @allure.description('Verify that message will be added to kafka (as-installPostbacks-20220421) message')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('version', ['1', '3', '4', '5'])
    def test_install_post_back_message(self, pub_app_id, version):
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
        r = get(get_new_endpoint_qa(version), params, headers=platform_headers(debug='scrat', sdk_version=None))

        response_payload = r.json()
        ext_message = response_payload['ext']['debug']['message']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(ext_message['vungleType'], equal_to('directAttribution'))
        assert_that(response_payload['device_ip'], equal_to(jp_ip))
        assert_that(response_payload['device_name'], equal_to('Apple'))
        assert_that(response_payload['os_version'], equal_to('13'))
        assert_that(ext_message['device_ip'], equal_to(jp_ip))
        assert_that(ext_message['device_name'], equal_to('Apple'))
        assert_that(ext_message['os_version'], equal_to('13'))

    @allure.feature('install')
    @allure.tag('normal', 'v0.165.0')
    @allure.story('PBJ-5008 populate geo ip data for MMP install events')
    @allure.description('Verify the geo info is parsed from the device_ip of the request payload')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('version', ['1', '3', '4', '5'])
    def test_geo_info_install_post_back_message_1(self, pub_app_id, version):
        test_ifa = gen_device_id()
        params = {
            "app_id": common_test_app,
            "ifa": test_ifa,
            "match_type": 'fingerprint',
            "country_code": 'US',
            "aaid": test_app_id_ios.replace('\"', '"').split('"')[3],
            "conversion": '1',
            "event_id": test_campaign_ios.split('|')[3],
            "device_ip": ca_us_ip,
            "device_name": "Apple",
            "os_version": "13"
        }
        r = get(get_new_endpoint_qa(version), params,
                headers=platform_headers(debug='scrat', sdk_version=None, src_ip=au_ip))

        response_payload = r.json()
        ext_message = response_payload['ext']['debug']['message']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(ext_message['geoip_city'], equal_to('Fremont'))
        assert_that(ext_message['geoip_country_code'], equal_to('US'))
        assert_that(ext_message['geoip_region'], equal_to('CA'))

    @allure.feature('install')
    @allure.tag('normal', 'v0.165.0')
    @allure.story('PBJ-5008 populate geo ip data for MMP install events')
    @allure.description('Verify the geo info will not be parsed from the header of the request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('version', ['1', '3', '4', '5'])
    def test_geo_info_install_post_back_message_2(self, pub_app_id, version):
        test_ifa = gen_device_id()
        params = {
            "app_id": common_test_app,
            "ifa": test_ifa,
            "match_type": 'fingerprint',
            "country_code": 'US',
            "aaid": test_app_id_ios.replace('\"', '"').split('"')[3],
            "conversion": '1',
            "event_id": test_campaign_ios.split('|')[3],
            "device_name": "Apple",
            "os_version": "13"
        }
        r = get(get_new_endpoint_qa(version), params,
                headers=platform_headers(debug='scrat', sdk_version=None, src_ip=ca_us_ip))

        response_payload = r.json()
        ext_message = response_payload['ext']['debug']['message']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(ext_message['geoip_city'], equal_to(None))
        assert_that(ext_message['geoip_country_code'], equal_to(None))
        assert_that(ext_message['geoip_region'], equal_to(None))