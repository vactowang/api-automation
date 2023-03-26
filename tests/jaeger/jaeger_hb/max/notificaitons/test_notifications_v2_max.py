import pytest
import allure
import base64

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('HBP Max')
class TestNotificationsV2Max(object):

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

    @allure.feature('max support')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description('Verify that the NURL contains action mbr for Max')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_nurl_details_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['nurl'].count('settlement_price'), equal_to(1))
            assert_that(bid_info['nurl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['nurl'])
            assert_that(ext['name'], equal_to('max'))
            assert_that(ext['id'], equal_to(event_id))
            assert_that(isinstance(ext['price'], float) or isinstance(ext['price'], int))
            assert_that(isinstance(ext['bid'], str))
            assert_that(isinstance(ext['internal'], bool))

    @allure.feature('max support')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description('Verify that the LURL contains action mbr for Max')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_lurl_details_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['lurl'].count('loss_reason=${AUCTION_LOSS}'), equal_to(1))
            assert_that(bid_info['lurl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['lurl'])
            assert_that(ext['name'], equal_to('max'))
            assert_that(ext['id'], equal_to(event_id))
            assert_that(isinstance(ext['price'], float) or isinstance(ext['price'], int))
            assert_that(isinstance(ext['bid'], str))
            assert_that(isinstance(ext['internal'], bool))

    @allure.feature('max support')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support'
                  'PBJ-3632 Add placement_ref_id & pub_app_id to bill notification ext')
    @allure.description('Verify that the BURL contains action mbr for Max'
                        'Verify the placement_ref_id & pub_app_id were added in ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_burl_details_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['burl'].count('settlement_price'), equal_to(1))
            assert_that(bid_info['burl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['burl'])
            assert_that(ext['appid'], equal_to(pub_app_id))
            assert_that(ext['prid'], equal_to(common_test_placement))
            assert_that(ext['name'], equal_to('max'))
            assert_that(ext['id'], equal_to(event_id))
            assert_that(isinstance(ext['price'], float) or isinstance(ext['price'], int))
            assert_that(isinstance(ext['bid'], str))
            assert_that(isinstance(ext['internal'], bool))

    @allure.feature('max support')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description('Verify that the LURL contains settlement price for Max')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_lurl_contains_settlement_price_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            # Only for the default lurl config
            # assert_that(bid_info['lurl'].count('settlement_price'), equal_to(1))

    @allure.feature('max support')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description(
        'Verify that the Max NURL contains ordinal view count, the value is half of the original ordinal view count')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_nurl_ordinal_view_count_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['nurl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['nurl'])
            assert_that(ext['ordinal'], ordinal_view_count)

    @allure.feature('max support')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description('Verify that the Max LURL does not contains action mbr')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_auction_mbr_not_in_lurl_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            # Only for the default lurl config
            # assert_that(bid_info['lurl'].count('auction_mbr=${AUCTION_MBR}'), equal_to(0))

    @allure.feature('max support')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description('Verify that the Max LURL does not contain network clearing price')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_network_clearing_price_not_in_lurl_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['lurl'].count('network_clearing_price=${NETWORK_CLEARING_PRICE}'), equal_to(0))

    @allure.feature('max support')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description('Verify that the Max LURL contains ordinal view count')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ordinal_view_ount_in_lurl_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['lurl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['lurl'])
            assert_that(ext['ordinal'], ordinal_view_count)

    @allure.feature('max support')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description('Verify that the Max BURL contains ordinal view count')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ordinal_view_ount_in_burl_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['burl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['burl'])
            assert_that(ext['ordinal'], ordinal_view_count)

    @allure.feature('max support')
    @allure.tag('smoke')
    @allure.story('PBJ-1904 HBP Max support')
    @allure.description('Verify that the Max NURL does not contain isBill')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_is_bill_not_in_nurl_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['nurl'].count('isBill'), equal_to(0))

    @allure.feature('max support')
    @allure.tag('smoke', 'v0.47.0')
    @allure.story('PBJ-2790 Migrate partners to HTTPS support only')
    @allure.description('Verify that the Max URLs use https not http')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_url_use_https_max(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_max)
            assert_that(bid_info['nurl'].count('https://'), equal_to(1))
            assert_that(bid_info['burl'].count('https://'), equal_to(1))
            assert_that(bid_info['lurl'].count('https://'), equal_to(1))

    @allure.feature('max support')
    @allure.tag('normal', 'v0.45.0')
    @allure.story('PBJ-2743 https notifications from MAX')
    @allure.description('Verify the Max URLs use https for specific pub apps')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5f5005df9329d700012c7d4c'])
    @pytest.mark.parametrize('placement', ['DEFAULT02021M1'])
    def test_url_use_https_1(self, pub_app_id, placement):
        info = request_hbp('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id())
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_valid_schema(response_payload, response_schema.hbp_max)
            assert_that(bid_info['nurl'].count('https://'), equal_to(1))
            assert_that(bid_info['burl'].count('https://'), equal_to(1))
            assert_that(bid_info['lurl'].count('https://'), equal_to(1))

    @allure.feature('max support')
    @allure.tag('normal', 'v0.45.0')
    @allure.story('PBJ-2743 https notifications from MAX')
    @allure.description('Verify the Max URLs use https for specific pub apps')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5f63bfa4df31560001c63fe2'])
    @pytest.mark.parametrize('placement', ['DEFAULT02021M2'])
    def test_url_use_https_2(self, pub_app_id, placement):
        info = request_hbp('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id())
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_valid_schema(response_payload, response_schema.hbp_max)
            assert_that(bid_info['nurl'].count('https://'), equal_to(1))
            assert_that(bid_info['burl'].count('https://'), equal_to(1))
            assert_that(bid_info['lurl'].count('https://'), equal_to(1))


    @allure.feature('max 2nd highest price')
    @allure.tag('normal')
    @allure.story('PBJ-4300 Look into if MAX & IS pass min_bid_to_win for the 2nd highest price on IAB auction')
    @allure.description('Verify hb-notification record the 2nd highest price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5f63bfa4df31560001c63fe2'])
    @pytest.mark.parametrize('placement', ['DEFAULT02021M2'])
    def test_2nd_price_01(self, pub_app_id, placement):
        info = request_hbp('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id())
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']
            # add second_highest_price={AUCTION_MIN_BID_TO_WIN} in notification url, this is only for MAX
            nurl = nurl+"&second_highest_price=${AUCTION_MIN_BID_TO_WIN}"
            r_url = get(nurl.replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MIN_BID_TO_WIN}', '5.3').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            # Verify thet second_highest_bid_price=5.3 in hb-notifications
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('max 2nd highest price')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4300 Look into if MAX & IS pass min_bid_to_win for the 2nd highest price on IAB auction')
    @allure.description('Verify hb-notification record the 2nd highest price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5f63bfa4df31560001c63fe2'])
    @pytest.mark.parametrize('placement', ['DEFAULT02021M2'])
    def test_2nd_price_test_mode(self, pub_app_id, placement):
        info = request_hbp('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=test_mode_device_id,
                           rtb=ext_test_mode_kraken_rtb_ids_mraid)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']
            # add second_highest_price={AUCTION_MIN_BID_TO_WIN} in notification url, this is only for MAX
            nurl = nurl + "&second_highest_price=${AUCTION_MIN_BID_TO_WIN}"
            r_url = get(nurl.replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MIN_BID_TO_WIN}', '5.3').replace(
                hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            # Verify thet second_highest_bid_price=5.3 in hb-notifications
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))