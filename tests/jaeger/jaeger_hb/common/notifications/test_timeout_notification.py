import pytest
import allure

from http import HTTPStatus

from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('HBP Notifications')
class TestTimeoutNotification(object):

    @allure.feature('hbp notifications')
    @allure.tag('smoke', 'v0.50.0')
    @allure.story('PBJ-2834 Prepare a bURL and a timeout notification URL for TopOn'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the timeout url normal response')
    @allure.severity('smoke')
    def test_timout_url_normal_response(self):
        timeout_url = hbp_timeout_url

        r_url = get(timeout_url.replace('${AUCTION_ID}', 'abcd1234').replace('${AUCTION_LOSS}', '1234'))
        assert_response_status_code(r_url.status_code, HTTPStatus.OK)
        response_payload_url = r_url.json()
        assert_that(response_payload_url['msg'], equal_to('ok'))
        assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'v0.50.0')
    @allure.story('PBJ-2834 Prepare a bURL and a timeout notification URL for TopOn'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the timeout url response with empty auction id value')
    @allure.severity('normal')
    def test_timout_url_response_empty_auction_id(self):
        timout_url = hbp_timeout_url

        r_url = get(timout_url.replace('${AUCTION_ID}', '').replace('${AUCTION_LOSS}', '1234'))
        assert_response_status_code(r_url.status_code, HTTPStatus.OK)
        response_payload_url = r_url.json()
        assert_that(response_payload_url['msg'], equal_to('ok'))
        assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'v0.50.0')
    @allure.story('PBJ-2834 Prepare a bURL and a timeout notification URL for TopOn'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the timeout url response with empty auction id value')
    @allure.severity('normal')
    def test_timout_url_response_empty_loss_reason(self):
        timout_url = hbp_timeout_url

        r_url = get(timout_url.replace('${AUCTION_ID}', 'abcd1234').replace('${AUCTION_LOSS}', ''))
        assert_response_status_code(r_url.status_code, HTTPStatus.OK)
        response_payload_url = r_url.json()
        assert_that(response_payload_url['msg'], equal_to('ok'))
        assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'R_v0.34.0')
    @allure.story('PBJ-2192 HBP notification urls when no settlement price'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the timeout url error response, invalid loss reason value')
    @allure.severity('normal')
    @pytest.mark.parametrize('param', ['${AUCTION_LOSS}', 'abcdefg123', ' '])
    def test_timout_url_error_response(self, param):
        timout_url = hbp_timeout_url

        r_url = get(timout_url.replace('${AUCTION_ID}', 'abcd1234').replace('${AUCTION_LOSS}', param))
        assert_response_status_code(r_url.status_code, HTTPStatus.OK)