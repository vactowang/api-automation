import pytest
import allure
import math

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestPMP(object):

    @allure.feature('pmp')
    @allure.tag('normal', 'v1.169.0')
    @allure.story('PBJ-2971 RTB :: PMP Array Still Sending Auction Type 2')
    @allure.description('Verify PMP obj from the bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_pmp_1(self, pub_app_id, placement):
        '''
            "_id": {
                "$oid": "5ba3e9bbc57a320010d8f9f0"
            },
            "bid_floor": 16,
            "allowed_application_ids": [{
                "$oid": "59786bc2a43b3a08620026b1"
            }],
            "countries": ["US", "CN"]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_exist(bid_request['imp'][0], 'pmp')
        assert_that(isinstance(bid_request['imp'][0]['pmp']['private_auction'], int))
        assert_that(bid_request['imp'][0]['pmp']['deals'][0]['id'], equal_to(test_deal_id))
        assert_that(bid_request['imp'][0]['pmp']['deals'][0]['bidfloor'], equal_to(16))
        assert_that(bid_request['imp'][0]['pmp']['deals'][0]['bidfloorcur'], equal_to('USD'))
        assert_that(isinstance(bid_request['imp'][0]['pmp']['deals'][0]['at'], int))

    @allure.feature('pmp')
    @allure.tag('normal', 'v1.169.0')
    @allure.story('PBJ-2971 RTB :: PMP Array Still Sending Auction Type 2')
    @allure.description('Verify PMP at value for 2nd price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_pmp_2(self, pub_app_id, placement):
        '''
            "_id": {
                "$oid": "5ba3e9bbc57a320010d8f9f0"
            },
            "bid_floor": 16,
            "allowed_application_ids": [{
                "$oid": "59786bc2a43b3a08620026b1"
            }],
            "countries": ["US", "CN"]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=cn_ip,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['pmp']['deals'][0]['at'], equal_to(bid_request['at']))
        assert_that(bid_request['imp'][0]['pmp']['deals'][0]['at'], equal_to(1))

    @allure.feature('pmp')
    @allure.tag('normal', 'v1.169.0')
    @allure.story('PBJ-2971 RTB :: PMP Array Still Sending Auction Type 2')
    @allure.description('Verify PMP at value for 1st price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_pmp_3(self, pub_app_id, placement):
        '''
            "_id": {
                "$oid": "5ba3e9bbc57a320010d8f9f0"
            },
            "bid_floor": 16,
            "allowed_application_ids": [{
                "$oid": "59786bc2a43b3a08620026b1"
            }],
            "countries": ["US", "CN"]
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['pmp']['deals'][0]['at'], equal_to(bid_request['at']))
        assert_that(bid_request['imp'][0]['pmp']['deals'][0]['at'], equal_to(1))
