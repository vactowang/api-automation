import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestAttribution(object):

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0', 'test_mode')
    @allure.story('PBJ-1899 SKAdNetwork support - jaeger should return attribution data in ad response')
    @allure.description('Verify that jaeger return the attribution info from DSP in test mode')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_attribution_info_test_mode(self, pub_app_id, placement, sdk_v, osv):
        network_ids = ['test.ad.nw.001', 'test.nw.45646546', kraken_served_ad_network_id]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'version')
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['fidelity_type'], equal_to(0))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'version')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_type')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_description')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_purchaser_name')

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0')
    @allure.story('PBJ-1899 SKAdNetwork support - jaeger should return attribution data in ad response')
    @allure.description('Verify that jaeger return the attribution info from DSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_attribution_info_from_idsp(self, pub_app_id, placement, sdk_v, osv):
        network_ids = ['test.ad.nw.001', 'test.nw.45646546', kraken_served_ad_network_id]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv, gdpr='opted_out', ccpa='opted_out')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=eu_country_ip, sdk_version=sdk_v, debug='jaeger',
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'version')
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['fidelity_type'], equal_to(0))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'version')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_type')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_description')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_purchaser_name')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'R_1.135.0')
    @allure.story('PBJ-1899 SKAdNetwork support - jaeger should return attribution data in ad response')
    @allure.description('Verify that Jaeger passed no network id to iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_attribution_info_no_network_id_passed(self, pub_app_id, placement, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(ad_markup, 'attribution')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for idsp when sdk >= 6.10.0 and osv >= 14.5 '
                        'in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_for_skadimpression_attribution_1(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids_1,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'version')
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['fidelity_type'], equal_to(0))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'version')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_type')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_description')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_purchaser_name')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for idsp when sdk < 6.10.0 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('osv', ['14.4', '14.5'])
    def test_for_skadimpression_attribution_2(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids_1,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'timestamp')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for idsp when sdk >= 6.10.0 and osv < 14.5 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_for_skadimpression_attribution_3(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids_1,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'version')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for idsp when sdk >= 6.10.0 and osv >= 14.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5', '14.6'])
    def test_for_skadimpression_attribution_4(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'version')
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['fidelity_type'], equal_to(0))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'version')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_type')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_description')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_purchaser_name')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for idsp when sdk < 6.10.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('osv', ['14.4', '14.5'])
    def test_for_skadimpression_attribution_5(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'timestamp')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for idsp when sdk >= 6.10.0 and osv < 14.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_for_skadimpression_attribution_6(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'version')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for edsp when sdk >= 6.10.0 and osv >= 14.5 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5', '14.6'])
    def test_for_skadimpression_attribution_7(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['cDkw7geQsH.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to('cDkw7geQsH.skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'version')
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['ad_network_id'],
                    equal_to('cDkw7geQsH.skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['fidelity_type'], equal_to(0))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'version')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_type')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_description')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_purchaser_name')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for edsp when sdk < 6.10.0 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('osv', ['14.4', '14.5'])
    def test_for_skadimpression_attribution_8(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['cDkw7geQsH.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['ad_network_id'],
                    equal_to('cDkw7geQsH.skadnetwork'))
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'timestamp')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for edsp when SDK >= 6.10.0 and osv < 14.5 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_for_skadimpression_attribution_9(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['cDkw7geQsH.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to('cDkw7geQsH.skadnetwork'))
        assert_keys_not_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'fidelity_type')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'version')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for edsp when sdk >= 6.10.0 and osv >= 14.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_for_skadimpression_attribution_10(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['cDkw7geQsH.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to('cDkw7geQsH.skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'version')
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['ad_network_id'],
                    equal_to('cDkw7geQsH.skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['fidelity_type'], equal_to(0))
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'version')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_type')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_description')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['viewthrough'], 'ad_purchaser_name')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for edsp when sdk < 6.10.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('osv', ['14.4', '14.5'])
    def test_for_skadimpression_attribution_11(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['cDkw7geQsH.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['ad_network_id'],
                    equal_to('cDkw7geQsH.skadnetwork'))
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork'], 'timestamp')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for the attributijon for edsp when sdk >= 6.10.0 and osv < 14.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_for_skadimpression_attribution_12(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['cDkw7geQsH.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to('cDkw7geQsH.skadnetwork'))
        assert_keys_not_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'fidelity_type')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'source_app_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'itunes_item_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'signature')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'campaign_id')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'nonce')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'timestamp')
        assert_keys_exist(ad_markup['attribution']['skadnetwork']['storekit'], 'version')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v0.17.0', 'test_mode', 'kraken')
    @allure.story('PBJ-2893 Kraken should generate SkAdnetwork signature dynamically')
    @allure.description('Verify that Kraken response the non-hard coded skadnetwork info for new format')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_kraken_support_skadnetwork_1(self, pub_app_id, placement, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        storekit_sig = ad_markup['attribution']['skadnetwork']['storekit']['signature']
        storekit_nonce = ad_markup['attribution']['skadnetwork']['storekit']['nonce']
        viewthrough_sig = ad_markup['attribution']['skadnetwork']['viewthrough']['signature']
        viewthrough_nonce = ad_markup['attribution']['skadnetwork']['viewthrough']['nonce']

        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['source_app_id'],
                    equal_to(int(bid_request['app']['bundle'])))
        assert_that(storekit_sig, not equal_to(None))
        assert_that(storekit_nonce, not equal_to(None))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['fidelity_type'], equal_to(0))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['source_app_id'],
                    equal_to(int(bid_request['app']['bundle'])))
        assert_that(viewthrough_sig, not equal_to(None))
        assert_that(viewthrough_nonce, equal_to(storekit_nonce))

        r1 = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                         rtb_selector=test_mode_kraken_rtb_ids))
        response_payload_1 = r1.json()
        assert_response_status_code(r1.status_code, HTTPStatus.OK)
        assert_valid_schema(r1.json(), response_schema.ads_v5_debug)

        ad_markup_1 = response_payload_1['ads'][0]['ad_markup']
        assert_that(ad_markup_1['attribution']['skadnetwork']['storekit']['signature'], not equal_to(storekit_sig))
        assert_that(ad_markup_1['attribution']['skadnetwork']['storekit']['nonce'], not equal_to(storekit_nonce))
        assert_that(ad_markup_1['attribution']['skadnetwork']['viewthrough']['signature'],
                    not equal_to(viewthrough_sig))
        assert_that(ad_markup_1['attribution']['skadnetwork']['viewthrough']['nonce'], not equal_to(viewthrough_nonce))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v0.17.0', 'kraken')
    @allure.story('PBJ-2893 Kraken should generate SkAdnetwork signature dynamically')
    @allure.description('Verify that Kraken response the non-hard coded skadnetwork info for new format '
                        'in non-test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_kraken_support_skadnetwork_2(self, pub_app_id, placement, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), skadnetwork_ids=network_ids,
                                            os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        storekit_sig = ad_markup['attribution']['skadnetwork']['storekit']['signature']
        storekit_nonce = ad_markup['attribution']['skadnetwork']['storekit']['nonce']
        viewthrough_sig = ad_markup['attribution']['skadnetwork']['viewthrough']['signature']
        viewthrough_nonce = ad_markup['attribution']['skadnetwork']['viewthrough']['nonce']

        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['source_app_id'],
                    equal_to(int(bid_request['app']['bundle'])))
        assert_that(storekit_sig, not equal_to(None))
        assert_that(storekit_nonce, not equal_to(None))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['fidelity_type'], equal_to(0))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['version'], equal_to('2.2'))
        assert_that(ad_markup['attribution']['skadnetwork']['viewthrough']['source_app_id'],
                    equal_to(int(bid_request['app']['bundle'])))
        assert_that(viewthrough_sig, not equal_to(None))
        assert_that(viewthrough_nonce, equal_to(storekit_nonce))

        r1 = post(ads_v5_endpoint_qa, json=req,
                  headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                           rtb_selector=non_test_mode_kraken_rtb_ids))
        response_payload_1 = r1.json()
        assert_response_status_code(r1.status_code, HTTPStatus.OK)
        assert_valid_schema(r1.json(), response_schema.ads_v5_debug)

        ad_markup_1 = response_payload_1['ads'][0]['ad_markup']
        assert_that(ad_markup_1['attribution']['skadnetwork']['storekit']['signature'], not equal_to(storekit_sig))
        assert_that(ad_markup_1['attribution']['skadnetwork']['storekit']['nonce'], not equal_to(storekit_nonce))
        assert_that(ad_markup_1['attribution']['skadnetwork']['viewthrough']['signature'],
                    not equal_to(viewthrough_sig))
        assert_that(ad_markup_1['attribution']['skadnetwork']['viewthrough']['nonce'], not equal_to(viewthrough_nonce))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v0.17.0', 'test_mode', 'kraken')
    @allure.story('PBJ-2893 Kraken should generate SkAdnetwork signature dynamically')
    @allure.description('Verify that Kraken response the non-hard coded skadnetwork info for old format')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_kraken_support_skadnetwork_3(self, pub_app_id, placement, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        ad_markup = response_payload['ads'][0]['ad_markup']
        sig = ad_markup['attribution']['skadnetwork']['signature']
        nonce = ad_markup['attribution']['skadnetwork']['nonce']

        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['ad_network_id'], equal_to(kraken_served_ad_network_id))
        assert_that(sig, not equal_to(None))
        assert_that(nonce, not equal_to(None))

        r1 = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                         rtb_selector=test_mode_kraken_rtb_ids))
        response_payload_1 = r1.json()
        assert_response_status_code(r1.status_code, HTTPStatus.OK)
        assert_valid_schema(r1.json(), response_schema.ads_v5_debug)

        ad_markup_1 = response_payload_1['ads'][0]['ad_markup']
        assert_that(ad_markup_1['attribution']['skadnetwork']['signature'], not equal_to(sig))
        assert_that(ad_markup_1['attribution']['skadnetwork']['nonce'], not equal_to(nonce))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v0.17.0', 'test_mode', 'kraken')
    @allure.story('PBJ-2893 Kraken should generate SkAdnetwork signature dynamically')
    @allure.description('Verify that Kraken response the non-hard coded skadnetwork info for old format '
                        'in non-test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_kraken_support_skadnetwork_4(self, pub_app_id, placement, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        ad_markup = response_payload['ads'][0]['ad_markup']
        sig = ad_markup['attribution']['skadnetwork']['signature']
        nonce = ad_markup['attribution']['skadnetwork']['nonce']

        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['ad_network_id'], equal_to(kraken_served_ad_network_id))
        assert_that(sig, not equal_to(None))
        assert_that(nonce, not equal_to(None))

        r1 = post(ads_v5_endpoint_qa, json=req,
                  headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                           rtb_selector=non_test_mode_kraken_rtb_ids))
        response_payload_1 = r1.json()
        assert_response_status_code(r1.status_code, HTTPStatus.OK)
        assert_valid_schema(r1.json(), response_schema.ads_v5_debug)

        ad_markup_1 = response_payload_1['ads'][0]['ad_markup']
        assert_that(ad_markup_1['attribution']['skadnetwork']['signature'], not equal_to(sig))
        assert_that(ad_markup_1['attribution']['skadnetwork']['nonce'], not equal_to(nonce))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v0.17.0', 'test_mode', 'kraken')
    @allure.story('PBJ-2893 Kraken should generate SkAdnetwork signature dynamically')
    @allure.description('Verify that Kraken does not serve with non-matched network id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_kraken_support_skadnetwork_5(self, pub_app_id, placement, sdk_v, osv):
        network_ids = ['test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'attribution')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v0.17.0', 'test_mode', 'kraken')
    @allure.story('PBJ-2893 Kraken should generate SkAdnetwork signature dynamically')
    @allure.description('Verify that Kraken does not serve with non-matched network id in non-test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_kraken_support_skadnetwork_6(self, pub_app_id, placement, sdk_v, osv):
        network_ids = ['test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'attribution')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v0.17.0', 'test_mode', 'kraken')
    @allure.story('PBJ-2893 Kraken should generate SkAdnetwork signature dynamically')
    @allure.description('Verify that Kraken response the non-hard coded skadnetwork info for new format'
                        '(storekit only)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_kraken_support_skadnetwork_7(self, pub_app_id, placement, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        storekit_sig = ad_markup['attribution']['skadnetwork']['storekit']['signature']
        storekit_nonce = ad_markup['attribution']['skadnetwork']['storekit']['nonce']

        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['source_app_id'],
                    equal_to(int(bid_request['app']['bundle'])))
        assert_that(storekit_sig, not equal_to(None))
        assert_that(storekit_nonce, not equal_to(None))

        r1 = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v,
                                                                         rtb_selector=test_mode_kraken_rtb_ids))
        response_payload_1 = r1.json()
        assert_response_status_code(r1.status_code, HTTPStatus.OK)
        assert_valid_schema(r1.json(), response_schema.ads_v5_debug)

        ad_markup_1 = response_payload_1['ads'][0]['ad_markup']
        assert_that(ad_markup_1['attribution']['skadnetwork']['storekit']['signature'], not equal_to(storekit_sig))
        assert_that(ad_markup_1['attribution']['skadnetwork']['storekit']['nonce'], not equal_to(storekit_nonce))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v0.17.0', 'test_mode', 'kraken')
    @allure.story('PBJ-2893 Kraken should generate SkAdnetwork signature dynamically')
    @allure.description('Verify that Kraken response the non-hard coded skadnetwork info for new format'
                        '(storekit only) in non-test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_kraken_support_skadnetwork_8(self, pub_app_id, placement, sdk_v, osv):
        network_ids = [kraken_served_ad_network_id, 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        storekit_sig = ad_markup['attribution']['skadnetwork']['storekit']['signature']
        storekit_nonce = ad_markup['attribution']['skadnetwork']['storekit']['nonce']

        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['ad_network_id'],
                    equal_to(kraken_served_ad_network_id))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['fidelity_type'], equal_to(1))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['version'], equal_to('2.0'))
        assert_that(ad_markup['attribution']['skadnetwork']['storekit']['source_app_id'],
                    equal_to(int(bid_request['app']['bundle'])))
        assert_that(storekit_sig, not equal_to(None))
        assert_that(storekit_nonce, not equal_to(None))

        r1 = post(ads_v5_endpoint_qa, json=req,
                  headers=platform_headers(debug='jaeger', sdk_version=sdk_v, src_ip=au_ip,
                                           rtb_selector=non_test_mode_kraken_rtb_ids))
        response_payload_1 = r1.json()
        assert_response_status_code(r1.status_code, HTTPStatus.OK)
        assert_valid_schema(r1.json(), response_schema.ads_v5_debug)

        ad_markup_1 = response_payload_1['ads'][0]['ad_markup']
        assert_that(ad_markup_1['attribution']['skadnetwork']['storekit']['signature'], not equal_to(storekit_sig))
        assert_that(ad_markup_1['attribution']['skadnetwork']['storekit']['nonce'], not equal_to(storekit_nonce))