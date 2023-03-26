import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bflat')
class TestBflatBasic(object):
    
    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('basic')
    @allure.description('Verify the event id from bid response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_basic_info_1(self, pub_app_id, placement):
        event_id = '60477c0fcf9272000148c19b'
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, event_id=event_id)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(response_payload['event_id'], equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('basic')
    @allure.description('Verify the bid id from bid response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_basic_info_2(self, pub_app_id, placement):
        bidid = '82317317-7e72-4927-8a0f-28f4b9c41253'
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, bidid=bidid)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(response_payload['bidid'], equal_to(bidid))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('basic')
    @allure.description('Verify the bid price from bid response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_basic_info_3(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_keys_exist(response_payload, 'bid_price')
        assert_that(isinstance(response_payload['bid_price'], float) or isinstance(response_payload['bid_price'], int))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-4169 Pass campaign rate type to bflat')
    @allure.description('Verify the \'campaign_rate_type\' added in bid_request can work well')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_basic_info_4(self, pub_app_id, placement):
        event_id = '60477c0fcf9272000148c19b'
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, event_id=event_id,
                                                campaign_rate_type='install')
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(response_payload['event_id'], equal_to(event_id))

    @allure.feature('basic')
    @allure.tag('smoke', 'v0.25.0')
    @allure.story('Adding the request device os from bid request')
    @allure.description('Verify the request device os')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('os', ['unknown', 'iOS', 'android', 'amazon', 'windows'])
    def test_basic_device_os(self, pub_app_id, placement, os):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, os=os)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_keys_not_exist(response_payload['ds_ext'], 'fall_back')
        assert_that('error' not in response_payload)

    # @allure.feature('no bid')
    # @allure.tag('normal', 'v0.25.0')
    # @allure.story('Allowing the no bidding case on Bflat')
    # @allure.description('Verify the no bid reason from bid response')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement_id])
    # def test_nbr(self, pub_app_id, placement):
    #     req = request_payload.bflat_bid_request(pub_app_id, placement, experiment=90, adv_erpm=0.0000000000001)
    #     r = post(bflat_bid_request_endpoint_qa, json=req)
    #     response_payload = r.json()
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.bflat_bid_response)
    #     assert_that(response_payload['nbr'], equal_to(101))

    @allure.feature('bid price')
    @allure.tag('normal', 'v0.26.0')
    @allure.story('bid price')
    @allure.description('Verify the zero bid price situation')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_0_bid_price(self, pub_app_id, placement):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement,
                                                experiment='idsp_video_8', adv_erpm=0.0000000000001,
                                                nostr_bid_price=0.0000000000001)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(response_payload['bid_price'], equal_to(0.0))

    # @allure.feature('hb nrg override')
    # @allure.tag('normal', 'v0.33.0')
    # @allure.story('hb nrg override')
    # @allure.description('Verify the hb nrg override field from bid request')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement_id])
    # @pytest.mark.parametrize('experiment', bflat_disabled_experiment_list)
    # @pytest.mark.parametrize('hb_nrg_override', [None, 0.5, 1.0])
    # def test_hb_nrg_override_1(self, pub_app_id, placement, experiment, hb_nrg_override):
    #     req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, experiment=experiment,
    #                                             hb_nrg_override=hb_nrg_override)
    #     r = post(bflat_bid_request_endpoint_qa, json=req)
    #     response_payload = r.json()
    #     ds_ext = response_payload['ds_ext']
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.bflat_bid_response)
    #     assert_that(isinstance(ds_ext['experiment_number'], int))
    #     assert_keys_not_exist(ds_ext, 'fall_back')

    @allure.feature('hb nrg override')
    @allure.tag('normal', 'v0.33.0')
    @allure.story('hb nrg override')
    @allure.description('Verify the hb nrg override field from bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('experiment', get_specify_bflat_exp_list())
    @pytest.mark.parametrize('hb_nrg_override', [None, 0.5, 1.0])
    def test_hb_nrg_override_2(self, pub_app_id, placement, experiment, hb_nrg_override):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, experiment=experiment,
                                                hb_nrg_override=hb_nrg_override, imp_type='banner')
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(isinstance(ds_ext['experiment_number'], int))
        assert_keys_not_exist(ds_ext, 'fall_back')

    @allure.feature('bid request')
    @allure.tag('normal', 'v0.39.0')
    @allure.story('PBJ-3589 Add bidrequest_imp_type field to b-flat')
    @allure.description('Verify the bidrequest_imp_type can be parsed correctly')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('experiment', get_specify_bflat_exp_list('idsp', 'video'))
    def test_bidrequest_imp_type_video_1(self, pub_app_id, placement, experiment):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, experiment=experiment)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(isinstance(ds_ext['experiment_number'], int))
        assert_keys_not_exist(ds_ext, 'fall_back')

    @allure.feature('bid request')
    @allure.tag('normal', 'v0.39.0')
    @allure.story('PBJ-3589 Add bidrequest_imp_type field to b-flat')
    @allure.description('Verify the bidrequest_imp_type can be parsed correctly')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('experiment', get_specify_bflat_exp_list())
    def test_bidrequest_imp_type_banner_1(self, pub_app_id, placement, experiment):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, experiment=experiment,
                                                imp_type='banner')
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        ds_ext = response_payload['ds_ext']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_that(isinstance(ds_ext['experiment_number'], int))
        assert_keys_not_exist(ds_ext, 'fall_back')

    @allure.feature('bid request')
    @allure.tag('normal', 'v0.39.0')
    @allure.story('PBJ-3589 Add bidrequest_imp_type field to b-flat')
    @allure.description('Verify that the bidrequest_imp_type is a required field')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('experiment', get_specify_bflat_exp_list())
    @pytest.mark.parametrize('imp_type', [None])
    def test_bidrequest_imp_type_2(self, pub_app_id, placement, experiment, imp_type):
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, experiment=experiment,
                                                imp_type=imp_type)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        assert_response_status_code(r.status_code, 422)

        response_payload = r.json()
        assert_that('bidrequest_imp_type' in response_payload['detail'][0]['loc'])
        assert_that(response_payload['detail'][0]['msg'], equal_to('field required'))
        assert_that(response_payload['detail'][0]['type'], equal_to('value_error.missing'))

    @allure.feature('max bid price')
    @allure.tag('normal')
    @allure.story('PBJ-3752 [BFlat] Return max_bid_price to HBP')
    @allure.description('Verify the returned max_bid_price is equal to the request max bid price when request os is not'
                        'iOS')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('max_bid_price', [0, 0.05, 5, 400])
    @pytest.mark.parametrize('os', ['windows', 'android', 'amazon'])
    def test_max_bid_price_1(self, pub_app_id, placement, max_bid_price, os):
        event_id = '60477c0fcf9272000148c19b'
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, event_id=event_id,
                                                max_bid_price=max_bid_price, os=os)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        assert_that(response_payload['max_bid_price'], equal_to(max_bid_price))

    @allure.feature('max bid price')
    @allure.tag('normal')
    @allure.story('PBJ-3752 [BFlat] Return max_bid_price to HBP')
    @allure.description('Verify the returned max_bid_price is equal to the request max bid price  when request geo is '
                        'not USA')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('max_bid_price', [0, 0.05, 5, 400])
    @pytest.mark.parametrize('geo_country', ['Japan'])
    def test_max_bid_price_2(self, pub_app_id, placement, max_bid_price, geo_country):
        event_id = '60477c0fcf9272000148c19b'
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, event_id=event_id,
                                                max_bid_price=max_bid_price, country=geo_country, is_dynamic_rate=1)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        assert_that(response_payload['max_bid_price'], equal_to(max_bid_price))

    @allure.feature('max bid price')
    @allure.tag('normal')
    @allure.story('PBJ-3752 [BFlat] Return max_bid_price to HBP')
    @allure.description('Verify the returned max_bid_price is equal to the request max bid price  when request geo is '
                        'not USA and os is not ios')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('max_bid_price', [0, 0.05, 5, 400])
    @pytest.mark.parametrize('geo_country', ['Japan'])
    @pytest.mark.parametrize('os', ['windows', 'android', 'amazon'])
    def test_max_bid_price_3(self, pub_app_id, placement, max_bid_price, geo_country, os):
        event_id = '60477c0fcf9272000148c19b'
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, event_id=event_id,
                                                max_bid_price=max_bid_price, country=geo_country, os=os)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        assert_that(response_payload['max_bid_price'], equal_to(max_bid_price))

    @allure.feature('max bid price')
    @allure.tag('normal')
    @allure.story('PBJ-3752 [BFlat] Return max_bid_price to HBP')
    @allure.description('Verify the returned max_bid_price=300 when request os=ios and geo=USA')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    @pytest.mark.parametrize('max_bid_price', [0, 0.05, 5, 400])
    def test_max_bid_price_4(self, pub_app_id, placement, max_bid_price):
        event_id = '60477c0fcf9272000148c19b'
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, event_id=event_id,
                                                max_bid_price=max_bid_price)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()
        assert_that(response_payload['max_bid_price'], equal_to(300))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-3964 Propagate `datasci_tags` into hbp-notifications topic'
                  'PBJ-4218 K value is missing in bflat datasci tags field in idsp_transactions table')
    @allure.description('Verify the \'datasci_tags\' is added for idsp')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_datasci_tags_idsp(self, pub_app_id, placement):
        bidid = '82317317-7e72-4927-8a0f-28f4b9c41253'
        req = request_payload.bflat_bid_request(pub_app_id=pub_app_id, placement_id=placement, bidid=bidid)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_keys_exist(response_payload, 'bflat_datasci_tags')
        bflat_datasci_tags = str_to_json(response_payload['bflat_datasci_tags'])
        assert_that(isinstance(bflat_datasci_tags['bp'], float))
        assert_that(isinstance(bflat_datasci_tags['b'], str))
        assert_that(isinstance(bflat_datasci_tags['e'], int))
        assert_that(bflat_datasci_tags['dsp_t'], 'idsp')
        assert_that(isinstance(bflat_datasci_tags['ad_t'], str))
        assert_that(isinstance(bflat_datasci_tags['k'], float))

    @allure.feature('basic')
    @allure.tag('smoke')
    @allure.story('PBJ-3964 Propagate `datasci_tags` into hbp-notifications topic')
    @allure.description('Verify the \'datasci_tags\' is added for edsp')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_id])
    def test_datasci_tags_edsp(self, pub_app_id, placement):
        bidid = '82317317-7e72-4927-8a0f-28f4b9c41253'
        req = request_payload.bflat_bid_request(adv_is_internal=False, pub_app_id=pub_app_id, placement_id=placement,
                                                bidid=bidid)
        r = post(bflat_bid_request_endpoint_qa, json=req)
        response_payload = r.json()

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.bflat_bid_response)
        assert_keys_exist(response_payload, 'bflat_datasci_tags')
        bflat_datasci_tags = str_to_json(response_payload['bflat_datasci_tags'])
        assert_that(isinstance(bflat_datasci_tags['bp'], float))
        assert_that(isinstance(bflat_datasci_tags['b'], str))
        assert_that(isinstance(bflat_datasci_tags['e'], int))
        assert_that(bflat_datasci_tags['dsp_t'], 'edsp')

