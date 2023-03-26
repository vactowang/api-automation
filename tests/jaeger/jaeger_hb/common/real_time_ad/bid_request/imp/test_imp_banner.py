import allure

from utils.behaviors import request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain
from utils.common import *
from utils.assertions import *
from settings import *



@allure.epic('Real-time imp banner')
class TestImpBanner(object):
    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp banner')
    @allure.description('Verify imp banner obj from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_imp_banner_info(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip, banner=True,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that('w' in bid_request['imp'][0]['banner'])
                assert_that('h' in bid_request['imp'][0]['banner'])
                assert_that('api' in bid_request['imp'][0]['banner'])

    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-1382 Support API attribute in OpenRTB Banner Object')
    @allure.description('Verify API attribute in banner obj for internal Banner ad')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_imp_banner_api_internal(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip, banner=True,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['imp'][0]['banner']['api'][0], equal_to(5))

    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the banner original w and h fields')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_banner_size(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip, banner=True,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['imp'][0]['banner']['w'], equal_to(320))
                assert_that(bid_request['imp'][0]['banner']['h'], equal_to(50))

    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-2813 Set imp.banner.ext.rp.size_id to request the banner in correct size.')
    @allure.description('Verify imp.banner.ext.rp.size_id in XAPI from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_banner_info(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip, banner=True,
                                                rtb=ext_test_mode_kraken_rtb_ids_banner_xapi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_test_mode_kraken_rtb_ids_banner_xapi)
                ext = bid_request['imp'][0]['banner']['ext']
                assert_keys_exist(ext, 'rp')
                assert_that(ext['rp']['size_id'], equal_to(int(43)))

    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-2813 Set imp.banner.ext.rp.size_id to request the banner in correct size.')
    @allure.description('Verify no XAPI from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_banner_info_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip, banner=True,
                                                rtb=test_mode_kraken_rtb_ids_banner_xapi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   test_mode_kraken_rtb_ids_banner_xapi)
                assert_keys_not_exist(bid_request['imp'][0]['banner'], 'ext')
