# from http import HTTPStatus
#
# import pytest
# import allure
#
# from utils.behaviors import request_hb_win_notification, request_hbp_no_notification
# from utils.common import *
# from utils.assertions import *
# from settings import *
# from data import response_schema, request_payload
# import time
#
#
# @allure.epic('scrat - report ad - v5')
# class TestReportAdHBMessageMax(object):
#
#     # @allure.feature('hb message')
#     # @allure.tag('normal', 'R_0.106.0')
#     # @allure.story('PBJ-2097 Not record max bid info in redis')
#     # @allure.description('Verify that there is no hb message when hb request with max')
#     # @allure.severity('normal')
#     # @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     # @pytest.mark.parametrize('placement', [common_test_placement])
#     # def test_report_ad_hb_message_max_not_record_bid_info(self, pub_app_id, placement):
#     #     if request_info['is_hbp_responded_200']:
#     #         req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
#     #                                                app_id=request_info['app_id'], campaign=request_info['campaign'],
#     #                                                ad_token=request_info['ad_token'])
#     #         r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
#     #
#     #         response_payload = r.json()
#     #         debug = response_payload['ext']['debug']
#     #         assert_response_status_code(r.status_code, HTTPStatus.OK)
#     #         assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#     #         assert_keys_exist(debug, 'hb_message')
#     #         assert_that(debug['hb_message'], equal_to(None))
#
#     @allure.feature('hb message')
#     @allure.tag('normal', 'v0.113.0')
#     @allure.story('PBJ-3000 MAX bid info has been cached on DynamoDB')
#     @allure.story('PBJ-3212 Only using tpat.start for MAX billing calculating')
#     @allure.description('Verify that there is hb message when hb request with max and send win notification')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('placement', [common_test_placement])
#     def test_report_ad_hb_message_max_record_bid_info_1(self, pub_app_id, placement):
#         ordinal_view_count = 11
#         request_info = request_hb_win_notification('max', ordinal_view_count, test_ifa=gen_device_id(36))
#         time.sleep(0.1)
#
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
#                                                    app_id=request_info['app_id'], campaign=request_info['campaign'],
#                                                    ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
#             response_payload = r.json()
#             debug = response_payload['ext']['debug']
#             assert_response_status_code(r.status_code, HTTPStatus.OK)
#             assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#             assert_keys_exist(debug, 'hb_message')
#             assert_that(debug['hb_message'] is None)
#
#
#     @allure.feature('hb message')
#     @allure.tag('normal', 'v0.114.0')
#     @allure.story('PBJ-3091 MAX has the same logic to send Vungle bill notification')
#     @allure.story('PBJ-3212 Only using tpat.start for MAX billing calculating')
#     @allure.description('Verify that there is hb message when hb request with max')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('placement', [common_test_placement])
#     def test_report_ad_hb_message_max_record_bid_info_2(self, pub_app_id, placement):
#         ordinal_view_count = 11
#         request_info = request_hbp_no_notification('max', ordinal_view_count, test_ifa=gen_device_id(36))
#         time.sleep(0.1)
#
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
#                                                    app_id=request_info['app_id'], campaign=request_info['campaign'],
#                                                    ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
#
#             response_payload = r.json()
#             debug = response_payload['ext']['debug']
#             assert_response_status_code(r.status_code, HTTPStatus.OK)
#             assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#             assert_keys_exist(debug, 'hb_message')
#             assert_that(debug['hb_message'] is None)
#
#
#     @allure.feature('hb message')
#     @allure.tag('normal', 'v0.122.0')
#     @allure.story('PBJ-3070 Disable Server side bill notification if SDK version >=6.10.1')
#     @allure.description('Verify that the bill notification will be disabled when reportAd SDK version >= 6.10.1')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('placement', [common_test_placement])
#     @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
#     def test_report_ad_disable_bill_notification_max_1(self, pub_app_id, placement, sdk_v):
#         test_ifa = gen_device_id()
#         request_info = request_hbp_no_notification('max', 11, test_ifa=test_ifa, sdk_v='Vungle/6.10.0')
#         time.sleep(0.1)
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
#                                                    app_id=request_info['app_id'], campaign=request_info['campaign'],
#                                                    ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req,
#                      headers=platform_headers(debug='scrat', sdk_version=sdk_v))
#
#             response_payload = r.json()
#             debug = response_payload['ext']['debug']
#             assert_response_status_code(r.status_code, HTTPStatus.OK)
#             assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#             assert_keys_exist(debug, 'hb_message')
#             assert_that(debug['hb_message'], equal_to(None))
#
#     @allure.feature('hb message')
#     @allure.tag('normal', 'v0.122.0')
#     @allure.story('PBJ-3070 Disable Server side bill notification if SDK version >=6.10.1')
#     @allure.story('PBJ-3212 Only using tpat.start for MAX billing calculating')
#     @allure.description('Verify that the bill notification will not be disabled when reportAd SDK version < 6.10.1')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('placement', [common_test_placement])
#     @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
#     def test_report_ad_disable_bill_notification_max_2(self, pub_app_id, placement, sdk_v):
#         test_ifa = gen_device_id()
#         request_info = request_hbp_no_notification('max', 11, test_ifa=test_ifa, sdk_v='Vungle/6.10.0')
#         time.sleep(0.1)
#
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True,
#                                                    app_id=request_info['app_id'], campaign=request_info['campaign'],
#                                                    ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req,
#                      headers=platform_headers(debug='scrat', sdk_version=sdk_v))
#
#             response_payload = r.json()
#             debug = response_payload['ext']['debug']
#             assert_response_status_code(r.status_code, HTTPStatus.OK)
#             assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#             assert_that(debug['hb_message'], equal_to(None))
