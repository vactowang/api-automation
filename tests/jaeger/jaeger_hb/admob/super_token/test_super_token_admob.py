import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema
import base64


@allure.epic('HBP Admob')
class TestSuperTokenAdmob(object):

    @pytest.fixture(scope="class", autouse=True)
    def get_jaeger_response_bid_token_admob(self):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id(), rtb=meister_rtb_ids)
        global bid_token
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens = bid_token
        global super_token
        super_token = "1:" + base64.b64encode(bid_tokens.encode('ascii')).decode('ascii')

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify that HBP can response normally with valid super token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_with_valid_super_token_admob(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))
        response_payload = r.json()
        bid_info = response_payload['seatbid'][0]['bid'][0]
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.hbp_admob)
        assert_that(bid_info['burl'].count('https://'), equal_to(1))

    @allure.feature('admob support')
    @allure.tag('smoke')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify that HBP response 204 with super token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_with_invalid_super_token_admob(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token='1:123456')
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify that HBP response 204 with non-matched super token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_with_non_matched_super_token_admob(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa,
                                        bid_token=default_non_match_super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify that HBP response with invalid placement and non-matched super token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_with_invalid_placement_non_matched_super_token_admob(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, 'ABCDEFG', ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)