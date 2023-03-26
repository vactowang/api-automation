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


@allure.epic('HBP Admob')
class TestNotificationsV1Admob(object):

    @pytest.fixture(scope="class", autouse=True)
    def get_jaeger_response_bid_token(self):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        global bid_token
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token
        global super_token
        super_token = "1:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        global event_id
        event_id = jaeger_response['ads'][0]['ad_markup']['id']

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob'
                  'PBJ-3632 Add placement_ref_id & pub_app_id to bill notification ext')
    @allure.description('Verify that the default ordinal view count in burl for Admob'
                        'Verify the placement_ref_id & pub_app_id were added in ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_default_ordinal_view_ount_in_burl_admob(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_that(bid_info['burl'].count('ext='), equal_to(1))
            ext = decode_ext(url=bid_info['burl'])
            assert_that(ext['appid'], equal_to(pub_app_id))
            assert_that(ext['prid'], equal_to(common_test_placement))
            assert_that(ext['ordinal'], equal_to(-1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('admob support')
    @allure.tag('smoke', 'v0.53.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the event notification token for Admob')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_event_notification_token_admob_1(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_that(bid_info['ext']['event_notification_token']['payload'],
                        is_not(bid_info['burl'].split('ext=')[1]))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')
