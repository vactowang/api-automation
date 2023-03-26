import pytest
import allure
import base64

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp, decode_admob_event_token
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('HBP Admob')
class TestNotificationsV2Admob(object):

    @pytest.fixture(scope="class", autouse=True)
    def get_jaeger_response_bid_token(self):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id(), retry_mode='kraken')
        global ordinal_view_count
        ordinal_view_count = 20
        global bid_token
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        global super_token
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        global event_id
        event_id = jaeger_response['ads'][0]['ad_markup']['id']

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob'
                  'PBJ-3632 Add placement_ref_id & pub_app_id to bill notification ext'
                  'PBJ-3964 Propagate `datasci_tags` into hbp-notifications topic')
    @allure.description('Verify that the BURL contains action mbr for Admob'
                        'Verify the placement_ref_id & pub_app_id were added in ext'
                        'Verify the bflat_datasci_tags were added in ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_burl_details_admob(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5', debug='jaeger'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_that(bid_info['burl'].count('settlement_price'), equal_to(1))
            assert_that(bid_info['burl'].count('price_encrypted'), equal_to(1))
            assert_that(bid_info['burl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['burl'])
            assert_that(ext['appid'], equal_to(pub_app_id))
            assert_that(ext['prid'], equal_to(common_test_placement))
            assert_that(ext['name'], equal_to('admob'))
            assert_that(ext['id'], equal_to(event_id))
            assert_that(isinstance(ext['price'], float) or isinstance(ext['price'], int))
            assert_that(isinstance(ext['bid'], str))
            assert_that(isinstance(ext['internal'], bool))
            # check 'bflat_datasci_tags'
            assert_keys_exist(ext, 'bflat_datasci_tags')
            bflat_datasci_tags = str_to_json(ext['bflat_datasci_tags'])
            assert_that(isinstance(bflat_datasci_tags['bp'], float))
            assert_that(isinstance(bflat_datasci_tags['b'], str))
            assert_that(isinstance(bflat_datasci_tags['e'], int))
            # if Jaeger get bid token from external Kraken, the value should be 'edsp'
            # assert_that(bflat_datasci_tags['dsp_t'], equal_to('idsp'))
            assert_that(isinstance(bflat_datasci_tags['ad_t'], str))
            # if Jaeger get bid token from external Kraken, the the bidder is 'MarginExtenderBidder', so no 'k' field.
            # assert_that(isinstance(bflat_datasci_tags['k'], float))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.53.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob'
                  'PBJ-3632 Add placement_ref_id & pub_app_id to bill notification ext'
                  'PBJ-4019 Change HBP bidID from uuid to objectID')
    @allure.description('Verify the event notification token for Admob'
                        'Verify the placement_ref_id & pub_app_id were added in ext'
                        'Verify the ordinal <= 16')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_event_notification_token_admob_2(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_notification_token = bid_info['ext']['event_notification_token']['payload']
            decode_info = decode_admob_event_token(event_notification_token)
            ext = decode_ext(url=bid_info['burl'])
            assert_that(ext['appid'], equal_to(pub_app_id))
            assert_that(ext['prid'], equal_to(common_test_placement))
            assert_that(decode_info["adv_is_internal"], equal_to(ext['internal']))
            assert_that(decode_info["bidid"], equal_to(ext['bid']))
            assert_that(decode_info["event_id"], equal_to(ext['id']))
            assert_that(decode_info["pub_app_obj_id"], equal_to(ext['appid']))
            # the ordinal <= 16
            assert_that(decode_info["n_ordinal_view"], less_than_or_equal_to(16))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('admob support')
    @allure.tag('normal', 'v0.84.0')
    @allure.story('PBJ-4114 Fix admob notification old style pubappId')
    @allure.description('Verify the event notification token can be decoded correctly with the old style pub app id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_placement_old])
    def test_event_notification_token_admob_3(self, pub_app_id, placement):
        info = request_hbp('admob', 20, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id())

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_notification_token = bid_info['ext']['event_notification_token']['payload']
            decode_info = decode_admob_event_token(event_notification_token)
            ext = decode_ext(url=bid_info['burl'])
            assert_that(ext['appid'], equal_to(pub_app_id))
            assert_that(ext['prid'], equal_to(placement))
            assert_that(decode_info["adv_is_internal"], equal_to(ext['internal']))
            assert_that(decode_info["bidid"], equal_to(ext['bid']))
            assert_that(decode_info["event_id"], equal_to(ext['id']))
            assert_that(decode_info["pub_app_obj_id"], is_not(ext['appid']))
            # the ordinal <= 16
            assert_that(decode_info["n_ordinal_view"], less_than_or_equal_to(16))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify that the Admob BURL contains ordinal view count')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ordinal_view_ount_in_burl_admob(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_that(bid_info['burl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['burl'])
            assert_that(ext['ordinal'], ordinal_view_count)
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify that the Admob URLs use https not http')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_url_use_https_admob(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_that(bid_info['burl'].count('https://'), equal_to(1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the Admob URLs use https for specific pub apps')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5f5005df9329d700012c7d4c'])
    @pytest.mark.parametrize('placement', ['DEFAULT02021M1'])
    def test_url_use_https_1(self, pub_app_id, placement):
        info = request_hbp('admob', 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id())
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_valid_schema(response_payload, response_schema.hbp_admob)
            assert_that(bid_info['burl'].count('https://'), equal_to(1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the Admob URLs use https for specific pub apps')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5f63bfa4df31560001c63fe2'])
    @pytest.mark.parametrize('placement', ['DEFAULT02021M2'])
    def test_url_use_https_2(self, pub_app_id, placement):
        info = request_hbp('admob', 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id())
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_valid_schema(response_payload, response_schema.hbp_admob)
            assert_that(bid_info['burl'].count('https://'), equal_to(1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')


