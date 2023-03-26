import pytest
import allure

from http import HTTPStatus

from data import request_payload, response_schema
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp, request_hbp_with_real_time_token, \
    get_bid_request_obj_from_jaeger_explain, get_bid_request_obj_from_hbp_explain
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('HBP external Notifications')
class TestExtWinNotification(object):

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario II: LO win on HBP Auction, LO will receive win notification:'
                        '')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_win_notification_on_hbp_auction_w_o_burl_03(self, pub_app_id, placement, sdk_v, partner):
        # mock l_nurl
        l_nurl = "http://kraken-lo1-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification_loss)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (bid_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '10').replace(hbp_ssl_host, hbp_host)
                       .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check rtb id is 6246e6b95890c35df3ee9822
            # verifiy krakn-lo1 will receive log:
            # Got notifications: Got notifications: /nurl?price=1.000000000&ex_price=10.000000000"}}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario III: LO win on HBP Auction, LO will receive win notification:'
                        '')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_win_notification_on_hbp_auction_w_burl_03(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo1-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification_loss)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (bid_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check rtb id is 6246e6b95890c35df3ee9822
            # verifiy krakn-lo1 will receive log:
            # Got notifications: Got notifications: /nurl?price=1.000000000&ex_price=10.000000000"}}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify admob external notification : win notification')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_win_notification_on_hbp_auction_for_admob_03(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo1-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % (l_nurl)
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, admob_status_code=1,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification_loss)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            event_id = response_payload['ext']['debug']['auction_result']['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl))
            request_payload = info['hbp_request']
            request_headers = info['hbp_request_headers']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                }
            }
            exmbtw = {
                "minimum_bid_to_win": 2
            }
            creative_status_code = {
                "creative_status_code": 1,
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)
            request_payload.get("ext").get("bid_feedback")[0].update(exmbtw)
            request_payload.get("ext").get("bid_feedback")[0].update(creative_status_code)

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # # check rtb id is 6246e6b95890c35df3ee9822
            # # verifiy krakn-lo1 will receive log:
            # {"level":"info","ts":"2022-05-16T10:49:49Z","msg":"Got notifications: /nurl?price=1.000000000&ex_price=2.000000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario II: LO win on HBP Auction, LO will receive win notification:'
                        '')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_win_notification_on_hbp_auction_w_o_burl_03(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo1-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification_loss)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (bid_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '10').replace(hbp_ssl_host, hbp_host)
                       .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check rtb id is 6246e6b95890c35df3ee9822
            # verifiy krakn-lo1 will receive log:
            # Got notifications: Got notifications: /nurl?price=1.000000000&ex_price=10.000000000"}}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4612 Look into LO side questions about win notification')
    @allure.description('Verify the auction id fix on win notification url for admob realtime mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_win_notification_fix_1(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}&auction_id=${AUCTION_ID}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % (l_nurl)
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, admob_status_code=1,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            event_id = response_payload['ext']['debug']['auction_result']['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl.replace('${AUCTION_ID}', event_id)))
            request_payload = info['hbp_request']
            request_headers = info['hbp_request_headers']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                }
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /nurl?price=98.000000000&ex_price=&auction_id=632ac1c6ffd35d35adb4e421"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4612 Look into LO side questions about win notification')
    @allure.description('Verify the auction id fix on win notification url for realtime mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_win_notification_fix_2(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}&auction_id=${AUCTION_ID}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (bid_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl.replace('${AUCTION_ID}', bid_id)))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '50').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /nurl?price=98.000000000&ex_price=&auction_id=632ac1c6ffd35d35adb4e421"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4612 Look into LO side questions about win notification')
    @allure.description('Verify the auction id fix on win notification url for precache mode with v3 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_multi_cache_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_win_notification_fix_3(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}&auction_id=${AUCTION_ID}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, ads_debug='jaeger',
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            ads_response_payload = info['ads_response']
            hbp_response_payload = info['hbp_response']
            bid_info = hbp_response_payload['seatbid'][0]['bid'][0]
            event_id = ads_response_payload['ads'][0]['ad_markup']['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl.replace('${AUCTION_ID}', event_id)))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /nurl?price=98.000000000&ex_price=&auction_id=632ac1c6ffd35d35adb4e421"}




    @allure.feature('support extension type')
    @allure.tag('normal')
    @allure.story('[SPO] Auction ID shows original one on duplicate Bid Requests'
                  'PBJ-4857 [SPO] Auction ID shows original one on duplicate Bid Requests')
    @allure.description('Verify that Auction ID should also be duplicated one')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['adtiming'])
    @pytest.mark.parametrize('rtb_id', [liftoff_rtbids_liftoff_dup, liftoff_rtbids_liftoff_specify_dup])
    def test_dup_auction_id_01(self, pub_app_id, placement, sdk_v, partner, rtb_id):
        # mock l_nurl
        l_nurl = "http://kraken-lo1-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}&event_id=${AUCTION_ID}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=rtb_id)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
            bid_request_id = bid_request['id']
            l_nurl = l_nurl.replace('${AUCTION_ID}',bid_request_id)
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (bid_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '10').replace(hbp_ssl_host, hbp_host)
                       .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)



    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4612 Look into LO side questions about win notification'
                  'PBJ-4857 [SPO] Auction ID shows original one on duplicate Bid Requests')
    @allure.description('Verify the auction id fix on win notification url for precache mode with v3 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_multi_cache_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('rtb_id', [liftoff_rtbids_liftoff_dup, liftoff_rtbids_liftoff_specify_dup])
    def test_dup_auction_id_02(self, pub_app_id, placement, sdk_v, partner, rtb_id):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}&auction_id=${AUCTION_ID}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, ads_debug='jaeger',
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=rtb_id)
        if info['is_hbp_responded_200']:
            ads_response_payload = info['ads_response']
            hbp_response_payload = info['hbp_response']
            bid_info = hbp_response_payload['seatbid'][0]['bid'][0]
            event_id = ads_response_payload['ads'][0]['ad_markup']['id']
            bid_request = get_bid_request_obj_from_jaeger_explain(ads_response_payload)
            bid_request_id = bid_request['id']
            l_nurl = l_nurl.replace('${AUCTION_ID}', bid_request_id)
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # / nurl?price = 1.000000000 & ex_price = 1.000000000 & auction_id = 6363a80cef11790106511b9b___5337

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for loss notification url for realtime traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_real_time_win_notification_ex_auction_01(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb='6246e6b95890c35df3ee9822,5fd965d7323580001628bf72')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (bid_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl.replace('${AUCTION_ID}', bid_id)))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '50').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '100')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /nurl?price=98.000000000&ex_auction_price=&ex_auction_price_v=98.000000000&partner=adtiming"}


    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for win notification url for realtime traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_win_notification_ex_auction_02(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb='6246e6b95890c35df3ee9822,5fd965d7323580001628bf72')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (bid_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl.replace('${AUCTION_ID}', bid_id)))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '50').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '100')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            #{"level":"info","msg":"Got notifications: /nurl?price=98.000000000&ex_auction_price=100.000000000&ex_auction_price_v=142.857142857&partner=max"}


    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description('Verify new macros are added for loss notification url for realtime traffic:admob')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_win_notification_ex_auction_03(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % (l_nurl)
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, admob_status_code=1,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            event_id = response_payload['ext']['debug']['auction_result']['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl.replace('${AUCTION_ID}', event_id)))
            request_payload = info['hbp_request']
            request_headers = info['hbp_request_headers']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                }
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /nurl?price=98.000000000&ex_auction_price=1.090000000&ex_auction_price_v=4.000000000&partner=admob"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for loss notification url for realtime traffic(with v2 token)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_win_notification_ex_auction_04(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"

        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, ads_debug='jaeger',
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            ads_response_payload = info['ads_response']
            ads_response_event_id = ads_response_payload['ads'][0]['ad_markup']['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (ads_response_event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl.replace('${AUCTION_ID}', ads_response_event_id)))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /lurl?mbtw=98.000000000&exbtw=1.090000000&exbtwv=98.000000000&auction_id=632ac1c6ffd35d35adb4e421"}



    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description('Verify new macros are added for loss notification url for realtime traffic(with v2 token):admob')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_win_notification_ex_auction_05(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % (l_nurl)
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, admob_status_code=1,ads_debug='jaeger',
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            ads_response_payload = info['ads_response']
            ads_response_event_id = ads_response_payload['ads'][0]['ad_markup']['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (ads_response_event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl.replace('${AUCTION_ID}', ads_response_event_id)))
            request_payload = info['hbp_request']
            request_headers = info['hbp_request_headers']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                }
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /nurl?price=98.000000000&ex_price=&auction_id=632ac1c6ffd35d35adb4e421"}
