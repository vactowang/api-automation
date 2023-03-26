import pytest
import allure

from utils.assertions import *
from http import HTTPStatus
from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain
from utils.common import *
from settings import *


@allure.epic('bid request')
class TestBidRequest(object):

    @allure.feature('bcat list')
    @allure.tag('normal')
    @allure.story('PBJ-3994 Adjust to bCat setting on Dashboard')
    @allure.description('Verify bcat field based on dashboard setting in case of no config in app&pub')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', [common_test_placement_1])
    def test_bcat_setting_on_dashboard_01(self, pub_app_id, placement_id):
        """
        without 'ad_cat_blocklist' field in application and application account
        """
        test_ifa = gen_device_id()
        if env == 'ci':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        # check bcat in bid_request

    @allure.feature('max duration')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4103 Max Duration Testing')
    @allure.description('Test max duration and skipafter in case of skipable is true for interstial placement '
                        'via test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_apps', max_duration_apps)
    @pytest.mark.parametrize('rtb_ids', [ext_test_mode_kraken_rtb_ids_mraid])
    def test_max_duration_072(self, pub_apps, rtb_ids):
        """
             db setting: placement level
             is_skippable: true


             application level:
             maxVideoLength: 32
        """

        test_ifa = test_mode_device_id
        req = request_payload.s2s_payload_sigmob_ios(pub_apps['pub_app'], pub_apps['placement'], ifa=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb_ids)
        maxDuration = bid_request['imp'][0]['video']['maxduration']
        video = bid_request['imp'][0]['video']
        assert_that(maxDuration, equal_to(120))
        assert_that(video['skip'], equal_to(1))
        assert_keys_exist(video, 'skipafter')
        assert_that(video['skipafter'], equal_to(5))

    @allure.feature('LO bid request')
    @allure.tag('normal')
    @allure.story('PBJ-4467 Jaeger - Remove ext.region in bid request to LO')
    @allure.description('Verify the field region is removed for LO')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_no_region_for_LO(self, pub_app_id, placement_id):

        test_ifa = gen_device_id()
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_liftoff.split(',')[1]
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['ext'], 'region')

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-4441 SSP - Make use of app_set_id for Android if no other device id available (Jaeger)')
    @allure.description('Test read ifa as device id if ifa and device.ext.ifv exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_device_id_ios_01(self, pub_app, placement_id):

        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app, placement_id, ifa=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']
        assert_that(device_info['id'], equal_to(test_ifa))
        assert_that(device_info['source'], equal_to('IFA'))

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-4441 SSP - Make use of app_set_id for Android if no other device id available (Jaeger)')
    @allure.description('Test read ifa as device id if ifa and device.ext.ifv exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_device_id_ios_02(self, pub_app, placement_id):

        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app, placement_id, ifa="", ifv=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']
        assert_that(device_info['id'], test_ifa)
        assert_that(device_info['source'], equal_to('IDFV'))

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-4441 SSP - Make use of app_set_id for Android if no other device id available (Jaeger)')
    @allure.description('Test vungle generate device id if no id exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('empty_device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-'])
    def test_device_id_ios_03(self, pub_app, placement_id, empty_device_id):
        req = request_payload.s2s_payload_sigmob_ios(pub_app, placement_id, ifa=empty_device_id, ifv=empty_device_id)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']
        assert_that(device_info['source'], equal_to('Vungle_FP'))

    @allure.feature('device info')
    @allure.story('PBJ-4441 SSP - Make use of app_set_id for Android if no other device id available (Jaeger)')
    @allure.description('Test read ifa as device id if ifa exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    def test_device_id_android_01(self, pub_app, placement_id):

        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_android(pub_app, placement_id, ifa=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']
        assert_that(device_info['id'], test_ifa)
        assert_that(device_info['source'], equal_to('IFA'))

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-4441 SSP - Make use of app_set_id for Android if no other device id available (Jaeger)')
    @allure.description('Test read android_id as device id only android_id exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    def test_device_id_android_02(self, pub_app, placement_id):

        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_android(pub_app, placement_id, ifa="", android_id=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']
        assert_that(device_info['id'], test_ifa)
        assert_that(device_info['source'], equal_to('ISU'))

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-4441 SSP - Make use of app_set_id for Android if no other device id available (Jaeger)')
    @allure.description('Test read app_set_id as device id if only app_set_id exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    def test_device_id_android_03(self, pub_app, placement_id):

        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_android(pub_app, placement_id, ifa="", android_id="",
                                                         app_set_id=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']
        assert_that(device_info['id'], test_ifa)
        assert_that(device_info['source'], equal_to('AppSetID'))


    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-4441 SSP - Make use of app_set_id for Android if no other device id available (Jaeger)')
    @allure.description('Test read app_set_id as device id if only app_set_id exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    def test_device_id_android_03_i(self, pub_app, placement_id):

        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_android(pub_app, placement_id, ifa="", android_id="",
                                                         app_set_id=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']
        assert_that(device_info['id'], test_ifa)
        assert_that(device_info['source'], equal_to('AppSetID'))
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['device']['ext']['vungle']['id_source'], equal_to("AppSetID"))

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-4441 SSP - Make use of app_set_id for Android if no other device id available (Jaeger)')
    @allure.description('Test read ifa as device id if ifa, android_id, app_set_id exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    def test_device_id_android_04(self, pub_app, placement_id):

        test_ifa = gen_device_id()
        test_ifa1= gen_device_id()
        req = request_payload.s2s_payload_sigmob_android(pub_app, placement_id, ifa=test_ifa, android_id=test_ifa1,
                                                         app_set_id=test_ifa1)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger',
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']
        assert_that(device_info['id'], test_ifa)
        assert_that(device_info['source'], equal_to('IFA'))

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-4441 SSP - Make use of app_set_id for Android if no other device id available (Jaeger)')
    @allure.description('Test read android_id as device id if android_id, app_set_id exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    def test_device_id_android_05(self, pub_app, placement_id):

        test_ifa = gen_device_id()
        test_ifa1= gen_device_id()
        req = request_payload.s2s_payload_sigmob_android(pub_app, placement_id, ifa="", android_id=test_ifa1,
                                                         app_set_id=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']
        assert_that(device_info['id'], test_ifa1)
        assert_that(device_info['source'], equal_to('ISU'))

    @allure.feature('device info')
    @allure.tag('normal')
    @allure.story('PBJ-4441 SSP - Make use of app_set_id for Android if no other device id available (Jaeger)')
    @allure.description('Test vungle generate device id if no id exist')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    @pytest.mark.parametrize('empty_device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-'])
    def test_device_id_android_06(self, pub_app, placement_id, empty_device_id):
        req = request_payload.s2s_payload_sigmob_android(pub_app, placement_id, ifa=empty_device_id, android_id=empty_device_id,
                                                         app_set_id=empty_device_id)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        device_info = response_payload['ext']['debug']['auction_result']['device_info']
        assert_that(device_info['source'], equal_to('Vungle_FP'))

    @allure.feature('support extension type')
    @allure.tag('normal')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify hb flag work well for s2s request on rtb.support_extension_type setting')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_support_extension_hb_flag_01(self, pub_app_id, placement):

        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement, ifv=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger',
                                          rtb_selector=ext1_non_kraken_test_mode_default_hb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext1_non_kraken_test_mode_default_hb)

        source_ext = bid_request['source']['ext']
        assert_keys_exist(source_ext, 'header_bidding')
        assert_that(source_ext['header_bidding'], equal_to(0))

    @allure.feature('support extension type')
    @allure.tag('normal')
    @allure.story('PBJ-4748 [SPO] VX sends duplicate Bid Requests to Accelerate for experiment testing')
    @allure.description('Verify bidrequest_id with suffix will not impact s2s bid response')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_support_extension_dup_01(self, pub_app_id, placement):

        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement, ifv=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger',
                                          rtb_selector=ext2_non_kraken_test_mode_default_dup))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext2_non_kraken_test_mode_default_dup)
        bid_request_id = bid_request['id']
        assert_that("___" in bid_request_id)
        bid_request_id_suffix = int(bid_request_id.split('___')[1])
        assert_that(isinstance(bid_request_id_suffix, int))

