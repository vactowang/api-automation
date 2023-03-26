import pytest
import allure

from http import HTTPStatus

from data import request_payload, response_schema
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('HBP Notifications')
class TestBillNotification(object):

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

    @allure.feature('hbp notifications')
    @allure.tag('smoke')
    @allure.story('bill notification')
    @allure.description('Verify the BURL normal response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_burl_normal_response(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']
            r_url = get(burl.replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', '5.6'))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal')
    @allure.story('bill notification')
    @allure.description('Verify the BURL error response, empty settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_burl_response_empty_settlement_price(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']

            r_url = get(burl.replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', ''))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'R_v0.34.0')
    @allure.story('PBJ-2192 HBP notification urls when no settlement price'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the BURL error response, invalid settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('param', ['${AUCTION_PRICE}', 'abcdefg123', ' '])
    def test_burl_error_response_1(self, pub_app_id, param):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']

            r_url = get(burl.replace('${AUCTION_PRICE}', param)
                        .replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            msg = 'Request invalid: convert settlement_price error with \'%s\'.' % param
            assert_that(response_payload_url['msg'], equal_to(msg))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2981 Decrypt settlement_price in burl for Admob'
                  'PBJ-3746 Adjust HBP admob encrypt key'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the BURL normal response for Admob')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('encrypted_price', hbp_admob_encrypted_price)
    def test_burl_normal_response_admob(self, pub_app_id, encrypted_price):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']
            r_url = get(burl.replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', encrypted_price))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'v0.84.0')
    @allure.story('PBJ-4114 Fix admob notification old style pubappId')
    @allure.description('Verify the BURL normal response for Admob with the old style pub app id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_placement_old])
    @pytest.mark.parametrize('encrypted_price', hbp_admob_encrypted_price)
    def test_burl_normal_response_admob_1(self, pub_app_id, encrypted_price, placement):
        info = request_hbp('admob', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id())

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']

            r_url = get(burl.replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host)
                        .replace('${AUCTION_PRICE}', encrypted_price))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))
            # check the pub app id from hb-notifications message, the value should be store id not obj id

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2981 Decrypt settlement_price in burl for Admob'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the BURL error response, empty settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_burl_response_empty_settlement_price_admob(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']
            r_url = get(burl.replace('${AUCTION_PRICE}', '').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2981 Decrypt settlement_price in burl for Admob'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the BURL error response, invalid settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('param', ['${AUCTION_PRICE}', 'abcdefg123', ' ', '2.7', 'YWJjMTIzZGVmNDU2Z2hpN7fhC'])
    def test_burl_error_response_admob(self, pub_app_id, param):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            burl = bid_info['burl']

            r_url = get(burl.replace('${AUCTION_PRICE}', param).replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            msg = 'Request invalid: convert settlement_price error with \'%s\'.' % param
            assert_that(response_payload_url['msg'], equal_to(msg))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('disable bid info recording')
    @allure.tag('normal', 'v0.52.0')
    @allure.story('PBJ-3026 Disable HBP record bidinfo cache after 6.10.1'
                  'PBJ-3964 Propagate `datasci_tags` into hbp-notifications topic')
    @allure.description('Verify that the bid info will not be recorded via SDK >= 6.10.1'
                        'Verify the bflat_datasci_tags were added in ext')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('partner', burl_hb_partners)
    def test_sdk_burl_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            burl = response_payload['seatbid'][0]['bid'][0]['burl']
            ext = decode_ext(url=burl)
            assert_that(ext['sdk_burl'], equal_to(True))
            # check 'bflat_datasci_tags'
            assert_keys_exist(ext, 'bflat_datasci_tags')
            bflat_datasci_tags =str_to_json(ext['bflat_datasci_tags'])
            assert_that(isinstance(bflat_datasci_tags['bp'], float))
            assert_that(isinstance(bflat_datasci_tags['b'], str))
            assert_that(isinstance(bflat_datasci_tags['e'], int))
            assert_that(bflat_datasci_tags['dsp_t'], 'edsp')
            assert_that(isinstance(bflat_datasci_tags['ad_t'], str))


    @allure.feature('disable bid info recording')
    @allure.tag('normal', 'v0.52.0')
    @allure.story('PBJ-3026 Disable HBP record bidinfo cache after 6.10.1')
    @allure.description('Verify that the bid info will be recorded via SDK < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('partner', burl_hb_partners)
    def test_sdk_burl_2(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))

            burl = response_payload['seatbid'][0]['bid'][0]['burl']
            ext = decode_ext(url=burl)
            assert_keys_not_exist(ext, 'sdk_burl')
