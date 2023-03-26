import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestAdbuilderBoxerRequestNormal(object):

    @allure.feature('ios 15 support')
    @allure.tag('smoke', 'v1.199.0', 'test_mode')
    @allure.story('PBJ-3860 [iOS15 + SDK6.10.1] AC MultiPage Reward: Missing Incentivized popup once closing the '
                  'playing video')
    @allure.description('Verify the INCENTIVIZED filed for rewarded placement via the iOS 15 request '
                        'when SDK <= 6.10.2 iDSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['15'])
    def test_incentivized_field_1(self, pub_app_id, placement, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        normal = response_payload['ext']['debug']['auction_result']['adbuilder_boxer_request']['Normal']

        assert_that(normal['INCENTIVIZED'], equal_to('true'))

    @allure.feature('ios 15 support')
    @allure.tag('smoke', 'v1.199.0', 'test_mode')
    @allure.story('PBJ-3860 [iOS15 + SDK6.10.1] AC MultiPage Reward: Missing Incentivized popup once closing the '
                  'playing video')
    @allure.description('Verify the INCENTIVIZED filed for instl placement via the iOS 15 request '
                        'when SDK <= 6.10.2 iDSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['15'])
    def test_incentivized_field_2(self, pub_app_id, placement, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        normal = response_payload['ext']['debug']['auction_result']['adbuilder_boxer_request']['Normal']

        assert_keys_exist(normal, 'INCENTIVIZED')

    @allure.feature('ios 15 support')
    @allure.tag('normal', 'v1.199.0')
    @allure.story('PBJ-3860 [iOS15 + SDK6.10.1] AC MultiPage Reward: Missing Incentivized popup once closing the '
                  'playing video')
    @allure.description('Verify the INCENTIVIZED filed for rewarded placement via the iOS 15 request '
                        'when SDK <= 6.10.2 eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['15'])
    def test_incentivized_field_3(self, pub_app_id, placement, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=sdk_v,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        normal = response_payload['ext']['debug']['auction_result']['adbuilder_boxer_request']['Normal']

        assert_that(normal['INCENTIVIZED'], equal_to('true'))

    @allure.feature('ios 15 support')
    @allure.tag('normal', 'v1.199.0')
    @allure.story('PBJ-3860 [iOS15 + SDK6.10.1] AC MultiPage Reward: Missing Incentivized popup once closing the '
                  'playing video')
    @allure.description('Verify the INCENTIVIZED filed for instl placement via the iOS 15 request '
                        'when SDK <= 6.10.2 eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['15'])
    def test_incentivized_field_4(self, pub_app_id, placement, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, sdk_version=sdk_v,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        normal = response_payload['ext']['debug']['auction_result']['adbuilder_boxer_request']['Normal']

        assert_keys_exist(normal, 'INCENTIVIZED')

    @allure.feature('ios 15 support')
    @allure.tag('normal', 'v1.199.0', 'test_mode')
    @allure.story('PBJ-3860 [iOS15 + SDK6.10.1] AC MultiPage Reward: Missing Incentivized popup once closing the '
                  'playing video')
    @allure.description('Verify the INCENTIVIZED filed for rewarded placement via the iOS 15 request '
                        'when SDK > 6.10.2')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('osv', ['15'])
    def test_incentivized_field_5(self, pub_app_id, placement, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        assert_keys_not_exist(response_payload['ext']['debug']['auction_result'], 'adbuilder_boxer_request')

    @allure.feature('ios 15 support')
    @allure.tag('normal', 'v1.199.0', 'test_mode')
    @allure.story('PBJ-3860 [iOS15 + SDK6.10.1] AC MultiPage Reward: Missing Incentivized popup once closing the '
                  'playing video')
    @allure.description('Verify the INCENTIVIZED filed for rewarded placement via the iOS 15- request '
                        'when SDK <= 6.10.2')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['14'])
    def test_incentivized_field_6(self, pub_app_id, placement, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        assert_keys_not_exist(response_payload['ext']['debug']['auction_result'], 'adbuilder_boxer_request')

    @allure.feature('ios 15 support')
    @allure.tag('normal', 'v1.199.0')
    @allure.story('PBJ-3860 [iOS15 + SDK6.10.1] AC MultiPage Reward: Missing Incentivized popup once closing the '
                  'playing video')
    @allure.description('Verify the INCENTIVIZED filed for rewarded placement via the iOS 15 request '
                        'when SDK <= 6.10.2 Meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['15'])
    def test_incentivized_field_7(self, pub_app_id, placement, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=meister_rtb_ids,
                                          sdk_version=sdk_v))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()
        normal = response_payload['ext']['debug']['auction_result']['adbuilder_boxer_request']['Normal']
        assert_that(normal['INCENTIVIZED'], equal_to('true'))

    @allure.feature('ios 15 support')
    @allure.tag('normal', 'v1.199.0')
    @allure.story('PBJ-3860 [iOS15 + SDK6.10.1] AC MultiPage Reward: Missing Incentivized popup once closing the '
                  'playing video')
    @allure.description('Verify the INCENTIVIZED filed for instl placement via the iOS 15 request '
                        'when SDK <= 6.10.2 Meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['15'])
    def test_incentivized_field_8(self, pub_app_id, placement, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=meister_rtb_ids,
                                          sdk_version=sdk_v))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        normal = response_payload['ext']['debug']['auction_result']['adbuilder_boxer_request']['Normal']

        assert_keys_not_exist(normal, 'INCENTIVIZED')