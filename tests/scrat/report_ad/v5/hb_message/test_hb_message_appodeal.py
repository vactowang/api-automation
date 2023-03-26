# import pytest
# import allure
#
# from http import HTTPStatus
# from data import request_payload
# from utils.behaviors import request_hb_win_notification
# from utils.common import *
# from utils.assertions import *
# from settings import *
# from data import response_schema
# import time
#
#
# @allure.epic('scrat - report ad - v5')
# class TestReportAdHBMessageAppodeal(object):
#
#     @allure.feature('hb message')
#     @allure.tag('normal', 'R_0.101.0')
#     @allure.story('PBJ-1961 Avoid header_bidding if SDK Version < 6.6.1 and pub is not appodeal')
#     @allure.description('Verify the header bidding works for appodeal pubs via both SDK < 6.6.1 and SDK >= 6.6.1')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub', [{'pub_app_id': '5a35a75845eaab51250070a5', 'placement_ref_id': 'DEFAULT52238'},
#                                      {'pub_app_id': '5963678b3fc929fb1000090b', 'placement_ref_id': 'DEFAULT35140'}])
#     @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.0', 'Vungle/6.6.1', 'Vungle/6.6.2'])
#     def test_report_ad_hb_message_appodeal_pubs_1(self, pub, sdk_v):
#         test_ifa = gen_device_id()
#         ordinal_view_count = 11
#         request_info = request_hb_win_notification('max', ordinal_view_count, test_ifa=test_ifa,
#                                                    pub_app_id=pub['pub_app_id'], placement_ref_id=pub['placement_ref_id'])
#
#         time.sleep(0.1)
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub['pub_app_id'], pub['placement_ref_id'], ifa=test_ifa,
#                                                    header_bidding=True, app_id=request_info['app_id'],
#                                                    campaign=request_info['campaign'], ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', sdk_version=sdk_v))
#
#             response_payload = r.json()
#             debug = response_payload['ext']['debug']
#             assert_response_status_code(r.status_code, HTTPStatus.OK)
#             assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#             assert_keys_exist(debug, 'hb_message')
#             assert_that(debug['hb_message']['event_id'], equal_to(request_info['event_id']))
#             assert_that(debug['hb_message']['bidid'], equal_to(request_info['bid_id']))
#             assert_that(debug['hb_message']['supply_name'], equal_to('max'))
#             assert_keys_exist(debug['hb_message'], 'timestamp')
#             assert_that(debug['hb_message']['bid_price'], equal_to(request_info['bid_price']))
#             assert_that(debug['hb_message']['settlement_price'], equal_to(request_info['bid_price']))
#             assert_that(debug['hb_message']['bid_won'], equal_to(True))
#             assert_that(debug['hb_message']['is_bill'], equal_to(True))
#             assert_that(debug['hb_message']['notification_type'], equal_to(102))
#             assert_that(debug['hb_message']['n_ordinal_view'], equal_to(request_info['ordinal_view']))
#             assert_that(debug['hb_message']['adv_is_internal'], equal_to(True))
#
#     @allure.feature('hb message')
#     @allure.tag('normal', 'R_0.103.0')
#     @allure.story('PBJ-1990 Add one more pub for appodeal hbp')
#     @allure.description('Verify the header bidding works for appodeal pubs via both SDK < 6.6.1 and SDK >= 6.6.1')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub', [{'pub_app_id': '5cfe1d24706918125238768f', 'placement_ref_id': 'DEFAULT-4587331'}])
#     @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.0', 'Vungle/6.6.1', 'Vungle/6.6.2'])
#     def test_report_ad_hb_message_appodeal_pubs_2(self, pub, sdk_v):
#         test_ifa = gen_device_id()
#         ordinal_view_count = 11
#         request_info = request_hb_win_notification('max', ordinal_view_count, test_ifa=test_ifa,
#                                                    pub_app_id=pub['pub_app_id'], placement_ref_id=pub['placement_ref_id'])
#
#         time.sleep(0.1)
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub['pub_app_id'], pub['placement_ref_id'], ifa=test_ifa,
#                                                    header_bidding=True, app_id=request_info['app_id'],
#                                                    campaign=request_info['campaign'], ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', sdk_version=sdk_v))
#
#             response_payload = r.json()
#             debug = response_payload['ext']['debug']
#             assert_response_status_code(r.status_code, HTTPStatus.OK)
#             assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#             assert_keys_exist(debug, 'hb_message')
#             assert_that(debug['hb_message']['event_id'], equal_to(request_info['event_id']))
#             assert_that(debug['hb_message']['bidid'], equal_to(request_info['bid_id']))
#             assert_that(debug['hb_message']['supply_name'], equal_to('max'))
#             assert_keys_exist(debug['hb_message'], 'timestamp')
#             assert_that(debug['hb_message']['bid_price'], equal_to(request_info['bid_price']))
#             assert_that(debug['hb_message']['settlement_price'], equal_to(request_info['bid_price']))
#             assert_that(debug['hb_message']['bid_won'], equal_to(True))
#             assert_that(debug['hb_message']['is_bill'], equal_to(True))
#             assert_that(debug['hb_message']['notification_type'], equal_to(102))
#             assert_that(debug['hb_message']['n_ordinal_view'], equal_to(request_info['ordinal_view']))
#             assert_that(debug['hb_message']['adv_is_internal'], equal_to(True))
