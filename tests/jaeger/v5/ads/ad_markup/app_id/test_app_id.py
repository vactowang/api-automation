import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
@allure.feature('basic')
class TestAppId(object):

    @allure.tag('basic', 'smoke')
    @allure.story('app id')
    @allure.description('Verify app id string from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_app_id(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(str(ad_markup['app_id']).count('app_id'), equal_to(1))
            assert_that(str(ad_markup['app_id']).count('eventID'), equal_to(1))