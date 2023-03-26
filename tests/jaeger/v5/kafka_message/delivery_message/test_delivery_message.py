import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain, request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain, get_bid_response_obj_from_jaeger_explain, get_ext_debug_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema
import json



@allure.epic('jaeger v5')
@allure.feature('message')
@allure.feature('as-deliveries')
class TestDeliveryMessage(object):

    @allure.tag('basic')
    @allure.story('auto cache')
    @allure.story('PBJ-4050 [Jaeger]Support A/B testing for auto-cache')
    @allure.description('Verify experiment info \'PlacementIsAutoCached\' was record to delivery message')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_auto_cache_experiment_01(self, pub_app_id):
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_rewarded_placement, ifa='df4f1de5-9225-46f5-b363-f8d776934da9')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids, sdk_version='Vungle/6.10.3',
                                                                        src_ip=fr_ip, debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'exp_to_bucket', is {\\"AutoCache_2022_Phase1\\":\\""AutoCache\\""}",
        # and check field:   "placement_is_auto_cached":true,
        # send delivery message only for non test mode idsp and meister.



    @allure.tag('basic')
    @allure.story('auto cache')
    @allure.story('PBJ-4068 [Jaeger] Read experiments from config extension for recording')
    @allure.description('Verify experiment info \'PlacementIsAutoCached\' was record to delivery message when request '
                        'ads with config extension over 6.11+')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_auto_cache_experiment_config_extension_01(self, pub_app_id):
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_rewarded_placement, ifa=gen_device_id(),
                                                ext=config_extension_1)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids, sdk_version='Vungle/6.11.1',
                                                                        src_ip=fr_ip, debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'exp_to_bucket' is {\\"AutoCache_2022_Phase1\\":\\""AutoCache\\"",
        # \\"KONAVerifyAB_4068\\":\\"KONAAB2\\"}",
        # and check field:   "placement_is_auto_cached":true,
        # send delivery message only for non test mode idsp and meister.


    @allure.tag('basic')
    @allure.story('auto cache')
    @allure.story('PBJ-4068 [Jaeger] Read experiments from config extension for recording')
    @allure.description('Verify experiment info \'PlacementIsAutoCached\' was record to delivery message when request '
                        'ads without config extension over 6.11+')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_auto_cache_experiment_config_extension_02(self, pub_app_id):
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_rewarded_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids, sdk_version='Vungle/6.11.1',
                                                                        src_ip=fr_ip, debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'exp_to_bucket' is {\\"AutoCache_2022_Phase1\\":\\""AutoCache\\"",
        # \\"KONAVerifyAB_4068\\":\\"KONAAB2\\"}",
        # and check field:   "placement_is_auto_cached":true,
        # send delivery message only for non test mode idsp and meister.



    @allure.tag('basic')
    @allure.story('auto cache')
    @allure.story('PBJ-4068 [Jaeger] Read experiments from config extension for recording')
    @allure.description('Verify experiment info \'PlacementIsAutoCached\' was record to delivery message when request '
                        'ads with config extension and no IFA over 6.11+')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_auto_cache_experiment_config_extension_03(self, pub_app_id):
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_rewarded_placement, ifa="",
                                                ext=config_extension_1)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids, sdk_version='Vungle/6.11.1',
                                                                        src_ip=fr_ip, debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'exp_to_bucket', is {\\"AutoCache_2022_Phase1\\":\\""AutoCache\\"",
        # \\"KONAVerifyAB_4068\\":\\"KONAAB2\\"}",
        # and check field:   "placement_is_auto_cached":true,
        # send delivery message only for non test mode idsp and meister.


    @allure.tag('basic')
    @allure.story('auto cache')
    @allure.story('PBJ-4068 [Jaeger] Read experiments from config extension for recording')
    @allure.description('Verify experiment info \'PlacementIsAutoCached\' was record to delivery message when request '
                        'ads without config extension and no IFA over 6.11+')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_auto_cache_experiment_config_extension_04(self, pub_app_id):
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_rewarded_placement, ifa="")
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids, sdk_version='Vungle/6.11.1',
                                                                        src_ip=fr_ip, debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'exp_to_bucket', is {\\"AutoCache_2022_Phase1\\":\\""AutoCache\\"",
        # \\"KONAVerifyAB_4068\\":\\"KONAAB2\\"}",
        # and check field:   "placement_is_auto_cached":true,
        # send delivery message only for non test mode idsp and meister.



    @allure.tag('basic')
    @allure.story('auto cache')
    @allure.story('PBJ-4068 [Jaeger] Read experiments from config extension for recording')
    @allure.description('Verify experiment info \'PlacementIsAutoCached\' was record to delivery message when request '
                        'ads with previous config extension over 6.11+')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_auto_cache_experiment_config_extension_05(self, pub_app_id):
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_rewarded_placement, ifa=gen_device_id(),
                                                ext=config_extension)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids, sdk_version='Vungle/6.11.1',
                                                                        src_ip=fr_ip, debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'exp_to_bucket', is {\\"AutoCache_2022_Phase1\\":\\""AutoCache\\"",
        # \\"KONAVerifyAB_4068\\":\\"KONAAB2\\"}",
        # and check field:   "placement_is_auto_cached":true,
        # send delivery message only for non test mode idsp and meister.




    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3992 PBJ-3992 Log "SKO Auto Allowed" & other SKO related signals so that Vungle DS can'
                  ' consumer later on')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_adv_pref_skfsc_default.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_adv_pref_skfsc_default.split('|')[1]])
    def test_sko_liftoff_1(self, pub_app_id, placement):
        """
            app level: FSC=adv_pref, SK_FSC=default
            placement level: FSC=inherit
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_liftoff))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('default'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('adv_pref'))
        # check sk_experience=default and video_click_area='adv_pref'
        # added to 'as-requestAds'



    @allure.tag('basic', 'v1.216.0')
    @allure.story('experiment')
    @allure.story('PBJ-4193 2022 Ad download optimization experiment'
                  'PBJ-4438 Remove autocache flag override for ADO experiment'
                  'PBJ-4493 Change version whitelist for DO_2022_phase2')
    @allure.description('Verify the experiment info is added in transaction message and autocached is false'
                        'for enter experiment pub app'
                        'Verify that the experiment will not impact the autocache flag'
                        'Verify that sdk version > 6.11 will enter the experiment')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    def test_ad_download_opt_01(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.jaeger_v5_ios(pub_app_id, "DEFAULT02024", ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, ext=config_extension_do_exp_with_on)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=meister_rtb_ids,
                                          sdk_version='Vungle/6.11.3',
                                          src_ip=au_ip, debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'exp_to_bucket', is {\\"DownloadOptimization_2022\\":\\""Optimization_ON\\""}",
        # "is_ad_download_optimized":true,

    @allure.tag('basic', 'v1.216.0')
    @allure.story('experiment')
    @allure.story('PBJ-4193 2022 Ad download optimization experiment'
                  'PBJ-4438 Remove autocache flag override for ADO experiment'
                  'PBJ-4493 Change version whitelist for DO_2022_phase2')
    @allure.description('Verify the experiment info is added in transaction message and autocached is false'
                        'for enter experiment pub app'
                        'Verify that the experiment will not impact the autocache flag'
                        'Verify that sdk version > 6.11 will enter the experiment')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    def test_ad_download_opt_02(self, pub_app_id):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.jaeger_v5_ios(pub_app_id, "DEFAULT02024", ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, ext=config_extension_do_exp_with_off)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=meister_rtb_ids,
                                          sdk_version='Vungle/6.11.3',
                                          src_ip=au_ip, debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'exp_to_bucket', is {\\"DownloadOptimization_2022\\":\\""Optimization_OFF\\""}",
        # "is_ad_download_optimized":false,


    @allure.tag('basic', 'v1.216.0')
    @allure.story('experiment')
    @allure.story('PBJ-4193 2022 Ad download optimization experiment'
                  'PBJ-4438 Remove autocache flag override for ADO experiment'
                  'PBJ-4493 Change version whitelist for DO_2022_phase2')
    @allure.description('Verify the experiment info is added in transaction message and autocached is false'
                        'for enter experiment pub app'
                        'Verify that the experiment will not impact the autocache flag'
                        'Verify that sdk version < 6.11 will enter the experiment')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('ext', [config_extension_do_exp_with_on, config_extension_do_exp_with_off, ''])
    def test_ad_download_opt_03(self, pub_app_id, ext):
        network_ids = ["test.ad.nw.001", "test.nw.45646546"]
        req = request_payload.jaeger_v5_ios(pub_app_id, "DEFAULT02024", ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, ext=ext)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=meister_rtb_ids,
                                          sdk_version='Vungle/6.10.3',
                                          src_ip=au_ip, debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify no 'DownloadOptimization_2022' in 'exp_to_bucket'",




    @allure.tag('basic', 'v1.225.0 ')
    @allure.story('campaign A/B test')
    @allure.story('PBJ-4202 Add a new field in `as-deliveries` to identify the campaign A/B test state')
    @allure.description('Verify that new field `creative_ab_set` is added')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_add_field_for_campaign_AB_test(self, pub_app_id):
        Override_Bid_Ext = {
            "vungle":
            {
                "ad_app_object_id": "4ee19fb8121ae61a03000022",
                "ad_app_store_id": "adv-store-id",
                "vid": "562721e66ddcba3a68000053",
                "attribution_method": "skadnetwork",
                "campaign_rate_type": "target_cpi",
                "campaign_rate": 110,
                "creative_ab_set": "b"
            }
        }
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_rewarded_placement, ifa='df4f1de5-9225-46f5-b363-f8d776934da9')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids, sdk_version='Vungle/6.10.3',
                                                                        src_ip=fr_ip, override_bid_ext=json.dumps(Override_Bid_Ext),
                                                                        debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # check field:   "creative_ab_set":"b",

    @allure.tag('basic', 'v1.225.0 ')
    @allure.story('campaign A/B test')
    @allure.story('PBJ-4202 Add a new field in `as-deliveries` to identify the campaign A/B test state')
    @allure.description('Verify that new field `creative_ab_set` is added')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_add_field_for_campaign_AB_test_02(self, pub_app_id):
        Override_Bid_Ext = {
            "vungle":
                {
                    "ad_app_object_id": "4ee19fb8121ae61a03000022",
                    "ad_app_store_id": "adv-store-id",
                    "vid": "562721e66ddcba3a68000053",
                    "attribution_method": "skadnetwork",
                    "campaign_rate_type": "target_cpi",
                    "campaign_rate": 110,
                    "creative_ab_set": "a"
                }

        }
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_rewarded_placement,
                                                ifa='df4f1de5-9225-46f5-b363-f8d776934da9')
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids, sdk_version='Vungle/6.10.3',
                                          src_ip=fr_ip, override_bid_ext=json.dumps(Override_Bid_Ext),
                                          debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # check field:   "creative_ab_set":"a",

    # @allure.feature('S2S')
    # @allure.tag('normal')
    # @allure.story('PBJ-4432 S2S - write partner field to s2s_partner in delivery/transaction')
    # @allure.description('Verify s2s request will send \'S2SPartner\' field to delivery message')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement_id', [common_test_placement])
    # def test_s2s_record_in_delivery_message(self, pub_app_id, placement_id):
    #     test_ifa = gen_device_id()
    #     req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa)
    #     r = post(s2s_v5_sigmob_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=None,
    #                                       rtb_selector=meister_rtb_ids))
    #     assert_that(r.status_code, equal_to(HTTPStatus.OK))
    #     # Verify that s2s_partner has been recorded



    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4406 Add ADO dimension in reporting')
    @allure.description('Verify that the is_ad_download_optimized is added to delivery')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_record_is_ado_to_delivery_01(self, pub_app_id, placement_id):
        '''

       'ad_load_optimization_enabled= True' setting in DB
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        # assert 'is_ad_download_optimized = true in message



    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4406 Add ADO dimension in reporting')
    @allure.description('Verify that the is_ad_download_optimized = false if the traffic is enter the ADO exp')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_record_is_ado_to_delivery_02(self, pub_app_id, placement_id):
        '''

       'ad_load_optimization_enabled= True' setting in DB
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=it_ip, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        # assert 'is_ad_download_optimized = false in message



    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4406 Add ADO dimension in reporting')
    @allure.description('Verify that the is_ad_download_optimized is added to delivery')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    def test_record_is_ado_to_delivery_03(self, pub_app_id, placement_id):
        '''

       'ad_load_optimization_enabled= false' setting in DB
        '''
        req = request_payload.jaeger_v5_android(pub_app_id, placement_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids, debug='jaeger'))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        # assert 'is_ad_download_optimized = false in message



    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4406 Add ADO dimension in reporting')
    @allure.description('Verify that the is_ad_download_optimized is added to delivery')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement_id', [common_test_placement_2])
    def test_record_is_ado_to_delivery_04(self, pub_app_id, placement_id):
        '''

       no setting 'ad_load_optimization_enabled= false'in DB
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        # assert 'is_ad_download_optimized = false in message

    @allure.tag('basic')
    @allure.story('campaign A/B test')
    @allure.story('PBJ-4444 add new field `campaign_ab_test_id` to `as-deliveries`')
    @allure.description('Verify that new field `campaign_ab_test_id` is added')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_add_field_for_campaign_AB_test_03(self, pub_app_id):
        Override_Bid_Ext = {
            "vungle":
                {
                    "ad_app_object_id": "4ee19fb8121ae61a03000022",
                    "ad_app_store_id": "adv-store-id",
                    "vid": "562721e66ddcba3a68000053",
                    "attribution_method": "skadnetwork",
                    "campaign_rate_type": "target_cpi",
                    "campaign_rate": 110,
                    "campaign_ab_test_id": 121212
                }

        }
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_rewarded_placement,
                                                ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids, sdk_version='Vungle/6.10.3',
                                          src_ip=fr_ip, override_bid_ext=json.dumps(Override_Bid_Ext),
                                          debug='jaeger'))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # check field:   "campaign_ab_test_id":"emilyTest",


    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4611 Be able to record 3page publisher settings in the looker.')
    @allure.description('Verify the publisher setting has been recorded to delivery')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_01(self, pub_app_id, placement, sdk_v):
        """

        app setting:
        allow_static_endcard: true
        allow_skip_button: true
        allow_storekit_transition:true
        static_ec_close_button_delay:25

        placement no setting
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        # Verified in delivery:
        #   "allow_static_endcard":true,
        #   "allow_skip_button":true,
        #   "allow_storekit_transition":true,
        #   "static_ec_close_button_delay":25


    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4611 Be able to record 3page publisher settings in the looker.')
    @allure.description('Verify the publisher setting has been recorded to delivery')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_02(self, pub_app_id, placement, sdk_v):
        """

        app setting:
        allow_static_endcard: true
        allow_skip_button: true
        allow_storekit_transition:true
        static_ec_close_button_delay:25

        placement setting:
        static_ec_close_button_delay:3
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        # Verified in delivery:
        #   "allow_static_endcard":true,
        #   "allow_skip_button":true,
        #   "allow_storekit_transition":true,
        #   "static_ec_close_button_delay": 3


    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4611 Be able to record 3page publisher settings in the looker.')
    @allure.description('Verify the publisher setting has been recorded to delivery')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_03(self, pub_app_id, placement, sdk_v):
        """

        app setting:
        allow_static_endcard: false
        allow_skip_button: false
        allow_storekit_transition:false


         placement setting:
         static_ec_close_button_delay:13
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        # Verified in delivery:
        #   "allow_static_endcard":false,
        #   "allow_skip_button":false,
        #   "allow_storekit_transition":fasle,
        #   "static_ec_close_button_delay": 13




    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4611 Be able to record 3page publisher settings in the looker.')
    @allure.description('Verify the publisher setting has been recorded to delivery')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_04(self, pub_app_id, placement, sdk_v):
        """

        app no setting:


        placement setting:
        static_ec_close_button_delay:16
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        # Verified in delivery:
        #   "allow_static_endcard":true (default),
        #   "allow_skip_button":true (default),
        #   "allow_storekit_transition":true (default),
        #   "static_ec_close_button_delay": 16

    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4611 Be able to record 3page publisher settings in the looker.')
    @allure.description('Verify the publisher setting has been recorded to delivery')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_finally_delivery_static_endcard_01(self, pub_app_id, placement, sdk_v):
        """

        app setting:
        allow_static_endcard: true
        static_ec_close_button_delay:25

        placement no setting

        creative setting:

        """
        # over_ride_adm = 'seatbid.0.bid.0.adm@"{\'id\': \'63297d1e3ff0b881298a2015\',\'campaign\': \'5eb9877e136f432531e6f285|5eb9a49a5ddc02539da7c732|test-ads|63297d1e3ff0b881298a2015\',\'app_id\': \'$0${\\\"app_id\\\":\\\"5dc44eacf080325a55721f8f\\\",\\\"eventID\\\":\\\"63297d1e3ff0b881298a2015\\\"}\",\"expiry\": 1589902809,\"tpat\": {\"moat\": {\"is_enabled\": false,\"extra_vast\": \"\"},\"clickUrl\": [\"https:\/\/apps.apple.com\/us\/app\/toss-a-coin\/id1046740065?uo=4\"],\"checkpoint.0\": [\"https:\/\/ingest.vungle.com\/tpat?event_id=63297d1e3ff0b881298a2015&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0\",\"https:\/\/events.api.vungle.com\/v1\/tpat?event_id=63297d1e3ff0b881298a2015&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=start\"],\"checkpoint.25\": [\"https:\/\/ingest.vungle.com\/tpat?event_id=63297d1e3ff0b881298a2015&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.25\",\"https:\/\/events.api.vungle.com\/v1\/tpat?event_id=63297d1e3ff0b881298a2015&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=firstQuartile\"],\"checkpoint.50\": [\"https:\/\/ingest.vungle.com\/tpat?event_id=63297d1e3ff0b881298a2015&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.5\",\"https:\/\/events.api.vungle.com\/v1\/tpat?event_id=63297d1e3ff0b881298a2015&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=midpoint\"],\"checkpoint.75\": [\"https:\/\/ingest.vungle.com\/tpat?event_id=63297d1e3ff0b881298a2015&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.75\",\"https:\/\/events.api.vungle.com\/v1\/tpat?event_id=63297d1e3ff0b881298a2015&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=thirdQuartile\"],\"checkpoint.100\": [\"https:\/\/ingest.vungle.com\/tpat?event_id=63297d1e3ff0b881298a2015&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=1\",\"https:\/\/events.api.vungle.com\/v1\/tpat?event_id=63297d1e3ff0b881298a2015&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=complete\"],\"postroll.view\": [\"https:\/\/ingest.vungle.com\/tpat?event_id=63297d1e3ff0b881298a2015&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_VIEW\",\"https:\/\/events.api.vungle.com\/v1\/tpat?event_id=63297d1e3ff0b881298a2015&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_view\"],\"postroll.click\": [\"https:\/\/ingest.vungle.com\/tpat?event_id=63297d1e3ff0b881298a2015&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_CLICK\",\"https:\/\/events.api.vungle.com\/v1\/tpat?event_id=63297d1e3ff0b881298a2015&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_click\"],\"video.close\": [\"https:\/\/ingest.vungle.com\/tpat?event_id=63297d1e3ff0b881298a2015&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=VIDEO_CLOSE\",\"https:\/\/events.api.vungle.com\/v1\/tpat?event_id=63297d1e3ff0b881298a2015&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=video_close\"],\"video.unmute\": [\"https:\/\/ingest.vungle.com\/tpat?event_id=63297d1e3ff0b881298a2015&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=UNMUTE\",\"https:\/\/events.api.vungle.com\/v1\/tpat?event_id=63297d1e3ff0b881298a2015&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=unmute\"],\"video.mute\": [\"https:\/\/ingest.vungle.com\/tpat?event_id=63297d1e3ff0b881298a2015&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=MUTE\",\"https:\/\/events.api.vungle.com\/v1\/tpat?event_id=63297d1e3ff0b881298a2015&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=mute\"],\"closeButtonClick\": [\"http:\/\/ingest.vungle.com\/tpat?event_id=563d9a4f044e3a06363808af&event_type=close_button_click\"],\"nearCloseButtonClick\": [\"http:\/\/ingest.vungle.com\/tpat?event_id=563d9a4f044e3a06363808af&event_type=near_close_button_click\"],\"download.ctaClick\": [\"http:\/\/ingest.vungle.com\/tpat?event_id=563d9a4f044e3a06363808af&event_type=cta_click\"],\"download.fullScreenClick\": [\"http:\/\/ingest.vungle.com\/tpat?event_id=563d9a4f044e3a06363808af&event_type=fullscreen_click\"],\"muteButtonClick\": [\"http:\/\/ingest.vungle.com\/tpat?event_id=563d9a4f044e3a06363808af&event_type=mute_button_click\"],\"privacyButtonClick\": [\"http:\/\/ingest.vungle.com\/tpat?event_id=563d9a4f044e3a06363808af&event_type=privacy_button_click\"],\"storeKitOverlay.autoOpen.storeEndcardTimer\": [\"http:\/\/ingest.vungle.com\/tpat?event_id=563d9a4f044e3a06363808af&event_type=store_kit_overlay_auto_open\"],\"playableEndcardClick\": [\"https:\/\/tpat-qa.api.vungle.io\/v1\/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=playable_endcard_click\"],\"download.ASOIInteraction\": [\"https:\/\/tpat-qa.api.vungle.io\/v1\/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_interaction\"],\"download.ASOIComplete\": [\"https:\/\/tpat-qa.api.vungle.io\/v1\/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_complete\"]},\"delay\": 0,\"showClose\": 9999,\"showCloseIncentivized\": 9999,\"countdown\": 0,\"url\": \"\",\"videoWidth\": 0,\"videoHeight\": 0,\"md5\": \"fake_md5\",\"callToActionDest\": \"https:\/\/apps.apple.com\/us\/app\/toss-a-coin\/id1046740065?uo=4&ppid=313f8c39-0eb3-45ad-88ff-891559d47302\",\"callToActionUrl\": \"https:\/\/apps.apple.com\/us\/app\/toss-a-coin\/id1046740065?uo=4\",\"adType\": \"vungle_mraid\",\"templateURL\": \"https:\/\/cdn-lb.vungle.com\/templates\/88f37b43a983d8700fc2b7a0ca4b5a37.zip\",\"templateSettings\": {\"normal_replacements\": {\"INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS\": \"9999\",\"INCENTIVIZED_CONTINUE_TEXT\": \"Continue\",\"PRIVACY_BODY_TEXT\": \"Vungle, Inc. understands the importance of privacy. Vungle operates a mobile ad network (the \'Ad Network\' or the \'Services\') through which Vungle displays targeted, contextual ads.\",\"VUNGLE_PRIVACY_URL\": \"https:\/\/privacy.vungle.com\/\",\"APP_NAME\": \"Toss a Coin\",\"CTA_BUTTON_BACKGROUND\": \"#01b27a\",\"CTA_BUTTON_TEXT\": \"Download\",\"START_MUTED\": \"true\",\"AUTO_LOCALIZE\": \"true\",\"CLOSE_BUTTON_DELAY_SECONDS\": \"9999\",\"FULL_CTA\": \"true\",\"APP_DESCRIPTION\": \"Vungle\",\"CTA_BUTTON_URL\": \"https:\/\/apps.apple.com\/us\/app\/angry-birds-2\/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302&durl=https%3A%2F%2Fapp.adjust.com\",\"PRIVACY_CLOSE_TEXT\": \"Read Vungle\'s Privacy Policy\",\"INCENTIVIZED_TITLE_TEXT\": \"Close this ad?\",\"PRIVACY_CONTINUE_TEXT\": \"Close\",\"THEME\": \"dark\",\"ACTION_TRACKING\": \"false\",\"INCENTIVIZED_BODY_TEXT\": \"Are you sure you want to skip this ad? You must finish watching to claim your reward.\",\"INCENTIVIZED_CLOSE_TEXT\": \"Close\",\"VIDEO_PROGRESS_BAR\": \"true\",\"SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN\": \"true\",\"SHOW_EC_CLOSE_BUTTON_COUNTDOWN\": \"false\",\"SK_CTA_ONLY\": \"product_view\",\"SK_ASOI_COMPLETE\": \"off\",\"SK_ASOI_AGGRESSIVE\": \"default\",\"SK_FSC\": \"overlay_view\"},\"cacheable_replacements\": {\"CAROUSEL_IMAGE_3\": {\"url\": \"https:\/\/cdn-lb.vungle.com\/templates\/creative_assets\/5eb9a49a5ddc02539da7c732\/1589224580023-Screen_Shot_2020-05-11_at_12.16.02_PM.png\",\"extension\": \"png\"},\"MAIN_VIDEO\": {\"url\": \"https:\/\/cdn-lb.vungle.com\/zen\/OYOC0703-720x1280-Q2.mp4\",\"extension\": \"mp4\"},\"POWERED_BY_VUNGLE\": {\"url\": \"https:\/\/cdn-lb.vungle.com\/templates\/defaults\/img\/vungle.svg\",\"extension\": \"svg\"},\"APP_ICON\": {\"url\": \"https:\/\/cdn-lb.vungle.com\/templates\/creative_assets\/5eb9a49a5ddc02539da7c732\/1589224409047-Toss-a-coin_icon_copy.png\",\"extension\": \"png\"},\"APP_RATING\": {\"url\": \"https:\/\/cdn-lb.vungle.com\/templates\/defaults\/img\/4.5-stars.svg\",\"extension\": \"svg\"},\"CAROUSEL_IMAGE_1\": {\"url\": \"https:\/\/cdn-lb.vungle.com\/templates\/creative_assets\/5eb9a49a5ddc02539da7c732\/1589224575863-Screen_Shot_2020-05-11_at_12.16.02_PM.png\",\"extension\": \"png\"},\"CAROUSEL_IMAGE_2\": {\"url\": \"https:\/\/cdn-lb.vungle.com\/templates\/creative_assets\/5eb9a49a5ddc02539da7c732\/1589224584145-Screen_Shot_2020-05-11_at_12.16.02_PM.png\",\"extension\": \"png\"},\"FONT_URL\": {\"url\": \"https:\/\/fonts.gstatic.com\/s\/opensans\/v13\/cJZKeOuBrn4kERxqtaUH3SZ2oysoEQEeKwjgmXLRnTc.ttf\",\"extension\": \"ttf\"}}},\"templateId\": \"58c2f62c34f5e387180003fa\",\"template_type\": \"multi_page_fullscreen\",\"ad_market_id\": \"\",\"chk\": \"fake_chk\",\"retryCount\": 3,\"asyncThreshold\": 40,\"ad_token\": \"eyJjYW1wYWlnbiI6IjVlYjk4NzdlMTM2ZjQzMjUzMWU2ZjI4NXw1ZWI5YTQ5YTVkZGMwMjUzOWRhN2M3MzJ8ZGF0YXNjaS0tYmxyXzIwMTkxMTAxX3ZpZXdfY3RzXzM2NV9oZHdfbGF0X3NnZF9leHBsb2l0LS1zdWNjZXNzLS1tZWlzdGVyfDVlYmFjMzU5ODk1NWYzMDAwMTljNmUxZSJ9\",\"video_object_id\": \"5eb98e4ba71f20254c64ada9\",\"requires_sideloading\": false,\"bid_token\": \"1|c173ad44d14fe336627037a99a41e47372dff0af|bqtc6mecpo6uqhq83f20\",\'data_science_cache\': \'\'}"'
        # over_ride_adm = over_ride_adm.replace("\/" ,"/").replace('\"', '\\\'')
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=meister_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger'))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        # Verified in delivery:
        #   "allow_static_endcard":true,
        #   "allow_skip_button":true,
        #   "allow_storekit_transition":true,
        #   "static_ec_close_button_delay":25



    @allure.tag('lmt flag')
    @allure.story('normal')
    @allure.story('PBJ-4848 RTA - pass lmt for realtime HB request by config extension')
    @allure.description('Verify do_not_track flag is consisent with config extension in realtime token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_lmt_flag_0(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                config_extension=config_extension_lmt_flag_0)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # Verify that do_not_track=false in delivery



    @allure.tag('lmt flag')
    @allure.story('normal')
    @allure.story('PBJ-4848 RTA - pass lmt for realtime HB request by config extension')
    @allure.description('Verify do_not_track flag is consisent with config extension in realtime token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_lmt_flag_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                config_extension=config_extension_lmt_flag_1)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # Verify that do_not_track=true in delivery



    @allure.tag('lmt flag')
    @allure.story('normal')
    @allure.story('PBJ-4848 RTA - pass lmt for realtime HB request by config extension')
    @allure.description('Verify lmt flag is consisent with config extension in realtime token')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement, common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_lmt_flag_original(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                config_extension=config_extension_1)
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            # Verify that do_not_track=false in delivery: casuse no lmt flag in config_extension, will use bid_request.lmt value


    @allure.story('Real Time Experiment')
    @allure.tag('basic')
    @allure.story('PBJ-4876 RTA - use all data source from SDK instead of mediation partner')
    @allure.description('Verify that all fields will rely on the sdk')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_realtime_exp])
    @pytest.mark.parametrize('placement_id', [common_test_pre_cache_placement])
    def test_realtime_exp_fields_checked_delivery(self, pub_app_id, placement_id):

        try:
            info = request_hbp_with_real_time_token('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement_id,
                                                    rtb=test_mode_kraken_rtb_ids, ads_retry_mode='meister',
                                                    test_device_id=test_mode_device_id, ads_debug='jaeger',
                                                    no_pre_cache_token=False, ip=au_ip,
                                                    sdk_v=test_default_real_time_sdk_version,
                                                    explain='jaeger', config_extension=config_extension_RTA)

            if info['is_hbp_responded_200']:
                response_payload = info['hbp_response']
                bid_response = response_payload['seatbid'][0]['bid'][0]
                adm = bid_response['adm']
                assert_that("1" in adm)
                # Verify "exp_to_bucket":"{\\"Real_Time_Ads_New_2022_Oct_14\\":\\"RealTimeAds_Disabled\\"}"
        except Exception as err:
            assert_that('bid_token' in err.args)
            # Verify "exp_to_bucket":"{\\"Real_Time_Ads_New_2022_Oct_14\\":\\"RealTimeAds_NoCache\\"}"
            # if the previous request fall to RealTimeAds_NoCache bucket, will serve realtime request.
            info = request_hbp_with_real_time_token('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement_id,
                                                    rtb=test_mode_kraken_rtb_ids,
                                                    token_device_id=test_mode_device_id, ads_retry_mode='meister',
                                                    no_pre_cache_token=True, ip=fr_ip,
                                                    config_extension=config_extension_RTA,
                                                    sdk_v=test_default_real_time_sdk_version,
                                                    explain='jaeger')
            response_payload = info['hbp_response']
            bid_resquet = get_bid_request_obj_from_hbp_explain(response_payload)
            bid_response = response_payload['seatbid'][0]['bid'][0]
            adm = bid_response['adm']
            assert_that("2" in adm)
            # Verified fields from sdk
            device = bid_resquet['device']
            assert_that(device['connectiontype'], equal_to(2))
            assert_that(device['carrier'], equal_to("emily_mobile"))
            assert_that(device['make'], equal_to("Apple"))
            assert_that(device['model'], equal_to("iPhone15,6"))
            assert_that(device['os'], equal_to("iOS"))
            assert_that(device['osv'], equal_to("12.4"))
            assert_that(device['h'], equal_to(2688))
            assert_that(device['w'], equal_to(1242))
            assert_that(device['ua'], equal_to(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"))
            # also validate those fields in deliver plus 'storage_bytes_available', 'volume', 'battery_level,
            # connection_detail, connection,device_make  , device_make_by_wurfl ,device_model_by_wurfl ,browser_user_agent,
            # device_height, device_width'




    @allure.tag('basic')
    @allure.story('PBJ-4907 Add a new field "roas_target_multiplier" to kafka topic "as-deliveries"')
    @allure.description('Verify "roas_target_multiplier" is added to ad-deliveries')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_record_target_multiplier(self, pub_app_id, placement_id):
        over_ride_bid_reponse = 'seatbid.0.bid.0.ext.vungle.roas.target_multiplier@0.15'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version='Vungle/6.11.3',
                                          src_ip=au_ip, debug='jaeger', override_bid_response_any=over_ride_bid_reponse))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'ad-deliveries':roas_target_multiplier:0.15



    @allure.tag('basic', 'v1.252.0')
    @allure.story('PBJ-5073 populate fields of predicted_user_ltv and predicted_pay_rate to kafka topic '
                  'as-deliveries-20220421')
    @allure.description('Verify "predicted_user_ltv", "predicted_pay_rate" are added to ad-deliveries')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_record_roas_predicted_fields(self, pub_app_id, placement_id):
        over_ride_bid_reponse = 'seatbid.0.bid.0.ext.vungle.roas.predicted_pay_rate@0.35|||seatbid.0.bid.0.ext.vungle.roas.predicted_user_ltv@0.15'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version='Vungle/6.11.3',
                                          src_ip=au_ip, debug='jaeger', override_bid_response_any=over_ride_bid_reponse))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify values in 'ad-deliveries':roas_predicted_user_ltv":0.15,"roas_predicted_pay_rate":0.35

    @allure.tag('basic')
    @allure.story('as deliveried', 'v1.255.0')
    @allure.story('PBJ-5134 Add account ID in as-deliveries Kafka topic')
    @allure.description('Verify account id for adv_account_id and pub_account_id are record to delivery message')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_add_account_id_01(self, pub_app_id):
        override_bid_response = 'seatbid.0.bid.0.ext.vungle.ad_app_account_id@"emily_adv_account_id"'
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids,
                                                                        sdk_version='Vungle/6.10.3',
                                                                        src_ip=au_ip, debug='jaeger',
                                                                        override_bid_response_any=override_bid_response))

        response_payload = r.json()
        ads = response_payload['ads'][0]

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # verify fields 'adv_account_id' and 'pub_account_id' are added to delivery message.




    @allure.tag('basic')
    @allure.story('as deliveried', 'v1.255.0')
    @allure.story('PBJ-5134 Add account ID in as-deliveries Kafka topic')
    @allure.description('Verify account id for adv_account_id and pub_account_id are record to delivery message')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_real_time_placement])
    def test_realtime_test_add_account_id_01(self, pub_app_id, placement_id):
        override_bid_response = 'seatbid.0.bid.0.ext.vungle.ad_app_account_id@"emily_adv_account_id"'
        info = request_hbp_with_real_time_token('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement_id,
                                                rtb=meister_rtb_ids, ads_retry_mode='meister',
                                                test_device_id=gen_device_id(), ads_debug='jaeger',
                                                no_pre_cache_token=True, ip=au_ip,
                                                sdk_v=test_default_real_time_sdk_version,
                                                explain='jaeger', config_extension=config_extension_RTA,
                                                override_bid_response_any=override_bid_response)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']

            debug = response_payload['ext']['debug']['as-deliveries']
            assert_keys_exist(debug, 'adv_account_id')
            assert_keys_exist(debug, 'pub_account_id')
            assert_that(debug['adv_account_id'], equal_to('5ef98edf7f0ee3001567b2bf'))
            assert_that(debug['pub_account_id'], equal_to('597565c6c5511a1b62000990'))


    @allure.tag('RTA test mode')
    @allure.story('normal', 'v1.259.0')
    @allure.story('PBJ-5161 Please confirm app ID \'4ee19fb8121ae61a03000022\' is a test app')
    @allure.description('Verify no delivery record to kafka for RTA test mode request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_realtime_exp])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_test_mode_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=test_mode_kraken_rtb_ids,
                                                config_extension=config_extension_RTA
                                                )
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            bid_response = info['hbp_response']
            deliveries=get_ext_debug_from_jaeger_explain(bid_response, 'as-deliveries')
            assert_that(deliveries is None)



    @allure.tag('RTA test mode')
    @allure.story('normal', 'v1.259.0')
    @allure.story('PBJ-5161 Please confirm app ID \'4ee19fb8121ae61a03000022\' is a test app')
    @allure.description('Verify no delivery record to kafka for RTA test mode request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_realtime_exp])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_test_mode_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, is_test=1,
                                                explain=True, coppa=True, rtb=test_mode_kraken_rtb_ids,
                                                config_extension=config_extension_RTA
                                                )
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            bid_response = info['hbp_response']
            deliveries=get_ext_debug_from_jaeger_explain(bid_response, 'as-deliveries')
            assert_that(deliveries is None)



    @allure.tag('RTA test mode')
    @allure.story('normal', 'v1.259.0')
    @allure.story('PBJ-5161 Please confirm app ID \'4ee19fb8121ae61a03000022\' is a test app')
    @allure.description('Verify no delivery record to kafka for RTA test mode request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app_rta])
    @pytest.mark.parametrize('placement', [android_common_test_placement_rta])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_test_mode_03(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token('max', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                test_device_id=test_mode_device_id,
                                                platform='android', ip=au_ip, is_test=1,
                                                no_pre_cache_token=True, config_extension=config_extension_RTA_android_realtime,
                                                sdk_v=test_default_real_time_sdk_version,
                                                explain='jaeger')
        response_payload = info['hbp_response']
        bid_response = response_payload['seatbid'][0]['bid'][0]
        adm = bid_response['adm']
        assert_that("2" in adm)
        deliveries = get_ext_debug_from_jaeger_explain(response_payload, 'as-deliveries')
        assert_that(deliveries is None)


    @allure.tag('RTA test mode')
    @allure.story('normal', 'v1.259.0')
    @allure.story('PBJ-5161 Please confirm app ID \'4ee19fb8121ae61a03000022\' is a test app')
    @allure.description('Verify the delivery will be recorded to kafka for RTA non test mode request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_realtime_exp])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_test_mode_04(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, is_test=0,
                                                explain=True, coppa=True, rtb=meister_rtb_ids,
                                                config_extension=config_extension_RTA
                                                )
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            bid_response = info['hbp_response']
            deliveries=get_ext_debug_from_jaeger_explain(bid_response, 'as-deliveries')
            assert_that(deliveries is not None)



    @allure.tag('RTA test mode')
    @allure.story('normal', 'v1.259.0')
    @allure.story('PBJ-5161 Please confirm app ID \'4ee19fb8121ae61a03000022\' is a test app')
    @allure.description('Verify the delivery will not be recorded to kafka for realtime test mode traffic')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_test_mode_05(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, is_test=1,
                                                explain=True, coppa=True, rtb=test_mode_kraken_rtb_ids
                                                )
        if info['is_hbp_responded_200']:
            assert_that(info['is_hbp_responded_200'], equal_to(True))
            bid_response = info['hbp_response']
            deliveries=get_ext_debug_from_jaeger_explain(bid_response, 'as-deliveries')
            assert_that(deliveries is None)
