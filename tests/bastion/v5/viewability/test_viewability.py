import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestViewAbilityBastion(object):

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for om enabled app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_om_enabled_status_bastion_app_enabled(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.7'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        viewability = response_payload['viewability']
        assert_that(viewability['om'], equal_to(True))

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for no om setting in app level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    def test_om_enabled_status_bastion_app_default_setting(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.7'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        viewability = response_payload['viewability']
        assert_that(viewability['om'], equal_to(True))

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for om disabled app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b2'])
    def test_om_enabled_status_bastion_app_disabled(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.7'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        viewability = response_payload['viewability']
        assert_that(viewability['om'], equal_to(False))

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for vungle api version < 5.7')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('apiv', ['5.6'])
    def test_om_enabled_status_bastion_vungle_api_version_ctl_1(self, pub_app_id, apiv):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(vungle_version=apiv))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        viewability = response_payload['viewability']
        assert_that(viewability['om'], equal_to(False))

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for vungle api version >= 5.7')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('apiv', ['5.7', '5.8'])
    def test_om_enabled_status_bastion_vungle_api_version_ctl_2(self, pub_app_id, apiv):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(vungle_version=apiv))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        viewability = response_payload['viewability']
        assert_that(viewability['om'], equal_to(True))