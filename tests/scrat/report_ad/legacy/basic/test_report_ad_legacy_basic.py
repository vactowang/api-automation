import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - report ad - legacy')
class TestReportAdLegacyBasic(object):

    @allure.feature('report ad legacy')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad legacy')
    @allure.description('Verify the report ad legacy endpoints work fine')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('version', ['1', '3', '4'])
    def test_report_ad_legacy_basic(self, pub_app_id, version):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_legacy_android(pub_app_id, ifa=test_ifa)
        r = post(get_report_ad_endpoint_qa(version), json=req,
                 headers=platform_headers(sdk_version='VungleDroid/5.9.9'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))