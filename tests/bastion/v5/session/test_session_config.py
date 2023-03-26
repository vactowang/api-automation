import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestSessionConfig(object):

    @allure.feature('session data switch')
    @allure.tag('smoke')
    @allure.story('PBJ-1769 Session data switch in Bastion'
                  'PBJ-3375 Session Data: Platform Work - bastion'
                  'PBJ-4171 Set session data flag disabled by default for 6.11 GA SDK')
    @allure.description('Verify the session data switch in case of app level setting is true')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_session_data_switch_app_true(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        session = response_payload['session']
        # update based on PBJ-4171
        assert_that(session['enabled'], equal_to(False))
        assert_that(session['limit'] is not empty())


    @allure.feature('session data switch')
    @allure.tag('smoke')
    @allure.story('PBJ-1769 Session data switch in Bastion'
                  'PBJ-3375 Session Data: Platform Work - bastion')
    @allure.description('Verify the session data switch in case of app level setting is false')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_session_data_switch_app_false(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        session = response_payload['session']
        assert_that(session['enabled'], equal_to(False))
        assert_that(session['limit'] is not empty())

    @allure.feature('session data switch')
    @allure.tag('smoke')
    @allure.story('PBJ-1769 Session data switch in Bastion'
                  'PBJ-3375 Session Data: Platform Work - bastion')
    @allure.description('Verify the session data switch in case of app level setting is null')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    def test_session_data_switch_app_null(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        session = response_payload['session']
        assert_that(session['enabled'], equal_to(False))
        assert_that(session['limit'] is not empty())

    @allure.feature('session timout')
    @allure.tag('normal', 'R_v0.96.0')
    @allure.story('PBJ-2107 Add session_timeout in /config'
                  'PBJ-3375 Session Data: Platform Work - bastion')
    @allure.description('Verify the session timeout in 15 mins')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_session_timeout(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        session = response_payload['session']
        assert_that(session['timeout'], equal_to(900))
        assert_that(session['limit'] is not empty())

    @allure.feature('session timout')
    @allure.tag('normal', 'R_v0.96.0')
    @allure.story('PBJ-2107 Add session_timeout in /config'
                  'PBJ-3375 Session Data: Platform Work - bastion')
    @allure.description('Verify the session timeout in 15 mins')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_session_timeout(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        session = response_payload['session']
        assert_that(session['timeout'], equal_to(900))
        assert_that(session['limit'] is not empty())

    @allure.feature('session data switch')
    @allure.tag('smoke')
    @allure.story('PBJ-3375 Session Data: Platform Work - bastion')
    @allure.description('Verify limit field is added in sessions object for android platform')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_session_data_android(self, pub_app_id):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        session = response_payload['session']
        assert_that(session['limit'] is not empty())