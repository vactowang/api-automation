import re

import pytest
import allure
import math

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema



@allure.epic('jaeger v5')
class TestImp(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp')
    @allure.description('Verify imp details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_details(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_request['imp'][0]['displaymanager'], equal_to('Vungle'))
            assert_keys_exist(bid_request['imp'][0], 'displaymanagerver')
            assert_that(bid_request['imp'][0]['tagid'], equal_to(common_test_placement))
            assert_that('secure' in bid_request['imp'][0])

    @allure.feature('bid floor')
    @allure.tag('basic', 'test mode')
    @allure.story('PBJ-3593 IAB bidfloor should not read from the CPM floor that was set up for rev share placements')
    @allure.description('Verify bid floor from debug info for test mode eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_bid_floor_for_test_mode_edsp(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', header_bidding=True, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that('bidfloor' in bid_request['imp'][0])
            assert_that(bid_request['imp'][0]['bidfloor'], equal_to(1))

    @allure.feature('bid floor')
    @allure.tag('basic')
    @allure.story('PBJ-3593 IAB bidfloor should not read from the CPM floor that was set up for rev share placements')
    @allure.description('Verify bid floor from debug info for non test mode eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_bid_floor_for_non_test_mode_edsp(self, pub_app_id):
        """
        Test country setting:

        {
            "name" : "United Kingdom",
            "iso_code2" : "AU",
            "iso_code3" : "AUS",
            "reserve_floor" : 1.0
            "banner_reserve_floor: 30
        }

        Placement level setting:
        {
            "default_flat_cpm": 0.8
            "default_rev_share": 0.6
        }
        """


        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_programmatic_mrec_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that('bidfloor' in bid_request['imp'][0])
            assert_that(bid_request['imp'][0]['bidfloor'], equal_to(30))

    # @allure.feature('bid floor')
    # @allure.tag('basic', 'test mode')
    # @allure.story('PBJ-3593 IAB bidfloor should not read from the CPM floor that was set up for rev share placements')
    # @allure.description('Verify \'erpmtarget\'=0.01 field from debug info for hb enabled test mode iDSP')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # def test_imp_bid_floor_for_test_mode_idsp(self, pub_app_id):
    #     if env == 'ci':
    #         rtb = test_mode_kraken_rtb_ids.split(',')[0]
    #     elif env == 'qa' or env == 'regression':
    #         rtb = test_mode_kraken_rtb_ids.split(',')[1]
    #     req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', header_bidding=True, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))
    #
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #     if 'sleep' not in ad_markup:
    #         bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #         assert_response_status_code(r.status_code, HTTPStatus.OK)
    #         assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #         assert_that('bidfloor' in bid_request['imp'][0])
    #         assert_keys_exist(bid_request['imp'][0]['ext']['vungle'], 'erpmtarget')
    #         assert_that(bid_request['imp'][0]['ext']['vungle']['erpmtarget'], equal_to(0.01))


    @allure.feature('bid floor')
    @allure.tag('basic')
    @allure.story('PBJ-3593 IAB bidfloor should not read from the CPM floor that was set up for rev share placements')
    @allure.description('Verify no \'erpmtarget\' field from debug info for hb enabled non test mode iDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_bid_floor_for_non_test_mode_idsp(self, pub_app_id):
        if env == 'ci':
            rtb = non_test_mode_kraken_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = non_test_mode_kraken_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', header_bidding=True, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb, src_ip=fr_ip))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that('bidfloor' in bid_request['imp'][0])
            assert_keys_not_exist(bid_request['imp'][0]['ext']['vungle'], 'erpmtarget')


    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp')
    @allure.description('Verify imp bid floor from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_bid_floor(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that('bidfloor' in bid_request['imp'][0])
            assert_that(bid_request['imp'][0]['bidfloorcur'], equal_to('USD'))

    @allure.feature('bid request bidfloor')
    @allure.tag('smoke', 'PBJ20S1')
    @allure.story('banner default floor')
    @allure.description('Test for banner default reserved global floor')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_banner_default_reserved_global_floor(self, pub_app_id):
        """
        banner default reserved global floor is 0.15

        Test country setting:

        {
            "name" : "United Kingdom",
            "iso_code2" : "GB",
            "iso_code3" : "GBR",
            "reserve_floor" : 1.0
        }

        geo.gb:{
            "external_dynamic_cpm_floor":2
        }

        Placement level setting:
        {
            "default_flat_cpm": 0.8
            "default_rev_share": 0.6
        }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=gb_ip, sdk_version='Vungle/6.3.2', debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        serving_cost = 0.05
        rev_share = 0.6
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2))

    @allure.feature('bid request bidfloor')
    @allure.tag('smoke', 'PBJ20S1')
    @allure.story('banner default floor')
    @allure.description('Test for banner floor with country setting')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_banner_floor_with_country_setting(self, pub_app_id):
        '''
        Test country setting:

        {
            "name" : "India",
            "iso_code2" : "IN",
            "iso_code3" : "IND",
            "reserve_floor" : 0.5,
            "banner_reserve_floor" : 0.3
        }

        Placement level setting:
        {
            "default_flat_cpm": 2
            "default_rev_share": 0.6,
            "external_default_dynamic_cpm_floor": 7

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=in_ip, sdk_version='Vungle/6.3.2', debug='jaeger',
                                          rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        flat_cpm = 2
        rev_share = 0.6
        assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
                                 flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))

    @allure.feature('bid request bidfloor')
    @allure.tag('smoke', 'PBJ20S1')
    @allure.story('banner default floor')
    @allure.description('Test for video default reserved global floor')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_video_default_reserved_global_floor(self, pub_app_id):
        '''
        Video default reserved global floor is 2
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip='127.0.0.1', sdk_version='Vungle/6.3.2', debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2))

    @allure.feature('bid request bidfloor')
    @allure.tag('smoke', 'PBJ20S1')
    @allure.story('banner default floor')
    @allure.description('Test for video floor with country setting')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_video_floor_with_country_setting(self, pub_app_id):
        '''
        Video default reserved global floor is 2

        Test country setting:

        {
            "name" : "United Kingdom",
            "iso_code2" : "AU",
            "iso_code3" : "GBR",
            "reserve_floor" : 1.0
        }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50916IMA', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=gb_ip, sdk_version='Vungle/6.3.2', debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(1))

    @allure.feature('instl')
    @allure.tag('normal', 'v1.153.0')
    @allure.story('PBJ-2385 The instl field in bidrequest')
    @allure.description('Verify the instl field for non incentivized placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50916IMA'])
    def test_for_instl_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('instl')
    @allure.tag('normal', 'test_mode', 'v1.153.0')
    @allure.story('PBJ-2385 The instl field in bidrequest')
    @allure.description('Verify the instl field for non incentivized placement edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50916IMA'])
    def test_for_instl_1_ext(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('instl')
    @allure.tag('normal', 'v1.153.0')
    @allure.story('PBJ-2385 The instl field in bidrequest')
    @allure.description('Verify the instl field for incentivized placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_for_instl_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('instl')
    @allure.tag('normal', 'test_mode', 'v1.153.0')
    @allure.story('PBJ-2385 The instl field in bidrequest')
    @allure.description('Verify the instl field for incentivized placement edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_for_instl_2_ext(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('instl')
    @allure.tag('normal', 'v1.153.0')
    @allure.story('PBJ-2385 The instl field in bidrequest')
    @allure.description('Verify the instl field for banner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_for_instl_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('instl')
    @allure.tag('normal', 'v1.153.0')
    @allure.story('PBJ-2385 The instl field in bidrequest')
    @allure.description('Verify the instl field for mrec')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_image_mrec_placement])
    def test_for_instl_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('instl')
    @allure.tag('normal', 'test_mode', 'v1.153.0')
    @allure.story('PBJ-2385 The instl field in bidrequest')
    @allure.description('Verify the instl field for mrec edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_image_mrec_placement])
    def test_for_instl_4_ext(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'v1.172.0')
    @allure.story('PBJ-3035 Supported template types for native placement, PBJ-3075 Ads response for native ads')
    @allure.description('Verify the native request in bid request for native type placement via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['imp'][0], 'native')
        assert_that(isinstance(bid_request['imp'][0]['native']['request'], str))
        assert_that('eventtrackers' in bid_request['imp'][0]['native']['request'])
        assert_that(isinstance(bid_request['imp'][0]['native']['ver'], str))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'v1.172.0', 'test_mode')
    @allure.story('PBJ-3035 Supported template types for native placement, PBJ-3075 Ads response for native ads')
    @allure.description('Verify the native request in bid request for native type placement via iDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['imp'][0], 'native')
        assert_that(isinstance(bid_request['imp'][0]['native']['request'], str))
        assert_that('eventtrackers' in bid_request['imp'][0]['native']['request'])
        assert_that(isinstance(bid_request['imp'][0]['native']['ver'], str))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'v1.172.0')
    @allure.story('PBJ-3035 Supported template types for native placement, PBJ-3075 Ads response for native ads')
    @allure.description('Verify the native request in bid request for native type placement via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['imp'][0], 'native')
        assert_that(isinstance(bid_request['imp'][0]['native']['request'], str))
        assert_that('eventtrackers' in bid_request['imp'][0]['native']['request'])
        assert_that(isinstance(bid_request['imp'][0]['native']['ver'], str))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'v1.172.0', 'test_mode')
    @allure.story('PBJ-3035 Supported template types for native placement, PBJ-3075 Ads response for native ads')
    @allure.description('Verify the native request in bid request for native type placement via eDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['imp'][0], 'native')
        assert_that(isinstance(bid_request['imp'][0]['native']['request'], str))
        assert_that('eventtrackers' in bid_request['imp'][0]['native']['request'])
        assert_that(isinstance(bid_request['imp'][0]['native']['ver'], str))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-4125 Only check required fields for Native Bid Response')
    @allure.description('Verify jaeger will serve native placement without feild CTA Destination in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_bid_response_01(self, pub_app_id, placement):
        asserts_fields_obj = (
            {
                "id": 4,
                "required": 1,
                "data": {
                    "value": "cta text"
                }
            },
            {
                "id": 8,
                "required": 1,
                "data": {
                    "value": "https://cdn-lb.vungle.com/templates/defaults/img/4.5-stars.svg"
                }
            }
        )
        adm = json.dumps(json.dumps(native_response_edsp(*asserts_fields_obj)))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-4125 Only check required fields for Native Bid Response')
    @allure.description('Verify jaeger will serve native placement without feild CTA Text in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_bid_response_02(self, pub_app_id, placement):
        asserts_fields_obj = (
            {
                "id": 3,
                "required": 1,
                "data": {
                    "value": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302"
                }
            },
            {
                "id": 8,
                "required": 1,
                "data": {
                    "value": "https://cdn-lb.vungle.com/templates/defaults/img/4.5-stars.svg"
                }
            }
        )
        adm = json.dumps(json.dumps(native_response_edsp(*asserts_fields_obj)))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-4125 Only check required fields for Native Bid Response')
    @allure.description('Verify jaeger will serve native placement without field Star Ratings in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_bid_response_03(self, pub_app_id, placement):
        asserts_fields_obj = (
            {
                "id": 3,
                "required": 1,
                "data": {
                    "value": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302"
                }
            },
            {
                "id": 4,
                "required": 1,
                "data": {
                    "value": "cta text"
                }
            }
        )
        adm = json.dumps(json.dumps(native_response_edsp(*asserts_fields_obj)))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-4125 Only check required fields for Native Bid Response')
    @allure.description('Verify jaeger will serve native placement without field Star Ratings, '
                        'CTA Text, CTA Destination in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_bid_response_04(self, pub_app_id, placement):
        adm = json.dumps(json.dumps(native_response_edsp()))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4125 Only check required fields for Native Bid Response')
    @allure.description('Verify jaeger will serve native placement without field Star Ratings, '
                        'CTA Text, CTA Destination in bid response via test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_bid_response_05(self, pub_app_id, placement):
        adm = json.dumps(json.dumps(native_response_edsp()))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.216.0')
    @allure.story('PBJ-4188 Do Not Reject Native bid response without Asset ID = 11(sponsored by)')
    @allure.description('Verify jaeger will serve native placement without Asset ID = 11 in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_bid_response_06(self, pub_app_id, placement):
        adm = json.dumps(json.dumps(native_response_edsp()))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.216.0')
    @allure.story('PBJ-4188 Do Not Reject Native bid response without Asset ID = 11(sponsored by)')
    @allure.description('Verify jaeger will serve native placement with Asset ID = 11 in bid response and will use '
                        'DSP\'s assert in the token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_bid_response_07(self, pub_app_id, placement):
        assert_obj = {
                    "id": 11,
                    "required": 1,
                    "data": {
                        "value": "emily_test_assert_11"
                    }
                }
        adm = json.dumps(json.dumps(native_response_edsp(assert_obj)))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_that(normal_replacements['SPONSORED_BY'], equal_to('emily_test_assert_11'))

    @allure.feature('native placement')
    @allure.tag('normal', 'test_mode', 'v1.216.0')
    @allure.story('PBJ-4188 Do Not Reject Native bid response without Asset ID = 11(sponsored by)')
    @allure.description('Verify jaeger will serve native placement with Asset ID = 11 in bid response and will use '
                        'DSP\'s assert in the token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_bid_response_08(self, pub_app_id, placement):
        assert_obj = {
                    "id": 11,
                    "required": 1,
                    "data": {
                        "value": "emily_test_assert_11"
                    }
                }
        adm = json.dumps(json.dumps(native_response_edsp(assert_obj)))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_mraid,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_that(normal_replacements['SPONSORED_BY'], equal_to('emily_test_assert_11'))

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.216.0')
    @allure.story('PBJ-4188 Do Not Reject Native bid response without Asset ID = 11(sponsored by)')
    @allure.description('Verify the assert ID=11 is not a required field in bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_bid_response_09(self, pub_app_id, placement):

        adm = json.dumps(json.dumps(native_response_edsp()))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        native_obj = bid_request['imp'][0]['native']
        assertIDS = native_obj['request']
        assertIDS = json.loads(assertIDS)['assets']
        # Verified that assertId is not a required field
        for x in assertIDS:
            if x['id'] == 11:
                assert_keys_not_exist(x, 'required')
            else:
                continue
    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support impression tracker in Native Bid Response markup, & clicktrackers')
    @allure.description('Verify jaeger will serve native placement with eventtrackers in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_support_eventtrackers(self, pub_app_id, placement):
        adm = json.dumps(json.dumps(native_response_edsp()))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support impression tracker in Native Bid Response markup, & clicktrackers')
    @allure.description('Verify jaeger will serve native placement with imptrackers in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_support_imptrackers(self, pub_app_id, placement):
        adm = json.dumps(json.dumps(native_response_edsp(eventtrackers=False, imptrackers=True)))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support impression tracker in Native Bid Response markup, & clicktrackers')
    @allure.description('Verify jaeger will serve native placement with clicktrackers in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_support_clicktrackers(self, pub_app_id, placement):
        adm = json.dumps(json.dumps(native_response_edsp(eventtrackers=False, clicktrackers=True)))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support impression tracker in Native Bid Response markup, & clicktrackers')
    @allure.description('Verify jaeger will serve native placement with clicktrackers, imptrackers and '
                        'eventtrackers in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_support_trackers(self, pub_app_id, placement):
        adm = json.dumps(json.dumps(native_response_edsp(eventtrackers=True, imptrackers=True, clicktrackers=True)))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4115 Support impression tracker in Native Bid Response markup, & clicktrackers')
    @allure.description('Verify jaeger will serve native placement with clicktrackers, imptrackers and '
                        'in bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_support_imptrackers_clickertrackers_t(self, pub_app_id, placement):
        adm = json.dumps(json.dumps(native_response_edsp(eventtrackers=False, imptrackers=True, clicktrackers=True)))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4257 Support .jpeg file and don\'t reject image with .jpeg file extension')
    @allure.description('Verify jaeger will serve native placement with jpeg image')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_support_jpeg(self, pub_app_id, placement):
        adm = json.dumps(json.dumps(native_response_edsp()))
        adm_obj = 'seatbid.0.bid.0.adm@"%s"' % adm
        adm_obj = adm_obj.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, override_bid_response_any=adm_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that(ad_markup['campaign'], is_not(None))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3850 Add reserved floor for Native Ad by country.')
    @allure.description('Verify bidfloor is equal to banner_reserve_floor which setting in countries collection'
                        'when flat_cpm < banner_reserve_floor and banner_reserve_floor > reserve_floor')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_reserve_floor_01(self, pub_app_id, placement):
        """
        formula: real flat_cpm = flat_cpm(setting in db) / ((1 - serCost) * revShare)
        countries setting:  "banner_reserve_floor":30
        placement setting:
                   "AU": {
                       "flat_cpm": 0.8
                       "rev_share": 0.6

                   }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, src_ip=au_ip))

        response_payload = r.json()
        serving_cost = 0.05
        rev_share = 0.6
        flat_cpm = 0.8 / (1 - serving_cost) / (rev_share * jaeger_adjuster)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        bidfloor = bid_request['imp'][0]['bidfloor']
        assert_that(bidfloor, equal_to(30))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3850 Add reserved floor for Native Ad by country.')
    @allure.description('Verify bidfloor is equal to banner_reserve_floor which setting in countries collection'
                        'when flat_cpm < banner_reserve_floor and banner_reserve_floor = reserve_floor')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_reserve_floor_02(self, pub_app_id, placement):
        """
        formula: real flat_cpm = flat_cpm(setting in db) / ((1 - serCost) * revShare)
        countries setting:  "banner_reserve_floor":2.5
        placement setting:
                   "AU": {
                       "flat_cpm": 0.8
                       "rev_share": 0.6

                   }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, src_ip=fr_ip))

        response_payload = r.json()
        serving_cost = 0.05
        rev_share = 0.6
        flat_cpm = 0.8 / (1 - serving_cost) / (rev_share * jaeger_adjuster)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        bidfloor = bid_request['imp'][0]['bidfloor']
        assert_that(bidfloor, equal_to(2.5))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3850 Add reserved floor for Native Ad by country.')
    @allure.description('Verify bidfloor is equal to banner_reserve_floor which setting in countries collection'
                        'when flat_cpm < banner_reserve_floor and banner_reserve_floor < reserve_floor')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_reserve_floor_03(self, pub_app_id, placement):
        """
        formula: real flat_cpm = flat_cpm(setting in db) / ((1 - serCost) * revShare)
        countries setting:  "banner_reserve_floor":2.3
        placement global setting:
                  {
                       "flat_cpm": 0.4
                       "rev_share": 0.6

                   }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, src_ip=jp_ip))

        response_payload = r.json()
        serving_cost = 0.05
        rev_share = 0.6
        flat_cpm = 0.4 / (1 - serving_cost) / (rev_share * jaeger_adjuster)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        bidfloor = bid_request['imp'][0]['bidfloor']
        assert_that(bidfloor, equal_to(2.3))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3850 Add reserved floor for Native Ad by country.')
    @allure.description('Verify bidfloor is equal to flat_cpm'
                        'when flat_cpm > banner_reserve_floor')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_native_reserve_floor_04(self, pub_app_id, placement):
        """
        formula: real flat_cpm = flat_cpm(setting in db) / ((1 - serCost) * revShare)
        countries setting:  "banner_reserve_floor":1
        placement global setting:
                   {
                       "flat_cpm": 7
                       "rev_share": 0.6
                   }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, src_ip=ca_us_ip))

        response_payload = r.json()
        serving_cost = 0.05
        rev_share = 0.6
        #4675 implement
        flat_cpm = 2

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        bidfloor = bid_request['imp'][0]['bidfloor']
        rev_share = 0.6
        assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
                                 flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))


    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3850 Add reserved floor for Native Ad by country.')
    @allure.description('Verify bidfloor is equal to placement flat cpm when '
                        'there is no banner_reserve_floor in country and flat_cpm>0.15')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_reserve_floor_05(self, pub_app_id, placement):
        """
        formula: real flat_cpm = flat_cpm(setting in db) / ((1 - serCost) * revShare)
        countries setting:  "reserve_floor":1
        placement global setting:
                 {
                       "flat_cpm": 0.4
                       "rev_share": 0.6

                   }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, src_ip=cn_ip))

        response_payload = r.json()
        serving_cost = 0.05
        rev_share = 0.6
        flat_cpm = 1 / (1 - serving_cost) / (rev_share)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        bidfloor = bid_request['imp'][0]['bidfloor']
        assert_that(math.isclose(bidfloor, flat_cpm))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3850 Add reserved floor for Native Ad by country.')
    @allure.description('Verify bidfloor is equal to 0.15 when placement flatcpm<0.15'
                        'and there is no banner_reserve_floor in country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    def test_native_reserve_floor_06(self, pub_app_id, placement):
        """
        formula: real flat_cpm = flat_cpm(setting in db) / ((1 - serCost) * revShare)
        countries setting:  "reserve_floor":1
        placement setting:
                   {
                       "flat_cpm": 0.1
                       "rev_share": 0.6

                   }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, src_ip=cn_ip))

        response_payload = r.json()
        serving_cost = 0.05
        rev_share = 0.6
        flat_cpm = 0.1 / (1 - serving_cost) / (rev_share * jaeger_adjuster)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        bidfloor = bid_request['imp'][0]['bidfloor']
        assert_that(bidfloor, equal_to(0.15))

    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file'
    #               'PBJ-3352 Support sequence number of multiple config file for experiment framework')
    # @allure.description('Verify only non-hb and flat cpm enabled placement can enter the experiment')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    # @pytest.mark.parametrize('placement', ['HJKM6GM50919F'])
    # @pytest.mark.parametrize('flat_cpm', [1.8])
    # @pytest.mark.parametrize('factor', [1.5])
    # def test_flat_cpm_experiment_v7_1(self, pub_app_id, placement, flat_cpm, factor):
    #     '''
    #         "is_flat_cpm_enabled": true
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 1.8
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], equal_to(flat_cpm * factor))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file'
    #               'PBJ-3352 Support sequence number of multiple config file for experiment framework')
    # @allure.description('Verify only non-hb and flat cpm enabled placement can enter the experiment')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    # @pytest.mark.parametrize('placement', ['HJKM6GM50919F'])
    # @pytest.mark.parametrize('flat_cpm', [2])
    # @pytest.mark.parametrize('factor', [1.5])
    # def test_flat_cpm_experiment_v7_global(self, pub_app_id, placement, flat_cpm, factor):
    #     '''
    #         "is_flat_cpm_enabled": true
    #         default_flat_cpm: 2
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=fr_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], equal_to(flat_cpm * factor))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization'
                  'PBJ-4820 External Dynamic CPM Floor logic change')
    @allure.description('Verify that bid floor = THEN MAX(External Dynamic CPM Floor, Reserved Floor)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    def test_ext_dynamatic_floor_1(self, pub_app_id, placement):
        '''
            "is_flat_cpm_enabled": true
            "FR": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 3.4884,
                "flat_cpm": 1.8,
                "external_dynamic_cpm_floor": 2
            }

            Fr reserve floor: 2.5

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2.5))
        # verify "external_dynamic_floor":2, which is geo.external_dynamic_cpm_floor

    @allure.feature('flat cpm')
    @allure.tag('normal', 'test_mode' ,'v1.241.0')
    @allure.story(
        "PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization,"
        "PBJ-4820 External Dynamic CPM Floor logic change")
    @allure.description('Verify that bid floor = THEN MAX(External Dynamic CPM Floor, Reserved Floor)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    def test_ext_dynamatic_floor_t(self, pub_app_id, placement):
        '''
            "is_flat_cpm_enabled": true
            "FR": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 3.4884,
                "external_dynamic_cpm_floor": 2
            }
        Fr reserve floor: 2.5

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2.5))
        # verify "external_dynamic_floor":2, which is geo.external_dynamic_cpm_floor

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization'
                  'PBJ-4820 External Dynamic CPM Floor logic change')
    @allure.description('Verify that bid floor = THEN MAX(External Dynamic CPM Floor, Reserved Floor')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    @pytest.mark.parametrize('flat_cpm', [2])
    @pytest.mark.parametrize('factor', [1.5])
    def test_ext_dynamatic_floor_2(self, pub_app_id, placement, flat_cpm, factor):
        """
            "is_flat_cpm_enabled": true
            "external_default_dynamic_cpm_floor":2

            default_flat_cpm: 2

            reserve_floor:2
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=it_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        rev_share = 0.6
        assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
                                 flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))
        # verify "external_dynamic_floor":2, which is external_default_dynamic_cpm_floor

    @allure.feature('flat cpm')
    @allure.tag('normal', 'test_mode', 'v1.241.0')
    @allure.story(
        'PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization'
         'PBJ-4820 External Dynamic CPM Floor logic change')
    @allure.description('Verify that bid floor = THEN MAX(External Dynamic CPM Floor, Reserved Floor')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    @pytest.mark.parametrize('flat_cpm', [2])
    @pytest.mark.parametrize('factor', [1.5])
    def test_ext_dynamatic_floor_2_t(self, pub_app_id, placement, flat_cpm, factor):
        '''
            "is_flat_cpm_enabled": true
            "external_default_dynamic_cpm_floor":2

            default_flat_cpm: 2

            reserve_floor:2
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=it_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        rev_share = 0.6
        assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
                                 flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))
        # verify "external_dynamic_floor":2, which is external_default_dynamic_cpm_floor

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization')
    @allure.description('Verify non-hb and flat cpm enabled placement\'s  bid floor = country.reserve_floor if '
                        'flat cpm * factor < country.reserve_floor')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    @pytest.mark.parametrize('flat_cpm', [2])
    @pytest.mark.parametrize('factor', [1.5])
    def test_ext_dynamatic_floor_3(self, pub_app_id, placement, flat_cpm, factor):
        '''
            "is_flat_cpm_enabled": true
            "external_default_dynamic_cpm_floor":3

            country:
            "reserve_floor": 4
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(4))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization')
    @allure.description('Verify non-hb and flat cpm enabled placement\'s  bid floor = country.reserve_floor if '
                        'flat cpm * factor < country.reserve_floor via test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    @pytest.mark.parametrize('flat_cpm', [2])
    @pytest.mark.parametrize('factor', [1.5])
    def test_ext_dynamatic_floor_3_t(self, pub_app_id, placement, flat_cpm, factor):
        '''
            "is_flat_cpm_enabled": true
            "external_default_dynamic_cpm_floor":3

            country:
            "reserve_floor": 4
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(4))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('VM-54 extend external_dynamic_floor to Native')
    @allure.description('Verify that bid floor = THEN MAX(External Dynamic CPM Floor, Reserved Floor) for native '
                        'placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_placement_native])
    def test_ext_dynamatic_floor_native_01(self, pub_app_id, placement):
        '''
            "is_flat_cpm_enabled": true
            "FR": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 3.4884,
                "flat_cpm": 1.8,
                "external_dynamic_cpm_floor": 2
            }

            Fr reserve floor: 2.5

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2.5))
        # verify "external_dynamic_floor":2, which is geo.external_dynamic_cpm_floor


    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('VM-54 extend external_dynamic_floor to Native')
    @allure.description('Verify that bid floor = THEN MAX(External Dynamic CPM Floor, Reserved Floor) for native '
                        'placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_placement_native])
    def test_ext_dynamatic_floor_native_02(self, pub_app_id, placement):
        '''
            "is_flat_cpm_enabled": true
            "CN": {
                "external_dynamic_cpm_floor": 3
            }

            CN reserve floor: 1

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=cn_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(3))
        # verify "external_dynamic_floor":2, which is geo.external_dynamic_cpm_floor

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('VM-54 extend external_dynamic_floor to Native')
    @allure.description('Verify that bid floor = calculating external bid floor when geo level no setting for native '
                        'placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_placement_native])
    @pytest.mark.parametrize('src_ip', [au_ip, it_ip])
    def test_ext_dynamatic_floor_native_03(self, pub_app_id, placement, src_ip):
        '''
            "is_flat_cpm_enabled": true
            "AU": {
               "flat_cpm":2
            }
            "IT":{}
            "default_flat_cpm":2
            "external_default_dynamic_cpm_floor":2


            AU reserve floor: 1
            banner_reserve_floor:30


            IT reserve floor: 2

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=src_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        bid_floor = bid_request['imp'][0]['bidfloor']
        rev_share = 0.6
        cal_bid_floor = 2 / (1 - 0.05) / (rev_share * jaeger_adjuster)
        if src_ip == au_ip:
            assert_that(bid_floor, equal_to(30))
        elif src_ip == it_ip:
            assert_that(math.isclose(bid_floor, cal_bid_floor))



    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('VM-54 extend external_dynamic_floor to Native')
    @allure.description('Verify that bid floor = THEN MAX(External Dynamic CPM Floor, 0.01) for native '
                        'placement via hb')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_placement_native])
    def test_ext_dynamatic_floor_native_04(self, pub_app_id, placement):
        '''
            "is_flat_cpm_enabled": true
            "FR": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 3.4884,
                "flat_cpm": 1.8,
                "external_dynamic_cpm_floor": 2
            }

            Fr reserve floor: 2.5

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2))
        # verify "external_dynamic_floor":2, which is geo.external_dynamic_cpm_floor

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('VM-54 extend external_dynamic_floor to Native')
    @allure.description('Verify that bid floor = THEN MAX(External Dynamic CPM Floor, 0.01) for native '
                        'placement via hb')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_placement_native])
    def test_ext_dynamatic_floor_native_05(self, pub_app_id, placement):
        '''
            "is_flat_cpm_enabled": true
            "KP": {
                "external_dynamic_cpm_floor": 0.001
            }

            kp reserve floor: 1

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=kp_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(0.01))
        # verify "external_dynamic_floor":2, which is geo.external_dynamic_cpm_floor

    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.241.0')
    # @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization'
    #               'PBJ-4820 External Dynamic CPM Floor logic change')
    # @allure.description('Verify the app and country which is not in config file will be dropped to no_op bucket'
    #                     'Verify that bid floor = THEN MAX(External Dynamic CPM Floor, Reserved Floor')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    # @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_not_in_config])
    # @pytest.mark.parametrize('flat_cpm', [2.5])
    # def test_flat_cpm_experiment_v8_4(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         is_flat_cpm_enabled: true
    #         "external_default_dynamic_cpm_floor": 2.5
    #
    #         country:
    #         "reserve_floor": 2.5
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=it_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2.5))

    # @allure.feature('flat cpm')
    # @allure.tag('normal')
    # @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization'
    #               'PBJ-4820 External Dynamic CPM Floor logic change')
    # @allure.description('Verify the app and country which is not in config file will be dropped to no_op bucket,'
    #                     'and flat_cpm > country.reserve_floor'
    #                     'Verify that bid floor = THEN MAX(External Dynamic CPM Floor, Reserved Floor')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    # @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_not_in_config])
    # @pytest.mark.parametrize('flat_cpm', [1.4])
    # @pytest.mark.parametrize('factor', [1.5])
    # def test_flat_cpm_experiment_v8_4_geo(self, pub_app_id, placement, flat_cpm, factor):
    #     '''
    #         is_flat_cpm_enabled: true
    #         "external_default_dynamic_cpm_floor": 2.5
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 1.8,
    #             "external_dynamic_cpm_floor": 1.4
    #         }
    #       AU
    #       reserve_floor: 1
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], equal_to(1.4))

    # @allure.feature('flat cpm')
    # @allure.tag('normal')
    # @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization')
    # @allure.description('Verify the app and country which is not in config file will be dropped to no_op bucket,'
    #                     'and flat_cpm < country.reserve_floor')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    # @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_not_in_config])
    # @pytest.mark.parametrize('flat_cpm', [2.5])
    # def test_flat_cpm_experiment_v8_4_c(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         is_flat_cpm_enabled: true
    #         "external_default_dynamic_cpm_floor": 2.5
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 1.8
    #         }
    #       us
    #       reserve_floor: 4
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=us_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], equal_to(4))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization'
                  'PBJ-4820 External Dynamic CPM Floor logic change')
    @allure.description('Verify hb and flat cpm enabled placement read flat cpm value from'
                        'placement.geo.external_dynamic_cpm_floor in MongoDB: does not enter the experiment, flat cpm >'
                        'country reserve floor'
                        'Verify that bid floor = THEN MAX(External Dynamic CPM Floor, iabDefaultFloor')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    @pytest.mark.parametrize('flat_cpm', [2])
    def test_flat_cpm_v8_hb_ext_flat_cpm_exist(self, pub_app_id, placement, flat_cpm):
        """
            "is_flat_cpm_enabled": true
            "default_dynamic_cpm_floor":2
            "FR": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 3.4884,
                "external_dynamic_cpm_floor": 2
            }
            iabDefaultFloor: 0.01

            Fr reserve floor: 2.5

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization')
    @allure.description('Verify hb and flat cpm enabled placement read flat cpm value from'
                        'placement.external_default_dynamic_cpm_floor in MongoDB: does not enter the experiment, flat cpm >'
                        'country reserve floor')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    @pytest.mark.parametrize('flat_cpm', [2])
    @pytest.mark.parametrize('factor', [1.5])
    def test_flat_cpm_v8_hb_deflat_ext_flat_cpm_exist(self, pub_app_id, placement, flat_cpm, factor):
        '''
            "is_flat_cpm_enabled": true
            "external_default_dynamic_cpm_floor":2

            "default_flat_cpm":2

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=it_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2))

    @allure.feature('flat cpm')
    @allure.tag('normal')
    @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization')
    @allure.description('Verify hb and flat cpm enabled placement read flat cpm value from'
                        'placement.external_default_dynamic_cpm_floor in MongoDB: does not enter the experiment, flat cpm <'
                        'country reserve floor')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    @pytest.mark.parametrize('flat_cpm', [2])
    @pytest.mark.parametrize('factor', [1.5])
    def test_flat_cpm_v8_hb_deflat_ext_flat_cpm_exist_01(self, pub_app_id, placement, flat_cpm, factor):
        '''
            "is_flat_cpm_enabled": true
            "external_default_dynamic_cpm_floor":2

            us
            reserve_floor: 4
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(4))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization')
    @allure.description('Verify bidfloor = 0.01, if the calculate flat_cpm value < 0.01')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    @pytest.mark.parametrize('flat_cpm', [0.001])
    @pytest.mark.parametrize('factor', [1.5])
    def test_flat_cpm_v8_hb_less_than_0_0_1(self, pub_app_id, placement, flat_cpm, factor):
        """
            "is_flat_cpm_enabled": true
            "KP" :{
                "external_dynamic_cpm_floor": 0.001
            }
            iabDefaultFloor = 0.01
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=kp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(0.01))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.241.0')
    @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization')
    @allure.description('Verify hb traffic and no external_default_dynamic_cpm_floor setting in DB will default to '
                        'country.reserve_floor""')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919-2'])
    @pytest.mark.parametrize('country', [fr_ip, us_ip])
    def test_flat_cpm_v8_5(self, pub_app_id, placement, country):
        '''
        fr
        reserve_floor: 2.5

        us
        reserve_floor: 4
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=country,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        if country == fr_ip:
            assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2.5))
        elif country == us_ip:
            assert_that(bid_request['imp'][0]['bidfloor'], equal_to(4))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.236.0')
    @allure.story(
        'PBJ-4675 add external dynamic cpm floor fields in Mongo for Banner placements')
    @allure.description('Verify non-hb and flat cpm enabled banner placement read flat cpm value from'
                        'external_default_dynamic_cpm_floor=7 which setting in db '
                        'does not enter flat cpm experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('flat_cpm', [2])
    def test_flat_cpm_v8_1_banner(self, pub_app_id, placement, flat_cpm):
        """
            "external_default_dynamic_cpm_floor":7
            "is_flat_cpm_enabled": true
            "default_flat_cpm": 2

            US banner reserve floor: 1

        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False,
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        rev_share = 0.6
        assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
                                 flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.236.0')
    @allure.story(
        'PBJ-4675 add external dynamic cpm floor fields in Mongo for Banner placements')
    @allure.description('Verify non-hb and flat cpm enabled banner placement read flat cpm value from db config'
                        'external_default_dynamic_cpm_floor=7 which setting in db '
                        'does not enter flat '
                        'cpm experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('flat_cpm', [2])
    def test_flat_cpm_v8_2_banner(self, pub_app_id, placement, flat_cpm):
        '''
            "external_default_dynamic_cpm_floor":7
            "is_flat_cpm_enabled": true
            "GB":{
             "external_dynamic_cpm_floor": 2
            }
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False,
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=gb_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.236.0')
    @allure.story(
        'PBJ-4675 add external dynamic cpm floor fields in Mongo for Banner placements')
    @allure.description('Verify non-hb and flat cpm enabled banner placement read flat cpm value from db config: '
                        'does not enter flat '
                        'cpm experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('flat_cpm', [1.8])
    @pytest.mark.parametrize('factor', [1.5])
    def test_flat_cpm_v8_3_banner(self, pub_app_id, placement, flat_cpm, factor):
        '''
            "is_flat_cpm_enabled": true
            "FR": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 3.4884,
                "flat_cpm": 1.8,
                "external_dynamic_cpm_floor": 2
            }

            AU reserve floor: 2.5

            reserve floor> flat cpm

        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False,
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(30))

    @allure.feature('flat cpm')
    @allure.tag('normal', 'v1.236.0')
    @allure.story(
        'PBJ-4675 add external dynamic cpm floor fields in Mongo for Banner placements')
    @allure.description('Verify bidfloor = 0.01, if the calculate flat_cpm value < 0.01')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('flat_cpm', [0.001])
    def test_flat_cpm_v8_4_banner(self, pub_app_id, placement, flat_cpm):
        '''
            "is_flat_cpm_enabled": true
            "kp": {
                "external_dynamic_cpm_floor": 0.001
            }


        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=kp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(0.01))

    @allure.feature('flat cpm')
    @allure.tag('normal')
    @allure.story('PBJ-4537 Add capability to dynamically update eDSP floors in MongoDB for External Floor Optimization')
    @allure.description('Verify non-hb traffic and flat cpm enabled, default to flat_cpm * 1.5""')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919-2'])
    @pytest.mark.parametrize('flat_cpm', [1.8])
    @pytest.mark.parametrize('factor', [1.5])
    def test_flat_cpm_v8_6(self, pub_app_id, placement, flat_cpm, factor):
        """
               "is_flat_cpm_enabled": true
               "AU": {
                   "nrg_multiplier": 1.7,
                   "rev_share": 0.6,
                   "dynamic_cpm_floor": 3.4884,
                   "flat_cpm": 1.8
               }
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        rev_share = 0.6
        assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
                                          flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))

    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file'
    #               'PBJ-3593 IAB bidfloor should not read from the CPM floor that was set up for rev share placements')
    # @allure.description('Verify that hb and flat cpm enabled placement can not enter the experiment')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', ['HJKM6GM50919-2'])
    # @pytest.mark.parametrize('flat_cpm', [1.8])
    # def test_flat_cpm_experiment_v7_2(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 1.8
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], equal_to(1))
    #     # rev_share = 0.6
    #     # assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
    #     #                          flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify that non-hb and flat cpm disabled placement can not enter the experiment')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', ['HJKM6GM50919-1'])
    # @pytest.mark.parametrize('flat_cpm', [1.8])
    # @pytest.mark.parametrize('factor', [1])
    # def test_flat_cpm_experiment_v7_3(self, pub_app_id, placement, flat_cpm, factor):
    #     '''
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 1.8
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], not equal_to(flat_cpm * factor))
    #
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify that hb and flat cpm disabled placement can not enter the experiment')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', ['HJKM6GM50919-3'])
    # @pytest.mark.parametrize('flat_cpm', [1.8])
    # @pytest.mark.parametrize('factor', [1])
    # def test_flat_cpm_experiment_v7_4(self, pub_app_id, placement, flat_cpm, factor):
    #     '''
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], not equal_to(flat_cpm * factor))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file'
    #               'PBJ-3593 IAB bidfloor should not read from the CPM floor that was set up for rev share placements')
    # @allure.description('Verify non-hb and flat cpm enabled placement with hb traffic can not enter the experiment')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    # @pytest.mark.parametrize('flat_cpm', [2.0])
    # def test_flat_cpm_experiment_v7_5(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 2.0
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], equal_to(1))
    #     # rev_share = 0.6
    #     # assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
    #     #                          flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify the traffic from CN can not enter the experiment')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    # @pytest.mark.parametrize('flat_cpm', [2])
    # def test_flat_cpm_experiment_v7_61(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         "CN": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 2
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=cn_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     rev_share = 0.6
    #     assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
    #                              flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify the flat cpm will use the country reserve value if it less than the reserve value')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    # @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement])
    # @pytest.mark.parametrize('flat_cpm', [2])
    # def test_flat_cpm_experiment_v7_62(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         Placement: default_flat_cpm: 2
    #         Country US reserve_floor: 4
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=ca_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], equal_to(4))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify the experiment factor will not affect the internal flat cpm value')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    # @pytest.mark.parametrize('flat_cpm', [2.0])
    # def test_flat_cpm_experiment_v7_7(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 2.0
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=meister_rtb_ids))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['ext']['vungle']['flat_cpm'], equal_to(flat_cpm))
    #
    #     rev_share = 0.6
    #     serving_cost = 0.05
    #     cpm_floor = 0.58
    #
    #     erpm_target = cpm_floor / (1 - serving_cost) / (rev_share * jaeger_adjuster)
    #     assert_that(math.isclose(bid_request['imp'][0]['ext']['vungle']['erpmtarget'], erpm_target))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0', 'test_mode')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify the experiment factor will not affect the internal flat cpm value in test mode')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    # @pytest.mark.parametrize('flat_cpm', [2.0])
    # def test_flat_cpm_experiment_v7_8(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 2.0
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['ext']['vungle']['flat_cpm'], equal_to(flat_cpm))
    #
    #     rev_share = 0.6
    #     serving_cost = 0.05
    #     cpm_floor = 0.58
    #
    #     erpm_target = cpm_floor / (1 - serving_cost) / (rev_share * jaeger_adjuster)
    #     assert_that(math.isclose(bid_request['imp'][0]['ext']['vungle']['erpmtarget'], erpm_target))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify the app and country which is not in config file will be dropped to no_op bucket'
    #                     )
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    # @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_not_in_config])
    # @pytest.mark.parametrize('flat_cpm', [1.4])
    # def test_flat_cpm_experiment_v7_9(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         "external_default_dynamic_cpm_floor": 2.5
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 1.8,
    #             "external_dynamic_cpm_floor": 1.4
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], not equal_to(flat_cpm*1.5))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0', 'test_mode')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify the app and country which is not in config file will be dropped to no_op bucket'
    #                     ' in test mode'
    #                     )
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    # @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_not_in_config])
    # @pytest.mark.parametrize('flat_cpm', [1.4])
    # def test_flat_cpm_experiment_v7_9t(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         "external_default_dynamic_cpm_floor": 2.5
    #         "AU": {
    #             "nrg_multiplier": 1.7,
    #             "rev_share": 0.6,
    #             "dynamic_cpm_floor": 0.58,
    #             "flat_cpm": 1.8,
    #             "external_dynamic_cpm_floor": 1.4
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['imp'][0]['bidfloor'], not equal_to(flat_cpm*1.5))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify the placement and country which is in config file as no_op')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('flat_cpm', [0.4])
    # def test_flat_cpm_experiment_v7_10(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         "default_flat_cpm": 0.4,
    #         "default_rev_share": 0.6
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=fr_ip,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     rev_share = 0.6
    #     country_floor = 2.5
    #     if flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster) < country_floor:
    #         assert_that(bid_request['imp'][0]['bidfloor'], equal_to(country_floor))
    #     else:
    #         assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
    #                                  flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0', 'test_mode')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify the placement and country which is in config file as no_op in test mode')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('flat_cpm', [0.4])
    # def test_flat_cpm_experiment_v7_10t(self, pub_app_id, placement, flat_cpm):
    #     '''
    #         "default_flat_cpm": 0.4,
    #         "default_rev_share": 0.6
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=fr_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     rev_share = 0.6
    #     country_floor = 2.5
    #     if flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster) < country_floor:
    #         assert_that(bid_request['imp'][0]['bidfloor'], equal_to(country_floor))
    #     else:
    #         assert_that(math.isclose(bid_request['imp'][0]['bidfloor'],
    #                                  flat_cpm / (1 - 0.05) / (rev_share * jaeger_adjuster)))
    #
    # @allure.feature('flat cpm')
    # @allure.tag('normal', 'v1.164.0', 'v1.167.0', 'v1.169.0', 'v1.171.0', 'v1.173.0', 'v1.174.0', 'test_mode')
    # @allure.story('PBJ-3159 Experiment supports bucket configuration in s3 file')
    # @allure.description('Verify the placement and country which is in config file as dynamic_150 in test mode')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('flat_cpm', [0.3])
    # @pytest.mark.parametrize('factor', [1.5])
    # def test_flat_cpm_experiment_v7_11(self, pub_app_id, placement, flat_cpm, factor):
    #     '''
    #         "GB": {
    #             "dynamic_cpm_floor": 0.1,
    #             "flat_cpm": 0.3,
    #             "rev_share": 0.5
    #         }
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=gb_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     country_floor = 1
    #     if flat_cpm * factor < country_floor:
    #         assert_that(bid_request['imp'][0]['bidfloor'], equal_to(country_floor))
    #     else:
    #         assert_that(bid_request['imp'][0]['bidfloor'], equal_to(flat_cpm * factor))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3297 Check Native Ads bid response from external DSPs and make sure only legit bids '
                  'participate the auction')
    @allure.description('Verify the native request in bid request for native type placement via test mode eDSP ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_only_support_native_image_for_test_mode_edsp(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        native_request = bid_request['imp'][0]['native']['request']
        native_request = str_to_json(native_request)
        request_assert = native_request['assets']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details'][rtb]
        response_assert = str_to_json(bid_response['seatbid'][0]['bid'][0]['adm'])['native']['assets']
        for x in request_assert:
            for y in response_assert:
                if x['id'] == y['id']:
                    assert_that(y.keys, x.keys)
                    if 'img' in x:
                        if x['id'] == 1:
                            assert_that(x['img']['mimes'], equal_to(['image/jpg', 'image/gif', 'image/png']))
                        assert_keys_exist(y, 'img')
                        img_url_suffix = y['img']['url'][-3:]
                        assert_that(img_url_suffix, is_in(['jpg', 'gif', 'png']))
                    else:
                        continue
                else:
                    continue

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3297 Check Native Ads bid response from external DSPs and make sure only legit bids '
                  'participate the auction')
    @allure.description('Verify the native request in bid request for native type placement via non test mode eDSP ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_only_support_native_image_for_non_test_mode_edsp(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        native_request = bid_request['imp'][0]['native']['request']
        native_request = str_to_json(native_request)
        request_assert = native_request['assets']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details'][rtb]
        response_assert = str_to_json(bid_response['seatbid'][0]['bid'][0]['adm'])['native']['assets']
        for x in request_assert:
            for y in response_assert:
                if x['id'] == y['id']:
                    assert_that(y.keys, x.keys)
                    if 'img' in x:
                        if x['id'] == 1:
                            assert_that(x['img']['mimes'], equal_to(['image/jpg', 'image/gif', 'image/png']))
                        assert_keys_exist(y, 'img')
                        img_url_suffix = y['img']['url'][-3:]
                        assert_that(img_url_suffix, is_in(['jpg', 'gif', 'png']))
                    else:
                        continue
                else:
                    continue

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3297 Check Native Ads bid response from external DSPs and make sure only legit bids '
                  'participate the auction')
    @allure.description('Verify the native request in bid request for native type placement via test mode iDSP ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_only_support_native_image_for_test_mode_idsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        native_request = bid_request['imp'][0]['native']['request']
        native_request = str_to_json(native_request)
        img = native_request['assets'][0]['img']
        assert_keys_exist(img, 'mimes')
        assert_that(['image/jpg', 'image/gif', 'image/png'], equal_to(img['mimes']))


    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3297 Check Native Ads bid response from external DSPs and make sure only legit bids '
                  'participate the auction')
    @allure.description('Verify the native request in bid request for native type placement via non test mode iDSP ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_only_support_native_image_for_non_test_mode_idsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        native_request = bid_request['imp'][0]['native']['request']
        native_request = str_to_json(native_request)
        img = native_request['assets'][0]['img']
        assert_keys_exist(img, 'mimes')
        assert_that(['image/jpg', 'image/gif', 'image/png'], equal_to(img['mimes']))


    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3599 Exchange - Update "privacy icon", and "privacy url" from Required to '
                  'Optional in the bid request and bid response')
    @allure.description('Verify "privacy icon" and "privacy url" is optional field'
                        ' for native type placement via non test mode idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_optional_field_native_image_for_non_test_mode_idsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        native_request = bid_request['imp'][0]['native']['request']
        native_request = str_to_json(native_request)
        assets = native_request['assets']
        for x in assets:
            if x['id'] == 9 or x['id'] == 10:
                assert_keys_not_exist(x, 'required')
            else:
                continue

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3599 Exchange - Update "privacy icon", and "privacy url" from Required to '
                  'Optional in the bid request and bid response')
    @allure.description('Verify "privacy icon" and "privacy url" is optional field'
                        ' for native type placement via  test mode idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_optional_field_native_image_for_test_mode_idsp(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        native_request = bid_request['imp'][0]['native']['request']
        native_request = str_to_json(native_request)
        assets = native_request['assets']
        for x in assets:
            if x['id'] == 9 or x['id'] == 10:
                assert_keys_not_exist(x, 'required')
            else:
                continue




    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3599 Exchange - Update "privacy icon", and "privacy url" from Required to '
                  'Optional in the bid request and bid response')
    @allure.description('Verify "privacy icon" and "privacy url" is optional field'
                        ' for native type placement via meister ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_optional_field_native_image_for_meister(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        native_request = bid_request['imp'][0]['native']['request']
        native_request = str_to_json(native_request)
        assets = native_request['assets']
        for x in assets:
            if x['id'] == 9 or x['id'] == 10:
                assert_keys_not_exist(x, 'required')
            else:
                continue


    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3599 Exchange - Update "privacy icon", and "privacy url" from Required to '
                  'Optional in the bid request and bid response')
    @allure.description('Verify "privacy icon" and "privacy url" is optional field'
                        ' for native type placement via meister ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_optional_field_native_image_for_meister(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        native_request = bid_request['imp'][0]['native']['request']
        native_request = str_to_json(native_request)
        assets = native_request['assets']
        for x in assets:
            if x['id'] == 9 or x['id'] == 10:
                assert_keys_not_exist(x, 'required')
            else:
                continue

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3599 Exchange - Update "privacy icon", and "privacy url" from Required to '
                  'Optional in the bid request and bid response')
    @allure.description('Verify "privacy icon" and "privacy url" is optional field'
                        ' for native type placement via non test mode edsp ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_optional_field_native_image_for_non_test_mode_edsp(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        native_request = bid_request['imp'][0]['native']['request']
        native_request = str_to_json(native_request)
        assets = native_request['assets']
        for x in assets:
            if x['id'] == 9 or x['id'] == 10:
                assert_keys_not_exist(x, 'required')
            else:
                continue

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('PBJ-3599 Exchange - Update "privacy icon", and "privacy url" from Required to '
                  'Optional in the bid request and bid response')
    @allure.description('Verify "privacy icon" and "privacy url" is optional field'
                        ' for native type placement via test mode edsp ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_optional_field_native_image_for_test_mode_edsp(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        native_request = bid_request['imp'][0]['native']['request']
        native_request = str_to_json(native_request)
        assets = native_request['assets']
        for x in assets:
            if x['id'] == 9 or x['id'] == 10:
                assert_keys_not_exist(x, 'required')
            else:
                continue

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0', 'test_mode')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections')
    @allure.description('Verify the override value of instl will be passed to bid request for rewarded placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids])
    def test_instl_flag_1(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    # @allure.feature('interstitial flag')
    # @allure.tag('normal', 'v1.177.0', 'test_mode')
    # @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections'
    #               'PBJ-3454 Safeguard "Interstitial" override for RTB connections'
    #               'PBJ-3530 Remove safeguard "Interstitial" override for RTB connections')
    # @allure.description('Verify the override value of instl will be passed to bid request for rewarded placement')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1])
    # def test_instl_flag_2(self, pub_app_id, placement, rtb):
    #     '''
    #         rtb connection setting:
    #         "interstitial": false
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0', 'test_mode')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections')
    @allure.description('Verify the override value of instl will be passed to bid request for interstitial placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids])
    def test_instl_flag_3(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    # @allure.feature('interstitial flag')
    # @allure.tag('normal', 'v1.177.0', 'test_mode')
    # @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections'
    #               'PBJ-3454 Safeguard "Interstitial" override for RTB connections'
    #               'PBJ-3530 Remove safeguard "Interstitial" override for RTB connections')
    # @allure.description('Verify the override value of instl will be passed to bid request for interstitial placement')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement_instl])
    # @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1])
    # def test_instl_flag_4(self, pub_app_id, placement, rtb):
    #     '''
    #         rtb connection setting:
    #         "interstitial": false
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0', 'test_mode')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections')
    @allure.description('Verify the override value of instl will be passed to bid request for banner placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids])
    def test_instl_flag_5(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0', 'test_mode')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections')
    @allure.description('Verify the override value of instl will be passed to bid request for banner placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1])
    def test_instl_flag_6(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": false
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0', 'test_mode')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections')
    @allure.description('Verify the override value of instl will be passed to bid request for mrec placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids])
    def test_instl_flag_7(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    # @allure.feature('interstitial flag')
    # @allure.tag('normal', 'v1.177.0', 'test_mode')
    # @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections'
    #               'PBJ-3454 Safeguard "Interstitial" override for RTB connections'
    #               'PBJ-3530 Remove safeguard "Interstitial" override for RTB connections')
    # @allure.description('Verify the override value of instl will be passed to bid request for mrec placement')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    # @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1])
    # def test_instl_flag_8(self, pub_app_id, placement, rtb):
    #     '''
    #         rtb connection setting:
    #         "interstitial": false
    #     '''
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections')
    @allure.description('Verify the override value of instl will be passed for rewarded placement via eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_instl_flag_1_ext(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections'
                  'PBJ-3454 Safeguard "Interstitial" override for RTB connections')
    @allure.description('Verify the override value of instl will not be passed for rewarded placement via eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_1])
    def test_instl_flag_2_ext(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": false
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections')
    @allure.description('Verify the override value of instl will be passed for interstitial placement via eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_instl_flag_3_ext(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections'
                  'PBJ-3454 Safeguard "Interstitial" override for RTB connections')
    @allure.description('Verify the override value of instl will be passed to for interstitial placement via eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_1])
    def test_instl_flag_4_ext(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": false
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections')
    @allure.description('Verify the override value of instl will be passed for banner placement via eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_instl_flag_5_ext(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections')
    @allure.description('Verify the override value of instl will be passed for banner placement via eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_mraid_1])
    def test_instl_flag_6_ext(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": false
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections')
    @allure.description('Verify the override value of instl will be passed for banner placement via eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_instl_flag_7_ext(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.177.0')
    @allure.story('PBJ-3222 RTB :: Introduce Interstitial Flag Controllability for RTB Banner Connections'
                  'PBJ-3454 Safeguard "Interstitial" override for RTB connections')
    @allure.description('Verify the override value of instl will not be passed for banner placement via eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_mraid_1])
    def test_instl_flag_8_ext(self, pub_app_id, placement, rtb):
        '''
            rtb connection setting:
            "interstitial": false
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for banner via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_instl_flag_wo_1(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for banner via edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('rtb', [ext1_non_test_mode_kraken_rtb_ids_mraid])
    def test_instl_flag_wo_2(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for mrec via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_video_mrec_placement])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_instl_flag_wo_3(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for mrec via edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    @pytest.mark.parametrize('rtb', [ext1_non_test_mode_kraken_rtb_ids_mraid])
    def test_instl_flag_wo_4(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for rewarded via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_instl_flag_wo_5(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for rewarded via edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_instl_flag_wo_6(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for interstitial via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_instl_flag_wo_7(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for interstitial via edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_instl_flag_wo_8(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    # @allure.feature('interstitial flag')
    # @allure.tag('normal', 'v1.183.0', 'test_mode')
    # @allure.story('PBJ-3454 Safeguard "Interstitial" override for RTB connections'
    #               'PBJ-3530 Remove safeguard "Interstitial" override for RTB connections')
    # @allure.description('Verify the no instl in bid request if rtb sets instl as false for instl placement via idsp')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement_instl])
    # @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1])
    # def test_instl_flag_rtb_1(self, pub_app_id, placement, rtb):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
    # 
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    # 
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_not_exist(bid_request['imp'][0], 'instl')
    # 
    # @allure.feature('interstitial flag')
    # @allure.tag('normal', 'v1.183.0', 'test_mode')
    # @allure.story('PBJ-3454 Safeguard "Interstitial" override for RTB connections'
    #               'PBJ-3530 Remove safeguard "Interstitial" override for RTB connections'
    #               )
    # @allure.description('Verify the no instl in bid request if rtb sets instl as false for instl placement via edsp')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement_instl])
    # @pytest.mark.parametrize('rtb', [ext_test_mode_kraken_rtb_ids_vast_1])
    # def test_instl_flag_rtb_2(self, pub_app_id, placement, rtb):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
    # 
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    # 
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_not_exist(bid_request['imp'][0], 'instl')
    # 
    # @allure.feature('interstitial flag')
    # @allure.tag('normal', 'v1.183.0', 'test_mode')
    # @allure.story('PBJ-3454 Safeguard "Interstitial" override for RTB connections'
    #               'PBJ-3530 Remove safeguard "Interstitial" override for RTB connections')
    # @allure.description('Verify no instl in bid request if rtb sets instl as false for rewarded placement via idsp'
    #                     )
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_1])
    # def test_instl_flag_rtb_3(self, pub_app_id, placement, rtb):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
    # 
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    # 
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_not_exist(bid_request['imp'][0], 'instl')
    # 
    # @allure.feature('interstitial flag')
    # @allure.tag('normal', 'v1.183.0', 'test_mode')
    # @allure.story('PBJ-3454 Safeguard "Interstitial" override for RTB connections'
    #               'PBJ-3530 Remove safeguard "Interstitial" override for RTB connections')
    # @allure.description('Verify no instl in bid request if rtb sets instl as false for rewarded placement via edsp')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('rtb', [ext_test_mode_kraken_rtb_ids_vast_1])
    # def test_instl_flag_rtb_4(self, pub_app_id, placement, rtb):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
    # 
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    # 
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.183.0', 'test_mode')
    @allure.story('PBJ-3454 Safeguard "Interstitial" override for RTB connections'
                  )
    @allure.description('Verify instl in bid request follows placement if no setting on rtb '
                        'for rewarded placement via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_2])
    def test_instl_flag_rtb_5(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.183.0', 'test_mode')
    @allure.story('PBJ-3454 Safeguard "Interstitial" override for RTB connections')
    @allure.description('Verify the instl in bid request follows placement if no setting on rtb '
                        'for rewarded placement via edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_test_mode_kraken_rtb_ids_vast])
    def test_instl_flag_rtb_6(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.183.0', 'test_mode')
    @allure.story('PBJ-3454 Safeguard "Interstitial" override for RTB connections')
    @allure.description('Verify the instl in bid request follows placement if no setting on rtb '
                        'for instl placement via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids_2])
    def test_instl_flag_rtb_7(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.183.0', 'test_mode')
    @allure.story('PBJ-3454 Safeguard "Interstitial" override for RTB connections')
    @allure.description('Verify the instl in bid request follows placement if no setting on rtb '
                        'for instl placement via edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [ext_test_mode_kraken_rtb_ids_vast])
    def test_instl_flag_rtb_8(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.183.0', 'test_mode')
    @allure.story('PBJ-3451 instl tag missing in the bid request for interstitial placement')
    @allure.description('Verify the instl in bid request for instl placement via '
                        'multiple idsp with different instl setting')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    def test_instl_flag_rtb_9(self, pub_app_id, placement):
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids_2.split(',')[0] + ',' + test_mode_kraken_rtb_ids_5.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids_2.split(',')[1] + ',' + test_mode_kraken_rtb_ids_5.split(',')[1]

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    # @allure.feature('interstitial flag')
    # @allure.tag('normal', 'v1.183.0', 'test_mode')
    # @allure.story('PBJ-3451 instl tag missing in the bid request for interstitial placement')
    # @allure.description('Verify the instl in bid request for instl placement via '
    #                     'multiple edsp with different instl setting')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement_instl])
    # def test_instl_flag_rtb_10(self, pub_app_id, placement):
    #     if env == 'ci':
    #         rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0] + ',' + \
    #               ext_test_mode_kraken_rtb_ids_vast_1.split(',')[0]
    #     elif env == 'qa' or env == 'regression':
    #         rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1] + ',' + \
    #               ext_test_mode_kraken_rtb_ids_vast_1.split(',')[1]
    # 
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
    # 
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
    # 
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify 320x480 Mapping for liftoff and other edsps on android platform")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_fullscreen_inter_playable_placement,
                                           android_fullscreen_reward_playable_placement])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_android_path, '320x480 Mapping'))
    def test_320_480_mapping_on_android(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(320))
        assert_that(imp[0]['video']['w'], equal_to(480))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(320))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(480))
            assert_that(imp[0]['banner']['h'], equal_to(320))
            assert_that(imp[0]['banner']['w'], equal_to(480))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify 480x320 Mapping for liftoff and other edsps on android platform")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_fullscreen_inter_playable_placement,
                                           android_fullscreen_reward_playable_placement])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_android_path, '480x320 Mapping'))
    def test_480_320_mapping_on_android(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(480))
        assert_that(imp[0]['video']['w'], equal_to(320))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(480))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(320))
            assert_that(imp[0]['banner']['h'], equal_to(480))
            assert_that(imp[0]['banner']['w'], equal_to(320))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify 768x1024 Mapping for liftoff and other edsps on android platform")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_fullscreen_inter_playable_placement,
                                           android_fullscreen_reward_playable_placement])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_android_path, '768x1024 Mapping'))
    def test_768_1024_mapping_on_android(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(768))
        assert_that(imp[0]['video']['w'], equal_to(1024))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(768))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(1024))
            assert_that(imp[0]['banner']['h'], equal_to(768))
            assert_that(imp[0]['banner']['w'], equal_to(1024))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify 1024x768 Mapping for liftoff and other edsps on android platform")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_fullscreen_inter_playable_placement,
                                           android_fullscreen_reward_playable_placement])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_android_path, '1024x768 Mapping'))
    def test_1024_768_mapping_on_android(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(1024))
        assert_that(imp[0]['video']['w'], equal_to(768))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(1024))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(768))
            assert_that(imp[0]['banner']['h'], equal_to(1024))
            assert_that(imp[0]['banner']['w'], equal_to(768))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify h&w for existing in both 320x480 and 768x1024 "
                        "for deviceType is phone on android platform")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_fullscreen_inter_playable_placement,
                                           android_fullscreen_reward_playable_placement])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_android_path,
                                                            'Exists in both 320x480 and 768x1024'))
    def test_320_480_mapping_for_phone_on_android(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                                w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        imp = bid_request['imp']
        assert_that(device['devicetype'], equal_to(4))
        assert_that(imp[0]['video']['h'], equal_to(320))
        assert_that(imp[0]['video']['w'], equal_to(480))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(320))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(480))
            assert_that(imp[0]['banner']['h'], equal_to(320))
            assert_that(imp[0]['banner']['w'], equal_to(480))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify real h&w mapping")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_fullscreen_inter_playable_placement,
                                           android_fullscreen_reward_playable_placement])
    def test_real_h_w_mapping_on_android(self, pub_app_id, placement, rtbs):

        request_payload_h = 1234
        request_payload_w = 111

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                                w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        imp = bid_request['imp']
        assert_that(device['devicetype'], equal_to(4))
        assert_that(imp[0]['video']['h'], equal_to(1234))
        assert_that(imp[0]['video']['w'], equal_to(111))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(1234))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(111))
            assert_that(imp[0]['banner']['h'], equal_to(1234))
            assert_that(imp[0]['banner']['w'], equal_to(111))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify h&w for existing in both 320x480 and 768x1024 "
                        "for deviceType is tablet on android platform")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_fullscreen_inter_playable_placement,
                                           android_fullscreen_reward_playable_placement])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_android_path,
                                                            'Exists in both 320x480 and 768x1024'))
    def test_768_1024_mapping_for_tablet_on_android(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        test_ua = "Mozilla/5.0 (Linux; Android 7.0; SM-T819 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko)" \
                  " Version/4.0 Chrome/83.0.4103.101 Safari/537.36,SM-G965N,Samsung,4"
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                                w=request_payload_w, ua=test_ua)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        imp = bid_request['imp']
        assert_that(device['devicetype'], equal_to(5))
        assert_that(imp[0]['video']['h'], equal_to(768))
        assert_that(imp[0]['video']['w'], equal_to(1024))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(768))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(1024))
            assert_that(imp[0]['banner']['h'], equal_to(768))
            assert_that(imp[0]['banner']['w'], equal_to(1024))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify h&w for existing in both 480x320 and 1024x768 "
                        "for deviceType is phone on android platform")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_fullscreen_inter_playable_placement,
                                           android_fullscreen_reward_playable_placement])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_android_path,
                                                            'Exists in both 480x320 and 1024x768'))
    def test_480_320_mapping_for_phone_on_android(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                                w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        imp = bid_request['imp']
        assert_that(device['devicetype'], equal_to(4))
        assert_that(imp[0]['video']['h'], equal_to(480))
        assert_that(imp[0]['video']['w'], equal_to(320))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(480))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(320))
            assert_that(imp[0]['banner']['h'], equal_to(480))
            assert_that(imp[0]['banner']['w'], equal_to(320))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify h&w for existing in both 480x320 and 1024x768 "
                        "for deviceType is tablet on android platform")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_fullscreen_inter_playable_placement,
                                           android_fullscreen_reward_playable_placement])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_android_path,
                                                            'Exists in both 480x320 and 1024x768'))
    def test_1024_768_mapping_for_tablet_on_android(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        test_ua = "Mozilla/5.0 (Linux; Android 7.0; SM-T819 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko)" \
                  " Version/4.0 Chrome/83.0.4103.101 Safari/537.36,SM-G965N,Samsung,4"
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                                w=request_payload_w, ua=test_ua)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        device = bid_request['device']
        imp = bid_request['imp']
        assert_that(device['devicetype'], equal_to(5))
        assert_that(imp[0]['video']['h'], equal_to(1024))
        assert_that(imp[0]['video']['w'], equal_to(768))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(1024))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(768))
            assert_that(imp[0]['banner']['h'], equal_to(1024))
            assert_that(imp[0]['banner']['w'], equal_to(768))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify 320x480 Mapping for liftoff on ios platform")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_third_party_placement_crtype_01])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_ios_path, '320x480 Mapping'))
    def test_320_480_mapping_on_ios(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(320))
        assert_that(imp[0]['video']['w'], equal_to(480))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(320))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(480))
            assert_that(imp[0]['banner']['h'], equal_to(320))
            assert_that(imp[0]['banner']['w'], equal_to(480))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify 480x320 Mapping for liftoff on ios platform")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_third_party_placement_crtype_01])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_ios_path, '480x320 Mapping'))
    def test_480_320_mapping_on_ios(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(480))
        assert_that(imp[0]['video']['w'], equal_to(320))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(480))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(320))
            assert_that(imp[0]['banner']['h'], equal_to(480))
            assert_that(imp[0]['banner']['w'], equal_to(320))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify 768x1024 Mapping for liftoff on ios platform")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_third_party_placement_crtype_01])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_ios_path, '768x1024 Mapping'))
    def test_768_1024_mapping_on_ios(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(768))
        assert_that(imp[0]['video']['w'], equal_to(1024))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(768))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(1024))
            assert_that(imp[0]['banner']['h'], equal_to(768))
            assert_that(imp[0]['banner']['w'], equal_to(1024))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify 1024x768 Mapping Mapping for liftoff on ios platform")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_third_party_placement_crtype_01])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('data', read_one_column_of_csv(device_mapping_ios_path, '1024x768 Mapping'))
    def test_1024_768_mapping_on_ios(self, pub_app_id, placement, data, rtbs):

        request_payload_h = int(data.split('x')[0])
        request_payload_w = int(data.split('x')[1])

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(1024))
        assert_that(imp[0]['video']['w'], equal_to(768))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(1024))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(768))
            assert_that(imp[0]['banner']['h'], equal_to(1024))
            assert_that(imp[0]['banner']['w'], equal_to(768))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3556 AdRequest Size Standardization//Consolidation to LiftOff DSP'
                  'PBJ-3715 Bid request for fullscreen playables contains the correct video and banner '
                  'width & height for LO'
                  'PBJ-3848 Size Consolidation to all eDSPs')
    @allure.description("Verify real h&w Mapping Mapping for liftoff on ios platform")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('rtbs', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                      ext1_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_third_party_placement_crtype_01])
    def test_real_h_w_mapping_on_ios(self, pub_app_id, placement, rtbs):

        request_payload_h = 1234
        request_payload_w = 234

        if env == 'ci':
            rtb = rtbs.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtbs.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(1234))
        assert_that(imp[0]['video']['w'], equal_to(234))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(1234))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(234))
            assert_that(imp[0]['banner']['h'], equal_to(1234))
            assert_that(imp[0]['banner']['w'], equal_to(234))

    @allure.feature('device mapping')
    @allure.tag('normal', 'v1.193.0')
    @allure.story('PBJ-3616 Size Consolidation A/B testing to all eDSPs')
    @allure.description("Verify device mapping works for the rtb in experiment white list for iOS")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_third_party_placement_crtype_01])
    def test_device_mapping_ab_testing_1(self, pub_app_id, placement):
        # In the '480x320' Mapping
        request_payload_h = 1792
        request_payload_w = 828

        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(480))
        assert_that(imp[0]['video']['w'], equal_to(320))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(480))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(320))
            assert_that(imp[0]['banner']['h'], equal_to(480))
            assert_that(imp[0]['banner']['w'], equal_to(320))

    @allure.feature('device mapping')
    @allure.tag('normal', 'v1.193.0')
    @allure.story('PBJ-3616 Size Consolidation A/B testing to all eDSPs')
    @allure.description("Verify device mapping works for the rtb in experiment white list for Android")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_fullscreen_inter_playable_placement])
    def test_device_mapping_ab_testing_2(self, pub_app_id, placement):
        # In the 'Exists in both 480x320 and 1024x768' Mapping
        request_payload_h = 1920
        request_payload_w = 1080

        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                                w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(480))
        assert_that(imp[0]['video']['w'], equal_to(320))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(480))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(320))
            assert_that(imp[0]['banner']['h'], equal_to(480))
            assert_that(imp[0]['banner']['w'], equal_to(320))

    @allure.feature('device mapping')
    @allure.tag('normal', 'v1.193.0')
    @allure.story('PBJ-3616 Size Consolidation A/B testing to all eDSPs')
    @allure.description("Verify that the rtb not in experiment white list will not be impacted for iOS")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, common_test_third_party_placement_crtype_01])
    def test_device_mapping_ab_testing_3(self, pub_app_id, placement):
        # In the '480x320' Mapping
        request_payload_h = 1792
        request_payload_w = 828

        if env == 'ci':
            rtb = meister_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = meister_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(request_payload_h))
        assert_that(imp[0]['video']['w'], equal_to(request_payload_w))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(request_payload_h))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(request_payload_w))
            assert_that(imp[0]['banner']['h'], equal_to(request_payload_h))
            assert_that(imp[0]['banner']['w'], equal_to(request_payload_w))

    @allure.feature('device mapping')
    @allure.tag('normal', 'v1.193.0')
    @allure.story('PBJ-3616 Size Consolidation A/B testing to all eDSPs')
    @allure.description("Verify that the rtb not in experiment white list will not be impacted for Android")
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement, android_common_test_placement_legacy])
    def test_device_mapping_ab_testing_4(self, pub_app_id, placement):
        # In the 'Exists in both 480x320 and 1024x768' Mapping
        request_payload_h = 1920
        request_payload_w = 1080

        if env == 'ci':
            rtb = meister_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = meister_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), h=request_payload_h,
                                                w=request_payload_w)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['video']['h'], equal_to(request_payload_h))
        assert_that(imp[0]['video']['w'], equal_to(request_payload_w))
        if "banner" in imp[0]:
            assert_that(imp[0]['banner']['format'][0]['h'], equal_to(request_payload_h))
            assert_that(imp[0]['banner']['format'][0]['w'], equal_to(request_payload_w))
            assert_that(imp[0]['banner']['h'], equal_to(request_payload_h))
            assert_that(imp[0]['banner']['w'], equal_to(request_payload_w))



    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3616 Size Consolidation A/B testing to all eDSPs')
    @allure.description("Verify Verify ad size experiment only be available for video and playable, "
                        "banner is not target of ad size experiment.")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_device_mapping_ab_not_avaiable_for_banner_placement(self, pub_app_id, placement):
        # In the '480x320' Mapping
        request_payload_h = 1792
        request_payload_w = 828

        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w, banner=True)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['banner']['format'][0]['h'], equal_to(90))
        assert_that(imp[0]['banner']['format'][0]['w'], equal_to(728))
        assert_that(imp[0]['banner']['h'], equal_to(90))
        assert_that(imp[0]['banner']['w'], equal_to(728))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3616 Size Consolidation A/B testing to all eDSPs')
    @allure.description("Verify Verify ad size experiment only be available for video and playable, "
                        "banner is not target of ad size experiment.")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_device_mapping_ab_not_avaiable_for_banner_placement_01(self, pub_app_id, placement):
        # In the 'Exists in both 480x320 and 1024x768' Mapping
        request_payload_h = 1920
        request_payload_w = 1080

        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w, banner=True)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['banner']['format'][0]['h'], equal_to(90))
        assert_that(imp[0]['banner']['format'][0]['w'], equal_to(728))
        assert_that(imp[0]['banner']['h'], equal_to(90))
        assert_that(imp[0]['banner']['w'], equal_to(728))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3616 Size Consolidation A/B testing to all eDSPs')
    @allure.description("Verify Verify ad size experiment only be available for video and playable, "
                        "banner is not target of ad size experiment.")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_device_mapping_ab_not_avaiable_for_banner_placement_02(self, pub_app_id, placement):
        # In the '480x320' Mapping
        request_payload_h = 1792
        request_payload_w = 828

        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w, banner=True)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['banner']['format'][0]['h'], equal_to(90))
        assert_that(imp[0]['banner']['format'][0]['w'], equal_to(728))
        assert_that(imp[0]['banner']['h'], equal_to(90))
        assert_that(imp[0]['banner']['w'], equal_to(728))

    @allure.feature('device mapping')
    @allure.tag('normal')
    @allure.story('PBJ-3616 Size Consolidation A/B testing to all eDSPs')
    @allure.description("Verify Verify ad size experiment only be available for video and playable, "
                        "banner is not target of ad size experiment.")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_device_mapping_ab_not_avaiable_for_banner_placement_03(self, pub_app_id, placement):
        # In the 'Exists in both 480x320 and 1024x768' Mapping
        request_payload_h = 1920
        request_payload_w = 1080

        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), h=request_payload_h,
                                            w=request_payload_w, banner=True)

        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        imp = bid_request['imp']
        assert_that(imp[0]['banner']['format'][0]['h'], equal_to(90))
        assert_that(imp[0]['banner']['format'][0]['w'], equal_to(728))
        assert_that(imp[0]['banner']['h'], equal_to(90))
        assert_that(imp[0]['banner']['w'], equal_to(728))

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-3901 Set floor to be at $0.01 cent for LiftOff DSP'
                  'PBJ-3975 Update bid floor for LiftOff DSP'
                  'PBJ-4036 Change price Rtb filter for Liftoff according to dynamic bid floor.')
    @allure.description('Verify bid floor is $0.15 for the header bidding traffic via the LO eDSP RTB, video, non-US')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True])
    @pytest.mark.parametrize('sdkv', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('bid_price', [0.01, 0.15, 1])
    def test_liftoff_bid_floor_1(self, pub_app_id, placement, hb, sdkv, bid_price):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[1]
        override_price_any = bid_price
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, sdk_version=sdkv,
                                          override_price_any=override_price_any))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(0.15))
        bid_floor = (bid_request['imp'][0]['bidfloor'])
        if bid_price < bid_floor:
            # Verify jaeger will not serve in case of bid price is lower than bidfloor.
            assert_keys_exist(ad_markup, 'sleep')
            assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        else:
            assert_keys_not_exist(ad_markup, 'sleep')


    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-3901 Set floor to be at $0.01 cent for LiftOff DSP'
                  'PBJ-4036 Change price Rtb filter for Liftoff according to dynamic bid floor.'
                  )
    @allure.description('Verify it will not impact the non-header bidding traffic via the LO eDSP RTB')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [False])
    @pytest.mark.parametrize('sdkv', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('bid_price', [0.01, 1, 1.2])
    def test_liftoff_bid_floor_2(self, pub_app_id, placement, hb, sdkv, bid_price):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[1]

        override_price_any = bid_price
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, sdk_version=sdkv,
                                          override_price_any=override_price_any))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(1))
        bid_floor = (bid_request['imp'][0]['bidfloor'])
        if bid_price < bid_floor:
            # Verify jaeger will not serve in case of bid price is lower than bidfloor.
            assert_keys_exist(ad_markup, 'sleep')
            assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        else:
            assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-3975 Update bid floor for LiftOff DSP'
                  'PBJ-4036 Change price Rtb filter for Liftoff according to dynamic bid floor.')
    @allure.description('Verify bid floor is $0.5 for the header bidding traffic via the LO eDSP RTB, video, US')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdkv', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('bid_price', [0.01, 0.5, 1.2])
    def test_liftoff_bid_floor_3(self, pub_app_id, placement, sdkv, bid_price):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[1]
        override_price_any = bid_price
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip, rtb_selector=rtb, sdk_version=sdkv,
                                          override_price_any=override_price_any))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(0.5))
        bid_floor = (bid_request['imp'][0]['bidfloor'])
        if bid_price < bid_floor:
            # Verify jaeger will not serve in case of bid price is lower than bidfloor.
            assert_keys_exist(ad_markup, 'sleep')
            assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        else:
            assert_keys_not_exist(ad_markup, 'sleep')


    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-3975 Update bid floor for LiftOff DSP'
                  'PBJ-4036 Change price Rtb filter for Liftoff according to dynamic bid floor.')
    @allure.description('Verify bid floor is $0.05 for the header bidding traffic via the LO eDSP RTB, banner, non-US')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('sdkv', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('bid_price', [0.01, 0.05, 1.2])
    def test_liftoff_bid_floor_4(self, pub_app_id, placement, sdkv, bid_price):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[1]

        override_price_any = bid_price
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, sdk_version=sdkv,
                                          override_price_any=override_price_any
                                          ))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(0.05))
        bid_floor = (bid_request['imp'][0]['bidfloor'])
        if bid_price < bid_floor:
            # Verify jaeger will not serve in case of bid price is lower than bidfloor.
            assert_keys_exist(ad_markup, 'sleep')
            assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        else:
            assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-3975 Update bid floor for LiftOff DSP'
                  'PBJ-4036 Change price Rtb filter for Liftoff according to dynamic bid floor.')
    @allure.description('Verify bid floor is the default value for the header bidding traffic via the LO eDSP RTB, '
                        'banner, US')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('sdkv', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('bid_price', [0.01, 1, 1.2])
    def test_liftoff_bid_floor_5(self, pub_app_id, placement, sdkv, bid_price):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[1]
        override_price_any = bid_price
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip, rtb_selector=rtb, sdk_version=sdkv,
                                          override_price_any=override_price_any))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # reserved floor
        bid_floor = 1
        if bid_price < bid_floor:
            # Verify jaeger will not serve in case of bid price is lower than bidfloor.
            assert_keys_exist(ad_markup, 'sleep')
            assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        else:
            assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-3975 Update bid floor for LiftOff DSP'
                  'PBJ-4036 Change price Rtb filter for Liftoff according to dynamic bid floor.')
    @allure.description('Verify bid floor is the default value for the header bidding traffic via the LO eDSP RTB, '
                        'mrec, non-US')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    @pytest.mark.parametrize('sdkv', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('bid_price', [1, 2.5, 3.6])
    def test_liftoff_bid_floor_6(self, pub_app_id, placement, sdkv, bid_price):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[1]

        override_price_any = bid_price
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip, rtb_selector=rtb, sdk_version=sdkv,
                                          override_price_any=override_price_any))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2.5))
        bid_floor = (bid_request['imp'][0]['bidfloor'])
        if bid_price < bid_floor:
            # Verify jaeger will not serve in case of bid price is lower than bidfloor.
            assert_keys_exist(ad_markup, 'sleep')
            assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        else:
            assert_keys_not_exist(ad_markup, 'sleep')


    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-3975 Update bid floor for LiftOff DSP'
                  'PBJ-4036 Change price Rtb filter for Liftoff according to dynamic bid floor.')
    @allure.description('Verify bid floor is the default value for the header bidding traffic via the LO eDSP RTB, '
                        'mrec, US')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_programmatic_mrec_placement])
    @pytest.mark.parametrize('sdkv', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('bid_price', [0.99, 1, 3.6])
    def test_liftoff_bid_floor_7(self, pub_app_id, placement, sdkv, bid_price):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[1]
        override_price_any = bid_price
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip, rtb_selector=rtb, sdk_version=sdkv,
                                          override_price_any=override_price_any
                                          ))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(1))
        bid_floor = (bid_request['imp'][0]['bidfloor'])
        if bid_price < bid_floor:
            # Verify jaeger will not serve in case of bid price is lower than bidfloor.
            assert_keys_exist(ad_markup, 'sleep')
            assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        else:
            assert_keys_not_exist(ad_markup, 'sleep')


    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-3975 Update bid floor for LiftOff DSP'
                  'PBJ-4036 Change price Rtb filter for Liftoff according to dynamic bid floor.')
    @allure.description('Verify bid floor is the default value for the header bidding traffic via the LO eDSP RTB, '
                        'mrec, US for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_preCache_mrec_test_placement])
    @pytest.mark.parametrize('sdkv', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('bid_price', [0.99, 1, 3.6])
    def test_liftoff_bid_floor_8(self, pub_app_id, placement, sdkv, bid_price):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[1]
        override_price_any = bid_price
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip, rtb_selector=rtb, sdk_version=sdkv,
                                          override_price_any=override_price_any
                                          ))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(1))
        bid_floor = (bid_request['imp'][0]['bidfloor'])
        if bid_price < bid_floor:
            # Verify jaeger will not serve in case of bid price is lower than bidfloor.
            assert_keys_exist(ad_markup, 'sleep')
            assert_that(ad_markup['info'], equal_to('impression auctioned but unsold'))
        else:
            assert_keys_not_exist(ad_markup, 'sleep')

    @allure.feature('bid floor')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4608 Jaeger - Do not send bid request to eDSP if bid floor larger than a threshold')
    @allure.description('Verify jaeger will not serve for edsp bidfloor>=5000')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919-2'])
    @pytest.mark.parametrize('country', [ir_ip])
    def test_threshold_for_bid_floor_e(self, pub_app_id, placement, country):
        """
        ir
        reserve_floor: 5000
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=country,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(5000))
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, "sleep")


    @allure.feature('bid floor')
    @allure.tag('normal', 'v1.240.0')
    @allure.story('PBJ-4608 Jaeger - Do not send bid request to eDSP if bid floor larger than a threshold')
    @allure.description('Verify jaeger will serve for idsp bidfloor>=5000')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919-2'])
    @pytest.mark.parametrize('country', [ir_ip])
    def test_threshold_for_bid_floor_i(self, pub_app_id, placement, country):
        """
        ir
        reserve_floor: 5000
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=country,
                                          rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(5000))
        assert_keys_not_exist(response_payload, "sleep")



    @allure.feature('bid floor')
    @allure.tag('normal', 'test_mode', 'v1.240.0')
    @allure.story('PBJ-4608 Jaeger - Do not send bid request to eDSP if bid floor larger than a threshold')
    @allure.description('Verify jaeger will not serve for edsp bidfloor>=5000')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919-2'])
    @pytest.mark.parametrize('country', [ir_ip])
    def test_threshold_for_bid_floor_e_test_mode(self, pub_app_id, placement, country):
        """
        ir
        reserve_floor: 5000
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=country,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['bidfloor'], equal_to(5000))
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, "sleep")




