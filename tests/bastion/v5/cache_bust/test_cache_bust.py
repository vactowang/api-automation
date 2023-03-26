import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestCacheBustBastion(object):

    @allure.feature('cache bust')
    @allure.tag('smoke', 'v0.98.0', 'test_mode')
    @allure.story('PBJ-2303 Bastion config support for cache bust')
    @allure.description('Verify the cache bust support on Bastion')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('vungle_v', ['5.7', '5.8'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0', 'Vungle/6.9.0'])
    def test_cache_bust_support_1(self, pub_app_id, vungle_v, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(vungle_version=vungle_v, sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        cache_bust = response_payload['cache_bust']
        assert_that(cache_bust['enabled'], equal_to(True))
        assert_that(cache_bust['interval'], equal_to(3600))

    @allure.feature('cache bust')
    @allure.tag('smoke', 'v0.98.0', 'test_mode')
    @allure.story('PBJ-2303 Bastion config support for cache bust')
    @allure.description('Verify the cache bust endpoint')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_cache_bust_support_2(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload['endpoints'], 'cache_bust')
        assert_that('/api/v5/cache_bust' in response_payload['endpoints']['cache_bust'])


    # @allure.feature('cache bust')
    # @allure.tag('smoke')
    # @allure.story('PBJ-4313 Set CacheBustEnabled by the settings rather than Jaeger toggle')
    # @allure.description('Verify the cache bust enabled = False when there is no cache bust process even it\'s'
    #                     'True in config map')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [mrec_test_app])
    # def test_cache_bust_toggle_01(self, pub_app_id):
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload['cache_bust'], 'enabled')
    #     assert_that(response_payload['cache_bust']['enabled'], equal_to(False))


    # @allure.feature('cache bust')
    # @allure.tag('smoke')
    # @allure.story('PBJ-4313 Set CacheBustEnabled by the settings rather than Jaeger toggle')
    # @allure.description('Verify the cache bust enabled = True when there is no cache bust process in cache_bust_pub '
    #                     'collection but has cache bust process in cache_bust_request process and it\'s'
    #                     'True in config map')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [mrec_test_app])
    # def test_cache_bust_toggle_01_e(self, pub_app_id):
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload['cache_bust'], 'enabled')
    #     assert_that(response_payload['cache_bust']['enabled'], equal_to(True))


    # @allure.feature('cache bust')
    # @allure.tag('smoke')
    # @allure.story('PBJ-4313 Set CacheBustEnabled by the settings rather than Jaeger toggle')
    # @allure.description('Verify the cache bust enabled = True when there is no cache bust process both '
    #                     'in cache_bust_pub collection and in cache_bust_request process and it\'s'
    #                     'True in config map')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # def test_cache_bust_toggle_01_e1(self, pub_app_id):
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #     assert_keys_exist(response_payload['cache_bust'], 'enabled')
    #     assert_that(response_payload['cache_bust']['enabled'], equal_to(False))


    @allure.feature('cache bust')
    @allure.tag('smoke')
    @allure.story('PBJ-4313 Set CacheBustEnabled by the settings rather than Jaeger toggle')
    @allure.description('Verify the cache bust enabled = True when there is  cache bust process and it\'s'
                        'True in condig map')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_cache_bust_toggle_02(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)
        assert_keys_exist(response_payload['cache_bust'], 'enabled')
        assert_that(response_payload['cache_bust']['enabled'], equal_to(True))


#
#     @allure.feature('cache bust')
#     @allure.tag('smoke', 'v0.98.0', 'test_mode')
#     @allure.story('PBJ-2304 Bastion cache bust support')
#     @allure.description('Verify the cache bust response info')
#     @allure.severity('smoke')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('last_cache_bust', [0, None])
#     def test_cache_bust_endpoint(self, pub_app_id, last_cache_bust):
#         req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
#         r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))
#
#         response_payload = r.json()
#         assert_response_status_code(r.status_code, HTTPStatus.OK)
#         assert_valid_schema(response_payload, response_schema.cache_bust)
#         assert_that(isinstance(response_payload['cache_bust']['last_updated'], int))
#         assert_that(isinstance(response_payload['cache_bust']['campaign_ids'], list))
#         assert_that(isinstance(response_payload['cache_bust']['creative_ids'], list))
#
#     @allure.feature('cache bust')
#     @allure.tag('normal', 'v0.98.0', 'test_mode')
#     @allure.story('PBJ-2304 Bastion cache bust support')
#     @allure.description('Verify the cache bust request with 0 or no last update time')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('last_cache_bust', [0, None])
#     def test_cache_bust_endpoint_1(self, pub_app_id, last_cache_bust):
#         req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
#         r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))
#
#         response_payload = r.json()
#         assert_response_status_code(r.status_code, HTTPStatus.OK)
#         assert_valid_schema(response_payload, response_schema.cache_bust)
#         assert_that(isinstance(response_payload['cache_bust']['last_updated'], int))
#         assert_that(isinstance(response_payload['cache_bust']['campaign_ids'], list))
#         if len(response_payload['cache_bust']['campaign_ids']) > 0:
#             assert_that(isinstance(response_payload['cache_bust']['campaign_ids'][0]['id'], str))
#             assert_that(isinstance(response_payload['cache_bust']['campaign_ids'][0]['timestamp_bust_end'], int))
#         assert_that(isinstance(response_payload['cache_bust']['creative_ids'], list))
#         if len(response_payload['cache_bust']['creative_ids']) > 0:
#             assert_that(isinstance(response_payload['cache_bust']['creative_ids'][0]['id'], str))
#             assert_that(isinstance(response_payload['cache_bust']['creative_ids'][0]['timestamp_bust_end'], int))
#
#     @allure.feature('cache bust')
#     @allure.tag('normal', 'v0.98.0', 'test_mode')
#     @allure.story('PBJ-2304 Bastion cache bust support')
#     @allure.description('Verify the cache bust request with last update time over the update time of all records')
#     @allure.severity('normal')
#     @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     @pytest.mark.parametrize('last_cache_bust', [4070908800])
#     def test_cache_bust_endpoint_2(self, pub_app_id, last_cache_bust):
#         '''
#         4070908800 is a time on 2099/01/01
#         '''
#         req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
#         r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))
#
#         response_payload = r.json()
#         assert_response_status_code(r.status_code, HTTPStatus.OK)
#         assert_valid_schema(response_payload, response_schema.cache_bust)
#         assert_that(len(response_payload['cache_bust']['campaign_ids']), equal_to(0))
#         assert_that(len(response_payload['cache_bust']['creative_ids']), equal_to(0))
#
#     # @allure.feature('cache bust')
#     # @allure.tag('normal', 'v0.98.0', 'test_mode')
#     # @allure.story('PBJ-2304 Bastion cache bust support')
#     # @allure.description('Verify the cache bust condition of data update time > last update time')
#     # @allure.severity('normal')
#     # @pytest.mark.parametrize('pub_app_id', [common_test_app])
#     # @pytest.mark.parametrize('last_cache_bust', [1615894807])
#     # def test_cache_bust_endpoint_3(self, pub_app_id, last_cache_bust):
#     #     '''
#     #     1615894807 is the middle time of these two data
#     #     '''
#     #     req = request_payload.cache_bust_ios(pub_app_id, last_cache_bust=last_cache_bust)
#     #     r = post(cache_bust_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.8'))
#     #
#     #     response_payload = r.json()
#     #     assert_response_status_code(r.status_code, HTTPStatus.OK)
#     #     assert_valid_schema(response_payload, response_schema.cache_bust)
#     #     assert_that(len(response_payload['cache_bust']['campaign_ids']), equal_to(0))
#     #     assert_that(len(response_payload['cache_bust']['creative_ids']), equal_to(1))