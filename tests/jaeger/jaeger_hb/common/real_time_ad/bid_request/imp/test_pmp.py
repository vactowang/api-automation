
import allure

from utils.behaviors import request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain
from utils.common import *
from utils.assertions import *
from settings import *



@allure.epic('Real-time imp pmp')
class TestPMP(object):
    @allure.feature('pmp')
    @allure.tag('normal', 'v1.169.0')
    @allure.story('PBJ-2971 RTB :: PMP Array Still Sending Auction Type 2')
    @allure.description('Verify PMP obj from the bid request')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_rewarded_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_pmp_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ca_us_ip,
                                                rtb=meister_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, meister_rtb_ids)
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
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_rewarded_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_pmp_2(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=cn_ip,
                                                rtb=meister_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, meister_rtb_ids)
                assert_that(bid_request['imp'][0]['pmp']['deals'][0]['at'], equal_to(bid_request['at']))
                assert_that(bid_request['imp'][0]['pmp']['deals'][0]['at'], equal_to(1))

    @allure.feature('pmp')
    @allure.tag('normal', 'v1.169.0')
    @allure.story('PBJ-2971 RTB :: PMP Array Still Sending Auction Type 2')
    @allure.description('Verify PMP at value for 1st price')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_rewarded_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_pmp_3(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ca_us_ip,
                                                rtb=meister_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, meister_rtb_ids)
                assert_that(bid_request['imp'][0]['pmp']['deals'][0]['at'], equal_to(bid_request['at']))
                assert_that(bid_request['imp'][0]['pmp']['deals'][0]['at'], equal_to(1))

