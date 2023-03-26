import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_hb_win_notification
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('scrat - report ad - v5')
class TestReportAdMessageHB(object):

    @pytest.fixture(scope="class", autouse=True)
    def get_hb_request_info(self):
        global request_info
        ordinal_view_count = 11
        request_info = request_hb_win_notification('max', ordinal_view_count)

    @allure.feature('report ad message')
    @allure.tag('hb')
    @allure.story('report ad message hb from debug info')
    @allure.description('Verify report ad message hb flag from debug info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('hb_flag', [True, False])
    def test_report_ad_message_hb_flag(self, pub_app_id, hb_flag):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=hb_flag,
                                               app_id=gen_test_app_id(), campaign=request_info['campaign'],
                                               ad_token=request_info['ad_token'])
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_that(debug['report_ad_message']['is_header_bidding'], equal_to(hb_flag))

    @allure.feature('report ad message')
    @allure.tag('hb')
    @allure.story('report ad message hb from debug info')
    @allure.description('Verify report ad message hb flag version contrl from debug info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.0', 'Vungle/6.5.9', 'Vungle/6.6.1', 'Vungle/6.6.2'])
    def test_report_ad_message_hb_flag_version_ctl(self, pub_app_id, sdk_v):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=True,
                                               app_id=gen_test_app_id(), campaign=request_info['campaign'],
                                               ad_token=request_info['ad_token'])
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', sdk_version=sdk_v))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        if sdk_v in ('Vungle/6.6.1', 'Vungle/6.6.2'):
            assert_that(debug['report_ad_message']['is_header_bidding'], equal_to(True))
        else:
            assert_keys_not_exist(debug['report_ad_message'], 'is_header_bidding')

    @allure.feature('report ad message')
    @allure.tag('hb')
    @allure.story('report ad message hb info from debug info'
                  'PBJ-3367 Remove bidinfo from scrat reportAd message')
    @allure.description('Verify report ad message hbp supply name from debug info')
    @allure.description('Verify hbp supply name is removed from debug info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_remove_hbp_supply_name(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=True,
                                               app_id=request_info['app_id'], campaign=request_info['campaign'],
                                               ad_token=request_info['ad_token'])
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug['report_ad_message'], 'hbp_supply_name')


    @allure.feature('report ad message')
    @allure.tag('hb')
    @allure.story('report ad message hb info from debug info'
                  'PBJ-3367 Remove bidinfo from scrat reportAd message')
    @allure.description('Verify no hbp bid info from debug info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_remove_hbp_bid_info(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=True,
                                               app_id=gen_test_app_id(), campaign=request_info['campaign'],
                                               ad_token=request_info['ad_token'])
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug['report_ad_message'], 'hbp_bid_id')
        assert_keys_not_exist(debug['report_ad_message'], 'hbp_bid_price')
        assert_keys_not_exist(debug['report_ad_message'], 'hbp_bid_timestamp')
        assert_keys_not_exist(debug['report_ad_message'], 'hbp_cache_source')



    @allure.feature('report ad message')
    @allure.tag('hb')
    @allure.story('report ad message hb info from debug info'
                  'PBJ-3367 Remove bidinfo from scrat reportAd message')
    @allure.description('Verify no hbp ordinal view count from debug info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_report_ad_message_remove_hbp_ordinal_view(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=True,
                                               app_id=gen_test_app_id(), campaign=request_info['campaign'],
                                               ad_token=request_info['ad_token'])
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        assert_keys_not_exist(debug['report_ad_message'], 'hbp_ordinal')
