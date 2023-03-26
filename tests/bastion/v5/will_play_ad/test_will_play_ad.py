import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestWillPlayAd(object):

    @allure.feature('will play ad')
    @allure.tag('normal', 'v0.109.0')
    @allure.story('PBJ-3265 config returns will_play_ad enabled')
    @allure.description('Test for config must returns will play ad disable for SDK >= 6.5.0 with iOS app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.5.0', 'Vungle/6.5.1'])
    def test_will_play_ad_1(self, pub_app_id, sdk_v):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['will_play_ad']['enabled'], equal_to(False))

    @allure.feature('will play ad')
    @allure.tag('normal', 'v0.109.0')
    @allure.story('PBJ-3265 config returns will_play_ad enabled')
    @allure.description('Test for config must returns will play ad disable for SDK >= 6.5.0 with Android app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.5.0', 'Vungle/6.5.1'])
    def test_will_play_ad_2(self, pub_app_id, sdk_v):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['will_play_ad']['enabled'], equal_to(False))

    @allure.feature('will play ad')
    @allure.tag('normal', 'v0.109.0')
    @allure.story('PBJ-3265 config returns will_play_ad enabled')
    @allure.description('Test for config must returns will play ad disable for SDK >= 6.5.0 with Windows app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.5.0', 'Vungle/6.5.1'])
    def test_will_play_ad_3(self, pub_app_id, sdk_v):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['will_play_ad']['enabled'], equal_to(False))

    @allure.feature('will play ad')
    @allure.tag('normal', 'v0.109.0')
    @allure.story('PBJ-3265 config returns will_play_ad enabled')
    @allure.description('Test for config must returns will play ad disable for SDK >= 6.5.0 with Amazon app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.5.0', 'Vungle/6.5.1'])
    def test_will_play_ad_4(self, pub_app_id, sdk_v):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['will_play_ad']['enabled'], equal_to(False))

    @allure.feature('will play ad')
    @allure.tag('normal', 'v0.109.0')
    @allure.story('PBJ-3265 config returns will_play_ad enabled')
    @allure.description('Test for config must returns will play ad disable for SDK < 6.5.0 with iOS app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.9'])
    def test_will_play_ad_5(self, pub_app_id, sdk_v):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['will_play_ad']['enabled'], equal_to(True))

    @allure.feature('will play ad')
    @allure.tag('normal', 'v0.109.0')
    @allure.story('PBJ-3265 config returns will_play_ad enabled')
    @allure.description('Test for config must returns will play ad disable for SDK < 6.5.0 with Android app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.9'])
    def test_will_play_ad_6(self, pub_app_id, sdk_v):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['will_play_ad']['enabled'], equal_to(True))

    @allure.feature('will play ad')
    @allure.tag('normal', 'v0.109.0')
    @allure.story('PBJ-3265 config returns will_play_ad enabled')
    @allure.description('Test for config must returns will play ad disable for SDK < 6.5.0 with Windows app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.9'])
    def test_will_play_ad_7(self, pub_app_id, sdk_v):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['will_play_ad']['enabled'], equal_to(True))

    @allure.feature('will play ad')
    @allure.tag('normal', 'v0.109.0')
    @allure.story('PBJ-3265 config returns will_play_ad enabled')
    @allure.description('Test for config must returns will play ad disable for SDK < 6.5.0 with Amazon app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.4.9'])
    def test_will_play_ad_8(self, pub_app_id, sdk_v):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        assert_that(response_payload['will_play_ad']['enabled'], equal_to(True))