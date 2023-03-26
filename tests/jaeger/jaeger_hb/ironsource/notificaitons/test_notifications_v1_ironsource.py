import pytest
import allure
import base64

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('HBP Ironsource')
class TestNotificationsV1Ironsource(object):

    @pytest.fixture(scope="class", autouse=True)
    def get_jaeger_response_bid_token(self):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        global bid_token
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token
        global super_token
        super_token = "1:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        global event_id
        event_id = jaeger_response['ads'][0]['ad_markup']['id']

    @allure.feature('ironsource support')
    @allure.tag('smoke')
    @allure.story('PBJ-2013 New endpoint for Ironsource')
    @allure.description('Verify that the default ordinal view count in nurl for ironsource')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_default_ordinal_view_ount_in_nurl_ironsource(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.hbp_ironsource(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_ironsource_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_ironsource)
            assert_that(bid_info['nurl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['nurl'])
            assert_that(ext['ordinal'], equal_to(-1))

    @allure.feature('ironsource support')
    @allure.tag('smoke')
    @allure.story('PBJ-2013 New endpoint for Ironsource')
    @allure.description('Verify that the default ordinal view count in lurl for ironsource')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_default_ordinal_view_ount_in_lurl_ironsource(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.hbp_ironsource(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_ironsource_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_ironsource)
            assert_that(bid_info['lurl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['lurl'])
            assert_that(ext['ordinal'], equal_to(-1))

