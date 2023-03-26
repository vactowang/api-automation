import pytest
import allure

from http import HTTPStatus

from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('Scrat Notifications')
class TestScratTimeoutNotification(object):

    @allure.feature('scrat notifications')
    @allure.tag('smoke', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the timeout url normal response')
    @allure.severity('smoke')
    def test_scrat_timout_url_normal_response(self):
        r_url = get(scrat_timeout_endpoint_qa.replace('${AUCTION_ID}', 'abcd1234').replace('${AUCTION_LOSS}', '1234'))
        assert_response_status_code(r_url.status_code, HTTPStatus.OK)
        response_payload_url = r_url.json()
        assert_that(response_payload_url['msg'], equal_to('ok'))
        assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the timeout url response with empty auction id value')
    @allure.severity('normal')
    def test_scrat_timout_url_response_empty_auction_id(self):
        r_url = get(scrat_timeout_endpoint_qa.replace('${AUCTION_ID}', '').replace('${AUCTION_LOSS}', '1234'))
        assert_response_status_code(r_url.status_code, HTTPStatus.OK)
        response_payload_url = r_url.json()
        assert_that(response_payload_url['msg'], equal_to('ok'))
        assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the timeout url response with empty auction id value')
    @allure.severity('normal')
    def test_scrat_timout_url_response_empty_loss_reason(self):
        r_url = get(scrat_timeout_endpoint_qa.replace('${AUCTION_ID}', 'abcd1234').replace('${AUCTION_LOSS}', ''))
        assert_response_status_code(r_url.status_code, HTTPStatus.OK)
        response_payload_url = r_url.json()
        assert_that(response_payload_url['msg'], equal_to('ok'))
        assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('scrat notifications')
    @allure.tag('normal', 'v0.123.0')
    @allure.story('PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the timeout url error response, invalid loss reason value')
    @allure.severity('normal')
    @pytest.mark.parametrize('param', ['${AUCTION_LOSS}', 'abcdefg123', ' '])
    def test_scrat_timout_url_error_response(self, param):
        r_url = get(scrat_timeout_endpoint_qa.replace('${AUCTION_ID}', 'abcd1234').replace('${AUCTION_LOSS}', param))
        assert_response_status_code(r_url.status_code, HTTPStatus.OK)