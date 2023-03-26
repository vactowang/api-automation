import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain, request_hbp_with_real_time_token, \
    get_ext_debug_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestBidRequestExt(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request ext')
    @allure.description('Verify bid request ext details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_bid_request_ext_schain_details(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(isinstance(bid_request['ext']['schain']['complete'], int))
        assert_that(isinstance(bid_request['ext']['schain']['ver'], str))
        assert_that(isinstance(bid_request['ext']['schain']['nodes'][0]['asi'], str))
        assert_that(isinstance(bid_request['ext']['schain']['nodes'][0]['sid'], str))
        assert_that(isinstance(bid_request['ext']['schain']['nodes'][0]['rid'], str))
        assert_that(isinstance(bid_request['ext']['schain']['nodes'][0]['name'], str))
        assert_that(isinstance(bid_request['ext']['schain']['nodes'][0]['hp'], int))

    @allure.feature('bid request supply chain obj')
    @allure.tag('normal')
    @allure.story('seller.json')
    @allure.description('Test for supply chain obj - sid is not in seller.json')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b1'])
    def test_schain_obj_sid_not_in_seller_json(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        schain_obj = bid_request['ext']['schain']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(schain_obj['ver'], not empty())
        assert_that(schain_obj['complete'], not empty())
        assert_that(schain_obj['nodes'][0]['asi'], not empty())
        assert_that(schain_obj['nodes'][0]['sid'], not empty())
        assert_that(schain_obj['nodes'][0]['name'], not empty())
        assert_that(schain_obj['nodes'][0]['rid'], bid_request['id'])
        assert_that(schain_obj['nodes'][0]['hp'], not empty())

    @allure.feature('bid request supply chain obj')
    @allure.tag('normal')
    @allure.story('seller.json')
    @allure.description('Test for supply chain obj - sid in seller.json')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [app_id_schain_test])
    def test_schain_obj_sid_in_seller_json(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id_schain_test, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        schain_obj = bid_request['ext']['schain']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(schain_obj['ver'], not empty())
        assert_that(schain_obj['complete'], not empty())
        assert_that(schain_obj['nodes'][0]['asi'], not empty())
        assert_that(schain_obj['nodes'][0]['sid'], not empty())
        assert_keys_not_exist(schain_obj['nodes'][0], 'name')
        assert_that(schain_obj['nodes'][0]['rid'], bid_request['id'])
        assert_that(schain_obj['nodes'][0]['hp'], not empty())

    @allure.feature('moat')
    @allure.tag('normal', 'R_1.125.0')
    @allure.story('PBJ-1555 Add moat_sdk Attribute to BidRequest.Ext')
    @allure.description('Verify moat_sdk field in case of iOS SDK >= 5.1.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/5.1.0', 'Vungle/5.1.1', 'Vungle/6.5.3'])
    def test_moat_sdk_ios_existing(self, pub_app_id, sdk_ver):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_ver,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['ext']['moat_sdk'], equal_to(1))
        assert_that(bid_request['ext']['vungle']['src'], equal_to('sdk'))

    @allure.feature('moat')
    @allure.tag('normal', 'R_1.125.0')
    @allure.story('PBJ-1555 Add moat_sdk Attribute to BidRequest.Ext')
    @allure.description('Verify moat_sdk field in case of iOS SDK < 5.1.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/5.0.9'])
    def test_moat_sdk_ios_non_existing(self, pub_app_id, sdk_ver):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_ver,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['ext'], 'moat_sdk')

    @allure.feature('moat')
    @allure.tag('normal', 'R_1.125.0')
    @allure.story('PBJ-1555 Add moat_sdk Attribute to BidRequest.Ext')
    @allure.description('Verify moat_sdk field in case of Android SDK >= 5.3.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('sdk_ver', ['VungleDroid/5.3.0', 'VungleDroid/5.3.1', 'VungleDroid/6.5.3'])
    def test_moat_sdk_android_existing(self, sdk_ver):
        req = request_payload.jaeger_v5_android(android_common_test_app, android_common_test_placement,
                                                android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_ver))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['ext']['moat_sdk'], equal_to(1))

    @allure.feature('moat')
    @allure.tag('normal', 'R_1.125.0')
    @allure.story('PBJ-1555 Add moat_sdk Attribute to BidRequest.Ext')
    @allure.description('Verify moat_sdk field in case of Android SDK < 5.3.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('sdk_ver', ['VungleDroid/5.2.9'])
    def test_moat_sdk_android_non_existing(self, sdk_ver):
        req = request_payload.jaeger_v5_android(android_common_test_app, android_common_test_placement,
                                                android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_ver))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['ext'], 'moat_sdk')

    @allure.feature('vision')
    @allure.tag('ext')
    @allure.story('PBJ-3370 RTB :: Malformed Banner Bid Requests')
    @allure.description('Verify there is no user.ext.vungle from bid_request for XRTB even visionEnabled = true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_remove_ext_vungle_for_xrtb_01(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
                                            banner=True, vision=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip, sdk_version="Vungle/6.11.0",
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        user = bid_request['user']
        assert_keys_not_exist(user['ext'], 'vungle')

    @allure.feature('vision')
    @allure.tag('ext')
    @allure.story('PBJ-3370 RTB :: Malformed Banner Bid Requests')
    @allure.description('Verify there is no user.ext.vungle from bid_request for XRTB even visionEnabled = true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_remove_ext_vungle_for_xrtb_02(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            banner=True, vision=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast,
                                          sdk_version="Vungle/6.11.0"))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        user = bid_request['user']
        assert_keys_not_exist(user['ext'], 'vungle')

    @allure.feature('vision')
    @allure.tag('ext')
    @allure.story('PBJ-3370 RTB :: Malformed Banner Bid Requests')
    @allure.description('Verify there is user.ext.vungle from bid_request for meister when visionEnabled = true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_remove_ext_vungle_for_meister(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
                                            banner=True, vision=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                          rtb_selector=meister_rtb_ids,
                                          sdk_version="Vungle/6.11.0"))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        user = bid_request['user']
        assert_keys_exist(user['ext'], 'vungle')
        assert_that(user['ext']['vungle'], not empty())

    @allure.feature('vision')
    @allure.tag('ext')
    @allure.story('PBJ-3370 RTB :: Malformed Banner Bid Requests')
    @allure.description('Verify there is user.ext.vungle from bid_request for meister when visionEnabled = true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_remove_ext_vungle_for_kraken(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            banner=True, vision=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version="Vungle/6.11.0"))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        user = bid_request['user']
        assert_keys_exist(user['ext'], 'vungle')
        assert_that(user['ext']['vungle'], not empty())

    @allure.feature('vision')
    @allure.tag('ext')
    @allure.story('PBJ-3370 RTB :: Malformed Banner Bid Requests')
    @allure.description('Verify there is no user.ext.vungle from bid_request for XRTB even visionEnabled = false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_banner_placement_1])
    def test_remove_ext_vungle_for_xrtb_03(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
                                             banner=True, vision=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version="Vungle/6.11.0"))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        user = bid_request['user']
        assert_keys_not_exist(user, 'ext')

    @allure.feature('vision')
    @allure.tag('ext')
    @allure.story('PBJ-3370 RTB :: Malformed Banner Bid Requests')
    @allure.description('Verify there is no user.ext.vungle from bid_request for XRTB even visionEnabled = false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_banner_placement_1])
    def test_remove_ext_vungle_for_xrtb_04(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            banner=True, vision=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast,
                                          sdk_version="Vungle/6.11.0"))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        user = bid_request['user']
        assert_keys_not_exist(user, 'ext')

    @allure.feature('vision')
    @allure.tag('ext')
    @allure.story('PBJ-3370 RTB :: Malformed Banner Bid Requests')
    @allure.description('Verify there is no user.ext.vungle from bid_request for meister when visionEnabled = false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_banner_placement_1])
    def test_remove_ext_vungle_for_meister_01(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
                                            banner=True, vision=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                          rtb_selector=meister_rtb_ids,
                                          sdk_version="Vungle/6.11.0"))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        user = bid_request['user']
        assert_keys_not_exist(user, 'ext')

    @allure.feature('vision')
    @allure.tag('ext', 'test_mode')
    @allure.story('PBJ-3370 RTB :: Malformed Banner Bid Requests')
    @allure.description('Verify there is no user.ext.vungle from bid_request when visionEnabled = false in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_banner_placement_1])
    def test_remove_ext_vungle_for_kraken_01(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            banner=True, vision=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ca_us_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version="Vungle/6.11.0"))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        user = bid_request['user']
        assert_keys_not_exist(user, 'ext')

    @allure.feature('liftoff support')
    @allure.tag('normal', 'v1.212.0', 'v1.215.0')
    @allure.story('PBJ-4091 Support Vungle US-only vs. Regional Endpoint A/B Test'
                  'PBJ-4199 Set the ext.region by the audit list from LO team'
                  'PBJ-4450 Jaeger - Update LO bid request region to US'
                  'PBJ-4467 Jaeger - Remove ext.region in bid request to LO')
    @allure.description("Verify the region should be EU for eu ips which exist in the list"
                        "via liftoff_us or liftoff rtb connection"
                        "Verify that all region should be US for LO requests"
                        "Verify that the region field is removed")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('src_ip', [fr_ip, gb_ip, de_ip])
    @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us, ext_non_test_mode_kraken_rtb_ids_mraid_liftoff])
    def test_liftoff_us_1(self, pub_app_id, placement, src_ip, rtb_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=src_ip, debug='jaeger',
                                          rtb_selector=rtb_id))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['ext'], 'region')

    @allure.feature('liftoff support')
    @allure.tag('normal', 'v1.212.0', 'v1.215.0')
    @allure.story('PBJ-4091 Support Vungle US-only vs. Regional Endpoint A/B Test'
                  'PBJ-4199 Set the ext.region by the audit list from LO team'
                  'PBJ-4450 Jaeger - Update LO bid request region to US'
                  'PBJ-4467 Jaeger - Remove ext.region in bid request to LO')
    @allure.description("Verify the region should be AP for ap ips which exist in the list"
                        "via liftoff_us or liftoff rtb connection"
                        "Verify that the region field is removed")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('src_ip', [jp_ip, cn_ip])
    @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us, ext_non_test_mode_kraken_rtb_ids_mraid_liftoff])
    def test_liftoff_us_2(self, pub_app_id, placement, src_ip, rtb_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=src_ip, debug='jaeger',
                                          rtb_selector=rtb_id))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_keys_not_exist(bid_request['ext'], 'region')

    @allure.feature('liftoff support')
    @allure.tag('normal', 'v1.212.0', 'v1.215.0')
    @allure.story('PBJ-4091 Support Vungle US-only vs. Regional Endpoint A/B Test'
                  'PBJ-4199 Set the ext.region by the audit list from LO team'
                  'PBJ-4467 Jaeger - Remove ext.region in bid request to LO')
    @allure.description("Verify the region should be US which exist duplicate countries sheet in the list"
                        "via liftoff_us or liftoff rtb connection")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('src_ip', [ao_ip, et_ip])
    @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us, ext_non_test_mode_kraken_rtb_ids_mraid_liftoff])
    def test_liftoff_us_3(self, pub_app_id, placement, src_ip, rtb_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=src_ip, debug='jaeger',
                                          rtb_selector=rtb_id))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_keys_not_exist(bid_request['ext'], 'region')

    @allure.feature('liftoff support')
    @allure.tag('normal', 'v1.212.0', 'v1.215.0')
    @allure.story('PBJ-4091 Support Vungle US-only vs. Regional Endpoint A/B Test'
                  'PBJ-4199 Set the ext.region by the audit list from LO team'
                  'PBJ-4450 Jaeger - Update LO bid request region to US'
                  'PBJ-4467 Jaeger - Remove ext.region in bid request to LO')
    @allure.description("Verify the region should be US which not exist in the list"
                        "via liftoff_us or liftoff rtb connection")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('src_ip', [ca_us_ip, us_ip])
    @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us, ext_non_test_mode_kraken_rtb_ids_mraid_liftoff])
    def test_liftoff_us_4(self, pub_app_id, placement, src_ip, rtb_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=src_ip, debug='jaeger',
                                          rtb_selector=rtb_id))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_keys_not_exist(bid_request['ext'], 'region')

    @allure.feature('liftoff support')
    @allure.tag('normal', 'test_mode', 'v1.212.0', 'v1.215.0')
    @allure.story('PBJ-4091 Support Vungle US-only vs. Regional Endpoint A/B Test'
                  'PBJ-4199 Set the ext.region by the audit list from LO team'
                  'PBJ-4450 Jaeger - Update LO bid request region to US'
                  'PBJ-4467 Jaeger - Remove ext.region in bid request to LO')
    @allure.description("Verify the region should be US via liftoff_us rtb connection in test mode")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('src_ip', [fr_ip, jp_ip, us_ip])
    @pytest.mark.parametrize('rtb_id', [ext_test_mode_kraken_rtb_ids_vast_liftoff_us,
                                        ext_test_mode_kraken_rtb_ids_vast_liftoff_notification])
    def test_liftoff_us_5(self, pub_app_id, placement, src_ip, rtb_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=src_ip, debug='jaeger',
                                          rtb_selector=rtb_id))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['ext'], 'region')

    @allure.feature('liftoff support')
    @allure.tag('normal', 'v1.212.0', 'v1.215.0')
    @allure.story('PBJ-4091 Support Vungle US-only vs. Regional Endpoint A/B Test'
                  'PBJ-4199 Set the ext.region by the audit list from LO team')
    @allure.description("Verify there is no region field via the normal rtb connection")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_liftoff_us_6(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_keys_not_exist(bid_request['ext'], 'region')

    @allure.feature('network ID')
    @allure.tag('normal')
    @allure.story('PBJ-4934 Smart/Equative - Add support for bidrequest.ext.network_id')
    @allure.description("Verify pass networkid")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_id', [ext1_non_test_mode_kraken_networkID])
    def test_pass_network_id(self, pub_app_id, placement, rtb_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                          rtb_selector=rtb_id))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_keys_exist(bid_request['ext'], 'network_id')
        assert_that(bid_request['ext']['network_id'], equal_to(4383))

    @allure.feature('network ID')
    @allure.tag('normal')
    @allure.story('PBJ-4934 Smart/Equative - Add support for bidrequest.ext.network_id')
    @allure.description("Verify does not pass network_id to other dsp")
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_pass_network_id_1(self, pub_app_id, placement, rtb_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, debug='jaeger',
                                          rtb_selector=rtb_id))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_keys_not_exist(bid_request['ext'], 'network_id')

    # @allure.feature('SKO & SKPV')
    # @allure.tag('normal')
    # @allure.story('PBJ-5222 Adding SKO Auto and SKPV flags in bid request')
    # @allure.description("Verify skpv in cases of:app.allow_storekit_transition=true, "
    #                     "placement.supported_template_types=[ "
    #                     "'single_page_fullscreen', "
    #                     "'multi_page_fullscreen']")
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('placement', [common_test_realtime_coppa_placement_1])
    # @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast])
    # def test_bid_request_skpv_01(self, pub_app_id, placement, rtb_id):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, debug='jaeger',
    #                                       rtb_selector=rtb_id))
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     ext_skadn = bid_request['imp'][0]['ext']['skadn']
    #     assert_keys_exist(ext_skadn['ext'], 'skpv')
    #     assert_that(ext_skadn['ext']['skpv'], equal_to(True))
    #
    # @allure.feature('SKO & SKPV')
    # @allure.tag('normal')
    # @allure.story('PBJ-5222 Adding SKO Auto and SKPV flags in bid request')
    # @allure.description(
    #     'Verify skpv in cases of:app.allow_storekit_transition=false, placement.supported_template_types=['
    #     '\'single_page_fullscreen\', '
    #     '\'multi_page_fullscreen\']')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    # @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast])
    # def test_bid_request_skpv_02(self, pub_app_id, placement, rtb_id):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, debug='jaeger',
    #                                       rtb_selector=rtb_id))
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     ext_skadn = bid_request['imp'][0]['ext']['skadn']
    #     assert_keys_exist(ext_skadn['ext'], 'skpv')
    #     assert_that(ext_skadn['ext']['skpv'], equal_to(False))
    #
    # @allure.feature('SKO & SKPV')
    # @allure.tag('normal')
    # @allure.story('PBJ-5222 Adding SKO Auto and SKPV flags in bid request')
    # @allure.description("Verify skpv both in cases of: app.allow_storekit_transition=n/a, "
    #                     "placement.supported_template_types=[ "
    #                     "'single_page_fullscreen', "
    #                     "'multi_page_fullscreen']")
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    # @pytest.mark.parametrize('placement', [common_test_placement_1_instl])
    # @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast])
    # def test_bid_request_skpv_03(self, pub_app_id, placement, rtb_id):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, debug='jaeger',
    #                                       rtb_selector=rtb_id))
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     ext_skadn = bid_request['imp'][0]['ext']['skadn']
    #     assert_keys_exist(ext_skadn['ext'], 'skpv')
    #     assert_that(ext_skadn['ext']['skpv'], equal_to(True))
    #
    # @allure.feature('SKO & SKPV')
    # @allure.tag('normal')
    # @allure.story('PBJ-5222 Adding SKO Auto and SKPV flags in bid request')
    # @allure.description("Verify skpv both are yes in cases of:app.allow_storekit_transition=true, "
    #                     "placement.supported_template_types=[ "
    #                     "'single_page_fullscreen']")
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('placement', [common_test_no_coppa_placement])
    # @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast])
    # def test_bid_request_skpv_4(self, pub_app_id, placement, rtb_id):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, debug='jaeger',
    #                                       rtb_selector=rtb_id))
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     ext_skadn = bid_request['imp'][0]['ext']['skadn']
    #     assert_keys_exist(ext_skadn['ext'], 'skpv')
    #     assert_that(ext_skadn['ext']['skpv'], equal_to(False))
    #
    # @allure.feature('SKO & SKPV')
    # @allure.tag('normal')
    # @allure.story('PBJ-5222 Adding SKO Auto and SKPV flags in bid request')
    # @allure.description("Verify sko and skpv both are yes in cases of: app.fullscreenClickable=adv_pref")
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('placement', [common_test_no_coppa_placement])
    # @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast])
    # def test_bid_request_sko_1(self, pub_app_id, placement, rtb_id):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, debug='jaeger',
    #                                       rtb_selector=rtb_id))
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     ext_skadn = bid_request['imp'][0]['ext']['skadn']
    #     assert_keys_exist(ext_skadn['ext'], 'sko')
    #     assert_that(ext_skadn['ext']['sko'], equal_to(True))
    #
    # @allure.feature('SKO & SKPV')
    # @allure.tag('normal')
    # @allure.story('PBJ-5222 Adding SKO Auto and SKPV flags in bid request')
    # @allure.description("Verify sko in cases of: app.fullscreenClickable=fsc_on")
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    # @pytest.mark.parametrize('placement', [common_test_placement_10])
    # @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast])
    # def test_bid_request_sko_2(self, pub_app_id, placement, rtb_id):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, debug='jaeger',
    #                                       rtb_selector=rtb_id))
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     ext_skadn = bid_request['imp'][0]['ext']['skadn']
    #     assert_keys_exist(ext_skadn['ext'], 'sko')
    #     assert_that(ext_skadn['ext']['sko'], equal_to(False))
    #
    # @allure.feature('SKO & SKPV')
    # @allure.tag('normal')
    # @allure.story('PBJ-5222 Adding SKO Auto and SKPV flags in bid request')
    # @allure.description("Verify sko and skpv both are yes in cases of: app.fullscreenClickable=fsc_off")
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_vast])
    # def test_bid_request_sko_3(self, pub_app_id, placement, rtb_id):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, debug='jaeger',
    #                                       rtb_selector=rtb_id))
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     ext_skadn = bid_request['imp'][0]['ext']['skadn']
    #     assert_keys_exist(ext_skadn['ext'], 'sko')
    #     assert_that(ext_skadn['ext']['sko'], equal_to(False))

    @allure.tag('RTA')
    @allure.story('normal', 'v1.259.2')
    @allure.story('PBJ-5331 RTA - Add is realtime flag to bid request to Accelerate')
    @allure.description('Verify realtime flag is added to Accelerate')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_rta_realtime_flag_for_lo_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            response_payload = info['hbp_response']
            debug = get_bid_request_obj_from_jaeger_explain(response_payload)
            source_ext = debug['source']['ext']
            assert_that(source_ext['realtime'], equal_to(True))

    @allure.tag('RTA')
    @allure.story('normal', 'v1.259.2')
    @allure.story('PBJ-5331 RTA - Add is realtime flag to bid request to Accelerate')
    @allure.description('Verify realtime flag is added to Accelerate')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_realtime_exp])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_rta_realtime_flag_for_lo_2(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True, config_extension=config_extension_RTA,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            response_payload = info['hbp_response']
            debug = get_bid_request_obj_from_jaeger_explain(response_payload)
            source_ext = debug['source']['ext']
            assert_that(source_ext['realtime'], equal_to(True))

    @allure.tag('RTA')
    @allure.story('normal', 'v1.259.2')
    @allure.story('PBJ-5331 RTA - Add is realtime flag to bid request to Accelerate')
    @allure.description('Verify no realtime flag is added to other dsps')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_rta_realtime_flag_for_lo_3(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            response_payload = info['hbp_response']
            debug = get_bid_request_obj_from_jaeger_explain(response_payload)
            source_ext = debug['source']['ext']
            assert_keys_not_exist(source_ext, 'realtime')
