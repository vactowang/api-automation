import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
@allure.feature('basic')
class TestBastionEndpoints(object):

    @allure.feature('experiments')
    @allure.tag('normal', 'v0.117.0')
    @allure.story('PBJ-3978 Implements KONA Experiments code in Bastion')
    @allure.description('Test that the app which enter experiment will return the endpoint in bucket for ads')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b3', '59786bc2a43b3a08620016b4'])
    def test_kona_exp_1(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that('api' in response_payload['endpoints']['ads'])

    @allure.feature('experiments')
    @allure.tag('normal', 'v0.117.0')
    @allure.story('PBJ-3978 Implements KONA Experiments code in Bastion')
    @allure.description('Test that the app which not enter experiment will not be impacted')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_kona_exp_2(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['endpoints']['ads'],
                    equal_to('http://jaeger-reg-apiqa-jaeger.ads-qa.vungle.com/api/v5/ads'))

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-3828 [Bastion]Add experiments to config extension')
    @allure.description('Test the experiments added to config extension in the bid response when the request '
                        'enter the experiment for sdk_v>=6.11+')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1', 'Vungle/6.12.0'])
    def test_kona_config_ext_1(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that('config_extension' in response_payload)
        config_extension_string = response_payload['config_extension']
        # to check when request with config_ext, no error
        req = request_payload.config_v5_ios(pub_app_id, ext=config_extension_string)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-3828 [Bastion]Add experiments to config extension')
    @allure.description('Test the experiments added to config extension in the bid response when the request '
                        'enter the experiment for sdk_v>=6.11+ on android platform')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_kona_config_ext_2(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that('config_extension' in response_payload)
        config_extension_string = response_payload['config_extension']
        # to check when request with config_ext, no error
        req = request_payload.config_v5_android(pub_app_id, ext=config_extension_string)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-4111 It can\'t enter the KONA A/B experiment in case of device id is null '
                  'from the config request')
    @allure.description('Test for it can enter into experiment if device id is null for iOS pub')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_kona_config_ext_3(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id, ifa='', idfv='')
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that('config_extension' in response_payload)
        config_extension_string = response_payload['config_extension']
        # to check when request with config_ext, no error
        req = request_payload.config_v5_ios(pub_app_id, ext=config_extension_string)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-4111 It can\'t enter the KONA A/B experiment in case of device id is null '
                  'from the config request')
    @allure.description('Test for it can enter into experiment if device id is null for iOS pub')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_kona_config_ext_4(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_android(pub_app_id, android_id='')
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that('config_extension' in response_payload)
        config_extension_string = response_payload['config_extension']
        # to check when request with config_ext, no error
        req = request_payload.config_v5_android(pub_app_id, ext=config_extension_string)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-3828 [Bastion]Add experiments to config extension')
    @allure.description('Test the experiment will apply in case of request with exp name in config extension via 6.11+')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_kona_config_ext_apply_scope_01(self, pub_app_id, sdk_v):
        '''
        experiments setting:

        apply_strategy:'bastion'
        name: KONAVerifyAB_4068
        '''
        req = request_payload.config_v5_ios(pub_app_id, ext=config_extension_1)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('api' in response_payload['endpoints']['ads'])
        assert_keys_exist(response_payload, 'config_extension')
        cfg_ext = response_payload['config_extension']
        cfg_ext = base64.b64decode(cfg_ext).decode('utf-8')
        assert_that("KONAVerifyAB_4068" in cfg_ext)

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-3828 [Bastion]Add experiments to config extension')
    @allure.description('Test the experiment will apply in case of request with exp name '
                        'in config extension for null IFA via 6.11+')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_kona_config_ext_apply_scope_02(self, pub_app_id, sdk_v):
        '''
        experiments setting:

        apply_strategy:'bastion'
        name: KONAVerifyAB_4068
        '''
        req = request_payload.config_v5_ios(pub_app_id, ext=config_extension_1, ifa="")
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('api' in response_payload['endpoints']['ads'])
        assert_keys_exist(response_payload, 'config_extension')
        cfg_ext = response_payload['config_extension']
        cfg_ext = base64.b64decode(cfg_ext).decode('utf-8')
        assert_that("KONAVerifyAB_4068" in cfg_ext)

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-3828 [Bastion]Add experiments to config extension')
    @allure.description('Test the experiment will apply in case of request with exp name '
                        'not in config extension via 6.11+')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_kona_config_ext_apply_scope_03(self, pub_app_id, sdk_v):
        '''
        experiments setting:

        apply_strategy:'bastion'
        name: KONAVerifyAB_4068
        '''
        req = request_payload.config_v5_ios(pub_app_id, ext=config_extension)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('api' in response_payload['endpoints']['ads'])
        assert_keys_exist(response_payload, 'config_extension')
        cfg_ext = response_payload['config_extension']
        cfg_ext = base64.b64decode(cfg_ext).decode('utf-8')
        assert_that("KONAVerifyAB_4068" in cfg_ext)

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-3828 [Bastion]Add experiments to config extension')
    @allure.description('Test the experiment will apply in case of request with exp name '
                        'not in config extension for null IFA via 6.11+')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_kona_config_ext_apply_scope_04(self, pub_app_id, sdk_v):
        '''
        experiments setting:

        apply_strategy:'bastion'
        name: KONAVerifyAB_4068
        '''
        req = request_payload.config_v5_ios(pub_app_id, ext=config_extension, ifa="")
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('api' in response_payload['endpoints']['ads'])
        assert_keys_exist(response_payload, 'config_extension')
        cfg_ext = response_payload['config_extension']
        cfg_ext = base64.b64decode(cfg_ext).decode('utf-8')
        assert_that("KONAVerifyAB_4068" in cfg_ext)

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-3828 [Bastion]Add experiments to config extension')
    @allure.description('Test the experiment will apply in case of request without config extension via 6.11+')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_kona_config_ext_apply_scope_05(self, pub_app_id, sdk_v):
        '''
        experiments setting:

        apply_strategy:'bastion'
        name: KONAVerifyAB_4068
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('api' in response_payload['endpoints']['ads'])
        assert_keys_exist(response_payload, 'config_extension')
        cfg_ext = response_payload['config_extension']
        cfg_ext = base64.b64decode(cfg_ext).decode('utf-8')
        assert_that("KONAVerifyAB_4068" in cfg_ext)

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-3828 [Bastion]Add experiments to config extension')
    @allure.description('Test the experiment will apply in case of request without config extension '
                        'for null IFA via 6.11+')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_kona_config_ext_apply_scope_06(self, pub_app_id, sdk_v):
        '''
        experiments setting:

        apply_strategy:'bastion'
        name: KONAVerifyAB_4068
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa="")
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('api' in response_payload['endpoints']['ads'])
        assert_keys_exist(response_payload, 'config_extension')
        cfg_ext = response_payload['config_extension']
        cfg_ext = base64.b64decode(cfg_ext).decode('utf-8')
        assert_that("KONAVerifyAB_4068" in cfg_ext)

    @allure.feature('experiments')
    @allure.tag('normal')
    @allure.story('PBJ-3828 [Bastion]Add experiments to config extension')
    @allure.description('Test there is no config extension for the pub app which does not enter experiment and '
                        'request with config extension')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_kona_config_ext_apply_scope_07(self, pub_app_id, sdk_v):
        '''
        experiments setting:

        apply_strategy:'bastion'
        name: KONAVerifyAB_4068
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa="")
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('api' in response_payload['endpoints']['ads'])
        cfg_ext = response_payload['config_extension']
        cfg_ext = base64.b64decode(cfg_ext).decode('utf-8')
        assert_that('KONAVerifyAB' not in config_extension)

    @allure.feature('endpoints')
    @allure.tag('normal')
    @allure.story('PBJ-4434 SDK Error and Metrics logging - Bastion return endpoint')
    @allure.description('Verify Bastion  return the two endpoints for SDK error and metrics logging')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    def test_error_log_and_metrics_endpoint_add_to_bastion(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        endpoints = response_payload['endpoints']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(endpoints, 'error_logs')
        assert_keys_exist(endpoints, 'metrics')
        assert_that('/sdk/error_logs' in endpoints['error_logs'])
        assert_that('/sdk/metrics' in endpoints['metrics'])



    @allure.feature('endpoints')
    @allure.tag('normal')
    @allure.story('PBJ-5054 Update JS files for OMSDK')
    @allure.description('Verify that upgrade omsdkJs version to 1.4.2 for sdk_v=7.0.1')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.1', 'Vungle/7.0.2', 'Vungle/7.1.0'])
    def test_omsdkJs_update_01(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        endpoints = response_payload['endpoints']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(endpoints, 'omsdk_js')
        assert_that(endpoints['omsdk_js'], equal_to('https://cdn-lb.vungle.com/omsdk/1_4_2'))



    @allure.feature('endpoints')
    @allure.tag('normal')
    @allure.story('PBJ-5054 Update JS files for OMSDK')
    @allure.description('Verify that  omsdkJs version keep 1.3.16 for specify sdk version:Vungle/7.0.0-early, '
                        'Vungle/7.0.0-early2, Vungle/7.0.0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0-early', 'Vungle/7.0.0-early2', 'Vungle/7.0.0'])
    def test_omsdkJs_update_02(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        endpoints = response_payload['endpoints']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_exist(endpoints, 'omsdk_js')
        assert_that(endpoints['omsdk_js'], equal_to('https://cdn-lb.vungle.com/omsdk/1_3_16'))



    @allure.feature('endpoints')
    @allure.tag('normal')
    @allure.story('PBJ-5054 Update JS files for OMSDK')
    @allure.description('Verify that no omsdkJs endpoint below 7.0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    def test_omsdkJs_update_03(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        endpoints = response_payload['endpoints']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_keys_not_exist(endpoints, 'omsdk_js')







