import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - session end')
class TestSessionEndBasic(object):

    @allure.feature('session end')
    @allure.tag('basic', 'smoke')
    @allure.story('session end')
    @allure.description('Verify all the session end endpoints work fine')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('version', ['1', '3', '4'])
    def test_session_end_basic(self, pub_app_id, version):
        test_ifa = gen_device_id()
        req = request_payload.session_end(pub_app_id, ifa=test_ifa)
        r = post(get_session_end_endpoint_qa(version), json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))