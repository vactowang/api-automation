import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('scrat - report ad - v5')
class TestUserActionMessage(object):

    @allure.feature('user action message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad user action message from debug info')
    @allure.description('Verify user action message basic from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_user_action_message_basic(self, pub_app_id):
        test_ifa = gen_device_id()
        app_id = gen_test_app_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=app_id)
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        # PBJ-4919 removed.
        # assert_that(debug['user_action_message']['event_id'], equal_to(app_id.replace('\"', '"').split('"')[-2]))
        # assert_that(isinstance(debug['user_action_message']['timestamp'], str))



    @allure.feature('user action message')
    @allure.tag('basic', 'smoke')
    @allure.story('report ad user action message from debug info')
    @allure.description('Verify user action message actions from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_user_action_message_actions(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.report_ad_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, app_id=gen_test_app_id())
        r = post(get_report_ad_endpoint_qa('5'), json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.report_ad_v5_debug)
        # PBJ-4919 removed.
        # assert_that(isinstance(debug['user_action_message']['user_actions'], list))
        # assert_that(isinstance(debug['user_action_message']['user_actions'][0], list))
        # assert_that(debug['user_action_message']['user_actions'][0][0]['action'],
        #             is_in(["videoLength", "videoViewed", "download", "mraidOpen", "mraidClose"]))
        # assert_that(isinstance(debug['user_action_message']['user_actions'][0][0]['timestamp_millis'], int))