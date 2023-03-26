import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - impression')
class TestScratImpression(object):

    @allure.feature('sdk hbp impression')
    @allure.tag('basic', 'smoke', 'v0.118.0', 'v0.123.0')
    @allure.story('PBJ-2805 HBP impression url change to scrat, '
                  'PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the hbp impression endpoint work fine with no param')
    @allure.severity('smoke')
    def test_scrat_impression_basic_1(self):
        req = request_payload.hbp_impression()
        r = get(scrat_impression_endpoint_qa(env), params=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('Request invalid: cannot get extInfo param.'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk hbp impression')
    @allure.tag('basic', 'smoke', 'v0.118.0', 'v0.123.0')
    @allure.story('PBJ-2805 HBP impression url change to scrat,'
                  'PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the hbp impression endpoint work fine with empty ext param')
    @allure.severity('smoke')
    def test_scrat_impression_basic_2(self):
        req = request_payload.hbp_impression(ext='')
        r = get(scrat_impression_endpoint_qa(env), params=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('Request invalid: cannot get extInfo param.'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk hbp impression')
    @allure.tag('basic', 'smoke', 'v0.118.0', 'v0.123.0')
    @allure.story('PBJ-2805 HBP impression url change to scrat,'
                  'PBJ-3102 Scrat mediation notification can work same as HBP')
    @allure.description('Verify the hbp impression endpoint work fine with invalid ext param')
    @allure.severity('smoke')
    def test_scrat_impression_basic_3(self):
        req = request_payload.hbp_impression(ext='123456')
        r = get(scrat_impression_endpoint_qa(env), params=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that('Request invalid: decode notification info failed' in response_payload['msg'])
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk hbp impression')
    @allure.tag('basic', 'smoke', 'v0.118.0', 'v0.123.0')
    @allure.story('PBJ-2805 HBP impression url change to scrat,'
                  'PBJ-3102 Scrat mediation notification can work same as HBP'
                  'PBJ-3864 [Scrat] [Scrat] delete f=b decode for impression')
    @allure.description('Verify the hbp impression endpoint work fine with no f=b ext param')
    @allure.severity('smoke')
    def test_scrat_impression_no_f_b_basic_4(self):
        req = request_payload.hbp_impression(ext=test_hbp_impression_no_f_b_param)
        r = get(scrat_impression_endpoint_qa(env), params=req, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk hbp impression')
    @allure.tag('basic')
    @allure.story('PBJ-3680 [Scrat] able to decode impression url with f=b')
    @allure.description('Verify the hbp impression endpoint work fine with new ext param')
    @allure.severity('smoke')
    def test_scrat_impression_new_basic_4(self):
        r = get(scrat_impression_endpoint_qa(env) + '?ext=' + test_hbp_impression_ext_param, headers=platform_headers())

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('s2s impression')
    @allure.tag('basic')
    @allure.story('PBJ-4435 s2s should use TPAT instead of s2s notifications for eDSP billing')
    @allure.description('Verify the message has been written to TPAT topic when send S2S impression successed')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_scrat_impression_s2s_01(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa, regs=True)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid'][0]
        imptrackers = bid['ext']['imptrackers']
        for url in imptrackers:
            if 'impression' in url:
                r = get(url)
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))
        # Verify that message has been written to the 'as-tpats' topic with fields: {
        # "event_id":"62ccdb25bc7e5b009aab6ae4","event_type":"start","is_demand_third_party":true,"is_test":false,
        # "timestamp":"2022-07-12 02:23:34.987"}

    @allure.feature('s2s impression')
    @allure.tag('basic', 'test_mode')
    @allure.story('PBJ-4435 s2s should use TPAT instead of s2s notifications for eDSP billing')
    @allure.description('Verify the message has been written to TPAT topic when send S2S impression successed')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_scrat_impression_s2s_02(self, pub_app_id, placement_id):
        test_ifa = test_mode_device_id
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa, regs=True)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]['bid'][0]
        imptrackers = bid['ext']['imptrackers']
        for url in imptrackers:
            if 'impression' in url:
                r = get(url)
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))
        # Verify that message has been written to the 'as-tpats' topic with fields: { {
        # "event_id":"62ccdbabbc7e5b009aab6ae6","event_type":"start","is_demand_third_party":true,"is_test":true,
        # "timestamp":"2022-07-12 02:25:48.677"}
