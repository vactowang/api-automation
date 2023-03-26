import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v5')
class TestPlacementConfig(object):

    @allure.feature('HBP')
    @allure.tag('smoke')
    @allure.story('PBJ-1330 HBP placement level config')
    @allure.description('Verify the placement config via is_hb_participation is true in placement level')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_placement_config_true(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'DEFAULT02021':
                assert_that(placement_obj['header_bidding'], equal_to(True))

    @allure.feature('HBP')
    @allure.tag('smoke')
    @allure.story('PBJ-1330 HBP placement level config')
    @allure.description('Verify the placement config via is_hb_participation is false in placement level')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_placement_config_false(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'AREYOUS82690':
                assert_keys_not_exist(placement_obj, 'header_bidding')

    @allure.feature('HBP')
    @allure.tag('smoke')
    @allure.story('PBJ-1330 HBP placement level config')
    @allure.description('Verify the placement config via is_hb_participation is null in placement level')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hbp_placement_config_null(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'HJKM6GM50919':
                assert_keys_not_exist(placement_obj, 'header_bidding')

    @allure.feature('HBP')
    @allure.tag('smoke')
    @allure.story('PBJ-1330 HBP placement level config')
    @allure.description('Verify the placement config via no is_hb_participation setting in placement level')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_no_hbp_placement_config(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == '0H90YVC08232':
                assert_keys_not_exist(placement_obj, 'header_bidding')

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.92.0')
    @allure.story('PBJ-1763 Stop reading placement level priority')
    @allure.description('Verify placement auto cache priority configuration does not work any more, '
                        'placement is not in appextensions but has setting in placement level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_placement_auto_cache_priority_config(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'DEFAULT02021':
                assert_keys_not_exist(placement_obj, 'cache_priority')

    @allure.feature('placement')
    @allure.tag('normal')
    @allure.story('support sequential download')
    @allure.description('Verify placement has no auto cache priority configuration')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_placement_no_auto_cache_priority_config(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'HJKM6GM50919':
                assert_keys_not_exist(placement_obj, 'cache_priority')

    @allure.feature('placement')
    @allure.tag('normal')
    @allure.story('support sequential download')
    @allure.description('Verify auto cache priority set as null in placement level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_placement_auto_cache_priority_config_null(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == '0H90YVC08232':
                assert_keys_not_exist(placement_obj, 'cache_priority')

    @allure.feature('banner')
    @allure.tag('normal', 'R_v0.88.0')
    @allure.story('PBJ-1362 filter out banner placement')
    @allure.description('Verify filtering out banner placement in case of vungle version below 5.4')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_filter_out_banner(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(vungle_version='5.3.9'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        flag = 0
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'BANNER-TEST-01':
                flag = 1
        assert_that(flag, equal_to(0))

    @allure.feature('banner')
    @allure.tag('normal', 'R_v0.88.0')
    @allure.story('PBJ-1362 filter out banner placement')
    @allure.description('Verify it does not filter out banner placement in case of vungle version above or equal 5.4')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('vungle_ver', ['5.4', '5.4.0', '5.4.1'])
    def test_not_filter_out_banner(self, pub_app_id, vungle_ver):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(vungle_version=vungle_ver))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        flag = 0
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'BANNER-TEST-01':
                flag = 1
                assert_that('banner' in placement_obj['supported_template_types'])
        assert_that(flag, equal_to(1))

    # @allure.feature('auto cache')
    # @allure.tag('normal', 'test_mode', 'R_v0.90.0')
    # @allure.story('PBJ-1658 AutoCache A/B testing experiment')
    # @allure.description('Verify for the auto cache A/B testing experiment')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # def test_auto_cache_ab_testing_match_experiment(self, pub_app_id):
    #     '''
    #
    #     Experiments:
    #
    #     {
    #         "name": "AutoCache - always false",
    #         "mutual_id": "5ee1b9760dac7b0d8cd89266",
    #         "allocate_strategy": "hash_device_id",
    #         "salt": "08ef8664e4f1f4be68b9ab7652ec0a092cad3203ccaa32cf8e42b72e57a53ade",
    #         "countries": ["RU"],
    #         "is_all_countries": false,
    #         "is_all_applications": false,
    #         "traffic_percentage": 10000,
    #         "scope": "jaeger",
    #         "start_date": {
    #             "$date": "2019-03-01T00:00:00.000Z"
    #         },
    #         "end_date": {
    #             "$date": "2099-12-31T23:59:59.999Z"
    #         },
    #         "app_whitelist": ["59786bc2a43b3a08620026b1"],
    #         "enabled": true,
    #         "buckets": [{
    #             "name": "Disable AutoCache",
    #             "weight": 100,
    #             "ext": {
    #                 "is_auto_cache": false
    #             }
    #         }, {
    #             "name": "AutoCache",
    #             "weight": 0,
    #             "ext": {
    #                 "is_auto_cache": true
    #             }
    #         }],
    #         "placement_whitelist": []
    #     }
    #     '''
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=ru_ip, vungle_version='5.3'))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #
    #     placements = response_payload['placements']
    #     for placement_obj in placements:
    #         if placement_obj['reference_id'] == 'DEFAULT02021':
    #             assert_that(placement_obj['is_auto_cached'], equal_to(False))

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.90.0')
    @allure.story('PBJ-1658 AutoCache A/B testing experiment')
    @allure.description('Verify for not matching the auto cache A/B testing experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_auto_cache_ab_testing_not_match_experiment(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=gb_ip, vungle_version='5.3'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'DEFAULT02021':
                assert_that(placement_obj['is_auto_cached'], equal_to(True))

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.90.0')
    @allure.story('PBJ-1658 AutoCache A/B testing experiment')
    @allure.description('Verify the auto cache A/B testing experiment will not serve for vungle version < 5.3')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_auto_cache_ab_testing_experiment_not_serve(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=ru_ip, vungle_version='5.2'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'DEFAULT02021':
                assert_that(placement_obj['is_auto_cached'], equal_to(True))

    # @allure.feature('auto cache')
    # @allure.tag('normal', 'test_mode', 'R_v0.91.0')
    # @allure.story('PBJ-1679 Always run auto cache experiment no mater it is auto cache enabled or not')
    # @allure.description('Verify for the auto cache A/B testing experiment on auto cache disabled placement')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # def test_auto_cache_disabled_placement_ab_testing_match_experiment(self, pub_app_id):
    #     '''
    #
    #     Experiments:
    #
    #     {
    #         "name": "AutoCache - always true",
    #         "mutual_id": "5ee1b9760dac7b0d8cd89266",
    #         "allocate_strategy": "hash_device_id",
    #         "salt": "08ef8664e4f1f4be68b9ab7652ec0a092cad3203ccaa32cf8e42b72e57a53ade",
    #         "countries": ["KR"],
    #         "is_all_countries": false,
    #         "is_all_applications": false,
    #         "traffic_percentage": 10000,
    #         "scope": "jaeger",
    #         "start_date": {...},
    #         "end_date": {...},
    #         "app_whitelist": ["59786bc2a43b3a08620026b1"],
    #         "enabled": true,
    #         "buckets": [{
    #             "name": "Disable AutoCache",
    #             "weight": 0,
    #             "ext": {
    #                 "is_auto_cache": false
    #             }
    #         }, {
    #             "name": "AutoCache",
    #             "weight": 100,
    #             "ext": {
    #                 "is_auto_cache": true
    #             }
    #         }],
    #         "placement_whitelist": []
    #     }
    #
    #     '''
    #     req = request_payload.config_v5_ios(pub_app_id)
    #     r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=kr_ip, vungle_version='5.3'))
    #
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(response_payload, response_schema.config_v5)
    #
    #     placements = response_payload['placements']
    #     for placement_obj in placements:
    #         if placement_obj['reference_id'] == 'AREYOUS82690':
    #             assert_that(placement_obj['is_auto_cached'], equal_to(True))

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.91.0')
    @allure.story('PBJ-1679 Always run auto cache experiment no mater it is auto cache enabled or not')
    @allure.description(
        'Verify for not matching the auto cache A/B testing experiment on auto cache disabled placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_auto_cache_disabled_placement_ab_testing_not_match_experiment(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=gb_ip, vungle_version='5.3'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'AREYOUS82690':
                assert_that(placement_obj['is_auto_cached'], equal_to(False))

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.91.0')
    @allure.story('PBJ-1679 Always run auto cache experiment no mater it is auto cache enabled or not')
    @allure.description('Verify the auto cache A/B testing experiment will not serve '
                        'for vungle version < 5.3 on auto cache disabled placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_auto_cache_disabled_placement_ab_testing_experiment_not_serve(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=kr_ip, vungle_version='5.2'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'AREYOUS82690':
                assert_that(placement_obj['is_auto_cached'], equal_to(False))

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.92.0')
    @allure.story('PBJ-1748 Cache priority mongoDB change, PBJ-1763 Stop reading placement level priority')
    @allure.description('Verify placement auto cache priority - '
                        'placement not in appextensions but has setting in placement level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_placement_auto_cache_priority_placement_not_in_appextensions(self, pub_app_id):
        '''
        Placement level setting:

        "auto_cache_priority": 1
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'DEFAULT02021':
                assert_keys_not_exist(placement_obj, 'cache_priority')

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.92.0')
    @allure.story('PBJ-1748 Cache priority mongoDB change')
    @allure.description('Verify placement auto cache priority - placement in appextensions')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_placement_auto_cache_priority_placement_in_appextensions(self, pub_app_id):
        '''
        Placement level setting:
        "auto_cache_priority": 3

        Index in placements_priority of appextensions: 0
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'AREYOUS82690':
                assert_that(placement_obj['cache_priority'], equal_to(1))

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.92.0')
    @allure.story('PBJ-1748 Cache priority mongoDB change')
    @allure.description('Verify placement auto cache priority - '
                        'placement in appextensions but no placement level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_placement_auto_cache_priority_placement_in_appextensions_no_placement_setting(self, pub_app_id):
        '''
        Index in placements_priority of appextensions: 1
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'HJKM6GM50918':
                assert_that(placement_obj['cache_priority'], equal_to(2))

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.92.0')
    @allure.story('PBJ-1748 Cache priority mongoDB change')
    @allure.description('Verify placement auto cache priority - '
                        'placement not in appextensions and no placement level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_placement_auto_cache_priority_placement_not_in_appextensions_no_placement_setting(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'HJKM6GM50919':
                assert_keys_not_exist(placement_obj, 'cache_priority')

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.92.0')
    @allure.story('PBJ-1748 Cache priority mongoDB change, PBJ-1763 Stop reading placement level priority')
    @allure.description('Verify placement auto cache priority - '
                        'no placements_priority array in appextensions for the app but has setting in placement level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5d4be99434c2bc00181da7f3'])
    def test_placement_auto_cache_priority_no_placements_priority(self, pub_app_id):
        '''
        Placement level setting:
        "auto_cache_priority": 2
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'DEFAULT-9424312':
                assert_keys_not_exist(placement_obj, 'cache_priority')

    @allure.feature('auto cache')
    @allure.tag('normal', 'test_mode', 'R_v0.92.0')
    @allure.story('PBJ-1748 Cache priority mongoDB change, PBJ-1763 Stop reading placement level priority')
    @allure.description('Verify placement auto cache priority - '
                        'no document in appextensions for the app but has setting in placement level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5e57a3a6130de800018aca0d'])
    def test_placement_auto_cache_priority_no_appextensions_doc(self, pub_app_id):
        '''
        Placement level setting:
        "auto_cache_priority": 1
        '''
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'DEFAULT-6818423':
                assert_keys_not_exist(placement_obj, 'cache_priority')

    @allure.feature('header bidding support')
    @allure.tag('normal', 'v0.99.0')
    @allure.story('PBJ-2447 Support default size for banners for hb')
    @allure.description('Verify the default size for hb banner from placement config')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hb_banner_size_1(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'BANNER-TEST-03':
                assert_that(placement_obj['ad_size'], 'banner')

    @allure.feature('header bidding support')
    @allure.tag('normal', 'v0.99.0')
    @allure.story('PBJ-2447 Support default size for banners for hb')
    @allure.description('Verify the default size for non-hb banner from placement config')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_hb_banner_size_2(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'EMILY_BANNER_THIRD_PARTY-0959887':
                assert_keys_not_exist(placement_obj, 'ad_size')

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('native placement')
    @allure.description('Verify the template type and ad format for native type placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_bastion_native_type_1(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == common_test_native_placement:
                assert_that(placement_obj['supported_template_types'], equal_to(['native']))
                assert_that(placement_obj['supported_ad_formats'], equal_to(['vungle_mraid', 'third_party']))

    @allure.feature('native placement')
    @allure.tag('normal')
    @allure.story('native placement')
    @allure.description('Verify the template type and ad format for the third party only native type placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_bastion_native_type_2(self, pub_app_id):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        for placement_obj in placements:
            if placement_obj['reference_id'] == 'NATIVE-002':
                assert_that(placement_obj['supported_template_types'], equal_to(['native']))
                assert_that(placement_obj['supported_ad_formats'], equal_to(['third_party']))

    @allure.feature('native placement')
    @allure.tag('normal', 'v0.108.0')
    @allure.story('PBJ-3195 Check SDK version for Native placement in config request')
    @allure.description('Verify the native type placement will not be returned if SDK < 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', [test_default_multi_cache_sdk_version, test_default_sdk_version])
    def test_bastion_native_type_3(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        native_existing_flag = False
        for placement_obj in placements:
            if placement_obj['reference_id'] == common_test_native_placement:
                native_existing_flag = True
        assert_that(native_existing_flag, equal_to(False))

    @allure.feature('native placement')
    @allure.tag('normal', 'v0.108.0')
    @allure.story('PBJ-3195 Check SDK version for Native placement in config request')
    @allure.description('Verify the native type placement will not be returned if SDK >= 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version, 'Vungle/6.11.1'])
    def test_bastion_native_type_4(self, pub_app_id, sdk_v):
        req = request_payload.config_v5_ios(pub_app_id)
        r = post(config_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(response_payload, response_schema.config_v5)

        placements = response_payload['placements']
        native_existing_flag = False
        for placement_obj in placements:
            if placement_obj['reference_id'] == common_test_native_placement:
                native_existing_flag = True
        assert_that(native_existing_flag, equal_to(True))