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
class TestImpBanner(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('bid request imp banner'
                  'PBJ-4927 Missing "id": 1  & "mimes" in the banner object')
    @allure.description('Verify imp banner obj from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_banner_info(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, header_bidding=True, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('w' in bid_request['imp'][0]['banner'])
        assert_that('h' in bid_request['imp'][0]['banner'])
        assert_that('api' in bid_request['imp'][0]['banner'])
        # PBJ-4927
        assert_keys_exist(bid_request['imp'][0]['banner'], 'id')
        assert_keys_exist(bid_request['imp'][0]['banner'], 'mimes')
        assert_that(bid_request['imp'][0]['banner']['id'], equal_to('1'))
        assert_that(bid_request['imp'][0]['banner']['mimes'], equal_to(['image/jpg', 'image/gif', 'text/html']))

    @allure.feature('banner')
    @allure.tag('smoke', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1382 Support API attribute in OpenRTB Banner Object')
    @allure.description('Verify API attribute in banner obj for internal Banner ad')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_banner_api_internal(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['banner']['api'][0], equal_to(5))

    @allure.feature('programmatic support')
    @allure.tag('smoke', 'test_mode', 'R_1.122.0')
    @allure.story('PBJ-1382 Support API attribute in OpenRTB Banner Object'
                  'PBJ-4927 Missing "id": 1  & "mimes" in the banner object')
    @allure.description('Verify API attribute in banner obj for programmatic Banner ad')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_banner_api_programmatic(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['banner']['api'][0], equal_to(5))
        # PBJ-4927
        assert_keys_exist(bid_request['imp'][0]['banner'], 'id')
        assert_keys_exist(bid_request['imp'][0]['banner'], 'mimes')
        assert_that(bid_request['imp'][0]['banner']['id'], equal_to('1'))
        assert_that(bid_request['imp'][0]['banner']['mimes'], equal_to(['image/jpg', 'image/gif', 'text/html']))


    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0', 'test_mode')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the banner original w and h fields')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_banner_size(self, pub_app_id):
        '''

        Banner size: banner_leaderboard 728*90
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['banner']['w'], equal_to(728))
        assert_that(bid_request['imp'][0]['banner']['h'], equal_to(90))

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0', 'test_mode')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the banner w and h fields in openrtb25x')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_banner_size_for_openrtb25x(self, pub_app_id):
        '''

        Banner size: banner_leaderboard 728*90
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['banner']['format'][0]['w'], equal_to(728))
        assert_that(bid_request['imp'][0]['banner']['format'][0]['h'], equal_to(90))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2813 Set imp.banner.ext.rp.size_id to request the banner in correct size.')
    @allure.description('Verify imp.banner.ext.rp.size_id in XAPI from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_banner_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_imp_banner_info_leaderboard(self, pub_app_id, placement, hb):
        '''

             Banner size: banner_leaderboard 728*90
        '''
        rtb = ext_test_mode_kraken_rtb_ids_banner_xapi
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            header_bidding=hb, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        ext = bid_request['imp'][0]['banner']['ext']
        assert_keys_exist(ext, 'rp')
        assert_that(ext['rp']['size_id'], equal_to(int(2)))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2813 Set imp.banner.ext.rp.size_id to request the banner in correct size.')
    @allure.description('Verify imp.banner.ext.rp.size_id in XAPI from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_banner_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_imp_banner_info_banner(self, pub_app_id, placement, hb):
        '''

             Banner size: banner 320*50
        '''
        rtb = ext_test_mode_kraken_rtb_ids_banner_xapi
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            header_bidding=hb, banner=True, banner_type='banner')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        ext = bid_request['imp'][0]['banner']['ext']
        assert_keys_exist(ext, 'rp')
        assert_that(ext['rp']['size_id'], equal_to(int(43)))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2813 Set imp.banner.ext.rp.size_id to request the banner in correct size.')
    @allure.description('Verify imp.banner.ext.rp.size_id in XAPI from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_banner_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_imp_banner_info_banner_short(self, pub_app_id, placement, hb):
        '''

             Banner size: banner_short 300*50
        '''
        rtb = ext_test_mode_kraken_rtb_ids_banner_xapi
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            header_bidding=hb, banner=True, banner_type='banner_short')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        ext = bid_request['imp'][0]['banner']['ext']
        assert_keys_exist(ext, 'rp')
        assert_that(ext['rp']['size_id'], equal_to(int(44)))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2813 Set imp.banner.ext.rp.size_id to request the banner in correct size.')
    @allure.description('Verify no XAPI from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_banner_placement])
    def test_imp_no_banner_info_leaderboard(self, pub_app_id, placement):
        '''

             Banner size: banner_leaderboard 728*90
        '''
        rtb = test_mode_kraken_rtb_ids_banner_xapi
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=rtb, debug='jaeger'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['imp'][0]['banner'], 'ext')

    @allure.feature('third party playable')
    @allure.tag('normal', 'v1.197.0')
    @allure.story('PBJ-3810 For fullscreen video placements, send Only video object if a RTB doesn\'t have '
                  '\"third party playable\" selected'

                  )
    @allure.description('Verify it only sends video type bid request to DSP via the RTB connection without '
                        'third_party_playable support')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_vungle_mraid_third_party_placement])
    def test_third_party_playable_send_banner_1(self, pub_app_id, placement):
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
        assert_keys_not_exist(bid_request['imp'][0], 'banner')



    @allure.feature('third party playable')
    @allure.tag('normal', 'v1.197.0')
    @allure.story('PBJ-3810 For fullscreen video placements, send Only video object if a RTB doesn\'t have '
                  '\"third party playable\" selected'
                  'PBJ-4927 Missing "id": 1  & "mimes" in the banner object')
    @allure.description('Verify it sends video+banner type bid request to DSP via the RTB connection with '
                        'third_party_playable support')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_vungle_mraid_third_party_placement])
    def test_third_party_playable_send_banner_2(self, pub_app_id, placement):
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
        assert_keys_exist(bid_request['imp'][0], 'banner')
        # PBJ-4927
        assert_keys_exist(bid_request['imp'][0]['banner'], 'id')
        assert_keys_exist(bid_request['imp'][0]['banner'], 'mimes')
        assert_that(bid_request['imp'][0]['banner']['id'], equal_to('1'))
        assert_that(bid_request['imp'][0]['banner']['mimes'], equal_to(['image/jpg', 'image/gif', 'text/html']))

    @allure.feature('third party playable')
    @allure.tag('normal', 'v1.197.1')
    @allure.story('PBJ-3821 Jaeger doesn\'t send playable impression to LO Playable DSP in some case')
    @allure.description('Verify it only sends video type bid request to DSP via the RTB connection without'
                        'third_party_playable supported RTB which mixed with the third_party_playable supported RTB')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_vungle_mraid_third_party_placement])
    def test_third_party_playable_send_banner_3(self, pub_app_id, placement):
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
        assert_keys_not_exist(bid_request['imp'][0], 'banner')

    @allure.feature('third party playable')
    @allure.tag('normal', 'v1.197.1')
    @allure.story('PBJ-3821 Jaeger doesn\'t send playable impression to LO Playable DSP in some case')
    @allure.description('Verify it sends video+banner type bid request to DSP via the RTB connection with'
                        'third_party_playable supported RTB which mixed with the third_party_playable '
                        'non-supported RTB')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_vungle_mraid_third_party_placement])
    def test_third_party_playable_send_banner_4(self, pub_app_id, placement):
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

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_mraid)
        assert_keys_exist(bid_request['imp'][0], 'banner')