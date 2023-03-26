import pytest
import allure

from utils.behaviors import request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain, get_bid_response_obj_from_jaeger_explain, verify_real_time_token
from utils.common import *
from utils.assertions import *
from settings import *



@allure.epic('Real-time bid request')
class TestDeviceDetails(object):

    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request device')
    @allure.description('Verify app device details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_device_details(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(test_mode_device_id))
                assert_that(device['geo']['country'], equal_to('FRA'))
                assert_that(device['ip'], equal_to(eu_country_ip))
                assert_that(device['os'], equal_to_ignoring_case('iOS'))
                assert_that(device['osv'], equal_to('13'))

    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request device')
    @allure.description('Verify the device geo field for openrtb25x changes')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_geo_openrtb25x(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip='45.251.108.248',
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                device = bid_request['device']
                assert_that(device['geo']['ipservice'], equal_to(3))

    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request device')
    @allure.description('Verify the no ipservice field in device geo when geo info in ads request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_no_geo_openrtb25x(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, geo=True,
                                                no_pre_cache_token=True, explain=True, ip='45.251.108.248',
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                device = bid_request['device']
                assert_keys_not_exist(device['geo'], 'ipservice')


    @allure.feature('wurfl support')
    @allure.tag('normal')
    @allure.story('PBJ-1724 Support wurfl in Jaeger')
    @allure.description('Verify that the valid Android ua string in ads request with iOS device')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_valid_ua_ios(self, pub_app_id, partner, sdk_v, placement):
        test_ua = 'Mozilla/5.0 (Linux; Android 7.0; SM-T819 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Version/4.0 Chrome/83.0.4103.101 Safari/537.36,SM-G965N,Samsung,4'
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, geo=True,
                                                no_pre_cache_token=True, explain=True, ua=test_ua,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                device = bid_request['device']
                assert_that(device['ua'], equal_to(test_ua))



    @allure.feature('device details')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-2256 Set LMT to FALSE when IFA is present with non-zero value')
    @allure.description('Verify the lmt should be 0 with vaild IFA')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('lmt', [0, 1])
    def test_real_time_lmt_with_vaild_ifa(self, pub_app_id, placement, sdk_v, partner, lmt):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, geo=True,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext1_non_test_mode_kraken_rtb_ids_vast, lmt=lmt)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext1_non_test_mode_kraken_rtb_ids_vast)
                assert_that(bid_request['device']['lmt'], equal_to(lmt))

    @allure.feature('device details')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-2256 Set LMT to FALSE when IFA is present with non-zero value')
    @allure.description('Verify the lmt should keep the original value with invaild IFA')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('ifa', ['00000000-0000-0000-0000-000000000000', ''])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    @pytest.mark.parametrize('lmt', [0, 1])
    def test_real_time_lmt_with_invaild_ifa(self, pub_app_id, placement, sdk_v, partner, lmt, ifa):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=ifa, sdk_v=sdk_v, geo=True,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext1_non_test_mode_kraken_rtb_ids_vast, lmt=lmt)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext1_non_test_mode_kraken_rtb_ids_vast)
                assert_that(bid_request['device']['lmt'], equal_to(lmt))


    @allure.feature('device details')
    @allure.feature('support ipv6')
    @allure.tag('smoke')
    @allure.story('PBJ-3258 RTB::Feature request to support ipv6 format')
    @allure.description("Verify there is ipv6 field from bid request for non test mode XRTB")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_ipv6_for_XRTB(self, pub_app_id, placement, sdk_v, partner):
        rtb = ext1_non_test_mode_kraken_rtb_ids_vast
        test_ifa = gen_device_id(digital=36)
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_ifa, sdk_v=sdk_v, geo=True,
                                                no_pre_cache_token=True, explain=True, ip=ipv6_example_01, rtb=rtb)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ip'], equal_to(ipv6_example_01))


    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-3210 Update ios Make & model specific for meister in bidrequest')
    @allure.description("Verify the ios Make & model specific have updated")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_specific_the_make_and_model(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, geo=True,
                                                no_pre_cache_token=True, explain=True, rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                device = bid_request['device']
                bid_request_make = device['make']
                bid_request_model = device['model']
                assert_that(bid_request_make, equal_to("Apple"))
                assert_that(bid_request_model, equal_to("iPhone11,8"))



    @allure.feature('device info')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3472 Update Apple\'s mobile device codes types For new apple devices')
    @allure.description("Verify the new app devices has updated for non test mode edsp")
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('new_app_devices', new_app_devices)
    def test_real_time_new_app_devices_updated_non_test_mode(self, pub_app_id, placement, new_app_devices, partner, sdk_v):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, geo=True,
                                                ua='Mozilla/5.0', model=new_app_devices["model"],
                                                no_pre_cache_token=True, explain=True, ip=fr_ip,
                                                rtb=ext1_non_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext1_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                assert_keys_exist(device, 'hwv')
                assert_that(device['hwv'], equal_to(new_app_devices['make']))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id from token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_token_ios(self, pub_app_id, placement, sdk_v, partner):
        partner_device_id = gen_device_id()
        token_device_id = gen_device_id()
        ios_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                token_device_id=token_device_id, token_ios_device_id=ios_device_id)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_device_id))


    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.236.0')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token'
                  'PBJ-4708 Jaeger - Make device id lower case if it is from idfv for realtime')
    @allure.description('Verify jaeger read device id from token for idfv')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_token_idfv(self, pub_app_id, placement, sdk_v, partner):
        partner_device_id = gen_device_id()
        ios_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                idfv=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_mraid,
                                                token_ios_device_id=ios_device_id, ip=au_ip)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:

                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(ios_device_id.lower()))
                assert_that(device_info['source'], 'IDFV')


    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id from token for idfv: edsp allow idfv')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_token_allow_idfv_edsp(self, pub_app_id, placement, sdk_v, partner):
        """

        rtb level setting:
        allow_idfv: true
        """
        partner_device_id = gen_device_id()
        ios_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                idfv=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                token_ios_device_id=ios_device_id, ip=au_ip)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                assert_keys_exist(device['ext'], 'idfv')
                assert_that(device['ext']['idfv'], equal_to(ios_device_id))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(ios_device_id.lower()))
                assert_that(device_info['source'], 'IDFV')



    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id from token for idfv via meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids, ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_real_time_read_device_id_from_token_idfv_meister(self, pub_app_id, placement, sdk_v, partner, rtb):
        rtb = rtb
        partner_device_id = gen_device_id()
        ios_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                idfv=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb,
                                                token_ios_device_id=ios_device_id)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                device = bid_request['device']
                assert_keys_exist(device['ext']['vungle'], 'idfv')
                assert_that(device['ext']['vungle']['idfv'], equal_to(ios_device_id))
                assert_that(device_info['id'], equal_to(ios_device_id.lower()))
                assert_that(device_info['source'], 'IDFV')


    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id from token for android(android id)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_token_android(self, pub_app_id, placement, sdk_v, partner):
        partner_device_id = gen_device_id()
        android_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                token_android_device_id=android_device_id,
                                                platform='android')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(android_device_id))
                assert_that(device_info['source'], 'ISU')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id from token for android(android id) meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_token_android_meister(self, pub_app_id, placement, sdk_v, partner):
        rtb = meister_rtb_ids
        partner_device_id = gen_device_id()
        android_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                token_android_device_id=android_device_id,
                                                platform='android')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                device = bid_request['device']
                assert_keys_exist(device['ext']['vungle'], 'isu')
                assert_that(device['ext']['vungle']['isu'], equal_to(android_device_id))
                assert_that(device_info['id'], equal_to(android_device_id))



    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id from token for android(app set id)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_token_android_01(self, pub_app_id, placement, sdk_v, partner):
        partner_device_id = gen_device_id()
        app_set_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                token_app_set_id=app_set_id, platform='android')

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(app_set_id))
                assert_that(device_info['source'], 'AppSetID')


    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id from token for windows(android id)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_realtime_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_token_windows_01(self, pub_app_id, placement, sdk_v, partner):
        partner_device_id = gen_device_id()
        ashwid = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                token_windows_device_id=ashwid, platform='windows')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(ashwid))
                assert_that(device_info['source'], 'ASHWID')

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id from token for windows(android id)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_realtime_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_token_windows_01_meister(self, pub_app_id, placement, sdk_v, partner):
        rtb = test_mode_kraken_rtb_ids
        partner_device_id = test_mode_device_id
        ashwid = test_mode_device_id
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                token_windows_device_id=ashwid, platform='windows')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                device = bid_request['device']
                assert_keys_exist(device['ext']['vungle'], 'isu')
                assert_that(device['ext']['vungle']['isu'], equal_to(ashwid))
                assert_that(device_info['id'], equal_to(ashwid))
                assert_that(device_info['source'], 'ASHWID')



    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id from ifa if both ifa and android_id exists in token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_token_android_02(self, pub_app_id, placement, sdk_v, partner):
        partner_device_id = gen_device_id()
        device_ifa = gen_device_id()
        android_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                token_device_id=device_ifa, token_android_device_id=android_device_id, platform='android')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(device_ifa))



    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id if device id in token is zeroOut or invalid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('device_id', ['-', '00000000-0000-0000-0000-000000000000', '0000-0000'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_token_android_03(self, pub_app_id, placement, sdk_v, partner, device_id):
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                token_android_device_id=device_id, platform='android')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(partner_device_id))


    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read partner\'s device id if device id not in token:'
                        'only ifa exist in partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_partner_01(self, pub_app_id, placement, sdk_v, partner):
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                platform='android')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(partner_device_id))


    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read partner\'s device id if device id not in token:'
                        'ifa and android id exist in partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_partner_02(self, pub_app_id, placement, sdk_v, partner):
        partner_device_id = gen_device_id()
        partner_android_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, partner_android_id=partner_android_id,
                                                sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                platform='android')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(partner_device_id))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read partner\'s device id if device id not in token:'
                        'ifa and app set id exist in partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_partner_03(self, pub_app_id, placement, sdk_v, partner):
        partner_device_id = gen_device_id()
        partner_app_set_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, partner_app_set_id=partner_app_set_id,
                                                sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                platform='android')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(partner_device_id))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read partner\'s device id if device id not in token:'
                        'android id and app set id exist in partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_partner_04(self, pub_app_id, placement, sdk_v, partner):
        partner_android_id = gen_device_id()
        partner_app_set_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id="", partner_app_set_id=partner_app_set_id,
                                                partner_android_id=partner_android_id,
                                                sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                platform='android')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(partner_android_id))
                assert_that(device_info['source'], equal_to('ISU'))


    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read partner\'s device id if device id not in token:'
                        'only app set id exist in partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_partner_05(self, pub_app_id, placement, sdk_v, partner):
        partner_app_set_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id="", partner_app_set_id=partner_app_set_id,
                                                partner_android_id="",
                                                sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=meister_rtb_ids,
                                                platform='android')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(partner_app_set_id))
                assert_that(device_info['source'], equal_to('AppSetID'))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify jaeger read device id from partner: ifa and idfv both exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_partner_06(self, pub_app_id, placement, sdk_v, partner):
        partner_ifa = gen_device_id()
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_ifa,
                                                idfv=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(partner_ifa))
                assert_that(device_info['source'], 'IFA')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v1.236.0')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token'
                  'PBJ-4672 Realtime - Missing Device ids in device ext in the bid request to iDSPs'
                  'PBJ-4708 Jaeger - Make device id lower case if it is from idfv for realtime')
    @allure.description('Verify jaeger read device id from partner: only idfv exist, edsp allow idfv')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_read_device_id_from_partner_07_allow_idfv(self, pub_app_id, placement, sdk_v, partner):
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=None,
                                                idfv=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb,
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                device = bid_request['device']
                assert_keys_exist(device['ext'], 'idfv')
                assert_that(device['ext']['idfv'], equal_to(partner_device_id))
                assert_that(device_info['id'], equal_to(partner_device_id.lower()))
                assert_that(device_info['source'], 'IDFV')


    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token'
                  'PBJ-4672 Realtime - Missing Device ids in device ext in the bid request to iDSPs')
    @allure.description('Verify jaeger read device id from partner: only idfv exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids, ext_non_test_mode_kraken_rtb_ids_vast_liftoff])
    def test_real_time_read_device_id_from_partner_07(self, pub_app_id, placement, sdk_v, partner, rtb):
        rtb = rtb
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=None,
                                                idfv=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb,
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                device = bid_request['device']
                assert_keys_exist(device['ext']['vungle'], 'idfv')
                assert_that(device['ext']['vungle']['idfv'], equal_to(partner_device_id))
                assert_that(device['ext']['vungle']['id'], equal_to(partner_device_id.lower()))
                assert_that(device_info['id'], equal_to(partner_device_id.lower()))
                assert_that(device_info['source'], 'IDFV')

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, gaid exists, allow retrieving android_id, app_set_id exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_01(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGVSy47bMAz8F57trOI4ie1b0d1bs5c+Lm0h0BLtaOOVXD2ctEH+vVSKogv0JIlDDodDXUE5G8hG6K6g1Iz5DBFjCtCBmyNpaSzcChj17DP4SiHgSHIhH4yznCVWAgoILnlF/LSOKyJ5VDHjxT+6ZE/WnXMoGqaJ+DpDJ25MrmkxufgKaLV3Rt+v8ywDRZlf0KyFardalM1e7Mt+aHS52fRNifsBNQ5Cq+0uy+wxcu+fMiALlGSxn4jrB5wCFUCXSPaP7CuYIIPRNDnU/yUGLRV6LXFBM2UIuugT3ce0b9JzkLuagY2DSjX1sKt2Zb1r2rKu2r7EfqvKvtJDK7Ru23bLw09ox8QWcgX9NUP+cjYH3gWDDx+PnHFEw9jipsToRAtN7NWqqrmbpx+J7buvzNnBjPLNXPA0NpfD4yEdPh3WH16ezs/v68vzy+dvSYiNZkrntbE4ycXQGbp1AbMnherIm47uxDTQff2eHTjJFNhDVpq/B3xJdpzoMW/nYbdaV7z12+03fvXGoEACAAA='
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        rtb = meister_rtb_ids
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_ifa))
                assert_that(device_info['source'], equal_to('IFA'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, gaid exists, allow retrieving android_id, app_set_id NOT exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_02(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGVRy07DMBD8lz2nJQ2hanJDwI1y4XEBZG3sTWpq7OBHWqj676xBCCROcWZ2Z3dmDyCdDWQjtAeQcsT8DRFjCtCCGyMpoS0cCxjU6DP5SiHgQGIiH7SzXFXOSygguOQl8a913BHJo4yZL37lkt1at8tQ1CwT8XWEtjyyuKJJ5+YDoFXeacVPhjuMLPQuAvI0QRY7Q0z1aAIVQPtI9nuHA+ggglZkHKp/hUEJiV4JnFCbTEEbfaKvne2f8gzyVN1zClDJVd0vq+WsXq6aWV013Qy7MznrKtU3pVJN05yxE4N2SJwHd9CPM/HhbAbOg8aT2w1XbFAzNzmTmDU0kWHj86rmaZ7eEmfxlb+zvR7EH19wNaz268t1Wt+tF9cvV7ubi3p/83L/lMryVLGk80pbNGLStIN2UcDoSaLc8Nmi27IMtI/POYGtSIEz5E3zreEh2cHQZY76ZDlfVHzC4/ETpCDR7Q0CAAA='
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        rtb = meister_rtb_ids
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_ifa))
                assert_that(device_info['source'], equal_to('IFA'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, gaid exists, NOT allow retrieving android_id, app_set_id exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_03(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGVSy47bMAz8F57trOI4ie1b0d1bs5c+Lm0h0BLtaOOVXD2ctEH+vVSKogv0JIlDDodDXUE5G8hG6K6g1Iz5DBFjCtCBmyNpaSzcChj17DP4SiHgSHIhH4yznCVWAgoILnlF/LSOKyJ5VDHjxT+6ZE/WnXMoGqaJ+DpDJ25MrmkxufgKaLV3Rt+v8ywDRZlf0KyFardalM1e7Mt+aHS52fRNifsBNQ5Cq+0uy+wxcu+fMiALlGSxn4jrB5wCFUCXSPaP7CuYIIPRNDnU/yUGLRV6LXFBM2UIuugT3ce0b9JzkLuagY2DSjX1sKt2Zb1r2rKu2r7EfqvKvtJDK7Ru23bLw09ox8QWcgX9NUP+cjYH3gWDDx+PnHFEw9jipsToRAtN7NWqqrmbpx+J7buvzNnBjPLNXPA0NpfD4yEdPh3WH16ezs/v68vzy+dvSYiNZkrntbE4ycXQGbp1AbMnherIm47uxDTQff2eHTjJFNhDVpq/B3xJdpzoMW/nYbdaV7z12+03fvXGoEACAAA='
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        rtb = meister_rtb_ids
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_ifa))
                assert_that(device_info['source'], equal_to('IFA'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, gaid exists, NOT allow retrieving android_id, app_set_id NOT exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_04(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGVRy07DMBD8lz2nJQ2hanJDwI1y4XEBZG3sTWpq7OBHWqj676xBCCROcWZ2Z3dmDyCdDWQjtAeQcsT8DRFjCtCCGyMpoS0cCxjU6DP5SiHgQGIiH7SzXFXOSygguOQl8a913BHJo4yZL37lkt1at8tQ1CwT8XWEtjyyuKJJ5+YDoFXeacVPhjuMLPQuAvI0QRY7Q0z1aAIVQPtI9nuHA+ggglZkHKp/hUEJiV4JnFCbTEEbfaKvne2f8gzyVN1zClDJVd0vq+WsXq6aWV013Qy7MznrKtU3pVJN05yxE4N2SJwHd9CPM/HhbAbOg8aT2w1XbFAzNzmTmDU0kWHj86rmaZ7eEmfxlb+zvR7EH19wNaz268t1Wt+tF9cvV7ubi3p/83L/lMryVLGk80pbNGLStIN2UcDoSaLc8Nmi27IMtI/POYGtSIEz5E3zreEh2cHQZY76ZDlfVHzC4/ETpCDR7Q0CAAA='
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        rtb = meister_rtb_ids
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_ifa))
                assert_that(device_info['source'], equal_to('IFA'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true,  gaid exists, allow retrieving android_id, app_set_id exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_05(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGVSy3LbMAz8F55th7IdSdGt0+RW59LHpe1wQBKSaTOkzIfs1vG/F7TTaWZ6IsgFltgFzkx5F9El1p2ZUiOUMyZIObKO+TGhFsaxy4zyxhtqoniLU8hIyKDHUIAXjBEGFBOGaLyjer7gbMaiz0EhXZ0nroQBVCr47N9H2e2dP5anZIgmwcvIOn4hco2TKcVnBk4Hb/Q1HEcRMYlyY23F1cO95vO24c1c9q2er1aynUPTg4aea3VfFwESEv39S0SgBgU6kBapvgcbccbwlNDd2r5KjEaj9aD/S4xaKAhawATGFujmw1Wme5f+Zo4FN2RyhRrFv/rEb+/Kw4do4O7zljK2YAibvM2EWpzQkvzFck0EAQ+ZHLnOx7veDOJdq+xpaE+bx03efNlUn3ZPx+eP69Pz7uuPzPlKE6UP2jiwYjJ4ZF01Y2NABWpLY01+TzSs+86qVymxkSBrpZayqXW91G1bN3It5QNUTdPqqidY1q/ykPpq2Nom195L7vGw4+xncWUvciRfSWpZJvYtu8HiY5nYXb2olrQJl8sfP14jc24CAAA='
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        partner_device_id = gen_device_id()
        rtb = meister_rtb_ids
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['source'], equal_to('Vungle_FP'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true,  gaid exists, allow retrieving android_id, app_set_id NOT exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_06(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGWST3PaMBDFv8uePcQmjE196yS5lVza5NJ2NCtpMQJFMvpjaAnfvStIJpnpyfL+Vk/vrXQC5V0kl6A/gVIjlm9MmHKEHvyYSAvj4Fxx33ilJoq3dQqZmAx6DAW8UIw4kJgoROMd769nNVQQfQ6K+Nd51koUUKXCq4+Dsts5fyilZFgm4csIfX1mcU2TKZtPgE4HbzQvuSwxsdAfEZFPE+RQWmK0RhupAjomclcPF7/RaLIe9X+NUQuFQQuc0NiCrqEunt2n9rekFt2QOSI7pnez4q93pfA1Grz5vuGODRpmk7eZqaWJLGeZzRcsEGifOd5l2N6tzSA+WYWHYXlc3a/y6seq+bZ9ODzeLY6P26dfua5vNUv6oI1DKyZDB+hvKxgDKVQbvqPkdywD/U9oXqWkTqJslZrLrtXtXC+XbScXUn7BpuuWulkzlu2r3Kd1M2xsl1vvZe1pv63hd5nKTuTIc+Wo5WXAc3aDpfsy/pt21sz5Ws/nfz+Vlr07AgAA'
        r = verify_real_time_token(url_encoder(token))
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=meister_rtb_ids,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['source'], equal_to('Vungle_FP'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true,  gaid exists, NOT allow retrieving android_id, app_set_id exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_07(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGVSy3LbMAz8F55th7IdSdGt0+RW59LHpe1wQBKSaTOkzIfs1vG/F7TTaWZ6IsgFltgFzkx5F9El1p2ZUiOUMyZIObKO+TGhFsaxy4zyxhtqoniLU8hIyKDHUIAXjBEGFBOGaLyjer7gbMaiz0EhXZ0nroQBVCr47N9H2e2dP5anZIgmwcvIOn4hco2TKcVnBk4Hb/Q1HEcRMYlyY23F1cO95vO24c1c9q2er1aynUPTg4aea3VfFwESEv39S0SgBgU6kBapvgcbccbwlNDd2r5KjEaj9aD/S4xaKAhawATGFujmw1Wme5f+Zo4FN2RyhRrFv/rEb+/Kw4do4O7zljK2YAibvM2EWpzQkvzFck0EAQ+ZHLnOx7veDOJdq+xpaE+bx03efNlUn3ZPx+eP69Pz7uuPzPlKE6UP2jiwYjJ4ZF01Y2NABWpLY01+TzSs+86qVymxkSBrpZayqXW91G1bN3It5QNUTdPqqidY1q/ykPpq2Nom195L7vGw4+xncWUvciRfSWpZJvYtu8HiY5nYXb2olrQJl8sfP14jc24CAAA='
        r = verify_real_time_token(url_encoder(token))
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=meister_rtb_ids,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['source'], equal_to('Vungle_FP'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true,  gaid exists,  NOT allow retrieving android_id, app_set_id NOT exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_08(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGWST3PaMBDFv8uePcQmjE196yS5lVza5NJ2NCtpMQJFMvpjaAnfvStIJpnpyfL+Vk/vrXQC5V0kl6A/gVIjlm9MmHKEHvyYSAvj4Fxx33ilJoq3dQqZmAx6DAW8UIw4kJgoROMd769nNVQQfQ6K+Nd51koUUKXCq4+Dsts5fyilZFgm4csIfX1mcU2TKZtPgE4HbzQvuSwxsdAfEZFPE+RQWmK0RhupAjomclcPF7/RaLIe9X+NUQuFQQuc0NiCrqEunt2n9rekFt2QOSI7pnez4q93pfA1Grz5vuGODRpmk7eZqaWJLGeZzRcsEGifOd5l2N6tzSA+WYWHYXlc3a/y6seq+bZ9ODzeLY6P26dfua5vNUv6oI1DKyZDB+hvKxgDKVQbvqPkdywD/U9oXqWkTqJslZrLrtXtXC+XbScXUn7BpuuWulkzlu2r3Kd1M2xsl1vvZe1pv63hd5nKTuTIc+Wo5WXAc3aDpfsy/pt21sz5Ws/nfz+Vlr07AgAA'
        r = verify_real_time_token(url_encoder(token))
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=meister_rtb_ids,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['source'], equal_to('Vungle_FP'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, gaid NOT exists, allow retrieving android_id, app_set_id exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_09(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAG2ST3PaMBDFv4vOQGQgtvEt0+RWcumfS9vRrKS1ESiSsSRDS/juXUEyZaY5Wdrf6q3fk05MeRfQRdacmFI95G+IEFNgDfN9RC2MY+cJ9fVXaoJ4W7dgAxLqdD9k8oIhQIdixCEY70iAzzibsODToJC2zpNYxAFUzHzyb1JyO+cPuRQNyUR46VnDzySucTT58ImB04M3+mYp8o4pXRUVtHW7qjVX9yWJQN+LgPHK64Kr1b3m07ri1VS2tZ4uFrKeQtWChpbrfIYmSYj0b79FADIg0IG0qN9cThgeI7qrrUsGwWi0HvR/jUELBYMWMIKxGbEmDgkvMbib9lykqaaFjz1YcF2iOIniezDij3e58BAM3H3ZUMcGDLHR20TU4oiWcpvNl6Q84D5RlJeb9a41nbjxwJ66+rh+XKf113Xxeft0eP60PD5vv/1MnC80SfpBGwdWjAYPrCkmrB9QgdrQg4h+RzKs+cGKVymxkiBLpeayKnU513VdVnIp5QqKqqp10RKW5avcx7boNrZKpfeSe9xvOfuV49qJFChwspqfIfueXGfxMd/vXTkr5vSEzue/pri136gCAAA='
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        token_ifa= token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        rtb = meister_rtb_ids
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_ifa))
                assert_that(device_info['source'], equal_to('IFA'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, gaid NOT exists, allow retrieving android_id, app_set_id NOT exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_10(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAG1Sy3LbMAz8F5w1juS4kqJbp8ktzqWPS9vhgCQk02ZIWSRlt47/vaCTTjzTnkRiocXugidQ3gVyEboTKDVi/oaIMQXowI+RtDAOzgX3ja+oCeLt3KMNxNCgxykjzxQCDiRmmoLxjgnKRQkFBJ8mRXx1nskiTahixov3ScntnD/kUjRME/F5hK48M7mm2eSfT4BOT97oq6PIN1C6qRrs2/6u1aX6UGe1EiPP+SUCshhBDqUl/aa4ADpGcq8SL36C0WQ96n8agxYKJy1wRmMzBF2cEl0suav2XOSppsf/6SnAohsSR8Mo/TUpfnuXCx+DwZvPG+7YoGFs9jYxamkmyxkslitmnmifOJbLlrzrzSCuPMDD0B7X9+u0/rKuHrcPh6dPq+PT9uuPVJa3min9pI1DK2ZDB+iqAsaJFKoNLzf6HdNA9x2qFympkShrpZayqXW91G1bN3Il5R1WTdPqqmdY1i9yH/tq2Ngm1d7L0tN+W8LPHNdOpMCBs9X8pOBbcoOl+7yrm3pRLfk5nM9/ADugFCB0AgAA'
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        rtb = meister_rtb_ids
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_ifa))
                assert_that(device_info['source'], equal_to('IFA'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, gaid NOT exists, NOT allow retrieving android_id, app_set_id exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_11(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGVSy3LbMAz8F55th7IdSdGtk+QW59LHpe1wQBKSaTOkzIfs1vG/F3TSaWZ6IoEFF9gFz0x5F9El1p2ZUiOUMyZIObKO+TGhFsaxy4zqxjfURPF+78FGJGjQYyjIC8YIA4oJQzTeEQFfcDZj0eegkELniSxhAJUKPvvXKbu988eSSoZoEryMrOMXItc4mfL4zMDp4I2+XsdRREyiRKytuLq71XzeNryZy77V89VKtnNoetDQc61u66JAQqLev0QEGlCgA2lRv6uYMTwldG9jXzVGo9F60P8VRi0UBC1gAmMLxLoUMl5lug/lJUldTU9OMRJmwQ2Z7KEI/woVv70riU/RwM3nLVVswRA2eZsJtTihJR8WyzUxBTxksua6Ke96M4gPM7PHoT1tHjZ582VTPe0ej8/369Pz7uuPzPlKE6UP2jiwYjJ4ZF01Y2NABWpLC05+TzSs+86qVymxkSBrpZayqXW91G1bN3It5R1UTdPqqidY1q/ykPpq2Nom195L7vGw4+xnsWcvciSDSWr5VuxbdoPFh7K6m3pRLelLXC5/AH03+wx4AgAA'
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        token_app_set_id = token_response_payload['token']['device']['android']['app_set_id']
        partner_device_id = gen_device_id()
        rtb = meister_rtb_ids
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_app_set_id))
                assert_that(device_info['source'], equal_to('AppSetID'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, gaid NOT exists, NOT allow retrieving android_id, app_set_id NOT exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_12(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGVSy3LbMAz8F5w1juR6JEe3TpNbnUsflybDAUlIps2QMh+yG8f/XtBJp5npiSAWXOwCPIPyLpJL0J9BqQnLGROmHKEHPyXSwji4VFw3vaEmivd4QBuJoVFPoSDPFCOOJGYK0XjHBPWihgqiz0ERX51nskQBVSp49a9TdnvnjyWVDNMkfJ6gry9Mrmk25fEZ0OngjeaQ0xITE/0WEbmbIIfSkn6XVAGdErk3DVfB0WiyHvV/hVELhUELnNHYAkGfQqarZvehvCS5qxnYNrBKi27M7JVv9Fe1ePGuJD5HgzfftlyxRcPY7G1m1NJMlk0tlitmCnTI7PM6du8GM4oPmuF+XJ82d5u8+b5pvu7ujw9fVqeH3Y/HXNefNFP6oI1DK2ZDR+ibCqZACtWWt5X8nmmg/wXNq5TUSZStUkvZtbpd6vW67eRKyltsum6tm4Fh2b7KQxqacWu73Hova0+HXQ1PZTx7kSMPmK2WPwI/sxst3ZU93LSLZsn7vVz+AIusFTFFAgAA'
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        rtb = meister_rtb_ids
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(partner_device_id))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(partner_device_id))
                assert_that(device_info['source'], equal_to('IFA'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true,  gaid NOT exists, allow retrieving android_id, app_set_id exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_13(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGVSy3LbMAz8F55th7IdSdGt0+RW59LHpe1wQBKSaTOkzIfs1vG/F7TTaWZ6IsgFltgFzkx5F9El1p2ZUiOUMyZIObKO+TGhFsaxy4zyxhtqoniLU8hIyKDHUIAXjBEGFBOGaLyjer7gbMaiz0EhXZ0nroQBVCr47N9H2e2dP5anZIgmwcvIOn4hco2TKcVnBk4Hb/Q1HEcRMYlyY23F1cO95vO24c1c9q2er1aynUPTg4aea3VfFwESEv39S0SgBgU6kBapvgcbccbwlNDd2r5KjEaj9aD/S4xaKAhawATGFujmw1Wme5f+Zo4FN2RyhRrFv/rEb+/Kw4do4O7zljK2YAibvM2EWpzQkvzFck0EAQ+ZHLnOx7veDOJdq+xpaE+bx03efNlUn3ZPx+eP69Pz7uuPzPlKE6UP2jiwYjJ4ZF01Y2NABWpLY01+TzSs+86qVymxkSBrpZayqXW91G1bN3It5QNUTdPqqidY1q/ykPpq2Nom195L7vGw4+xncWUvciRfSWpZJvYtu8HiY5nYXb2olrQJl8sfP14jc24CAAA='
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        token_app_set_id = token_response_payload['token']['device']['android']['app_set_id']
        partner_device_id = gen_device_id()
        rtb = meister_rtb_ids
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['source'], equal_to('Vungle_FP'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true,  gaid NOT exists, allow retrieving android_id, app_set_id NOT exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_14(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGWSy27bMBBF/2XWgiO5huRqVzTZ1dnksWkKYkiOZdoMKfMhu3H87x3aKRqgK1Fzhpf3DnkC5V0kl6A/gVIjlm9MmHKEHvyYSAvj4Fxx33ilJoqPdQqZmAx6DAW8Uow4kJgoROMd769nNVQQfQ6K+Nd51koUUKXCq38HZbdz/lBKybBMwtcR+vrM4pomUzafAJ0O3mheclliYqHfIiKfJsihtMRojTZSBXRM5K4eLn6j0WQ96v8aoxYKgxY4obEFXUNdPLtP7R9JLbohc0R2TH/NijfvSuFbNHjzsOGODRpmk7eZqaWJLGeZzRcsEGifOd5l2N6tzSA+WYW7YXlc3a7y6nHV/NjeHe6/L47326eXXNdfNEv6oI1DKyZDB+ibCsZACtWG7yj5HctA/xOadympkyhbpeaya3U718tl28mFlF+x6bqlbtaMZfsu92ndDBvb5dZ7WXvab2v4VaayEznyXDlqeRnwnN1g6baM/6adNXO+1vP5D1l/ado7AgAA'
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=meister_rtb_ids,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['source'], equal_to('Vungle_FP'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true,  gaid NOT exists, NOT allow retrieving android_id, app_set_id exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_15(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGVSy3LbMAz8F55th7IdSdGt0+RW59LHpe1wQBKSaTOkzIfs1vG/F7TTaWZ6IsgFltgFzkx5F9El1p2ZUiOUMyZIObKO+TGhFsaxy4zyxhtqoniLU8hIyKDHUIAXjBEGFBOGaLyjer7gbMaiz0EhXZ0nroQBVCr47N9H2e2dP5anZIgmwcvIOn4hco2TKcVnBk4Hb/Q1HEcRMYlyY23F1cO95vO24c1c9q2er1aynUPTg4aea3VfFwESEv39S0SgBgU6kBapvgcbccbwlNDd2r5KjEaj9aD/S4xaKAhawATGFujmw1Wme5f+Zo4FN2RyhRrFv/rEb+/Kw4do4O7zljK2YAibvM2EWpzQkvzFck0EAQ+ZHLnOx7veDOJdq+xpaE+bx03efNlUn3ZPx+eP69Pz7uuPzPlKE6UP2jiwYjJ4ZF01Y2NABWpLY01+TzSs+86qVymxkSBrpZayqXW91G1bN3It5QNUTdPqqidY1q/ykPpq2Nom195L7vGw4+xncWUvciRfSWpZJvYtu8HiY5nYXb2olrQJl8sfP14jc24CAAA='
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        token_app_set_id = token_response_payload['token']['device']['android']['app_set_id']
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=meister_rtb_ids,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['source'], equal_to('Vungle_FP'))


    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true,  gaid NOT exists,  NOT allow retrieving android_id, app_set_id NOT exists')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_16(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAAGWSy27bMBBF/2XWgiO5huRqVzTZ1dnksWkKYkiOZdoMKfMhu3H87x3aKRqgK1Fzhpf3DnkC5V0kl6A/gVIjlm9MmHKEHvyYSAvj4Fxx33ilJoqPdQqZmAx6DAW8Uow4kJgoROMd769nNVQQfQ6K+Nd51koUUKXCq38HZbdz/lBKybBMwtcR+vrM4pomUzafAJ0O3mheclliYqHfIiKfJsihtMRojTZSBXRM5K4eLn6j0WQ96v8aoxYKgxY4obEFXUNdPLtP7R9JLbohc0R2TH/NijfvSuFbNHjzsOGODRpmk7eZqaWJLGeZzRcsEGifOd5l2N6tzSA+WYW7YXlc3a7y6nHV/NjeHe6/L47326eXXNdfNEv6oI1DKyZDB+ibCsZACtWG7yj5HctA/xOadympkyhbpeaya3U718tl28mFlF+x6bqlbtaMZfsu92ndDBvb5dZ7WXvab2v4VaayEznyXDlqeRnwnN1g6baM/6adNXO+1vP5D1l/ado7AgAA'
        r = verify_real_time_token(url_encoder(token))
        token_response_payload = r.json()
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=meister_rtb_ids,
                                                platform='android', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['source'], equal_to('Vungle_FP'))

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, IDFA allowed, IDFV allowed')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_ios_01(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAE22Wa3ObOBSG/4u+Jm7ExUC80w/4ktnujGN7G2fcbnYYAbIgYIERl6Rp//uKyHHF+nwyIz1+z3su0ugNRQUXlNdo8oaiqCT9r6hJ3Qg0QUVZ0zhIOfp1jVhcVoPNhme86Di6RnV6oHL5UKIJvkbyWxBGg5ZWIi24JCUiiqaKqPwumzBPRUIr9EuKxrRN++W3d43gR8F7xhcpebr5mhDOEpLKf6eF6Jk03rdy2zM82/AW7sheLLyR7c2dkVzAIzx3DMd1sbWY4t5xSOqaVq+BINJKQDkJcxqjyZ7kgkrNvcwVub5jTm+n/miBZ1LLtsyR55jm6A7bd97YmvtT35EGcmmlkUnJf1A+mt3LpbbIG2k5py3N3/OmLzXlKuO3Pl8eX8YUgUhjmhfkck/EQUSqOCAtSfN+67TTl6mix0ZW+L1HBd+nLNCC9eUtqjjlJA/alHZoYl6jsqIRiRLZvbrIJIkm/yDz55fqYY/9z59/RmFoWSKvmzTbu8mY5+4eS5n/E/VYI5gipsnj68vmg2hjjagBwjY0wnMVUeOl+eVM4Fojxoqwrr6uv50JR9cIIWIYhb0TLcuaIwOj2Cen3sv3l+4jl0Yj3IJdEjbW6uHhk8YOR+wcZaz7IBDh6T4iBhCGHmUMEMOqV4ooDOuhPHeu0ntLlY88adb83Lla12AMIBq9+89Kw/txtXdhH4IBRKP74IpYjm9f5/AECXxJDHvrKA3cLPynmw08yiBS60iq4jyvVtvnDp5ldknYht47TxGH7O/7+Kxx1DUiDBH6lJ36b89wvoSdJhDR6FFyFeXPB2fddnDNIMLRp4yoKGF276x8+MQoYr71dtMOdooBYjBDmSL81V/fr35Pqp5LzABC6ARVhBuFVtiBU1ZgiBjM8mnaw/Vu6oM1PUBErXcuPZ26bbKdbcAbpASJQecUwdazrvXBznkYIIa3odJ42OWPv+cU64QJEc7gFsKXhNXqFTsChG3pE3SrolTJt9LcwKcfA0SrV6xVhEhXTzd3PmyEAYiNtTiepZCdWWxXcHczRZjGoiwZ3Dt8SQxvf0NpdCv/EG/A++FWaXTLDcUMTKaCiOEcKuLoseWBwSfmo6rhXcjgemD0b/+8yIJGyHeQfMX0rz302HCW06cb55NhfsJ/cFKnLZWPsv8ApYY3lhIKAAA='
        r = verify_real_time_token(url_encoder(token))
        rtb = meister_rtb_ids
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='ios', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_ifa))
                assert_that(device_info['source'], 'ifa')

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, IDFA disallowed, IDFV disallowed')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_ios_02(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAE3WUXW/aMBiF/4tvyyAffKRMvQhdJ20So3RQsY4pchLH8TB2GtuBlfa/z8G0BGFykUTx4/Oe49fxDiScCcQkGO5AkhSwfgoJpRJgCHghURoRBt5aAKdFeTKo2IrxDQMtIMka6c/rAgydFtDvAmIUVagUhDNNakRwVSZIvxcqpkTkqARvWjRFFak/7/Ya0QtnNRMKApednzlkOIdEzyZc1AxJs6qW0xNjKCUq/0UC6jIRYjCmKAXDDFKBNJ/pHMA5XJ8st/dLi1NdRmnDegaq01ScKu2FogpRHajdN6TnB1036A2u3RZAW4mYCbero7H03IKIBEkR5fB8TKRRAss0ghUktB46jNQrUqJnpRdz3w7OMoKjRrF6JXmZEgZpVBG0AUOvBYoSJTDJdaMkX2kSDH8D7/VbOcuc8ObmNYljj6ypVGSVDfIeo10Ha5kzQjYI19kTo2D7tN28E7zXIK4NwV1/Vhw10iPhV4agubpn03eCNTU8bCOaTvtGI3i5ygb4g2g6DQzhqLtw2Zna41oR1vDa7Ron69XDj/QjL22I+NKxEOtGGl8Zonvr0PHUvqrYQpz48I3Gl3mwGG2sGp6NOM1iiHDy/ekqtDqV2EY0e6cMMUhiP7ZX8W3E6Q45dDe+X4xCq0bvsIfm+fz2Qv+xheBNIjHEbEEf/x59NKtAQ5T5r8KbWvfQwBCCTJadr6FVJDZWFx6fTy6EMSKee1cUF7aqITbjKXKwNe7AVHkO8HiN7T8VBn/q82MVKaHPPX1q1Sc3eFQMU7Ts9Nuu13Y+MyhJhfQB+x+palNA3gUAAA=='
        r = verify_real_time_token(url_encoder(token))
        rtb = ext_non_test_mode_kraken_rtb_ids_vast
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='ios', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(partner_device_id))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(partner_device_id))
                assert_that(device_info['source'], 'ifa')

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, IDFA allowed, IDFV disallowed')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_ios_03(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAE22W23KbOhSG30W3iRsZMCbu9AI7yezuGcd2G2fcNnsYAbJQwAIjDjm0714ROY7YXlcw6OP/10kavaIoF5KKCk1eURQVpHvKilS1RBOUFxWNAy7Qn3PE4qLsLdYiFXkr0Dmq+I6qz7sCTfA5Uu+SMBo0tJQ8F4pUiMzrMqLqvajDjMuEluiPEo1pw7vPr28awUsuOsaXnDxcfE+IYAnh6m+ey47h8bbp5NSPIakqWj4HkiibgAoSZjRGky3JJFX8VuWBxr5rTS+n/uAaz7yB49jWwHMta3CDnRtvZF/5U99V4pmyqVXA6g8qBrNb9anJs1qFk9GGZm850aeKCp3Na5eLiE89ZSB5TLOcnK7JOIhIGQekITzrlg4rXQlKuq9V9d7qn4stZ4Fh1pUuL2MuSBY0nLZoMjxHRUkjEiWqM1WeKhJNfiHr99fybov9L19+R2Fo2zKrap5ux8lIZOMtVjL/J6qRQTBNTJP756fVO9HEBlEBhDM0CG+siQrPra9HAlcGMdKEffZ9+eNIuKZGCBF9F/ZGNCyt9wx0cQ6Rek8/n9r3XGqDGOfslHCwUQ8PHzQ2OGJHl5EZBwGIfsVKBmgMTZcRRHhmLpEm8qF9Vxw7V5q9pTqOLKmX4ti5yoyDMYCoze4/ag3v5Ww7hnORDCBqMw6hifno8vkKniCJT4l+b12tgetr/+FiBY8yiFQmwrXP42KxfmzhWWanhDM06+5pYpd+u42PGntTI8IQYU7ZoXfODGdzONIEImrTJdMu/9y5y6aFawYRrjllRLuE6a278OEdo4mrtbeZtnCkGCB6M5Rqwl/8+/PsY1LNXGIGENIkqCbGUWiHLThlOYaI3iwfpj1cbqY+WNMdRFRm5/hh162T9WwFniAFSPQ6pwm2nLWND3bOwwDRPw21xt0mu/+YU2wSFkS4vRMEnxJ2Y1ZsDxCObU7QpXYpkx+FtYJ3PwaIxqxYownJFw8XNz4cCAMQBxs+nq2RjZWvF3B3U01Yw+uiYHDv8CnRP/2HWqOdryhmYKglBoj+lGli77H5jsH74aCx8Hfxx3lo9u7yvarhTcjgemD0X3e9SINaqnuQusV0Nzl0XwuW0YcL99PQ+oQ/C1LxhqoL11/0Mzs97gkAAA=='
        r = verify_real_time_token(url_encoder(token))
        rtb = meister_rtb_ids
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='ios', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_ifa))
                assert_that(device_info['source'], 'ifa')

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is false, IDFA disallowed, IDFV allowed')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_ios_04(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAE42VX2+bMBTFv4tfmzT8h2bqA0kTaZO6LltTZV0mZMAYL45NsSFd0373mThtieqH8ZAg/OPcc+41sAcZZwIxCcZ7kGUV7P6FhLIRYAx4JVGeEAZeBgDnVX2y2LAN4zsGBkCSLVKXtxUYWwOgzgXEKGlRLQhnilSI4E2dIXVeNSklokQ1eFGiOWpJd3l/0EieOOuYWBC4Hv0oIcMlJOpuwkXHkLxou+VgejGLr5yh68fx0IuDeDiZT4PhfGqHs3Aazyee3zlOoZSo/psIqKwkiMGUohyMC0gFUpqFygqs4zE0/LweygBVVhoVSt2BusQtp43yS1GLqAp9HmjScSPPjvzwwh4A9CgR0w3Yd/FZ/tGCSATJEeXw45rIkwzWeQJbSGi3dFzpulajh0Y1/DAyzgqCk16xrtu8zgmDNGkJ2oGxMwBVjTKYlWqYkm8UCca/gPP8ub4trPjy8jlLUwe7VDZkU4Slz6h7SP2BkD3C1sQkerx/3L0Svt8jLo7EysowfiP6Ghk+ENx2b6v3Kvk74TSaoGXzjS1eCa9fxbFMRL9KoDWip7MixEYi0hpWM4vXo4XRSPsfiK6z3Xz/mr91xOl5dYRlInp9d6QmvKlFrxfmvmMD4fV8uK4mrpbRarIzT9dEnGh42kd88+X+LDY6FdhAuP20jdYIs9RNd+bZYRPRTxse559+W01ic1rLRPTTBprgy3I5XRgJHxuI072sidsVvfvzvtv7PqCuUpc/K8e8D0MT4fd9QF1FkJv1aB4bkVSLrBy+vDE3xNMijj2rKmwME2lid71AFjY3xDIQJ49uqjUeIny9xcbxSwx+d++xTdII9f5Vb8/uKwPuGoYpWo+Cc9s5tz4xKEmL1MfgHzbJAgOKBgAA'
        r = verify_real_time_token(url_encoder(token))
        rtb = meister_rtb_ids
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        token_idfv = token_response_payload['token']['device']['ios']['idfv']
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=False, rtb=rtb,
                                                platform='ios', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_idfv.lower()))
                assert_that(device_info['source'], 'IDFV')

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true, IDFA allowed, IDFV allowed')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_ios_05(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAE4WWXW/aMBSG/4tvW4ZJCKRMuwhsaJ1Ega1UbGOKnMQ4LsYO+aJdt/8+p4bVUc+0XEAUP3nPp0/8hGIlCypLNHpCcZyR5r8oSVkVaIRUVtIk5BL9vkQsyfLWYiV3Uh0lukQl31P9eJ+hEb5E+r4gjIY1zQuupCY1Uqgqj6m+z6pI8CKlOfqtRRNa8+bx07NG+FPJhgkKTjbdLymRLCVcv81V0TA82dZ6eeoPp2PfczvT/sTv9IPhpHM1cJwO7nv+0B9cDYbBpPE4ImVJ88ewINqVkEoSCZqg0ZaIgmrNrY4V4dPVAX7Ol3ZAaFcqHZR+g8rO5EY/qpWotMuC1lQ8x00fSipNxE9NvDJ5bbMIC55QocjrtSIJY5InIakJF83SaaVJU04Plc7wc42U3HIWWsaa9Ko84ZKIsOb0iEbOJcpyGpM41dUr1U6TaPQdOb+u89stDt69+xVHkct6SVnx3XaYelKQbRPmK0JYBGPPxDi9e3xYngnPIiIfA4TrWRql0SjxzLn+S/RLS8MzGu7Fl8XXFyuWp9GQAQSx/YiMRs121YGBVvqnWPyHbw/HM+HY0SqIcG0NfIp2jWMGW3EhgthEDBGORZADRPi2xpXxVPXc2+ylcnbWE0OItFrIJVjbFAOEY2vcGw3/58V2yMCM7SGiXX1jZeZdPb6H+6OACM+z+8NYwdWHYNNdgq1M8f8Ro3I/n6/uj7AnENHudkPk15vu2DknPvVtZ2OD7Hefb5K/Itg2E4GE3QCnFulPsJjBxWMgYWvcG+Lj7WBRH8EtQyCilfiBIaLdzWAewJvKEO9X/np8BD3lENFqImnyEcw/fbv4RzNjiGiNMqMxjCM3gv1IIcKxNXanDREt1uMAzClnANGOxWioVbqaLOEtAxK2ldwQbDE51gFcOQYQ7YFpNG7X4u6llVtj6NSFbaI9ZCCNvt0fPYhoxZIZIk+/Zg6cD8EAorUtc0MUfL7pTgPQzAFE2oPZIGtHrV56uV1/Qzi9D1kGjzuFAcK1NSqjcZwtKWagFYEhopUzo3Hw2WzP4PlwsjIP9gn8wRycsxpNI/hD5TD0ozmB7MKq0EclfdBpDoTorpJM0E138KbnvMFvJSl5TfW57Q9j46qbNQoAAA=='
        r = verify_real_time_token(url_encoder(token))
        rtb = meister_rtb_ids
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        token_idfv = token_response_payload['token']['device']['ios']['idfv']
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb,
                                                platform='ios', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_idfv.lower()))
                assert_that(device_info['source'], 'IDFV')

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true, IDFA disallowed, IDFV disallowed')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_ios_06(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAE4WWXU/bMBSG/4tvgWFSSj8mLgrbtE0qLaNl3cYUOYnreHXtNI5TGOy/z8EltbWDlos2ip+c854vx48oVVJTWaHhI0rTgjT/uiKV0WiIVFHRLOYS/TlELCvKYNHIlVRbiQ5RxdfUPl4XaIgPkb3XhNG4pqXmSlrSIlqZMqX2vjCJ4DqnJfpjjWa05s3jx2cb8W8lG2akObk7vsmJZDnh9m2udMPwbFk35uyLCakqWj7Emlg3MZUkETRDwyURmlp+aeNAeHcdAT8vlzUurBtjBds3qDy6vLKPaiWMlSNoTcVzTPS+otJF89jEIrN/fepY84wKRf5d01mckjKLSU24aJZ2K00KSroxNnvP+VdyyVnsOWtSp8qMSyLimtMtGkaHqChpStLcVqZSK0ui4Q8UPX2dmW7Bzs+f0iTpZKqqDF8te3lXCvIcZvT0qZwt8WhHpIVHDKL/Eh1HXOS3D/fXL4T2iYIBRJl5xNIRFR5Hn/Y2fEI6onNwM/3WEnXXIwwGiMonSkfUbGU2rPXiE+ud0v799/stqENhgCh9G9mOWOCUtV5q30YNEaWfMQESvpeUAYQRHqEdoU46s2JfOZ/AjhC5mco2YxtfaRckfKWJU9r/fbDstTo2vhcCEUH1mSPG3cHDu1c6CCLCDnIENu9Hd8fXYLgnMBJ0u4v312Qy/7UFlWwwQARKcmdjvfpylbWEP3V9AxGFV93+rkNOL7EY7/Pu1/+UQYQfbt8RH2dn07r1YvxYKgwQQbTK2UhWV2eTETgx0tl4N+8vLrag0g6DCD9jPWdjNPn8/WDfqZmfDwYRQXEd0UuTTgLrOMUQ4es4c4RIpouLEWijCxK+jsFu6ub5/BKeqR5IBDPlCDa93Natl2CvqyAi2Os2jpgtxK3Xp77SFQaIQEcKEcb3oiEi3JWdjjL/VkRwnw4wQAR7HXU2NJ/cHX9oww03TBgJ9mWHLCI13/dyWH9HRCfvi4KBGSEQEU6/i2Y7vqaYgV76EBHG64hNn43XDJqHwe67vZ2M1tkr37qXvCcfkle+dRj9bA4gq9hoe1Ky55zmrIdujWSC3h2fvTmJ3uC3klS8pvZI9hcFvJUKEAoAAA=='
        r = verify_real_time_token(url_encoder(token))
        rtb = meister_rtb_ids
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        token_idfv = token_response_payload['token']['device']['ios']['idfv']
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb,
                                                platform='ios', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(partner_device_id))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(partner_device_id))
                assert_that(device_info['source'], 'ifa')

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true, IDFA allowed, IDFV disallowed')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_ios_07(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAE4WWW1PiMBTHv0teRQ3lIrLjA95m3RkEVnDQdaeTtiGNhLQ0bUHR776pQUjWs7N9gE7z6/9cc5oNChOpqMxRd4PCMCXVv8pJXijURUma08jnEr3XEIvSzFks5FwmK4lqKOcLqh8vUtTFNaTvFWHUL2mmeCI1qRGVFFlI9X1aBIKrmGboXYtGtOTV482Hhv+ayIrpKU6eju9iIllMuH6bJ6pieDQrKzn9YkDynGYvviLajE8lCQSNUHdGhKKan+k4EN5eh8DP56XFhTZTaIf1G1QeXtzqR2UiCu2OoCUVHzHRdU6liWZTxSKjrzaVr3hERUK+rqnID0kW+aQkXFRL25UqBRldFjp7H/lP5Iwz3zJWpS7JIi6J8EtOV6jr1VCa0ZCEsa5Mnsw1ibq/kPd2k41nuHd29hYGQYPVRV7w+ewkbklBGNMyX4jIImb4gziP71/Wo0+i0bKInAFEy7ISdIxGjvvezY5o5hbRMkTj4G74sCOIrRFARMvyNDgxfpRsXiwZaKW59bSzflyvdrHYBMYA4dkZS7YaUxyynZWOrXEKEcQmQgwQjqcNiPAsgiwNkdQb43RfObsukfFDxMVQ7jLm2cQzRDj9ERsrndeD2QmDqw8RTsYWxkq/dfpyua9cy64+RDhWlLGCi6ve0/EIbFTK/o8YlefBYPK8gjuVAYTriSEW85+30Y7AdmW21f2LsDUCo9G8wKK/99TWeMYQ4excQ3wft4flCsxqGyKcPUUMEcxv24MevGMMcTnpTM/h/SAZQDiecqPRG/x4PPjHjGEQ4fSy0TgJg0aw98PWmEOE28vbbg+G0/MeHAsGCKcu3Ggkk3hyMQL3ZYYhwtkPhmDDi1W5s+JOMohwK2f8GE/F/b5PnRkTQIQ7pzBANO0OqkOEE21qiCx+SD1452YMIJx8CEMoPng6vobbsAEi7jw0yNRLJvtedjvEEF79Kk33s8wmCohwp7+Jd9UfUQzP5ZRBhG1FGI1lh/UXDJ4gW41BbxHB37r2Z1aD6wD+gngM/a6OF3O/UPocpE8x1UkO3ReSCfp03D6qe0f4myQ5L6k+cP0BVFIb9u4JAAA='
        r = verify_real_time_token(url_encoder(token))
        rtb = meister_rtb_ids
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb,
                                                platform='ios', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(partner_device_id))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(partner_device_id))
                assert_that(device_info['source'], 'ifa')

    @allure.feature('real-time ad')
    @allure.tag('real time token E2E')
    @allure.story('PBJ-4409 Realtime - Support putting device ids in realtime token')
    @allure.description('Verify RTA tokens work well for case:'
                        'disable_ad_id is true, IDFA disallowed, IDFV allowed')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_device_id_E2E_ios_08(self, pub_app_id, placement, sdk_v, partner):
        token = '3:H4sIAAAAAAAAE4WVXXOiMBSG/0tuqzUi1I+dXqDWme6Mum6163bdYQKEkIoJEkBb2/++obE2TtNZLpQhD+8578kJ5wACzgRmOegdQBCkqPoXOcoLAXqApzkOPcrAaw2QMM3OFgu2ZnzHQA3kdIPl400KerAG5L1ABHslzgTlTJISEbzIAizv08JPqIhxBl6laIhLWj0+vGl4z5xVjCsoWjXuYsRIjKh8m3JRMTSMSrncb3YHln3j1m27ParbQ3tU71twUHe7Qwc2+90WhHaVsY/yHGdPnkAyFQ8z5Cc4BL0IJQJLzUh6BfB41Q0/75dMIJGpFNKUfAOz+mAiH5U8KWTKCS5x8uYb73PMlOND5ZeFn2MKT9AQJxx9XhOhF6As9FCJaFItHVeqMmV4W8gKv+0RZxElnhasKi/PQspQ4pUU70DPqoE0wwEKYrl7OV9LEvT+AOvl17xwUnJ9/RL4fivIkryg66gdOyzp0sqm9XKbzSPovhNprhGt/xKWIvrx/dN+dooSakREFNHZP+x3J8LRiPCosYQBIUYiUBq82ZqnH3noXqAiwlVjsrv7ENFTXSskiYsf7JTqVid8aCJ0M47S6DxfRG1itEuggdjqqSJFjJ3u0/CLkikCFjfuqjEz150YET1OU6k8TqeLx50xTqxEsttVo2+5ZjsK2ax/TsKTSKrtTaeEBoJruXYKpWEPYDKeGUvSMRJ6B9iKGC46y/7OuDVtaCJ0jZbScKffHy7MXdQ0EqHu9tiJSzoqvjhVimgHfss3Z3oFTcSZ22Mj+j+WfddYsS4xEbqGozT4Il4Mvmh3YiLOaqqI+TK5/2ihM41ARdlOnCU11+NREVn8O7VmxtONiYE4d6s0BJ2uGiPX/BFRIkuLL6auueyKsJo3aWo+uzE0EGd2kdK4HWY5dc12FbEbzzA0f8wwNBBnmXaORe2Q8YaY2rArJ9Tfan6svULIQSfHVDXOwX3BSIJXjavLpnUJvzGU0xLLqfsPKtUbEvMHAAA='
        r = verify_real_time_token(url_encoder(token))
        rtb = meister_rtb_ids
        token_response_payload = r.json()
        token_ifa = token_response_payload['token']['device']['ifa']
        token_idfv = token_response_payload['token']['device']['ios']['idfv']
        partner_device_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=partner_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=rtb,
                                                platform='ios', provide_token=token)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, rtb)
                device = bid_request['device']
                assert_that(device['ifa'], equal_to(token_ifa))
                device_info = response_payload['ext']['debug']['auction_result']['device_info']
                assert_that(device_info['id'], equal_to(token_idfv.lower()))
                assert_that(device_info['source'], 'idfv')