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
class TestConfigV5(object):

    @allure.story('Test for config v5 iOS')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_config_v5_ios(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=test_default_real_time_sdk_version))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

    @allure.story('Test for config v5 android')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_config_v5_android(self, pub_app_id):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

    @allure.story('Test for config v5 windows')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    def test_config_v5_windows(self, pub_app_id):
        req = request_payload.config_v5_windows(pub_app_id, windows_common_test_placement)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

    @allure.story('Test for config v5 with vungle droid version 5')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_config_v5_ios_vungle_droid_v5(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id, common_test_placement)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='VungleDroid/5.9.9'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

    @allure.story('Test for config v5 request without placement id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_config_v5_without_placement(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

    @allure.story('Test for config v5 with invalid placement id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_config_v5_with_invalid_placement(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id, 'ABCED1234')
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        assert_response_status_code(r.status_code, HTTPStatus.BAD_REQUEST)

    @allure.story('Test for config v5 with banner placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_config_v5_with_banner(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id, 'BANNER-TEST-01')
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

    @allure.story('Test for GDPR function in config v5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    @pytest.mark.parametrize('gdpr', ['opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_gdpr_config_v5(self, pub_app_id, ip, gdpr):
        req = request_payload.config_v5_ios(pub_app_id, gdpr=gdpr)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=ip))
        assert_response_status_code(r.status_code, HTTPStatus.OK)

    @allure.story('Test for auto cache in config v5')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_auto_cache_config_v5(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id, common_test_placement, auto_cached=True)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.1'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

    @allure.story('Test for default SDK refresh duration')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sdk_refresh_duration(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['config']['refresh_time'], equal_to(86400000))

    @allure.story('Test for Kiloo consent status override')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['58fa97228fac7a64660001d3'])
    def test_kiloo_consent_status(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=eu_country_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['gdpr']['is_country_data_protected'], equal_to(False))
        assert_that(response_payload['gdpr']['consent_title'], equal_to('Personalized Ads'))
        assert_that(response_payload['gdpr']['consent_message'],
                    equal_to('Ads are personalized. Denying would disable it'))
        assert_that(response_payload['gdpr']['consent_message_version'], equal_to('0.0'))
        assert_that(response_payload['gdpr']['button_accept'], equal_to('Accept'))
        assert_that(response_payload['gdpr']['button_deny'], equal_to('Deny'))

    @allure.story('Test for config v5 with the app of inactive account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5ee727db9b7e6205a49e5b18'])
    def test_config_v5_with_app_of_inactive_account(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        assert_response_status_code(r.status_code, HTTPStatus.BAD_REQUEST)

    # ------- below test cases are for coppa_preference=2 (means prefer api's value) and sdk_v>=6.10.4------------------

    @allure.feature('COPPA support')
    @allure.tag('smoke')
    @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
                  'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    @allure.description('Verify the disable_ad_id flag for Android when sdk_v>=6.10.4')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_config_v5_coppa_android_1(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:

        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;

        """
        req = request_payload.config_v5_android(pub_app_id, coppa=coppa)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_ad_id')

        if coppa:
            assert_that(response_payload['disable_ad_id'] is True)
        else:
            assert_that(response_payload['disable_ad_id'] is False)

    @allure.feature('COPPA support')
    @allure.tag('smoke')
    @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
                  'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    @allure.description('Verify the disable_ad_id flag flag for Android when sdk_v>=6.10.4')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_config_v5_coppa_android_2(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:

        "isCoppaCompliant": true
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;

        """
        req = request_payload.config_v5_android(pub_app_id, coppa=coppa)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_ad_id')
        if coppa is False:
            assert_that(response_payload['disable_ad_id'] is False)
        else:
            assert_that(response_payload['disable_ad_id'] is True)

    @allure.feature('COPPA support')
    @allure.tag('smoke')
    @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
                  'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    @allure.description('Verify the disable_ad_id flag flag for Amazon when sdk_v>=6.10.4')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_config_v5_coppa_amazon_1(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:

        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;

        """
        req = request_payload.config_v5_amazon(pub_app_id, coppa=coppa)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_ad_id')
        assert_that(response_payload['disable_ad_id'] is False)

    @allure.feature('COPPA support')
    @allure.tag('smoke')
    @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
                  'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    @allure.description('Verify the disable_ad_id flag for ios when sdk_v>=6.11.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_config_v5_coppa_ios_1(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:

        "isCoppaCompliant": true
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;

        """
        req = request_payload.config_v5_ios(pub_app_id, coppa=coppa)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_ad_id')
        if coppa is False:
            assert_that(response_payload['disable_ad_id'] is False)
        else:
            assert_that(response_payload['disable_ad_id'] is True)

    @allure.feature('COPPA support')
    @allure.tag('smoke')
    @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
                  'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    @allure.description('Verify the disable_ad_id flag for ios when sdk_v>=6.11.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_config_v5_coppa_ios_2(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:

        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;

        """
        req = request_payload.config_v5_ios(pub_app_id, coppa=coppa)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_ad_id')
        if coppa:
            assert_that(response_payload['disable_ad_id'] is True)
        else:
            assert_that(response_payload['disable_ad_id'] is False)

    @allure.feature('COPPA support')
    @allure.tag('smoke')
    @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
                  'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    @allure.description('Verify the disable_ad_id flag for windows when sdk_v>=6.11.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_config_v5_coppa_windows_1(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:

        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;

        """
        req = request_payload.config_v5_windows(pub_app_id, coppa=coppa)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_ad_id')
        assert_that(response_payload['disable_ad_id'] is False)

    # ------- below test cases are for coppa_preference=1 (means dashboard+api's value) and sdk_v>=6.10.4---------------
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for Android when sdk_v>=6.10.4 and coppa_preference=1')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_coppa_perference1_android_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #
    #     """
    #     req = request_payload.config_v5_android(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #
    #     if coppa:
    #         assert_that(response_payload['disable_ad_id'] is True)
    #     else:
    #         assert_that(response_payload['disable_ad_id'] is False)
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag flag for Android when sdk_v>=6.10.4 and coppa_preference=1')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_coppa_perference1_android_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": true
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
    #
    #     """
    #     req = request_payload.config_v5_android(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is True)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag flag for Amazon when sdk_v>=6.10.4 and coppa_preference =1')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_coppa_preference1_amazon_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #
    #     """
    #     req = request_payload.config_v5_amazon(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for ios when sdk_v>=6.11.0 and coppa_preference =1')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_coppa_preference1_ios_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": true
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
    #
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is True)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for ios when sdk_v>=6.11.0 and coppa_preference =1')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_coppa_preference1_ios_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     if coppa:
    #         assert_that(response_payload['disable_ad_id'] is True)
    #     else:
    #         assert_that(response_payload['disable_ad_id'] is False)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for windows when sdk_v>=6.11.0 and coppa_preference =1')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_coppa_perference1_windows_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #
    #     """
    #     req = request_payload.config_v5_windows(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)

    # ----------------- below test cases are for no coppa_perference and sdk_v>=6.10.4----------------------------------
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for Android when sdk_v>=6.10.4 and no coppa_preference')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_coppa_perference_android_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #     default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_android(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #
    #     if coppa:
    #         assert_that(response_payload['disable_ad_id'] is True)
    #     else:
    #         assert_that(response_payload['disable_ad_id'] is False)
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag flag for Android when sdk_v>=6.10.4 and no coppa_preference')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_coppa_perference_android_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": true
    #     case:
    #     "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
    #      default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_android(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is True)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag flag for Amazon when sdk_v>=6.10.4 and and no coppa_preference')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_coppa_perference_amazon_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #      default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_amazon(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for ios when sdk_v>=6.11.0 and no coppa_preference')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_coppa_perference_ios_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": true
    #     case:
    #     coppa_preference:1; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
    #     default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is True)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for ios when sdk_v>=6.11.0 and no coppa_preference')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_coppa_perference_ios_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #     default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     if coppa:
    #         assert_that(response_payload['disable_ad_id'] is True)
    #     else:
    #         assert_that(response_payload['disable_ad_id'] is False)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for windows when sdk_v>=6.11.0 and no coppa_preference')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_coppa_perference_windows_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #     default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_windows(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)

    # ----- below test cases are for no coppa_perference and disable_ad_id_by_reg is null  and sdk_v>=6.10.4------------

    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for Android when sdk_v>=6.10.4 and no reg')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_reg_android_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     "disable_ad_id_by_reg": {}; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #     default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_android(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag flag for Android when sdk_v>=6.10.4 and no reg')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_reg_android_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": true
    #     case:
    #     "disable_ad_id_by_reg": {}; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #     default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_android(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag flag for Amazon when sdk_v>=6.10.4 and and no reg')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_reg_amazon_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     "disable_ad_id_by_reg": {}; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #     default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_amazon(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for ios when sdk_v>=6.11.0 and no reg')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_reg_ios_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": true
    #     case:
    #     "disable_ad_id_by_reg": {}; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #     default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for ios when sdk_v>=6.11.0 and no reg')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_reg_ios_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #      "disable_ad_id_by_reg": {}; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #     default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for windows when sdk_v>=6.11.0 and no reg')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_reg_windows_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     case:
    #      "disable_ad_id_by_reg": {}; is_coppa(api):% coppa; is_coppa(dashboard):false;
    #     default coppa_preference=1
    #     """
    #     req = request_payload.config_v5_windows(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)

    # ---------------------------------------below test cases are for no legal_config in DB-----------------------------
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for Android when sdk_v>=6.10.4 no legal_config setting')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_legal_config_android_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     no legal_config setting
    #     """
    #     req = request_payload.config_v5_android(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag flag for Android when sdk_v>=6.10.4 and no legal_config setting')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_legal_config_android_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": true
    #     case:
    #     no legal_config
    #     """
    #     req = request_payload.config_v5_android(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag flag for Amazon when sdk_v>=6.10.4 and no legal_config setting')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_legal_config_amazon_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     no legal_config
    #     """
    #     req = request_payload.config_v5_amazon(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for ios when sdk_v>=6.11.0 and no legal_config setting')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_legal_config_ios_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": true
    #     case:
    #     no legal_config
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for ios when sdk_v>=6.11.0 and no legal_config')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_legal_config_ios_2(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     no legal_config
    #
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)
    #
    # @allure.feature('COPPA support')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x'
    #               'PBJ-3645 [COPPA][Bastion] Return is_coppa from dashboard setting for SDK for 6.11.0')
    # @allure.description('Verify the disable_ad_id flag for windows when sdk_v>=6.11.0 and  no legal_config')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('coppa', ["", True, False])
    # def test_config_v5_no_legal_config_windows_1(self, pub_app_id, sdk_v, coppa):
    #     """
    #     application coppa setting:
    #
    #     "isCoppaCompliant": false
    #     case:
    #     no legal_config
    #
    #     """
    #     req = request_payload.config_v5_windows(pub_app_id, coppa=coppa)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'disable_ad_id')
    #     assert_that(response_payload['disable_ad_id'] is False)

    # --------------------------------------below test cases are for  sdk_v< 6.10.4-------------------------------------

    @allure.feature('COPPA support')
    @allure.tag('smoke')
    @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x')
    @allure.description('Verify the disable_ad_id_if_coppa flag for Android when sdk_v< 6.10.4')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.10.0'])
    def test_config_v5_coppa_android_3(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_ad_id_if_coppa')
        assert_that(response_payload['disable_ad_id_if_coppa'] is True)

    @allure.feature('COPPA support')
    @allure.tag('smoke')
    @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x')
    @allure.description('Verify the disable_ad_id_if_coppa flag for Amazon when sdk_v < 6.10.4')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.10.0'])
    def test_config_v5_coppa_amazon_2(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_amazon(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_ad_id_if_coppa')
        assert_that(response_payload['disable_ad_id_if_coppa'] is False)

    @allure.feature('COPPA support')
    @allure.tag('smoke')
    @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x')
    @allure.description('Verify no disable_ad_id_if_coppa flag for ios when sdk_v< 6.11.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_config_v5_coppa_ios_3(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(response_payload, 'disable_ad_id_if_coppa')

    @allure.feature('COPPA support')
    @allure.tag('smoke')
    @allure.story('PBJ-3855 [Bastion] Return disable_ad_id for android>= 6.10.4 others 6.11.x')
    @allure.description('Verify no disable_ad_id_if_coppa flag for windows when sdk_v< 6.11.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_config_v5_coppa_windows_2(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_windows(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(response_payload, 'disable_ad_id_if_coppa')

    @allure.feature('auto cache')
    @allure.tag('smoke')
    @allure.story('PBJ-4049 [Bastion]Support A/B testing for auto-cache')
    @allure.description('Verify the auto cache flag=true in config response for enter experiment placement which '
                        'is_auto_cached=false in placement collection')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_auto_cache_flag_01(self, pub_app_id, sdk_v):
        '''
        experiment setting:
        {
          "_id": ObjectId("6231b336c12929fe79b9a7da"),
          "name": "AutoCache_2022_Phase1",
          "mutual_id": "6231b33da1efed76fac2b5b2",
          "allocate_strategy": "hash_device_id",
          "salt": "6231b34651116effe9bb2b9f",
          "is_all_countries": false,
          "countries": ["ID","PH","BR","SE","ES", "FR","IN"],
          "is_all_applications": false,
          "traffic_percentage": 10000,
          "scope": "jaeger",
          "start_date": ISODate("2022-03-21T00:00:00.000Z"),
          "end_date": ISODate("2099-12-31T23:59:59.999Z"),
          "enabled": true,
          "buckets": [
            {
              "_id": ObjectId("6231b351ea1d1d072d3cde92"),
              "name": "AutoCache",
              "weight": 100,
              "ext": {
                "is_auto_cache":true
              }
            },
            {
              "_id": ObjectId("6231b35c7149f347f8aeb3f8"),
              "name": "DisableAutoCache",
              "weight": 0,
              "ext": {
                  "is_auto_cache":false
              }
            }
          ],
          "app_whitelist": ["5e96a7062a68960001f67e01", "60c96bc54a4869cbbce2dc12", "5dbbcb0a073003001420bd62", "5e71a2a6d41f640001c61f0d", "610a7e3c4091446ef9cc6341", "5ae1d7c5cf3ad762761bbca1", "610e7a46b65052701ed62ca0", "60ca68c2be78bbdb97b2f0ff", "614a190a4331e96aca3d84ec", "5de6af07d1c7b800122d6eb7", "5aadecfe4a7f2166bec31525", "59d79942143c3e9b09005bd7", "60997467de80d741d7d10d58", "5c9c7a04d13ede0012e22ff2", "606a4bfe98071b6c2e623c92", "5e4e6838246d020018f1e653", "5fbf44956834251059a6f007", "59786bc2a43b3a08620026b1", "59e781de7fff7cb02500ca0e", "5dd72ebf001c531f8cf48083",],
          "placement_whitelist": []
        '''
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'CC4RVAN74965':
                assert_that(placement_obj['is_auto_cached'], equal_to(True))

    @allure.feature('auto cache')
    @allure.tag('smoke')
    @allure.story('PBJ-4049 [Bastion]Support A/B testing for auto-cache')
    @allure.description('Verify the auto cache flag=false in config response for enter experiment banner placement '
                        'which is_auto_cached=false in placement collection')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_auto_cache_flag_02(self, pub_app_id, sdk_v):
        '''
        experiment setting:
        {
          "_id": ObjectId("6231b336c12929fe79b9a7da"),
          "name": "AutoCache_2022_Phase1",
          "mutual_id": "6231b33da1efed76fac2b5b2",
          "allocate_strategy": "hash_device_id",
          "salt": "6231b34651116effe9bb2b9f",
          "is_all_countries": false,
          "countries": ["ID","PH","BR","SE","ES", "FR","IN"],
          "is_all_applications": false,
          "traffic_percentage": 10000,
          "scope": "jaeger",
          "start_date": ISODate("2022-03-21T00:00:00.000Z"),
          "end_date": ISODate("2099-12-31T23:59:59.999Z"),
          "enabled": true,
          "buckets": [
            {
              "_id": ObjectId("6231b351ea1d1d072d3cde92"),
              "name": "AutoCache",
              "weight": 100,
              "ext": {
                "is_auto_cache":true
              }
            },
            {
              "_id": ObjectId("6231b35c7149f347f8aeb3f8"),
              "name": "DisableAutoCache",
              "weight": 0,
              "ext": {
                  "is_auto_cache":false
              }
            }
          ],
          "app_whitelist": ["5e96a7062a68960001f67e01", "60c96bc54a4869cbbce2dc12", "5dbbcb0a073003001420bd62", "5e71a2a6d41f640001c61f0d", "610a7e3c4091446ef9cc6341", "5ae1d7c5cf3ad762761bbca1", "610e7a46b65052701ed62ca0", "60ca68c2be78bbdb97b2f0ff", "614a190a4331e96aca3d84ec", "5de6af07d1c7b800122d6eb7", "5aadecfe4a7f2166bec31525", "59d79942143c3e9b09005bd7", "60997467de80d741d7d10d58", "5c9c7a04d13ede0012e22ff2", "606a4bfe98071b6c2e623c92", "5e4e6838246d020018f1e653", "5fbf44956834251059a6f007", "59786bc2a43b3a08620026b1", "59e781de7fff7cb02500ca0e", "5dd72ebf001c531f8cf48083",],
          "placement_whitelist": []
        '''
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'BANNER_REALTIME_TEST-5167578':
                assert_that(placement_obj['is_auto_cached'], equal_to(False))

    @allure.feature('auto cache')
    @allure.tag('smoke')
    @allure.story('PBJ-4049 [Bastion]Support A/B testing for auto-cache')
    @allure.description('Verify the auto cache flag=false in config response for enter experiment placement '
                        'which is_auto_cached=false in placemnt collection when sdk_v>6.11.x')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_auto_cache_flag_03(self, pub_app_id, sdk_v):
        '''
        experiment setting:
        {
          "_id": ObjectId("6231b336c12929fe79b9a7da"),
          "name": "AutoCache_2022_Phase1",
          "mutual_id": "6231b33da1efed76fac2b5b2",
          "allocate_strategy": "hash_device_id",
          "salt": "6231b34651116effe9bb2b9f",
          "is_all_countries": false,
          "countries": ["ID","PH","BR","SE","ES", "FR","IN"],
          "is_all_applications": false,
          "traffic_percentage": 10000,
          "scope": "jaeger",
          "start_date": ISODate("2022-03-21T00:00:00.000Z"),
          "end_date": ISODate("2099-12-31T23:59:59.999Z"),
          "enabled": true,
          "buckets": [
            {
              "_id": ObjectId("6231b351ea1d1d072d3cde92"),
              "name": "AutoCache",
              "weight": 100,
              "ext": {
                "is_auto_cache":true
              }
            },
            {
              "_id": ObjectId("6231b35c7149f347f8aeb3f8"),
              "name": "DisableAutoCache",
              "weight": 0,
              "ext": {
                  "is_auto_cache":false
              }
            }
          ],
          "app_whitelist": ["5e96a7062a68960001f67e01", "60c96bc54a4869cbbce2dc12", "5dbbcb0a073003001420bd62", "5e71a2a6d41f640001c61f0d", "610a7e3c4091446ef9cc6341", "5ae1d7c5cf3ad762761bbca1", "610e7a46b65052701ed62ca0", "60ca68c2be78bbdb97b2f0ff", "614a190a4331e96aca3d84ec", "5de6af07d1c7b800122d6eb7", "5aadecfe4a7f2166bec31525", "59d79942143c3e9b09005bd7", "60997467de80d741d7d10d58", "5c9c7a04d13ede0012e22ff2", "606a4bfe98071b6c2e623c92", "5e4e6838246d020018f1e653", "5fbf44956834251059a6f007", "59786bc2a43b3a08620026b1", "59e781de7fff7cb02500ca0e", "5dd72ebf001c531f8cf48083",],
          "placement_whitelist": []
        '''
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'CC4RVAN74965-5167578':
                assert_that(placement_obj['is_auto_cached'], equal_to(False))

    @allure.feature('auto cache')
    @allure.tag('smoke')
    @allure.story('PBJ-4049 [Bastion]Support A/B testing for auto-cache')
    @allure.description('Verify the auto cache flag=false in config response for enter experiment placement '
                        'which is_auto_cached=false in placement collection when ip in not in db list')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_auto_cache_flag_04(self, pub_app_id, sdk_v):
        '''
        experiment setting:
        {
          "_id": ObjectId("6231b336c12929fe79b9a7da"),
          "name": "AutoCache_2022_Phase1",
          "mutual_id": "6231b33da1efed76fac2b5b2",
          "allocate_strategy": "hash_device_id",
          "salt": "6231b34651116effe9bb2b9f",
          "is_all_countries": false,
          "countries": ["ID","PH","BR","SE","ES", "FR","IN"],
          "is_all_applications": false,
          "traffic_percentage": 10000,
          "scope": "jaeger",
          "start_date": ISODate("2022-03-21T00:00:00.000Z"),
          "end_date": ISODate("2099-12-31T23:59:59.999Z"),
          "enabled": true,
          "buckets": [
            {
              "_id": ObjectId("6231b351ea1d1d072d3cde92"),
              "name": "AutoCache",
              "weight": 100,
              "ext": {
                "is_auto_cache":true
              }
            },
            {
              "_id": ObjectId("6231b35c7149f347f8aeb3f8"),
              "name": "DisableAutoCache",
              "weight": 0,
              "ext": {
                  "is_auto_cache":false
              }
            }
          ],
          "app_whitelist": ["5e96a7062a68960001f67e01", "60c96bc54a4869cbbce2dc12", "5dbbcb0a073003001420bd62", "5e71a2a6d41f640001c61f0d", "610a7e3c4091446ef9cc6341", "5ae1d7c5cf3ad762761bbca1", "610e7a46b65052701ed62ca0", "60ca68c2be78bbdb97b2f0ff", "614a190a4331e96aca3d84ec", "5de6af07d1c7b800122d6eb7", "5aadecfe4a7f2166bec31525", "59d79942143c3e9b09005bd7", "60997467de80d741d7d10d58", "5c9c7a04d13ede0012e22ff2", "606a4bfe98071b6c2e623c92", "5e4e6838246d020018f1e653", "5fbf44956834251059a6f007", "59786bc2a43b3a08620026b1", "59e781de7fff7cb02500ca0e", "5dd72ebf001c531f8cf48083",],
          "placement_whitelist": []
        '''
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=cn_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'CC4RVAN74965-5167578':
                assert_that(placement_obj['is_auto_cached'], equal_to(False))

    @allure.feature('auto cache')
    @allure.tag('smoke')
    @allure.story('PBJ-4049 [Bastion]Support A/B testing for auto-cache')
    @allure.description('Verify the auto cache flag will not be impacted in config response for '
                        'not enter experiment placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_auto_cache_flag_05(self, pub_app_id, sdk_v):
        '''
        experiment setting:
        {
          "_id": ObjectId("6231b336c12929fe79b9a7da"),
          "name": "AutoCache_2022_Phase1",
          "mutual_id": "6231b33da1efed76fac2b5b2",
          "allocate_strategy": "hash_device_id",
          "salt": "6231b34651116effe9bb2b9f",
          "is_all_countries": false,
          "countries": ["ID","PH","BR","SE","ES", "FR","IN"],
          "is_all_applications": false,
          "traffic_percentage": 10000,
          "scope": "jaeger",
          "start_date": ISODate("2022-03-21T00:00:00.000Z"),
          "end_date": ISODate("2099-12-31T23:59:59.999Z"),
          "enabled": true,
          "buckets": [
            {
              "_id": ObjectId("6231b351ea1d1d072d3cde92"),
              "name": "AutoCache",
              "weight": 100,
              "ext": {
                "is_auto_cache":true
              }
            },
            {
              "_id": ObjectId("6231b35c7149f347f8aeb3f8"),
              "name": "DisableAutoCache",
              "weight": 0,
              "ext": {
                  "is_auto_cache":false
              }
            }
          ],
          "app_whitelist": ["5e96a7062a68960001f67e01", "60c96bc54a4869cbbce2dc12", "5dbbcb0a073003001420bd62", "5e71a2a6d41f640001c61f0d", "610a7e3c4091446ef9cc6341", "5ae1d7c5cf3ad762761bbca1", "610e7a46b65052701ed62ca0", "60ca68c2be78bbdb97b2f0ff", "614a190a4331e96aca3d84ec", "5de6af07d1c7b800122d6eb7", "5aadecfe4a7f2166bec31525", "59d79942143c3e9b09005bd7", "60997467de80d741d7d10d58", "5c9c7a04d13ede0012e22ff2", "606a4bfe98071b6c2e623c92", "5e4e6838246d020018f1e653", "5fbf44956834251059a6f007", "59e781de7fff7cb02500ca0e", "5dd72ebf001c531f8cf48083",],
          "placement_whitelist": []
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=cn_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'HJKM6GM50919':
                assert_that(placement_obj['is_auto_cached'], equal_to(False))

    @allure.feature('auto cache')
    @allure.tag('smoke')
    @allure.story('PBJ-4049 [Bastion]Support A/B testing for auto-cache')
    @allure.description('Verify the auto cache flag=true in config response for enter experiment placement which '
                        'is_auto_cached=false in placemnt collection for windows')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    def test_auto_cache_flag_06(self, pub_app_id, sdk_v):
        '''
        experiment setting:
        {
          "_id": ObjectId("6231b336c12929fe79b9a7da"),
          "name": "AutoCache_2022_Phase1",
          "mutual_id": "6231b33da1efed76fac2b5b2",
          "allocate_strategy": "hash_device_id",
          "salt": "6231b34651116effe9bb2b9f",
          "is_all_countries": false,
          "countries": ["ID","PH","BR","SE","ES", "FR","IN"],
          "is_all_applications": false,
          "traffic_percentage": 10000,
          "scope": "jaeger",
          "start_date": ISODate("2022-03-21T00:00:00.000Z"),
          "end_date": ISODate("2099-12-31T23:59:59.999Z"),
          "enabled": true,
          "buckets": [
            {
              "_id": ObjectId("6231b351ea1d1d072d3cde92"),
              "name": "AutoCache",
              "weight": 100,
              "ext": {
                "is_auto_cache":true
              }
            },
            {
              "_id": ObjectId("6231b35c7149f347f8aeb3f8"),
              "name": "DisableAutoCache",
              "weight": 0,
              "ext": {
                  "is_auto_cache":false
              }
            }
          ],
          "app_whitelist": ["5e96a7062a68960001f67e01", "60c96bc54a4869cbbce2dc12", "5dbbcb0a073003001420bd62", "5e71a2a6d41f640001c61f0d", "610a7e3c4091446ef9cc6341", "5ae1d7c5cf3ad762761bbca1", "610e7a46b65052701ed62ca0", "60ca68c2be78bbdb97b2f0ff", "614a190a4331e96aca3d84ec", "5de6af07d1c7b800122d6eb7", "5aadecfe4a7f2166bec31525", "59d79942143c3e9b09005bd7", "60997467de80d741d7d10d58", "5c9c7a04d13ede0012e22ff2", "606a4bfe98071b6c2e623c92", "5e4e6838246d020018f1e653", "5fbf44956834251059a6f007", "59786bc2a43b3a08620026b1", "59e781de7fff7cb02500ca0e", "5dd72ebf001c531f8cf48083",],
          "placement_whitelist": []
        '''
        req = request_payload.config_v5_windows(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'REWARDEDDT-0648491':
                assert_that(placement_obj['is_auto_cached'], equal_to(True))

    @allure.feature('auto cache')
    @allure.tag('smoke')
    @allure.story('PBJ-3828 [Bastion]Add experiments to config extension')
    @allure.description('Verify the config extension should not include auto cache  experiment since bastion is not '
                        'in apply_strategy over 6.11+')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_auto_cache_flag_for_config_extension_01(self, pub_app_id, sdk_v):
        '''
        experiment setting:
        {
          "_id": ObjectId("6231b336c12929fe79b9a7da"),
          "name": "AutoCache_2022_Phase1",
          "mutual_id": "6231b33da1efed76fac2b5b2",
          "allocate_strategy": "hash_device_id",
          "salt": "6231b34651116effe9bb2b9f",
          "is_all_countries": false,
          "countries": ["ID","PH","BR","SE","ES", "FR","IN"],
          "is_all_applications": false,
          "traffic_percentage": 10000,
          "scope": "jaeger",
          "start_date": ISODate("2022-03-21T00:00:00.000Z"),
          "end_date": ISODate("2099-12-31T23:59:59.999Z"),
          "enabled": true,
          "buckets": [
            {
              "_id": ObjectId("6231b351ea1d1d072d3cde92"),
              "name": "AutoCache",
              "weight": 100,
              "ext": {
                "is_auto_cache":true
              }
            },
            {
              "_id": ObjectId("6231b35c7149f347f8aeb3f8"),
              "name": "DisableAutoCache",
              "weight": 0,
              "ext": {
                  "is_auto_cache":false
              }
            }
          ],
          "app_whitelist": ["5e96a7062a68960001f67e01", "60c96bc54a4869cbbce2dc12", "5dbbcb0a073003001420bd62", "5e71a2a6d41f640001c61f0d", "610a7e3c4091446ef9cc6341", "5ae1d7c5cf3ad762761bbca1", "610e7a46b65052701ed62ca0", "60ca68c2be78bbdb97b2f0ff", "614a190a4331e96aca3d84ec", "5de6af07d1c7b800122d6eb7", "5aadecfe4a7f2166bec31525", "59d79942143c3e9b09005bd7", "60997467de80d741d7d10d58", "5c9c7a04d13ede0012e22ff2", "606a4bfe98071b6c2e623c92", "5e4e6838246d020018f1e653", "5fbf44956834251059a6f007", "59786bc2a43b3a08620026b1", "59e781de7fff7cb02500ca0e", "5dd72ebf001c531f8cf48083",],
          "placement_whitelist": []
          "apply_strategy":["jaeger"]
        '''
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'CC4RVAN74965':
                assert_that(placement_obj['is_auto_cached'], equal_to(False))
        cfg_ext = response_payload['config_extension']
        cfg_ext = base64.b64decode(cfg_ext).decode('utf-8')
        assert_that("AutoCache_2022_Phase1" not in cfg_ext)

    # @allure.feature('auto cache')
    # @allure.tag('smoke')
    # @allure.story('PBJ-4049 [Bastion]Support A/B testing for auto-cache')
    # @allure.description('Verify the auto cache flag =false in config response for '
    #                     'enter experiment placement which is_auto_cached=true in placemeng config')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_auto_cache_flag_06(self, pub_app_id, sdk_v):
    #     '''
    #     experiment setting:
    #     {
    #       "_id": ObjectId("6231b336c12929fe79b9a7da"),
    #       "name": "AutoCache_2022_Phase1",
    #       "mutual_id": "6231b33da1efed76fac2b5b2",
    #       "allocate_strategy": "hash_device_id",
    #       "salt": "6231b34651116effe9bb2b9f",
    #       "is_all_countries": false,
    #       "countries": ["ID","PH","BR","SE","ES", "FR","IN"],
    #       "is_all_applications": false,
    #       "traffic_percentage": 10000,
    #       "scope": "jaeger",
    #       "start_date": ISODate("2022-03-21T00:00:00.000Z"),
    #       "end_date": ISODate("2099-12-31T23:59:59.999Z"),
    #       "enabled": true,
    #       "buckets": [
    #         {
    #           "_id": ObjectId("6231b351ea1d1d072d3cde92"),
    #           "name": "AutoCache",
    #           "weight": 0,
    #           "ext": {
    #             "is_auto_cache":true
    #           }
    #         },
    #         {
    #           "_id": ObjectId("6231b35c7149f347f8aeb3f8"),
    #           "name": "DisableAutoCache",
    #           "weight": 100,
    #           "ext": {
    #               "is_auto_cache":false
    #           }
    #         }
    #       ],
    #       "app_whitelist": ["5e96a7062a68960001f67e01", "60c96bc54a4869cbbce2dc12", "5dbbcb0a073003001420bd62", "5e71a2a6d41f640001c61f0d", "610a7e3c4091446ef9cc6341", "5ae1d7c5cf3ad762761bbca1", "610e7a46b65052701ed62ca0", "60ca68c2be78bbdb97b2f0ff", "614a190a4331e96aca3d84ec", "5de6af07d1c7b800122d6eb7", "5aadecfe4a7f2166bec31525", "59d79942143c3e9b09005bd7", "60997467de80d741d7d10d58", "5c9c7a04d13ede0012e22ff2", "606a4bfe98071b6c2e623c92", "5e4e6838246d020018f1e653", "5fbf44956834251059a6f007", "59e781de7fff7cb02500ca0e", "5dd72ebf001c531f8cf48083",],
    #       "placement_whitelist": []
    #     '''
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     placements = response_payload['placements']
    #     for placement_obj in placements:
    #         if placement_obj['reference_id'] == 'DEFAULT95027':
    #             assert_that(placement_obj['is_auto_cached'], equal_to(False))
    #         # check will not impact banner placement
    #         if placement_obj['reference_id'] == 'IN_APP_BIDDING_DISABLED_BANNER-9471286':
    #             assert_that(placement_obj['is_auto_cached'], equal_to(True))

    @allure.feature('session data')
    @allure.tag('smoke')
    @allure.story('PBJ-4049 Set session data flag disabled by default for 6.11 GA SDK')
    @allure.description('Verify session.enabled is false for dashboard setting is true')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0 GA', 'Vungle/6.11.1'])
    def test_session_enabled_01(self, pub_app_id, sdk_v):
        '''

        application setting:

        "sessionEnabled":true


        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        session = response_payload['session']
        assert_that(session['enabled'], equal_to(False))

    @allure.feature('session data')
    @allure.tag('smoke')
    @allure.story('PBJ-4049 Set session data flag disabled by default for 6.11 GA SDK')
    @allure.description('Verify session.enabled is false for dashboard setting is false')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0 GA', 'Vungle/6.11.1'])
    def test_session_enabled_02(self, pub_app_id, sdk_v):
        '''

        application setting:

        "sessionEnabled":false


        '''
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        session = response_payload['session']
        assert_that(session['enabled'], equal_to(False))

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story(
        'PBJ-4178 Add /status for HAProxy health check same with the main port for Bastion/Jaeger/HBP/Scrat')
    @allure.description('Verify /status endpoint work well on bastion')
    @allure.severity('smoke')
    def test_config_status_endpoint(self):
        r = get(config_status_endpoint_qa)
        assert_that(r.status_code, equal_to(200))

    @allure.story('Test for config v5 iOS')
    @allure.tag('basic', 'smoke', 'v0.121.0')
    @allure.story('PBJ-4205 Set Grindr Multi cache to 3 on Banner/MREC inventory'
                  'PBJ-4245 Update Multicache to 4 from 3 (which was set last week) on the 2 bidding placements')
    @allure.description('Verify max_hb_cache=4 for the specific placements on bastion')
    @pytest.mark.parametrize('pub_app_id', ["5cecaad90d9f9400180f505d"])
    def test_max_hb_cache(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_multi_cache_sdk_version))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] in ["BANNER-TEST-01", "BANNER-TEST-02"]:
                assert_that(placement_obj['max_hb_cache'], equal_to(4))

    @allure.story('Test for config v5 iOS')
    @allure.tag('basic', 'smoke', 'v0.121.0')
    @allure.story('PBJ-4205 Set Grindr Multi cache to 3 on Banner/MREC inventory'
                  'PBJ-4245 Update Multicache to 4 from 3 (which was set last week) on the 2 bidding placements')
    @allure.description('Verify the function will not impact other placements')
    @pytest.mark.parametrize('pub_app_id', ["5cecaad90d9f9400180f505d"])
    def test_max_hb_cache_01(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_multi_cache_sdk_version))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == "DEFAULT-9229332":
                assert_that(placement_obj['max_hb_cache'], equal_to(2))

    @allure.story('config extension')
    @allure.tag('basic')
    @allure.tag('basic', 'v0.131.0')
    @allure.story('PBJ-4848 RTA - pass lmt for realtime HB request by config extension')
    @allure.description('Verify lmt flag is added to config extension over sdk 6.12+')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('lmt', [0, 1])
    @pytest.mark.parametrize('sdk_v', ["Vungle/6.12.0"])
    def test_config_extension_lmt_flag_01(self, pub_app_id, lmt, sdk_v):

        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id(), lmt=lmt)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        config_extension = response_payload['config_extension']
        # verify that false/true in config extension.


    @allure.story('config extension')
    @allure.tag('basic')
    @allure.tag('basic', 'v0.131.0')
    @allure.story('PBJ-4848 RTA - pass lmt for realtime HB request by config extension')
    @allure.description('Verify no lmt flag added to config extension < sdk 6.12+')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('lmt', [0, 1])
    @pytest.mark.parametrize('sdk_v', ["Vungle/6.11.0"])
    def test_config_extension_lmt_flag_02(self, pub_app_id, lmt, sdk_v):

        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id(), lmt=lmt)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        config_extension = response_payload['config_extension']
        # verify no false/true in config extension.



    @allure.story('Real Time Experiment')
    @allure.tag('basic')
    @allure.story('PBJ-4876 RTA - use all data source from SDK instead of mediation partner')
    @allure.description('Verify below fields will add to config extension for 6.12+')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    def test_realtime_experiment_config_extension_01(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        config_extension = response_payload['config_extension']
        parse_config_extension = decode_base64(config_extension)
        # validate that:
        # connectiontype, make, model, os, osv, ua, h, w, ext.vungle.storage_bytes_available,
        # ext.vungle.volume, ext.vungle.battery_level
        # will record in config extension.

    @allure.story('Real Time Experiment')
    @allure.tag('basic')
    @allure.story('PBJ-4876 RTA - use all data source from SDK instead of mediation partner')
    @allure.description('Verify below fields will not add to config extension < 6.12+')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_realtime_exp])
    @pytest.mark.parametrize('placement_id', [common_test_pre_cache_placement])
    def test_realtime_experiment_config_extension_02(self, pub_app_id, placement_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version="Vungle/6.11.2", src_ip=au_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        if 'config_extension' in response_payload:
            assert_that('disable_ad_id' not in str(decode_base64(response_payload['config_extension'])))


    @allure.story('RTA')
    @allure.tag('basic')
    @allure.story('PBJ-5030 RTA - Refactor experiment to split traffic by config for Android')
    @allure.description('Verify will add android in config extension')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app_rta])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement_rta])
    @pytest.mark.parametrize('device_id', ["", gen_device_id()])
    def test_rta_android_01(self, pub_app_id, placement_id, device_id):
        req = request_payload.config_v5_android(pub_app_id, ifa=device_id, android_id=device_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        config_extension = response_payload['config_extension']
        placement_mc = response_payload['placements'][0]['max_hb_cache']
        decode_cfg = str(decode_base64(config_extension))
        if 'RealTimeAds_Disabled' in decode_cfg:
            assert_that(placement_mc, equal_to(2))
        elif 'RealTimeAds_NoCache' in decode_cfg:
            assert_that(placement_mc, equal_to(0))
    #
    # @allure.story('Real Time Experiment')
    # @allure.tag('basic')
    # @allure.story('PBJ-4306 2022 Real Time Ads Experiment')
    # @allure.description('Verify ad_load_optimization.enabled follows the experiment config if it enters the experiment')
    # @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620036b1'])
    # def test_realtime_experiment_03(self, pub_app_id):
    #     '''
    #         experiment setting: "ado_enabled": true
    #         pub app setting: "ad_load_optimization_enabled": false
    #     '''
    #     req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(True))
    #
    # @allure.story('Real Time Experiment')
    # @allure.tag('basic')
    # @allure.story('PBJ-4306 2022 Real Time Ads Experiment')
    # @allure.description('Verify ad_load_optimization.enabled=false if not enter the experiment for pub app not setting'
    #                     'ad_load_optimization')
    # @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620036b2'])
    # def test_realtime_experiment_04(self, pub_app_id):
    #     req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=fr_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(False))
    #
    # @allure.story('Real Time Experiment')
    # @allure.tag('basic')
    # @allure.story('PBJ-4306 2022 Real Time Ads Experiment')
    # @allure.description('Verify the non-hb placements will not enter the experiment')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement_id', ['HJKM6GM50911', 'HJKM6GM50918'])
    # def test_realtime_experiment_05(self, pub_app_id, placement_id):
    #
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #
    #     placements = response_payload['placements']
    #     for placement_obj in placements:
    #         if placement_obj['reference_id'] == placement_id:
    #             assert_keys_not_exist(placement_obj, 'max_hb_cache')
    #
    # @allure.story('Real Time Experiment')
    # @allure.tag('basic')
    # @allure.story('PBJ-4306 2022 Real Time Ads Experiment')
    # @allure.description('Verify app which is not added in whitelist will not enter the experiment')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('placement_id', ['VIDEO_MREC_TEST_ANDROID-001'])
    # def test_realtime_experiment_06(self, pub_app_id, placement_id):
    #
    #     req = request_payload.config_v5_android(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #
    #     placements = response_payload['placements']
    #     for placement_obj in placements:
    #         if placement_obj['reference_id'] == placement_id:
    #             assert_that(placement_obj['max_hb_cache'], equal_to(4))
    #
    # @allure.story('Real Time Experiment')
    # @allure.tag('basic')
    # @allure.story('PBJ-4306 2022 Real Time Ads Experiment'
    #               'PBJ-4667 Realtime - Only support realtime and realtime experiment from SDK 6.12+')
    # @allure.description('Verify app will not enter the experiment for sdk version < 6.12')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement_id', [common_test_pre_cache_placement, common_test_hybrid_placement])
    # def test_realtime_experiment_07(self, pub_app_id, placement_id):
    #
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=pre_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #
    #     placements = response_payload['placements']
    #     for placement_obj in placements:
    #         if placement_obj['reference_id'] == placement_id:
    #             assert_that(placement_obj['max_hb_cache'] not in [0, 3, 2])
    #
    # @allure.story('Experiment Framework')
    # @allure.tag('basic')
    # @allure.story('PBJ-4325 Jaeger - Experiment framework refactor for SDK >= 6.12')
    # @allure.description('Verify request with config extension and same device id will enter the same bucket.')
    # @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620036b1'])
    # def test_experiment_framework_refactor_01(self, pub_app_id):
    #     '''
    #         pub app 59786bc2a43b3a08620036b1 will only enter experiment Real_Time_Ads_2022_Phase0
    #     '''
    #     test_device_id = gen_device_id()
    #     req = request_payload.config_v5_ios(pub_app_id, ifa=test_device_id)
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     config_extension = response_payload['config_extension']
    #     req = request_payload.config_v5_ios(pub_app_id, ifa=test_device_id, ext=config_extension)
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     config_extension_1 = response_payload['config_extension']
    #     assert_that(config_extension, equal_to(config_extension_1))

    # @allure.story('Experiment Framework')
    # @allure.tag('basic')
    # @allure.story('PBJ-4325 Jaeger - Experiment framework refactor for SDK >= 6.11')
    # @allure.description('Verify request with config extension and same device id will enter the same bucket'
    #                     'traffic setting is 50%.')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    # def test_experiment_framework_refactor_02(self, pub_app_id):
    #     test_device_id = gen_device_id()
    #     req = request_payload.config_v5_ios(pub_app_id, ifa=test_device_id)
    #
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     config_extension = response_payload['config_extension']
    #     req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id(), ext=config_extension)
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     if 'config_extension' in response_payload:
    #         config_extension_1 = response_payload['config_extension']
    #         assert_that(config_extension, equal_to(config_extension_1))

    @allure.feature('realTime IP')
    @allure.tag('smoke')
    @allure.story('PBJ-4408 Realtime - Add IP to config extension in Bastion')
    @allure.description('Verify ip is added to config extension when ip_allowed=True:'
                        'realtime.hb_config = False, account = True')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_config_ip_01(self, pub_app_id, sdk_v):
        """
        realtime.hb_config.ip_allowed = False

        account.ip_allowed = True
        """
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        config_extension = response_payload['config_extension']
        parse_config_extension = str(decode_base64(config_extension))
        assert_that(fr_ip in parse_config_extension)


    @allure.feature('RTA')
    @allure.tag('smoke', 'v0.134.0')
    @allure.story('PBJ-4967 RTA - Fix no IFA when SDK not initialized issue')
    @allure.description('Verify disable_ad_id is added in config extension')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_rta_config_extension(self, pub_app_id, sdk_v):

        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        config_extension = response_payload['config_extension']
        parse_config_extension = str(decode_base64(config_extension))
        # assert that  disable_ad_id is added in config extension





    # @allure.feature('realTime IP')
    # @allure.tag('smoke')
    # @allure.story('PBJ-4408 Realtime - Add IP to config extension in Bastion')
    # @allure.description('Verify ip doses not add to config extension when ip_allowed=False:'
    #                     'realtime.hb_config = False, account = False')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # def test_config_ip_02(self, pub_app_id, sdk_v):
    #     """
    #     realtime.hb_config.ip_allowed = False
    #
    #     account.ip_allowed = False
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     config_extension = response_payload['config_extension']
    #     parse_config_extension = str(decode_base64(config_extension), 'utf-8')
    #     assert_that(fr_ip not in parse_config_extension)
    #
    # @allure.feature('realTime IP')
    # @allure.tag('smoke')
    # @allure.story('PBJ-4408 Realtime - Add IP to config extension in Bastion')
    # @allure.description('Verify ip doses not add to config extension when ip_allowed=False:'
    #                     'realtime.hb_config = False, account no setting')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    # @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # def test_config_ip_03(self, pub_app_id, sdk_v):
    #     """
    #     realtime.hb_config.ip_allowed = False
    #
    #     account.ip_allowed no setting
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     config_extension = response_payload['config_extension']
    #     parse_config_extension = str(decode_base64(config_extension), 'utf-8')
    #     assert_that(fr_ip not in parse_config_extension)

    @allure.feature('SKAdNetwork ID')
    @allure.tag('smoke')
    @allure.story('PBJ-4633 [RTA]Use SKAdNetwork ID from the Vungle app, instead of relying on mediation partners')
    @allure.description('Verify add network_ids in config extension')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    def test_skad_add_to_config_extension_01(self, pub_app_id, sdk_v):

        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=cn_ip))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'config_extension')
        config_extension = response_payload['config_extension']
        config_extension = str(decode_base64(config_extension))
        assert_that('test.ad.nw.001', is_in(config_extension))
        assert_that('test.nw.45646546', is_in(config_extension))

    # @allure.feature('realTime IP')
    # @allure.tag('smoke')
    # @allure.story('PBJ-4408 Realtime - Add IP to config extension in Bastion')
    # @allure.description('Verify ip doses add to config extension when ip_allowed=True:'
    #                     'realtime.hb_config = True, account = True/not Setting')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # def test_config_ip_04(self, pub_app_id, sdk_v):
    #     """
    #     realtime.hb_config.ip_allowed = True
    #
    #     account.ip_allowed=True/notSetting
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     config_extension = response_payload['config_extension']
    #     parse_config_extension = str(decode_base64(config_extension))
    #     assert_that(fr_ip in parse_config_extension)

    # @allure.feature('realTime IP')
    # @allure.tag('smoke')
    # @allure.story('PBJ-4408 Realtime - Add IP to config extension in Bastion')
    # @allure.description('Verify ip doses add to config extension when ip_allowed=True:'
    #                     'realtime.hb_config = True, account = not Set')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # def test_config_ip_05(self, pub_app_id, sdk_v):
    #     """
    #     realtime.hb_config.ip_allowed = True
    #
    #     account.ip_allowed=notSetting
    #     """
    #     req = request_payload.config_v5_android(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     config_extension = response_payload['config_extension']
    #     parse_config_extension = str(decode_base64(config_extension))
    #     assert_that(fr_ip in parse_config_extension)

    # @allure.feature('realTime IP')
    # @allure.tag('smoke')
    # @allure.story('PBJ-4408 Realtime - Add IP to config extension in Bastion')
    # @allure.description('Verify ip doses not add to config extension when ip set as below:'
    #                     'realtime.hb_config = True, account = False')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # def test_config_ip_06(self, pub_app_id, sdk_v):
    #     """
    #     realtime.hb_config.ip_allowed = True
    #
    #     account.ip_allowed=False
    #     """
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_not_exist(response_payload, 'config_extension')

    @allure.story('disable reportAd')
    @allure.tag('basic')
    @allure.story('PBJ-4345 add flag to disable reportAd for eDSP')
    @allure.description('Verify no \'disable_report_ad\' field if no setting in MongoDB')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_disable_reportAd_01(self, pub_app_id, sdk_v, rtb_ids):
        '''

        No 'disable_report_ad' setting in MongoDB
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(response_payload, 'disable_report_ad')

    @allure.story('disable reportAd')
    @allure.tag('basic')
    @allure.story('PBJ-4345 add flag to disable reportAd for eDSP')
    @allure.description('Verify disable_report_ad=0 if disable_report_ad=0 in MongoDB')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.1'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_disable_reportAd_02(self, pub_app_id, sdk_v, rtb_ids):
        '''

        'disable_report_ad'=0 setting in MongoDB
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_report_ad')
        assert_that(isinstance(response_payload['disable_report_ad'], int))
        assert_that(response_payload['disable_report_ad'], equal_to(0))

    @allure.story('disable reportAd')
    @allure.tag('basic')
    @allure.story('PBJ-4345 add flag to disable reportAd for eDSP')
    @allure.description('Verify disable_report_ad=1 if disable_report_ad=1 in MongoDB')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_disable_reportAd_03(self, pub_app_id, sdk_v, rtb_ids):
        '''

        'disable_report_ad'=1 setting in MongoDB
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_report_ad')
        assert_that(isinstance(response_payload['disable_report_ad'], int))
        assert_that(response_payload['disable_report_ad'], equal_to(1))

    @allure.story('disable reportAd')
    @allure.tag('basic')
    @allure.story('PBJ-4345 add flag to disable reportAd for eDSP')
    @allure.description('Verify disable_report_ad=2 if disable_report_ad=2 in MongoDB')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.1'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_disable_reportAd_04(self, pub_app_id, sdk_v, rtb_ids):
        '''

        'disable_report_ad'=2 setting in MongoDB
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_report_ad')
        assert_that(isinstance(response_payload['disable_report_ad'], int))
        assert_that(response_payload['disable_report_ad'], equal_to(2))

    @allure.story('disable reportAd')
    @allure.tag('basic')
    @allure.story('PBJ-4345 add flag to disable reportAd for eDSP')
    @allure.description('Verify disable_report_ad=3 if disable_report_ad=3 in MongoDB')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_3])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.1'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_disable_reportAd_05(self, pub_app_id, sdk_v, rtb_ids):
        '''

        'disable_report_ad'=3 setting in MongoDB
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_report_ad')
        assert_that(isinstance(response_payload['disable_report_ad'], int))
        assert_that(response_payload['disable_report_ad'], equal_to(3))

    @allure.story('disable reportAd')
    @allure.tag('basic')
    @allure.story('PBJ-4345 add flag to disable reportAd for eDSP')
    @allure.description('Verify disable_report_ad=1 if disable_report_ad=4 in MongoDB')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_4])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.1'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_disable_reportAd_06(self, pub_app_id, sdk_v, rtb_ids):
        '''

        'disable_report_ad'=4 setting in MongoDB
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'disable_report_ad')
        assert_that(isinstance(response_payload['disable_report_ad'], int))
        assert_that(response_payload['disable_report_ad'], equal_to(0))

    @allure.story('disable reportAd')
    @allure.tag('basic')
    @allure.story('PBJ-4345 add flag to disable reportAd for eDSP')
    @allure.description('Verify not exist disable_report_ad if sdk version < 6.12')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.1'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_disable_reportAd_07(self, pub_app_id, sdk_v, rtb_ids):
        '''

        'disable_report_ad'=2 setting in MongoDB
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(response_payload, 'disable_report_ad')

    @allure.story('disable reportAd')
    @allure.tag('basic')
    @allure.story('PBJ-4345 add flag to disable reportAd for eDSP')
    @allure.description('Verify not exist disable_report_ad if sdk version > 7.0+')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0', 'Vungle/7.0.1'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_disable_reportAd_08(self, pub_app_id, sdk_v, rtb_ids):
        '''

        'disable_report_ad'=1 setting in MongoDB
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(response_payload, 'disable_report_ad')



    @allure.story('error logging')
    @allure.tag('basic', 'v0.129.0')
    @allure.story('PBJ-4618 Add support for logLevels for 7.0 SDK error logging')
    @allure.description('Verify bastion response loglevel=0 when:'
                        'global.log_metrics_global_config.log_level_global_switch=true,'
                        'app.error_log_level=0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_support_loglevel_01(self, pub_app_id, sdk_v, rtb_ids):
        """

        global: realtime.jaeger_config = {
                          "log_metrics_global_config":{
                           log_level_global_switch: true
                           metrics_global_switch: true

                        }
                }
        application: error_log_level:0
                     metrics_switch: true
        """
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'log_metrics')
        assert_that(response_payload['log_metrics']['error_log_level'], equal_to(0))
        assert_that(response_payload['log_metrics']['metrics_is_enabled'], equal_to(True))

    @allure.story('error logging')
    @allure.tag('basic', 'v0.129.0')
    @allure.story('PBJ-4618 Add support for logLevels for 7.0 SDK error logging')
    @allure.description('Verify bastion response loglevel=0 when:'
                        'global.log_metrics_global_config.log_level_global_switch=true,'
                        'without error log seting in app level')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_support_loglevel_02(self, pub_app_id, sdk_v, rtb_ids):
        """

        global: realtime.jaeger_config = {
                          "log_metrics_global_config":{
                           log_level_global_switch: true
                            metrics_global_switch: true
                        }
                }
        application: no setting
                     metrics_switch: false
        """
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'log_metrics')
        assert_that(response_payload['log_metrics']['error_log_level'], equal_to(1))
        assert_that(response_payload['log_metrics']['metrics_is_enabled'], equal_to(False))

    @allure.story('error logging')
    @allure.tag('basic', 'v0.129.0')
    @allure.story('PBJ-4618 Add support for logLevels for 7.0 SDK error logging')
    @allure.description('Verify bastion response loglevel=2 when:'
                        'global.log_metrics_global_config.log_level_global_switch=true,'
                        'app.error_log_level=2')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_support_loglevel_03(self, pub_app_id, sdk_v, rtb_ids):
        '''

        global: realtime.jaeger_config = {
                          "log_metrics_global_config":{
                           log_level_global_switch: true
                           metrics_global_switch: true
                        }
                }
        application: error_log_level:2
                     metrics_switch: no setting
        '''
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'log_metrics')
        assert_that(response_payload['log_metrics']['error_log_level'], equal_to(2))
        assert_that(response_payload['log_metrics']['metrics_is_enabled'], equal_to(True))

    # @allure.story('error logging')
    # @allure.tag('basic')
    # @allure.story('PBJ-4618 Add support for logLevels for 7.0 SDK error logging')
    # @allure.description('Verify bastion response loglevel=2 when:'
    #                     'global.log_metrics_global_config.log_level_global_switch=false,'
    #                     )
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_2, common_test_app, common_test_app_1])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    # @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    # def test_support_loglevel_04(self, pub_app_id, sdk_v, rtb_ids):
    #     '''
    #
    #     global: realtime.jaeger_config = {
    #                       "log_metrics_global_config":{
    #                        log_level_global_switch: fasle
    #                        metrics_global_switch: fasle
    #                     }
    #             }
    #     application: error_log_level:2/0/no setting
    #     '''
    #     req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload, 'log_metrics')
    #     assert_that(response_payload['log_metrics']['error_log_level'], equal_to(0))
    #     assert_that(response_payload['log_metrics']['metrics_is_enable'], equal_to(False))

    # @allure.story('Real Time Experiment')
    # @allure.tag('normal')
    # @allure.story('PBJ-4698 Realtime - Control ADO is on or off in experiment configure')
    # @allure.description('Verify the ad_load_optimization flag follows the config in experiment if the traffic enter '
    #                     'experiment')
    # @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620036b1'])
    # def test_realtime_experiment_ado_1(self, pub_app_id):
    #     '''
    #         experiment setting: "ado_enabled": true
    #         pub app setting: "ad_load_optimization_enabled": false
    #     '''
    #     req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(True))
    #
    # @allure.story('Real Time Experiment')
    # @allure.tag('normal')
    # @allure.story('PBJ-4698 Realtime - Control ADO is on or off in experiment configure')
    # @allure.description('Verify the ad_load_optimization flag follows the pub app setting if the traffic does not'
    #                     ' enter experiment')
    # @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620036b3'])
    # def test_realtime_experiment_ado_2(self, pub_app_id):
    #     '''
    #         experiment setting: "ado_enabled": true
    #         pub app setting: "ad_load_optimization_enabled": false
    #     '''
    #     req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(False))

    # @allure.story('Real Time Experiment')
    # @allure.tag('normal')
    # @allure.story('PBJ-4698 Realtime - Control ADO is on or off in experiment configure')
    # @allure.description('Verify the ad_load_optimization flag follows the pub app setting if the traffic enter '
    #                     'experiment but no ado setting in experiment')
    # @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620036b1'])
    # def test_realtime_experiment_ado_3(self, pub_app_id):
    #     '''
    #         no experiment level setting
    #         pub app setting: "ad_load_optimization_enabled": false
    #     '''
    #     req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
    #     r = post(config_v5_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=test_default_real_time_sdk_version, src_ip=au_ip))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_that(response_payload['ad_load_optimization']['enabled'], equal_to(False))

    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.tag('v0.130.0')
    @allure.story('PBJ-4679 SDK 7.0 - HB should always be pure realtime as no precache supported')
    @allure.description('Verify all hb placement will be realtime mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sdk_7_placement_type_01(self, pub_app_id):
        """

        placement db setting:
            max_hb_cache: 1
            hb_cache_type: "multi_cache"
        """
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/7.0.0'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'INTER-MREC-003':
                assert_that(placement_obj['max_hb_cache'], equal_to(0))

    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.tag('v0.130.0')
    @allure.story('PBJ-4679 SDK 7.0 - HB should always be pure realtime as no precache supported')
    @allure.description('Verify all hb placement will be realtime mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sdk_7_placement_type_02(self, pub_app_id):
        """

        placement db setting:
            max_hb_cache: 1
            hb_cache_type: "multi_cache"
        """
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.12.0'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'INTER-MREC-003':
                assert_that(placement_obj['max_hb_cache'], equal_to(1))

    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.tag('v0.130.0')
    @allure.story('PBJ-4669 add a feature flag for template heartbeat check')
    @allure.description('Verify heartbeat check flag return true')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sdk_7_heartbeat_check_01(self, pub_app_id):
        """
        realtime.jaeger_config setting:
        value.template.heartbeat_enabled":true
        application:
        heartbeat_check_enabled: true
        """
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/7.0.0'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload,'template')
        assert_keys_exist(response_payload['template'], 'heartbeat_check_enabled')
        assert_that(response_payload['template']['heartbeat_check_enabled'], equal_to(True))



    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.tag('v0.130.0')
    @allure.story('PBJ-4669 add a feature flag for template heartbeat check')
    @allure.description('Verify heartbeat check flag return false')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    def test_sdk_7_heartbeat_check_02(self, pub_app_id):
        """
        application:
        realtime.jaeger_config setting:
        value.template.heartbeat_enabled":true
        heartbeat_check_enabled: false
        """
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/7.0.0'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'template')
        assert_keys_exist(response_payload['template'], 'heartbeat_check_enabled')
        assert_that(response_payload['template']['heartbeat_check_enabled'], equal_to(False))



    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.tag('v0.130.0')
    @allure.story('PBJ-4669 add a feature flag for template heartbeat check')
    @allure.description('Verify heartbeat check flag default is false')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    def test_sdk_7_heartbeat_check_03(self, pub_app_id):
        """
        application:
        realtime.jaeger_config setting:
        value.template.heartbeat_enabled":true
         no heartbeat_check_enabled setting
        """
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/7.0.0'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'template')
        assert_keys_exist(response_payload['template'], 'heartbeat_check_enabled')
        assert_that(response_payload['template']['heartbeat_check_enabled'], equal_to(False))



    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.tag('')
    @allure.story('PBJ-4729 need to host mraid.js and omsdk js files on cdn')
    @allure.description('Verify two new endpoints are added for sdk 7.0+')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0', 'Vungle/7.0.1'])
    def test_sdk_7_0_1(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        endpoints = response_payload['endpoints']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(endpoints, 'mraid_js')
        assert_keys_exist(endpoints, 'omsdk_js')
        assert_that(endpoints['mraid_js'], equal_to('https://cdn-lb.vungle.com/mraid/4_9_1'))


    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.story('PBJ-4729 need to host mraid.js and omsdk js files on cdn')
    @allure.description('Verify no js endpoints below sdk 7.0+')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.6'])
    def test_sdk_7_0_2(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        endpoints = response_payload['endpoints']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(endpoints, 'mraid_js')
        assert_keys_not_exist(endpoints, 'omsdk_js')


    @allure.story('SDK 7.0')
    @allure.tag('basic')
    @allure.story('PBJ-4618 Add support for logLevels for 7.0 SDK error logging')
    @allure.description('Verify no log and metric below 7.0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast, non_test_mode_kraken_rtb_ids])
    def test_sdk_7_0_3(self, pub_app_id, sdk_v, rtb_ids):
        """

        global: realtime.jaeger_config = {
                          "log_metrics_global_config":{
                           log_level_global_switch: true
                           metrics_global_switch: true

                        }
                }
        application: error_log_level:0
                     metrics_switch: true
        """
        req = request_payload.config_v5_ios(pub_app_id, ifa=gen_device_id())
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=fr_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(response_payload, 'log_metrics')



    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.story('PBJ-4669 add a feature flag for template heartbeat check')
    @allure.description('Verify no heartbeat check flag below sdk< 7.0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    def test_sdk_0_4(self, pub_app_id, sdk_v):
        """
        realtime.jaeger_config setting:
        value.template.heartbeat_enabled":true
        application:
        heartbeat_check_enabled: true
        """
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_not_exist(response_payload, 'template')



    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.tag('basic', 'v0.131.0')
    @allure.story('PBJ-4714 Force RI feature if S2S rewarded callback enabled on SDK 7.0')
    @allure.description('Verify ri.enable=true for callbackURL is not empty')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    def test_force_ri_01(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        ri = response_payload['ri']
        assert_that(ri['enabled'], equal_to(True))

    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.tag('basic', 'v0.131.0')
    @allure.story('PBJ-4714 Force RI feature if S2S rewarded callback enabled on SDK 7.0')
    @allure.description('Verify ri.enable=false for callbackURL is not empty but sdk version<7.0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    def test_force_ri_02(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        ri = response_payload['ri']
        assert_that(ri['enabled'], equal_to(False))


    @allure.story('SDK 7.0')
    @allure.severity('smoke')
    @allure.tag('basic', 'v0.131.0')
    @allure.story('PBJ-4714 Force RI feature if S2S rewarded callback enabled on SDK 7.0')
    @allure.description('Verify ri.enable=false for callbackURL is empty')
    @pytest.mark.parametrize('pub_app_id', [android_common_coppa_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    def test_force_ri_03(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        ri = response_payload['ri']
        assert_that(ri['enabled'], equal_to(False))

    @allure.story('PBJ-5133 Add a feature flag for Clever Cache in config response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_clever_cache_ios(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'clever_cache')
        assert_that(response_payload['clever_cache']['enabled'], equal_to(True))
        assert_that(response_payload['clever_cache']['disk_size'], equal_to(1000))
        assert_that(response_payload['clever_cache']['disk_percentage'], equal_to(3))

    @allure.story('PBJ-5133 Add a feature flag for Clever Cache in config response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_clever_cache_android(self, pub_app_id):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'clever_cache')
        assert_that(response_payload['clever_cache']['enabled'], equal_to(True))
        assert_that(response_payload['clever_cache']['disk_size'], equal_to(1000))
        assert_that(response_payload['clever_cache']['disk_percentage'], equal_to(3))


    @allure.story('PBJ-5133 Add a feature flag for Clever Cache in config response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    def test_clever_cache_windows(self, pub_app_id):
        req = request_payload.config_v5_windows(pub_app_id, windows_common_test_placement)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload, 'clever_cache')
        assert_that(response_payload['clever_cache']['enabled'], equal_to(True))
        assert_that(response_payload['clever_cache']['disk_size'], equal_to(1000))
        assert_that(response_payload['clever_cache']['disk_percentage'], equal_to(3))