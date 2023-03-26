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


@allure.epic('HBP Bid Price')
class TestHBPBidPrice(object):

    @allure.feature('hbp price')
    @allure.tag('normal', 'v1.226.0')
    @allure.story('PBJ-2470 HBP eDSP price should be 0.85 of original bid price'
                  'PBJ-3483 Mongo margin value out of range'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that the bid price of 2nd price auction for eDSP margin extender which the app is not '
                        'entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('partner', ['aequus'])
    def test_expose_eDSP_margin_extender_1(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.26
            bid_floor = 1
            2nd price auction, so the original bid price = bid_floor
        '''
        bid_price = 98
        extender = 0.26
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=cn_ip, is_hb=partner)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=cn_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req,
                             headers=hbp_headers(rtb_selector=rtb, src_ip=cn_ip, debug='jaeger'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            transactions = get_ext_debug_from_jaeger_explain(response_payload, 'recommender_info')
            if 'margin' in transactions['ds_ext']:
                extender = transactions['ds_ext']['margin']
            else:
                extender = transactions['ds_ext']['margin_extender']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal')
    @allure.story('PBJ-2470 HBP eDSP price should be 0.85 of original bid price'
                  'PBJ-3483 Mongo margin value out of range'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI')
    @allure.description('Verify that the bid price of 1st price auction for eDSP margin extender which the app is not '
                        'entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('partner', ['ironsource'])
    def test_expose_eDSP_margin_extender_2(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.29
            bid_floor = 2.5
            1st price auction, use the original bid price 98
        '''
        bid_price = 98
        extender = 0.29
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=us_ip, is_hb=partner)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=us_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req,
                             headers=hbp_headers(rtb_selector=rtb, src_ip=us_ip, debug='jaeger'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            transactions = get_ext_debug_from_jaeger_explain(response_payload, 'recommender_info')
            if 'margin' in transactions['ds_ext']:
                extender = transactions['ds_ext']['margin']
            else:
                extender = transactions['ds_ext']['margin_extender']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal')
    @allure.story('PBJ-2470 HBP eDSP price should be 0.85 of original bid price'
                  'PBJ-3483 Mongo margin value out of range'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI')
    @allure.description('Verify that the bid price of 1st price auction will match the binding rule for eDSP margin '
                        'extender when ccpa optedout'
                        ' which the app is not '
                        'entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('partner', ['max'])
    def test_expose_eDSP_margin_extender_3(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.27
            bid_floor = 2.5
            1st price auction, use the original bid price 98
        '''
        bid_price = 98
        extender = 0.27
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=us_ip, is_hb=partner)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=us_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req,
                             headers=hbp_headers(rtb_selector=rtb, src_ip=us_ip))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal')
    @allure.story('PBJ-2470 HBP eDSP price should be 0.85 of original bid price'
                  'PBJ-3483 Mongo margin value out of range'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI')
    @allure.description('Verify that the bid price of 1st price auction for eDSP margin extender which the app is not '
                        'entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_expose_eDSP_margin_extender_4(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.22
            bid_floor = 2.5
            1st price auction, use the original bid price 98
        '''
        bid_price = 98
        extender = 0.22
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=us_ip, banner=True)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=us_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req,
                             headers=hbp_headers(rtb_selector=rtb, src_ip=us_ip))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal')
    @allure.story('PBJ-2470 HBP eDSP price should be 0.85 of original bid price'
                  'PBJ-3483 Mongo margin value out of range'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI')
    @allure.description('Verify that the eDSP margin extender will not impact iDSP in 1st price auction which the app '
                        'is not entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('partner', ['max'])
    def test_expose_eDSP_margin_extender_5(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.27
            bid_floor = 1
            1st price auction, so the original bid price = bid_floor
        '''
        bid_price = 98
        extender = 0.27
        rtb = meister_rtb_ids
        jaeger_response = request_ads_ios_no_retry(pub_app_id=pub_app_id, placement_ref_id=placement,
                                                   test_ifa=gen_device_id(), ip=us_ip, rtb=rtb)
        if 'sleep' not in jaeger_response['ads'][0]['ad_markup']:
            ordinal_view_count = 7
            bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
            bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
            super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

            test_ifa = gen_device_id(36)
            req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token,
                                              ip=us_ip)
            r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req,
                                 headers=hbp_headers(rtb_selector=rtb, src_ip=us_ip))

            if r.status_code == HTTPStatus.OK:
                response_payload = r.json()
                bid_info = response_payload['seatbid'][0]['bid'][0]

                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
                assert_that(round(bid_info['price'], 2), is_not(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal', 'v1.226.0')
    @allure.story('PBJ-2470 HBP eDSP price should be 0.85 of original bid price'
                  'PBJ-3483 Mongo margin value out of range'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that the eDSP margin extender will not impact iDSP in 2nd price auction which the app '
                        'is not entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('partner', ['max'])
    def test_expose_eDSP_margin_extender_6(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.3
            bid_floor = 1
            2nd price auction, so the original bid price = bid_floor
        '''
        bid_price = 98
        extender = 0.3
        rtb = meister_rtb_ids
        jaeger_response = request_ads_ios_no_retry(pub_app_id=pub_app_id, placement_ref_id=placement,
                                                   test_ifa=gen_device_id(), ip=cn_ip, rtb=rtb)
        if 'sleep' not in jaeger_response['ads'][0]['ad_markup']:
            ordinal_view_count = 7
            bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
            bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
            super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

            test_ifa = gen_device_id(36)
            req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token,
                                              ip=cn_ip)
            r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req,
                                 headers=hbp_headers(rtb_selector=rtb, src_ip=cn_ip))

            if r.status_code == HTTPStatus.OK:
                response_payload = r.json()
                bid_info = response_payload['seatbid'][0]['bid'][0]

                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
                assert_that(round(bid_info['price'], 2), is_not(round(bid_price * (1 - extender), 2)))


    @allure.feature('hbp price')
    @allure.tag('normal', 'v1.226.0')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that bid price in 2nd price auction which the app is not mapping strategy rule')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    @pytest.mark.parametrize('partner', ['max'])
    def test_expose_eDSP_margin_extender_is_default_2nd(self, pub_app_id, placement, partner):
        """
            HBP_EDSP_MARGIN_EXTENDER = 0.31
             bid_floor = 2.5
             2nd price auction, use the original bid price 1
        """

        bid_price = 98
        extender = 0.31
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement,
                                          test_ifa=gen_device_id(),
                                          rtb=rtb, ip=cn_ip)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=cn_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req,
                             headers=hbp_headers(rtb_selector=rtb, src_ip=cn_ip, debug='jaeger'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            transactions = get_ext_debug_from_jaeger_explain(response_payload, 'recommender_info')
            if 'margin' in transactions['ds_ext']:
                extender = transactions['ds_ext']['margin']
            else:
                extender = transactions['ds_ext']['margin_extender']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI')
    @allure.description('Verify that bid price in 1st price auction which the app is not mapping strategy rule')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    @pytest.mark.parametrize('partner', ['max'])
    def test_expose_eDSP_margin_extender_is_default_1st(self, pub_app_id, placement, partner):
        """
            HBP_EDSP_MARGIN_EXTENDER = 0.31
             bid_floor = 2.5
             2nd price auction, use the original bid price 1
        """

        bid_price = 98
        extender = 0.31
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement,
                                          test_ifa=gen_device_id(),
                                          rtb=rtb)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req,
                             headers=hbp_headers(rtb_selector=rtb, debug='jaeger'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            transactions = get_ext_debug_from_jaeger_explain(response_payload, 'recommender_info')
            if 'margin' in transactions['ds_ext']:
                extender = transactions['ds_ext']['margin']
            else:
                extender = transactions['ds_ext']['margin_extender']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))


    @allure.feature('hbp price')
    @allure.tag('normal', 'v1.226.0')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger'
                  'PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-3672 Expose eDSP margin on App Bidding in the Admin UI'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that bid price in 2nd price auction which the app is not entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_fullscreen_inter_playable_placement])
    @pytest.mark.parametrize('partner', ['max'])
    def test_expose_eDSP_margin_extender_for_android(self, pub_app_id, placement, partner):
        """
            HBP_EDSP_MARGIN_EXTENDER = 0.25
             bid_floor = 2.5
             2nd price auction, use the original bid price 1
        """

        bid_price = 98
        extender = 0.25
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        jaeger_response = request_ads_android(pub_app_id=pub_app_id, placement_ref_id=placement,
                                              test_android_id=gen_device_id(),
                                              rtb=rtb, ip=cn_ip, is_hb=partner)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=cn_ip,
                                          platform='android')
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req,
                             headers=hbp_headers(rtb_selector=rtb, src_ip=cn_ip, debug='jaeger'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            transactions = get_ext_debug_from_jaeger_explain(response_payload, 'recommender_info')
            if 'margin' in transactions['ds_ext']:
                extender = transactions['ds_ext']['margin']
            else:
                extender = transactions['ds_ext']['margin_extender']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal', 'v1.226.0')
    @allure.story('PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that the bid price of 2nd price auction for eDSP margin extender which the app is '
                        'entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [edsp_exp_test_app])
    @pytest.mark.parametrize('placement', [edsp_exp_test_placement])
    @pytest.mark.parametrize('partner', ['charboost'])
    def test_edsp_margin_extender_7(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.28
            bid_floor = 1
            2nd price auction, so the original bid price = bid_floor
        '''
        bid_price = 98
        extender = 0.28
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=cn_ip)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=cn_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req, headers=hbp_headers(rtb_selector=rtb))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal')
    @allure.story('PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs')
    @allure.description('Verify that the bid price of 1st price auction for eDSP margin extender which the app is '
                        'entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [edsp_exp_test_app])
    @pytest.mark.parametrize('placement', [edsp_exp_test_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_extender_8(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.28
            bid_floor = 2.5
            1st price auction, use the original bid price 98
        '''
        bid_price = 98
        extender = 0.28
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=fr_ip)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=fr_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req, headers=hbp_headers(rtb_selector=rtb,
                                                                                              debug='jaeger'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            transactions = get_ext_debug_from_jaeger_explain(response_payload, 'recommender_info')
            if 'margin' in transactions['ds_ext']:
                extender = transactions['ds_ext']['margin']
            else:
                extender = transactions['ds_ext']['margin_extender']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('hbp price')
    @allure.tag('normal','v1.226.0')
    @allure.story('PBJ-3720 Run A/B testing on different eDSP margin on the provided list of appIDs'
                  'PBJ-4421 Run 1st price auction for all CN traffic')
    @allure.description('Verify that the eDSP margin extender will not impact iDSP in 2nd price auction which the app '
                        'is entered into experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [edsp_exp_test_app])
    @pytest.mark.parametrize('placement', [edsp_exp_test_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_extender_9(self, pub_app_id, placement, partner):
        '''
            HBP_EDSP_MARGIN_EXTENDER = 0.28
            bid_floor = 1
            2nd price auction, so the original bid price = bid_floor
        '''
        bid_price = 98
        extender = 0.28
        rtb = meister_rtb_ids
        jaeger_response = request_ads_ios_no_retry(pub_app_id=pub_app_id, placement_ref_id=placement,
                                                   test_ifa=gen_device_id(), ip=cn_ip, rtb=rtb)
        if 'sleep' not in jaeger_response['ads'][0]['ad_markup']:
            ordinal_view_count = 7
            bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
            bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
            super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

            test_ifa = gen_device_id(36)
            req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token,
                                              ip=cn_ip)
            r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req, headers=hbp_headers(rtb_selector=rtb))

            if r.status_code == HTTPStatus.OK:
                response_payload = r.json()
                bid_info = response_payload['seatbid'][0]['bid'][0]

                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
                assert_that(round(bid_info['price'], 2), is_not(round(bid_price * (1 - extender), 2)))



    @allure.feature('edsp margin')
    @allure.tag('normal')
    @allure.story('PBJ-4042 Support setting App bidding traffic margin for LO for banner / mrec ad format')
    @allure.description('Verify the margin for Liftoff is 0.15 for banner placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_liftoff_1(self, pub_app_id, placement, partner):
        bid_price = 98
        extender = 0.15
        rtb = ext_non_test_mode_kraken_rtb_ids_mraid_liftoff
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=au_ip, banner=True)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=au_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req, headers=hbp_headers(rtb_selector=rtb))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('edsp margin')
    @allure.tag('normal')
    @allure.story('PBJ-4042 Support setting App bidding traffic margin for LO for banner / mrec ad format')
    @allure.description('Verify the margin for Liftoff is 0.15 for mrec placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_mrec_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_liftoff_2(self, pub_app_id, placement, partner):
        bid_price = 98
        extender = 0.15
        rtb = ext_non_test_mode_kraken_rtb_ids_mraid_liftoff
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=au_ip)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=au_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req, headers=hbp_headers(rtb_selector=rtb,
                                                                                              debug='jaeger'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            transactions = get_ext_debug_from_jaeger_explain(response_payload, 'recommender_info')
            if 'margin' in transactions['ds_ext']:
                extender = transactions['ds_ext']['margin']
            else:
                extender = transactions['ds_ext']['margin_extender']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), equal_to(round(bid_price * (1 - extender), 2)))

    @allure.feature('edsp margin')
    @allure.tag('normal')
    @allure.story('PBJ-4042 Support setting App bidding traffic margin for LO for banner / mrec ad format')
    @allure.description('Verify the margin for Liftoff does not impact the other eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_liftoff_3(self, pub_app_id, placement, partner):
        bid_price = 98
        extender = 0.15
        rtb = ext_non_test_mode_kraken_rtb_ids_mraid
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=au_ip, banner=True)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=au_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req, headers=hbp_headers(rtb_selector=rtb))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), is_not(round(bid_price * (1 - extender), 2)))

    @allure.feature('edsp margin')
    @allure.tag('normal')
    @allure.story('PBJ-4042 Support setting App bidding traffic margin for LO for banner / mrec ad format')
    @allure.description('Verify the margin for Liftoff does not impact the other eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_mrec_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_liftoff_4(self, pub_app_id, placement, partner):
        bid_price = 98
        extender = 0.15
        rtb = ext_non_test_mode_kraken_rtb_ids_mraid
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=au_ip)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=au_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req, headers=hbp_headers(rtb_selector=rtb))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), is_not(round(bid_price * (1 - extender), 2)))

    @allure.feature('edsp margin')
    @allure.tag('normal')
    @allure.story('PBJ-4042 Support setting App bidding traffic margin for LO for banner / mrec ad format')
    @allure.description('Verify the margin for Liftoff does not impact the video type')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_edsp_margin_liftoff_5(self, pub_app_id, placement, partner):
        bid_price = 98
        extender = 0.15
        rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          rtb=rtb, ip=au_ip)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token, ip=au_ip)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req, headers=hbp_headers(rtb_selector=rtb))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            assert_that(round(bid_info['price'], 2), is_not(round(bid_price * (1 - extender), 2)))


    @allure.feature('bid price')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4054 Add hard limit for all recommendation prices')
    @allure.description('Verify the bid limit setting for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('partner', ['max'])
    def test_bid_price_limit_1(self, pub_app_id, placement, partner):
        '''
            HBP_PRICE_HARD_LIMIT: "127000"
            KRAKEN_OPENRTB_BID_PRICE: "128.0"
        '''
        override_bid_price = 'seatbid.0.bid.0.price@10000'
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, post_retry=False,
                           test_device_id=test_mode_device_id, is_test=0, rtb=test_mode_kraken_int4_rtb_ids, debug='jaeger',
                           override_bid_response_any=override_bid_price)
        assert_that(info['is_hbp_responded_200'], equal_to(True))

        hbp_response = info['hbp_response']
        price = hbp_response['seatbid'][0]['bid'][0]['price']
        assert_that(price, equal_to(50.001))

    @allure.feature('bid price')
    @allure.tag('normal')
    @allure.story('PBJ-4054 Add hard limit for all recommendation prices')
    @allure.description('Verify the bid limit setting for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('partner', ['max'])
    def test_bid_price_limit_2(self, pub_app_id, placement, partner):
        '''
            JAEGER_DATASCI_PRICE_HARD_LIMIT: "127000"
            KRAKEN_OPENRTB_BID_PRICE: "128.0"
        '''
        override_bid_price = 'seatbid.0.bid.0.price@20000'
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, post_retry=False,
                           test_device_id=gen_device_id(), is_test=0, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                           debug='jaeger', ads_debug='jaeger',
                           override_bid_response_any=override_bid_price)
        assert_that(info['is_hbp_responded_200'], equal_to(True))

        hbp_response = info['hbp_response']
        price = hbp_response['seatbid'][0]['bid'][0]['price']
        assert_that(price, equal_to(127))

