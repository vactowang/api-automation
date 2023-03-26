import pytest
import allure
from http import HTTPStatus
from data import request_payload
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp_with_real_time_token
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('HBP Admob')
class TestTestModeAdmob(object):

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob'
                  'PBJ-3761 Temp change admob test mode bidprice to 4999')
    @allure.description('Verify the Admob test mode with the token not in redis for v1 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_1(self, pub_app_id, endpoint):
        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=s2s_test_mode_token, 
                                        is_test=1)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_that(bid_info['price'], equal_to(99))
            assert_that(response_payload['ext']['test'], equal_to(1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the Admob non test mode with the token not in redis for v1 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_2(self, pub_app_id, endpoint):
        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=s2s_test_mode_token,
                                        is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob'
                  'PBJ-3761 Temp change admob test mode bidprice to 4999')
    @allure.description('Verify the Admob test mode with the token not in redis for v2 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_3(self, pub_app_id, endpoint):
        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=s2s_test_mode_token,
                                        is_test=1)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        response_payload = r.json()
        bid_info = response_payload['seatbid'][0]['bid'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.hbp_admob)
        assert_that(bid_info['price'], equal_to(99))
        assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the Admob non test mode with the token not in redis for v2 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_4(self, pub_app_id, endpoint):
        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=s2s_test_mode_token,
                                        is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the case of vungle in test mode and test flag is 1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_enhance_1(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=test_mode_device_id, rtb=test_mode_kraken_rtb_ids)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                        is_test=1)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_that(bid_info['price'], equal_to(4999))
            assert_that(response_payload['ext']['test'], equal_to(1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the case of vungle in test mode and test flag is 0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_enhance_2(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=test_mode_device_id, rtb=test_mode_kraken_rtb_ids)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                        is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the case of vungle not in test mode and test flag is 1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_enhance_3(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                        is_test=1)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_that(bid_info['price'], equal_to(4999))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the case of vungle not in test mode and test flag is 0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_enhance_4(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                        is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            if endpoint == hbp_test_endpoint_qa:
                assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)
            else:
                response_payload = r.json()
                bid_info = response_payload['seatbid'][0]['bid'][0]

                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.hbp_admob)
                assert_that(bid_info['price'], not equal_to(50.001))
                assert_keys_not_exist(response_payload, 'ext')
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('Admob response')
    @allure.tag('normal')
    @allure.story('PBJ-3154 Update AdMob Open Bidding Bid Response')
    @allure.description('Verify response fields for v2 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.1'])
    def test_admob_response_fields_v2(self, pub_app_id, endpoint, sdk_v, placement):
        jaeger_response = request_ads_ios(pub_app_id=pub_app_id, placement_ref_id=placement, test_ifa=gen_device_id(),
                                          banner=True, ip=au_ip, retry_mode='meister')
        if 'sleep' not in jaeger_response['ads'][0]['ad_markup']:
            ordinal_view_count = 7
            bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
            bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
            super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

            banner_format = [{"w": 300, "h": 50}]
            test_ifa = gen_device_id()
            req = request_payload.hbp_admob(pub_app_id, placement, ifa=test_ifa, bid_token=super_token, is_test=0,
                                            banner_format=banner_format)
            r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v))
            request_billing_id = req['imp'][0]['ext']['billing_id']
            request_format = req['imp'][0]['banner']['format'][0]
            request_height = request_format['h']
            request_width = request_format['w']

            if r.status_code == HTTPStatus.OK:
                if endpoint == hbp_test_endpoint_qa:
                    assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)
                else:
                    response_payload = r.json()
                    bid_info = response_payload['seatbid'][0]['bid'][0]
                    cid = bid_info['cid']
                    crid = bid_info['crid']
                    response_height = bid_info['h']
                    response_width = bid_info['w']
                    assert_response_status_code(r.status_code, HTTPStatus.OK)
                    billing_id = response_payload['seatbid'][0]['bid'][0]['ext']['billing_id']
                    assert_that(billing_id, is_in(request_billing_id))
                    assert_that(cid, billing_id)
                    assert_valid_schema(response_payload, response_schema.hbp_admob)
                    assert_keys_exist(response_payload, 'cur')
                    assert_keys_exist(response_payload['cur'], 'USD')
                    assert_that(crid, is_not(None))
                    assert_that(request_height, equal_to(response_height))
                    assert_that(request_width, equal_to(response_width))

    @allure.feature('Admob response')
    @allure.tag('smoke')
    @allure.story('PBJ-3154 Update AdMob Open Bidding Bid Response')
    @allure.description('Verify the responded fields for V3 token')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement,
                                           common_test_pre_cache_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_admob_response_field_v3(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            cid = bid_info['cid']
            crid = bid_info['crid']
            billing_id = response_payload['seatbid'][0]['bid'][0]['ext']['billing_id']
            assert_that(cid, equal_to(billing_id))
            assert_valid_schema(response_payload, response_schema.hbp_admob)
            assert_keys_exist(response_payload, 'cur')
            assert_keys_exist(response_payload['cur'], 'USD')
            assert_that(crid, is_not(None))

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the test flag is 1 when HBP request in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_flag_1(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=test_mode_device_id, rtb=test_mode_kraken_rtb_ids)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                        bid_token=super_token, is_test=1)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.hbp_admob)
            assert_that(response_payload['ext']['test'], equal_to(1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.51.0')
    @allure.story('PBJ-2895 bidresponse for google/AdMob')
    @allure.description('Verify the test flag is 0 when HBP request in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_flag_2(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                        is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            if endpoint == hbp_test_endpoint_qa:
                assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)
            else:
                response_payload = r.json()

                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.hbp_admob)
                assert_keys_not_exist(response_payload, 'ext')
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.53.0')
    @allure.story('PBJ-3028 Update admob bidresponse fields')
    @allure.description('Verify the field adm is changed to "sdk_rendered_ad"')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_field_updated(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                        is_test=0)

        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            sdk_rendered_ad = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
            assert_keys_exist(sdk_rendered_ad, 'id')

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.53.0')
    @allure.story('PBJ-3028 Update admob bidresponse fields')
    @allure.description('Verify returning billing_id in bid.ext')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_billing_id(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                        is_test=0)

        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        request_billing_id = req['imp'][0]['ext']['billing_id']
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()

            billing_id = response_payload['seatbid'][0]['bid'][0]['ext']['billing_id']
            assert_that(billing_id, is_in(request_billing_id))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('test mode')
    @allure.tag('normal', 'v0.53.0')
    @allure.story('PBJ-3028 Update admob bidresponse fields')
    @allure.description('Verify updating bid.id to request id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_test_mode_bid_id(self, pub_app_id, endpoint):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

        test_ifa = gen_device_id()
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token,
                                        is_test=0)

        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        request_id = req['id']
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            response_id = response_payload['id']
            response_bid_id = response_payload['seatbid'][0]['bid'][0]['id']
            assert_that(response_id, equal_to(request_id))
            assert_that(response_bid_id, equal_to(request_id))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')
