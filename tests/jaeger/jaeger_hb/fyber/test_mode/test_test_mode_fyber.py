import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('HBP Fyber')
class TestTestModeFyber(object):

    @allure.feature('test mode')
    @allure.tag('normal')
    @allure.story('PBJ-2039 HBP test mode refactor',
                  'PBJ-2190 Generic testing endpoint for Vungle app bidding')
    @allure.description('Verify the Fyber test mode with the token not in redis for v1 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_fyber_endpoint_qa, hbp_test_endpoint_qa])
    def test_fyber_test_mode_1(self, pub_app_id, endpoint):
        test_ifa = gen_device_id()
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa,
                                           bid_token=s2s_test_mode_token, is_test=1)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_fyber)
            assert_that(bid_info['price'], equal_to(99))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('normal')
    @allure.story('PBJ-2039 HBP test mode refactor',
                  'PBJ-2190 Generic testing endpoint for Vungle app bidding')
    @allure.description('Verify the Fyber non test mode with the token not in redis for v1 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_fyber_endpoint_qa, hbp_test_endpoint_qa])
    def test_fyber_test_mode_2(self, pub_app_id, endpoint):
        test_ifa = gen_device_id()
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa,
                                           bid_token=s2s_test_mode_token, is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('test mode')
    @allure.tag('normal')
    @allure.story('PBJ-2039 HBP test mode refactor',
                  'PBJ-2190 Generic testing endpoint for Vungle app bidding')
    @allure.description('Verify the Fyber test mode with the token not in redis for v2 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_fyber_endpoint_qa, hbp_test_endpoint_qa])
    def test_fyber_test_mode_3(self, pub_app_id, endpoint):
        test_ifa = gen_device_id()
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa,
                                           bid_token=s2s_test_mode_token, is_test=1)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_fyber)
            assert_that(bid_info['price'], equal_to(99))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('normal')
    @allure.story('PBJ-2039 HBP test mode refactor'
                  'PBJ-2190 Generic testing endpoint for Vungle app bidding')
    @allure.description('Verify the Fyber non test mode with the token not in redis for v2 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_fyber_endpoint_qa, hbp_test_endpoint_qa])
    def test_fyber_test_mode_4(self, pub_app_id, endpoint):
        test_ifa = gen_device_id()
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa,
                                           bid_token=s2s_test_mode_token, is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('test mode')
    @allure.tag('normal')
    @allure.story('PBJ-2139 Enhance HBP S2S Testing mode & Publisher Test Mode',
                  'PBJ-2190 Generic testing endpoint for Vungle app bidding')
    @allure.description('Verify the case of vungle in test mode and test flag is 1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_fyber_endpoint_qa, hbp_test_endpoint_qa])
    def test_fyber_test_mode_enhance_1(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=test_mode_device_id, rtb=test_mode_kraken_rtb_ids)
        ordinal_view_count = 11
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                           is_test=1)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_fyber)
            assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('normal')
    @allure.story('PBJ-2139 Enhance HBP S2S Testing mode & Publisher Test Mode',
                  'PBJ-2190 Generic testing endpoint for Vungle app bidding')
    @allure.description('Verify the case of vungle in test mode and test flag is 0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_fyber_endpoint_qa])
    def test_fyber_test_mode_enhance_2(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=test_mode_device_id, rtb=test_mode_kraken_rtb_ids)
        ordinal_view_count = 11
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                           is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)

    @allure.feature('test mode')
    @allure.tag('normal')
    @allure.story('PBJ-2139 Enhance HBP S2S Testing mode & Publisher Test Mode',
                  'PBJ-2190 Generic testing endpoint for Vungle app bidding')
    @allure.description('Verify the case of vungle not in test mode and test flag is 1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_fyber_endpoint_qa, hbp_test_endpoint_qa])
    def test_fyber_test_mode_enhance_3(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        ordinal_view_count = 11
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                           is_test=1)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_fyber)
            assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('normal')
    @allure.story('PBJ-2139 Enhance HBP S2S Testing mode & Publisher Test Mode',
                  'PBJ-2190 Generic testing endpoint for Vungle app bidding')
    @allure.description('Verify the case of vungle not in test mode and test flag is 0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_fyber_endpoint_qa, hbp_test_endpoint_qa])
    def test_fyber_test_mode_enhance_4(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        ordinal_view_count = 11
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                           is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            if endpoint == hbp_test_endpoint_qa:
                assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)
            else:
                response_payload = r.json()
                bid_info = response_payload['seatbid'][0]['bid'][0]

                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.hbp_fyber)
                assert_that(bid_info['price'], not equal_to(50.001))
                assert_keys_not_exist(response_payload, 'ext')

    @allure.feature('test mode')
    @allure.tag('normal')
    @allure.story('PBJ-2158 Adding test flag of HBP in test mode',
                  'PBJ-2190 Generic testing endpoint for Vungle app bidding')
    @allure.description('Verify the test flag is 1 when HBP request in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_fyber_endpoint_qa, hbp_test_endpoint_qa])
    def test_fyber_test_mode_flag_1(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=test_mode_device_id, rtb=test_mode_kraken_rtb_ids)
        ordinal_view_count = 11
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                           bid_token=super_token, is_test=1)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_fyber)
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('normal')
    @allure.story('PBJ-2158 Adding test flag of HBP in test mode',
                  'PBJ-2190 Generic testing endpoint for Vungle app bidding')
    @allure.description('Verify the test flag is 0 when HBP request in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_fyber_endpoint_qa, hbp_test_endpoint_qa])
    def test_fyber_test_mode_flag_2(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        ordinal_view_count = 11
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_fyber(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                           is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            if endpoint == hbp_test_endpoint_qa:
                assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)
            else:
                response_payload = r.json()

                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.hbp_fyber)
                assert_keys_not_exist(response_payload, 'ext')
