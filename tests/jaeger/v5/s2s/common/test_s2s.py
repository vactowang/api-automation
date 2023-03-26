import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_s2s, get_bid_request_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('jaeger v5 s2s')
class TestS2S(object):

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3554 S2S - Update bid price')
    @allure.description('Verify s2s  serve non test mode edsp'
                        'Verify bid price is 0.01')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_s2s_server_edsp(self, pub_app_id, placement):
        req = request_payload.s2s_payload_ios(pub_app_id, placement)
        r = post(s2s_v5_standard_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast, debug='jaeger',
                                          src_ip=fr_ip))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3554 S2S - Update bid price')
    @allure.description('Verify s2s  serve non test mode edsp'
                        'Verify bid price is 0.01')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_s2s_server_with_regs_edsp(self, pub_app_id, placement):
        req = request_payload.s2s_payload_ios(pub_app_id, placement, regs=True)
        r = post(s2s_v5_standard_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast, debug='jaeger'))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3554 S2S - Update bid price')
    @allure.description('Verify s2s  serve test mode edsp'
                        'Verify bid price is 0.01')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_s2s_server_test_mode_edsp(self, pub_app_id, placement):
        req = request_payload.s2s_payload_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(s2s_v5_standard_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2S API phase 2 Implementation - Support Internal Ads'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify s2s not serve via test mode kraken')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_s2s_serve_idsp_test_mode_kraken(self, pub_app_id, placement):
        req = request_payload.s2s_payload_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))
        # response_payload = r.json()
        # bid = response_payload['seatbid'][0]['bid']
        # assert_keys_exist(bid[0], 'adm')
        # assert_that("<VAST" in bid[0]['adm'])
        # assert_that(bid[0]['adm'], is_not(None))
        # assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2S API phase 2 Implementation - Support Internal Ads'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify s2s not serve via non test mode kraken')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_not_serve_idsp_non_test_mode_kraken(self, pub_app_id, placement):
        req = request_payload.s2s_payload_ios(pub_app_id, placement, ifa=gen_device_id(), ip=au_ip)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids))
        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))
        # response_payload = r.json()
        # bid = response_payload['seatbid'][0]['bid']
        # assert_keys_exist(bid[0], 'adm')
        # assert_that("<VAST" in bid[0]['adm'])
        # assert_that(bid[0]['adm'], is_not(None))
        # assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2S API phase 2 Implementation - Support Internal Ads'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify s2s not serve via non test mode kraken for android')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_not_s2s_serve_idsp_kraken_android(self, pub_app_id, placement):
        req = request_payload.s2s_payload_android(pub_app_id, placement, ip=au_ip)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids))
        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))
        # response_payload = r.json()
        # bid = response_payload['seatbid'][0]['bid']
        # assert_keys_exist(bid[0], 'adm')
        # assert_that("<VAST" in bid[0]['adm'])
        # assert_that(bid[0]['adm'], is_not(None))
        # assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3554 S2S - Update bid price')
    @allure.description('Verify s2s  serve non test mode edsp'
                        'Verify bid price is 0.01')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_s2s_server_edsp_android(self, pub_app_id, placement):
        req = request_payload.s2s_payload_android(pub_app_id, placement)
        r = post(s2s_v5_standard_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3554 S2S - Update bid price')
    @allure.description('Verify s2s  serve non test mode edsp'
                        'Verify bid price is 0.01')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_s2s_server_edsp_with_regs_android(self, pub_app_id, placement):
        req = request_payload.s2s_payload_android(pub_app_id, placement, regs=True)
        r = post(s2s_v5_standard_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2s - S2S API phase 2 Implementation - Support Internal Ads'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify s2s serve meister for Interstitial & Rewarded placements on ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_s2s_placement, common_test_s2s_instl_placement])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_serve_meister_for_ios_placements(self, pub_app_id, placement, s2s_partner):
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement, ifa=gen_device_id(),
                        rtb=meister_rtb_ids)
        assert_keys_exist(r, 'nbr')
        # debug = r['ext']['debug']
        # assert_keys_exist(debug, 'auction_result')
        # bid = r['seatbid'][0]['bid']
        # assert_keys_exist(bid[0], 'adm')
        # assert_that("<VAST" in bid[0]['adm'])
        # assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2s - S2S API phase 2 Implementation - Support Internal Ads'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify s2s not serve meister for Interstitial & Rewarded placements on android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('s2s_partner', ['standard'])
    def test_not_serve_meister_for_android_placements(self, pub_app_id, placement, s2s_partner):
        r = request_s2s(platform='android', supply=s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement,
                        ifa=gen_device_id(),
                        rtb=meister_rtb_ids)
        assert_keys_exist(r, 'nbr')
        # debug = r['ext']['debug']
        # assert_keys_exist(debug, 'auction_result')
        # bid = r['seatbid'][0]['bid']
        # assert_keys_exist(bid[0], 'adm')
        # assert_that("<VAST" in bid[0]['adm'])
        # assert_that(bid[0]['adm'], is_not(None))
        # assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-4302 Jaeger - S2S add missing android_id field')
    @allure.description('Verify android_id pass to downstream')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    @pytest.mark.parametrize('s2s_partner', ['standard', 'sigmob'])
    def test_pass_android_id(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(platform='android', supply=s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id,
                        ifa='', android_id=test_ifa, rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        bid_device_info = r['ext']['debug']['auction_result']['device_info']
        assert_that(bid_device_info['source'], equal_to('ISU'))
        assert_that(bid_device_info['id'], equal_to(test_ifa))


    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-4302 Jaeger - S2S add missing android_id field'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify android_id pass to downstream')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    @pytest.mark.parametrize('s2s_partner', ['standard', 'sigmob'])
    def test_pass_android_id_i(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(platform='android', supply=s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id,
                        ifa='', android_id=test_ifa, rtb=meister_rtb_ids)
        assert_keys_exist(r, 'nbr')
        # bid_device_info = r['ext']['debug']['auction_result']['device_info']
        # assert_that(bid_device_info['source'], equal_to('ISU'))
        # assert_that(bid_device_info['id'], equal_to(test_ifa))


    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-4302 Jaeger - S2S add missing android_id field')
    @allure.description('Verify app_set_id pass to downstream')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    @pytest.mark.parametrize('s2s_partner', ['standard', 'sigmob'])
    def test_pass_app_set_id(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(platform='android', supply=s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id,
                        ifa='', app_set_id=test_ifa, rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext_non_test_mode_kraken_rtb_ids_vast)
        device_ext_vungle = bid_request['device']['ext']
        assert_keys_exist(device_ext_vungle, 'app_set_id')
        assert_that(device_ext_vungle['app_set_id'], equal_to(test_ifa))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-4302 Jaeger - S2S add missing android_id field'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify app_set_id pass to downstream')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    @pytest.mark.parametrize('s2s_partner', ['standard', 'sigmob'])
    def test_pass_app_set_id_i(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(platform='android', supply=s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id,
                        ifa='', app_set_id=test_ifa, rtb=meister_rtb_ids)
        assert_keys_exist(r, 'nbr')
        # bid_request = get_bid_request_obj_from_jaeger_explain(r, meister_rtb_ids)
        # device_ext_vungle = bid_request['device']['ext']['vungle']
        # assert_keys_exist(device_ext_vungle, 'app_set_id')
        # assert_that(device_ext_vungle['app_set_id'], equal_to(test_ifa))


    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-4302 Jaeger - S2S add missing android_id field')
    @allure.description('Verify ashwid pass to downstream')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement_id', [windows_common_test_placement])
    @pytest.mark.parametrize('s2s_partner', ['standard', 'sigmob'])
    def test_pass_ashwid(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(platform='windows', supply=s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id,
                        ifa='', ashwid=test_ifa, rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        bid_device_info = r['ext']['debug']['auction_result']['device_info']
        assert_that(bid_device_info['source'], equal_to('ASHWID'))
        assert_that(bid_device_info['id'], equal_to(test_ifa))


    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-4302 Jaeger - S2S add missing android_id field'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify ashwid pass to downstream')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement_id', [windows_common_test_placement])
    @pytest.mark.parametrize('s2s_partner', ['standard', 'sigmob'])
    def test_pass_ashwid_1(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(platform='windows', supply=s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id,
                        ifa='', ashwid=test_ifa, rtb=meister_rtb_ids)
        assert_keys_exist(r, 'nbr')
        # bid_device_info = r['ext']['debug']['auction_result']['device_info']
        # assert_that(bid_device_info['source'], equal_to('ASHWID'))
        # assert_that(bid_device_info['id'], equal_to(test_ifa))


    # --------------------------------------------below cases are for active partners-----------------------------------
    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3941 S2S - do not serve traffic from pub which are not in partner pub list for onboarding')
    @allure.description('Verify s2s serve active partner for Interstitial & Rewarded placements '
                        'via edsp on ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_s2s_instl_placement])
    def test_serve_edsp_for_active_partner(self, pub_app_id, placement):
        req = request_payload.s2s_payload_ios(pub_app_id, placement)
        r = post(s2s_v5_active_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast, debug='jaeger'))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that("<VAST" in bid[0]['adm'])
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))


    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3941 S2S - do not serve traffic from pub which are not in partner pub list for onboarding')
    @allure.description('Verify s2s serve active partner for Interstitial & Rewarded placements '
                        'via edsp on android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_serve_edsp_for_active_partner_android(self, pub_app_id, placement):
        req = request_payload.s2s_payload_android(pub_app_id, placement)
        r = post(s2s_v5_active_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that("<VAST" in bid[0]['adm'])
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))


    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3941 S2S - do not serve traffic from pub which are not in partner pub list for onboarding')
    @allure.description('Verify s2s serve active partner for Interstitial & Rewarded placements '
                        'via edsp on amazon platform')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    def test_serve_edsp_for_active_partner_amazon(self, pub_app_id, placement):
        req = request_payload.s2s_payload_sigmob_amazon(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(s2s_v5_active_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_consentString))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that("<VAST" in bid[0]['adm'])
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3941 S2S - do not serve traffic from pub which are not in partner pub list for onboarding')
    @allure.description('Verify s2s serve active partner for Interstitial & Rewarded placements '
                        'via edsp on windows platform')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    def test_serve_edsp_for_active_partner_windows(self, pub_app_id, placement):
        req = request_payload.s2s_payload_sigmob_windows(pub_app_id, placement)
        r = post(s2s_v5_active_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that("<VAST" in bid[0]['adm'])
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3941 S2S - do not serve traffic from pub which are not in partner pub list for onboarding'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify s2s serve active partner for Interstitial & Rewarded placements '
                        'via meister on ios platform')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_s2s_placement])
    def test_serve_meister_for_active_partner(self, pub_app_id, placement):
        req = request_payload.s2s_payload_ios(pub_app_id, placement)
        r = post(s2s_v5_active_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=meister_rtb_ids))
        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))
        # response_payload = r.json()
        # bid = response_payload['seatbid'][0]['bid']
        # assert_keys_exist(bid[0], 'adm')
        # assert_that("<VAST" in bid[0]['adm'])
        # assert_that(bid[0]['adm'], is_not(None))
        # assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3941 S2S - do not serve traffic from pub which are not in partner pub list for onboarding'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify s2s serve active partner for Interstitial & Rewarded placements '
                        'via meister on android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', ['s2s-android-DEFAULT02022'])
    def test_serve_meister_for_active_partner_android(self, pub_app_id, placement):
        req = request_payload.s2s_payload_android(pub_app_id, placement)
        r = post(s2s_v5_active_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=meister_rtb_ids))
        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))
        # response_payload = r.json()
        # bid = response_payload['seatbid'][0]['bid']
        # assert_keys_exist(bid[0], 'adm')
        # assert_that("<VAST" in bid[0]['adm'])
        # assert_that(bid[0]['adm'], is_not(None))
        # assert_that(bid[0]['price'], equal_to(0.01))

    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2s - S2S API phase 2 Implementation - Support Internal Ads'
                  'PBJ-4420 s2s should not send bid request to internal DSP at this point')
    @allure.description('Verify s2s serve active partner for Interstitial & Rewarded placements '
                        'via meister on windows platform')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    def test_serve_meister_for_active_partner_windows(self, pub_app_id, placement):
        req = request_payload.s2s_payload_sigmob_windows(pub_app_id, placement)
        r = post(s2s_v5_active_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=meister_rtb_ids))
        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))
        # response_payload = r.json()
        # bid = response_payload['seatbid'][0]['bid']
        # assert_keys_exist(bid[0], 'adm')
        # assert_that("<VAST" in bid[0]['adm'])
        # assert_that(bid[0]['adm'], is_not(None))
        # assert_that(bid[0]['price'], equal_to(0.01))

    # --------------------------------------------below cases are for onboarding partners-------------------------------
    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2s - S2S API phase 2 Implementation - Support Internal Ads')
    @allure.description('Verify s2s serve onboarding partner for pub apps are match accountid ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_s2s_instl_placement])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_serve_matched_onboarding_partner(self, pub_app_id, placement, rtb_ids):
        """
        Setting in DB
        account_id:"597565c6c5511a1b62000990"
        pub_app_store_ids:["59786bc2a43b3a08620026b1", "59e781de7fff7cb02500ca0e", "5c003b9a3933314cf38ff7f3"]

        note: '59786bc2a43b3a08620026b1, 59e781de7fff7cb02500ca0e' are matched account id,
              '5c003b9a3933314cf38ff7f3' is not matched account id.
        """
        req = request_payload.s2s_payload_ios(pub_app_id, placement)
        r = post(s2s_v5_onboarding_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=rtb_ids,
                                          debug='jaeger'))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that("<VAST" in bid[0]['adm'])
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))


    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2s - S2S API phase 2 Implementation - Support Internal Ads')
    @allure.description('Verify s2s serve onboarding partner for pub apps are not in pub app ids list ')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_serve_matched_onboarding_partner_01(self, pub_app_id, placement, rtb_ids):
        """
        Setting in DB
        account_id:"597565c6c5511a1b62000990"
        pub_app_store_ids:["59786bc2a43b3a08620026b1", 59e781de7fff7cb02500ca0e, "5c003b9a3933314cf38ff7f3"]
        """
        req = request_payload.s2s_payload_android(pub_app_id, placement)
        r = post(s2s_v5_onboarding_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=rtb_ids,
                                          debug='jaeger'))
        assert_that(r.status_code, equal_to(HTTPStatus.OK))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid']
        assert_keys_exist(bid[0], 'adm')
        assert_that("<VAST" in bid[0]['adm'])
        assert_that(bid[0]['adm'], is_not(None))
        assert_that(bid[0]['price'], equal_to(0.01))


    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2s - S2S API phase 2 Implementation - Support Internal Ads')
    @allure.description('Verify s2s not serve onboarding partner for pub app is not matched accountid ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', ['COPPA-TEST_01'])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids])
    def test_not_serve_matched_onboarding_partner_02(self, pub_app_id, placement, rtb_ids):
        """
        Setting in DB
        account_id:"597565c6c5511a1b62000990"
        pub_app_store_ids:["59786bc2a43b3a08620026b1", "5c003b9a3933314cf38ff7f3", 59e781de7fff7cb02500ca0e]

        note: '59786bc2a43b3a08620026b1, 59e781de7fff7cb02500ca0e' are matched account id,
              '5c003b9a3933314cf38ff7f3' is not matched account id.
        """
        req = request_payload.s2s_payload_ios(pub_app_id, placement)
        r = post(s2s_v5_onboarding_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=rtb_ids,
                                         ))
        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))



    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2s - S2S API phase 2 Implementation - Support Internal Ads')
    @allure.description('Verify s2s not serve onboarding partner for '
                        'pub app is matched accountid but not in pub app list')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_3])
    @pytest.mark.parametrize('placement', [common_test_placement_3])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids])
    def test_not_serve_matched_onboarding_partner_03(self, pub_app_id, placement, rtb_ids):
        """
        Setting in DB
        account_id:"597565c6c5511a1b62000990"
        pub_app_store_ids:["59786bc2a43b3a08620026b1", "5c003b9a3933314cf38ff7f3", 59e781de7fff7cb02500ca0e]

        note: '59786bc2a43b3a08620026b1, 59e781de7fff7cb02500ca0e' are matched account id,
              '5c003b9a3933314cf38ff7f3' is not matched account id.
        """
        req = request_payload.s2s_payload_ios(pub_app_id, placement)
        r = post(s2s_v5_onboarding_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=rtb_ids,
                                          ))
        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))



    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2s - S2S API phase 2 Implementation - Support Internal Ads')
    @allure.description('Verify s2s not serve onboarding partner for '
                        'pub app is matched accountid but not in pub app list')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('placement', [android_common_coppa_placememt])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids])
    def test_not_serve_matched_onboarding_partner_04(self, pub_app_id, placement, rtb_ids):
        """
        Setting in DB
        account_id:"597565c6c5511a1b62000990"
        pub_app_store_ids:["59786bc2a43b3a08620026b1", "5c003b9a3933314cf38ff7f3", 59e781de7fff7cb02500ca0e]

        note: '59786bc2a43b3a08620026b1, 59e781de7fff7cb02500ca0e' are matched account id,
              '5c003b9a3933314cf38ff7f3' is not matched account id.
        """
        req = request_payload.s2s_payload_android(pub_app_id, placement)
        r = post(s2s_v5_onboarding_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=rtb_ids))
        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))





    # --------------------------------------------below cases are for inactive partners-------------------------------
    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2s - S2S API phase 2 Implementation - Support Internal Ads')
    @allure.description('Verify s2s not serve inactive partner')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_s2s_instl_placement])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids])
    def test_not_serve_inactive_partner(self, pub_app_id, placement, rtb_ids):
        """
        Setting in DB
        status: inactive
        """
        req = request_payload.s2s_payload_ios(pub_app_id, placement)
        r = post(s2s_v5_inactive_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=rtb_ids))
        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))



    @allure.feature('s2s')
    @allure.tag('smoke')
    @allure.story('PBJ-3337 S2S - filter out internal rtb for s2s traffic'
                  'PBJ-3697 S2s - S2S API phase 2 Implementation - Support Internal Ads')
    @allure.description('Verify s2s not serve inactive partner')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_s2s_instl_placement])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast, meister_rtb_ids])
    def test_not_serve_invalid_partner(self, pub_app_id, placement, rtb_ids):
        """
        Not set in db
        """
        req = request_payload.s2s_payload_ios(pub_app_id, placement)
        r = post(s2s_v5_invalid_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, rtb_selector=rtb_ids))
        assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))



    @allure.feature('s2s')
    @allure.feature('placement throttle')
    @allure.tag('normal')
    @allure.story('PBJ-4756 Support the manual configurable throttling by dimension on Bastion for unprofitable '
                  'traffic.')
    @allure.description('Verify 50 percent traffic of au will serve successfully')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_throttle_placement])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_placement_throttle_02(self, pub_app_id, placement, rtb_ids):
        """

             "is_throttling_enabled":true
             "default_throttling": 5000
             geo{
                 "au": 5000
                 "us"  10000
             }
             """
        req = request_payload.s2s_payload_ios(pub_app_id, placement, ip=au_ip)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=rtb_ids, src_ip=au_ip, sdk_version=None))

        assert_that(r.status_code in [200, 204])



