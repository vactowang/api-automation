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
class TestPlacementId(object):

    @allure.tag('basic', 'smoke')
    @allure.story('placement')
    @allure.description('Verify placement id from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_placement_id(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that(ads['placement_reference_id'], equal_to('DEFAULT02021'))

    @allure.tag('basic')
    @allure.story('KONA experiment')
    @allure.story('PBJ-3979 Run KONA Experiment in jaeger record to message')
    @allure.description('Verify experiment info was record to transaction&delivery message')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    def test_kona_experiment_01(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02022', ifa='V9SHDTQ68ELAHLH7LEFWFWNE9RBZW0H5JJK0')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'exp_to_bucket', send delivery message only for non test mode idsp and meister.

    @allure.tag('basic')
    @allure.story('KONA experiment')
    @allure.story('PBJ-3828 Add experiments to config extension')
    @allure.description('Verify add config extension in ad request will not cause error')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620016b4'])
    def test_kona_config_ext_01(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02022', ifa='V9SHDTQ68ELAHLH7LEFWFWNE9RBZW0H5JJK0',
                                            ext=config_extension)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
