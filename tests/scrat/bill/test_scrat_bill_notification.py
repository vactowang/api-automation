import pytest
import allure

from http import HTTPStatus

from data import request_payload, response_schema
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('Scrat Notifications')
class TestScratBillNotification(object):

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
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP'
                  'PBJ-3964 Propagate `datasci_tags` into hbp-notifications topic')
    @allure.description('Verify the BURL normal response'
                        'Verify the bflat_datasci_tags were added in ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_burl_normal_response(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']

            r_url = get(burl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', '5.6'))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the BURL error response, empty settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_burl_response_empty_settlement_price(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']

            r_url = get(burl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', ''))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the BURL error response, invalid settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('param', ['${AUCTION_PRICE}', 'abcdefg123', ' '])
    def test_scrat_burl_error_response(self, pub_app_id, param):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']

            r_url = get(burl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', param))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            msg = 'Request invalid: convert settlement_price error with \'%s\'.' % param
            assert_that(response_payload_url['msg'], equal_to(msg))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the BURL normal response for Admob')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('encrypted_price', hbp_admob_encrypted_price)
    def test_scrat_burl_normal_response_admob(self, pub_app_id, encrypted_price):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']

            r_url = get(burl.replace(scrat_notification_host_ssl, scrat_notification_host)
                            .replace('${AUCTION_PRICE}', encrypted_price))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the BURL error response, empty settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_scrat_burl_response_empty_settlement_price_admob(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']

            r_url = get(burl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', ''))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the BURL error response, invalid settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('param', ['${AUCTION_PRICE}', 'abcdefg123', ' ', '2.7', 'YWJjMTIzZGVmNDU2Z2hpN7fhC'])
    def test_scrat_burl_error_response_admob(self, pub_app_id, param):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']

            r_url = get(burl.replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', param))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            msg = 'Request invalid: convert settlement_price error with \'%s\'.' % param
            assert_that(response_payload_url['msg'], equal_to(msg))
            assert_that(response_payload_url['code'], equal_to(200))