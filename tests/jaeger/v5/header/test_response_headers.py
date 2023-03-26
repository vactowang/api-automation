import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_hbp_with_real_time_token, decode_real_time_adunit
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema
from datetime import datetime


@allure.epic('jaeger v5')
class TestResponseHeaders(object):

    @allure.feature('gzip support')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3468 Add regression test case to check the existence of gzip header when gzip is enabled')
    @allure.description('Verify the response header content encoding for gzip enabled')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_gzip_response_header_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post_gzip(ads_v5_endpoint_qa, data=gzip_encode(req),
                      headers=platform_headers(rtb_selector=meister_rtb_ids, accept_encoding='gzip',
                                               content_encoding='gzip'))
        assert_response_status_code(r[0].status_code, HTTPStatus.OK)
        assert_valid_schema(r[0].json(), response_schema.ads_v5)

    @allure.feature('gzip support')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3468 Add regression test case to check the existence of gzip header when gzip is enabled')
    @allure.description('Verify the response header content encoding for gzip disabled')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_gzip_response_header_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)