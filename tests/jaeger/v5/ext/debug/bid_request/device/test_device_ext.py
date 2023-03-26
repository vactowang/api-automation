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
class TestDeviceExt(object):

    @allure.feature('bid request device')
    @allure.tag('normal', 'R_1.153.0')
    @allure.story('PBJ-2363 Jaeger bid request muted field should be correct')
    @allure.description('Verify the muted in bid request should be 0 when sound_enabled is 1 for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sound_enabled', [1])
    def test_sound_enabled_android_1(self, pub_app_id, placement, sound_enabled):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(),
                                                sound_enabled=sound_enabled)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['ext']['vungle']['muted'], equal_to(0))

    @allure.feature('bid request device')
    @allure.tag('normal', 'R_1.153.0')
    @allure.story('PBJ-2363 Jaeger bid request muted field should be correct')
    @allure.description('Verify the muted in bid request should be 1 when sound_enabled is 0 for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sound_enabled', [0, None])
    def test_sound_enabled_android_2(self, pub_app_id, placement, sound_enabled):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(),
                                                sound_enabled=sound_enabled)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['ext']['vungle']['muted'], equal_to(1))

    @allure.feature('bid request device')
    @allure.tag('normal', 'R_1.153.0')
    @allure.story('PBJ-2363 Jaeger bid request muted field should be correct')
    @allure.description('Verify the muted in bid request should be 0 when sound_enabled is 1 for amazon')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    @pytest.mark.parametrize('sound_enabled', [1])
    def test_sound_enabled_amazon_1(self, pub_app_id, placement, sound_enabled):
        req = request_payload.jaeger_v5_amazon(pub_app_id, placement, ifa=gen_device_id(), sound_enabled=sound_enabled)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()

        if 'sleep' not in response_payload['ads'][0]['ad_markup']:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(bid_request['device']['ext']['vungle']['muted'], equal_to(0))

    @allure.feature('bid request device')
    @allure.tag('normal', 'R_1.153.0')
    @allure.story('PBJ-2363 Jaeger bid request muted field should be correct')
    @allure.description('Verify the muted in bid request should be 1 when sound_enabled is 0 for amazon')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    @pytest.mark.parametrize('sound_enabled', [0, None])
    def test_sound_enabled_amazon_2(self, pub_app_id, placement, sound_enabled):
        req = request_payload.jaeger_v5_amazon(pub_app_id, placement, ifa=gen_device_id(), sound_enabled=sound_enabled)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()

        if 'sleep' not in response_payload['ads'][0]['ad_markup']:
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(bid_request['device']['ext']['vungle']['muted'], equal_to(1))

    @allure.feature('bid request device')
    @allure.tag('normal', 'R_1.153.0')
    @allure.story('PBJ-2363 Jaeger bid request muted field should be correct')
    @allure.description('Verify the muted in bid request should be 1 when sound_enabled is 1 for ios')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sound_enabled', [1])
    def test_sound_enabled_ios_1(self, pub_app_id, placement, sound_enabled):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), sound_enabled=sound_enabled)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['ext']['vungle']['muted'], equal_to(1))

    @allure.feature('bid request device')
    @allure.tag('normal', 'R_1.153.0')
    @allure.story('PBJ-2363 Jaeger bid request muted field should be correct')
    @allure.description('Verify the muted in bid request should be 1 when sound_enabled is 0 for ios')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sound_enabled', [0, None])
    def test_sound_enabled_ios_2(self, pub_app_id, placement, sound_enabled):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), sound_enabled=sound_enabled)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['ext']['vungle']['muted'], equal_to(1))

    @allure.feature('bid request device')
    @allure.tag('normal', 'v1.166.0')
    @allure.story('PBJ-2870 Passing IDFV to specific RTB partners')
    @allure.description('Verify that IDFV always pass to Meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_idsp_1(self, pub_app_id, placement):
        idfv = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['ext']['vungle']['idfv'], equal_to(idfv))

    @allure.feature('bid request device')
    @allure.tag('normal', 'v1.166.0', 'test_mode')
    @allure.story('PBJ-2870 Passing IDFV to specific RTB partners')
    @allure.description('Verify that IDFV always pass to iDSP when allow_idfv is true in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_idsp_2(self, pub_app_id, placement):
        idfv = test_mode_device_id
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv, ifa='')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['ext']['vungle']['idfv'], equal_to(idfv))

    @allure.feature('bid request device')
    @allure.tag('normal', 'v1.166.0', 'test_mode')
    @allure.story('PBJ-2870 Passing IDFV to specific RTB partners')
    @allure.description('Verify that IDFV always pass to iDSP when allow_idfv is false in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_idsp_3(self, pub_app_id, placement):
        idfv = test_mode_device_id
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv, ifa='')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['ext']['vungle']['idfv'], equal_to(idfv))

    @allure.feature('bid request device')
    @allure.tag('normal', 'v1.166.0')
    @allure.story('PBJ-2870 Passing IDFV to specific RTB partners')
    @allure.description('Verify that IDFV always pass to iDSP when allow_idfv is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_idsp_4(self, pub_app_id, placement):
        idfv = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['ext']['vungle']['idfv'], equal_to(idfv))

    @allure.feature('bid request device')
    @allure.tag('normal', 'v1.166.0')
    @allure.story('PBJ-2870 Passing IDFV to specific RTB partners')
    @allure.description('Verify that IDFV pass to eDSP when allow_idfv is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_edsp_1(self, pub_app_id, placement):
        idfv = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['ext']['idfv'], equal_to(idfv))

    @allure.feature('bid request device')
    @allure.tag('normal', 'v1.166.0', 'test_mode')
    @allure.story('PBJ-2870 Passing IDFV to specific RTB partners')
    @allure.description('Verify that IDFV pass to eDSP when allow_idfv is true in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_edsp_2(self, pub_app_id, placement):
        idfv = test_mode_device_id
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv, ifa='')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_wurfl))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(bid_request['device']['ext']['idfv'], equal_to(idfv))

    @allure.feature('bid request device')
    @allure.tag('normal', 'v1.166.0', 'test_mode')
    @allure.story('PBJ-2870 Passing IDFV to specific RTB partners')
    @allure.description('Verify that IDFV does not pass to iDSP when allow_idfv is false in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_edsp_3(self, pub_app_id, placement):
        idfv = test_mode_device_id
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv, ifa='')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(bid_request['device']['ext'], 'idfv')

    @allure.feature('bid request device')
    @allure.tag('normal', 'v1.166.0')
    @allure.story('PBJ-2870 Passing IDFV to specific RTB partners')
    @allure.description('Verify that IDFV does not pass to iDSP when allow_idfv is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_idfv_edsp_4(self, pub_app_id, placement):
        idfv = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(bid_request['device']['ext'], 'idfv')

    @allure.feature('bid request device')
    @allure.tag('normal')
    @allure.story('PBJ-3781 Send Vungle Device extension to LiftOff')
    @allure.description('Verify that exist vungle extension and IDFV pass to liftoff when allow_idfv is true')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_liftoff_device_ext_01(self, pub_app_id, placement, rtb):
        idfv = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa='', idfv=idfv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(bid_request['device']['ext'], 'vungle')
        vungle_ext = bid_request['device']['ext']['vungle']
        assert_that(vungle_ext['idfv'], equal_to(idfv))
        assert_keys_exist(vungle_ext, 'battery_level')
        assert_keys_exist(vungle_ext, 'battery_optimization')
        assert_that(vungle_ext['id_source'], equal_to('IDFV'))
        assert_that(bid_request['device']['ext']['idfv'], equal_to(idfv))

    @allure.feature('bid request device')
    @allure.tag('normal')
    @allure.story('PBJ-3781 Send Vungle Device extension to LiftOff')
    @allure.description('Verify that exist vungle extension and IDFV pass to liftoff when allow_idfv is false')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_liftoff_device_ext_02(self, pub_app_id, placement):
        idfv = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa='', idfv=idfv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid_liftoff))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              ext_non_test_mode_kraken_rtb_ids_mraid_liftoff)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(bid_request['device']['ext'], 'vungle')
        vungle_ext = bid_request['device']['ext']['vungle']
        assert_that(vungle_ext['idfv'], equal_to(idfv))
        assert_keys_exist(vungle_ext, 'battery_level')
        assert_keys_exist(vungle_ext, 'battery_optimization')
        assert_that(vungle_ext['id_source'], equal_to('IDFV'))

    @allure.feature('bid request device')
    @allure.tag('normal')
    @allure.story('PBJ-3781 Send Vungle Device extension to LiftOff')
    @allure.description('Verify that exist vungle extension and IDFV pass to liftoff when allow_idfv is false')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_liftoff_device_ext_03(self, pub_app_id, placement):
        idfv = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid_liftoff))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload,
                                                              ext_non_test_mode_kraken_rtb_ids_mraid_liftoff)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(bid_request['device']['ext'], 'vungle')
        vungle_ext = bid_request['device']['ext']['vungle']
        assert_that(vungle_ext['idfv'], equal_to(idfv))
        assert_keys_exist(vungle_ext, 'battery_level')
        assert_keys_exist(vungle_ext, 'battery_optimization')
        assert_that(vungle_ext['id_source'], equal_to('IFA'))

    @allure.feature('bid request device')
    @allure.tag('normal')
    @allure.story('PBJ-3781 Send Vungle Device extension to LiftOff')
    @allure.description('Verify that exist vungle extension and IDFV pass to liftoff when allow_idfv is true')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_liftoff_device_ext_04(self, pub_app_id, placement, rtb):
        idfv = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(bid_request['device']['ext'], 'vungle')
        vungle_ext = bid_request['device']['ext']['vungle']
        assert_that(vungle_ext['idfv'], equal_to(idfv))
        assert_keys_exist(vungle_ext, 'battery_level')
        assert_keys_exist(vungle_ext, 'battery_optimization')
        assert_that(vungle_ext['id_source'], equal_to('IFA'))

    @allure.feature('bid request device')
    @allure.tag('normal')
    @allure.story('PBJ-4320 Reporting iOS ATT Status')
    @allure.description('Verify that pass att status to downdtreams for edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_att_status_01(self, pub_app_id, placement, rtb):
        idfv = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, idfv=idfv, atts=1)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(bid_request['device']['ext'], 'atts')
        assert_that(bid_request['device']['ext']['atts'], equal_to(1))
        # Verify kafka message


    @allure.feature('bid request device')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4320 Reporting iOS ATT Status')
    @allure.description('Verify that pass att status to downdtreams for test mode edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_test_mode_kraken_rtb_ids_vast])
    def test_att_status_02(self, pub_app_id, placement, rtb):
        ifa = test_mode_device_id
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=ifa, atts=2)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(bid_request['device']['ext'], 'atts')
        assert_that(bid_request['device']['ext']['atts'], equal_to(2))
        # Verify kafka message



    @allure.feature('bid request device')
    @allure.tag('normal')
    @allure.story('PBJ-4320 Reporting iOS ATT Status')
    @allure.description('Verify that pass att status to downdtreams for idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_att_status_03(self, pub_app_id, placement, rtb):
        ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=ifa, atts=2)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(bid_request['device']['ext'], 'atts')
        assert_that(bid_request['device']['ext']['atts'], equal_to(2))
        # Verify kafka message



    @allure.feature('bid request device')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4320 Reporting iOS ATT Status')
    @allure.description('Verify that pass att status to downdtreams for test mode idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids])
    def test_att_status_04(self, pub_app_id, placement, rtb):
        ifa = test_mode_device_id
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=ifa, atts=0)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(bid_request['device']['ext'], 'atts')
        assert_that(bid_request['device']['ext']['atts'], equal_to(0))
        # Verify kafka message



    @allure.feature('bid request device')
    @allure.tag('normal' ,'v1.245.0')
    @allure.story('PBJ-4819 In-Banner Video Muted/Unmuted')
    @allure.description('Verify bidrequest.device.ext.muted field exist if rtb support "consumable"')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_muted_banner_01(self, pub_app_id, placement, rtb):
        ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=ifa, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_exist(bid_request['device']['ext'], 'muted')
        assert_that(bid_request['device']['ext']['muted'], equal_to(1))



    @allure.feature('bid request device')
    @allure.tag('normal' , 'v1.245.0')
    @allure.story('PBJ-4819 In-Banner Video Muted/Unmuted')
    @allure.description('Verify bidrequest.device.ext.muted field exist if rtb does not support "consumable"')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_1])
    def test_muted_banner_02(self, pub_app_id, placement, rtb):
        ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=ifa, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(bid_request['device']['ext'], 'muted')

