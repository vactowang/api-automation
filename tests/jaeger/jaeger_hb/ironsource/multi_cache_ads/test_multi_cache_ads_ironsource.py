import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import post_hbp_request, request_hb_win_notification, request_hbp, request_hb_loss_notification
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema
import time


@allure.epic('HBP Ironsource')
class TestMultiCacheAdsIronsource(object):

    @allure.feature('hbp winttl')
    @allure.tag('normal', 'v0.41.0', 'v0.52.0', 'v0.62.0')
    @allure.story('PBJ-2421 winttl for all partner in multi-cache in HBP'
                  'PBJ-3437 HBP - win ttl feature enhancement')
    @allure.description('Verify it will bid again for the token which has already win via SDK version >= 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    def test_ironsource_winttl_sdk_version_1(self, pub_app_id, placement, sdk_v):
        info = request_hb_win_notification('ironsource', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                           test_device_id=gen_device_id(), sdk_v=sdk_v)
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request(hbp_ironsource_endpoint_qa, json=req, headers=hbp_headers())

            if r.status_code == HTTPStatus.OK:
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                response_payload = r.json()
                assert_valid_schema(r.json(), response_schema.hbp_common)
                assert_keys_exist(response_payload, 'id')

    @allure.feature('hbp winttl')
    @allure.tag('normal', 'v0.41.0', 'v0.52.0', 'v0.62.0')
    @allure.story('PBJ-2421 winttl for all partner in multi-cache in HBP'
                  'PBJ-3437 HBP - win ttl feature enhancement')
    @allure.description('Verify it will bid again for the token which has already win via SDK version < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_ironsource_winttl_sdk_version_2(self, pub_app_id, placement, sdk_v):
        info = request_hb_win_notification('ironsource', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                           test_device_id=gen_device_id(), sdk_v=sdk_v)
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request(hbp_ironsource_endpoint_qa, json=req, headers=hbp_headers())

            if r.status_code == HTTPStatus.OK:
                response_payload = r.json()
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.hbp_ironsource)
                assert_keys_exist(response_payload, 'id')

    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal', 'v0.41.0', 'v0.52.0')
    @allure.story('PBJ-2389 Update response ADM')
    @allure.description('Verify the updated adm via SDK version >= 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    def test_ironsource_adm_1(self, pub_app_id, placement, sdk_v):
        info = request_hbp('ironsource', 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.hbp_ironsource)

            adm = response_payload['seatbid'][0]['bid'][0]['adm']
            assert_that(str_to_json(adm)['event_id'], equal_to(info['ads_response']['ads'][0]['ad_markup']['id']))
            assert_that(scrat_impression_endpoint_qa('qa') in str_to_json(adm)['impression'][0])
            assert_that(str_to_json(adm)['version'], equal_to(1))

    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal', 'v0.41.0', 'v0.52.0')
    @allure.story('PBJ-2389 Update response ADM')
    @allure.description('Verify the updated adm via SDK version < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_ironsource_adm_2(self, pub_app_id, placement, sdk_v):
        info = request_hbp('ironsource', 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.hbp_ironsource)
            assert_that(response_payload['seatbid'][0]['bid'][0]['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal', 'v0.41.0', 'v0.52.0')
    @allure.story('PBJ-2390 Impression url in adm')
    @allure.description('Verify the impresson url from response adm')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_ironsource_adm_impression_url(self, pub_app_id, placement, sdk_v):
        info = request_hbp('ironsource', 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.hbp_ironsource)

            adm = response_payload['seatbid'][0]['bid'][0]['adm']

            r = get(str_to_json(adm)['impression'][0])
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(response_payload['msg'], equal_to('ok'))
            assert_that(response_payload['code'], equal_to(200))

    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal', 'v0.41.0', 'v0.52.0')
    @allure.story('PBJ-2386 Multi winttl ads filtered out from the candidate ads')
    @allure.description('Verify the no bid token can join the bidding')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2'])
    def test_ironsource_winttl_filter_out_1(self, pub_app_id, placement, sdk_v):
        info = request_hbp('ironsource', 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.hbp_ironsource)
            assert_keys_exist(response_payload, 'id')

    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal', 'v0.41.0', 'v0.52.0')
    @allure.story('PBJ-2386 Multi winttl ads filtered out from the candidate ads')
    @allure.description('Verify the loss token can join the bidding again')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2'])
    def test_ironsource_winttl_filter_out_2(self, pub_app_id, placement, sdk_v):
        info = request_hb_loss_notification('ironsource', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                            test_device_id=gen_device_id(), sdk_v=sdk_v)
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request(hbp_ironsource_endpoint_qa, json=req, headers=hbp_headers())

            if r.status_code == HTTPStatus.OK:
                response_payload = r.json()
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.hbp_ironsource)
                assert_keys_exist(response_payload, 'id')
