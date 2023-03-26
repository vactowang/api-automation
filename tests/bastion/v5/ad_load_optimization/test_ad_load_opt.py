import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestAdLoadOpt(object):

    @allure.feature('ad download optimization')
    @allure.tag('normal', 'v0.103.0')
    @allure.story('PBJ-2988 Ad download optimization flag on config response')
    @allure.description('Test for the ad load optimization value for the enabled pub app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_load_opt_1(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(True))

    @allure.feature('ad download optimization')
    @allure.tag('normal', 'v0.103.0')
    @allure.story('PBJ-2988 Ad download optimization flag on config response')
    @allure.description('Test for the ad load optimization value for the not enabled pub app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_ad_load_opt_2(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(False))

    @allure.feature('ad download optimization')
    @allure.tag('normal', 'v0.103.0')
    @allure.story('PBJ-2988 Ad download optimization flag on config response')
    @allure.description('Test for the ad load optimization value for the no set pub app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    def test_ad_load_opt_3(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(False))

    @allure.feature('ad download optimization')
    @allure.tag('normal', 'v0.103.0')
    @allure.story('PBJ-2988 Ad download optimization flag on config response')
    @allure.description('Test for the ad load optimization value for the enabled Android pub app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ad_load_opt_4(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(True))

    @allure.feature('ad download optimization')
    @allure.tag('normal', 'v0.103.0')
    @allure.story('PBJ-2988 Ad download optimization flag on config response')
    @allure.description('Verify that Bastion does not filter the Windows and Amazon app on ad load optimization')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app, amazon_common_test_app])
    def test_ad_load_opt_5(self, pub_app_id):
        '''
            App level setting:
            "ad_load_optimization_enabled": true
        '''
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(True))

    @allure.feature('ad download optimization')
    @allure.tag('normal', 'v0.104.0')
    @allure.story('PBJ-3072 Default value for feature flag for ad download optimization to be OFF')
    @allure.description('Test for the ad load optimization default value should be false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    def test_ad_load_opt_default_value(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(False))

    @allure.feature('ad download optimization')
    @allure.tag('normal', 'v0.105.0', 'v0.124.0')
    @allure.story('PBJ-3073 Ad Download experiment'
                  'PBJ-4193 2022 Ad download optimization experiment'
                  'PBJ-4438 Remove autocache flag override for ADO experiment '
                  'PBJ-4493 Change version whitelist for DO_2022_phase2')
    @allure.description('Test for a no setting app enter the bucket of optimize'
                        'Test for all placements autocache are disabled if enter the experiment'
                        'Test for all autocache flag respect the setting on dashboard')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    def test_ad_download_exp_1(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=it_ip, sdk_version='Vungle/6.11.1'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        config_extension = response_payload['config_extension']
        parse_config_extension = str(decode_base64(config_extension))
        if 'Optimization_OFF' in parse_config_extension:

            assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(False))
        elif 'Optimization_ON' in parse_config_extension:
            assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(True))
        placements = response_payload['placements']
        for placement in placements:
            if placement['reference_id'] == 'DEFAULT02024':
                assert_that(placement['is_auto_cached'], equal_to(True))
            if placement['reference_id']  == 'AREYOUS82694':
                assert_that(placement['is_auto_cached'], equal_to(False))

    @allure.feature('ad download optimization')
    @allure.tag('normal', 'v0.105.0', 'v0.124.0')
    @allure.story('PBJ-3073 Ad Download experiment'
                  'PBJ-4193 2022 Ad download optimization experiment'
                  'PBJ-4438 Remove autocache flag override for ADO experiment'
                  'PBJ-4493 Change version whitelist for DO_2022_phase2')
    @allure.description('Test for a non-optimized app enter the bucket of optimize'
                        'Test for all placements autocache are disabled if enter the experiment'
                        'Test for sdk_v<6.11 will not enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_ad_download_exp_2(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=it_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(response_payload, 'config_extension')
        # config_extension = response_payload['config_extension']
        # parse_config_extension = str(decode_base64(config_extension))
        # assert_that('DownloadOptimization_2022' not in parse_config_extension)

    @allure.feature('ad download optimization')
    @allure.tag('normal', 'v0.105.0', 'v0.124.0')
    @allure.story('PBJ-3073 Ad Download experiment'
                  'PBJ-4193 2022 Ad download optimization experiment'
                  'PBJ-4493 Change version whitelist for DO_2022_phase2')
    @allure.description('Test for experiment will not impact the app which does not enter the experiment'
                        'Test for experiment will not impact the placment\' autocache if the app '
                        'does not enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    def test_ad_download_exp_3(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        config_extension = response_payload['config_extension']
        parse_config_extension = str(decode_base64(config_extension))
        assert_that('DownloadOptimization_2022' not in parse_config_extension)
        assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(False))
        placements = response_payload['placements']
        for placement in placements:
            if placement['reference_id'] == 'DEFAULT02024':
                assert_that(placement['is_auto_cached'], equal_to(True))

    @allure.feature('ad download optimization')
    @allure.tag('normal', 'v0.105.0', 'v0.124.0')
    @allure.story('PBJ-3073 Ad Download experiment'
                  'PBJ-4193 2022 Ad download optimization experiment'
                  'PBJ-4493 Change version whitelist for DO_2022_phase2')
    @allure.description('Test for experiment will not impact the app which does not enter the experiment'
                        'Test for experiment will not impact the placment\' autocache if the app '
                        'does not enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_ad_download_exp_4(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        config_extension = response_payload['config_extension']
        parse_config_extension = str(decode_base64(config_extension))
        assert_that('DownloadOptimization_2022' not in parse_config_extension)
        assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(False))
        placements = response_payload['placements']
        for placement in placements:
            if placement['reference_id'] == 'DEFAULT02022':
                assert_that(placement['is_auto_cached'], equal_to(True))


