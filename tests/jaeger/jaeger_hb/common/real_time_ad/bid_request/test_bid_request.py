import allure

from utils.behaviors import request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('Real-time bid request')
class TestBidRequest(object):

    # @allure.feature('basic')
    # @allure.tag('test_mode', 'smoke', 'basic')
    # @allure.story('bid request test mode')
    # @allure.description('Test for enable test mode by device id')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', config['hb_partners'])
    # def test_real_time_enable_test_mode_by_device_id(self, pub_app_id, placement, sdk_v, partner):
    #
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             test_device_id=test_mode_device_id, sdk_v=sdk_v,
    #                                             no_pre_cache_token=True, explain=True, ip=ca_ip,
    #                                             rtb=test_mode_kraken_rtb_ids_1)
    #
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         if "err_msg" not in response_payload['ext']:
    #             bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
    #             assert_that(bid_request['test'], equal_to(1))
    #
    #         assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))

    @allure.feature('bcat list')
    @allure.tag('normal', 'R_1.151.0')
    @allure.story('PBJ-2315 Remove IAB14-1 Dating from Bcat')
    @allure.description('Verify that there is no IAB14-1 from bcat list')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_bcat_list(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ca_us_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that('IAB14-1' not in bid_request['bcat'])
                assert_that('IAB7-44' not in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal', 'v1.158.0')
    # @allure.story('PBJ-2618 Remove IAB11 for xRTB stackadapt in bid request')
    # @allure.description('Verify for not removing IAB11 for eDSP')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # @pytest.mark.parametrize('partner', config['hb_partners'])
    # def test_real_time_removing_edsp_2(self, pub_app_id, placement, sdk_v, partner):
    #
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             test_device_id=test_mode_device_id, sdk_v=sdk_v,
    #                                             no_pre_cache_token=True, explain=True, ip=ca_ip,
    #                                             rtb=ext_test_mode_kraken_rtb_ids_mraid)
    #
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         if "err_msg" not in response_payload['ext']:
    #             bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_test_mode_kraken_rtb_ids_mraid)
    #             assert_that('IAB11' in bid_request['bcat'])
    #             assert_that('IAB7-44' not in bid_request['bcat'])

    # @allure.feature('bcat list')
    # @allure.tag('normal', 'v1.158.0')
    # @allure.story('PBJ-2618 Remove IAB11 for xRTB stackadapt in bid request')
    # @allure.description('Verify the supported_extension_type will not work for iDSP')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # @pytest.mark.parametrize('partner', config['hb_partners'])
    # def test_real_time_removing_idsp_1(self, pub_app_id, placement, sdk_v, partner):
    #     '''
    #            Setup for the test iDSP rtb: "supported_extension_type": "NoIAB11"
    #     '''
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             test_device_id=test_mode_device_id, sdk_v=sdk_v,
    #                                             no_pre_cache_token=True, explain=True, ip=ca_ip,
    #                                             rtb=test_mode_kraken_rtb_ids)
    #
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         if "err_msg" not in response_payload['ext']:
    #             bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
    #             assert_keys_not_exist(bid_request, 'NoIAB11')
    #             assert_that('IAB11' in bid_request['bcat'])

    @allure.feature('block adv')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2685 Block advertising apps through domain (account&app)')
    @allure.description('Verify the domain on app black list can not be served by Jaeger')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_block_adv_domain_1(self, pub_app_id, placement, sdk_v, partner):
        """
           Account setting:
               adDomainBlacklist": ["domain3.com", "domain4.com"]
           APP setting:
              adDomainBlacklist": ["domain3.com", "domain2.com"]

        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ca_us_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['badv'],
                            equal_to(['charm00.com', 'com.mopub.video', 'com.murka.scatterslots', 'domain2.com',
                                      'domain3.com', 'domain4.com', 'glu.com', 'hhijb.com', 'osityh.com',
                                      'testabc.com']))

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.')
    @allure.description('Verify banner + video object from bid request for Interstitial&rewarded placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_playable_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_fullscreen_support_placements_edsp(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.cid@"realTimeCid_%s"' % gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_mraid,
                                                override_bid_response_any=override_bid_response_any)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_mraid)
                imp = bid_request['imp']
                assert_keys_exist(imp[0], 'banner')
                assert_that(imp[0]['banner']['api'][0], equal_to(5))
                assert_that(imp[0]['banner']['pos'], equal_to(7))
                assert_that(imp[0]['banner']['vcm'], equal_to(1))
                assert_keys_exist(imp[0], 'video')

    @allure.feature('xapi suport')
    @allure.tag('normal')
    @allure.story('PBJ-2809 Create HTTP authentication header for XAPI integration')
    @allure.description('Verify the auth token from the bid request header for XAPI eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_xapi_auth_header_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ca_us_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_xapi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request_header = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                          ext_non_test_mode_kraken_rtb_ids_vast_xapi,
                                                                          content='Header')
                assert_keys_exist(bid_request_header, 'Authorization')

    @allure.feature('xapi suuport')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-2809 Create HTTP authentication header for XAPI integration')
    @allure.description('Verify the auth token from the bid request header for XAPI eDSP with programmatic banner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_xapi_auth_header_2(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, banner=True,
                                                no_pre_cache_token=True, explain=True, ip=ca_us_ip,
                                                rtb=ext_test_mode_kraken_rtb_ids_banner_xapi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request_header = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                          ext_test_mode_kraken_rtb_ids_banner_xapi,
                                                                          content='Header')
                assert_keys_exist(bid_request_header, 'Authorization')

    @allure.feature('xapi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-2809 Create HTTP authentication header for XAPI integration')
    @allure.description('Verify there is no auth token from the bid request header for non-XAPI eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_xapi_auth_header_3(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, banner=True,
                                                no_pre_cache_token=True, explain=True, ip=ca_us_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request_header = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                          ext_non_test_mode_kraken_rtb_ids_vast,
                                                                          content='Header')
                assert_keys_not_exist(bid_request_header, 'Authorization')

    @allure.feature('real time')
    @allure.tag('basic', 'smoke')
    @allure.story('real time corner case')
    @allure.description('Verify jaeger will not serve in case of legacy placement for real time traffic')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ["realtime_INTER-MREC-005"])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_not_serve_for_legacy_placement(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload['ext'], 'err_msg')
            assert_that('NoServPlacementNotFound' in response_payload['ext']['err_msg'])

    @allure.feature('auction type experiment')
    @allure.tag('normal', 'v1.223.0')
    @allure.story('PBJ-4216 Experiment 1st Price Auction for China Traffic')
    @allure.description('Verify CN traffic will follow 1st action price rule if enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', ['VIDEO_REALTIME_TEST-3176951'])
    @pytest.mark.parametrize('ip', [cn_ip])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_1st_auction_price_exp_01(self, pub_app_id, placement, sdk_v, partner, ip):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ip,
                                                rtb=meister_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, meister_rtb_ids)
                assert_that(bid_request['at'], is_in([1, 2]))

    @allure.feature('auction type experiment')
    @allure.tag('normal', 'v1.223.0')
    @allure.story('PBJ-4216 Experiment 1st Price Auction for China Traffic')
    @allure.description('Verify settlement price is the higher price if CN traffic enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', ['VIDEO_REALTIME_TEST-3176951'])
    @pytest.mark.parametrize('ip', [cn_ip])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_1st_auction_price_exp_02(self, pub_app_id, placement, sdk_v, partner, ip):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ip,
                                                rtb='60a2773fb3bbef2c0884d8bb,60adc79dfb70f80016e36884')

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   '60a2773fb3bbef2c0884d8bb,60adc79dfb70f80016e36884')
                bid_info = response_payload['seatbid'][0]['bid'][0]
                # assert settlement price is more higher if at=1
                assert_that(bid_request['at'], is_in([1, 2]))
                bid_info = response_payload['seatbid'][0]['bid'][0]
                nurl = bid_info['nurl']

                r_url = get(
                    nurl.replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '5.6').replace(
                        hbp_ssl_host, hbp_host)
                    .replace(scrat_notification_host_ssl, scrat_notification_host))
                response_payload_url = r_url.json()
                assert_that(response_payload_url['msg'], equal_to('ok'))
                assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('bid floor')
    @allure.tag('normal')
    @allure.story('PBJ-4608 Jaeger - Do not send bid request to eDSP if bid floor larger than a threshold')
    @allure.description('Verify jaeger will not serve for edsp bidfloor>=5000')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_threshold_for_bid_floor_e(self, pub_app_id, placement, sdk_v, partner):
        """
           ir
           reserve_floor: 5000
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ir_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_RTA_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast,
                                                                   )
                assert_that(bid_request['imp'][0]['bidfloor'], equal_to(5000))
                assert_keys_exist(response_payload, 'err_msg')

    @allure.feature('No Serve')
    @allure.tag('normal')
    @allure.story('panic')
    @allure.description('Verify jaeger will not panic w/ no banner/video/native obj and  device id')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_panic_case(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=None, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast, video_flag=False,
                                                banner_flag=False, idfv=None)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload['ext'],  "err_msg")
            assert_that("NO_SERV_REQUEST_VALIDATION_ERROR" in response_payload["ext"]["err_msg"])


    @allure.feature('support extension type')
    @allure.tag('normal')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify bidrequest_id with suffix will not impact hbp bid response')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_supprot_extension_type_for_hbp_01(self, pub_app_id, placement, sdk_v, partner):
        """
          rtb_setting:
           "supported_extension_type": "default_hb"
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext1_non_kraken_test_mode_default_hb)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext1_non_kraken_test_mode_default_hb)

                source_ext = bid_request['source']['ext']
                assert_keys_exist(source_ext, 'header_bidding')
                assert_that(source_ext['header_bidding'], equal_to(1))


    @allure.feature('support extension type')
    @allure.tag('normal')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify bidrequest_id with suffix will not impact realtime hbp bid response')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_supprot_extension_type_for_hbp_dup_01(self, pub_app_id, placement, sdk_v, partner):
        """
        rtb_setting:
        "supported_extension_type": "default_dup"
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext2_non_kraken_test_mode_default_dup)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext2_non_kraken_test_mode_default_dup)
                bid_request_id = bid_request['id']
                assert_that("___" in bid_request_id)
                bid_request_id_suffix = int(bid_request_id.split('___')[1])
                assert_that(isinstance(bid_request_id_suffix, int))
                bid_info = response_payload['seatbid'][0]['bid'][0]
                assert_that('___' not in bid_info['id'])


    @allure.feature('support extension type')
    @allure.tag('normal')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify bidrequest_id with suffix will not impact hbp precache bid response')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_supprot_extension_type_for_hbp_dup_02(self, pub_app_id, placement, sdk_v, partner):
        """
        rtb_setting:
        "supported_extension_type": "default_dup"
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, ip=au_ip,
                                                rtb=ext2_non_kraken_test_mode_default_dup)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that('___' not in bid_info['id'])


    @allure.feature('bid floor')
    @allure.tag('normal')
    @allure.story('PBJ-4608 Jaeger - Do not send bid request to eDSP if bid floor larger than a threshold')
    @allure.description('Verify jaeger will serve for idsp bidfloor>=5000')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_threshold_for_bid_floor_i(self, pub_app_id, placement, sdk_v, partner):
        """
           ir
           reserve_floor: 5000
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ir_ip,
                                                rtb=meister_rtb_ids, config_extension=config_extension_RTA_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   meister_rtb_ids,
                                                                   )
                assert_that(bid_request['imp'][0]['bidfloor'], equal_to(5000))
                assert_keys_not_exist(response_payload, 'err_msg')