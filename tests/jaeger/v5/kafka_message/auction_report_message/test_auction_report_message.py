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
@allure.feature('ex-jaeger-auction-report-1')
class TestAuctionReportMessage(object):

    @allure.feature('Block Adomain')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-3867 Block Adomain on RTB level'
                  'PBJ-4007 Jaeger should send RTB account \'s adomain backlist through badv field of bid request.')
    @allure.description('Verify block the adomain which set in account mongodb for ios platform, PBJ 4014')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_adomain_blocking_edsp_ios_01(self, pub_app_id, placement):
        """
        account setting:

        adDomainBlacklist:{"glu.com", "testabc.com"}
        """
        override_bid_adomain = 'glu.com,testabc.com'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_block_adomain,
                                          override_bid_adomain=override_bid_adomain, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              ext_non_test_mode_kraken_rtb_block_adomain)
        badv = bid_request['badv']
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(ad_markup, 'sleep')
        assert_keys_exist(badv, override_bid_adomain.split(',')[0])
        assert_keys_exist(badv, override_bid_adomain.split(',')[1])
        # check 'transaction message' ex-jaeger-auction-report-1
        #  resp_no_bid_reason: 10011
        #  resp_bid_status: blocked for addomain blocking
        # check PBJ-4062, the ‘resp_adm_type' and 'req_ad_type' fields are added in this topic.




    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4013 Block CRID on RTB Account level, PBJ 4014')
    @allure.description('Verify block the CRID which set in rtb account mongodb for ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_edsp_ios_02(self, pub_app_id, placement):
        """
       account setting:

       adCrIDBlacklist:['574351a9740cf4426b30d030', '574351a9740cf4426b30d034']
        """
        override_crid = '574351a9740cf4426b30d034'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_block_crid,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], 'impression auctioned but unsold')
        # check 'transaction message' ex-jaeger-auction-report-1
        #  resp_no_bid_reason: 10012
        #  resp_bid_status: blocked for crid blocking

    @allure.feature('fullscreen playable')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-4104 MRAID Playable Reporting')
    @allure.description('Verify the field "mraid_palyable" is added for playable placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_01])
    def test_report_field_01(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        imp = bid_request['imp']
        assert_keys_exist(imp[0], 'banner')
        assert_that(imp[0]['banner']['api'][0], equal_to(5))
        assert_that(imp[0]['banner']['pos'], equal_to(7))
        assert_that(imp[0]['banner']['vcm'], equal_to(1))
        assert_keys_exist(imp[0], 'video')
        # check 'transaction message' ex-jaeger-auction-report-1
        #   "resp_adm_type":"mraid_playable",

    @allure.feature('fullscreen playable')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-4104 MRAID Playable Reporting')
    @allure.description('Verify the field "mraid_palyable" is added for playable placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_01])
    def test_report_field_02(self, pub_app_id, placement):
        # no attr=13 response
        Override_Bid_Ext = {
            "crtype": "MRAID 2.0",
        }
        if env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                                header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                              rtb_selector=rtb, override_bid_ext=json.dumps(Override_Bid_Ext)))
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            seatbid = bid_response[rtb]['seatbid']
            adm = seatbid[0]['bid'][0]['adm']
            assert_keys_not_exist(ad_markup, 'sleep')
            templateURL = ad_markup['templateURL']
            assert 'programmaticFullscreen-v4.zip' in templateURL
        # check 'transaction message' ex-jaeger-auction-report-1
        #   "resp_adm_type":"mraid_regular",


    @allure.feature('auction report')
    @allure.tag('normal')
    @allure.story('PBJ-4817 Jaeger - Add is realtime to auction report')
    @allure.description('Verify \'is_realtime=true\' in auction report')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_auction_request_01(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                config_extension="")
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that req_is_realtime=true"

    @allure.feature('auction report')
    @allure.tag('normal')
    @allure.story('PBJ-4817 Jaeger - Add is realtime to auction report')
    @allure.description('Verify \'is_realtime=false\' in auction report')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_auction_request_02(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                config_extension="")
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that req_is_realtime=false"

    @allure.feature('auction report')
    @allure.tag('normal')
    @allure.story('PBJ-4817 Jaeger - Add is realtime to auction report')
    @allure.description('Verify the field "req_is_realtime=false" for waterfall request')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_auction_report_waterfall_flag(self, pub_app_id, placement):

        if env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                                header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                              rtb_selector=rtb))
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            # Verify that req_is_realtime=false"

    @allure.feature('auction report')
    @allure.tag('normal')
    @allure.story('PBJ-4817 Jaeger - Add is realtime to auction report')
    @allure.description('Verify the field "req_is_realtime=false" for s2s request')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_auction_report_s2s(self, pub_app_id, placement):

        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement, ifv=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger',
                                          rtb_selector=ext2_non_kraken_test_mode_default_dup))
        # Verify that req_is_realtime=false"


