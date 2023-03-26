from http import HTTPStatus

import allure

from data import request_payload, response_schema
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('jaeger nurl')
class TestWinNotification(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-5303 Change "nURL" firing logic from LoadAd to "playAd"')
    @allure.description('Verify that nurl has been move to checkpoint.0 for sdk>=6.11.0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('ip', [jp_ip])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0','Vungle/6.10.6', 'Vungle/6.10.5'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_nurl_move_to_checkpoint0_01(self, pub_app_id, placement, rtb_ids, ip, sdk_v):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        checkPoint0 = tpat['checkpoint.0']
        nurl = [x for i, x in enumerate(checkPoint0) if x.find('/win') != -1][0]
        assert_that(nurl is not None)
