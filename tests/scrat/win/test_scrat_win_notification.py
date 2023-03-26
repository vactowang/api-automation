import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp_with_real_time_token
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('Scrat Notifications')
class TestScratWinNotification(object):

    @pytest.fixture(scope="class", autouse=True)
    def get_jaeger_response_bid_token(self):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        global ordinal_view_count
        ordinal_view_count = 7
        global bid_token
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        global super_token
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        global event_id
        event_id = jaeger_response['ads'][0]['ad_markup']['id']

    @allure.feature('scrat notifications')
    @allure.tag('smoke', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the NURL normal response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_nurl_normal_response(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']
            r_url = get(nurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '5.6'))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the NURL error response, empty settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_nurl_response_empty_settlement_price(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']

            r_url = get(nurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '10'))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the NURL error response, invalid settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('param', ['${AUCTION_PRICE}', 'abcdefg123', ' '])
    def test_scrat_nurl_error_response(self, pub_app_id, param):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']

            r_url = get(nurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', param))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            msg = 'Request invalid: convert settlement_price error with \'%s\'.' % param
            assert_that(response_payload_url['msg'], equal_to(msg))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3528 Sync HBP changes to Scrat')
    @allure.description('Verify the win ttl is written for max for non_realtime')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_write_win_ttl_for_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']

            r_url = get(nurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '10'))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3528 Sync HBP changes to Scrat')
    @allure.description('Verify the win ttl is not written for max for realtime')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_not_write_win_ttl_for_max_real_time(self, pub_app_id):
        info = request_hbp_with_real_time_token('max', 11, pub_app_id=pub_app_id, placement_ref_id=common_test_hybrid_placement,
                                                test_device_id=gen_device_id(), sdk_v='Vungle/6.10.0', coppa=False)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']
            r_url = get(nurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace(hbp_ssl_host, hbp_host)
                        .replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '10'))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal')
    @allure.story('PBJ-3528 Sync HBP changes to Scrat')
    @allure.description('Verify the win ttl is not written for max for realtime')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_not_write_win_ttl_for_max_real_time_02(self, pub_app_id):
        info = request_hbp_with_real_time_token('max', 11, pub_app_id=pub_app_id, placement_ref_id=common_test_hybrid_placement,
                                                test_device_id=gen_device_id(), sdk_v='Vungle/6.11.1', coppa=False)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']
            r_url = get(nurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace(hbp_ssl_host, hbp_host)
                        .replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '10'))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))