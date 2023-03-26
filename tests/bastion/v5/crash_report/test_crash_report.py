import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestCrashReport(object):

    @allure.feature('crash report')
    @allure.tag('normal')
    @allure.story('PBJ-1976 Crash report configure in config endpoint update')
    @allure.description('Verify the collect filter endpoint for crash report')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_collect_filter_endpoint_update(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['crash_report']['collect_filter'], equal_to('com.vungle'))