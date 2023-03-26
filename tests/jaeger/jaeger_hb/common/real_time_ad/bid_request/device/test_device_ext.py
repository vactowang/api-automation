import pytest
import allure

from utils.behaviors import request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('Real-time bid request')
class TestDeviceExt(object):

    @allure.feature('bid request device')
    @allure.story('PBJ-2363 Jaeger bid request muted field should be correct')
    @allure.description('Verify the muted in bid request should be 0 when sound_enabled is 1 for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sound_enabled', [True])
    def test_real_time_sound_enabled_android_1(self, pub_app_id, placement, sdk_v, partner, sound_enabled):

        info = request_hbp_with_real_time_token(partner, 11, platform='android', pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, sound_enabled=sound_enabled,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['device']['ext']['vungle']['muted'], equal_to(0))

    @allure.feature('bid request device')
    @allure.story('PBJ-2363 Jaeger bid request muted field should be correct')
    @allure.description('Verify the muted in bid request should be 1 when sound_enabled is 0 for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sound_enabled', [False, None])
    def test_real_time_sound_enabled_android_2(self, pub_app_id, placement, sdk_v, partner, sound_enabled):

        info = request_hbp_with_real_time_token(partner, 11, platform='android', pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, sound_enabled=sound_enabled,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['device']['ext']['vungle']['muted'], equal_to(1))

    # @allure.feature('bid request device')
    # @allure.story('PBJ-3781 Send Vungle Device extension to LiftOff')
    # @allure.description('Verify that exist vungle extension and IDFV pass to liftoff when allow_idfv is false')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # @pytest.mark.parametrize('partner', ['max'])
    # def test_liftoff_device_ext_01(self, pub_app_id, placement, sdk_v, partner):
    #
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
    #                                             explain=True, ip=eu_country_ip,
    #                                             rtb=ext_non_test_mode_kraken_rtb_ids_mraid_liftoff)
    #
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         if "err_msg" not in response_payload['ext']:
    #             bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_mraid_liftoff)
    #             assert_keys_exist(bid_request['device']['ext'], 'vungle')

    @allure.feature('bid request device')
    @allure.story('PBJ-3781 Send Vungle Device extension to LiftOff')
    @allure.description('Verify that exist vungle extension and IDFV pass to liftoff when allow_idfv is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_liftoff_device_ext_02(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast_liftoff)
                assert_keys_exist(bid_request['device']['ext'], 'vungle')

    @allure.feature('bid request device')
    @allure.story('PBJ-4320 Reporting iOS ATT Status')
    @allure.description('Verify that pass att status to downdtreams')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('atts', [0,1,2,3])
    def test_att_status_real_time(self, pub_app_id, placement, sdk_v, partner, atts):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip, atts=atts,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast_liftoff)

                assert_keys_exist(bid_request['device']['ext'], 'atts')
                assert_that(bid_request['device']['ext']['atts'], equal_to(atts))



