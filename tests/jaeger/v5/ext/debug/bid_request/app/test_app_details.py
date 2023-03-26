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
class TestAppDetails(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request app')
    @allure.description('Verify app details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_app_details(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['app']['id'], equal_to(common_test_app))
        assert_that(isinstance(bid_request['app']['name'], str))
        assert_that(isinstance(bid_request['app']['bundle'], str))
        assert_that(str(bid_request['app']['storeurl']).count('http'), equal_to(1))
        assert_that(isinstance(set(bid_request['app']['cat']), set))
        assert_that(isinstance(bid_request['app']['privacypolicy'], int))
        assert_that(isinstance(bid_request['app']['publisher']['id'], str))
        assert_that(isinstance(set(bid_request['app']['publisher']['cat']), set))
        assert_that(isinstance(bid_request['app']['keywords'], str))
        assert_that(isinstance(bid_request['app']['ver'], str))

    @allure.feature('app details')
    @allure.tag('normal', 'R_1.137.0')
    @allure.story('PBJ-1958 Remove IAB25-7 (Incentivized) in the CAT for rewarded video [oRTB 2.5]')
    @allure.description('Verify that IAB25-7 does not in cat list from bid request for rewarded video')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_remove_item_from_cat_list_1(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('IAB25-7' not in bid_request['app']['cat'])
        assert_that('IAB25-7' not in bid_request['app']['publisher']['cat'])

    @allure.feature('app details')
    @allure.tag('normal', 'R_1.137.0', 'test_mode')
    @allure.story('PBJ-1958 Remove IAB25-7 (Incentivized) in the CAT for rewarded video [oRTB 2.5]')
    @allure.description('Verify that IAB25-7 does not in cat list from bid request for rewarded video')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_remove_item_from_cat_list_2(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that('IAB25-7' not in bid_request['app']['cat'])
        assert_that('IAB25-7' not in bid_request['app']['publisher']['cat'])

    @allure.feature('app details')
    @allure.tag('normal', 'v1.157.0')
    @allure.story('PBJ-2594 Jaeger account tag should be propagate to application tag')
    @allure.description('Verify the keywords from bid request come from account and pub app setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_jaeger_account_tags_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['app']['keywords'], equal_to('app,account,managed'))

    @allure.feature('app details')
    @allure.tag('normal', 'v1.157.0', 'test_mode')
    @allure.story('PBJ-2594 Jaeger account tag should be propagate to application tag')
    @allure.description('Verify the keywords from bid request come from account and pub app setting in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_jaeger_account_tags_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['app']['keywords'], equal_to('app,account,managed'))

    @allure.feature('app details')
    @allure.tag('normal', 'v1.167.0')
    @allure.story('PBJ-2923 Implement the "managed-vpn" tag rule')
    @allure.description('Verify the keyword of managed-vpn from bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_jaeger_account_tags_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['app']['keywords'], equal_to('app,account,managed-vpn'))

    @allure.feature('app details')
    @allure.tag('normal', 'v1.167.0', 'test_mode')
    @allure.story('PBJ-2923 Implement the "managed-vpn" tag rule')
    @allure.description('Verify the keyword of managed-vpn from bid request in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    def test_jaeger_account_tags_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['app']['keywords'], equal_to('app,account,managed-vpn'))