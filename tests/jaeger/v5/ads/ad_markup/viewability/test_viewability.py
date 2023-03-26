import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestViewAbility(object):

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for om enabled app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_om_enabled_status_app_enabled(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        vungle_version='5.7'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'viewability')
        assert_that(ad_markup['viewability']['om']['is_enabled'], equal_to(True))
        assert_keys_exist(ad_markup['viewability']['om'], 'extra_vast')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for no om setting in app level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['DEFAULT02024'])
    def test_om_enabled_status_app_default_setting(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        vungle_version='5.7'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'viewability')
        assert_that(ad_markup['viewability']['om']['is_enabled'], equal_to(True))
        assert_keys_exist(ad_markup['viewability']['om'], 'extra_vast')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for om disabled app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b2'])
    @pytest.mark.parametrize('placement', ['DEFAULT02022'])
    def test_om_enabled_status_app_disabled(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        vungle_version='5.7'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(ad_markup, 'viewability')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for vungle api version < 5.7')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('apiv', ['5.6'])
    def test_om_enabled_status_vungle_api_version_ctl_1(self, pub_app_id, placement, apiv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        vungle_version=apiv))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(ad_markup, 'viewability')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for vungle api version >= 5.7')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('apiv', ['5.7', '5.8'])
    def test_om_enabled_status_vungle_api_version_ctl_2(self, pub_app_id, placement, apiv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                                                        vungle_version=apiv))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(ad_markup, 'viewability')
        assert_that(ad_markup['viewability']['om']['is_enabled'], equal_to(True))
        assert_keys_exist(ad_markup['viewability']['om'], 'extra_vast')