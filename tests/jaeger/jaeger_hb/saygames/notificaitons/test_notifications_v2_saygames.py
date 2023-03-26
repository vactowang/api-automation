import pytest
import allure
import base64

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('HBP Saygames')
class TestNotificationsV2Saygames(object):

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

    @allure.feature('saygames support')
    @allure.tag('smoke', 'R_v0.33.0')
    @allure.story('PBJ-2177 new endpoint for saygames')
    @allure.description('Verify that the NURL contains action mbr for Saygames')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_nurl_details_saygames(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_saygames(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_saygames)
            assert_that(bid_info['nurl'].count('settlement_price'), equal_to(1))
            assert_that(bid_info['nurl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['nurl'])
            assert_that(ext['name'], equal_to('saygames'))
            assert_that(ext['id'], equal_to(event_id))
            assert_that(isinstance(ext['price'], float) or isinstance(ext['price'], int))
            assert_that(isinstance(ext['bid'], str))
            assert_that(isinstance(ext['internal'], bool))

    @allure.feature('saygames support')
    @allure.tag('smoke', 'R_v0.33.0')
    @allure.story('PBJ-2177 new endpoint for saygames')
    @allure.description('Verify that the LURL contains action mbr for Saygames')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_lurl_details_saygames(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_saygames(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_saygames)
            assert_that(bid_info['lurl'].count('loss_reason=${AUCTION_LOSS}'), equal_to(1))
            assert_that(bid_info['lurl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['lurl'])
            assert_that(ext['name'], equal_to('saygames'))
            assert_that(ext['id'], equal_to(event_id))
            assert_that(isinstance(ext['price'], float) or isinstance(ext['price'], int))
            assert_that(isinstance(ext['bid'], str))
            assert_that(isinstance(ext['internal'], bool))

    @allure.feature('saygames support')
    @allure.tag('smoke', 'R_v0.33.0')
    @allure.story('PBJ-2177 new endpoint for saygames')
    @allure.description('Verify that the LURL contains settlement price for Saygames')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_lurl_contains_settlement_price_saygames(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_saygames(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_saygames)
            assert_that(bid_info['lurl'].count('settlement_price'), equal_to(1))

    @allure.feature('saygames support')
    @allure.tag('smoke', 'R_v0.33.0')
    @allure.story('PBJ-2177 new endpoint for saygames')
    @allure.description(
        'Verify that the Saygames NURL contains ordinal view count, the value is half of the original ordinal view count')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_nurl_ordinal_view_count_saygames(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_saygames(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_saygames)
            assert_that(bid_info['nurl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['nurl'])
            assert_that(ext['ordinal'], ordinal_view_count)

    @allure.feature('saygames support')
    @allure.tag('smoke', 'R_v0.33.0')
    @allure.story('PBJ-2177 new endpoint for saygames')
    @allure.description('Verify that the Saygames LURL does not contains action mbr')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_auction_mbr_not_in_lurl_saygames(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_saygames(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_saygames)
            assert_that(bid_info['lurl'].count('auction_mbr=${AUCTION_MBR}'), equal_to(0))

    @allure.feature('saygames support')
    @allure.tag('smoke', 'R_v0.33.0')
    @allure.story('PBJ-2177 new endpoint for saygames')
    @allure.description('Verify that the Saygames LURL does not contain network clearing price')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_network_clearing_price_not_in_lurl_saygames(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_saygames(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_saygames)
            assert_that(bid_info['lurl'].count('network_clearing_price=${NETWORK_CLEARING_PRICE}'), equal_to(0))

    @allure.feature('saygames support')
    @allure.tag('smoke', 'R_v0.33.0')
    @allure.story('PBJ-2177 new endpoint for saygames')
    @allure.description('Verify that the Saygames LURL contains ordinal view count')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ordinal_view_ount_in_lurl_saygames(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_saygames(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_saygames)
            assert_that(bid_info['lurl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['lurl'])
            assert_that(ext['ordinal'], ordinal_view_count)

    @allure.feature('saygames support')
    @allure.tag('smoke', 'R_v0.33.0')
    @allure.story('PBJ-2177 new endpoint for saygames')
    @allure.description('Verify that the Saygames NURL does not contain isBill')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_is_bill_not_in_nurl_saygames(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_saygames(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_saygames)
            assert_that(bid_info['nurl'].count('isBill'), equal_to(0))

