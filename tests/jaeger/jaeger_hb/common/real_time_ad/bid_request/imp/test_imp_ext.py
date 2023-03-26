
import allure
from utils.behaviors import request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain, get_bid_request_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *



@allure.epic('Real-time imp ext')
class TestImpExt(object):

    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp banner')
    @allure.description('Verify imp banner obj from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_ext_vungle_details(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(bid_request['imp'][0]['ext']['vungle']['placement_reference_id'],
                            equal_to(common_test_real_time_placement))
                assert_that('placement_id' in bid_request['imp'][0]['ext']['vungle'])
                assert_that(
                    set(bid_request['imp'][0]['ext']['vungle']['templatetypes']).issubset([0, 1, 2, 3, 4, 5, 6, 7, 8]))
                assert_that(set(bid_request['imp'][0]['ext']['vungle']['allowed_ad_types']).issubset([1, 2, 3]))
                assert_that(bid_request['imp'][0]['ext']['vungle']['rewarded'], equal_to(0))
                assert_that('orientation' in bid_request['imp'][0]['ext']['vungle'])
                assert_that(isinstance(bid_request['imp'][0]['ext']['vungle']['is_flat_cpm_enabled'], bool))
                assert_that(isinstance(bid_request['imp'][0]['ext']['vungle']['is_header_bidding'], bool))

    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp banner')
    @allure.story('PBJ-1506 Update the logic to get placement type.')
    @allure.description('Verify impType for mrec placement which no type in placement level setting')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ["realtime_INTER-MREC-001"])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_no_type_in_placement(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)

                # assert_that(bid_request['imp'][0]['ext']['impType'], equal_to('MREC'))


    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp banner')
    @allure.story('PBJ-1506 Update the logic to get placement type.')
    @allure.description('Verify impType for mrec placement which no template_type in placement level setting')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ["realtime_INTER-MREC-002"])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_type_no_template_type_in_placement(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(bid_request['imp'][0]['ext']['impType'], equal_to('MREC'))


    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp banner')
    @allure.story('PBJ-1506 Update the logic to get placement type.')
    @allure.description('Verify impType for mrec placement with type mrec in placement level setting')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ["realtime_INTER-MREC-003"])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_type_mrec_type_in_placement(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)

                # assert_that(bid_request['imp'][0]['ext']['impType'], equal_to('MREC'))

    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp banner')
    @allure.story('PBJ-1506 Update the logic to get placement type.')
    @allure.description('Verify impType for mrec placement which type is not mrec in placement level setting')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ["realtime_INTER-MREC-005_1"])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_type_type_not_mrec(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_keys_not_exist(bid_request['imp'][0]['ext'], 'impType')


    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp banner')
    @allure.story('PBJ-1506 Update the logic to get placement type.')
    @allure.description('Verify the template type in bid request for image mrec ad')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ["realtime_IMAGE-MREC-001"])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_template_type_for_image_mrec(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(9 in bid_request['imp'][0]['ext']['vungle']['templatetypes'])
                # assert_that(bid_request['imp'][0]['ext']['impType'], equal_to('MREC'))



    @allure.feature('openrtb 2.5 support')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp banner')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the skip field in openrtb25x for skippable ad')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ["realtime_HJKM6GM50918"])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_skippable_ad_openrtb25x(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(bid_request['imp'][0]['ext']['openrtb25x']['skip'], equal_to(1))


    @allure.feature('openrtb 2.5 support')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp banner')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the skip field in openrtb25x for skippable ad')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_skippable_banner_openrtb25x(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, banner=True,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(bid_request['imp'][0]['ext']['openrtb25x']['skip'], equal_to(1))


    @allure.feature('openrtb 2.5 support')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp ext')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the skip field in openrtb25x for non skippable ad')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_non_skippable_ad_openrtb25x(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(bid_request['imp'][0]['ext']['openrtb25x']['skip'], equal_to(0))


    # -------------------------------------------- skadnetwork programmatic -------------------------------------------

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support,'
                  'PBJ-2627 Jaeger should only pass the adnetwork id list specific for the eDSP')
    @allure.description('Test for Jaeger pass network id to external VAST Kraken')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_realtime_jaeger_pass_skadnetwork_id_ext_vast(self, pub_app_id, placement, sdk_v, partner):
        '''
        RTB connection:
            "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
        '''
        network_ids = ['test.ad.nw.001', 'test.nw.45646546', 'GTA9LK7P23.skadnetwork']
        expected_skadn_ids = ["GTA9LK7P23.skadnetwork", "test.ad.nw.001"]

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast, skadnetids=network_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_test_mode_kraken_rtb_ids_vast)
                assert_that(isinstance(bid_request['imp'][0]['ext']['skadn']['version'], str))
                assert_that(bid_request['imp'][0]['ext']['skadn']['sourceapp'], equal_to(common_test_app_market_id))
                assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support,'
                  'PBJ-2627 Jaeger should only pass the adnetwork id list specific for the eDSP')
    @allure.description('Test for Jaeger pass network id to external VAST Kraken')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_realtime_jaeger_pass_skadnetwork_id_ext_mraid_non_test_mode(self, pub_app_id, placement, sdk_v, partner):
        '''
        RTB connection:
            "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
        '''
        network_ids = ['test.ad.nw.001', 'test.nw.45646546', 'GTA9LK7P23.skadnetwork']
        expected_skadn_ids = ["GTA9LK7P23.skadnetwork", "test.ad.nw.001"]

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_mraid, skadnetids=network_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_mraid)
                assert_that(isinstance(bid_request['imp'][0]['ext']['skadn']['version'], str))
                assert_that(bid_request['imp'][0]['ext']['skadn']['sourceapp'], equal_to(common_test_app_market_id))
                assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support')
    @allure.description('Test for SDK does not pass any network id to Jaeger, external Kraken')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_realtime_jaeger_pass_skadnetwork_id_ext_3(self, pub_app_id, placement, sdk_v, partner):
        '''
        RTB connection:
            "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
        '''
        network_ids = []

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, banner=True,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast, skadnetids=network_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_test_mode_kraken_rtb_ids_vast)
                assert_that(isinstance(bid_request['imp'][0]['ext']['skadn']['version'], str))
                assert_that(bid_request['imp'][0]['ext']['skadn']['sourceapp'], equal_to(common_test_app_market_id))
                assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(network_ids))




    @allure.feature('bid request details')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request ext')
    @allure.description('PBJ-4633 [RTA]Use SKAdNetwork ID from the Vungle app, instead of relying on mediation partners')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_pass_skad_ids_to_dsp_from_token(self, pub_app_id, placement, sdk_v, partner):
        '''
              RTB connection:
                  "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
              '''
        token_network_ids = ['test.ad.nw.001', 'test.nw.45646546']
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, config_extension=real_time_config_extension_SKAN_ids,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast, skadnetids=[])

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_test_mode_kraken_rtb_ids_vast)
                assert_that(isinstance(bid_request['imp'][0]['ext']['skadn']['version'], str))
                assert_that(bid_request['imp'][0]['ext']['skadn']['sourceapp'], equal_to(common_test_app_market_id))
                assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(['test.ad.nw.001']))



    @allure.feature('HBP partner name')
    @allure.tag('smoke', 'v1.173.0')
    @allure.story('PBJ-3027 hb plugin version mapping name')
    @allure.description('Verify hb partners plugin version mapping from mongodb setting for in house type')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_realtime_hb_plugin_mapping_in_house_mapping(self, pub_app_id, placement, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=test_default_real_time_sdk_version,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)


        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(bid_request['imp'][0]['ext']['vungle']['hb_partner'], equal_to(partner))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid request via sdv version >=6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_realtime_deeplink(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_test_mode_kraken_rtb_ids_vast)
                deeplink = bid_request['imp'][0]['ext']['deeplink']
                assert_that(deeplink, equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for rewarded via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_instl_flag(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(bid_request['imp'][0]['ext']['vungle']['rewarded'], equal_to(0))

    @allure.feature('xapi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-2814 Integration and test XAPI')
    @allure.description('Verify the tokens from the bid request for XAPI eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_xapi_bid_request_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_xapi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast_xapi)
                assert_that(bid_request['imp'][0]['ext']['rp']['zone_id'], equal_to('2262356'))

    @allure.feature('xapi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-2814 Integration and test XAPI')
    @allure.description('Verify the tokens from the bid request for XAPI eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_xapi_bid_request_2(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, banner=True,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_test_mode_kraken_rtb_ids_banner_xapi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_test_mode_kraken_rtb_ids_banner_xapi)
                assert_that(bid_request['imp'][0]['ext']['rp']['zone_id'], equal_to('2262356'))

    @allure.feature('xapi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-2814 Integration and test XAPI')
    @allure.description('Verify there is no related token from the bid request for non-XAPI eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_xapi_bid_request_3(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
                assert_keys_not_exist(bid_request['imp'][0]['ext'], 'rp')

    @allure.feature('inmobi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-3252 RTB :: Support bidrequest.imp.ext.placementid')
    @allure.description('Verify the placementid of Vungle_InterstitialVideo_iOS for InMobi eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_inmobi_bid_request_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_inmobi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast_inmobi)
                assert_that(bid_request['imp'][0]['ext']['placementid'], '1645632767278')

    @allure.feature('inmobi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-3252 RTB :: Support bidrequest.imp.ext.placementid')
    @allure.description('Verify the placementid of Vungle_Banner_iOS for InMobi eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_inmobi_bid_request_2(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, banner=True,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_inmobi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast_inmobi)
                assert_that(bid_request['imp'][0]['ext']['placementid'], '1642988054140')

