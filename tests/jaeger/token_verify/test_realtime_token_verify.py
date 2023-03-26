import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import verify_real_time_token, encode_real_time_token, generate_real_time_token
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
@allure.feature('real-time token verify')
class TestRealtimeTokenVerify(object):

    @allure.feature('real-time token verify')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-2997 Token verify endpoint in QA')
    @allure.description('Verify the real-time token verify endpoint on QA')
    @allure.severity('normal')
    @pytest.mark.parametrize('token', [test_real_time_token])
    def test_token_verify_1(self, token):
        r = verify_real_time_token(token)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()

        assert_that(response_payload['token'], not equal_to(None))

    @allure.feature('real-time token verify')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-2997 Token verify endpoint in QA')
    @allure.description('Verify the real-time token verify endpoint on QA')
    @allure.severity('normal')
    @pytest.mark.parametrize('token', [None, ''])
    def test_token_verify_2(self, token):
        r = verify_real_time_token(token)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()

        assert_that('realtime token empty' in response_payload['err'])

    @allure.feature('real-time token verify')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-2997 Token verify endpoint in QA')
    @allure.description('Verify the real-time token verify endpoint on QA')
    @allure.severity('normal')
    @pytest.mark.parametrize('token', ['abc123'])
    def test_token_verify_3(self, token):
        r = verify_real_time_token(token)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()

        assert_that('realtime token format error' in response_payload['err'])

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 1 - Test for real-time ad token')
    @allure.description('Verify the generated real-time token if it is valid')
    @allure.severity('normal')
    def test_generated_real_time_token_1(self):
        test_ifa=gen_device_id()
        token_json = request_payload.real_time_token_json(token_device_id=test_ifa, token_ios_device_id=test_ifa,
                                                          token_android_device_id=test_ifa, token_app_set_id=test_ifa,
                                                          token_amazon_device_id=test_ifa, token_amazon_app_set_id=test_ifa,
                                                          token_windows_device_id=test_ifa)
        token = encode_real_time_token(token_json)
        r = verify_real_time_token(url_encoder(token))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()
        assert_that(response_payload['token'], equal_to(token_json))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 1 - Test for real-time ad token')
    @allure.description('Verify the generated real-time token if SDK version < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_generated_real_time_token_2(self, sdk_v):
        test_ifa = gen_device_id()
        token_json = request_payload.real_time_token_json(sdk_user_agent=sdk_v, token_device_id=test_ifa, token_ios_device_id=test_ifa,
                                                          token_android_device_id=test_ifa, token_app_set_id=test_ifa,
                                                          token_amazon_device_id=test_ifa, token_amazon_app_set_id=test_ifa,
                                                          token_windows_device_id=test_ifa)
        token = encode_real_time_token(token_json)
        r = verify_real_time_token(url_encoder(token))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()

        assert_that(response_payload['token'], equal_to(token_json))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 1 - Test for real-time ad token'
                  'PBJ-3508 [COPPA] read coppa flag from realtime token and process it with realtime case')
    @allure.description('Verify the generated real-time token if it is valid when is_coppa is true')
    @allure.severity('normal')
    def test_generated_real_time_token_3(self):
        test_ifa = gen_device_id()
        token_json = request_payload.real_time_token_json(is_coppa=True, token_device_id=test_ifa, token_ios_device_id=test_ifa,
                                                          token_android_device_id=test_ifa, token_app_set_id=test_ifa,
                                                          token_amazon_device_id=test_ifa, token_amazon_app_set_id=test_ifa,
                                                          token_windows_device_id=test_ifa)
        token = encode_real_time_token(token_json)

        r = verify_real_time_token(url_encoder(token))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()
        assert_that(response_payload['token'], equal_to(token_json))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 1 - Test for real-time ad token'
                  'PBJ-3508 [COPPA] read coppa flag from realtime token and process it with realtime case')
    @allure.description('Verify the generated real-time token if it is valid when is_coppa is false')
    @allure.severity('normal')
    def test_generated_real_time_token_4(self):
        test_ifa = gen_device_id()
        token_json = request_payload.real_time_token_json(is_coppa=False, token_device_id=test_ifa, token_ios_device_id=test_ifa,
                                                          token_android_device_id=test_ifa, token_app_set_id=test_ifa,
                                                          token_amazon_device_id=test_ifa, token_amazon_app_set_id=test_ifa,
                                                          token_windows_device_id=test_ifa)
        token = encode_real_time_token(token_json)

        r = verify_real_time_token(url_encoder(token))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()
        assert_that(response_payload['token'], equal_to(token_json))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 1 - Test for real-time ad token')
    @allure.description('Verify the generated real-time token from Jaeger end if it is valid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_generated_real_time_token_5(self, pub_app_id, placement):
        ordinal_view = 13
        data = generate_real_time_token(pub_app_id=pub_app_id, placement_ref_id=placement, ordinal_view=ordinal_view,
                                        test_device_id=gen_device_id())
        ads_response = data['ads_response']
        token = data['super_token_v3']
        r = verify_real_time_token(url_encoder(token))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()

        assert_that(response_payload['token']['request']['precached_tokens'][0],
                    equal_to(ads_response['ads'][0]['ad_markup']['bid_token']))
        assert_that(response_payload['token']['request']['ordinal_view'], equal_to(ordinal_view))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 1 - Test for real-time ad token')
    @allure.description('Verify the generated real-time token from Jaeger end if it is valid when is_coppa is True')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_generated_real_time_token_6(self, pub_app_id, placement):
        ordinal_view = 13
        data = generate_real_time_token(pub_app_id=pub_app_id, placement_ref_id=placement, ordinal_view=ordinal_view,
                                        test_device_id=gen_device_id(), coppa=True)
        ads_response = data['ads_response']
        r = verify_real_time_token(url_encoder(data['super_token_v3']))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()


        assert_that(response_payload['token']['request']['precached_tokens'][0],
                    equal_to(ads_response['ads'][0]['ad_markup']['bid_token']))
        assert_that(response_payload['token']['request']['ordinal_view'], equal_to(ordinal_view))
        assert_that(response_payload['token']['consent']['coppa']['is_coppa'], equal_to(True))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 1 - Test for real-time ad token')
    @allure.description('Verify the generated real-time token from Jaeger end if it is valid when is_coppa is False')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_generated_real_time_token_7(self, pub_app_id, placement):
        ordinal_view = 13
        data = generate_real_time_token(pub_app_id=pub_app_id, placement_ref_id=placement, ordinal_view=ordinal_view,
                                        test_device_id=gen_device_id(), coppa=False)
        ads_response = data['ads_response']
        r = verify_real_time_token(url_encoder(data['super_token_v3']))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()

        assert_that(response_payload['token']['request']['precached_tokens'][0],
                    equal_to(ads_response['ads'][0]['ad_markup']['bid_token']))
        assert_that(response_payload['token']['request']['ordinal_view'], equal_to(ordinal_view))
        assert_that(response_payload['token']['consent']['coppa']['is_coppa'], equal_to(False))

    @allure.feature('real-time ad')
    @allure.tag('normal')
    @allure.story('PBJ-3126 Real-time Ad Test - Req 1 - Test for real-time ad token')
    @allure.description('Verify the generated real-time token from Jaeger end if SDK version < 6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('coppa', [None, True, False])
    def test_generated_real_time_token_8(self, pub_app_id, placement, sdk_v, coppa):
        ordinal_view = 13
        data = generate_real_time_token(pub_app_id=pub_app_id, placement_ref_id=placement, ordinal_view=ordinal_view,
                                        test_device_id=gen_device_id(), sdk_v=sdk_v, coppa=coppa)
        ads_response = data['ads_response']
        r = verify_real_time_token(url_encoder(data['super_token_v3']))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.token_verify)
        response_payload = r.json()

        assert_that(response_payload['token']['request']['precached_tokens'][0],
                    equal_to(ads_response['ads'][0]['ad_markup']['bid_token']))
        assert_that(response_payload['token']['request']['ordinal_view'], equal_to(ordinal_view))
        if 'is_coppa' in response_payload['token']['consent']['coppa']:
            assert_that(response_payload['token']['consent']['coppa']['is_coppa'], equal_to(coppa))