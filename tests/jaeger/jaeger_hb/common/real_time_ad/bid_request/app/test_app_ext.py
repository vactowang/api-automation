import pytest
import allure

from utils.behaviors import  request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain
from utils.common import *
from utils.assertions import *
from settings import *



@allure.epic('Real-time bid request')
class TestAppExtDetails(object):

    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify app details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_app_ext_details(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['app']['ext']['vungle']['altid'], equal_to(common_test_app))
                assert_keys_exist(bid_request['app']['ext']['vungle'], 'bundleid')
                assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'name')
                assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'ver')


    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify no templates in app ext details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_no_templates(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_keys_not_exist(bid_request['app']['ext']['vungle'], 'templates')


    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify force view value from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5d4be99434c2bc00181da7f3'])
    @pytest.mark.parametrize('placement', ['VIDEO_REALTIME_TEST-31769501'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_app_ext_force_view(self, pub_app_id, placement, sdk_v, partner):
        """
           Pub app setting:

               "forceViewIncentivized" : true,
               "forceView" : true,
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_keys_not_exist(bid_request['app']['ext']['vungle'], 'templates')


    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify force view value from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5d4be99434c2bc00181da7f3'])
    @pytest.mark.parametrize('placement', ['VIDEO_REALTIME_TEST-31769501'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_ext_white_black_list(self, pub_app_id, placement, sdk_v, partner):
        """
       Pub app level setting:

           "adTagBlacklist" : [
           ],
           "adTagWhitelist" : [
               "aaa",
               "bbb",
               "ccc"
           ],
           "adWhitelist" : [
               ObjectId("4f7b866be5c7552241000ec6"),
               ObjectId("513a1d5e5cac775f65000047")
           ],
           "adBlacklist" : [
               ObjectId("513a1d5e5cac775f65000047")
           ],

       Placement level setting:

           "adBlacklist" : [],
           "adTagBlacklist" : [
               "aaa"
           ],
       """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['app']['ext']['vungle']['wtags'], equal_to(['bbb', 'ccc']))
                assert_that(bid_request['app']['ext']['vungle']['wadvid'], equal_to(["513a1d5e5cac775f65000047"]))
                assert_that(bid_request['app']['ext']['vungle']['badvid'], equal_to(["4f7b866be5c7552241000ec6"]))

    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify the account id in app obj of bid request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_app_ext_account_id(self, pub_app_id, placement, sdk_v, partner):
        """
              The account id of the test app '59786bc2a43b3a08620026b1' is '597565c6c5511a1b62000990'
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['app']['ext']['vungle']['accountid'], equal_to('597565c6c5511a1b62000990'))

    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify the account id in app obj of bid request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0;max'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_ext_sdk_mediation(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
                assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to('max'))


    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0;vunglehbs/3.0.0', 'Vungle/6.8.0;vunglehbs/4.0.0'])
    @pytest.mark.parametrize('partner', ['saygames','ohayoo'])
    def test_real_time_plugin_name_adapter_ver(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
                assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'],
                            equal_to(sdk_v.split(';')[1].split('/')[0]))
                assert_that(bid_request['app']['ext']['vungle']['sdk']['pluginver'],
                            equal_to(sdk_v.split(';')[1].split('/')[1]))


    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify the tokens from the bid request for XAPI eDSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_xapi_bid_request_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_xapi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast_xapi)
                assert_that(bid_request['app']['publisher']['ext']['rp']['account_id'], equal_to('23980'))
                assert_that(bid_request['app']['ext']['rp']['site_id'], equal_to('404098'))



    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify the tokens from the bid request for XAPI eDSP with hb traffic')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_xapi_bid_request_2(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip, is_hb=True,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_xapi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast_xapi)
                assert_that(bid_request['app']['publisher']['ext']['rp']['account_id'], equal_to('23980'))
                assert_that(bid_request['app']['ext']['rp']['site_id'], equal_to('404098'))



    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify the tokens from the bid request for XAPI eDSP with banner')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_xapi_bid_request_3(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, banner=True,
                                                explain=True, ip=eu_country_ip, is_hb=True,
                                                rtb=ext_test_mode_kraken_rtb_ids_banner_xapi)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_test_mode_kraken_rtb_ids_banner_xapi)
                assert_that(bid_request['app']['publisher']['ext']['rp']['account_id'], equal_to('23980'))
                assert_that(bid_request['app']['ext']['rp']['site_id'], equal_to('404098'))

    @allure.feature('app details')
    @allure.tag('basic', 'smoke')
    @allure.story('real time bid request app')
    @allure.description('Verify there is no related token from the bid request for non-XAPI eDSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_xapi_bid_request_4(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                assert_keys_not_exist(bid_request['app']['publisher'], 'ext')
                assert_keys_not_exist(bid_request['app'], 'ext')

