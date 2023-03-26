import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestBidResponseDetails(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid response details')
    @allure.description('Verify bid id from bid response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_bid_response_details_bid_id(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            for rtb_id in bid_response.keys():
                if 'seatbid' in bid_response[rtb_id]:
                    assert_response_status_code(r.status_code, HTTPStatus.OK)
                    assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                    assert_that(bid_response[rtb_id]['seatbid'][0]['bid'][0]['id'], ad_markup['id'])

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('bid response details')
    @allure.description('Verify campaign info from bid response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_bid_response_details_campaign(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        for rtb_id in bid_response.keys():
            if 'seatbid' in bid_response[rtb_id]:
                campaign_id = str(ad_markup['campaign']).split('|')[0]
                creative_id = str(ad_markup['campaign']).split('|')[1]

                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                assert_that(bid_response[rtb_id]['seatbid'][0]['bid'][0]['cid'], campaign_id)
                assert_that(bid_response[rtb_id]['seatbid'][0]['bid'][0]['crid'], creative_id)

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('sdk version')
    @allure.description('Test for legacy ad filter does not work for SDK version lower than 5.1')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b1'])
    def test_legacy_ad_filter_not_work(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'AREYOUS82690', ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/5.0.9', debug='jaeger'))

        response_payload = r.json()

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_response, not empty())

    @allure.feature('basic')
    @allure.tag('test_mode', 'smoke', 'basic')
    @allure.story('bid request test mode')
    @allure.description('Test for enable test mode by device id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_enable_test_mode_by_device_id(self, pub_app_id):
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids_1.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids_1.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['adm'], not empty())

    @allure.feature('test mode')
    @allure.tag('test_mode', 'smoke')
    @allure.story('test mode device support')
    @allure.description('Test for enable test mode by test mode pub app - windows device')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5b8d17307ad5a86fc53c7c8a'])
    def test_for_enable_test_mode_by_pub_app(self, pub_app_id):
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids_1.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids_1.split(',')[1]
        req = request_payload.jaeger_v5_windows(pub_app_id, 'DEFAULT-4642078', ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version='VungleWindows/6.4.0 (Windows 10; native)', debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['adm'], not empty())

    @allure.feature('test mode')
    @allure.tag('test_mode', 'smoke')
    @allure.story('test mode device support')
    @allure.description('Test for test mode amazon device support')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5bebe77a598bee2c619dca28'])
    def test_for_test_mode_amazon(self, pub_app_id):
        if env == 'ci':
            kraken_rtbconnection_id = test_mode_kraken_rtb_ids.split(',')[0]
            kraken_rtbconnection_id_1 = test_mode_kraken_rtb_ids_1.split(',')[0]
        elif env == 'qa' or env == 'regression':
            kraken_rtbconnection_id = test_mode_kraken_rtb_ids.split(',')[1]
            kraken_rtbconnection_id_1 = test_mode_kraken_rtb_ids_1.split(',')[1]
        req = request_payload.jaeger_v5_amazon(pub_app_id, 'DEFAULT-8228620', ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='VungleDroid/6.3.2', debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that(
                (bid_response[kraken_rtbconnection_id]['seatbid'][0]['bid'][0]['adm'], not empty())
                or
                (bid_response[kraken_rtbconnection_id_1]['seatbid'][0]['bid'][0]['adm'], not empty())
            )

    @allure.feature('test mode')
    @allure.tag('test_mode', 'smoke')
    @allure.story('test mode ad type support')
    @allure.description('Test for test mode mrec support')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_test_mode_mrec(self, pub_app_id):
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, 'MREC-TEST-01', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            sdk_version='Vungle/6.4.0', debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        if 'sleep' not in ad_markup:
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_that((bid_response[rtb]['seatbid'][0]['bid'][0]['adm'], not empty()))

    @allure.feature('test mode')
    @allure.tag('test_mode', 'smoke')
    @allure.story('test mode ad type support')
    @allure.description('Test for test mode banner support')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_test_mode_banner(self, pub_app_id):
        if env == 'ci':
            kraken_rtbconnection_id = test_mode_kraken_rtb_ids.split(',')[0]
            kraken_rtbconnection_id_1 = test_mode_kraken_rtb_ids_1.split(',')[0]
        elif env == 'qa' or env == 'regression':
            kraken_rtbconnection_id = test_mode_kraken_rtb_ids.split(',')[1]
            kraken_rtbconnection_id_1 = test_mode_kraken_rtb_ids_1.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(
            (bid_response[kraken_rtbconnection_id]['seatbid'][0]['bid'][0]['adm'], not empty())
            or
            (bid_response[kraken_rtbconnection_id_1]['seatbid'][0]['bid'][0]['adm'], not empty())
        )

    @allure.feature('test mode')
    @allure.tag('test_mode', 'normal')
    @allure.story('rtb connection selector')
    @allure.description('Test for selecting test mode rtbConnection in case of test mode turned on')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_select_test_mode_rtb(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if env == 'ci':
            assert_keys_exist(bid_response, test_mode_kraken_rtb_ids_1.split(',')[0])
        elif env == 'qa' or env == 'regression':
            assert_keys_exist(bid_response, test_mode_kraken_rtb_ids_1.split(',')[1])

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'test_mode', 'R_1.137.0')
    @allure.story('PBJ-1962 Add attribute method in delivery message')
    @allure.description('Verify that Kraken returns attribution_method')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_add_attribute_method_kraken(self, pub_app_id):
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_response[rtb]['seatbid'][0]['bid'][0]['ext']['vungle']['attribution_method'],
                          'skadnetwork')

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid response details')
    @allure.description('Verify ext vungle info in seatbid from bid response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_bid_response_details_seatbid_ext_vungle(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        for rtb_id in bid_response.keys():
            if 'seatbid' in bid_response[rtb_id]:
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'ad_app_store_id')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'ad_app_object_id')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'bid_price')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'conv_rate')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'campaign_base_rate')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'campaign_rate')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'campaign_surge_rate')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'campaign_rate_type')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'],
                                  'campaign_premium_rate')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'erpm')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'vid')
                assert_keys_exist(bid_response[rtb_id]['seatbid'][0]['bid'][0]['ext']['vungle'], 'bundle')

    @allure.feature('basic')
    @allure.tag('normal')
    @allure.story('bid response details')
    @allure.description('Verify the ext vungle info from bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_bid_response_details_ext_vungle(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        for rtb_id in bid_response.keys():
            if 'seatbid' in bid_response[rtb_id]:
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                assert_keys_exist(bid_response[rtb_id]['ext']['vungle'], 'ignoredevicehistory')

    @allure.feature('wurfl support')
    @allure.tag('normal', 'R_1.131.0')
    @allure.story('PBJ-1724 Support wurfl in Jaeger')
    @allure.description('Verify the wurfl info from bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_wurfl_bid_response(self, pub_app_id):
        test_ifa = gen_device_id()
        test_ua = 'test_ua'
        if env == 'ci':
            rtb = meister_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = meister_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa, make='Apple',
                                            model='iPhone11,8', ua=test_ua)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        for rtb_id in bid_response.keys():
            if 'seatbid' in bid_response[rtb_id]:
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                assert_that(bid_response[rtb_id]['ext']['vungle']['wurfl']['make'], equal_to('Apple'))
                assert_that(bid_response[rtb_id]['ext']['vungle']['wurfl']['model'], equal_to('iPhone11,8'))
                assert_keys_exist(bid_response[rtb_id]['ext']['vungle']['wurfl'], 'msrp')
                assert_keys_exist(bid_response[rtb_id]['ext']['vungle']['wurfl'], 'release_date')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support')
    @allure.description('Verify that the VAST external Kraken returns skadn')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_add_skadn_for_programmatic_vast(self, pub_app_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_response[rtb]['seatbid'][0]['bid'][0]['ext'], 'skadn')
        skadn = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']['skadn']
        assert_that(isinstance(skadn['version'], str))
        assert_that(isinstance(skadn['network'], str))
        assert_that(isinstance(skadn['campaign'], str))
        assert_that(isinstance(skadn['itunesitem'], str))
        assert_that(isinstance(skadn['nonce'], str))
        assert_that(isinstance(skadn['sourceapp'], str))
        assert_that(isinstance(skadn['timestamp'], str))
        assert_that(isinstance(skadn['signature'], str))
        assert_that(isinstance(skadn['ext'], dict))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support')
    @allure.description('Verify that the MRAID external Kraken returns skadn')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_ref_id', ['BANNER-TEST-01'])
    def test_add_skadn_for_programmatic_mraid(self, pub_app_id, placement_ref_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_response[rtb]['seatbid'][0]['bid'][0]['ext'], 'skadn')
        skadn = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']['skadn']
        assert_that(isinstance(skadn['version'], str))
        assert_that(isinstance(skadn['network'], str))
        assert_that(isinstance(skadn['campaign'], str))
        assert_that(isinstance(skadn['itunesitem'], str))
        assert_that(isinstance(skadn['nonce'], str))
        assert_that(isinstance(skadn['sourceapp'], str))
        assert_that(isinstance(skadn['timestamp'], str))
        assert_that(isinstance(skadn['signature'], str))
        assert_that(isinstance(skadn['ext'], dict))

    @allure.feature('market id blacklist')
    @allure.tag('normal', 'v1.157.0')
    @allure.story('PBJ-2609 Block advertising apps through Store ID (marketID)at the publisher account level')
    @allure.description('Verify the bundle id blacklist for iOS')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement_ref_id', [common_test_placement_10])
    def test_bundle_id_blacklist_ios(self, pub_app_id, placement_ref_id):
        '''
            The bundle id in blacklist: 618783545
        '''
        if env == 'ci':
            rtb = meister_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = meister_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle'], not equal_to('618783545'))

    @allure.feature('market id blacklist')
    @allure.tag('normal', 'v1.157.0')
    @allure.story('PBJ-2609 Block advertising apps through Store ID (marketID)at the publisher account level')
    @allure.description('Verify the bundle id blacklist for Android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_ref_id', [android_common_test_placement])
    def test_bundle_id_blacklist_android(self, pub_app_id, placement_ref_id):
        '''
            The bundle id in blacklist: com.babbel.mobile.android.en
        '''
        if env == 'ci':
            rtb = meister_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = meister_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement_ref_id, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle'], not equal_to('com.babbel.mobile.android.en'))

    @allure.feature('bundle id')
    @allure.tag('normal', 'v0.16.0', 'test_mode', 'kraken')
    @allure.story('PBJ-2664 Kraken should fill cat and bundle field for iDSP and eDSP')
    @allure.description('Verify the bundle id from bid response of internal Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_ref_id', [common_test_placement])
    def test_bundle_id_internal_kraken(self, pub_app_id, placement_ref_id):
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_response[rtb]['seatbid'][0]['bid'][0], 'bundle')
        assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle'], equal_to('1046740065'))

    @allure.feature('bundle id')
    @allure.tag('normal', 'v0.16.0', 'test_mode', 'kraken')
    @allure.story('PBJ-2664 Kraken should fill cat and bundle field for iDSP and eDSP')
    @allure.description('Verify the cat from bid response of internal Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_ref_id', [common_test_placement])
    def test_cat_internal_kraken(self, pub_app_id, placement_ref_id):
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_response[rtb]['seatbid'][0]['bid'][0], 'cat')
        assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['cat'], equal_to(['Movies', 'Music']))

    @allure.feature('bundle id')
    @allure.tag('normal', 'v0.16.0', 'test_mode', 'kraken')
    @allure.story('PBJ-2664 Kraken should fill cat and bundle field for iDSP and eDSP')
    @allure.description('Verify the bundle id from bid response of external Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_ref_id', [common_test_placement])
    def test_bundle_id_external_kraken(self, pub_app_id, placement_ref_id):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_response[rtb]['seatbid'][0]['bid'][0], 'bundle')
        assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle'], equal_to('1490962424'))

    @allure.feature('bundle id')
    @allure.tag('normal', 'v0.16.0', 'kraken')
    @allure.story('PBJ-2664 Kraken should fill cat and bundle field for iDSP and eDSP')
    @allure.description('Verify the bundle id from bid response of external Kraken in non-test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_ref_id', [common_test_placement])
    def test_bundle_id_external_kraken_non_test_mode(self, pub_app_id, placement_ref_id):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_response[rtb]['seatbid'][0]['bid'][0], 'bundle')
        assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle'], equal_to('1490962424'))

    @allure.feature('rtb meister support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3088 Send bid request to HBP specific Meister')
    @allure.description('Verify that the hb traffic can call the RTB Meister via the specific rtb connection')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_meister_bid_response_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=hb_meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_keys_exist(bid_response[hb_meister_rtb_ids], 'bidid')

    @allure.feature('rtb meister support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3088 Send bid request to HBP specific Meister')
    @allure.description('Verify that the hb traffic can not call the legacy Meister via the specific rtb connection')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_meister_bid_response_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=legacy_meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_not_exist(response_payload['ext']['debug'], 'auction_result')

    @allure.feature('rtb meister support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3088 Send bid request to HBP specific Meister')
    @allure.description('Verify that the non-hb traffic will not be impact with legacy Meister')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_meister_bid_response_3(self, pub_app_id, placement):
        if env == 'ci':
            rtb = legacy_meister_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = legacy_meister_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_keys_exist(bid_response[rtb], 'bidid')

    @allure.feature('rtb meister support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3088 Send bid request to HBP specific Meister')
    @allure.description('Verify that the non-hb traffic can not call the RTB Meister via the specific rtb connection')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_meister_bid_response_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=hb_meister_rtb_ids))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_not_exist(response_payload['ext']['debug'], 'auction_result')

    @allure.feature('rtb meister support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3088 Send bid request to HBP specific Meister')
    @allure.description('Verify that both hb and non-hb traffic will not be impact with eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_rtb_meister_bid_response_5(self, pub_app_id, placement, hb):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        assert_keys_exist(bid_response[rtb], 'id')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid response via sdv version >= 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_bid_response_traffic(self, pub_app_id, placement, sdk_v, hb):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid_ext = bid_request[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_exist(seat_bid_ext, 'deeplink')
        assert_that(isinstance(seat_bid_ext['deeplink'], str))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid response via sdv version >= 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_bid_response_traffic_test_mode(self, pub_app_id, placement, sdk_v, hb):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid_ext = bid_request[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_exist(seat_bid_ext, 'deeplink')
        assert_that(isinstance(seat_bid_ext['deeplink'], str))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid response via sdv version < 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_no_deeplink_in_bid_response_traffic_test_mode(self, pub_app_id, placement, sdk_v, hb):

        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid_ext = bid_request[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_not_exist(seat_bid_ext, 'deeplink')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid response via sdv version < 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_no_deeplink_in_bid_response_traffic(self, pub_app_id, placement, sdk_v, hb):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid_ext = bid_request[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_not_exist(seat_bid_ext, 'deeplink')


    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid response via sdv version >= 6.11.0'
                        ' and iDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('hb', [True])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_no_deeplink_in_bid_response_traffic_idsp(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=hb_meister_rtb_ids))
        response_payload = r.json()
        bid_request = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid_ext = bid_request[hb_meister_rtb_ids]['seatbid'][0]['bid'][0]['ext']
        assert_keys_not_exist(seat_bid_ext, 'deeplink')

    # ------------------------------------------- deeplink for android -------------------------------------------------

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid response via sdv version >= 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_bid_response_android(self, pub_app_id, placement, sdk_v, hb):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid_ext = bid_request[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_exist(seat_bid_ext, 'deeplink')
        assert_that(isinstance(seat_bid_ext['deeplink'], str))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid response via sdv version >= 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_bid_response_traffic_test_mode_android(self, pub_app_id, placement, sdk_v, hb):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb,
                                                android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid_ext = bid_request[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_exist(seat_bid_ext, 'deeplink')
        assert_that(isinstance(seat_bid_ext['deeplink'], str))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid response via sdv version < 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_no_deeplink_in_bid_response_traffic_test_mode_android(self, pub_app_id, placement, sdk_v, hb):

        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb,
                                                android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid_ext = bid_request[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_not_exist(seat_bid_ext, 'deeplink')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid response via sdv version < 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_no_deeplink_in_bid_response_traffic_android(self, pub_app_id, placement, sdk_v, hb):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid_ext = bid_request[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_not_exist(seat_bid_ext, 'deeplink')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid response via sdv version >= 6.11.0'
                        ' and iDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_no_deeplink_in_bid_response_traffic_idsp_android(self, pub_app_id, placement, sdk_v, hb):

        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=hb_meister_rtb_ids))
        response_payload = r.json()
        bid_request = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid_ext = bid_request[hb_meister_rtb_ids]['seatbid'][0]['bid'][0]['ext']
        assert_keys_not_exist(seat_bid_ext, 'deeplink')

    @allure.feature('first price auction')
    @allure.tag('normal', 'v1.176.0')
    @allure.story('PBJ-3227 In idsp_transaction, auction_actual_bid_price and auction_winning_bid_price are not equal '
                  'in 1st-price auction')
    @allure.description('Verify the settlement price = bid price if bid price < bid floor for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_1st_price_auction_edge_case_1(self, pub_app_id, placement):
        '''
            FR country floor = 2.5
            Kraken int1 bid price = 2
            erpmtarget < 2
        '''
        if env == 'qa' or env == 'regression':
            rtb = non_test_mode_kraken_int1_rtb_ids.split(',')[1]

            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=fr_ip, rtb_selector=rtb))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['price'], equal_to(2))

    @allure.feature('first price auction')
    @allure.tag('normal', 'v1.176.0', 'test_mode')
    @allure.story('PBJ-3227 In idsp_transaction, auction_actual_bid_price and auction_winning_bid_price are not equal '
                  'in 1st-price auction')
    @allure.description('Verify the settlement price = bid price if bid price < bid floor for iDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_1st_price_auction_edge_case_2(self, pub_app_id, placement, hb):
        '''
            FR country floor = 2.5
            Kraken int1 bid price = 2
            erpmtarget < 2
        '''
        if env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_int1_rtb_ids.split(',')[1]

            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=hb)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=fr_ip, rtb_selector=rtb))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['price'], equal_to(2))

    @allure.feature('parse third party imptrackers')
    @allure.tag('normal')
    @allure.story('PBJ-3226 RTB :: Banner Third Party Imptrackers Not Firing')
    @allure.description('Verify that there is imptrackers field from bid response for test mode eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_imptrackers_field_for_test_mode_edsp(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = ext1_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                                banner=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            bid_response_ext = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']
            assert_keys_exist(bid_response_ext, 'imptrackers')

    @allure.feature('parse third party imptrackers')
    @allure.tag('normal')
    @allure.story('PBJ-3226 RTB :: Banner Third Party Imptrackers Not Firing')
    @allure.description('Verify that parse imptrackers field from bid response to checkpoint.0 for test mode eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_parse_imptrackers_field_for_test_mode_edsp_01(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext1_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True,
                                            banner=True, )
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=fr_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        bid_response_ext = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_exist(bid_response_ext, 'imptrackers')
        bid_price = bid_response[rtb]['seatbid'][0]['bid'][0]['price']
        imptrackers = bid_response_ext['imptrackers']
        checkpoint0 = response_payload['ads'][0]['ad_markup']['tpat']['checkpoint.0']
        imptrackers[1] = imptrackers[1].replace('${AUCTION_PRICE}', format(bid_price, '.9f'))
        assert_that(set(imptrackers).issubset(set(checkpoint0)))

    @allure.feature('parse third party imptrackers')
    @allure.tag('normal')
    @allure.story('PBJ-3226 RTB :: Banner Third Party Imptrackers Not Firing')
    @allure.description('Verify that parse imptrackers field from bid response to play_percentage.0 for test mode eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_parse_imptrackers_field_for_test_mode_edsp_02(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext1_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, os_version='9.9', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        bid_response_ext = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_exist(bid_response_ext, 'imptrackers')
        bid_price = bid_response[rtb]['seatbid'][0]['bid'][0]['price']
        imptrackers = bid_response_ext['imptrackers']
        play_percentage_urls = response_payload['ads'][0]['ad_markup']['tpat']['play_percentage']
        percentage0 = ''
        for x in play_percentage_urls:
            if x['checkpoint'] == 0:
                percentage0 = x['urls']
            else:
                continue
        imptrackers[1] = imptrackers[1].replace('${AUCTION_PRICE}', format(bid_price, '.9f'))
        assert_that(set(imptrackers).issubset(set(percentage0)))

    @allure.feature('parse third party imptrackers')
    @allure.tag('normal')
    @allure.story('PBJ-3226 RTB :: Banner Third Party Imptrackers Not Firing')
    @allure.description('Verify that there is imptrackers field from bid response for non test mode eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_imptrackers_field_for_non_test_mode_edsp(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True,
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        bid_response_ext = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_exist(bid_response_ext, 'imptrackers')

    @allure.feature('parse third party imptrackers')
    @allure.tag('normal')
    @allure.story('PBJ-3226 RTB :: Banner Third Party Imptrackers Not Firing')
    @allure.description('Verify that parse imptrackers field from bid response to checkpoint.0 for non test mode eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_parse_imptrackers_field_for_non_test_mode_edsp_01(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True,
                                            header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        bid_response_ext = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_exist(bid_response_ext, 'imptrackers')
        bid_price = bid_response[rtb]['seatbid'][0]['bid'][0]['price']
        imptrackers = bid_response_ext['imptrackers']
        checkpoint0 = response_payload['ads'][0]['ad_markup']['tpat']['checkpoint.0']
        imptrackers[1] = imptrackers[1].replace('${AUCTION_PRICE}', format(bid_price, '.9f'))
        assert_that(set(imptrackers).issubset(set(checkpoint0)))

    @allure.feature('parse third party imptrackers')
    @allure.tag('normal')
    @allure.story('PBJ-3226 RTB :: Banner Third Party Imptrackers Not Firing')
    @allure.description(
        'Verify that parse imptrackers field from bid response to play_percentage.0 for non test mode eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_parse_imptrackers_field_for_non_test_mode_edsp_02(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(),
                                            header_bidding=True, os_version='9.9')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(r.json(), response_schema.ads_v5)

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        bid_response_ext = bid_response[rtb]['seatbid'][0]['bid'][0]['ext']
        assert_keys_exist(bid_response_ext, 'imptrackers')
        bid_price = bid_response[rtb]['seatbid'][0]['bid'][0]['price']
        imptrackers = bid_response_ext['imptrackers']
        play_percentage_urls = response_payload['ads'][0]['ad_markup']['tpat']['play_percentage']
        percentage0 = ''
        for x in play_percentage_urls:
            if x['checkpoint'] == 0:
                percentage0 = x['urls']
            else:
                continue
        imptrackers[1] = imptrackers[1].replace('${AUCTION_PRICE}', format(bid_price, '.9f'))
        assert_that(set(imptrackers).issubset(set(percentage0)))

    @allure.feature('Test mode improvement')
    @allure.tag('normal')
    @allure.story('PBJ-3261 Test mode improvement for app bidding - Jaeger')
    @allure.description('Verify that bid price is 100.001 from bid response for jaeger test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_test_mode_jaeger_01(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            price = bid_response[rtb]['seatbid'][0]['bid'][0]['price']
            assert_that('test-ads' in ad_markup['campaign'])
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_keys_exist(bid_response[rtb], 'id')
            assert_that(price, equal_to(100.001))

    @allure.feature('Test mode improvement')
    @allure.tag('normal')
    @allure.story('PBJ-3261 Test mode improvement for app bidding - Jaeger')
    @allure.description('Verify that bid price is 100.001 from bid response for jaeger test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    def test_test_mode_jaeger_02(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(sdk_version='Vungle/6.11.0', debug='jaeger', src_ip=au_ip,
                                              rtb_selector=rtb))
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            price = bid_response[rtb]['seatbid'][0]['bid'][0]['price']
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_keys_exist(bid_response[rtb], 'id')
            assert_that('test-ads' in ad_markup['campaign'])
            assert_that(price, equal_to(100.001))

    @allure.feature('Test mode improvement')
    @allure.tag('normal')
    @allure.story('PBJ-3261 Test mode improvement for app bidding - Jaeger')
    @allure.description('Verify that bid price is 100.001 from bid response for jaeger test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement])
    def test_test_mode_jaeger_03(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(sdk_version='Vungle/6.11.0', debug='jaeger', src_ip=au_ip,
                                              rtb_selector=rtb))
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            price = bid_response[rtb]['seatbid'][0]['bid'][0]['price']
            assert_keys_exist(bid_response[rtb], 'id')
            assert_that('test-ads' in ad_markup['campaign'])
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(price, equal_to(100.001))

    @allure.feature('Test mode improvement')
    @allure.tag('normal')
    @allure.story('PBJ-3261 Test mode improvement for app bidding - Jaeger')
    @allure.description('Verify that bid price is not the test price from bid response for jaeger non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    def test_test_mode_jaeger_04(self, pub_app_id, placement):
        rtb = meister_rtb_ids.split(',')[2]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        price = bid_response[rtb]['seatbid'][0]['bid'][0]['price']
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_that('test-ads' not in ad_markup['campaign'])
        assert_that(price, is_not(100.001))

    @allure.feature('tcpi')
    @allure.tag('normal')
    @allure.story('PBJ-3268 Ignore flat cpm NRG multiplier overrides for tCPI campaigns in Jaeger'
                  'PBJ-3335 Should use flat_cpm_value to check the tCPI bid price')
    @allure.description(
        'Verify jaeger serve and log error when campaign_rate_type=target_cpi and bid.price<flat_cpm_value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_TCPI_3])
    def test_jaeger_serve_but_log_error(self, pub_app_id, placement):
        """
        flat_cpm=100.002
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            header_bidding=True)
        Override_Bid_Ext = {
            "vungle":
                {
                    "ad_app_object_id": "4ee19fb8121ae61a03000022",
                    "ad_app_store_id": "adv-store-id",
                    "vid": "562721e66ddcba3a68000053",
                    "attribution_method": "skadnetwork",
                    "campaign_rate_type": "target_cpi",
                    "campaign_rate": 110
                }
        }
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                                                        rtb_selector=test_mode_kraken_rtb_ids,
                                                                        override_bid_ext=json.dumps(Override_Bid_Ext)))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that('sleep' not in ad_markup)

    @allure.feature('tcpi')
    @allure.tag('normal')
    @allure.story('PBJ-3268 Ignore flat cpm NRG multiplier overrides for tCPI campaigns in Jaeger'
                  'PBJ-3335 Should use flat_cpm_value to check the tCPI bid price')
    @allure.description(
        'Verify jaeger serve  when campaign_rate_type=target_cpi and bid.price>flat_cpm_value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_TCPI_2])
    def test_jaeger_serve_01(self, pub_app_id, placement):
        """
               flat_cpm=100
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            header_bidding=True)
        Override_Bid_Ext = {
            "vungle":
                {
                    "ad_app_object_id": "4ee19fb8121ae61a03000022",
                    "ad_app_store_id": "adv-store-id",
                    "vid": "562721e66ddcba3a68000053",
                    "attribution_method": "skadnetwork",
                    "campaign_rate_type": "target_cpi",
                    "campaign_rate": 90
                }
        }
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids,
                                          override_bid_ext=json.dumps(Override_Bid_Ext)))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that('sleep' not in ad_markup)

    @allure.feature('tcpi')
    @allure.tag('normal')
    @allure.story('PBJ-3268 Ignore flat cpm NRG multiplier overrides for tCPI campaigns in Jaeger')
    @allure.description(
        'Verify jaeger serve  when campaign_rate_type=target_cpi and bid.price=flat_cpm_value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_TCPI_1])
    def test_jaeger_serve_02(self, pub_app_id, placement):
        """
        flat_cpm=100.001
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id,
                                            header_bidding=True)
        Override_Bid_Ext = {
            "vungle":
                {
                    "ad_app_object_id": "4ee19fb8121ae61a03000022",
                    "ad_app_store_id": "adv-store-id",
                    "vid": "562721e66ddcba3a68000053",
                    "attribution_method": "skadnetwork",
                    "campaign_rate_type": "target_cpi",
                    "campaign_rate": 100.001
                }
        }
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids,
                                          override_bid_ext=json.dumps(Override_Bid_Ext)))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_that('sleep' not in ad_markup)

    @allure.feature('tcpi')
    @allure.tag('normal')
    @allure.story('PBJ-3405 The header of X-Vungle-Override-Bid-Ext doesn\'t work for eDSP(external Kraken)')
    @allure.description(
        'Verify jaeger serve  when campaign_rate_type=target_cpi and bid.price=flat_cpm_value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_TCPI_1])
    def test_parse_override_bid_ext_for_edsp(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        Override_Bid_Ext = {
            "vungle":
                {
                    "ad_app_object_id": "4ee19fb8121ae61a03000022",
                    "ad_app_store_id": "adv-store-id",
                    "vid": "562721e66ddcba3a68000053",
                    "attribution_method": "skadnetwork",
                    "no_override": False,
                    "campaign_rate_type": "target_cpi",
                    "campaign_rate": 99
                },
            "testgroups": [
                {
                    "experiment": "lv-margin-1",
                    "group": "lv-margin-control-2"
                }
            ]
        }
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          override_bid_ext=json.dumps(Override_Bid_Ext)))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        bid_response_detail = bid_response[rtb]
        if 'seatbid' in bid_response_detail:
            assert_keys_exist(bid_response_detail['seatbid'][0]['bid'][0]['ext'], 'vungle')
            assert_that(bid_response_detail['seatbid'][0]['bid'][0]['ext']['vungle']['campaign_rate'], equal_to(99))

    @allure.feature('tcpi')
    @allure.tag('normal')
    @allure.story('PBJ-3405 The header of X-Vungle-Override-Bid-Ext doesn\'t work for eDSP(external Kraken)')
    @allure.description(
        'Verify jaeger serve  when campaign_rate_type=target_cpi and bid.price=flat_cpm_value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_parse_override_bid_ext_for_edsp_on_android(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                header_bidding=True)
        Override_Bid_Ext = {
            "vungle":
                {
                    "ad_app_object_id": "4ee19fb8121ae61a03000022",
                    "ad_app_store_id": "adv-store-id",
                    "vid": "562721e66ddcba3a68000053",
                    "attribution_method": "skadnetwork",
                    "no_override": False,
                    "campaign_rate_type": "target_cpi",
                    "campaign_rate": 99
                },
            "testgroups": [
                {
                    "experiment": "lv-margin-1",
                    "group": "lv-margin-control-2"
                }
            ]
        }
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          override_bid_ext=json.dumps(Override_Bid_Ext)))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        bid_response_detail = bid_response[rtb]
        if 'seatbid' in bid_response_detail:
            assert_keys_exist(bid_response_detail['seatbid'][0]['bid'][0]['ext'], 'vungle')
            assert_that(bid_response_detail['seatbid'][0]['bid'][0]['ext']['vungle']['campaign_rate'], equal_to(99))

    @allure.feature('tcpi')
    @allure.tag('normal')
    @allure.story('PBJ-3405 The header of X-Vungle-Override-Bid-Ext doesn\'t work for eDSP(external Kraken)')
    @allure.description(
        'Verify jaeger serve  when campaign_rate_type=target_cpi and bid.price=flat_cpm_value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_TCPI_1])
    def test_parse_override_bid_ext_for_non_test_mode_edsp(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        Override_Bid_Ext = {
            "vungle":
                {
                    "ad_app_object_id": "4ee19fb8121ae61a03000022",
                    "ad_app_store_id": "adv-store-id",
                    "vid": "562721e66ddcba3a68000053",
                    "attribution_method": "skadnetwork",
                    "no_override": False,
                    "campaign_rate_type": "target_cpi",
                    "campaign_rate": 99
                },
            "testgroups": [
                {
                    "experiment": "lv-margin-1",
                    "group": "lv-margin-control-2"
                }
            ]
        }
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          override_bid_ext=json.dumps(Override_Bid_Ext)))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        bid_response_detail = bid_response[rtb]
        if 'seatbid' in bid_response_detail:
            assert_keys_exist(bid_response_detail['seatbid'][0]['bid'][0]['ext'], 'vungle')
            assert_that(bid_response_detail['seatbid'][0]['bid'][0]['ext']['vungle']['campaign_rate'], equal_to(99))

    # ------------------------------------------- minimum bid to win --------------------------------------------------

    @allure.feature('Minimum bid to win')
    @allure.tag('smoke')
    @allure.story('PBJ-3295 Implement minimum_bid_to_win')
    @allure.description('Verify that minimum bid to win added in bid response for non test mode edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_min_bid_to_win_bid_response_01(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_2.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_2.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid = bid_response[rtb]['seatbid']
        assert_that('lurl' in seat_bid[0]['bid'][0])
        assert_that('${MIN_BID_TO_WIN}' in seat_bid[0]['bid'][0]['lurl'])

    @allure.feature('Minimum bid to win')
    @allure.tag('smoke')
    @allure.story('PBJ-3295 Implement minimum_bid_to_win')
    @allure.description('Verify that minimum bid to win added in bid response for test mode idsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_min_bid_to_win_bid_response_02(self, pub_app_id, placement):
        if env == 'ci':
            rtb = test_mode_kraken_int2_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_int2_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid = bid_response[rtb]['seatbid']
        assert_that('lurl' in seat_bid[0]['bid'][0])
        assert_that('${MIN_BID_TO_WIN}' in seat_bid[0]['bid'][0]['lurl'])

    @allure.feature('Minimum bid to win')
    @allure.tag('smoke')
    @allure.story('PBJ-3295 Implement minimum_bid_to_win')
    @allure.description('Verify that minimum bid to win added in bid response for cn ip')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_min_bid_to_win_bid_response_for_cn_ip(self, pub_app_id, placement):
        if env == 'ci':
            rtb = test_mode_kraken_int2_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_int2_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=cn_ip, rtb_selector=rtb))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid = bid_response[rtb]['seatbid']
        assert_that('lurl' in seat_bid[0]['bid'][0])
        assert_that('${MIN_BID_TO_WIN}' in seat_bid[0]['bid'][0]['lurl'])

    @allure.feature('Minimum bid to win')
    @allure.tag('smoke')
    @allure.story('PBJ-3295 Implement minimum_bid_to_win')
    @allure.description('Verify for there is no min bid to win in lurl which Jaeger call for '
                        '"allow_min_bid_to_win": false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_min_bid_to_win_no_bid_response_03(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            seat_bid = bid_response[rtb]['seatbid']
            assert_that('lurl' in seat_bid[0]['bid'][0])
            assert_that('${MIN_BID_TO_WIN}' in seat_bid[0]['bid'][0]['lurl'])
            # Verify that the lurl which Jaeger sends to DSP has no value of MIN_BID_TO_WIN

    @allure.feature('Minimum bid to win')
    @allure.tag('smoke')
    @allure.story('PBJ-3295 Implement minimum_bid_to_win')
    @allure.description('Verify there is minimum bid to win added in bid response for mixed rtb ids')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_min_bid_to_win_no_bid_response_04(self, pub_app_id, placement):
        rtb = test_mode_kraken_int2_rtb_ids_1 + ',' + test_mode_kraken_int2_rtb_ids
        if env == 'qa' or env == 'regression':
            rtb_true = test_mode_kraken_int2_rtb_ids.split(",")[1]
            rtb_false = test_mode_kraken_int2_rtb_ids_1.split(",")[1]

            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            seat_bid_1 = bid_response[rtb_true]['seatbid']
            seat_bid_2 = bid_response[rtb_false]['seatbid']
            assert_that('lurl' in seat_bid_1[0]['bid'][0])
            assert_that('lurl' in seat_bid_2[0]['bid'][0])  # Verify that the lurl which Jaeger sends to DSP has no value of MIN_BID_TO_WIN

    @allure.feature('Minimum bid to win')
    @allure.tag('smoke')
    @allure.story('PBJ-3295 Implement minimum_bid_to_win')
    @allure.description('Verify that minimum bid to win added in bid response for test mode idsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_min_bid_to_win_bid_response_android(self, pub_app_id, placement):
        if env == 'ci':
            rtb = test_mode_kraken_int2_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_int2_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        seat_bid = bid_response[rtb]['seatbid']
        assert_that('lurl' in seat_bid[0]['bid'][0])
        assert_that('${MIN_BID_TO_WIN}' in seat_bid[0]['bid'][0]['lurl'])

    @allure.feature('fullscreen playable')
    @allure.tag('smoke', 'test_mode')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.'
                  'PBJ-3674 Internal Kraken need to implement same ad-size logic with '
                  'Meister and External Kraken need to support deprecate the adm type configuration')
    @allure.description('Verify jaeger will server when request banner+video impression for '
                        'Interstitial&rewarded via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_01,
                                           common_test_third_party_placement_crtype_02])
    def test_fullscreen_bid_response_test_mode_edsp(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':

            rtb = ext1_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=test_mode_device_id,
                                                header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                              rtb_selector=rtb))
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            templateURL = ad_markup['templateURL']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            seatbid = bid_response[rtb]['seatbid']
            adm = seatbid[0]['bid'][0]['adm']
            if 'rtbVideo.zip' in templateURL:
                assert 'VAST' in adm
            elif 'programmaticFullscreenPlayable.zip' in templateURL:
                assert_that(seatbid[0]['bid'][0]['attr'][0], equal_to(13))
                assert_that(seatbid[0]['bid'][0]['ext']['crtype'], equal_to('MRAID 2.0'))

    @allure.feature('fullscreen playable')
    @allure.tag('smoke', 'test_mode')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.'
                  'PBJ-3674 Internal Kraken need to implement same ad-size logic with '
                  'Meister and External Kraken need to support deprecate the adm type configuration'
                  'PBJ-3765 Check "attr=13" in the bid response for programmatic playables')
    @allure.description('Verify jaeger will server when request banner+video impression for '
                        'Interstitial&rewarded via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_01,
                                           common_test_third_party_placement_crtype_02])
    def test_fullscreen_bid_response_test_mode_edsp_no_mraid_version(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            Override_Bid_Ext = {
                "vungle":
                    {
                        "ad_app_object_id": "4ee19fb8121ae61a03000022",
                        "ad_app_store_id": "adv-store-id",
                        "vid": "562721e66ddcba3a68000053",
                        "attribution_method": "skadnetwork",
                        "campaign_rate_type": "target_cpi",
                        "campaign_rate": 90
                    }
            }
            rtb = ext1_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=test_mode_device_id,
                                                header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                              rtb_selector=rtb, override_bid_ext=json.dumps(Override_Bid_Ext)))
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            seatbid = bid_response[rtb]['seatbid']
            adm = seatbid[0]['bid'][0]['adm']

            if 'sleep' not in ad_markup:
                templateURL = ad_markup['templateURL']
                if 'rtbVideo.zip' in templateURL:
                    assert 'VAST' in adm
            elif 'sleep' in ad_markup:
                assert_keys_not_exist(seatbid[0]['bid'][0], 'attr')
                assert_keys_not_exist(seatbid[0]['bid'][0]['ext'], 'crtype')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.'
                  'PBJ-3674 Internal Kraken need to implement same ad-size logic with '
                  'Meister and External Kraken need to support deprecate the adm type configuration'
                  )
    @allure.description('Verify jaeger will server when request banner+video impression for '
                        'Interstitial&rewarded via non test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_crtype_attr_01])
    def test_fullscreen_bid_response_non_test_mode_edsp(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                                header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                              rtb_selector=rtb))
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            templateURL = ad_markup['templateURL']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            seatbid = bid_response[rtb]['seatbid']
            adm = seatbid[0]['bid'][0]['adm']

            if 'rtbVideo.zip' in templateURL:
                assert 'VAST' in adm
            elif 'programmaticFullscreenPlayable.zip' in templateURL:
                assert_that(seatbid[0]['bid'][0]['attr'][0], equal_to(13))
                assert_that(seatbid[0]['bid'][0]['ext']['crtype'], equal_to('MRAID 2.0'))

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.'
                  'PBJ-3674 Internal Kraken need to implement same ad-size logic with '
                  'Meister and External Kraken need to support deprecate the adm type configuration'
                  'PBJ-3756 Check "attr=13" in the bid response for programmatic playables'
                  )
    @allure.description('Verify jaeger will server when request banner+video impression for '
                        'Interstitial&rewarded via non test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_01,
                                           ])
    def test_fullscreen_bid_response_non_test_mode_edsp_no_mraid_version(self, pub_app_id, placement):
        Override_Bid_Ext = {
            "vungle":
                {
                    "ad_app_object_id": "4ee19fb8121ae61a03000022",
                    "ad_app_store_id": "adv-store-id",
                    "vid": "562721e66ddcba3a68000053",
                    "attribution_method": "skadnetwork",
                    "campaign_rate_type": "target_cpi",
                    "campaign_rate": 90
                }
        }
        if env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                                header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                              rtb_selector=rtb, override_bid_ext=json.dumps(Override_Bid_Ext)))
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            seatbid = bid_response[rtb]['seatbid']
            adm = seatbid[0]['bid'][0]['adm']

            if 'sleep' not in ad_markup:
                templateURL = ad_markup['templateURL']
                if 'rtbVideo.zip' in templateURL:
                    assert 'VAST' in adm
            elif 'sleep' in ad_markup:
                assert_keys_not_exist(seatbid[0]['bid'][0], 'attr')
                assert_keys_not_exist(seatbid[0]['bid'][0]['ext'], 'crtype')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.'
                  'PBJ-3674 Internal Kraken need to implement same ad-size logic with '
                  'Meister and External Kraken need to support deprecate the adm type configuration'
                  'PBJ-3756 Check "attr=13" in the bid response for programmatic playables'
                  'PBJ-4019 Do Not Reject bid response with Mraid 2.0 but not with attr=13'
                  )
    @allure.description('Verify jaeger will server when request banner+video impression for '
                        'Interstitial&rewarded via non test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_attr_02])
    def test_fullscreen_bid_response_non_test_mode_edsp_no_mraid_version_01(self, pub_app_id, placement):
        # no attr=13 response
        Override_Bid_Ext = {
            "crtype": "MRAID 2.0",
        }
        if env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_mraid.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                                header_bidding=True)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=fr_ip,
                                              rtb_selector=rtb, override_bid_ext=json.dumps(Override_Bid_Ext)))
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            seatbid = bid_response[rtb]['seatbid']
            adm = seatbid[0]['bid'][0]['adm']
            assert_keys_not_exist(ad_markup, 'sleep')
            templateURL = ad_markup['templateURL']
            assert 'programmaticFullscreen-v4.zip' in templateURL

    @allure.feature('fullscreen playable')
    @allure.tag('smoke', 'test_mode')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.'
                  'PBJ-3674 Internal Kraken need to implement same ad-size logic with '
                  'Meister and External Kraken need to support deprecate the adm type configuration'
                  )
    @allure.description('Verify jaeger will server when request banner+video impression for '
                        'Interstitial&rewarded via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_01])
    def test_fullscreen_bid_response_test_mode_idsp(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids_1.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=test_mode_device_id,
                                                header_bidding=False)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                              rtb_selector=rtb))
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            assert_keys_not_exist(ad_markup, 'info')

    @allure.feature('fullscreen playable')
    @allure.tag('smoke')
    @allure.story('PBJ-3351 Implement Jaeger side support for fullscreen playable ads.'
                  'PBJ-3674 Internal Kraken need to implement same ad-size logic with '
                  'Meister and External Kraken need to support deprecate the adm type configuration'
                  )
    @allure.description('Verify jaeger will server when request banner+video impression for '
                        'Interstitial&rewarded via non test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_third_party_placement_crtype_01])
    def test_fullscreen_bid_response_non_test_mode_idsp(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = non_test_mode_kraken_rtb_ids.split(',')[1]
            req = request_payload.jaeger_v5_ios(pub_app_id=pub_app_id, placement_id=placement, ifa=gen_device_id(),
                                                header_bidding=False)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                              rtb_selector=rtb))
            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']
            assert_keys_not_exist(ad_markup, 'info')

    @allure.feature('kraken features')
    @allure.tag('normal', 'v0.24.0', 'test_mode')
    @allure.story('PBJ-4195 Return valid ad_market_id in ad response')
    @allure.description('Verify that Kraken get the market id from meta file for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_kraken_returns_valid_ad_market_id_1(self, pub_app_id, placement):
        '''
            meta config for multiple page iOS:
            "ad_market_id": "1046740065"

            ADM config:
            null
        '''
        if env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]

            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle'], equal_to('1046740065'))

    @allure.feature('kraken features')
    @allure.tag('normal', 'v0.24.0', 'test_mode')
    @allure.story('PBJ-4195 Return valid ad_market_id in ad response')
    @allure.description('Verify that Kraken get the default hard-coded valid market id for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_single_page])
    def test_kraken_returns_valid_ad_market_id_2(self, pub_app_id, placement):
        '''
            meta config for single page iOS:
            null

            ADM config:
            null

            Default:
            "ad_market_id": "1046740065"
        '''
        if env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]

            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle'], equal_to('1046740065'))

    @allure.feature('kraken features')
    @allure.tag('normal', 'v0.24.0', 'test_mode')
    @allure.story('PBJ-4195 Return valid ad_market_id in ad response')
    @allure.description('Verify that Kraken get valid market id from ADM first for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_kraken_returns_valid_ad_market_id_3(self, pub_app_id, placement):
        '''
            meta config for Android:
            "ad_market_id": "com.vungle.games.tossacoin"

            ADM config:
            "ad_market_id": "com.vungle.games.tossacoin.test"
        '''
        if env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]

            req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle'],
                        equal_to('com.vungle.games.tossacoin.test'))

    @allure.feature('kraken features')
    @allure.tag('normal', 'v0.24.0', 'test_mode')
    @allure.story('PBJ-4195 Return valid ad_market_id in ad response')
    @allure.description('Verify that Kraken get the market id from meta file for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_kraken_returns_valid_ad_market_id_4(self, pub_app_id, placement):
        '''
            meta config for vast iOS:
            "ad_market_id": "1490962424"
        '''
        if env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]

            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle'], equal_to('1490962424'))

    @allure.feature('kraken features')
    @allure.tag('normal', 'v0.24.0', 'test_mode')
    @allure.story('PBJ-4195 Return valid ad_market_id in ad response')
    @allure.description('Verify that Kraken get the default hard-coded valid market id for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_kraken_returns_valid_ad_market_id_5(self, pub_app_id, placement):
        '''
            meta config for Android:
            null

            Default:
            "ad_market_id": "com.vungle.games.tossacoin"
        '''
        if env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]

            req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['bundle'], equal_to('com.vungle.games.tossacoin'))

    @allure.feature('external Notifications')
    @allure.tag('normal', 'v1.235.0', 'test_mode')
    @allure.story('PBJ-4612 Look into LO side questions about win notification')
    @allure.description('Verify the auction id fix on win notification url at Jaeger auction')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_win_notification_jaeger_auction_fix_1(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]
            # mock nurl
            nurl = "http://kraken-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}&auction_id=${AUCTION_ID}"
            override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % nurl

            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                              override_bid_response_any=override_bid_response_any))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['nurl'], equal_to(nurl))
            # check the rtb id
            # verify the kraken-apiqa pod will receive log like:
            # {"level":"info","msg":"Got notifications: /nurl?price=98.000000000&ex_price=&auction_id=632ac1c6ffd35d35adb4e421"}

    @allure.feature('external Notifications')
    @allure.tag('normal', 'v1.235.0', 'test_mode')
    @allure.story('PBJ-4612 Look into LO side questions about win notification')
    @allure.description('Verify the auction id fix on loss notification url at Jaeger auction')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_win_notification_jaeger_auction_fix_2(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            # mock vungle loss
            rtb = test_mode_kraken_int1_rtb_ids.split(',')[1] + ',' + \
                  ext_test_mode_kraken_rtb_ids_vast_liftoff_notification.split(',')[1]
            # mock lurl
            lurl = "http://kraken-int1-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?mbtw=${MIN_BID_TO_WIN}&exbtw=${EX_MIN_BID_TO_WIN}&exbtwv=${EX_MIN_BID_TO_WIN_V}&auction_id=${AUCTION_ID}"
            override_bid_response_any = 'seatbid.0.bid.0.lurl@"%s"' % lurl

            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                              override_bid_response_any=override_bid_response_any))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.ads_v5)

            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_that(bid_response[test_mode_kraken_int1_rtb_ids.split(',')[1]]['seatbid'][0]['bid'][0]['lurl'],
                        equal_to(lurl))
            # check the rtb id
            # verify the kraken-int1 pod will receive log like:
            # {"level":"info","msg":"Got notifications: /lurl?mbtw=98.000000000&exbtw=1.090000000&exbtwv=98.000000000&auction_id=632ac1c6ffd35d35adb4e421"}


