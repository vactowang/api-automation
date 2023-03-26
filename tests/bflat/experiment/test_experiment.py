import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bflat')
class TestBflatExperiment(object):

    # @allure.feature('experiment')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3931 Separate bflat AB test config between video and banner traffic')
    # @allure.description('Verify for bflat works fine with serving by random specific experiment for video placement')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement_id])
    # @pytest.mark.parametrize('experiment', get_specify_bflat_exp_list('random'))
    # @pytest.mark.parametrize('adv_internal', [True, False])
    # def test_specific_experiment(self, pub_app_id, placement, experiment, adv_internal):
    #     req = request_payload.bflat_bid_request(adv_is_internal=adv_internal, pub_app_id=pub_app_id,
    #                                             placement_id=placement, experiment=experiment)
    #     r = post(bflat_bid_request_endpoint_qa, json=req)
    #     response_payload = r.json()
    #     ds_ext = response_payload['ds_ext']
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.bflat_bid_response)
    #     assert_that(isinstance(ds_ext['experiment_number'], int))
    #     assert_that(ds_ext['experiment_number'], equal_to(int(experiment.split('_')[1])))
    #     assert_that(ds_ext['dsp_type'], equal_to('invalid'))
    #     assert_that(ds_ext['ad_type'], equal_to('invalid'))
    #     assert_keys_not_exist(ds_ext, 'fall_back')
    #
    # @allure.feature('experiment')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3931 Separate bflat AB test config between video and banner traffic')
    # @allure.description('Verify for bflat works fine with serving by random specific experiment for banner placement')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_banner_placement_id])
    # @pytest.mark.parametrize('experiment', get_specify_bflat_exp_list('random'))
    # @pytest.mark.parametrize('adv_internal', [True, False])
    # def test_specific_experiment_banner(self, pub_app_id, placement, experiment, adv_internal):
    #     req = request_payload.bflat_bid_request(adv_is_internal=adv_internal, pub_app_id=pub_app_id,
    #                                             placement_id=placement, experiment=experiment, imp_type='banner')
    #     r = post(bflat_bid_request_endpoint_qa, json=req)
    #     response_payload = r.json()
    #     ds_ext = response_payload['ds_ext']
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.bflat_bid_response)
    #     assert_that(isinstance(ds_ext['experiment_number'], int))
    #     assert_that(ds_ext['experiment_number'], equal_to(int(experiment.split('_')[1])))
    #     assert_that(ds_ext['dsp_type'], equal_to('invalid'))
    #     assert_that(ds_ext['ad_type'], equal_to('invalid'))
    #     assert_keys_not_exist(ds_ext, 'fall_back')

    @allure.feature('experiment')
    @allure.tag('smoke')
    @allure.story('PBJ-3931 Separate bflat AB test config between video and banner traffic')
    @allure.description('Verify for bflat works fine with serving by idsp specific experiment for video placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('experiment', get_specify_bflat_exp_list('idsp', 'video'))
    def test_specific_experiment_idsp_video(self, pub_app_id, placement, experiment):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, experiment=experiment)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(isinstance(ds_ext['experiment_number'], int))
        assert_that(ds_ext['dsp_type'], equal_to('idsp'))
        assert_that(ds_ext['ad_type'], equal_to('video'))
        assert_keys_not_exist(ds_ext, 'fall_back')

    @allure.feature('experiment')
    @allure.tag('smoke')
    @allure.story('PBJ-3931 Separate bflat AB test config between video and banner traffic')
    @allure.description('Verify for bflat works fine with serving by idsp specific experiment for banner placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement_id])
    @pytest.mark.parametrize('experiment', get_specify_bflat_exp_list('idsp', 'banner'))
    def test_specific_experiment_idsp_banner(self, pub_app_id, placement, experiment):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, experiment=experiment,
                                                imp_type='banner')
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(isinstance(ds_ext['experiment_number'], int))
        assert_that(ds_ext['dsp_type'], equal_to('idsp'))
        assert_that(ds_ext['ad_type'], equal_to('banner'))
        assert_keys_not_exist(ds_ext, 'fall_back')

    @allure.feature('experiment')
    @allure.tag('smoke')
    @allure.story('PBJ-3931 Separate bflat AB test config between video and banner traffic')
    @allure.description('Verify for bflat works fine with serving by edsp specific experiment for video placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('experiment', get_specify_bflat_exp_list('edsp', 'video'))
    def test_specific_experiment_edsp_video(self, pub_app_id, placement, experiment):
        req = request_payload.bflat_bid_request(adv_is_internal=False, pub_app_id=pub_app_id, placement_id=placement,
                                                experiment=experiment)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(isinstance(ds_ext['experiment_number'], int))
        assert_that(ds_ext['dsp_type'], equal_to('edsp'))
        assert_that(ds_ext['ad_type'], equal_to('video'))
        assert_keys_not_exist(ds_ext, 'fall_back')

    @allure.feature('experiment')
    @allure.tag('smoke')
    @allure.story('PBJ-3931 Separate bflat AB test config between video and banner traffic')
    @allure.description('Verify for bflat works fine with serving by edsp specific experiment for video placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement_id])
    @pytest.mark.parametrize('experiment', get_specify_bflat_exp_list('edsp', 'banner'))
    def test_specific_experiment_edsp_banner(self, pub_app_id, placement, experiment):
        req = request_payload.bflat_bid_request(adv_is_internal=False, pub_app_id=pub_app_id, placement_id=placement,
                                                experiment=experiment, imp_type='banner')
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(isinstance(ds_ext['experiment_number'], int))
        assert_that(ds_ext['dsp_type'], equal_to('edsp'))
        assert_that(ds_ext['ad_type'], equal_to('banner'))
        assert_keys_not_exist(ds_ext, 'fall_back')

    @allure.feature('experiment')
    @allure.tag('smoke', 'v0.53.0')
    @allure.story('PBJ-4624 Test Bflat release v0.53.0')
    @allure.description('Verify the new added model for exp idsp video 12')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('experiment', ['idsp_video_12'])
    def test_experiment_idsp_video_new(self, pub_app_id, placement, experiment):
        req = request_payload.bflat_bid_request(adv_is_internal=True, pub_app_id=pub_app_id, placement_id=placement,
                                                experiment=experiment, imp_type='video', campaign_rate_type='install')
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(isinstance(ds_ext['experiment_number'], int))
        assert_that(ds_ext['dsp_type'], equal_to('idsp'))
        assert_that(ds_ext['ad_type'], equal_to('video'))
        assert_keys_not_exist(ds_ext, 'fall_back')
        assert_that(ds_ext['bidder'], equal_to('KaplanMeierWinnersCurseBidder'))


