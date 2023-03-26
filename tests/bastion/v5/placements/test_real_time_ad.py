import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestRealTimeAd(object):

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.104.0')
    @allure.story('PBJ-3068 Bastion should return realtime settings in bastion response')
    @allure.description('Verify the max hb cache value should follow max_hb_rt_cache for multi_realtime type')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['REALTIME-FULLSCREEN'])
    def test_real_time_setting_1(self, pub_app_id, placement):
        '''
        Placement level setting:
            "is_hb_participation": true,
            "max_hb_cache": 1,
            "hb_cache_type": "multi_realtime",
            "max_hb_rt_cache": 4
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_that(placement_obj['max_hb_cache'], equal_to(4))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.104.0')
    @allure.story('PBJ-3068 Bastion should return realtime settings in bastion response')
    @allure.description('Verify the max hb cache value will not apply for non-hb placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['REALTIME-FULLSCREEN-2'])
    def test_real_time_setting_2(self, pub_app_id, placement):
        '''
        Placement level setting:
            "is_hb_participation": false,
            "max_hb_cache": 1,
            "hb_cache_type": "multi_realtime",
            "max_hb_rt_cache": 4
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_keys_not_exist(placement_obj, 'max_hb_cache')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.104.0')
    @allure.story('PBJ-3068 Bastion should return realtime settings in bastion response')
    @allure.description('Verify the max hb cache value will be 0 for realtime type placement via SDK >= 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['REALTIME-FULLSCREEN-1'])
    def test_real_time_setting_3(self, pub_app_id, placement):
        '''
        Placement level setting:
            "is_hb_participation": true,
            "max_hb_cache": 1,
            "hb_cache_type": "realtime",
            "max_hb_rt_cache": 4
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_that(placement_obj['max_hb_cache'], equal_to(0))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.104.0')
    @allure.story('PBJ-3068 Bastion should return realtime settings in bastion response')
    @allure.description('Verify that Bastion will handle the max value of max_hb_cache as 4')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['REALTIME-FULLSCREEN-3'])
    def test_real_time_setting_4(self, pub_app_id, placement):
        '''
        Placement level setting:
            "is_hb_participation": true,
            "max_hb_cache": 1,
            "hb_cache_type": "multi_realtime",
            "max_hb_rt_cache": 5
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_that(placement_obj['max_hb_cache'], equal_to(4))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.104.0')
    @allure.story('PBJ-3068 Bastion should return realtime settings in bastion response')
    @allure.description('Verify that Bastion side allows the value of max_hb_cache < 1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['REALTIME-FULLSCREEN-4'])
    def test_real_time_setting_5(self, pub_app_id, placement):
        '''
        Placement level setting:
            "is_hb_participation": true,
            "max_hb_cache": 1,
            "hb_cache_type": "multi_realtime",
            "max_hb_rt_cache": 0
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_that(placement_obj['max_hb_cache'], equal_to(0))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.104.0')
    @allure.story('PBJ-3068 Bastion should return realtime settings in bastion response')
    @allure.description('Verify the max hb cache value will be 1 if there is no max_hb_rt_cache setting on a hybrid'
                        'placement via SDK >= 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['REALTIME-FULLSCREEN-5'])
    def test_real_time_setting_6(self, pub_app_id, placement):
        '''
        Placement level setting:
            "is_hb_participation": true,
            "max_hb_cache": 2,
            "hb_cache_type": "multi_realtime"
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_that(placement_obj['max_hb_cache'], equal_to(1))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.106.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify the max hb cache value will not apply for the in-app bidding disabled app'
                        'via SDK version >= 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['IN_APP_BIDDING_DISABLED_VIDEO-2109348',
                                           'IN_APP_BIDDING_DISABLED_MREC-8321623',
                                           'IN_APP_BIDDING_DISABLED_BANNER-4616351'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_real_time_in_app_disabled_1(self, pub_app_id, placement, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_keys_not_exist(placement_obj, 'max_hb_cache')
                assert_keys_not_exist(placement_obj, 'header_bidding')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.106.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify the max hb cache value will not apply for the in-app bidding disabled app'
                        'via SDK version < 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['IN_APP_BIDDING_DISABLED_VIDEO-2109348',
                                           'IN_APP_BIDDING_DISABLED_MREC-8321623',
                                           'IN_APP_BIDDING_DISABLED_BANNER-4616351'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.9'])
    def test_real_time_in_app_disabled_2(self, pub_app_id, placement, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_keys_not_exist(placement_obj, 'max_hb_cache')
                assert_keys_not_exist(placement_obj, 'header_bidding')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.106.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify the max hb cache value will not apply for the in-app bidding disabled app'
                        'via SDK version <= 6.9.2')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['IN_APP_BIDDING_DISABLED_VIDEO-2109348',
                                           'IN_APP_BIDDING_DISABLED_MREC-8321623',
                                           'IN_APP_BIDDING_DISABLED_BANNER-4616351'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.2', 'Vungle/6.9.1'])
    def test_real_time_in_app_disabled_3(self, pub_app_id, placement, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_keys_not_exist(placement_obj, 'max_hb_cache')
                assert_keys_not_exist(placement_obj, 'header_bidding')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.106.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify the max hb cache value will not apply for the in-app bidding disabled app'
                        'via SDK version >= 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', ['IN_APP_BIDDING_DISABLED_VIDEO-8446105',
                                           'IN_APP_BIDDING_DISABLED_MREC-2612604',
                                           'IN_APP_BIDDING_DISABLED_BANNER-9471286'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_real_time_in_app_disabled_4(self, pub_app_id, placement, sdk_v):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_keys_not_exist(placement_obj, 'max_hb_cache')
                assert_keys_not_exist(placement_obj, 'header_bidding')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.106.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify the max hb cache value will not apply for the in-app bidding disabled app'
                        'via SDK version < 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', ['IN_APP_BIDDING_DISABLED_VIDEO-8446105',
                                           'IN_APP_BIDDING_DISABLED_MREC-2612604',
                                           'IN_APP_BIDDING_DISABLED_BANNER-9471286'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.9'])
    def test_real_time_in_app_disabled_5(self, pub_app_id, placement, sdk_v):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_keys_not_exist(placement_obj, 'max_hb_cache')
                assert_keys_not_exist(placement_obj, 'header_bidding')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.106.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify the max hb cache value will not apply for the in-app bidding disabled app'
                        'via SDK version <= 6.9.2')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', ['IN_APP_BIDDING_DISABLED_VIDEO-8446105',
                                           'IN_APP_BIDDING_DISABLED_MREC-2612604',
                                           'IN_APP_BIDDING_DISABLED_BANNER-9471286'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.2', 'Vungle/6.9.1'])
    def test_real_time_in_app_disabled_6(self, pub_app_id, placement, sdk_v):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_keys_not_exist(placement_obj, 'max_hb_cache')
                assert_keys_not_exist(placement_obj, 'header_bidding')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.107.0')
    @allure.story('PBJ-3200 Fix hb max cache response')
    @allure.description('Verify the max hb cache value will not be responded via SDK version <= 6.9.2')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement, common_test_hybrid_placement,
                                           common_test_pre_cache_placement, common_test_no_hb_cache_type_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.2', 'Vungle/6.9.1'])
    def test_hb_max_cache_response_1(self, pub_app_id, placement, sdk_v):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_keys_not_exist(placement_obj, 'max_hb_cache')

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.107.0')
    @allure.story('PBJ-3200 Fix hb max cache response')
    @allure.description('Verify the max hb cache value for hybrid placement via SDK version >= 6.10.1 or >= 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_hb_max_cache_response_2(self, pub_app_id, placement, sdk_v):
        '''
            max_hb_rt_cache = 4
        '''
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_that(placement_obj['max_hb_cache'], equal_to(4))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.107.0')
    @allure.story('PBJ-3200 Fix hb max cache response')
    @allure.description('Verify the max hb cache value for pre-cache placement via SDK version >= 6.10.1 or >= 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_hb_max_cache_response_3(self, pub_app_id, placement, sdk_v):
        '''
            max_hb_cache = 2
        '''
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_that(placement_obj['max_hb_cache'], equal_to(2))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.107.0')
    @allure.story('PBJ-3200 Fix hb max cache response')
    @allure.description('Verify the max hb cache value for the placement of no cache mode config '
                        'via SDK version >= 6.10.1 or >= 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_no_hb_cache_type_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_hb_max_cache_response_4(self, pub_app_id, placement, sdk_v):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_that(placement_obj['max_hb_cache'], equal_to(1))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.107.0')
    @allure.story('PBJ-3200 Fix hb max cache response')
    @allure.description('Verify the max hb cache value for real-time placement via SDK version >= 6.10.1 and < 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    def test_hb_max_cache_response_5(self, pub_app_id, placement, sdk_v):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_that(placement_obj['max_hb_cache'], equal_to(2))

    @allure.feature('real-time ad')
    @allure.tag('normal', 'v0.107.0')
    @allure.story('PBJ-3200 Fix hb max cache response')
    @allure.description('Verify the max hb cache value for real-time placement via SDK version >= 6.12.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0', 'Vungle/6.12.1'])
    def test_hb_max_cache_response_6(self, pub_app_id, placement, sdk_v):
        req = request_payload.config_v5_android(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == placement:
                assert_that(placement_obj['max_hb_cache'], equal_to(0))

