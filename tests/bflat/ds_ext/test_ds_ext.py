import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bflat_exp_list
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bflat')
class TestBflatDSExtention(object):

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the margin from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_1(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_keys_exist(ds_ext, 'margin')
        assert_that(isinstance(ds_ext['margin'], float))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the erpm from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_2(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        if 'erpm' in ds_ext:
            assert_that(isinstance(ds_ext['erpm'], float))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the margin target from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_3(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        if 'margin_target' in ds_ext:
            assert_that(isinstance(ds_ext['margin_target'], float))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the bid price from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_4(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_keys_exist(ds_ext, '_bid_price')
        assert_that(isinstance(ds_ext['_bid_price'], float) or isinstance(ds_ext['_bid_price'], int))
        assert_that(ds_ext['_bid_price'], equal_to(response_payload['bid_price']))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the create date time from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_5(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_keys_exist(ds_ext, 'create_datetime')
        assert_that(isinstance(ds_ext['create_datetime'], str))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the bidder name from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_6(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_keys_exist(ds_ext, 'bidder')
        assert_that(isinstance(ds_ext['bidder'], str))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the bflat server version from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_7(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_keys_exist(ds_ext, 'bflat_version')
        assert_that(isinstance(ds_ext['bflat_version'], str))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the served experiment from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_8(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(isinstance(ds_ext['experiment_number'], int))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the served experiment weigh from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_9(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_keys_exist(ds_ext, 'weight')
        assert_that(isinstance(ds_ext['weight'], int))
        assert_that(ds_ext['weight'], greater_than(0))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the params from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_10(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        if 'user_override' in ds_ext:
            assert_that(isinstance(ds_ext['user_override'], float))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the params from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_11(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        if 'nostr_bid' in ds_ext:
            assert_that(isinstance(ds_ext['nostr_bid'], float))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the params from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_12(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        if 'win_rate_pred' in ds_ext:
            assert_that(isinstance(ds_ext['win_rate_pred'], float))

    @allure.feature('ds_ext')
    @allure.tag('smoke')
    @allure.story('de_ext')
    @allure.description('Verify the params from bid response ds_ext')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_ds_extbasic_info_13(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        if 'k' in ds_ext:
            assert_that(isinstance(ds_ext['k'], float))

    @allure.feature('ngr overrides')
    @allure.tag('normal', 'v0.34.0')
    @allure.story('ngr overrides')
    @allure.description('Verify the default hb ngr will be used for the country not in geo config list')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_nrg_overrides_1(self, pub_app_id, placement):
        '''
            "default_hb_nrg": 0.99
            "geo_configs": {
                "US": {
                    "hb_nrg": 1.03
                },
                "JP": {
                    "hb_nrg": 0.98
                }
            },
        '''
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement,
                                                experiment='idsp_video_8', country='CHN')
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(ds_ext['user_override'], equal_to(0.99))

    @allure.feature('ngr overrides')
    @allure.tag('normal', 'v0.34.0')
    @allure.story('ngr overrides')
    @allure.description('Verify the country hb ngr will be used for the country not in geo config list')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_nrg_overrides_2(self, pub_app_id, placement):
        '''
            "default_hb_nrg": 0.99
            "geo_configs": {
                "US": {
                    "hb_nrg": 1.03
                },
                "JP": {
                    "hb_nrg": 0.98
                }
            },
        '''
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement,
                                                experiment='idsp_video_8', country='JPN')
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(ds_ext['user_override'], equal_to(0.98))

    @allure.feature('ngr overrides')
    @allure.tag('normal', 'v0.34.0')
    @allure.story('ngr overrides')
    @allure.description('Verify the global hb ngr value will be used if there is not setting on placement level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['5988205b4bd6652569001072'])
    def test_nrg_overrides_3(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement,
                                                experiment='idsp_video_8')
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(ds_ext['user_override'], equal_to(1))