import math

import pytest
import allure
from time import sleep

from http import HTTPStatus

from data import request_payload
from utils.behaviors import post_hbp_request, request_hb_win_notification, request_hbp, request_hb_loss_notification, \
    request_hbp_with_real_time_token, get_bid_request_obj_from_hbp_explain, request_realtime_win_notification, \
    post_hbp_request_no_retry, decode_admob_event_token, decode_admob_event_token_legacy, decode_real_time_adunit, \
    generate_real_time_token, encode_real_time_token
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema
import time


@allure.epic('Real-time Ad')
class TestHBPRealtimeAd(object):

    @allure.feature('real-time ad')
    @allure.tag('smoke', 'v0.69.0')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 1 - Test for real-time ad token'
                  'PBJ-3559 Remove 6.11.0 for supertoken v2 restriction in Jaeger'
                  'PBJ-3508 [COPPA] read coppa flag from realtime token and process it with realtime case')
    @allure.description('Verify the responded adm by requesting HBP with the real-time token via SDK >= 6.12.0'
                        'Verify read coppa flag from realtime token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_response_adm_1(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, coppa=coppa,
                                                no_pre_cache_token=False, ads_retry_mode='meister')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                rendering_data = adm['rendering_data']
                if rendering_data != "ADVANCED_BIDDER":
                    r = get(str_to_json(adm['rendering_data'])['impression'][0], headers=platform_headers())
                    response_payload = r.json()
                    assert_response_status_code(r.status_code, HTTPStatus.OK)
                    assert_that(response_payload['msg'], equal_to('ok'))
                    assert_that(response_payload['code'], equal_to(200))
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                if adm != "ADVANCED_BIDDER":
                    r = get(str_to_json(adm)['impression'][0], headers=platform_headers())
                    response_payload = r.json()
                    assert_response_status_code(r.status_code, HTTPStatus.OK)
                    assert_that(response_payload['msg'], equal_to('ok'))
                    assert_that(response_payload['code'], equal_to(200))

    @allure.feature('real-time ad')
    @allure.tag('smoke', 'v0.69.0')
    @allure.story('PBJ-3157 Real-time Ad Test - Req 6 - for banner ads supporting'
                  'PBJ-3559 Remove 6.11.0 for supertoken v2 restriction in Jaeger')
    @allure.description('Verify the responded adm by requesting HBP banner format via SDK >= 6.10.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement,
                                           ])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])

    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_response_adm_2(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True,
                                                coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                r = get(str_to_json(adm['rendering_data'])['impression'][0], headers=platform_headers())
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                r = get(str_to_json(adm)['impression'][0], headers=platform_headers())

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(response_payload['msg'], equal_to('ok'))
            assert_that(response_payload['code'], equal_to(200))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0', 'v0.69.0')
    @allure.story('PBJ-3157 Real-time Ad Test - Req 6 - for full screen video ads supporting'
                  'PBJ-3559 Remove 6.11.0 for supertoken v2 restriction in Jaeger')
    @allure.description('Verify the responded adm by requesting HBP full screen format via SDK >= 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [False])
    def test_real_time_ad_response_adm_3(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                r = get(str_to_json(adm['rendering_data'])['impression'][0], headers=platform_headers())
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                r = get(str_to_json(adm)['impression'][0], headers=platform_headers())

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(response_payload['msg'], equal_to('ok'))
            assert_that(response_payload['code'], equal_to(200))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0', 'v0.69.0')
    @allure.story('PBJ-3157 Real-time Ad Test - Req 6 - for mrec ads supporting'
                  'PBJ-3559 Remove 6.11.0 for supertoken v2 restriction in Jaeger')
    @allure.description('Verify the responded adm by requesting HBP mrec format via SDK >= 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_mrec_placement, common_test_hybrid_mrec_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_response_adm_4(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                r = get(str_to_json(adm['rendering_data'])['impression'][0], headers=platform_headers())
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                r = get(str_to_json(adm)['impression'][0], headers=platform_headers())

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(response_payload['msg'], equal_to('ok'))
            assert_that(response_payload['code'], equal_to(200))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 1 - Test for real-time ad token')
    @allure.description('Verify the v3 super token can work with the old format bid token via SDK < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_ad_response_adm_5(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']['rendering_data']
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
            assert_that(adm, equal_to('ADVANCED_BIDDER'))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 6 - for full screen video ads supporting')
    @allure.description('Verify the v3 super token can work with the old video format bid token via SDK < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_response_adm_6(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']['rendering_data']
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']

            assert_that(adm, equal_to('ADVANCED_BIDDER'))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 6 - for mrec ads supporting')
    @allure.description('Verify the v3 super token can work with the old mrec format bid token via SDK < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_mrec_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [False])
    def test_real_time_ad_response_adm_7(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']['rendering_data']
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']

            assert_that(adm, equal_to('ADVANCED_BIDDER'))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 6 - for banner ads supporting')
    @allure.description('Verify the v3 super token can work with the old banner format bid token via SDK < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [False])
    def test_real_time_ad_response_adm_8(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']['rendering_data']
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']

            assert_that(adm, equal_to('ADVANCED_BIDDER'))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0', 'v0.69.0')
    @allure.story('PBJ-3155 Real-time Ad Test - Req 4&5 - Test for supporting real-time ad markup'
                  'PBJ-3559 Remove 6.11.0 for supertoken v2 restriction in Jaeger'
                  'PBJ-3508 [COPPA] read coppa flag from realtime token and process it with realtime case')
    @allure.description('Verify the responded adm of real-time mode which the token includes no pre-cache tokens')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_ad_response_adm_real_time_only_1(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0', 'v0.69.0')
    @allure.story('PBJ-3155 Real-time Ad Test - Req 4&5 - Test for supporting real-time ad markup'
                  'PBJ-3559 Remove 6.11.0 for supertoken v2 restriction in Jaeger')
    @allure.description('Verify the responded adm of real-time mode which the token includes pre-cache tokens')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_response_adm_real_time_only_2(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                coppa=coppa, ads_retry_mode='meister')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                adm_version = str_to_json(adm['rendering_data'])['version']
                assert_that(adm_version in [1, 2])
                if adm_version == 2:
                    assert_keys_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                adm_version = str_to_json(adm)['version']
                assert_that(adm_version in [1, 2])
                if adm_version == 2:
                    assert_keys_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0', 'v0.69.0')
    @allure.story('PBJ-3155 Real-time Ad Test - Req 4&5 - Test for supporting real-time ad markup'
                  'PBJ-3559 Remove 6.11.0 for supertoken v2 restriction in Jaeger')
    @allure.description('Verify the responded adm of hybrid mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_response_adm_hybrid_1(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                coppa=coppa, ads_retry_mode='meister')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                adm_version = str_to_json(adm['rendering_data'])['version']
                assert_that(adm_version in [1, 2])
                if adm_version == 2:
                    assert_keys_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                adm_version = str_to_json(adm)['version']
                assert_that(adm_version in [1, 2])
                if adm_version == 2:
                    assert_keys_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0', 'v0.69.0')
    @allure.story('PBJ-3155 Real-time Ad Test - Req 4&5 - Test for supporting real-time ad markup'
                  'PBJ-3559 Remove 6.11.0 for supertoken v2 restriction in Jaeger')
    @allure.description('Verify the responded adm of hybrid mode which the token includes no pre-cache tokens')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_response_adm_hybrid_2(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True
                                                , coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0', 'v0.69.0')
    @allure.story('PBJ-3155 Real-time Ad Test - Req 4&5 - Test for supporting real-time ad markup'
                  'PBJ-3559 Remove 6.11.0 for supertoken v2 restriction in Jaeger')
    @allure.description('Verify the responded adm of pre-cache mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_response_adm_pre_cache_1(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False
                                                , coppa=coppa, ads_retry_mode='meister')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            ads_response = info['ads_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(1))
                assert_keys_not_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
                assert_that(str_to_json(adm['rendering_data'])['event_id'],
                            equal_to(ads_response['ads'][0]['ad_markup']['id']))
                r = get(str_to_json(adm['rendering_data'])['impression'][0], headers=platform_headers())
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(1))
                assert_keys_not_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')
                assert_that(str_to_json(adm)['event_id'], equal_to(ads_response['ads'][0]['ad_markup']['id']))
                r = get(str_to_json(adm)['impression'][0], headers=platform_headers())

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(response_payload['msg'], equal_to('ok'))
            assert_that(response_payload['code'], equal_to(200))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0', 'v0.69.0')
    @allure.story('PBJ-3155 Real-time Ad Test - Req 4&5 - Test for supporting real-time ad markup')
    @allure.description('Verify the responded adm of pre-cache mode which the token includes no pre-cache tokens'
                        'PBJ-3559 Remove 6.11.0 for supertoken v2 restriction in Jaeger')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_response_adm_pre_cache_2(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True
                                                , coppa=coppa)

        assert_that(info['is_hbp_responded_200'], equal_to(False))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3158 Real-time Ad Test - Req 8 - Test for passing ordinal view to Meister')
    @allure.story('PBJ-3935 HBP - Fix hb realtime crash when request device extension does not exist')
    @allure.description('Verify the responded adm of real-time mode which the token includes no pre-cache tokens')
    @allure.description('Verify hbp can work well for no device extension exists.')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_ad_ordinal_view_real_time_only_1(self, pub_app_id, placement, sdk_v, partner, oridinal_view,
                                                        coppa):

        override_bid_response_any = 'seatbid.0.bid.0.cid@"realTimeCid_r_%s"' % gen_device_id()
        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, coppa=coppa,
                                                ads_retry_mode='meister',
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_keys_exist(idsp_bid_request['app']['ext']['vungle'], 'hb_ordinal')
            hb_ordinal = idsp_bid_request['app']['ext']['vungle']['hb_ordinal']

            assert_that(hb_ordinal, equal_to(oridinal_view))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3158 Real-time Ad Test - Req 8 - Test for passing ordinal view to Meister')
    @allure.description('Verify hbp can work well for device extension exists.')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_ad_ordinal_view_real_time_only_for_device_ext(self, pub_app_id, placement, sdk_v, partner,
                                                                     oridinal_view,
                                                                     coppa):
        test_device_id = gen_device_id()
        device_ext = {
            "ifv": "",
            "atts": 3,
            "time_zone": "Asia/Shanghai",
            "volume_level": "0.47500002384185791",
            "battery_saver_enabled": 0,
            "muted": 1,
            "orientation": 0,
            "mac": "1121212",
            "idfv": test_device_id,
        }

        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=test_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, coppa=coppa,
                                                device_ext=device_ext)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_keys_exist(idsp_bid_request['app']['ext']['vungle'], 'hb_ordinal')
            hb_ordinal = idsp_bid_request['app']['ext']['vungle']['hb_ordinal']

            assert_that(hb_ordinal, equal_to(oridinal_view))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3158 Real-time Ad Test - Req 8 - Test for passing ordinal view to Meister')
    @allure.description('Verify hbp can work well for null device extension')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_ad_ordinal_view_real_time_only_null_device_ext_1(self, pub_app_id, placement, sdk_v, partner,
                                                                        oridinal_view,
                                                                        coppa):
        test_device_id = gen_device_id()
        device_ext = {

        }

        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=test_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, coppa=coppa,
                                                device_ext=device_ext)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_keys_exist(idsp_bid_request['app']['ext']['vungle'], 'hb_ordinal')
            hb_ordinal = idsp_bid_request['app']['ext']['vungle']['hb_ordinal']

            assert_that(hb_ordinal, equal_to(oridinal_view))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3158 Real-time Ad Test - Req 8 - Test for passing ordinal view to Meister')
    @allure.description('Verify the responded adm of real-time mode which the token includes pre-cache tokens')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_ordinal_view_real_time_only_2(self, pub_app_id, placement, sdk_v, partner, oridinal_view,
                                                        coppa):
        override_bid_response_any = 'seatbid.0.bid.0.cid@"realTimeCid_%s"' % gen_device_id()
        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, coppa=coppa,
                                                ads_retry_mode='meister',
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_keys_exist(idsp_bid_request['app']['ext']['vungle'], 'hb_ordinal')
            hb_ordinal = idsp_bid_request['app']['ext']['vungle']['hb_ordinal']
            assert_that(hb_ordinal, equal_to(oridinal_view))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3158 Real-time Ad Test - Req 8 - Test for passing ordinal view to Meister')
    @allure.description('Verify the responded adm of hybrid mode which the token includes no pre-cache tokens')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_ad_ordinal_view_hybrid_1(self, pub_app_id, placement, sdk_v, partner, oridinal_view, coppa):
        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, coppa=coppa, )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_keys_exist(idsp_bid_request['app']['ext']['vungle'], 'hb_ordinal')
            hb_ordinal = idsp_bid_request['app']['ext']['vungle']['hb_ordinal']

            assert_that(hb_ordinal, equal_to(oridinal_view))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3158 Real-time Ad Test - Req 8 - Test for passing ordinal view to Meister')
    @allure.description('Verify the responded adm of hybrid mode which the token includes pre-cache tokens')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_ordinal_view_hybrid_2(self, pub_app_id, placement, sdk_v, partner, oridinal_view, coppa):

        override_bid_response_any = 'seatbid.0.bid.0.cid@"realTimeCid_h_%s"'%gen_device_id()
        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, coppa=coppa,
                                                ads_retry_mode='meister', override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_keys_exist(idsp_bid_request['app']['ext']['vungle'], 'hb_ordinal')
            hb_ordinal = idsp_bid_request['app']['ext']['vungle']['hb_ordinal']
            assert_that(hb_ordinal, equal_to(oridinal_view))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3158 Real-time Ad Test - Req 8 - Test for passing ordinal view to Meister')
    @allure.description('Verify the responded adm of pre-cache mode which the token includes no pre-cache tokens')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_ordinal_view_pre_cache_1(self, pub_app_id, placement, sdk_v, partner, oridinal_view, coppa):
        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, coppa=coppa)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.hbp_error_realtime)
            assert_keys_exist(response_payload['ext'], 'err_msg')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3158 Real-time Ad Test - Req 8 - Test for passing ordinal view to Meister')
    @allure.description('Verify the responded adm of pre-cache mode which the token includes pre-cache tokens')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_ad_ordinal_view_pre_cache_2(self, pub_app_id, placement, sdk_v, partner, oridinal_view, coppa):
        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, coppa=coppa,
                                                ads_retry_mode='meister')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                assert_keys_exist(response_payload['seatbid'][0]['bid'][0]['ext'], 'sdk_rendered_ad')
            else:
                assert_keys_exist(response_payload['seatbid'][0]['bid'][0], 'adm')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify the SDK version will not impact the real-time serving on SSP side')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.1', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_ad_response_adm_sdk_version_1(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True
                                                , coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify the SDK version will not impact the pre-cache serving on SSP side')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.1', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_ad_response_adm_sdk_version_2(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, explain=True,
                                                coppa=coppa)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3204 Fix banner size behavior for hb realtime request')
    @allure.description('Verify the h,w under banner will be used if there is no banner format from bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max', 'admob'])
    @pytest.mark.parametrize('banner_format', [None, []])
    @pytest.mark.parametrize('coppa', [False])
    def test_real_time_banner_size_1(self, pub_app_id, placement, sdk_v, partner, banner_format, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True, explain=True,
                                                no_pre_cache_token=True, banner_format=banner_format,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_that(idsp_bid_request['imp'][0]['banner']['format'][0]['w'], equal_to(320))
            assert_that(idsp_bid_request['imp'][0]['banner']['format'][0]['h'], equal_to(50))
            assert_that(idsp_bid_request['imp'][0]['banner']['w'], equal_to(320))
            assert_that(idsp_bid_request['imp'][0]['banner']['h'], equal_to(50))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3204 Fix banner size behavior for hb realtime request')
    @allure.description('Verify the h,w under banner.format will be used if there is banner format from bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max', 'admob'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_banner_size_2(self, pub_app_id, placement, sdk_v, partner, coppa):
        banner_format = [
            {
                "w": 300,
                "h": 50
            }
        ]

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True, explain=True,
                                                no_pre_cache_token=True, banner_format=banner_format,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_that(idsp_bid_request['imp'][0]['banner']['format'][0]['w'], equal_to(300))
            assert_that(idsp_bid_request['imp'][0]['banner']['format'][0]['h'], equal_to(50))
            assert_that(idsp_bid_request['imp'][0]['banner']['w'], equal_to(300))
            assert_that(idsp_bid_request['imp'][0]['banner']['h'], equal_to(50))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3204 Fix banner size behavior for hb realtime request')
    @allure.description('Verify that no h,w under banner from the DSP bid request if there are multiple objs in'
                        'banner.format from bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max', 'admob'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_banner_size_3(self, pub_app_id, placement, sdk_v, partner, coppa):
        banner_format = [
            {
                "w": 300,
                "h": 50
            },
            {
                "w": 320,
                "h": 50
            }
        ]

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True, explain=True,
                                                no_pre_cache_token=True, banner_format=banner_format,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_that(idsp_bid_request['imp'][0]['banner']['format'], equal_to(banner_format))
            assert_that(idsp_bid_request['imp'][0]['banner']['format'], equal_to(banner_format))
            assert_keys_not_exist(idsp_bid_request['imp'][0]['banner'], 'w')
            assert_keys_not_exist(idsp_bid_request['imp'][0]['banner'], 'h')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3204 Fix banner size behavior for hb realtime request')
    @allure.description('Verify that only the Vungle supported banner format will be passed to DSP bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max', 'admob'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_banner_size_4(self, pub_app_id, placement, sdk_v, partner, coppa):
        banner_format = [
            {
                "w": 300,
                "h": 50
            },
            {
                "w": 310,
                "h": 50
            }
        ]
        expected_format = [
            {
                "w": 300,
                "h": 50
            }
        ]

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True, explain=True,
                                                no_pre_cache_token=True, banner_format=banner_format,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_that(idsp_bid_request['imp'][0]['banner']['format'], equal_to(expected_format))
            assert_that(idsp_bid_request['imp'][0]['banner']['format'], equal_to(expected_format))
            assert_that(idsp_bid_request['imp'][0]['banner']['w'], equal_to(300))
            assert_that(idsp_bid_request['imp'][0]['banner']['h'], equal_to(50))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3204 Fix banner size behavior for hb realtime request')
    @allure.description('Verify that only the Vungle supported banner format will be passed to DSP bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max', 'admob'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_banner_size_5(self, pub_app_id, placement, sdk_v, partner, coppa):
        banner_format = [
            {
                "w": 300,
                "h": 50
            },
            {
                "w": 310,
                "h": 50
            },
            {
                "w": 728,
                "h": 90
            }
        ]
        expected_format = [
            {
                "w": 300,
                "h": 50
            },
            {
                "w": 728,
                "h": 90
            }
        ]

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True, explain=True,
                                                no_pre_cache_token=True, banner_format=banner_format,
                                                rtb=ext1_non_test_mode_kraken_rtb_prefiltering_06, coppa=coppa)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

        idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
        assert_that(idsp_bid_request['imp'][0]['banner']['format'], equal_to(expected_format))
        assert_that(idsp_bid_request['imp'][0]['banner']['format'], equal_to(expected_format))
        assert_keys_not_exist(idsp_bid_request['imp'][0]['banner'], 'w')
        assert_keys_not_exist(idsp_bid_request['imp'][0]['banner'], 'h')

    @allure.feature('real-time PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify request with banner size "300x50", "320x50" for banner placement '
                        'will pass to downstreams')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_prefiltering_rtb_match_ad_size_01(self, pub_app_id, placement, sdk_v, partner, coppa):
        banner_format = [
            {
                "w": 300,
                "h": 50
            }
        ]

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True, explain=True,
                                                no_pre_cache_token=True, banner_format=banner_format,
                                                rtb=ext1_non_test_mode_kraken_rtb_prefiltering_06, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_that(idsp_bid_request['imp'][0]['banner']['format'][0]['w'], equal_to(300))
            assert_that(idsp_bid_request['imp'][0]['banner']['format'][0]['h'], equal_to(50))
            assert_that(idsp_bid_request['imp'][0]['banner']['w'], equal_to(300))
            assert_that(idsp_bid_request['imp'][0]['banner']['h'], equal_to(50))

    @allure.feature('real-time PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description('Verify request with banner size "728x90" for banner placement will not pass to downstreams')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_prefiltering_rtb_match_ad_size_02(self, pub_app_id, placement, sdk_v, partner, coppa):
        banner_format = [
            {
                "w": 728,
                "h": 90
            }
        ]

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True, explain=True,
                                                no_pre_cache_token=True, banner_format=banner_format,
                                                rtb=ext1_non_test_mode_kraken_rtb_prefiltering_06, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload['ext']['debug'], 'rtb_failed_filters')

    @allure.feature('real-time PreFiltering')
    @allure.tag('normal')
    @allure.story('PBJ-3996 Jaeger - RTB Filter Phase II')
    @allure.description(
        'Verify request with banner size "728x90" and "320x50" for banner placement will pass to downstreams')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_prefiltering_rtb_match_ad_size_03(self, pub_app_id, placement, sdk_v, partner, coppa):
        banner_format = [
            {
                "w": 728,
                "h": 90
            },
            {
                "w": 320,
                "h": 50
            }
        ]

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True, explain=True,
                                                no_pre_cache_token=True, banner_format=banner_format,
                                                rtb=ext1_non_test_mode_kraken_rtb_prefiltering_06, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_not_exist(response_payload['ext']['debug'], 'rtb_failed_filters')

    @allure.feature('real-time ad')
    @allure.tag('smoke')
    @allure.story('PBJ-3325 Test mode improvement for app bidding')
    @allure.description('Verify test mode for app bidding when app test mode = OFF and is_test=1')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement',
                             [common_test_placement, common_test_hybrid_placement, common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_test_mode_for_app_bidding_01(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1,
                                                coppa=coppa, no_pre_cache_token=False, ads_retry_mode='meister')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            price = response_payload['seatbid'][0]['bid'][0]['price']
            if partner == 'admob':
                assert_that(price, equal_to(4999))
            else:
                assert_that(price, equal_to(50.001))
            test_flag = response_payload['ext']['test']
            assert_that(test_flag, equal_to(1))

    @allure.feature('real-time ad')
    @allure.tag('smoke', 'v1.223.0')
    @allure.story('PBJ-3325 Test mode improvement for app bidding'
                  'PBJ-4361 RealTime:: All mediation partners should reponse creative id & campaign id')
    @allure.description('Verify test mode for app bidding when app test mode = OFF and is_test=0'
                        'Verify cid & crid exist in bid response ')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    def test_real_time_test_mode_for_app_bidding_02(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=0, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            price = response_payload['seatbid'][0]['bid'][0]['price']
            assert_that(price, is_not(99))
            assert_keys_exist(bid_info, 'cid')
            assert_keys_exist(bid_info, 'crid')
            assert_that(isinstance(bid_info['cid'], str))
            assert_that(isinstance(bid_info['crid'], str))

    @allure.feature('real-time ad')
    @allure.tag('smoke', 'v1.223.0')
    @allure.story('PBJ-3325 Test mode improvement for app bidding'
                  'PBJ-4361 RealTime:: All mediation partners should response creative id & campaign id')
    @allure.description('Verify test mode for app bidding when app test mode = OFF and is_test=0'
                        'Verify cid & crid exist in bid response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [False])
    def test_real_time_test_mode_for_app_bidding_with_no_precached_02(self, pub_app_id, placement, sdk_v, partner,
                                                                      coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                no_pre_cache_token=True,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=0, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            price = response_payload['seatbid'][0]['bid'][0]['price']
            assert_that(price, is_not(99))
            assert_keys_exist(bid_info, 'cid')
            assert_keys_exist(bid_info, 'crid')
            assert_that(isinstance(bid_info['cid'], str))
            assert_that(isinstance(bid_info['crid'], str))

    @allure.feature('real-time ad')
    @allure.tag('smoke')
    @allure.story('PBJ-3325 Test mode improvement for app bidding')
    @allure.description('Verify test mode for app bidding when app test mode = on and is_test=1')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement',
                             [common_test_placement, common_test_hybrid_placement, common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_test_mode_for_app_bidding_03(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=1, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            price = response_payload['seatbid'][0]['bid'][0]['price']
            if partner == 'admob':
                assert_that(price, equal_to(4999))
            else:
                assert_that(price, equal_to(50.001))
            test_flag = response_payload['ext']['test']
            assert_that(test_flag, equal_to(1))

    @allure.feature('real-time ad')
    @allure.tag('smoke')
    @allure.story('PBJ-3325 Test mode improvement for app bidding')
    @allure.description('Verify test mode for app bidding when app test mode = on and is_test=0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_hybrid_placement,
                                           common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_test_mode_for_app_bidding_04(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids, explain=True,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=0, coppa=coppa)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            price = bid_response['price']
            if partner == 'admob':
                assert_that(price, equal_to(4999))
                adm = json.loads(bid_response['ext']['sdk_rendered_ad']['rendering_data'])
            else:
                assert_that(price, equal_to(50.001))
                adm = json.loads(bid_response['adm'])
            if adm['version'] == 2:
                assert_keys_exist(response_payload, 'ext')
            else:
                test_flag = response_payload['ext']['test']
                assert_that(test_flag, equal_to(1))

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-4486 [Jaeger] fix winttl for using pub app obj id')
    @allure.description('Verify it will not bid again for the token which has already win on MAX real-time request with'
                        'pre-cached placement if the app in the winttl setting of the partner: storeID & pubappId different')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_placement_old])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_admob_winttl_realtime_storeID_pubappID_diff(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('admob', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                 rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                 no_pre_cache_token=False, ads_retry_mode='kraken')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_admob_endpoint_qa, json=req,
                                          headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug='jaeger',
                                                              rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.hbp_error_realtime)
            assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-4486 [Jaeger] fix winttl for using pub app obj id')
    @allure.description('Verify it will not bid again for the token which has already win on MAX real-time request with'
                        'pre-cached placement if the app in the winttl setting of the partner: storeID & pubappId different')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_placement_old])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.6', 'Vungle/6.12.0'])
    def test_max_winttl_realtime_storeID_pubappID_diff(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                 rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                 no_pre_cache_token=False, ads_retry_mode='kraken')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_max_endpoint_qa, json=req,
                                          headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug='jaeger',
                                                              rtb_selector=meister_rtb_ids))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.hbp_error_realtime)
            assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify it will not bid again for the token which has already win on MAX real-time request with'
                        'pre-cached placement if the app in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_sdk_version_realtime_1(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_max_endpoint_qa, json=req,
                                          headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug='jaeger',
                                                              rtb_selector=meister_rtb_ids))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.hbp_error_realtime)
            assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify it will bid again for the token which has already win on MAX real-time request with'
                        'pre-cached placement if the app not in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_sdk_version_realtime_1_1(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_max_endpoint_qa, json=req,
                                          headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug='jaeger',
                                                              rtb_selector=meister_rtb_ids))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            if 'ext' in response_payload and 'err_msg' in response_payload['ext']:
                assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' not in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3853 Apply winttl enhancement to all pubs for the pre-cached scenarios of real-time traffic',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify the winttl should be deleted if hits the winttl for two times on MAX real-time request '
                        'with pre-cached placement if the app in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_twice_hit_delete_winttl_realtime_1(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_max_endpoint_qa, json=req, headers=hbp_headers(debug='jaeger'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.hbp_error_precache)
            assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' in response_payload['ext']['err_msg'])
            # The 2nd time request
            r = post_hbp_request_no_retry(hbp_max_endpoint_qa, json=req,
                                          headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug='jaeger'))
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            if 'ext' in response_payload and 'err_msg' in response_payload['ext']:
                assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' not in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify it will bid again for the token which has already win on MAX real-time request with'
                        'real-time placement if the app in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_sdk_version_realtime_2(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=True, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_max_endpoint_qa, json=req,
                                          headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v,
                                                              rtb_selector=meister_rtb_ids, debug='jaeger'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            if 'ext' in response_payload and 'err_msg' in response_payload['ext']:
                assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' not in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify it will bid again for the token which has already win on MAX real-time request with'
                        'real-time placement if the app not in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_sdk_version_realtime_2_1(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=True, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_max_endpoint_qa, json=req,
                                          headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v,
                                                              rtb_selector=meister_rtb_ids, debug='jaeger'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            if 'ext' in response_payload and 'err_msg' in response_payload['ext']:
                assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' not in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3853 Apply winttl enhancement to all pubs for the pre-cached scenarios of real-time traffic',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify the change will not impact the real-time request for MAX '
                        'if the app not in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_twice_hit_delete_winttl_realtime_2_1(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=True, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request(hbp_max_endpoint_qa, json=req,
                                 headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, rtb_selector=meister_rtb_ids,
                                                     debug='jaeger'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            if 'ext' in response_payload and 'err_msg' in response_payload['ext']:
                assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' not in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3853 Apply winttl enhancement to all pubs for the pre-cached scenarios of real-time traffic',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify the change will not impact the real-time request for MAX '
                        'if the app in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_twice_hit_delete_winttl_realtime_2_2(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=True, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request(hbp_max_endpoint_qa, json=req,
                                 headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, rtb_selector=meister_rtb_ids,
                                                     debug='jaeger'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            if 'ext' in response_payload and 'err_msg' in response_payload['ext']:
                assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' not in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify it will bid again if the ordinal view count is less than the view in winttl '
                        'on MAX real-time request with pre-cached placement '
                        'if the app in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_sdk_version_realtime_3_1(self, pub_app_id, placement, sdk_v):
        test_ifa = gen_device_id()
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False)
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            ordinal_view_count = info['ordinal_view']
            bid_token = info['bid_token']
            info_1 = request_hbp_with_real_time_token('max', ordinal_view_count - 1, pub_app_id=pub_app_id,
                                                      placement_ref_id=placement, test_device_id=test_ifa, sdk_v=sdk_v,
                                                      rtb=meister_rtb_ids, no_pre_cache_token=False,
                                                      ads_retry_mode='meister', post_retry=False, explain=True,
                                                      existing_precache_bid_token=bid_token)
            if info_1['is_hbp_responded_200']:
                response_payload = info_1['hbp_response']
                if 'ext' in response_payload and 'err_msg' in response_payload['ext']:
                    assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' not in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify it will bid again if the ordinal view count is less than the view in winttl '
                        'on MAX real-time request with pre-cached placement '
                        'if the app not in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_sdk_version_realtime_3_2(self, pub_app_id, placement, sdk_v):
        test_ifa = gen_device_id()
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False)
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            ordinal_view_count = info['ordinal_view']
            bid_token = info['bid_token']
            info_1 = request_hbp_with_real_time_token('max', ordinal_view_count - 1, pub_app_id=pub_app_id,
                                                      placement_ref_id=placement, test_device_id=test_ifa, sdk_v=sdk_v,
                                                      rtb=meister_rtb_ids, no_pre_cache_token=False,
                                                      ads_retry_mode='meister', post_retry=False, explain=True,
                                                      existing_precache_bid_token=bid_token)
            if info_1['is_hbp_responded_200']:
                response_payload = info_1['hbp_response']
                if 'ext' in response_payload and 'err_msg' in response_payload['ext']:
                    assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' not in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify it will not bid again if the ordinal view count is equal to the view in winttl'
                        'if the app in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_sdk_version_realtime_4_1(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_max_endpoint_qa, json=req,
                                          headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug='jaeger',
                                                              rtb_selector=meister_rtb_ids))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.hbp_error_realtime)
            assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify it will bid again if the ordinal view count is equal to the view in winttl'
                        'if the app ont in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_sdk_version_realtime_4_2(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_max_endpoint_qa, json=req,
                                          headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug='jaeger',
                                                              rtb_selector=meister_rtb_ids))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            if 'ext' in response_payload and 'err_msg' in response_payload['ext']:
                assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' not in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify it will not bid again if the ordinal view count is greater than the view in winttl'
                        'if the app in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_sdk_version_realtime_5_1(self, pub_app_id, placement, sdk_v):
        test_ifa = gen_device_id()
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=test_ifa, sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            ordinal_view_count = info['ordinal_view']
            bid_token = info['bid_token']
            info_1 = request_hbp_with_real_time_token('max', ordinal_view_count + 1, pub_app_id=pub_app_id,
                                                      placement_ref_id=placement, test_device_id=test_ifa, sdk_v=sdk_v,
                                                      rtb=meister_rtb_ids, no_pre_cache_token=False,
                                                      ads_retry_mode='meister', post_retry=False, explain=True,
                                                      existing_precache_bid_token=bid_token)
            if info_1['is_hbp_responded_200']:
                response_payload = info_1['hbp_response']
                assert_valid_schema(response_payload, response_schema.hbp_error_realtime)
                assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' in response_payload['ext']['err_msg'])

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3501 Sync HBP changes to Jaeger',
                  'PBJ-4118 [Scrat] using app objectId for winttl app')
    @allure.description('Verify it will bid again if the ordinal view count is greater than the view in winttl'
                        'if the app not in the winttl setting of the partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.12.0'])
    def test_max_winttl_sdk_version_realtime_5_2(self, pub_app_id, placement, sdk_v):
        test_ifa = gen_device_id()
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False, ads_retry_mode='meister')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            ordinal_view_count = info['ordinal_view']
            bid_token = info['bid_token']
            info_1 = request_hbp_with_real_time_token('max', ordinal_view_count + 1, pub_app_id=pub_app_id,
                                                      placement_ref_id=placement, test_device_id=test_ifa, sdk_v=sdk_v,
                                                      rtb=meister_rtb_ids, no_pre_cache_token=False,
                                                      ads_retry_mode='meister', post_retry=False, explain=True,
                                                      existing_precache_bid_token=bid_token)
            if info_1['is_hbp_responded_200']:
                response_payload = info_1['hbp_response']
                if 'ext' in response_payload and 'err_msg' in response_payload['ext']:
                    assert_that('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL' not in response_payload['ext']['err_msg'])

    @allure.feature('win ttl experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4208 Reduce the WinTTL for MAX')
    @allure.description('Verify max will enter the experiment and winTTL experiment Tag is not added in bidtoken '
                        'on realTime mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.1;Max'])
    def test_max_winttl_experiment_realtime_1(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 10, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False, ads_retry_mode='meister')
        if info['is_hbp_responded_200']:
            ext = info['ext']
            assert_keys_exist(ext, 'exp_win_ttl')
            assert_that(ext['exp_win_ttl'] in [15, 30, 45, 60])
            # verify experiment info added in jaeger transaction & deliveriy
            # exp_to_bucket":"{\\"win_ttl\\":\\"X_mins\\"}
            # Verify scrat send win ttl and apply the experiment
            # Verify exp tag is added in hb-transaction
            # Verify hp notification

    @allure.feature('win ttl experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4208 Reduce the WinTTL for MAX')
    @allure.description('Verify max will enter the experiment and winTTL experiment Tag is not added'
                        'for realtime ads')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.1;Max'])
    def test_max_winttl_experiment_realtime_2(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=True, ads_retry_mode='meister')
        if info['is_hbp_responded_200']:
            ext = info['ext']
            assert_keys_not_exist(ext, 'exp_win_ttl')

    @allure.feature('win ttl experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4208 Reduce the WinTTL for MAX')
    @allure.description('Verify max will not enter the experiment and winTTL experiment Tag is not added'
                        'w/o partner name or plugin name for realtime ads')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.1'])
    def test_max_winttl_experiment_realtime_3(self, pub_app_id, placement, sdk_v):
        info = request_realtime_win_notification('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=sdk_v, rtb=meister_rtb_ids,
                                                 no_pre_cache_token=False, ads_retry_mode='meister')
        if info['is_hbp_responded_200']:
            ext = info['ext']
            assert_keys_not_exist(ext, 'exp_win_ttl')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3508 [COPPA] read coppa flag from realtime token and process it with realtime case')
    @allure.description('Verify coppa=1 in bidrequest when no coppa in realtime token but setting in dash')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_token_coppa_01(self, pub_app_id, placement, sdk_v, partner):
        """

             App level setting:
             "isCoppaCompliant": true

        """
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload)
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_request['regs']['coppa'], equal_to(1))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3508 [COPPA] read coppa flag from realtime token and process it with realtime case')
    @allure.description('Verify coppa=1 in bidrequest when is_coppa=True in realtime token and setting in dash')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_token_coppa_02(self, pub_app_id, placement, sdk_v, partner):
        """

             App level setting:
             "isCoppaCompliant": true

        """
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=hb_meister_rtb_ids,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload)
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_request['regs']['coppa'], equal_to(1))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3508 [COPPA] read coppa flag from realtime token and process it with realtime case')
    @allure.description('Verify no coppa in bidrequest when is_coppa=False in realtime token and setting in dash')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_token_coppa_03(self, pub_app_id, placement, sdk_v, partner):
        """

             App level setting:
             "isCoppaCompliant": true

        """
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                rtb=ext1_non_test_mode_kraken_rtb_ids_vast,
                                                explain=True, coppa=False, override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload)
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3508 [COPPA] read coppa flag from realtime token and process it with realtime case')
    @allure.description('Verify no coppa in bidrequest when no coppa in realtime and  setting is_coppa=false in dash')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', [common_test_real_time_no_coppa_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_token_coppa_04(self, pub_app_id, placement, sdk_v, partner):
        """

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": false

        """
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, rtb=ext1_non_test_mode_kraken_rtb_ids_vast,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload)
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3508 [COPPA] read coppa flag from realtime token and process it with realtime case')
    @allure.description('Verify coppa =1 in bidrequest when is_coppa=true in realtime and is_coppa=false in dash')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', [common_test_real_time_no_coppa_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_token_coppa_05(self, pub_app_id, placement, sdk_v, partner):
        """

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": false

        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext1_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload)
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_request['regs']['coppa'], equal_to(1))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3508 [COPPA] read coppa flag from realtime token and process it with realtime case')
    @allure.description('Verify coppa =1 in bidrequest when is_coppa=false in realtime and is_coppa=false in dash')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', [common_test_real_time_no_coppa_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_token_coppa_06(self, pub_app_id, placement, sdk_v, partner):
        """

        App level setting:
        "isCoppaCompliant": false

        Placement level setting:
        "is_coppa": false

        """
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext1_non_test_mode_kraken_rtb_ids_vast,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload)
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_keys_not_exist(bid_request['regs'], 'coppa')
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm['rendering_data']), 'adunit')
                assert_keys_exist(str_to_json(adm['rendering_data']), 'impression')
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))
                assert_keys_exist(str_to_json(adm), 'adunit')
                assert_keys_exist(str_to_json(adm), 'impression')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal')
    @allure.story('PBJ-3901 Set floor to be at $0.5 cent for LiftOff DSP')
    @allure.description('Verify bid floor is $0.5 for the real-time traffic via the LO eDSP RTB')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('oridinal_view', [11])
    def test_real_time_liftoff_bid_floor_1(self, pub_app_id, placement, sdk_v, partner, oridinal_view):
        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ads_retry_mode='kraken',
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'],
                                                               ext_non_test_mode_kraken_rtb_ids_vast_liftoff)

            assert_that(bid_request['imp'][0]['bidfloor'], equal_to(0.5))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3935 HBP - Fix hb realtime crash when request device extension does not exist')
    @allure.description('Verify hbp can work well for no device extension exists via windows platform')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_realtime_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [None])
    def test_hbp_realtime_work_for_none_device_ext_1(self, pub_app_id, placement, sdk_v, partner, oridinal_view,
                                                     coppa):

        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, coppa=coppa, platform='windows',
                                                ads_retry_mode='meister', config_extension=config_extension_RTA)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner != 'admob':
                assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3158 Real-time Ad Test - Req 8 - Test for passing ordinal view to Meister')
    @allure.description('Verify hbp can work well for device extension exists via windows')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_ad_ordinal_view_real_time_only_for_device_ext_2(self, pub_app_id, placement, sdk_v, partner,
                                                                       oridinal_view,
                                                                       coppa):
        test_device_id = gen_device_id()
        device_ext = {
            "locale": "en-US",
            "msaid": "3e09bc404f16b2e32de056b8216388c7",
            "ashwid": test_device_id,
            "language": "en",
            "connection_type": "wifi",
            "battery_state": "Discharging",
            "battery_saver_enabled": 0,
            "battery_level": 0.66,
            "storage_bytes_available": 782966620160,
            "time_zone": "America/Los_Angeles",
            "os_name": "WINDOWS"
        }

        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=test_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, coppa=coppa, platform='windows',
                                                device_ext=device_ext, ads_retry_mode='meister',
                                                config_extension=config_extension_RTA)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3158 Real-time Ad Test - Req 8 - Test for passing ordinal view to Meister')
    @allure.description('Verify hbp can work well for null device extension')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('oridinal_view', [11])
    @pytest.mark.parametrize('coppa', [None])
    def test_real_time_ad_ordinal_view_real_time_only_null_device_ext_2(self, pub_app_id, placement, sdk_v, partner,
                                                                        oridinal_view,
                                                                        coppa):
        test_device_id = gen_device_id()
        device_ext = {

        }

        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=test_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, coppa=coppa, platform='windows',
                                                device_ext=device_ext, ads_retry_mode='meister',
                                                config_extension=config_extension_RTA)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner != 'admob':
                assert_keys_exist(response_payload, 'seatbid')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3939 HB - Realtime failed to return bid for first time request')
    @allure.description('Verify the max real-time bid request can be served normally if ordinal view count is 1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('oridinal_view', [1])
    @pytest.mark.parametrize('no_pre_cache_token', [True, False])
    def test_real_time_ad_ordinal_view_real_time_only_max(self, pub_app_id, placement, sdk_v, partner, oridinal_view,
                                                          no_pre_cache_token):
        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=no_pre_cache_token, explain=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_keys_exist(idsp_bid_request['app']['ext']['vungle'], 'hb_ordinal')
            hb_ordinal = idsp_bid_request['app']['ext']['vungle']['hb_ordinal']

            assert_that(hb_ordinal, equal_to(oridinal_view))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3939 HB - Realtime failed to return bid for first time request')
    @allure.description('Verify the max real-time bid request can be served normally if ordinal view count is 1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('oridinal_view', [1])
    def test_real_time_ad_ordinal_view_hybrid_max(self, pub_app_id, placement, sdk_v, partner, oridinal_view):
        info = request_hbp_with_real_time_token(partner, oridinal_view, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            idsp_bid_request = get_bid_request_obj_from_hbp_explain(info['hbp_response'], hb_meister_rtb_ids)
            assert_keys_exist(idsp_bid_request['app']['ext']['vungle'], 'hb_ordinal')
            hb_ordinal = idsp_bid_request['app']['ext']['vungle']['hb_ordinal']

            assert_that(hb_ordinal, equal_to(oridinal_view))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4069- [AdMob Open Bidding] Investigate why the bidder is returning 4XX error to Google')
    @allure.description('Verify jaeger should not return 400 when request header contain \'charset=utf-8\'')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_header_contain_utf8(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=11, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, Content_Type_uft8=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4079 Change HBP bidID from uuid to objectID'
                  'PBJ-4110 Sync the change of ordinalMax = 16 to the Jaeger side on real-time bidding')
    @allure.description('Verify prase event token for v3 works well')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_decode_event_token_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=False)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_notification_token = bid_info['ext']['event_notification_token']['payload']
            decode_info = decode_admob_event_token(event_notification_token)
            ext = decode_ext(url=bid_info['burl'])
            assert_that(ext['appid'], equal_to(pub_app_id))
            assert_that(ext['prid'], equal_to(placement))
            assert_that(decode_info["adv_is_internal"], equal_to(ext['internal']))
            assert_that(decode_info["bidid"], equal_to(ext['bid']))
            assert_that(decode_info["event_id"], equal_to(ext['id']))
            assert_that(decode_info["pub_app_obj_id"], equal_to(ext['appid']))
            assert_that(decode_info["n_ordinal_view"], equal_to(16))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4114 Fix admob notification old style pubappId'
                  'PBJ-4110 Sync the change of ordinalMax = 16 to the Jaeger side on real-time bidding')
    @allure.description('Verify prase event token for v3 works well with the old style pub app id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_decode_event_token_2(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_notification_token = bid_info['ext']['event_notification_token']['payload']
            decode_info = decode_admob_event_token(event_notification_token)
            ext = decode_ext(url=bid_info['burl'])
            assert_that(ext['appid'], equal_to(pub_app_id))
            assert_that(ext['prid'], equal_to(placement))
            assert_that(decode_info["adv_is_internal"], equal_to(ext['internal']))
            assert_that(decode_info["bidid"], equal_to(ext['bid']))
            assert_that(decode_info["event_id"], equal_to(ext['id']))
            assert_that(decode_info["pub_app_obj_id"], is_not(ext['appid']))
            assert_that(decode_info["n_ordinal_view"], equal_to(16))

    @allure.feature('hbp')
    @allure.tag('normal')
    @allure.story('PBJ-4064 Wooga/Playtika in house app bidding - no bid')
    @allure.description('Verify hbp error message for request with invalid imp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_invalid_imp_for_real_time(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, imp=None)
        response_paybload = info['hbp_response']
        # nbr = 4 means NO_BID_INVALID_REQUEST
        assert_that(response_paybload['nbr'], equal_to(2))
        assert_that(response_paybload['ext']['err_msg'], equal_to("4: NSR: NO_SERV_REQUEST_VALIDATION_ERROR"))

    @allure.feature('hbp')
    @allure.tag('normal')
    @allure.story('PBJ-4064 Wooga/Playtika in house app bidding - no bid')
    @allure.description('Verify hbp error message for request with invalid imp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_invalid_imp_for_real_time(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, imp=None, compress='gzip')
        response_paybload = info['hbp_response']
        # nbr = 4 means NO_BID_INVALID_REQUEST
        assert_that(response_paybload['nbr'], equal_to(2))
        assert_that(response_paybload['ext']['err_msg'], equal_to("4: NSR: NO_SERV_REQUEST_VALIDATION_ERROR"))

    @allure.feature('hbp')
    @allure.tag('normal')
    @allure.story('PBJ-4203 Correct bid_nsr value in case of not found bid token'
                  'PBJ-4481 Jaeger - Sync HBP changes')
    @allure.description('Verify bid_nsr=8 when request precache with no precache token in v3 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_nsr_null_bid_token(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True)
        response_paybload = info['hbp_response']
        # nbr = 8 means NO_SERV_NO_BID_TOKENS
        # also check hb-transactions
        assert_that(response_paybload['ext']['err_msg'], equal_to("8: NSR: NO_SERV_NO_BID_TOKENS"))

    @allure.feature('hbp')
    @allure.tag('normal')
    @allure.story('PBJ-4481 Jaeger - Sync HBP changes')
    @allure.description('Verify bid_nsr=8 when request with invalid precache tokens')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('precache_tokens', [['2|TXlVjw==|']])
    def test_nsr_invalid_precache_bid_token(self, pub_app_id, placement, sdk_v, partner, precache_tokens):
        token_json = request_payload.real_time_token_json(pre_cached_tokens=precache_tokens, orinal_view=11,
                                                          sdk_user_agent=sdk_v)
        super_token_v3 = encode_real_time_token(token_json)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_device_id,
                                          bid_token=super_token_v3)
        r = post(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug='jaeger',
                                                                    rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_paybload = r.json()
        # nbr = 20 means  NO_SERV_FAILED_TO_GET_BIDTOKEN
        # also check hb-transactions
        assert_that(response_paybload['ext']['err_msg'], equal_to("20: NSR: NO_SERV_FAILED_TO_GET_BIDTOKEN"))

    @allure.feature('hbp')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4158 [AdMob Bidding] Investigate Real-Time bid token issue')
    @allure.description('Verify crid field is responsed via kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_crid_is_responsed_for_kraken_test_mode(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=test_mode_device_id,
                                                sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False,
                                                rtb=test_mode_kraken_int2_rtb_ids,
                                                override_bid_response_any=override_bid_response_any
                                                )
        response_paybload = info['hbp_response']
        bid = response_paybload["seatbid"][0]['bid'][0]
        assert_keys_exist(bid, 'crid')

    @allure.feature('hbp')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4158 [AdMob Bidding] Investigate Real-Time bid token issue')
    @allure.description('Verify crid field is responsed via kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_crid_is_responsed_for_kraken(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                )
        response_paybload = info['hbp_response']
        bid = response_paybload["seatbid"][0]['bid'][0]
        assert_keys_exist(bid, 'crid')

    @allure.feature('hbp')
    @allure.tag('normal')
    @allure.story('PBJ-4158 Add supply name to the BFlat features')
    @allure.description('Verify \'supply name\' to the blfat for precache placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_supply_name_pass_to_bflat_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True,
                                                rtb=meister_rtb_ids,
                                                )
        response_paybload = info['hbp_response']
        # check supply name in bflat bid_request

    @allure.feature('hbp')
    @allure.tag('normal')
    @allure.story('PBJ-4158 Add supply name to the BFlat features')
    @allure.description('Verify \'supply name\' to the blfat for precache placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_supply_name_pass_to_bflat_2(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                rtb=meister_rtb_ids,
                                                )
        response_paybload = info['hbp_response']
        # check supply name in bflat bid_request

    @allure.feature('hbp')
    @allure.tag('normal')
    @allure.story('PBJ-4210 Real-time request via eDSP should request to Bflat to get the bid price')
    @allure.description('Verify \'supply name\' to the blfat for precache placement via edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_supply_name_pass_to_bflat_3_e(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                )
        response_paybload = info['hbp_response']
        # check supply name in bflat bid_request

    @allure.feature('hbp')
    @allure.tag('normal')
    @allure.story('PBJ-4210 Real-time request via eDSP should request to Bflat to get the bid price')
    @allure.description('Verify \'supply name\' to the blfat for precache placement via edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_supply_name_pass_to_bflat_4_e(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                )
        response_paybload = info['hbp_response']
        # check supply name in bflat bid_request

    @allure.feature('event token')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4229 Add impType & os name for win rate metric for admob')
    @allure.description('Verify event token include the imp type for admob on test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_admob_event_token_include_imp_type_r_01(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                override_bid_response_any=override_bid_response_any
                                                )
        bid = info['hbp_response']['seatbid'][0]['bid'][0]
        event_token = bid['ext']['event_notification_token']['payload']
        decode_event_token = get(hbp_admob_event_token_decoder_qa + '?token=' + event_token)
        assert_response_status_code(decode_event_token.status_code, HTTPStatus.OK)
        decode_info = decode_event_token.json()
        assert_that(decode_info['impression_type'], equal_to('video'))

    @allure.feature('event token')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4229 Add impType & os name for win rate metric for admob')
    @allure.description('Verify event token include the imp type for admob on test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement,
                                           common_test_pre_cache_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_admob_event_token_include_imp_type_r_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_token = bid_info['ext']['event_notification_token']['payload']
            decode_event_token = get(hbp_admob_event_token_decoder_qa + '?token=' + event_token)
            assert_response_status_code(decode_event_token.status_code, HTTPStatus.OK)
            decode_info = decode_event_token.json()
            assert_that(decode_info['impression_type'], equal_to('banner'))

    @allure.feature('2nd highest price')
    @allure.tag('smoke')
    @allure.story('PBJ-4300 Look into if MAX & IS pass min_bid_to_win for the 2nd highest price on IAB auction')
    @allure.description('Verify record the 2nd highest price in notification for realtime')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    def test_admon_2nd_highest_price_real_time(self, pub_app_id, placement):
        info = request_realtime_win_notification("admob", 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=test_default_real_time_sdk_version,
                                                 no_pre_cache_token=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            # Verifiy that "second_highest_bid_price" has been recorded in hb notifications.

    @allure.feature('2nd highest price')
    @allure.tag('smoke')
    @allure.story('PBJ-4300 Look into if MAX & IS pass min_bid_to_win for the 2nd highest price on IAB auction')
    @allure.description('Verify record the 2nd highest price in notification for precache placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    def test_admob_2nd_highest_price_precache(self, pub_app_id, placement):
        info = request_realtime_win_notification("admob", 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v="Vungle/6.11.1",
                                                 no_pre_cache_token=False)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            # Verifiy that "second_highest_bid_price" has been recorded in hb notifications.

    @allure.feature('2nd highest price')
    @allure.tag('smoke')
    @allure.story('PBJ-4300 Look into if MAX & IS pass min_bid_to_win for the 2nd highest price on IAB auction')
    @allure.description('Verify record the 2nd highest price in notification for max')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    def test_max_2nd_highest_price_real_time(self, pub_app_id, placement):
        info = request_realtime_win_notification("max", 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v=test_default_real_time_sdk_version,
                                                 no_pre_cache_token=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            # Verifiy that "second_highest_bid_price=5.3" has been recorded in hb notifications.

    @allure.feature('2nd highest price')
    @allure.tag('smoke')
    @allure.story('PBJ-4300 Look into if MAX & IS pass min_bid_to_win for the 2nd highest price on IAB auction')
    @allure.description('Verify record the 2nd highest price in notification for max')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    def test_max_2nd_highest_price_precache(self, pub_app_id, placement):
        info = request_realtime_win_notification("max", 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=gen_device_id(), sdk_v="Vungle/6.11.1",
                                                 no_pre_cache_token=False)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            # Verifiy that "second_highest_bid_price=5.3" has been recorded in hb notifications.

    @allure.feature('2nd highest price')
    @allure.tag('smoke', 'test_mode')
    @allure.story('PBJ-4300 Look into if MAX & IS pass min_bid_to_win for the 2nd highest price on IAB auction')
    @allure.description('Verify record the 2nd highest price in notification for max')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    def test_max_2nd_highest_price_real_time_t(self, pub_app_id, placement):
        info = request_realtime_win_notification("max", 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                 test_device_id=test_mode_device_id, sdk_v=test_default_real_time_sdk_version,
                                                 no_pre_cache_token=True, rtb=ext1_test_mode_kraken_rtb_ids_mraid)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            # Verifiy that "second_highest_bid_price=5.3" has been recorded in hb notifications.

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.255.0')
    @allure.story('PBJ-4373 Jaeger - Add declared_ad for admob for ad quality'
                  'PBJ-5175 Look into RTA experiment Low performance issue')
    @allure.description('Verify declared_ad.video_url attribution is added in bid response for admob'
                        'Remove declared_ad for admob')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_admob_declared_ad_01(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            sdk_rendered_ad = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
            assert_keys_exist(sdk_rendered_ad, 'declared_ad')
            assert_keys_exist(sdk_rendered_ad['declared_ad'], 'video_url')
            assert_that(isinstance(sdk_rendered_ad['declared_ad']['video_url'], str))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'test_mode', 'v1.255.0')
    @allure.story('PBJ-4373 Jaeger - Add declared_ad for admob for ad quality'
                  'PBJ-5175 Look into RTA experiment Low performance issue')
    @allure.description('Verify declared_ad.video_url attribution is added in bid response for admob'
                        'Remove declared_ad for admob')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_admob_declared_ad_idsp_01(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=test_mode_kraken_rtb_ids,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            sdk_rendered_ad = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
            assert_keys_not_exist(sdk_rendered_ad, 'declared_ad')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.255.0')
    @allure.story('PBJ-4373 Jaeger - Add declared_ad for admob for ad quality'
                  'PBJ-5175 Look into RTA experiment Low performance issue')
    @allure.description('Verify declared_ad.video_vast_xml attribution is added in bid response for admob'
                        'Remove declared_ad for admob')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_admob_declared_ad_02(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            sdk_rendered_ad = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
            assert_keys_not_exist(sdk_rendered_ad, 'declared_ad')

    # @allure.feature('real-time ad')
    # @allure.tag('normal')
    # @allure.story('PBJ-4373 Jaeger - Add declared_ad for admob for ad quality')
    # @allure.description('Verify declared_ad.html_snippet attribution is added in bid response for admob')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_mrec_placement])
    # @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', ['admob'])
    # def test_real_time_admob_declared_ad_03(self, pub_app_id, placement, sdk_v, partner):
    #     override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
    #                                             explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
    #                                             override_bid_response_any=override_bid_response_any)
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
    #         sdk_rendered_ad = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
    #         assert_keys_exist(sdk_rendered_ad, 'declared_ad')
    #         assert_keys_exist(sdk_rendered_ad['declared_ad'], 'html_snippet')
    #         assert_that(isinstance(sdk_rendered_ad['declared_ad']['html_snippet'], str))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.255.0')
    @allure.story('PBJ-4560 Native Bidding is returning an internal error'
                  'PBJ-5175 Look into RTA experiment Low performance issue')
    @allure.description('Verify native bidding should not return error for admob'
                        'Remove declared_ad for admob')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_native_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_admob_declared_ad_native_edsp(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext1_non_test_mode_kraken_rtb_ids_vast,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            sdk_rendered_ad = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
            assert_keys_not_exist(sdk_rendered_ad, 'declared_ad')


    # @allure.feature('real-time ad')
    # @allure.tag('normal')
    # @allure.story('PBJ-4560 Native Bidding is returning an internal error')
    # @allure.description('Verify native bidding should not return error for admob')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_native_placement])
    # @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', ['admob'])
    # def test_real_time_admob_declared_ad_native_idsp(self, pub_app_id, placement, sdk_v, partner):
    #     override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
    #                                             explain=True, coppa=True, rtb=meister_rtb_ids,
    #                                             override_bid_response_any=override_bid_response_any)
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
    #         sdk_rendered_ad = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
    #         assert_keys_exist(sdk_rendered_ad, 'declared_ad')
    #         assert_keys_exist(sdk_rendered_ad['declared_ad'], 'native_response')
    #         assert_that(isinstance(sdk_rendered_ad['declared_ad']['native_response'], object))



    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4373 Jaeger - Add declared_ad for admob for ad quality')
    @allure.description('Verify declared_ad.html_snippet attribution is added in bid response for admob')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_admob_declared_ad_precache(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            sdk_rendered_ad = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
            assert_keys_not_exist(sdk_rendered_ad, 'declared_ad')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.174.0')
    @allure.story('PBJ-3044 Implement DDL strategy for real-time bidding')
    @allure.description('Verify the ddl will not be added without requesting sdk notification')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_ddl_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_ddl_1(self, pub_app_id, placement, partner):
        '''
            placement:
            daily_delivery_limit = 1
        '''
        if env == 'qa' or env == 'regression':
            test_ifa = gen_device_id()
            info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                    test_device_id=test_ifa, no_pre_cache_token=True)
            if info['is_hbp_responded_200']:
                response_payload = info['hbp_response']
                assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

                info_1 = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id,
                                                          placement_ref_id=placement,
                                                          test_device_id=test_ifa, no_pre_cache_token=True)

                if info_1['is_hbp_responded_200']:
                    response_payload = info_1['hbp_response']
                    assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.174.0')
    @allure.story('PBJ-3044 Implement DDL strategy for real-time bidding')
    @allure.description('Verify the ddl will be added with requesting sdk notification')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_ddl_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_ddl_2(self, pub_app_id, placement, partner):
        """
            placement:
            daily_delivery_limit = 1
        """
        if env == 'qa' or env == 'regression':
            test_ifa = gen_device_id()
            info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                    test_device_id=test_ifa, no_pre_cache_token=True)
            if info['is_hbp_responded_200']:
                response_payload = info['hbp_response']
                assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

                if partner == 'admob':
                    adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                    adunit = str_to_json(adm['rendering_data'])['adunit']
                else:
                    adm = response_payload['seatbid'][0]['bid'][0]['adm']
                    adunit = str_to_json(adm)['adunit']

                jaeger_response = decode_real_time_adunit(adunit)
                sdk_notification_url = jaeger_response['ads'][0]['ad_markup']['notification'][0]

                r = get(sdk_notification_url)
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                sleep(1)

                info_1 = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id,
                                                          placement_ref_id=placement,
                                                          test_device_id=test_ifa, no_pre_cache_token=True)

                assert_that(info_1['is_hbp_responded_200'], equal_to(False))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.92.0')
    @allure.story('PBJ-4425 HBP - Log bid request fields from mediation partner to hbp transactions'
                  'PBJ-4459 Jaeger - Change interface{} to string in hb transaction message')
    @allure.description('Verify log bid request fields to hbp transaction')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement, common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_log_request_fields_01(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # assert_that(isinstance(hbp_transaction['bidrequest_device_lmt'], bool))
            # assert_that(isinstance(hbp_transaction['bidrequest_device_dnt'], bool))
            # assert_that(isinstance(hbp_transaction['bidrequest_device_ext'], str))
            # assert_that(isinstance(hbp_transaction['bidrequest_regs'], str))
            # if partner == 'max':
            #     assert_that(isinstance(hbp_transaction['bidrequest_user_ext'], str))
            #     assert_that(isinstance(hbp_transaction['bidrequest_device_carrier'], str))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.92.0')
    @allure.story('PBJ-4425 HBP - Log bid request fields from mediation partner to hbp transactions'
                  'PBJ-4459 Jaeger - Change interface{} to string in hb transaction message')
    @allure.description('Verify log bid request fields to hbp transaction')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_log_request_fields_precache(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # assert_that(isinstance(hbp_transaction['bidrequest_device_lmt'], bool))
            # assert_that(isinstance(hbp_transaction['bidrequest_device_dnt'], bool))
            # assert_that(isinstance(hbp_transaction['bidrequest_device_ext'], str))
            # assert_that(isinstance(hbp_transaction['bidrequest_regs'], str))
            # if partner == 'max':
            #     assert_that(isinstance(hbp_transaction['bidrequest_user_ext'], str))
            #     assert_that(isinstance(hbp_transaction['bidrequest_device_carrier'], str))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.92.0')
    @allure.story('PBJ-4400 [HAProxy][HBP] Read request header and add to metrics')
    @allure.description('Verify X-Source, X-Env add in request header')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('header_dimension_source', ['', 'haproxy', 'akamai'])
    @pytest.mark.parametrize('header_dimension_env', ['', 'qa', 'stage', 'prod'])
    def test_real_time_header_source(self, pub_app_id, placement, sdk_v, partner, header_dimension_source,
                                     header_dimension_env):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                source=header_dimension_source, x_env=header_dimension_env)
        assert_that(info['is_hbp_responded_200'], equal_to(True))
        # Verify the dimension has record in signalFX 'ssp_hbp_http_request_duration_seconds_bucket '

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.92.0')
    @allure.story('PBJ-4400 [HAProxy][HBP] Read request header and add to metrics')
    @allure.description('Verify X-Source, X-Env add in request header')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('header_dimension_source', ['', 'haproxy', 'akamai'])
    @pytest.mark.parametrize('header_dimension_env', ['', 'qa', 'stage', 'prod'])
    def test_real_time_header_source_01(self, pub_app_id, placement, sdk_v, partner, header_dimension_source,
                                        header_dimension_env):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                source=header_dimension_source, x_env=header_dimension_env)
        assert_that(info['is_hbp_responded_200'], equal_to(True))
        # Verify the dimension has record in signalFX 'ssp_hbp_http_request_duration_seconds_bucket '

    @allure.feature('gzip')
    @allure.tag('normal', 'v0.92.0')
    @allure.story('PBJ-4380 HBP bidrequest always get a 204')
    @allure.description('Verify hbp request with gzip bid request will response successfully')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_gzip_request(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                compress='gzip', post_retry=False)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid['adm'], is_not(empty()))
        else:
            assert False

    @allure.feature('gzip')
    @allure.tag('normal', 'v0.92.0')
    @allure.story('PBJ-4380 HBP bidrequest always get a 204')
    @allure.description('Verify hbp request without gzip bid request will response successfully')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_not_gzip_request(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                compress=None, post_retry=False)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid['adm'], is_not(empty()))
        else:
            assert False

    @allure.feature('gzip')
    @allure.tag('normal', 'v0.92.0')
    @allure.story('PBJ-4380 HBP bidrequest always get a 204')
    @allure.description('Verify hbp request with gzip bid request will response successfully')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('compress', [None, 'gzip'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_gzip_request_precache(self, pub_app_id, placement, sdk_v, partner, compress):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                post_retry=False, compress=compress)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid['adm'], is_not(empty()))
        else:
            assert False

    @allure.feature('gzip')
    @allure.tag('normal', 'v0.94.0')
    @allure.story('PBJ-4463 Correct Content-Length header field in gzip middleware')
    @allure.description('Verify HBP response body size should match the Content-Length field value if it exists.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('compress', ['gzip'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_contentLength_match_gzip_body_size(self, pub_app_id, placement, sdk_v, partner, compress):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=False, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                post_retry=False, compress=compress, stream=True)

        if info['is_hbp_responded_200']:

            response_payload = info['hbp_response']
            response_headers = info['hbp_response_headers']
            content_length = response_headers['Content-Length']
            gzip_body_length = info['gzip_length']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(math.isclose(int(content_length), int(gzip_body_length), abs_tol=20))

        else:
            assert False

    @allure.feature('hbp transaction')
    @allure.tag('normal', 'v0.93.0')
    @allure.story('PBJ-4419 add fields to hb-transactions topic for DS')
    @allure.description('Verify fields has been added to hb-tranactions for realtime placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_add_fields_to_hb_transaction_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                post_retry=False)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid['adm'], is_not(empty()))
        # Verify that 'recommender_tag' field is added to hb-transaction for eDSP.

    @allure.feature('hbp transaction')
    @allure.tag('normal', 'v0.93.0')
    @allure.story('PBJ-4419 add fields to hb-transactions topic for DS')
    @allure.description('Verify fields has been added to hb-tranactions for realtime placement'
                        'PBJ-4428 Pass “is_dynamic_rate” to bflat')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_add_fields_to_hb_transaction_2(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                post_retry=False)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid['adm'], is_not(empty()))
        # Verify that 'recommender_tag', 'campaign_rate_type', 'is_dynamic_rate' fields are added to hb-transaction
        # for iDSP.

    @allure.feature('hbp transaction')
    @allure.tag('normal', 'v0.93.0')
    @allure.story('PBJ-4419 add fields to hb-transactions topic for DS')
    @allure.description('Verify fields has been added to hb-tranactions for realtime placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_add_fields_to_hb_transaction_3(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                post_retry=False)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid['adm'], is_not(empty()))
        # Verify that 'recommender_tag', 'campaign_rate_type', 'is_dynamic_rate' fields are added to hb-transaction
        # for iDSP.

    @allure.feature('hbp transaction')
    @allure.tag('normal', 'v0.93.0')
    @allure.story('PBJ-4419 add fields to hb-transactions topic for DS'
                  'PBJ-4428 Pass “is_dynamic_rate” to bflat')
    @allure.description('Verify fields has been added to hb-tranactions for realtime placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_add_fields_to_hb_transaction_4(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                post_retry=False)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid['adm'], is_not(empty()))
        # Verify that 'recommender_tag' field is added to hb-transaction for eDSP.
        # Verify that 'is_dynamic_rate' pass to Bflat feature object.

    @allure.feature('hbp transaction')
    @allure.tag('normal', 'test_mode', 'v0.93.0')
    @allure.story('PBJ-4419 add fields to hb-transactions topic for DS')
    @allure.description('Verify fields has been added to hb-tranactions for realtime placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('rtb_ids', [ext_test_mode_kraken_rtb_ids_vast, test_mode_kraken_rtb_ids])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_add_fields_to_hb_transaction_5(self, pub_app_id, placement, sdk_v, partner, rtb_ids):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb_ids,
                                                post_retry=False)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid['adm'], is_not(empty()))
        # Verify that 'recommender_tag' field is added to hb-transaction for eDSP.
        # Verify that 'recommender_tag', 'campaign_rate_type', 'is_dynamic_rate' fields are added to hb-transaction
        # for iDSP.
        #  Verify sdk_version is added to hb-transaction realtime mode (PBJ-4422)

    @allure.feature('hbp transaction')
    @allure.tag('normal')
    @allure.story('PBJ-4454 Many hbp transactions have max_bid_price = 5.0')
    @allure.description('Verify max_bid_price= 2000 for edsp for precache V3 token')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_max_bid_price_01(self, pub_app_id, placement, sdk_v, partner):
        override_bid_price = 'seatbid.0.bid.0.price@10000'
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                post_retry=False, override_bid_response_any=override_bid_price)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid['adm'], is_not(empty()))
            assert_that(bid['price'] > 5)
            #  Verify sdk_version is added to hb-transaction precache mode (PBJ-4422)
        # Verify that 'max_bid_price = 2000 for edsp.

    @allure.feature('hbp transaction')
    @allure.tag('normal')
    @allure.story('PBJ-4454 Many hbp transactions have max_bid_price = 5.0')
    @allure.description('Verify max_bid_price= 200 for idsp for precache V3 token')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_max_bid_price_02(self, pub_app_id, placement, sdk_v, partner):
        override_bid_price = 'seatbid.0.bid.0.price@10000'
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                post_retry=False, override_bid_response_any=override_bid_price)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid['adm'], is_not(empty()))
            assert_that(bid['price'] > 5)
        # Verify that 'max_bid_price = 200 for idsp.

    @allure.feature('real time')
    @allure.tag('normal')
    @allure.story('PBJ-4529 [Jaeger] Select correct experiment number for banner traffic.')
    @allure.description('Verify select banner experiment for banner traffic for realtime mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_choose_banner_exp_for_banner_placement_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, banner=True,
                                                explain=True, coppa=True, rtb=ext1_non_test_mode_kraken_rtb_ids_vast,
                                                post_retry=False)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

        #  extra_data={'experiment_node_id': '$experiment_edsp_banner_0'}

    @allure.feature('real time')
    @allure.tag('normal')
    @allure.story('PBJ-4529 [Jaeger] Select correct experiment number for banner traffic.')
    @allure.description('Verify select banner experiment for banner traffic for realtime mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_choose_banner_exp_for_banner_placement_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, banner=True,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                post_retry=False)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

        #  extra_data={'experiment_node_id': '$experiment_edsp_banner_0'}
        #  Verify sdk_version is added to hb-transaction (PBJ-4422)

    @allure.feature('real time')
    @allure.tag('normal')
    @allure.story('PBJ-4437 Incorrect RecommenderTag setting of Recommender Request on realtime case')
    @allure.description('Verify recommenderTag on realtime mode for idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_recommenderTag_realtime_idsp(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                post_retry=False)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

        #  "recommender_tag":"datasci--blr_20210101_tpat_nostr_log_sgd_exploit_w_calibration--{\\"skan-model\\":null}--success--meister"

    @allure.feature('real time')
    @allure.tag('normal')
    @allure.story('PBJ-4437 Incorrect RecommenderTag setting of Recommender Request on realtime case')
    @allure.description('Verify recommenderTag on realtime mode for edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_recommenderTag_realtime_edsp(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, banner=True,
                                                explain=True, coppa=True, rtb=ext1_non_test_mode_kraken_rtb_ids_vast,
                                                post_retry=False)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

        #  recommender_tag":"dsp-60a277a5b3bbef2c0884d8bc" in hp transaction
        #  also verify pass to bflat

    @allure.feature('Google Api Integration')
    @allure.tag('smoke', 'test_mode')
    @allure.story('PBJ-4336 Google Creative API Integration - [Jaeger]Submit creative to Kafka topic')
    @allure.description('Verify kafka message write to topic successfully via idsp')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_google_api_integration_i(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=1,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            price = bid_response['price']
            adm = json.loads(bid_response['ext']['sdk_rendered_ad']['rendering_data'])
            # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that sumit ' key of
            # cr-rev-mk.<murmur3sum32 of ([rtbAccountID]_[creativeID]>, with the given TTL' to redis

            # send second time
            notification_token = response_payload['seatbid'][0]['bid'][0]['ext']['event_notification_token']['payload']
            # Send request
            request_hbp(partner, 1, status_code=1, notification_token=notification_token, post_retry=False,
                        ads_retry_mode='kraken', debug='jaeger')
            # Verify that does not submit message to kafka topic: ex-jaeger-admob-creatives and redis

    @allure.feature('Google Api Integration')
    @allure.tag('smoke', 'test_mode')
    @allure.story('PBJ-4336 Google Creative API Integration - [Jaeger]Submit creative to Kafka topic via edsp')
    @allure.description('Verify kafka message write to topic successfully')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_google_api_integration_e(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=0,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            price = bid_response['price']
            adm = json.loads(bid_response['ext']['sdk_rendered_ad']['rendering_data'])
            # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that sumit ' key of
            # cr-rev-mk.<murmur3sum32 of ([rtbAccountID]_[creativeID]>, with the given TTL' to redis

    @allure.feature('Google Api Integration')
    @allure.tag('smoke', 'test_mode')
    @allure.story('PBJ-4336 Google Creative API Integration - [Jaeger]Submit creative to Kafka topic via edsp')
    @allure.description('Verify kafka message write to topic successfullt')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_google_api_integration_not_write_topic_to_other_partners(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=0)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            # Verify that does not submit message to kafka topic: ex-jaeger-admob-creatives and redis

    @allure.feature('Google Api Integration')
    @allure.tag('smoke', 'test_mode')
    @allure.story('PBJ-4336 Google Creative API Integration - [Jaeger]Submit creative to Kafka topic via edsp')
    @allure.description('Verify kafka message write to topic successfully')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_google_api_integration_e_precache(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=False, explain=True, is_hb=partner,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=0)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            price = bid_response['price']
            adm = json.loads(bid_response['ext']['sdk_rendered_ad']['rendering_data'])
            # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that sumit ' key of
            # cr-rev-mk.<murmur3sum32 of ([rtbAccountID]_[creativeID]>, with the given TTL' to redis

    @allure.feature('Google Api Integration')
    @allure.tag('smoke')
    @allure.story('PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob '
                  'feedback')
    @allure.description('Verify redis key is correct when creative_status_code=7/131 via eDSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('creative_status_code', [7, 131])
    def test_google_api_integration_creative_status_7_131(self, pub_app_id, placement, sdk_v, partner,
                                                          creative_status_code):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s_%s"' % (creative_status_code, get_current_timestamp())
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=True, is_hb=partner,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=0,
                                                admob_status_code=creative_status_code,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            price = bid_response['price']
            adm = json.loads(bid_response['ext']['sdk_rendered_ad']['rendering_data'])
            # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that submit ' key: of
            # cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.ALL, with the TTL=32 min' to redis , value=1

    @allure.feature('Google Api Integration')
    @allure.tag('smoke')
    @allure.story('PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob '
                  'feedback')
    @allure.description('Verify redis key is correct when creative_status_code=7/131 via iDSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('creative_status_code', [7, 131])
    def test_google_api_integration_creative_status_7_131_i(self, pub_app_id, placement, sdk_v, partner,
                                                            creative_status_code):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s_%s"' % (
        creative_status_code, get_current_timestamp())
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                no_pre_cache_token=True, explain=True, is_hb=partner,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=0,
                                                admob_status_code=creative_status_code,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            price = bid_response['price']
            adm = json.loads(bid_response['ext']['sdk_rendered_ad']['rendering_data'])
            # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that submit ' key: of
            # cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.ALL, with the TTL=32 min' to redis , value=1

    @allure.feature('Google Api Integration')
    @allure.tag('smoke')
    @allure.story('PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob '
                  'feedback')
    @allure.description('Verify redis key is correct when creative_status_code=7/131 via precache')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('creative_status_code', [7, 131])
    def test_google_api_integration_creative_status_7_131_precache(self, pub_app_id, placement, sdk_v, partner,
                                                            creative_status_code):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                no_pre_cache_token=False, explain=True, is_hb=partner,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=0,
                                                admob_status_code=creative_status_code)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            price = bid_response['price']
            adm = json.loads(bid_response['ext']['sdk_rendered_ad']['rendering_data'])
            # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that submit ' key: of
            # cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.ALL, with the TTL=32 min' to redis , value=1




    @allure.feature('Google Api Integration')
    @allure.tag('smoke')
    @allure.story(
        'PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob feedback')
    @allure.description('Verify redis key is correct when creative_status_code=129/130/205/10 via eDSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('creative_status_code', [129, 130, 205, 10])
    def test_google_api_integration_creative_status_others_e(self, pub_app_id, placement, sdk_v, partner,
                                                             creative_status_code):

        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s_%s"' % (
            creative_status_code, get_current_timestamp())
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=True, is_hb=partner,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=0,
                                                admob_status_code=creative_status_code,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            price = bid_response['price']
            adm = json.loads(bid_response['ext']['sdk_rendered_ad']['rendering_data'])
            # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that submit ' key: of
            # cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.<Region>, with the TTL=168 hours' to redis
            # Note, 129 -> region=CHN; 130 -> region=RUS; others -> ALL, value=0

    @allure.feature('Google Api Integration')
    @allure.tag('smoke')
    @allure.story(
        'PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob feedback')
    @allure.description('Verify redis key is correct when creative_status_code=129/130/205/10 via iDSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('creative_status_code', [129])
    def test_google_api_integration_creative_status_others_i(self, pub_app_id, placement, sdk_v, partner,
                                                             creative_status_code):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCrid_%s_%s"' % (
            creative_status_code, get_current_timestamp())
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                no_pre_cache_token=True, explain=True, is_hb=partner,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=0,
                                                admob_status_code=creative_status_code,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            price = bid_response['price']
            adm = json.loads(bid_response['ext']['sdk_rendered_ad']['rendering_data'])
            # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that submit ' key: of
            # cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.<Region>, with the TTL=168 hours' to redis
            # Note, 129 -> region=CHN; 130 -> region=RUS; others -> ALL, value=0

    @allure.feature('Google Api Integration')
    @allure.tag('smoke')
    @allure.story(
        'PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob feedback')
    @allure.description('Verify redis key is correct when creative_status_code=129/130/205/10 via precache')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('creative_status_code', [129, 130, 205, 10])
    def test_google_api_integration_creative_status_others_precache(self, pub_app_id, placement, sdk_v, partner,
                                                             creative_status_code):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=False, explain=True, is_hb=partner,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=0,
                                                admob_status_code=creative_status_code)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            price = bid_response['price']
            adm = json.loads(bid_response['ext']['sdk_rendered_ad']['rendering_data'])
            # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that submit ' key: of
            # cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.<Region>, with the TTL=168 hours' to redis
            # Note, 129 -> region=CHN; 130 -> region=RUS; others -> ALL, value=0
    # --------------------------------------------deprecate google api integration--------------------------------------
    # @allure.feature('Google Api Integration')
    # @allure.tag('smoke')
    # @allure.story(
    #     'PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob feedback')
    # @allure.description('Verify no serve if cr-rev-res exsiting in redis')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', ['admob'])
    # @pytest.mark.parametrize('creative_status_code', [131, 7, 205, 10])
    # def test_google_api_integration_filter_01(self, pub_app_id, placement, sdk_v, partner,
    #                                                                 creative_status_code):
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             rtb=test_mode_kraken_rtb_ids,
    #                                             no_pre_cache_token=True, explain=True, is_hb=partner,
    #                                             test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=0,
    #                                             admob_status_code=creative_status_code,
    #                                             buyer_creative_id="5cd92b2661a35300113a8487_vunglece4ae2")
    #     if info['is_hbp_responded_200']:
    #         # if keys exist in redis, will not serve successfully
    #         response_payload = info['hbp_response']
    #         ext = response_payload['ext']
    #         assert_keys_exist(ext, 'err_msg')

    #
    # @allure.feature('Google Api Integration')
    # @allure.tag('smoke')
    # @allure.story(
    #     'PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob feedback')
    # @allure.description('Verify will serve for realtime placement if cr-rev-res exsiting in redis and '
    #                     'request ip is not CN or RUS')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', ['admob'])
    # @pytest.mark.parametrize('creative_status_code', [129, 130])
    # def test_google_api_integration_filter_02(self, pub_app_id, placement, sdk_v, partner,
    #                                                                 creative_status_code):
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             rtb=test_mode_kraken_rtb_ids,
    #                                             no_pre_cache_token=True, explain=True,
    #                                             test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=0,
    #                                             admob_status_code=creative_status_code,
    #                                             buyer_creative_id="5cd92b2661a35300113a8487_vunglece4ae2")
    #     if info['is_hbp_responded_200']:
    #         # if keys exist in redis, will serve successfully for precache ads
    #         response_payload = info['hbp_response']
    #         bid_response = response_payload['seatbid'][0]['bid'][0]
    #         assert_keys_exist(bid_response, 'price')


    #
    # @allure.feature('Google Api Integration')
    # @allure.tag('smoke')
    # @allure.story(
    #     'PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob feedback')
    # @allure.description('Verify will not serve for realtime placement if cr-rev-res exsiting in redis and '
    #                     'request ip is CN')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', ['admob'])
    # @pytest.mark.parametrize('creative_status_code', [129])
    # def test_google_api_integration_filter_03(self, pub_app_id, placement, sdk_v, partner,
    #                                                                 creative_status_code):
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             rtb=test_mode_kraken_rtb_ids,
    #                                             no_pre_cache_token=True, explain=True,
    #                                             test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=0,
    #                                             admob_status_code=creative_status_code, ip=cn_ip,
    #                                             buyer_creative_id="5cd92b2661a35300113a8487_vunglece4ae2")
    #     if info['is_hbp_responded_200']:
    #         # if keys exist in redis, and request ip is cn will not serve successfully.
    #         response_payload = info['hbp_response']
    #         ext = response_payload['ext']
    #         assert_keys_exist(ext, 'err_msg')

    # @allure.feature('Google Api Integration')
    # @allure.tag('smoke')
    # @allure.story(
    #     'PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob feedback')
    # @allure.description('Verify will not serve for realtime placement if cr-rev-res exsiting in redis and '
    #                     'request ip is ru')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # @pytest.mark.parametrize('partner', ['admob'])
    # @pytest.mark.parametrize('creative_status_code', [130])
    # def test_google_api_integration_filter_04(self, pub_app_id, placement, sdk_v, partner,
    #                                                                 creative_status_code):
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             rtb=test_mode_kraken_rtb_ids,
    #                                             no_pre_cache_token=True, explain=True,
    #                                             test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=0,
    #                                             admob_status_code=creative_status_code, ip=ru_ip,
    #                                             buyer_creative_id="5cd92b2661a35300113a8487_vunglece4ae2")
    #     if info['is_hbp_responded_200']:
    #         # if keys exist in redis, and request ip is ru will not serve successfully.
    #         response_payload = info['hbp_response']
    #         ext = response_payload['ext']
    #         assert_keys_exist(ext, 'err_msg')
    #


    @allure.feature('Google Api Integration')
    @allure.tag('smoke')
    @allure.story(
        'PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob feedback')
    @allure.description('Verify will serve for precache ads if cr-rev-res exsiting in redis')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('creative_status_code', [131, 7])
    def test_google_api_integration_filter_05(self, pub_app_id, placement, sdk_v, partner,
                                                                    creative_status_code):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                no_pre_cache_token=False, explain=True,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=0,
                                                admob_status_code=creative_status_code,
                                                buyer_creative_id="5cd92b2661a35300113a8487_vunglece4ae2")
        if info['is_hbp_responded_200']:
            # if keys exist in redis, will serve successfully for precache ads
            response_payload = info['hbp_response']
            bid_response = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_response, 'price')

    @allure.feature('real eDSP crid')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP in bid response')
    @allure.description('Verify pass real crid of edsp for non HB traffic via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_edsp_crid_realtime(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.cid@"realTimeCid"|||seatbid.0.bid.0.crid@"realTimeCrid"'
        if partner == 'admob':
            override_bid_response_any = 'seatbid.0.bid.0.cid@"realTimeCid_admob_%s"|||seatbid.0.bid.0.crid@"realTimeCrid_admob_%s"'%(
                get_current_timestamp(), get_current_timestamp()
            )
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid = response_payload['seatbid'][0]['bid'][0]
            if partner == 'admob':
                assert_that(bid['cid'], equal_to('92233720368'))
                assert_that('5cd92b2661a35300113a8487_realTimeCrid_admob' in bid['crid'])
            else:
                assert_that(bid['cid'], equal_to('5cd92b2661a35300113a8487_realTimeCid'))
                assert_that(bid['crid'], equal_to('5cd92b2661a35300113a8487_realTimeCrid'))

            # Validate jaeger transaction and hbp transaction

    @allure.feature('real eDSP crid')
    @allure.tag('normal')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP in bid response')
    @allure.description('Verify pass real crid of edsp for non HB traffic via non test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_edsp_crid_realtime_nt(self, pub_app_id, placement, sdk_v, partner):
        override_bid_response_any = 'seatbid.0.bid.0.cid@"realtimenontestmodecid"|||seatbid.0.bid.0.crid@"realtimenontestmodecrid"'
        if partner == 'admob':
            override_bid_response_any = 'seatbid.0.bid.0.cid@"realTimeCid_admob_%s"|||seatbid.0.bid.0.crid@"realTimeCrid_admob_%s"' % (
               get_current_timestamp(), get_current_timestamp()
            )
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid = response_payload['seatbid'][0]['bid'][0]
            # default cid and crid
            if partner == 'admob':
                assert_that(bid['cid'], equal_to('92233720368'))
                assert_that('5cd92b2661a35300113a8487_realTimeCrid_admob' in bid['crid'])
            else:
                assert_that(bid['cid'], equal_to('5cd92b2661a35300113a8487_realtimenontestmodecid'))
                assert_that(bid['crid'], equal_to('5cd92b2661a35300113a8487_realtimenontestmodecrid'))
            # Validate jaeger transaction and hbp transaction


    @allure.feature('real eDSP crid')
    @allure.tag('normal')
    @allure.story('PBJ-4572 Pass real creative ID of eDSP in bid response')
    @allure.description('Verify the campaign in ads response will not be impacted for iDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_edsp_crid_realtime_meister(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=meister_rtb_ids, ads_retry_mode='meister',
                                                no_pre_cache_token=False, explain=True,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid = response_payload['seatbid'][0]['bid'][0]
            # default cid and crid
            assert_that("_" not in bid['cid'])
            assert_that("_" not in bid['crid'])
            # Validate jaeger transaction and hbp transaction


    @allure.feature('real-time ad')
    @allure.tag('smoke', 'SDK 7.0', 'v1.236.0')
    @allure.story('PBJ-4679 SDK 7.0 - HB should always be pure realtime as no precache supported')
    @allure.description('Verify that jaeger will serve realtime ads for precache placement when sdk_v>7+')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_banner_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('precache_mode', [False, True])
    @pytest.mark.parametrize('coppa', [True])
    def test_sdk_7_serve_for_precache_placement(self, pub_app_id, placement, sdk_v, partner, coppa, precache_mode):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True,
                                                coppa=coppa, no_pre_cache_token=precache_mode)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))

            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))


    @allure.feature('real-time ad')
    @allure.tag('smoke', 'SDK 7.0', 'test_mode', 'v1.236.0')
    @allure.story('PBJ-4679 SDK 7.0 - HB should always be pure realtime as no precache supported')
    @allure.description('Verify that jaeger will serve realtime ads for precache placement when sdk_v>7+ via test mode')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_banner_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('coppa', [True])
    @pytest.mark.parametrize('precache_mode', [True, False])
    def test_sdk_7_serve_for_precache_placement_t(self, pub_app_id, placement, sdk_v, partner, coppa, precache_mode):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, banner=True,
                                                is_test=1, rtb=test_mode_kraken_rtb_ids,
                                                coppa=coppa, no_pre_cache_token=precache_mode)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(2))

            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['version'], equal_to(2))



    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.237.0')
    @allure.story('PBJ-4732 HBP Table Experiment Numbers not recording impressions & revenue')
    @allure.description('Verify \'carried_experiments\' field is added to hb-transactions')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_new_field_for_precache_01(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_1, ads_debug='jaeger')
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that carried_experiments exists with the parsed config extension
            # {"AutoCache_2022_Phase1":"AutoCache","KONAVerifyAB_4068":"KONAAB2"}



    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.237.0')
    @allure.story('PBJ-4732 HBP Table Experiment Numbers not recording impressions & revenue')
    @allure.description('Verify \'carried_experiments\' field is added to hb-transactions')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_new_field_for_realtime(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_1, ip=au_ip)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that carried_experiments exists with the parsed config extension
            # {"AutoCache_2022_Phase1":"AutoCache","KONAVerifyAB_4068":"KONAAB2"}



    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.237.0')
    @allure.story('PBJ-4732 HBP Table Experiment Numbers not recording impressions & revenue')
    @allure.description('Verify \'carried_experiments\' field is added to hb-transactions')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_new_field_for_hybird(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_1)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that carried_experiments exists with the parsed config extension
            # {"AutoCache_2022_Phase1":"AutoCache","KONAVerifyAB_4068":"KONAAB2"}


    @allure.feature('real-time ad')
    @allure.tag('normal', 'test_mode', 'v1.237.0')
    @allure.story('PBJ-4732 HBP Table Experiment Numbers not recording impressions & revenue')
    @allure.description('Verify \'carried_experiments\' field is added to hb-transactions')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_new_field_for_test_mode(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=ext_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_1)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that carried_experiments exists with the parsed config extension
            # {"AutoCache_2022_Phase1":"AutoCache","KONAVerifyAB_4068":"KONAAB2"}



    @allure.feature('real-time ad')
    @allure.tag('normal', 'test_mode', 'v1.237.0')
    @allure.story('PBJ-4732 HBP Table Experiment Numbers not recording impressions & revenue')
    @allure.description('Verify \'carried_experiments\' field is added to hb-transactions')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_new_field_for_meister(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                config_extension=config_extension_1)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that carried_experiments exists with the parsed config extension
            # {"AutoCache_2022_Phase1":"AutoCache","KONAVerifyAB_4068":"KONAAB2"}


    @allure.feature('real-time ad')
    @allure.tag('normal', 'test_mode', 'v1.237.0')
    @allure.story('PBJ-4732 HBP Table Experiment Numbers not recording impressions & revenue')
    @allure.description('Verify \'carried_experiments\' field not exist')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_new_field_not_exist(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                config_extension="")
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that carried_experiments does not exists"



    @allure.feature('no serve')
    @allure.tag('normal')
    @allure.story('PBJ-4799 Large amount of request with "null" ad type value')
    @allure.description('Verify no bid_token precache')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_no_serve_for_nsr_8(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                )
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # Verify that bidrequest_imp_type is added to hb-transactions-noserv"


    @allure.feature('no serve')
    @allure.tag('normal')
    @allure.story('PBJ-4799 Large amount of request with "null" ad type value')
    @allure.description('Verify no bid_token precache')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['test-placement'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_no_serve_for_no_placement(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                )
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # Verify that bidrequest_imp_type is added to hb-transactions-noserv"


    @allure.feature('no serve')
    @allure.tag('normal')
    @allure.story('PBJ-4799 Large amount of request with "null" ad type value')
    @allure.description('Verify no bid_token precache')
    @pytest.mark.parametrize('pub_app_id', ['test-app-no-serve'])
    @pytest.mark.parametrize('placement', ['test-placement'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_no_serve_for_no_app(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                )
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # Verify that bidrequest_imp_type is added to hb-transactions-noserv"


    @allure.feature('no serve')
    @allure.tag('normal')
    @allure.story('PBJ-4799 Large amount of request with "null" ad type value')
    @allure.description('Verify no bid_token precache')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_no_serve_for_not_match_test_mode(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_test_mode_kraken_rtb_ids_vast,
                                                is_test=0)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that bidrequest_imp_type is added to hb-transactions-noserv"


    @allure.feature('no serve')
    @allure.tag('normal')
    @allure.story('PBJ-4799 Large amount of request with "null" ad type value')
    @allure.description('Verify no bid_token precache')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_no_serve_for_None_imp_realtime(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext1_non_test_mode_kraken_rtb_ids_vast,
                                                is_test=0, imp=None)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that no bidrequest_imp_type in hb-transactions-noserv"


    @allure.feature('no serve')
    @allure.tag('normal')
    @allure.story('PBJ-4799 Large amount of request with "null" ad type value')
    @allure.description('Verify no bid_token precache')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_no_serve_for_None_imp_precache(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                is_test=0, imp=None)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # hbp_transaction = info['hbp_response']['ext']['debug']['hb-transaction']
            # Verify that no bidrequest_imp_type in hb-transactions-noserv"

    @allure.feature('real-time ad')
    @allure.tag('smoke')
    @allure.story('PBJ-5110 [Jaeger][Deprecate HBP] Sync bidcache for lower than 6.10 SDK HB requests')
    @allure.description('Verify tpat start will record cache in hbtoken redis below 6.10')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('coppa', [True])
    def test_record_cache_in_redis(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, coppa=coppa,
                                                no_pre_cache_token=False, ads_retry_mode='meister',
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            jaeger_response = info['ads_response']
            ad_markup = jaeger_response['ads'][0]['ad_markup']
            tpat = ad_markup['tpat']['checkpoint.0']
            for url in tpat:
                if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                    tpat_start_url = url
            time.sleep(0.2)
            r = get(tpat_start_url.replace('https://events.ads.vungle.com', scrat_all_host),
                    headers=platform_headers(sdk_version=sdk_v))
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(response_payload['msg'], equal_to('ok'))
            assert_that(response_payload['code'], equal_to(200))

    @allure.feature('block')
    @allure.tag('basic', 'v1.257.0')
    @allure.story('PBJ-5258 Do not send rewarded video traffic to InMobi')
    @allure.description('Verify that jaeger will block rtb account id (60d191906f59f30017a17639) for rewarded placement'
                        )
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_rewarded_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('coppa', [True])
    def test_block_rewarded_for_inmobi_realTime(self, pub_app_id, placement, sdk_v, partner, coppa):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, coppa=coppa,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_default_InMobi)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            hbp_response = info['hbp_response']
            debug = hbp_response['ext']['debug']
            assert_that(debug['rtb_failed_filters'][ext_non_test_mode_kraken_default_InMobi], equal_to('placementTypeFilter'))



    @allure.feature('Deprecate HBP')
    @allure.tag('normal')
    @allure.story('PBJ-5173 [Jaeger][Deprecate HBP] Sync bflat request field')
    @allure.description('Verify `bidrequest_imp_bidfloor` is in the request from jaeger sent to bflat')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_bid_request_imp_bidfloor_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, ads_retry_mode='meister',
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            # assert that `bidrequest_imp_bidfloor` is added to the request from jaeger sent to bflat.
