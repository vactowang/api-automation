import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
@allure.feature('basic')
class TestTokens(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('tokens')
    @allure.description('Verify ad token from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_token(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that('ad_token' in ad_markup)

    @allure.feature('header bidding')
    @allure.tag('smoke', 'R_1.137.0')
    @allure.story('PBJ-1961 Avoid header_bidding if SDK Version < 6.6.1 and pub is not appodeal')
    @allure.description('Verify bid token presents from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement_id', [common_test_placement_10])
    def test_bid_token_exist(self, pub_app_id, placement_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('bid_token' in ad_markup)

    @allure.feature('header bidding')
    @allure.tag('smoke', 'R_1.137.0')
    @allure.story('PBJ-1961 Avoid header_bidding if SDK Version < 6.6.1 and pub is not appodeal')
    @allure.description('Verify bid token not present from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_bid_token_not_exist(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('bid_token' not in ad_markup)

    @allure.feature('header bidding')
    @allure.tag('smoke', 'R_1.137.0', 'test_mode')
    @allure.story('PBJ-1961 Avoid header_bidding if SDK Version < 6.6.1 and pub is not appodeal')
    @allure.description('Verify the header bidding works via SDK >= 6.6.1')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.1', 'Vungle/6.6.2'])
    def test_bid_token_sdk_version_1(self, pub_app_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('bid_token' in ad_markup)

    @allure.feature('header bidding')
    @allure.tag('smoke', 'R_1.137.0')
    @allure.story('PBJ-1961 Avoid header_bidding if SDK Version < 6.6.1 and pub is not appodeal')
    @allure.description('Verify the header bidding does not work via SDK < 6.6.1')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.0'])
    def test_bid_token_sdk_version_2(self, pub_app_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('bid_token' not in ad_markup)

    @allure.feature('banner')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-1434 ad_token in the ads response should be unique for banners in test mode')
    @allure.description('Verify ad token should be unique for banner in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_token_unique_banner_test_mode(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(), banner=True)
        ad_token_1 = ''
        ad_token_2 = ''

        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            ad_token_1 = ad_markup['ad_token']

        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids_1))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            ad_token_2 = ad_markup['ad_token']

        if ad_token_1 != '' and ad_token_2 != '':
            assert_that(ad_token_1, not equal_to(ad_token_2))

    @allure.feature('header bidding')
    @allure.tag('normal', 'R_1.137.0')
    @allure.story('PBJ-1961 Avoid header_bidding if SDK Version < 6.6.1 and pub is not appodeal')
    @allure.description('Verify the header bidding works for appodeal pubs via both SDK < 6.6.1 and SDK >= 6.6.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub', [{'pub_app_id': '5a35a75845eaab51250070a5', 'placement_ref_id': 'DEFAULT52238'},
                                     {'pub_app_id': '5963678b3fc929fb1000090b', 'placement_ref_id': 'DEFAULT35140'}])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.1', 'Vungle/6.6.2'])
    def test_hb_appodeal_pubs_1(self, pub, sdk_v):
        req = request_payload.jaeger_v5_ios(pub['pub_app_id'], pub['placement_ref_id'], ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('bid_token' in ad_markup)

    # @allure.feature('header bidding')
    # @allure.tag('normal', 'R_1.139.0')
    # @allure.story('PBJ-1990 Add one more pub for appodeal hbp')
    # @allure.description('Verify the header bidding works for appodeal pubs via both SDK < 6.6.1 and SDK >= 6.6.1')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub', [{'pub_app_id': '5cfe1d24706918125238768f', 'placement_ref_id': 'DEFAULT-4587331'}])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.6.0', 'Vungle/6.6.1', 'Vungle/6.6.2'])
    # def test_hb_appodeal_pubs_2(self, pub, sdk_v):
    #     req = request_payload.jaeger_v5_ios(pub['pub_app_id'], pub['placement_ref_id'], ifa=gen_device_id(),
    #                                         header_bidding=True)
    #     r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
    #                                                                     rtb_selector=meister_rtb_ids))
    #
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_that('bid_token' in ad_markup)

    @allure.feature('bid tokens')
    @allure.tag('normal')
    @allure.story('PBJ-3345 deprecate bid token v1')
    @allure.description('Verify Jaeger should no long return bid token v1 when SDK < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.9.0'])
    def test_not_support_bid_token_v1(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(),
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('bid_token' in ad_markup)
        assert_that('1|' not in ad_markup['bid_token'])

    @allure.feature('bid tokens')
    @allure.tag('normal')
    @allure.story('PBJ-3345 deprecate bid token v1')
    @allure.description('Verify Jaeger should no long return bid token v1 when SDK < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.9.0'])
    def test_not_support_bid_token_v1_2(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('bid_token' in ad_markup)
        assert_that('1|' not in ad_markup['bid_token'])

    @allure.feature('bid tokens')
    @allure.tag('normal')
    @allure.story('PBJ-3345 deprecate bid token v1')
    @allure.description('Verify Jaeger should no long return bid token v1 when SDK < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.9.0'])
    def test_not_support_bid_token_v1_android(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(),
                                                header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('bid_token' in ad_markup)
        assert_that('1|' not in ad_markup['bid_token'])
