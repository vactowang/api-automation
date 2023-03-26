import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('Scrat Notifications')
class TestScratLossNotification(object):

    @pytest.fixture(scope="class", autouse=True)
    def get_jaeger_response_bid_token(self):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id(), sdk_v='Vungle/6.11.0')
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
    @allure.description('Verify the LURL normal response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_lurl_normal_response(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']

            r_url = get(lurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_LOSS}', '1')
                        .replace('${AUCTION_MBR}', '5.6'))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the LURL error response, empty loss reason value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_lurl_response_empty_value_1(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']

            r_url = get(lurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_LOSS}', '')
                        .replace('${AUCTION_MBR}', '5.6'))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the LURL error response, empty auction mbr value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_lurl_response_empty_value_2(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']

            r_url = get(lurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_LOSS}', '1')
                        .replace('${AUCTION_MBR}', ''))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the LURL error response, invalid loss reason value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('param', ['${AUCTION_LOSS}', 'abcdefg123', ' '])
    def test_scrat_lurl_error_response_1(self, pub_app_id, param):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']

            r_url = get(lurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_LOSS}', param)
                        .replace('${AUCTION_MBR}', '5.6'))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            msg = 'Request invalid: convert loss_reason error with \'%s\'.' % param
            assert_that(response_payload_url['msg'], equal_to(msg))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the LURL error response, invalid auction mbr value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('param', ['${AUCTION_MBR}', 'abcdefg123', ' '])
    def test_scrat_lurl_error_response_2(self, pub_app_id, param):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']

            r_url = get(lurl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_LOSS}', '1')
                        .replace('${AUCTION_MBR}', param))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            msg = 'Request invalid: convert auction_mbr error with \'%s\'.' % param
            assert_that(response_payload_url['msg'], equal_to(msg))
            assert_that(response_payload_url['code'], equal_to(200))



