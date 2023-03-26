import pytest
import allure

from http import HTTPStatus

from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - session start')
class TestSessionStartBasic(object):

    @allure.feature('session start')
    @allure.tag('basic', 'smoke')
    @allure.story('session start')
    @allure.description('Verify all the session start endpoints work fine')
    @allure.severity('smoke')
    @pytest.mark.parametrize('version', ['1', '3', '4'])
    def test_session_start_basic(self, version):
        r = get(get_session_start_endpoint_qa(version), headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))