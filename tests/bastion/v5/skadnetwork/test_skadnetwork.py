import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestSKAdNetwork(object):

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_v0.95.0')
    @allure.story('PBJ-1891 SKAdNetwork support - Bastion returns ad network id list')
    @allure.description('Test for Bastion can return the matched ad network id list')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sk_ad_network_ids_1(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        skadnetwork = response_payload['skadnetwork']
        assert_that(skadnetwork['matched_adnetwork_ids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_v0.95.0')
    @allure.story('PBJ-1891 SKAdNetwork support - Bastion returns ad network id list')
    @allure.description('Test for Bastion can not return the non-matched ad network id list')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sk_ad_network_ids_2(self, pub_app_id):
        network_ids = ["sdfasdfsdfsdfasdf", "654131654645", "test.ad.nw.001"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        skadnetwork = response_payload['skadnetwork']
        assert_that(skadnetwork['matched_adnetwork_ids'], equal_to(['test.ad.nw.001']))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_v0.95.0')
    @allure.story('PBJ-1891 SKAdNetwork support - Bastion returns ad network id list')
    @allure.description('Test for Bastion can not return the non-matched ad network id list')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sk_ad_network_ids_3(self, pub_app_id):
        network_ids = ["sdfasdfsdfsdfasdf", "654131654645"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        skadnetwork = response_payload['skadnetwork']
        assert_keys_not_exist(skadnetwork, 'matched_adnetwork_ids')

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_v0.95.0')
    @allure.story('PBJ-1891 SKAdNetwork support - Bastion returns ad network id list')
    @allure.description('Test for SDK does not pass the id list')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sk_ad_network_ids_4(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=None)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        skadnetwork = response_payload['skadnetwork']
        assert_keys_not_exist(skadnetwork, 'matched_adnetwork_ids')

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_v0.95.0')
    @allure.story('PBJ-1891 SKAdNetwork support - Bastion returns ad network id list')
    @allure.description('Test for Bastion can not return the ad network id list from disabled rtb')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sk_ad_network_ids_5(self, pub_app_id):
        network_ids = ["from.disabled.rtb", "test.ad.nw.001"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        skadnetwork = response_payload['skadnetwork']
        assert_that(skadnetwork['matched_adnetwork_ids'], equal_to(['test.ad.nw.001']))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_v0.95.0')
    @allure.story('PBJ-1891 SKAdNetwork support - Bastion returns ad network id list')
    @allure.description('Test for Bastion can return the ad network id list from non test mode Kraken rtb')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sk_ad_network_ids_6(self, pub_app_id):
        network_ids = ["non.test.mode.kraken"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        skadnetwork = response_payload['skadnetwork']
        assert_that(skadnetwork['matched_adnetwork_ids'], equal_to(['non.test.mode.kraken']))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_v0.95.0')
    @allure.story('PBJ-1891 SKAdNetwork support - Bastion returns ad network id list')
    @allure.description('Test for Bastion can not return the ad network id list from test mode rtb')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_sk_ad_network_ids_7(self, pub_app_id):
        network_ids = ["test.mode.kraken", "non.test.mode.kraken"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        skadnetwork = response_payload['skadnetwork']
        assert_that(skadnetwork['matched_adnetwork_ids'], equal_to(['non.test.mode.kraken']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v0.100.0')
    @allure.story('PBJ-2562 Bastion do AdNetworkID compare case insensitive and keep original case in response')
    @allure.description('Test for the skadnetwork id insensitivity')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_skadnetwork_id_insensitive(self, pub_app_id):
        '''
            In MongoDB: non.test.mode.kraken
        '''
        network_ids = ["test.mode.kraken", "non.TEST.mode.Kraken"]
        req = request_payload.config_v5_ios(pub_app_id, skadnetwork_ids=network_ids)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        skadnetwork = response_payload['skadnetwork']
        assert_that(skadnetwork['matched_adnetwork_ids'], equal_to(['non.TEST.mode.Kraken']))