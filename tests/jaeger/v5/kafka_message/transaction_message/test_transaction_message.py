import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain, request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain, get_ext_debug_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
@allure.feature('message')
@allure.feature('hb-transaction')
class TestHBTransactionMessage(object):

    @allure.tag('hb_transaction ')
    @allure.story('normal',)
    @allure.story('PBJ-5236 Help investigate Outfit 7 bidrate being 100% on multiple apps')
    @allure.description('Verify pub_app_object_id is added to hb transaction')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_pub_app_id_to_hb_transaction_i(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=meister_rtb_ids)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            response_payload = info['hbp_response']
            debug = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
            assert_keys_exist(debug, 'pub_app_object_id')
            assert_that(debug['pub_app_object_id'], equal_to(debug['pub_app_id']))