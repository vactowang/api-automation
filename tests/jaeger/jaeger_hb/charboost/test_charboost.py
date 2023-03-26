import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import generate_real_time_token, request_hbp
from utils.common import *
from utils.assertions import *
from settings import *



@allure.epic('HBP charboost')
class TestCharboost(object):


    @allure.feature('bid request')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3127 Real-time Ad Test - Req 1 - Test for mapping the data to the HB bid request field for admob')
    @allure.description('Verify the mapping data to the hb bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_bid_request_mapping_for_real_time(self, pub_app_id, placement):
        test_ifa = gen_device_id(36)
        endpoint = get_hbp_partner_endpoint('charboost')
        data = generate_real_time_token(11, pub_app_id, placement, test_ifa)
        req = request_payload.hbp_partner('charboost', pub_app_id, placement, ifa=test_ifa,
                                          bid_token=data['super_token_v3'])
        r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        assert_response_status_code_in(r.status_code, HTTPStatus.NO_CONTENT, HTTPStatus.OK)
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'nurl')

