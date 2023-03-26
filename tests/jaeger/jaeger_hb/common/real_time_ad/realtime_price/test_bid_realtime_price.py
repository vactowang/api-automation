import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp_with_real_time_token, \
    request_ads_ios_no_retry, request_ads_android, request_hbp, get_ext_debug_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema
import math


@allure.epic('HBP Bid realtime Price')
class TestHBPBidRealtimePrice(object):

    @allure.feature('hbp price')
    @allure.tag('normal', 'v1.226.0')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that the bid price of 2nd price auction for eDSP margin extender on real-time ad '
                        'which the app is not entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['DEFAULT02021-REALTIME'])
    @pytest.mark.parametrize('partner', ['ironsource'])
    def test_expose_eDSP_margin_extender_realtime_01(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.31
            bid_floor = 1
            2nd price auction, so the original bid price = bid_floor
        '''
        bid_price = 98
        extender = 0.26
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), no_pre_cache_token=False,
                                                sdk_v=test_default_real_time_sdk_version, ip=cn_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI')
    @allure.description('Verify that the bid price of 1st price auction for eDSP margin extender on real-time ad '
                        'which the app is not entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['DEFAULT02021-REALTIME'])
    @pytest.mark.parametrize('partner', ['ironsource'])
    def test_expose_eDSP_margin_extender_realtime_02(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.31
            bid_floor = 2.5
            1st price auction, use the original bid price 98
        '''
        bid_price = 98
        extender = 0.26

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), no_pre_cache_token=True,
                                                sdk_v=test_default_real_time_sdk_version, ip=us_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                explain=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            transactions = get_ext_debug_from_jaeger_explain(response_payload, 'recommender_info')
            if 'margin' in transactions['ds_ext']:
                extender = transactions['ds_ext']['margin']
            else:
                extender = transactions['ds_ext']['margin_extender']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal', 'v1.226.0')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that the eDSP margin extender will not impact iDSP in 2nd price auction on'
                        'real-time ad which the app is not entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['DEFAULT02021-REALTIME'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_extender_realtime_03(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.31
            bid_floor = 1
            2nd price auction, so the original bid price = bid_floor
        '''
        bid_price = 98
        extender = 0.31
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), no_pre_cache_token=True,
                                                sdk_v=test_default_real_time_sdk_version, ip=cn_ip,
                                                rtb=meister_rtb_ids)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(round(bid_info['price'], 2), is_not(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal')
    @allure.story('PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs')
    @allure.description('Verify that the 1st price real-time request will not enter into experiment which '
                        'the app is in the list')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [edsp_exp_test_app])
    @pytest.mark.parametrize('placement', ['DEFAULT020A2-REALTIME'])
    @pytest.mark.parametrize('partner', ['max','admob'])
    def test_edsp_margin_extender_realtime_04(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.31
            bid_floor = 2.5
            1st price auction, use the original bid price 98
        '''
        bid_price = 98
        extender = 0.31

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), no_pre_cache_token=True,
                                                sdk_v=test_default_real_time_sdk_version, ip=fr_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast, explain=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            transactions = get_ext_debug_from_jaeger_explain(response_payload, 'recommender_info')
            if 'margin' in transactions['ds_ext']:
                extender = transactions['ds_ext']['margin']
            else:
                extender = transactions['ds_ext']['margin_extender']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal', 'v1.226.0')
    @allure.story('PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that the eDSP margin extender will not impact iDSP in 2nd price auction on'
                        'real-time ad which the app is in the list')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [edsp_exp_test_app])
    @pytest.mark.parametrize('placement', ['DEFAULT020A2-REALTIME'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_extender_realtime_05(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.31
            bid_floor = 1
            2nd price auction, so the original bid price = bid_floor
        '''
        bid_price = 98
        extender = 0.31
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), no_pre_cache_token=True,
                                                sdk_v=test_default_real_time_sdk_version, ip=cn_ip,
                                                rtb=meister_rtb_ids)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(round(bid_info['price'], 2), is_not(round(bid_price * (1 - extender), 2)))

    @allure.feature('edsp margin')
    @allure.tag('normal')
    @allure.story('PBJ-4042 Support setting App bidding traffic margin for LO for banner / mrec ad format')
    @allure.description('Verify the margin for Liftoff is 0.15 for banner placement does not impact real-time')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_liftoff_realtime_01(self, pub_app_id, placement, partner):
        bid_price = 98
        extender = 0.15
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), no_pre_cache_token=True,
                                                sdk_v=test_default_real_time_sdk_version, ip=au_ip, banner=True,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_mraid_liftoff)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(round(bid_info['price'], 2), is_not(round(bid_price * (1 - extender), 2)))

    @allure.feature('edsp margin')
    @allure.tag('normal')
    @allure.story('PBJ-4042 Support setting App bidding traffic margin for LO for banner / mrec ad format')
    @allure.description('Verify the margin for Liftoff is 0.15 for banner placement does not impact real-time')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_mrec_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_liftoff_realtime_02(self, pub_app_id, placement, partner):
        bid_price = 98
        extender = 0.15
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), no_pre_cache_token=True,
                                                sdk_v=test_default_real_time_sdk_version, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_mraid_liftoff)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(round(bid_info['price'], 2), is_not(round(bid_price * (1 - extender), 2)))

    @allure.feature('edsp margin')
    @allure.tag('normal')
    @allure.story('PBJ-4042 Support setting App bidding traffic margin for LO for banner / mrec ad format')
    @allure.description('Verify the margin for Liftoff is 0.15 for pre-cache banner placement via real-time')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_banner_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_liftoff_realtime_03(self, pub_app_id, placement, partner):
        bid_price = 98
        extender = 0.15
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), no_pre_cache_token=False,
                                                sdk_v=test_default_real_time_sdk_version, ip=au_ip, banner=True,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_mraid_liftoff,
                                                explain=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            transactions = get_ext_debug_from_jaeger_explain(response_payload, 'recommender_info')
            if 'margin' in transactions['ds_ext']:
                extender = transactions['ds_ext']['margin']
            else:
                extender = transactions['ds_ext']['margin_extender']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('edsp margin')
    @allure.tag('normal')
    @allure.story('PBJ-4042 Support setting App bidding traffic margin for LO for banner / mrec ad format')
    @allure.description('Verify the margin for Liftoff is 0.15 for pre-cache mrec placement via real-time')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_mrec_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_liftoff_realtime_04(self, pub_app_id, placement, partner):
        bid_price = 98
        extender = 0.15
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), no_pre_cache_token=False,
                                                sdk_v=test_default_real_time_sdk_version, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_mraid_liftoff)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('bid price')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4054 Add hard limit for all recommendation prices')
    @allure.description('Verify the bid limit setting for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['max'])
    def test_realtime_bid_price_limit_1(self, pub_app_id, placement, partner):
        '''
            HBP_PRICE_HARD_LIMIT: "127000"
            KRAKEN_OPENRTB_BID_PRICE: "128.0"
        '''
        override_bid_price = 'seatbid.0.bid.0.price@10000'
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), no_pre_cache_token=True,
                                                sdk_v=test_default_real_time_sdk_version, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_mraid_liftoff,
                                                override_bid_response_any=override_bid_price, explain=True)

        hbp_response = info['hbp_response']
        price = hbp_response['seatbid'][0]['bid'][0]['price']
        assert_that(price, equal_to(127))
