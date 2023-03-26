import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain, request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain, get_ext_debug_from_jaeger_explain, request_hbp
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
@allure.feature('message')
@allure.feature('hb-transaction')
class TestHBTransactionMessage(object):

    @allure.tag('hb_transaction ')
    @allure.story('normal', 'v1.259.0')
    @allure.story('PBJ-5266 Add new fields from Accelerate bid response into Bflat feature extra_data')
    @allure.description('Verify `bid_shading_bflat_group` is added to hb transaction')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_Accelerate_01(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response = "seatbid.0.bid.0.ext.testgroups@[{\"experiment\": \"bid-shading-bflat\", \"group\": " \
                                "\"experiment\"}]"
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                override_bid_response_any=override_bid_response,
                                                explain=True, coppa=True, rtb=liftoff_rtbids_liftoff_dup)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            response_payload = info['hbp_response']
            debug = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
            assert_that(debug['exp_to_bucket'], equal_to("{\"bid-shading-bflat\":\"experiment\"}"))
            assert_that(debug['bid_shading_bflat_group'], equal_to("experiment"))
            # assert that "bid_shading_bflat_group":"experiment" pass to bflat request.

    @allure.tag('hb_transaction ')
    @allure.story('normal', 'v1.259.0')
    @allure.story('PBJ-5266 Add new fields from Accelerate bid response into Bflat feature extra_data')
    @allure.description('Verify pub_app_object_id is added to hb transaction')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_Accelerate_02(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response = "seatbid.0.bid.0.ext.testgroups@[{\"experiment\": \"bid-shading-bflat\", \"group\": " \
                                "\"experiment_emily_27\"}]"
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, ads_debug='jaeger',
                                                override_bid_response_any=override_bid_response,
                                                explain=True, coppa=True, rtb=liftoff_rtbids_liftoff_dup)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            response_payload = info['hbp_response']
            debug = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
            assert_that(debug['bid_shading_bflat_group'], equal_to("experiment_emily_27"))

    @allure.tag('hb_transaction ')
    @allure.story('normal', 'v1.259.0')
    @allure.story('PBJ-5266 Add new fields from Accelerate bid response into Bflat feature extra_data')
    @allure.description('Verify pub_app_object_id is added to hb transaction')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_Accelerate_03(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response = "seatbid.0.bid.0.ext.testgroups@[{\"experiment\": \"bid-shading-bflat\", \"group\": " \
                                "\"experiment\"}]"
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), sdk_v=sdk_v, ads_debug='jaeger',
                           override_bid_response_any=override_bid_response, rtb=liftoff_rtbids_liftoff_dup)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # assert that "bid_shading_bflat_group":"experiment" add to hb transaction.
            # assert that "bid_shading_bflat_group":"experiment" pass to bflat request.

    @allure.tag('hb_transaction ')
    @allure.story('normal', 'v1.259.0')
    @allure.story('PBJ-5266 Add new fields from Accelerate bid response into Bflat feature extra_data')
    @allure.description('Verify `bid_shading_bflat_group` does not added to hb transaction for other dsp')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_Accelerate_04(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response = "seatbid.0.bid.0.ext.testgroups@[{\"experiment\": \"bid-shading-bflat\", \"group\": " \
                                "\"experiment\"}]"
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                override_bid_response_any=override_bid_response,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            response_payload = info['hbp_response']
            debug = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
            assert_that(debug['exp_to_bucket'], equal_to("{\"bid-shading-bflat\":\"experiment\"}"))
            assert_keys_not_exist(debug, 'bid_shading_bflat_group')