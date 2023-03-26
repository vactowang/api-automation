import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestGDPRConfig(object):

    @allure.feature('gdpr')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-2176 Disable the GDPR consent popup in X-Flow publisher on the Jaeger side')
    @allure.description('Verify gdpr status in case of account legitimate interest is false and gdpr delegate is false,'
                        'eu country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [gdpr_gdpr_delegate_f_legitimate_interest_f_app])
    def test_disable_gdpr_consent_popup_1(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=gb_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['gdpr']['is_country_data_protected'], equal_to(True))

    @allure.feature('gdpr')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-2176 Disable the GDPR consent popup in X-Flow publisher on the Jaeger side')
    @allure.description('Verify gdpr status in case of account legitimate interest is false and gdpr delegate is false,'
                        'non eu country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [gdpr_gdpr_delegate_f_legitimate_interest_f_app])
    def test_disable_gdpr_consent_popup_2(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['gdpr']['is_country_data_protected'], equal_to(False))

    @allure.feature('gdpr')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-2176 Disable the GDPR consent popup in X-Flow publisher on the Jaeger side')
    @allure.description('Verify gdpr status in case of account legitimate interest is true and no gdpr delegate,'
                        'eu country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [gdpr_gdpr_delegate_n_legitimate_interest_t_app])
    def test_disable_gdpr_consent_popup_3(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=gb_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['gdpr']['is_country_data_protected'], equal_to(False))

    @allure.feature('gdpr')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-2176 Disable the GDPR consent popup in X-Flow publisher on the Jaeger side')
    @allure.description('Verify gdpr status in case of account legitimate interest is true and no gdpr delegate,'
                        'non eu country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [gdpr_gdpr_delegate_n_legitimate_interest_t_app])
    def test_disable_gdpr_consent_popup_4(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['gdpr']['is_country_data_protected'], equal_to(False))

    @allure.feature('gdpr')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-2176 Disable the GDPR consent popup in X-Flow publisher on the Jaeger side')
    @allure.description('Verify gdpr status in case of account legitimate interest is false and gdpr delegate is true,'
                        'eu country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [gdpr_gdpr_delegate_t_legitimate_interest_f_app])
    def test_disable_gdpr_consent_popup_5(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=gb_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['gdpr']['is_country_data_protected'], equal_to(False))

    @allure.feature('gdpr')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-2176 Disable the GDPR consent popup in X-Flow publisher on the Jaeger side')
    @allure.description('Verify gdpr status in case of account legitimate interest is false and gdpr delegate is true,'
                        'non eu country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [gdpr_gdpr_delegate_t_legitimate_interest_f_app])
    def test_disable_gdpr_consent_popup_6(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['gdpr']['is_country_data_protected'], equal_to(False))

    @allure.feature('gdpr')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-2176 Disable the GDPR consent popup in X-Flow publisher on the Jaeger side')
    @allure.description('Verify gdpr status in case of account legitimate interest is true and gdpr delegate is true,'
                        'eu country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [gdpr_gdpr_delegate_t_legitimate_interest_t_app])
    def test_disable_gdpr_consent_popup_7(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=gb_ip))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['gdpr']['is_country_data_protected'], equal_to(False))

    @allure.feature('gdpr')
    @allure.tag('normal', 'R_0.97.0', 'test_mode')
    @allure.story('PBJ-2176 Disable the GDPR consent popup in X-Flow publisher on the Jaeger side')
    @allure.description('Verify gdpr status in case of account legitimate interest is true and gdpr delegate is true,'
                        'non eu country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [gdpr_gdpr_delegate_t_legitimate_interest_t_app])
    def test_disable_gdpr_consent_popup_8(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_that(response_payload['gdpr']['is_country_data_protected'], equal_to(False))