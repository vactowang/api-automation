import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('bastion v4')
@allure.feature('basic')
class TestConfigV4(object):

    @allure.story('Test for config v4 iOS')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5a55162ccbc18a63250138c6'])
    def test_config_v4_ios(self, pub_app_id):
        req = request_payload.config_v4_ios(pub_app_id)
        r = post(config_v4_endpoint_qa, json=req, headers=platform_headers(sdk_version='VungleDroid/4.0.3'))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.config_v4)

