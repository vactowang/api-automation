import pytest
import allure


from utils.behaviors import request_hbp_with_real_time_token, get_bid_request_obj_from_hbp_explain
from utils.assertions import *
from settings import *


@allure.epic('Real-time bid request ')
class TestAppDetails(object):

    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify app details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_app_details(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['app']['id'], equal_to(common_test_app))
                assert_that(isinstance(bid_request['app']['name'], str))
                assert_that(bid_request['app']['bundle'], equal_to(common_test_app_market_id))
                assert_that(str(bid_request['app']['storeurl']).count('http'), equal_to(1))
                assert_that(isinstance(set(bid_request['app']['cat']), set))
                assert_that(isinstance(bid_request['app']['privacypolicy'], int))
                assert_that(isinstance(bid_request['app']['publisher']['id'], str))
                assert_that(isinstance(set(bid_request['app']['publisher']['cat']), set))
                assert_that(isinstance(bid_request['app']['keywords'], str))
                assert_that(isinstance(bid_request['app']['ver'], str))
                assert_that(bid_request['app']['keywords'], equal_to('app,account,managed'))



    @allure.feature('app details')
    @allure.tag('normal')
    @allure.description('Verify that IAB25-7 does not in cat list from bid request for rewarded video')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_remove_item_from_cat_list_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that('IAB25-7' not in bid_request['app']['cat'])
                assert_that('IAB25-7' not in bid_request['app']['publisher']['cat'])

    @allure.feature('app details')
    @allure.tag('normal')
    @allure.description('Verify the keywords from bid request come from account and pub app setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_jaeger_account_tags_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['app']['keywords'], equal_to('app,account,managed'))



    @allure.feature('app details')
    @allure.tag('normal')
    @allure.description('Verify the keywords from bid request come from account and pub app setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_jaeger_account_tags_2(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['app']['keywords'], equal_to('app,account,managed-vpn'))