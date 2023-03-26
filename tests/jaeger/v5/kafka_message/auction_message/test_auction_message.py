import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain, request_hbp_with_real_time_token
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
@allure.feature('message')
@allure.feature('ex-jaeger-auction')
# JAEGER_AUCTION_LOG_PERCENTAGE config can control the write percentage
class TestAuctionMessage(object):

    @allure.feature('Auction Message')
    @allure.tag('normal')
    @allure.story('PBJ-5106 [Jaeger]Optimize topic ex-jaeger-auction with BidRequest.ext.')
    @allure.description('Verify bidrequest.ext will add to ex-jaeger-auction topic')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_networkID, None])
    def test_auction_message_01(self, pub_app_id, placement, rtb_ids):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=rtb_ids,
                                          debug='jaeger'))

        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # assert that 'bid_request_ext' added to auction message.

    @allure.feature('Auction Message')
    @allure.tag('normal')
    @allure.story('PBJ-5106 [Jaeger]Optimize topic ex-jaeger-auction with BidRequest.ext.')
    @allure.description('Verify bidrequest.ext will add to ex-jaeger-auction topic')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['max'])
    def test_auction_message_realtime_02(self, pub_app_id, placement, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=test_default_real_time_sdk_version,
                                                no_pre_cache_token=True, ip=fr_ip,
                                                explain=True, coppa=True, rtb=ext1_non_test_mode_kraken_networkID,
                                                )
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # assert that 'bid_request_ext' added to auction message.


