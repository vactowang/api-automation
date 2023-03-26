
import allure

from utils.behaviors import  request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('Real-time source ext')
class TestBidRequestSourceExt(object):

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the schain fields in openrtb25x - sid is not in seller.json')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_schain_info_openrtb25x_sid_not_in_seller_json(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ca_us_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                schain_obj = bid_request['source']['ext']['schain']
                assert_that(schain_obj['ver'], not empty())
                assert_that(schain_obj['complete'], not empty())
                assert_that(schain_obj['nodes'][0]['asi'], not empty())
                assert_that(schain_obj['nodes'][0]['sid'], not empty())
                assert_that(schain_obj['nodes'][0]['name'], not empty())
                assert_that(schain_obj['nodes'][0]['rid'], bid_request['id'])
                assert_that(schain_obj['nodes'][0]['hp'], not empty())


    # --------------------------------------------- OM SDK -----------------------------------------------------------
    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for om enabled app')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_om_enabled_status_source_ext_app_enabled(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ca_us_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                source_ext = bid_request['source']['ext']
                assert_that(source_ext['omidpn'], equal_to('vungle'))
                assert_that(source_ext['omidpv'], equal_to('6.11.0'))


    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for no om setting in app level')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_om_enabled_status_source_ext_app_default_setting(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=ca_us_ip, platform='android',
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                source_ext = bid_request['source']['ext']
                assert_that(source_ext['omidpn'], equal_to('vungle'))
                assert_that(source_ext['omidpv'], equal_to('6.11.0'))
