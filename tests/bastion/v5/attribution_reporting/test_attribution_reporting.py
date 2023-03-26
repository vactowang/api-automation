import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestAttributionReporting(object):

    @allure.feature('IMEI')
    @allure.tag('normal', 'R_v0.89.0')
    @allure.story('PBJ-1558 Bastion do NOT Fill the Field should_transmit_imei')
    @allure.description('Verify there is no obj of attribution_reporting from config response for iOS')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/5.0.0;native', 'Vungle/6.5.3;native'])
    def test_no_attribution_reporting_ios(self, pub_app_id, sdk_ver):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_ver))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(response_payload, 'attribution_reporting')

    @allure.feature('IMEI')
    @allure.tag('normal', 'R_v0.89.0')
    @allure.story('PBJ-1558 Bastion do NOT Fill the Field should_transmit_imei')
    @allure.description('Verify there is no obj of attribution_reporting from config response for Android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5a55162ccbc18a63250138c6'])
    @pytest.mark.parametrize('sdk_ver', ['VungleDroid/5.0.0', 'VungleDroid/6.2.9'])
    def test_no_attribution_reporting_android(self, pub_app_id, sdk_ver):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_ver))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(response_payload, 'attribution_reporting')