import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestImpVideo(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp video')
    @allure.description('Verify imp video info from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_video_info(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
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
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_video_ext(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that('skip' in bid_request['imp'][0]['video']['ext'])
            assert_that(bid_request['imp'][0]['video']['ext']['videotype'], equal_to('rewarded'))
            assert_that(bid_request['imp'][0]['video']['ext']['rewarded'], equal_to(1))

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0', 'test_mode')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the skip field in bid request video for skippable ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_skippable_ad_imp_video(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50918', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['video']['skip'], equal_to(1))
        assert_that(bid_request['imp'][0]['video']['skipafter'], equal_to(16))
        assert_that(bid_request['imp'][0]['video']['ext']['skip'], equal_to(1))

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0', 'test_mode')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the skip field in bid request video for non skippable ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_non_skippable_ad_imp_video(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['video']['ext']['skip'], equal_to(0))

    @allure.feature('mrec support')
    @allure.tag('normal', 'ad_format', 'v1.155.0')
    @allure.story('PBJ-2082 internal MREC placement use dimension w=480 h=400')
    @allure.description('Verify the video merc ad size is w=480 h=400 when request via meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_video_mrec_placement])
    def test_internal_mrec_size_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['video']['w'], equal_to(480))
        assert_that(bid_request['imp'][0]['video']['h'], equal_to(400))

    @allure.feature('mrec support')
    @allure.tag('normal', 'ad_format', 'v1.155.0')
    @allure.story('PBJ-2082 internal MREC placement use dimension w=480 h=400')
    @allure.description('Verify the image merc ad size is w=480 h=400 when request via meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_image_mrec_placement])
    def test_internal_mrec_size_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['video']['w'], equal_to(480))
        assert_that(bid_request['imp'][0]['video']['h'], equal_to(400))

    @allure.feature('mrec support')
    @allure.tag('normal', 'ad_format', 'test_mode', 'v1.155.0')
    @allure.story('PBJ-2082 internal MREC placement use dimension w=480 h=400')
    @allure.description('Verify the video merc ad size is w=480 h=400 when request via kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_video_mrec_placement])
    def test_internal_mrec_size_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['video']['w'], equal_to(480))
        assert_that(bid_request['imp'][0]['video']['h'], equal_to(400))

    @allure.feature('mrec support')
    @allure.tag('normal', 'ad_format', 'test_mode', 'v1.155.0')
    @allure.story('PBJ-2082 internal MREC placement use dimension w=480 h=400')
    @allure.description('Verify the image merc ad size is w=480 h=400 when request via kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_image_mrec_placement])
    def test_internal_mrec_size_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['video']['w'], equal_to(480))
        assert_that(bid_request['imp'][0]['video']['h'], equal_to(400))

    # --------------------------------------------- OM SDK -----------------------------------------------------------

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for om enabled app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_om_enabled_status_imp_video_app_enabled(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        vungle_version='5.7', debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['imp'][0]['video'], 'api')
        assert_that(7 in bid_request['imp'][0]['video']['api'])

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for no om setting in app level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['DEFAULT02024'])
    def test_om_enabled_status_imp_video_app_default_setting(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        vungle_version='5.7', debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['imp'][0]['video'], 'api')
        assert_that(7 in bid_request['imp'][0]['video']['api'])

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for om disabled app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b2'])
    @pytest.mark.parametrize('placement', ['DEFAULT02022'])
    def test_om_enabled_status_imp_video_app_disabled(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        vungle_version='5.7', debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['video'], 'api')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for vungle api version < 5.7')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('apiv', ['5.6'])
    def test_om_enabled_status_imp_video_vungle_api_version_ctl_1(self, pub_app_id, placement, apiv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        vungle_version=apiv, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['video'], 'api')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for vungle api version >= 5.7')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('apiv', ['5.7', '5.8'])
    def test_om_enabled_status_imp_video_vungle_api_version_ctl_2(self, pub_app_id, placement, apiv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        vungle_version=apiv, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['imp'][0]['video'], 'api')
        assert_that(7 in bid_request['imp'][0]['video']['api'])

    @allure.feature('rtb')
    @allure.tag('normal', 'R_1.153.0')
    @allure.story('PBJ-2400 Pass imp.video.companiontype for Endcard Enabled Bidders')
    @allure.description('Verify the companiontype field from bid request via Meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_companiontype_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids,
                                                                        debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['imp'][0]['video'], 'companiontype')
        assert_that(bid_request['imp'][0]['video']['companiontype'], equal_to([1, 2]))

    @allure.feature('rtb')
    @allure.tag('normal', 'R_1.153.0', 'test_mode')
    @allure.story('PBJ-2400 Pass imp.video.companiontype for Endcard Enabled Bidders')
    @allure.description('Verify the companiontype field from bid request via internal Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_companiontype_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids,
                                                                        debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['imp'][0]['video'], 'companiontype')
        assert_that(bid_request['imp'][0]['video']['companiontype'], equal_to([1, 2]))

    @allure.feature('rtb')
    @allure.tag('normal', 'R_1.153.0', 'test_mode')
    @allure.story('PBJ-2400 Pass imp.video.companiontype for Endcard Enabled Bidders')
    @allure.description('Verify the companiontype field from bid request via external Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_companiontype_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['imp'][0]['video'], 'companiontype')
        assert_that(bid_request['imp'][0]['video']['companiontype'], equal_to([1, 2]))

    @allure.feature('battery saver strategy')
    @allure.tag('normal', 'v1.168.0')
    @allure.story('PBJ-2940 Remove Battery saver strategy on iOS 11+')
    @allure.description('Verify that vungle-mraid will not be removed on iOS 11+')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['11.0', '11.1'])
    def test_battery_saver_strategy_1(self, pub_app_id, placement, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids,
                                                                        debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(2 in bid_request['imp'][0]['video']['playbackmethod'])

    @allure.feature('battery saver strategy')
    @allure.tag('normal', 'v1.168.0', 'test_mode')
    @allure.story('PBJ-2940 Remove Battery saver strategy on iOS 11+')
    @allure.description('Verify that vungle-mraid will not be removed on iOS 11+ in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['11.0', '11.1'])
    def test_battery_saver_strategy_2(self, pub_app_id, placement, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids,
                                                                        debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(2 in bid_request['imp'][0]['video']['playbackmethod'])

    @allure.feature('battery saver strategy')
    @allure.tag('normal', 'v1.168.0', 'test_mode')
    @allure.story('PBJ-2940 Remove Battery saver strategy on iOS 11+')
    @allure.description('Verify that vungle-mraid will not be removed on iOS 11+ in test mode with edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['11.0', '11.1'])
    def test_battery_saver_strategy_3(self, pub_app_id, placement, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(2 in bid_request['imp'][0]['video']['playbackmethod'])

    @allure.feature('battery saver strategy')
    @allure.tag('normal', 'v1.168.0')
    @allure.story('PBJ-2940 Remove Battery saver strategy on iOS 11+')
    @allure.description('Verify that vungle-mraid will not be removed on iOS < 11')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('osv', ['10.9'])
    def test_battery_saver_strategy_4(self, pub_app_id, placement, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids,
                                                                        debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(2 in bid_request['imp'][0]['video']['playbackmethod'])

    @allure.feature('battery saver strategy')
    @allure.tag('normal', 'v1.168.0')
    @allure.story('PBJ-2940 Remove Battery saver strategy on iOS 11+')
    @allure.description('Verify that vungle-mraid only imp will not be impacted')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['DEFAULT02021MRAID'])
    @pytest.mark.parametrize('osv', ['10.9', '11.0', '11.1'])
    def test_battery_saver_strategy_5(self, pub_app_id, placement, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids,
                                                                        debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(2 in bid_request['imp'][0]['video']['playbackmethod'])

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for rewarded via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_instl_video_rewarded_flag_1(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['video']['ext']['rewarded'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for rewarded via edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_instl_video_rewarded_flag_2(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['video']['ext']['rewarded'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for interstitial via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_instl_video_rewarded_flag_3(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['video']['ext'], 'rewarded')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for interstitial via edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_instl_video_rewarded_flag_4(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['video']['ext'], 'rewarded')

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3290 RTB :: Support Bidrequest.imp.video.placement')
    @allure.description('Verify the value of video.placement for the fullscreen placement via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_placement_instl])
    def test_video_placement_1(self, pub_app_id, placement):
        rtb = meister_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb, debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['video']['placement'], equal_to(5))

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3290 RTB :: Support Bidrequest.imp.video.placement')
    @allure.description('Verify the value of video.placement for the fullscreen placement via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_placement_instl])
    def test_video_placement_2(self, pub_app_id, placement):
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=rtb, debug='jaeger', src_ip=au_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['video']['placement'], equal_to(5))

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3290 RTB :: Support Bidrequest.imp.video.placement')
    @allure.description('Verify no video.placement for the banner placement via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_video_placement_3(self, pub_app_id, placement):
        rtb = meister_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb, debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['imp'][0]['banner'], 'placement')

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3290 RTB :: Support Bidrequest.imp.video.placement')
    @allure.description('Verify no video.placement for the banner placement via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_video_placement_4(self, pub_app_id, placement):
        rtb = ext_non_test_mode_kraken_rtb_ids_mraid
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=rtb, debug='jaeger', src_ip=au_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['imp'][0]['banner'], 'placement')

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3290 RTB :: Support Bidrequest.imp.video.placement')
    @allure.description('Verify no video.placement for the mrec placement via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_video_mrec_placement, common_test_image_mrec_placement])
    def test_video_placement_5(self, pub_app_id, placement):
        rtb = meister_rtb_ids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb, debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['imp'][0]['video'], 'placement')

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3290 RTB :: Support Bidrequest.imp.video.placement')
    @allure.description('Verify no video.placement for the mrec placement via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    def test_video_placement_6(self, pub_app_id, placement):
        rtb = ext_non_test_mode_kraken_rtb_ids_mraid
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=rtb, debug='jaeger', src_ip=au_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['imp'][0]['banner'], 'placement')

    @allure.feature('third party playable')
    @allure.tag('normal', 'v1.197.0')
    @allure.story('PBJ-3810 For fullscreen video placements, send Only video object if a RTB doesn\'t have '
                  '\"third party playable\" selected')
    @allure.description('Verify it only sends video type bid request to DSP via the RTB connection without '
                        'third_party_playable support')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_vungle_mraid_third_party_placement])
    def test_only_send_video_1(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=rtb, debug='jaeger', src_ip=au_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_exist(bid_request['imp'][0], 'video')

    @allure.feature('third party playable')
    @allure.tag('normal', 'v1.197.0')
    @allure.story('PBJ-3810 For fullscreen video placements, send Only video object if a RTB doesn\'t have '
                  '\"third party playable\" selected')
    @allure.description('Verify it sends video+banner type bid request to DSP via the RTB connection with '
                        'third_party_playable support')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_vungle_mraid_third_party_placement])
    def test_only_send_video_2(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=rtb, debug='jaeger', src_ip=au_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_exist(bid_request['imp'][0], 'video')

    @allure.feature('third party playable')
    @allure.tag('normal', 'v1.197.1')
    @allure.story('PBJ-3821 Jaeger doesn\'t send playable impression to LO Playable DSP in some case')
    @allure.description('Verify it only sends video type bid request to DSP via the RTB connection without'
                        'third_party_playable supported RTB which mixed with the third_party_playable supported RTB')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_vungle_mraid_third_party_placement])
    def test_only_send_video_3(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[0] + ',' + \
                  ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[1] + ',' + \
                  ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=rtb, debug='jaeger', src_ip=au_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        assert_keys_exist(bid_request['imp'][0], 'video')

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_mraid)
        assert_keys_exist(bid_request['imp'][0], 'video')

    @allure.feature('imp video')
    @allure.tag('normal', 'v1.237.0', 'test_mode')
    @allure.story('PBJ-4768 Clean up `allowedDeliveryTypes` in SSP service')
    @allure.description('Verify the value of video.delivery no longer respect the mongo setting for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_allowed_delivery_types_1(self, pub_app_id, placement):
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=rtb, debug='jaeger', src_ip=au_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['video']['delivery'], equal_to([2]))

    @allure.feature('imp video')
    @allure.tag('normal', 'v1.237.0', 'test_mode')
    @allure.story('PBJ-4768 Clean up `allowedDeliveryTypes` in SSP service')
    @allure.description('Verify the value of video.delivery no longer respect the mongo setting for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_allowed_delivery_types_2(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=rtb, debug='jaeger', src_ip=au_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['video']['delivery'], equal_to([2]))
