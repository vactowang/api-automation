import pytest
import allure

from data.request_payload import s2s_partner
from utils.assertions import *
from utils.behaviors import request_s2s, get_bid_request_obj_from_jaeger_explain
from utils.common import *
from settings import *



@allure.epic('bid price')
class TestBidprice(object):
    @allure.feature('Liftoff rtb')
    @allure.tag('normal')
    @allure.story('PBJ-3975 Update bid floor for LiftOff DSP'
                  'PBJ-4036 Change price Rtb filter for Liftoff according to dynamic bid floor.')
    @allure.description('Verify bid floor is the default value for the header bidding traffic via the LO eDSP RTB, '
                        'mrec, US for ios')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('bid_price', [0.001, 0.01, 1])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_liftoff_bid_floor_1(self, pub_app_id, placement_id, bid_price, rtb):
        if env == 'ci':
            rtb = rtb.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtb.split(',')[1]
        override_price_any = bid_price
        test_ifa = gen_device_id()
        r = request_s2s(pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=rtb,  ip=au_ip, override_price_any=override_price_any)

        bid_request = get_bid_request_obj_from_jaeger_explain(r, rtb)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(1))
        bid_floor = (bid_request['imp'][0]['bidfloor'])
        if bid_price < bid_floor:
            # Verify jaeger will not serve in case of bid price is lower than bidfloor.
            assert_keys_exist(r, 'nbr')
        else:
            assert_keys_not_exist(r, 'nbr')




    @allure.feature('bid floor')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4608 Jaeger - Do not send bid request to eDSP if bid floor larger than a threshold')
    @allure.description('Verify jaeger will serve for idsp bidfloor>=5000')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919-2'])
    def test_threshold_for_bid_floor_e(self, pub_app_id, placement):
        """
               ir
               reserve_floor: 5000
        """
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        test_ifa = gen_device_id()
        r = request_s2s(pub_app_id=pub_app_id, placement_ref_id=placement, ifa=test_ifa,
                        rtb=rtb,  ip=ir_ip)

        bid_request = get_bid_request_obj_from_jaeger_explain(r, rtb)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(5000))
        assert_keys_exist(r, 'nbr')


