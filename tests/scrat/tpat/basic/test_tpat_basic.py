import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - tpat')
class TestTpatBasic(object):

    @allure.feature('sdk tpat')
    @allure.tag('basic', 'smoke', 'v0.114.0')
    @allure.story('sdk tpat')
    @allure.description('Verify the tpat endpoint work fine')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_tpat_basic(self, pub_app_id):
        req = request_payload.tpat(pub=pub_app_id)
        r = get(tpat_endpoint_qa, params=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))