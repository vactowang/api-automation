import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema
import base64


@allure.epic('HBP basic')
class TestHBPBasic(object):

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

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-1461 HBP supply side testing')
    @allure.description('Verify the HBP max response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_max_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'lurl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-1461 HBP supply side testing')
    @allure.description('Verify the HBP max response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_max_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description('Verify the HBP Max response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_max_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'lurl')
            assert_keys_exist(bid_info, 'burl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description('Verify the HBP Max response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_max_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-1936 HBP Adtiming support')
    @allure.description('Verify the HBP adtiming response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_adtiming_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_adtiming(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_adtiming_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_adtiming)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'lurl')
            assert_keys_not_exist(bid_info, 'burl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-1936 HBP Adtiming support')
    @allure.description('Verify the HBP adtiming response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_adtiming_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_adtiming(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_adtiming_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_adtiming)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2013 New endpoint for Ironsource')
    @allure.description('Verify the HBP ironsource response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_ironsource_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_ironsource(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_ironsource_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_ironsource)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'lurl')
            assert_keys_not_exist(bid_info, 'burl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2013 New endpoint for Ironsource')
    @allure.description('Verify the HBP ironsource response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_ironsource_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_ironsource(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_ironsource_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_ironsource)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('normal', 'R_v0.31.0')
    @allure.story('PBJ-2140 New Bidding Endpoint for Ohayoo')
    @allure.description('Verify the HBP Ohayoo response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_ohayoo_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_ohayoo(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_ohayoo_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_ohayoo)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'lurl')
            assert_keys_not_exist(bid_info, 'burl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('normal', 'R_v0.31.0')
    @allure.story('PBJ-2140 New Bidding Endpoint for Ohayoo')
    @allure.description('Verify the HBP Ohayoo response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_ohayoo_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_ohayoo(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_ohayoo_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_ohayoo)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('normal', 'R_v0.33.0')
    @allure.story('PBJ-2177 new endpoint for saygames')
    @allure.description('Verify the HBP Saygames response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_saygames_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_saygames(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_saygames)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'lurl')
            assert_keys_not_exist(bid_info, 'burl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('normal', 'R_v0.33.0')
    @allure.story('PBJ-2177 new endpoint for saygames')
    @allure.description('Verify the HBP Saygames response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_saygames_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_saygames(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_saygames)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('normal', 'R_v0.40.0')
    @allure.story('PBJ-2332 new endpoint for aequus')
    @allure.description('Verify the HBP Aequus response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hbp_aequus_response_details(self, pub_app_id, placement):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_aequus(pub_app_id, placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_aequus_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_aequus)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'lurl')
            assert_keys_not_exist(bid_info, 'burl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('normal', 'R_v0.40.0')
    @allure.story('PBJ-2332 new endpoint for aequus')
    @allure.description('Verify the HBP Aequus response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hbp_aequus_response_event_id(self, pub_app_id, placement):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_aequus(pub_app_id, placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_aequus_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_aequus)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('smoke', 'v0.41.0')
    @allure.story('PBJ-2013 New endpoint for CharBoost')
    @allure.description('Verify the HBP CharBoost response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_charboost_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_charboost(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_charboost_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_charboost)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'lurl')
            assert_keys_not_exist(bid_info, 'burl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('smoke', 'v0.41.0')
    @allure.story('PBJ-2013 New endpoint for CharBoost')
    @allure.description('Verify the HBP CharBoost response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_charboost_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_charboost(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_charboost_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_charboost)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2708 New endpoint for Unity')
    @allure.description('Verify the HBP Unity response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_unity_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_unity(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_unity_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_unity)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'lurl')
            assert_keys_not_exist(bid_info, 'burl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2708 New endpoint for Unity')
    @allure.description('Verify the HBP Unity response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_unity_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_unity(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_unity_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_unity)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2784 HBP new endpoint for Fyber & TopOn')
    @allure.description('Verify the HBP Fyber response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_fyber_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_fyber_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_fyber)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'lurl')
            assert_keys_not_exist(bid_info, 'burl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2784 HBP new endpoint for Fyber & TopOn')
    @allure.description('Verify the HBP Fyber response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_fyber_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_fyber_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_fyber)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2784 HBP new endpoint for Fyber & TopOn')
    @allure.description('Verify the HBP TopOn response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_topon_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_topon(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_topon_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_topon)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'nurl')
            assert_keys_exist(bid_info, 'burl')
            assert_keys_exist(bid_info, 'lurl')
            assert_that(bid_info['adm'], equal_to('ADVANCED_BIDDER'))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-2784 HBP new endpoint for Fyber & TopOn')
    @allure.description('Verify the HBP TopOn response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_topon_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_topon(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_topon_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_topon)
            assert_that(bid_info['id'], not equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('smoke', 'v0.47.0')
    @allure.story('PBJ-2790 Migrate partners to HTTPS support only')
    @allure.description('Verify that the all URLs use https not http which ignore the mongo setting')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_url_use_https(self, pub_app_id, placement, partner):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(get_hbp_partner_endpoint(partner), json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.get_hbp_partner_schema(partner))
            if partner != 'admob':
                assert_that(bid_info['nurl'].count('https://'), equal_to(1))
                assert_that(bid_info['lurl'].count('https://'), equal_to(1))
            if partner == 'max' or partner == 'admob':
                assert_that(bid_info['burl'].count('https://'), equal_to(1))

    @allure.feature('basic')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the HBP Admob response details')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_admob_response_details(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_keys_exist(response_payload, 'id')
            assert_keys_exist(response_payload, 'seatbid')
            assert_keys_exist(response_payload['seatbid'][0], 'bid')
            assert_keys_exist(response_payload['seatbid'][0], 'seat')
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_keys_exist(bid_info, 'id')
            assert_keys_exist(bid_info, 'impid')
            assert_keys_exist(bid_info, 'price')
            assert_keys_exist(bid_info, 'burl')
            assert_keys_exist(bid_info, 'ext')
            assert_keys_exist(bid_info['ext']['sdk_rendered_ad'], "id")
            assert_keys_exist(bid_info['ext']['sdk_rendered_ad'], "rendering_data")
            assert_keys_exist(bid_info['ext']['event_notification_token'], 'payload')

    @allure.feature('basic')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the HBP Admob response event id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_admob_response_event_id(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_that(bid_info['id'], not equal_to(event_id))