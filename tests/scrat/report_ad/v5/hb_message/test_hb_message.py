# from http import HTTPStatus
#
# import pytest
# import allure
#
# from utils.behaviors import request_hb_win_notification
# from utils.common import *
# from utils.assertions import *
# from settings import *
# from data import response_schema, request_payload
# import time
#
#
# @allure.epic('scrat - report ad - v5')
# class TestReportAdHBMessage(object):
#
#     @allure.feature('hb message')
#     @allure.tag('basic', 'smoke')
#     @allure.story('report ad hb message from debug info')
#     @allure.description('Verify report ad hb message from debug info')
#     @allure.severity('smoke')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     def test_report_ad_hb_message_basic(self, pub_app_id):
#         test_ifa = gen_device_id()
#         request_info = request_hb_win_notification('max', 11, test_ifa=test_ifa)
#         time.sleep(0.1)
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=True,
#                                                    app_id=request_info['app_id'], campaign=request_info['campaign'],
#                                                    ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
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
#     @allure.tag('normal')
#     @allure.story('report ad hb message from debug info')
#     @allure.description('Verify hb message is empty when header bidding is false')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     def test_report_ad_hb_message_null(self, pub_app_id):
#         test_ifa = gen_device_id()
#         request_info = request_hb_win_notification('max', 11, test_ifa=test_ifa)
#         time.sleep(0.1)
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=False,
#                                                    app_id=request_info['app_id'], campaign=request_info['campaign'],
#                                                    ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
#
#             response_payload = r.json()
#             debug = response_payload['ext']['debug']
#             assert_response_status_code(r.status_code, HTTPStatus.OK)
#             assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#             assert_keys_exist(debug, 'hb_message')
#             assert_that(debug['hb_message'], equal_to(None))
#
#     @allure.feature('hb message')
#     @allure.tag('normal')
#     @allure.story('report ad hb message from debug info')
#     @allure.description('Verify hb message is empty when SDK < 6.6.1')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.0', 'Vungle/6.5.9'])
#     def test_report_ad_hb_message_version_ctl(self, pub_app_id, sdk_v):
#         test_ifa = gen_device_id()
#         request_info = request_hb_win_notification('max', 11, test_ifa=test_ifa)
#         time.sleep(0.1)
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=True,
#                                                    app_id=request_info['app_id'], campaign=request_info['campaign'],
#                                                    ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', sdk_version=sdk_v))
#
#             response_payload = r.json()
#             debug = response_payload['ext']['debug']
#             assert_response_status_code(r.status_code, HTTPStatus.OK)
#             assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#             assert_keys_exist(debug, 'hb_message')
#             assert_that(debug['hb_message'], equal_to(None))
#
#     @allure.feature('hb message')
#     @allure.tag('normal')
#     @allure.story('report ad hb message from debug info')
#     @allure.description('Verify hb message is empty when SDK >= 6.6.1')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.1', 'Vungle/6.6.2'])
#     def test_report_ad_hb_message_version_ctl_1(self, pub_app_id, sdk_v):
#         test_ifa = gen_device_id()
#         request_info = request_hb_win_notification('max', 11, test_ifa=test_ifa)
#         time.sleep(0.1)
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=True,
#                                                    app_id=request_info['app_id'], campaign=request_info['campaign'],
#                                                    ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat', sdk_version=sdk_v))
#
#             response_payload = r.json()
#             debug = response_payload['ext']['debug']
#             assert_response_status_code(r.status_code, HTTPStatus.OK)
#             assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#             assert_keys_exist(debug, 'hb_message')
#             assert_that(debug['hb_message'], not equal_to(None))
#
#     @allure.feature('hb message')
#     @allure.tag('basic', 'smoke')
#     @allure.story('report ad hb message from debug info')
#     @allure.description('Verify the bidrequest_test from hb message')
#     @allure.severity('smoke')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     def test_bidrequest_test_hb_message(self, pub_app_id):
#         test_ifa = gen_device_id()
#         request_info = request_hb_win_notification('max', 11, test_ifa=test_ifa)
#         time.sleep(0.1)
#         if request_info['is_hbp_responded_200']:
#             req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, header_bidding=True,
#                                                    app_id=request_info['app_id'], campaign=request_info['campaign'],
#                                                    ad_token=request_info['ad_token'])
#             r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))
#
#             response_payload = r.json()
#             debug = response_payload['ext']['debug']
#             assert_response_status_code(r.status_code, HTTPStatus.OK)
#             assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
#             assert_that(debug['hb_message']['bidrequest_test'], equal_to(0))
#
#     @allure.feature('hb message')
#     @allure.tag('normal', 'v0.121.0')
#     @allure.story('PBJ-3026 Disable HBP record bidinfo cache after 6.10.1')
#     @allure.description('Verify that the bid info will not be recorded via SDK >= 6.10.1')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('placement', [common_test_placement])
#     @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
#     def test_report_ad_hb_message_no_bid_info_recorded_1(self, pub_app_id, placement, sdk_v):
#         test_ifa = gen_device_id()
#         request_info = request_hb_win_notification('max', 11, test_ifa=test_ifa, sdk_v=sdk_v)
#         time.sleep(0.1)
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
#             assert_that(debug['hb_message'], equal_to(None))
#
#     @allure.feature('hb message')
#     @allure.tag('normal', 'v0.121.0')
#     @allure.story('PBJ-3026 Disable HBP record bidinfo cache after 6.10.1')
#     @allure.description('Verify that the bid info will be recorded via SDK < 6.10.1')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('placement', [common_test_placement])
#     @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
#     def test_report_ad_hb_message_no_bid_info_recorded_2(self, pub_app_id, placement, sdk_v):
#         test_ifa = gen_device_id()
#         request_info = request_hb_win_notification('max', 11, test_ifa=test_ifa, sdk_v=sdk_v)
#         time.sleep(0.1)
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
#             assert_that(debug['hb_message'], not equal_to(None))
#             assert_that(debug['hb_message']['is_bill'], equal_to(True))
#             assert_that(debug['hb_message']['notification_type'], equal_to(102))
#
#     @allure.feature('hb message')
#     @allure.tag('normal', 'v0.122.0')
#     @allure.story('PBJ-3070 Disable Server side bill notification if SDK version >=6.10.1')
#     @allure.description('Verify that the bill notification will be disabled when reportAd SDK version >= 6.10.1')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('placement', [common_test_placement])
#     @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
#     def test_report_ad_disable_bill_notification_1(self, pub_app_id, placement, sdk_v):
#         test_ifa = gen_device_id()
#         request_info = request_hb_win_notification('max', 11, test_ifa=test_ifa, sdk_v='Vungle/6.10.0')
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
#     @allure.description('Verify that the bill notification will not be disabled when reportAd SDK version < 6.10.1')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('placement', [common_test_placement])
#     @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
#     def test_report_ad_disable_bill_notification_2(self, pub_app_id, placement, sdk_v):
#         test_ifa = gen_device_id()
#         request_info = request_hb_win_notification('max', 11, test_ifa=test_ifa, sdk_v='Vungle/6.10.0')
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
#             assert_that(debug['hb_message'], not equal_to(None))
#             assert_that(debug['hb_message']['is_bill'], equal_to(True))
#             assert_that(debug['hb_message']['notification_type'], equal_to(102))
