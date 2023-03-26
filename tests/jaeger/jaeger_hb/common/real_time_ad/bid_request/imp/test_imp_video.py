import allure

from utils.behaviors import  request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain
from utils.common import *
from utils.assertions import *
from settings import *




@allure.epic('Real-time imp video')
class TestImpVideo(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp video')
    @allure.description('Verify imp video obj from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_video_info(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that('video/mp4' in bid_request['imp'][0]['video']['mimes'])
                assert_that('minduration' in bid_request['imp'][0]['video'])
                assert_that('maxduration' in bid_request['imp'][0]['video'])
                assert_that('protocols' in bid_request['imp'][0]['video'])
                assert_that('w' in bid_request['imp'][0]['video'])
                assert_that('h' in bid_request['imp'][0]['video'])
                assert_that('linearity' in bid_request['imp'][0]['video'])
                assert_that('minbitrate' in bid_request['imp'][0]['video'])
                assert_that('maxbitrate' in bid_request['imp'][0]['video'])
                assert_that('boxingallowed' in bid_request['imp'][0]['video'])
                assert_that('playbackmethod' in bid_request['imp'][0]['video'])
                assert_that('delivery' in bid_request['imp'][0]['video'])
                assert_that('pos' in bid_request['imp'][0]['video'])

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp video')
    @allure.description('Verify imp video ext from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['realtime_HJKM6GM50918'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_video_ext(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that('skip' in bid_request['imp'][0]['video']['ext'])
                assert_that(bid_request['imp'][0]['video']['ext']['videotype'], equal_to('rewarded'))
                assert_that(bid_request['imp'][0]['video']['ext']['rewarded'], equal_to(1))


    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the skip field in bid request video for skippable ad')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['realtime_HJKM6GM50918'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_skippable_ad_imp_video(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['imp'][0]['video']['skip'], equal_to(1))
                assert_that(bid_request['imp'][0]['video']['skipafter'], equal_to(16))
                assert_that(bid_request['imp'][0]['video']['ext']['skip'], equal_to(1))

    # @allure.feature('openrtb 2.5 support')
    # @allure.tag('normal', 'R_1.126.0', 'test_mode')
    # @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    # @allure.description('Verify the skip field in bid request video for non skippable ad')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # @pytest.mark.parametrize('partner', config['hb_partners'])
    # def test_real_time_non_skippable_ad_imp_video(self, pub_app_id, placement, sdk_v, partner):
    #
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             test_device_id=test_mode_device_id, sdk_v=sdk_v,
    #                                             no_pre_cache_token=True, explain=True, ip=au_ip,
    #                                             rtb=test_mode_kraken_rtb_ids_1)
    #
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         if "err_msg" not in response_payload['ext']:
    #             bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
    #             assert_that(bid_request['imp'][0]['video']['ext']['skip'], equal_to(0))

    @allure.feature('mrec support')
    @allure.tag('normal', 'ad_format', 'v1.155.0')
    @allure.story('PBJ-2082 internal MREC placement use dimension w=480 h=400')
    @allure.description('Verify the video merc ad size is w=480 h=400 when request via meister')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_mrec_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_internal_mrec_size_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['imp'][0]['video']['w'], equal_to(480))
                assert_that(bid_request['imp'][0]['video']['h'], equal_to(400))


    # --------------------------------------------- OM SDK -----------------------------------------------------------
    #
    # @allure.feature('omsdk support')
    # @allure.tag('normal', 'R_1.146.0', 'test_mode')
    # @allure.story('PBJ-1978 Regression test for OMSDK feature')
    # @allure.description('Verify the om enabled status for om enabled app')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # @pytest.mark.parametrize('partner', config['hb_partners'])
    # def test_real_time_om_enabled_status_imp_video_app_enabled(self, pub_app_id, placement, sdk_v, partner):
    #
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             test_device_id=test_mode_device_id, sdk_v=sdk_v,
    #                                             no_pre_cache_token=True, explain=True, ip=au_ip,
    #                                             rtb=ext_test_mode_kraken_rtb_ids_vast)
    #
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         if "err_msg" not in response_payload['ext']:
    #             bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_test_mode_kraken_rtb_ids_vast)
    #             assert_keys_exist(bid_request['imp'][0]['video'], 'api')
    #             assert_that(7 in bid_request['imp'][0]['video']['api'])
    #
    #
    #
    # @allure.feature('omsdk support')
    # @allure.tag('normal', 'R_1.146.0', 'test_mode')
    # @allure.story('PBJ-1978 Regression test for OMSDK feature')
    # @allure.description('Verify the om enabled status for om enabled app')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # def test_om_enabled_status_imp_video_app_enabled(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
    #                                                                     vungle_version='5.7', debug='jaeger'))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_exist(bid_request['imp'][0]['video'], 'api')
    #     assert_that(7 in bid_request['imp'][0]['video']['api'])
    #
    # @allure.feature('omsdk support')
    # @allure.tag('normal', 'R_1.146.0', 'test_mode')
    # @allure.story('PBJ-1978 Regression test for OMSDK feature')
    # @allure.description('Verify the om enabled status for no om setting in app level')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    # @pytest.mark.parametrize('placement', ['DEFAULT02024'])
    # def test_om_enabled_status_imp_video_app_default_setting(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
    #                                                                     vungle_version='5.7', debug='jaeger'))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_exist(bid_request['imp'][0]['video'], 'api')
    #     assert_that(7 in bid_request['imp'][0]['video']['api'])
    #
    # @allure.feature('omsdk support')
    # @allure.tag('normal', 'R_1.146.0', 'test_mode')
    # @allure.story('PBJ-1978 Regression test for OMSDK feature')
    # @allure.description('Verify the om enabled status for om disabled app')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b2'])
    # @pytest.mark.parametrize('placement', ['DEFAULT02022'])
    # def test_om_enabled_status_imp_video_app_disabled(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
    #                                                                     vungle_version='5.7', debug='jaeger'))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_not_exist(bid_request['imp'][0]['video'], 'api')
    #
    # @allure.feature('omsdk support')
    # @allure.tag('normal', 'R_1.146.0', 'test_mode')
    # @allure.story('PBJ-1978 Regression test for OMSDK feature')
    # @allure.description('Verify the om enabled status for vungle api version < 5.7')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('apiv', ['5.6'])
    # def test_om_enabled_status_imp_video_vungle_api_version_ctl_1(self, pub_app_id, placement, apiv):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
    #                                                                     vungle_version=apiv, debug='jaeger'))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_not_exist(bid_request['imp'][0]['video'], 'api')
    #
    # @allure.feature('omsdk support')
    # @allure.tag('normal', 'R_1.146.0', 'test_mode')
    # @allure.story('PBJ-1978 Regression test for OMSDK feature')
    # @allure.description('Verify the om enabled status for vungle api version >= 5.7')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('apiv', ['5.7', '5.8'])
    # def test_om_enabled_status_imp_video_vungle_api_version_ctl_2(self, pub_app_id, placement, apiv):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
    #                                                                     vungle_version=apiv, debug='jaeger'))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_exist(bid_request['imp'][0]['video'], 'api')
    #     assert_that(7 in bid_request['imp'][0]['video']['api'])

    @allure.feature('rtb')
    @allure.tag('normal', 'R_1.153.0')
    @allure.story('PBJ-2400 Pass imp.video.companiontype for Endcard Enabled Bidders')
    @allure.description('Verify the companiontype field from bid request via Meister')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_companiontype_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_keys_exist(bid_request['imp'][0]['video'], 'companiontype')
                assert_that(bid_request['imp'][0]['video']['companiontype'], equal_to([1, 2]))


    @allure.feature('battery saver strategy')
    @allure.tag('normal', 'v1.168.0')
    @allure.story('PBJ-2940 Remove Battery saver strategy on iOS 11+')
    @allure.description('Verify that vungle-mraid will not be removed on iOS 11+')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_battery_saver_strategy_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(2 in bid_request['imp'][0]['video']['playbackmethod'])


    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3290 RTB :: Support Bidrequest.imp.video.placement')
    @allure.description('Verify the value of video.placement for the fullscreen placement via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_video_placement_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(bid_request['imp'][0]['video']['placement'], equal_to(5))


    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3290 RTB :: Support Bidrequest.imp.video.placement')
    @allure.description('Verify no video.placement for the banner placement via iDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_video_placement_2(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, banner=True,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_keys_not_exist(bid_request['imp'][0]['banner'], 'placement')

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3290 RTB :: Support Bidrequest.imp.video.placement')
    @allure.description('Verify no video.placement for the mrec placement via iDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_mrec_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_video_placement_2(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_keys_not_exist(bid_request['imp'][0]['video'], 'placement')

    @allure.feature('third party playable')
    @allure.tag('normal', 'v1.197.0')
    @allure.story('PBJ-3810 For fullscreen video placements, send Only video object if a RTB doesn\'t have '
                  '\"third party playable\" selected')
    @allure.description('Verify it only sends video type bid request to DSP via the RTB connection without '
                        'third_party_playable support')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_playable_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_playable_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
                assert_keys_exist(bid_request['imp'][0], 'video')



