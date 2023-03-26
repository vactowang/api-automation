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


@allure.epic('HBP Appodeal')
class TestSuperTokenAppodeal(object):

    @pytest.fixture(scope="class", autouse=True)
    def get_jaeger_response_bid_token_appodeal(self):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        global bid_token
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens = bid_token
        global super_token
        super_token = "1:" + base64.b64encode(bid_tokens.encode('ascii')).decode('ascii')

    @allure.feature('appodeal support')
    @allure.tag('smoke')
    @allure.story('HBP Appodeal support')
    @allure.description('Verify that HBP can response normally with valid super token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_with_valid_super_token_appodeal(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner('appodeal', pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_appodeal_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema('appodeal'))
            assert_that(bid_info['nurl'].count('https://'), equal_to(1))
            assert_that(bid_info['lurl'].count('https://'), equal_to(1))

    @allure.feature('appodeal support')
    @allure.tag('smoke')
    @allure.story('HBP Appodeal support')
    @allure.description('Verify that HBP response 204 with super token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_with_invalid_super_token_appodeal(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner('appodeal', pub_app_id, common_test_placement, ifa=test_ifa, bid_token='1:123456')
        r = post_hbp_request(hbp_appodeal_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('appodeal support')
    @allure.tag('smoke')
    @allure.story('HBP Appodeal support')
    @allure.description('Verify that HBP response 204 with non-matched super token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_with_non_matched_super_token_appodeal(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner('appodeal', pub_app_id, common_test_placement, ifa=test_ifa,
                                           bid_token=default_non_match_super_token)
        r = post_hbp_request(hbp_appodeal_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('appodeal support')
    @allure.tag('smoke')
    @allure.story('HBP Appodeal support')
    @allure.description('Verify that HBP response with invalid placement and non-matched super token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_with_invalid_placement_non_matched_super_token_appodeal(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner('appodeal', pub_app_id, 'ABCDEFG', ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_appodeal_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)