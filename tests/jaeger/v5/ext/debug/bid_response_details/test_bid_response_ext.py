import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestBidResponseExt(object):

    @allure.feature('liftoff support')
    @allure.tag('normal', 'v1.181.0', 'test_mode')
    @allure.story('PBJ-3383 Ingest LiftOff bid response content to Experiment data for analysis')
    @allure.description('Verify the experiment info if bid response ext contains the testgroups obj via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_liftoff_exp_1(self, pub_app_id, placement):
        additional_bid_ext = {
            "testgroups": [
                {
                    "experiment": "lv-margin-1",
                    "group": "lv-margin-control-2"
                }
            ]
        }
        expected_bid_ext = test_default_bid_ext
        expected_bid_ext.update(additional_bid_ext)
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_ext=json.dumps(expected_bid_ext)))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_response_ext = response_payload['ext']['debug']['auction_result']['bid_response_details'][rtb]['seatbid'][0]['bid'][0]['ext']
        assert_that(bid_response_ext['testgroups'][0]['experiment'], equal_to('lv-margin-1'))
        assert_that(bid_response_ext['testgroups'][0]['group'], equal_to('lv-margin-control-2'))