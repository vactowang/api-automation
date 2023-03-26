import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestAppExtDetails(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request app')
    @allure.description('Verify app ext details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_app_ext_details(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['app']['ext']['vungle']['altid'], equal_to(common_test_app))
        assert_keys_exist(bid_request['app']['ext']['vungle'], 'bundleid')
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'name')
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'ver')

    @allure.feature('basic')
    @allure.tag('basic', 'normal')
    @allure.story('bid request app')
    @allure.description('Verify no templates in app ext details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_no_templates(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['app']['ext']['vungle'], 'templates')

    @allure.feature('basic')
    @allure.tag('basic', 'smoke', 'test_mode')
    @allure.story('bid request app force view')
    @allure.description('Verify force view value from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5d4be99434c2bc00181da7f3'])
    def test_app_ext_force_view(self, pub_app_id):
        '''
        Pub app setting:

            "forceViewIncentivized" : true,
            "forceView" : true,
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-9424312', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['app']['ext']['vungle']['forceView'], equal_to(1))
        assert_that(bid_request['app']['ext']['vungle']['forceViewIncentivized'], equal_to(1))

    @allure.feature('bid request app setting')
    @allure.tag('normal', 'smoke', 'test_mode')
    @allure.story('white list and black list')
    @allure.description('Verify tag/app white list and black list from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', ['5d4be99434c2bc00181da7f3'])
    def test_app_ext_white_black_list(self, pub_app_id):
        '''
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
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT-9424312', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['app']['ext']['vungle']['wtags'], equal_to(['bbb', 'ccc']))
        assert_that(bid_request['app']['ext']['vungle']['wadvid'], equal_to(["513a1d5e5cac775f65000047"]))
        assert_that(bid_request['app']['ext']['vungle']['badvid'], equal_to(["4f7b866be5c7552241000ec6"]))

    @allure.feature('bid request app setting')
    @allure.tag('smoke', 'R_1.123.0')
    @allure.story('PBJ-1435 add account id in app obj of bid request')
    @allure.description('Verify the account id in app obj of bid request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_app_ext_account_id(self, pub_app_id):
        '''
        The account id of the test app '59786bc2a43b3a08620026b1' is '597565c6c5511a1b62000990'
        '''
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['app']['ext']['vungle']['accountid'], equal_to('597565c6c5511a1b62000990'))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.139.0')
    @allure.story('PBJ-2003 HBP partner name in message record')
    @allure.description('Verify the mediation name from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_app_ext_sdk_mediation(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.8.0;Mopub',
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
        assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to('Mopub'))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'test_mode', 'R_1.139.0')
    @allure.story('PBJ-2003 HBP partner name in message record')
    @allure.description('Verify the mediation name from bid request sdk info in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_app_ext_sdk_mediation_test_mode(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.8.0;Mopub',
                                          rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
        assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to('Mopub'))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.147.0')
    @allure.story('PBJ-2191 Parse Plugin name & Adapter Version for Saygames & ohayoo')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0;vunglehbs/3.0.0', 'Vungle/6.8.0;vunglehbs/4.0.0'])
    def test_app_ext_plugin_name_adapter_ver(self, pub_app_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
        assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to(sdk_v.split(';')[1].split('/')[0]))
        assert_that(bid_request['app']['ext']['vungle']['sdk']['pluginver'],
                    equal_to(sdk_v.split(';')[1].split('/')[1]))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.147.0', 'test_mode')
    @allure.story('PBJ-2191 Parse Plugin name & Adapter Version for Saygames & ohayoo')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0;vunglehbs/3.0.0', 'Vungle/6.8.0;vunglehbs/4.0.0'])
    def test_app_ext_plugin_name_adapter_ver_test_mode(self, pub_app_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
        assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to(sdk_v.split(';')[1].split('/')[0]))
        assert_that(bid_request['app']['ext']['vungle']['sdk']['pluginver'],
                    equal_to(sdk_v.split(';')[1].split('/')[1]))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.152.0')
    @allure.story('PBJ-2333 Parse Plugin name & Adapter Version for Aequus')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0;vunglehbs/5.0.0'])
    def test_app_ext_plugin_name_adapter_ver_1(self, pub_app_id, sdk_v, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
        assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to(sdk_v.split(';')[1].split('/')[0]))
        assert_that(bid_request['app']['ext']['vungle']['sdk']['pluginver'],
                    equal_to(sdk_v.split(';')[1].split('/')[1]))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.152.0', 'test_mode')
    @allure.story('PBJ-2333 Parse Plugin name & Adapter Version for Aequus')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0;vunglehbs/5.0.0'])
    def test_app_ext_plugin_name_adapter_ver_test_mode_1(self, pub_app_id, sdk_v, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
        assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to(sdk_v.split(';')[1].split('/')[0]))
        assert_that(bid_request['app']['ext']['vungle']['sdk']['pluginver'],
                    equal_to(sdk_v.split(';')[1].split('/')[1]))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.153.0')
    @allure.story('PBJ-2333 Parse Plugin name & Adapter Version for charboost')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0;vunglehbs/6.0.0'])
    def test_app_ext_plugin_name_adapter_ver_2(self, pub_app_id, sdk_v, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
        assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to(sdk_v.split(';')[1].split('/')[0]))
        assert_that(bid_request['app']['ext']['vungle']['sdk']['pluginver'],
                    equal_to(sdk_v.split(';')[1].split('/')[1]))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'R_1.153.0', 'test_mode')
    @allure.story('PBJ-2333 Parse Plugin name & Adapter Version for charboost')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0;vunglehbs/6.0.0'])
    def test_app_ext_plugin_name_adapter_ver_test_mode_2(self, pub_app_id, sdk_v, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
        assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to(sdk_v.split(';')[1].split('/')[0]))
        assert_that(bid_request['app']['ext']['vungle']['sdk']['pluginver'],
                    equal_to(sdk_v.split(';')[1].split('/')[1]))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-3033 Add plugin name with vunglehbs map for rovio& admost in jaeger&scrat')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0;vunglehbs/9.0.0', 'Vungle/6.9.0;vunglehbs/10.0.0'])
    def test_app_ext_plugin_name_adapter_ver_3(self, pub_app_id, sdk_v, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
        assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to(sdk_v.split(';')[1].split('/')[0]))
        assert_that(bid_request['app']['ext']['vungle']['sdk']['pluginver'],
                    equal_to(sdk_v.split(';')[1].split('/')[1]))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.170.0', 'test_mode')
    @allure.story('PBJ-3033 Add plugin name with vunglehbs map for rovio& admost in jaeger&scrat')
    @allure.description('Verify the plugin name and adapter version from bid request sdk info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0;vunglehbs/9.0.0', 'Vungle/6.9.0;vunglehbs/10.0.0'])
    def test_app_ext_plugin_name_adapter_ver_test_mode_3(self, pub_app_id, sdk_v, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v, rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_exist(bid_request['app']['ext']['vungle']['sdk'], 'plugin')
        assert_that(bid_request['app']['ext']['vungle']['sdk']['plugin'], equal_to(sdk_v.split(';')[1].split('/')[0]))
        assert_that(bid_request['app']['ext']['vungle']['sdk']['pluginver'],
                    equal_to(sdk_v.split(';')[1].split('/')[1]))

    @allure.feature('xapi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-2814 Integration and test XAPI')
    @allure.description('Verify the tokens from the bid request for XAPI eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_xapi_bid_request_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_xapi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['app']['publisher']['ext']['rp']['account_id'], equal_to('23980'))
        assert_that(bid_request['app']['ext']['rp']['site_id'], equal_to('404098'))

    @allure.feature('xapi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-2814 Integration and test XAPI')
    @allure.description('Verify the tokens from the bid request for XAPI eDSP with hb traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_xapi_bid_request_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_xapi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['app']['publisher']['ext']['rp']['account_id'], equal_to('23980'))
        assert_that(bid_request['app']['ext']['rp']['site_id'], equal_to('404098'))

    @allure.feature('xapi suuport')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-2814 Integration and test XAPI')
    @allure.description('Verify the tokens from the bid request for XAPI eDSP with banner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_xapi_bid_request_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_banner_xapi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['app']['publisher']['ext']['rp']['account_id'], equal_to('23980'))
        assert_that(bid_request['app']['ext']['rp']['site_id'], equal_to('404098'))

    @allure.feature('xapi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-2814 Integration and test XAPI')
    @allure.description('Verify there is no related token from the bid request for non-XAPI eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_xapi_bid_request_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['app']['publisher'], 'ext')
        assert_keys_not_exist(bid_request['app'], 'ext')



    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify bcreatives in bid request which both setting in pub account and app level')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_01(self, pub_app_id, placement):
        """
        app setting:

        creative_id_blocklist:['629858c1ec89a361cec4ca7e', '62985b0bec89a361cec4ca83']

        pub account setting:
        creative_id_blocklist:['62985b0bec89a361cec4ca83', '5eb9a49a5ddc02539da7c732']
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids_no_adomain_block, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_exist(ext, 'bcreatives')
        assert_that(ext['bcreatives'], equal_to(['629858c1ec89a361cec4ca7e', '62985b0bec89a361cec4ca83', '5eb9a49a5ddc02539da7c732']))

    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify bcreatives in bid request which only setting in pub account level')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_block_crid_02(self, pub_app_id, placement):
        """
        app setting:

        pub account setting:
        creative_id_blocklist:['62985b0bec89a361cec4ca83', '5eb9a49a5ddc02539da7c732']
        """
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=meister_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_exist(ext, 'bcreatives')
        assert_that(ext['bcreatives'],
                    equal_to(['62985b0bec89a361cec4ca83', '5eb9a49a5ddc02539da7c732']))



    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify bcreatives in bid request which  setting in pub account level and null '
                        'creative_id_blocklist in app level')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    def test_block_crid_03(self, pub_app_id, placement):
        """
        app setting:
        creative_id_blocklist:[]
        pub account setting:
        creative_id_blocklist:['62985b0bec89a361cec4ca83', '5eb9a49a5ddc02539da7c732']
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=meister_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_exist(ext, 'bcreatives')
        assert_that(ext['bcreatives'],
                    equal_to(['62985b0bec89a361cec4ca83', '5eb9a49a5ddc02539da7c732']))



    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify bcreatives in bid request which setting in pub app level and not in app level')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', ['DEFAULT-5045327'])
    def test_block_crid_04(self, pub_app_id, placement):
        """
        app setting:
        creative_id_blocklist:['62986971ec89a361cec4ca85', '62986997ec89a361cec4ca86]
        pub account setting:
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=meister_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_exist(ext, 'bcreatives')
        assert_that(ext['bcreatives'],
                    equal_to(['62986971ec89a361cec4ca85', '62986997ec89a361cec4ca86']))


    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify no bcreatives in bid request which both not setting in pub app level and app level')
    @pytest.mark.parametrize('pub_app_id', [android_common_bcat_app])
    @pytest.mark.parametrize('placement', [android_common_bcat_placement])
    def test_block_crid_05(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=meister_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_not_exist(ext, 'bcreatives')

    @allure.feature('Block CRID')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify bcreatives in bid request which both setting in pub account and app level via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_06(self, pub_app_id, placement):
        """
        app setting:

        creative_id_blocklist:['629858c1ec89a361cec4ca7e', '62985b0bec89a361cec4ca83']

        pub account setting:
        creative_id_blocklist:['62985b0bec89a361cec4ca83', '5eb9a49a5ddc02539da7c732']
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_exist(ext, 'bcreatives')
        assert_that(ext['bcreatives'],
                    equal_to(['629858c1ec89a361cec4ca7e', '62985b0bec89a361cec4ca83', '5eb9a49a5ddc02539da7c732']))

    @allure.feature('Block CRID')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4558 eDSP Creative ID Blocking at Pub App and Pub Account Level')
    @allure.description('Verify jaeger block crid if rtb_account_id+_+crid match in DB setting in pub account '
                        'level via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_edsp_01(self, pub_app_id, placement):
        """

        pub account setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_test62623ad","5c4f51e0210b7e0015340a22_112795"]


        rtb account id: 5cd92b2661a35300113a8487
        """
        override_crid = 'test62623ad'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        as_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(as_markup, 'info')
        assert_that(as_markup['info'], equal_to("impression auctioned but unsold"))


    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4558 eDSP Creative ID Blocking at Pub App and Pub Account Level')
    @allure.description('Verify jaeger will serve ads if crid does not match with DB setting '
                        'in pub account level.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_edsp_02(self, pub_app_id, placement):
        """
        rtb account id: 5cd92b2661a35300113a8487
        pub account setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_test62623ad","5c4f51e0210b7e0015340a22_112795"]
        """
        override_crid = 'ext11111'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        as_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(as_markup, 'info')



    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4558 eDSP Creative ID Blocking at Pub App and Pub Account Level')
    @allure.description('Verify jaeger will serve ads if rtb_account_id does not match with DB setting '
                        'in pub account level.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_edsp_03(self, pub_app_id, placement):
        """
        rtb account id: 5cd92b2661a35300113a8497
        pub account setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_test62623ad","5c4f51e0210b7e0015340a22_112795"]
        """
        override_crid = 'test62623ad'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext4_test_mode_kraken_rtb_ids_vast, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        as_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(as_markup, 'info')



    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4558 eDSP Creative ID Blocking at Pub App and Pub Account Level')
    @allure.description('Verify jaeger will block  ads if rtb_account_id+_+crid match with DB setting '
                        'in app level.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_edsp_04(self, pub_app_id, placement):
        """
        rtb account id: 5cd92b2661a35300113a8497
        pub account setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_test62623ad","5c4f51e0210b7e0015340a22_112795"]
        app setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_ext11122"]
        """
        override_crid = "ext11122"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        as_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(as_markup, 'info')
        assert_that(as_markup['info'], equal_to("impression auctioned but unsold"))



    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4558 eDSP Creative ID Blocking at Pub App and Pub Account Level')
    @allure.description('Verify jaeger will serve ads for does not block creative')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_edsp_05(self, pub_app_id, placement):
        """
        rtb account id:
        6242b0f15890c35df3ee97fa:5cd92b2661a35300113a8497,
        5fd21adbc80cb9051249a6ad:5cd92b2661a35300113a8487,
        pub account setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_test62623ad","5c4f51e0210b7e0015340a22_112795"]
        app setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_ext11122", "5cd92b2661a35300113a8497_ext11133"]
        """
        override_crid = 'ext11133'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector='6242b0f15890c35df3ee97fa,5fd21adbc80cb9051249a6ad', src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')
        # rtb 5fd21adbc80cb9051249a6ad will win the auction
        campaign = ad_markup['campaign']
        assert_that("5fd21adbc80cb9051249a6ad" in campaign)

    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4558 eDSP Creative ID Blocking at Pub App and Pub Account Level')
    @allure.description('Verify jaeger will serve ads for high bid price crative')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_crid_edsp_06(self, pub_app_id, placement):
        """
        rtb account id:
        6242b0f15890c35df3ee97fa:5cd92b2661a35300113a8497,
        5fd21adbc80cb9051249a6ad:5cd92b2661a35300113a8487,
        pub account setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_test62623ad","5c4f51e0210b7e0015340a22_112795"]
        app setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_ext11122", "5cd92b2661a35300113a8497_ext11133"]
        """
        override_crid = 'ext11144'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector='6242b0f15890c35df3ee97fa,5fd21adbc80cb9051249a6ad', src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')
        # rtb 6242b0f15890c35df3ee97fa will win the auction
        campaign = ad_markup['campaign']
        assert_that("6242b0f15890c35df3ee97fa" in campaign)



    @allure.feature('Block CRID')
    @allure.tag('normal')
    @allure.story('PBJ-4558 eDSP Creative ID Blocking at Pub App and Pub Account Level')
    @allure.description('Verify jaeger will serve ads for idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_not_block_idsp_07(self, pub_app_id, placement):
        """
        rtb account id: 5cd92b2661a35300113a8487,
        pub account setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_test62623ad","5c4f51e0210b7e0015340a22_112795"]
        app setting:
        edsp_creative_id_blocklist:["5cd92b2661a35300113a8487_ext11122", "5cd92b2661a35300113a8497_ext11133"]
        """
        override_crid = 'ext11122'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6', override_crid=override_crid))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'info')




    @allure.feature('Block Template ID')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify btemplates in bid request which both setting in pub account')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_template_01(self, pub_app_id, placement):
        """
        pub account setting:
        template_blocklist:['templateblocks01', 'templateblocks02', 'templateblocks02']
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_exist(ext, 'btemplates')
        assert_that(ext['btemplates'], equal_to(['templateblocks01', 'templateblocks02']))

    @allure.feature('Block Template ID')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify not btemplates in bid request which not setting in pub account')
    @pytest.mark.parametrize('pub_app_id', [android_common_bcat_app])
    @pytest.mark.parametrize('placement', [android_common_bcat_placement])
    def test_block_template_02(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_not_exist(ext, 'btemplates')



    @allure.feature('Block Template ID')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify no btemplates in bid request with null template_blocklist setting in pub account')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', ['DEFAULT-5045327'])
    def test_block_template_03(self, pub_app_id, placement):
        """
               pub account setting:
               template_blocklist:[]
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_not_exist(ext, 'btemplates')


    @allure.feature('Block Template ID')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify btemplates in bid request which both setting in pub account via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_template_04(self, pub_app_id, placement):
        """
        pub account setting:
        template_blocklist:['templateblocks01', 'templateblocks02', 'templateblocks02']
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_exist(ext, 'btemplates')
        assert_that(ext['btemplates'], equal_to(['templateblocks01', 'templateblocks02']))



    @allure.feature('Block Creative Tag')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify btags in bid request which setting in pub account')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_creative_tag_01(self, pub_app_id, placement):
        """
        pub account setting:
        creative_tag_blocklist:['creativeTag01', 'creativeTag02']
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_exist(ext, 'btags')
        assert_that(ext['btags'], equal_to(['creativetag01', 'creativetag02']))


    @allure.feature('Block Creative Tag')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify no btags in bid request which not setting in pub account')
    @pytest.mark.parametrize('pub_app_id', [android_common_bcat_app])
    @pytest.mark.parametrize('placement', [android_common_bcat_placement])
    def test_block_creative_tag_02(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=non_test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_not_exist(ext, 'btags')


    @allure.feature('Block Creative Tag')
    @allure.tag('normal')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify no btags in bid request with null creative_tag_blocklist setting in pub account')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement', ['DEFAULT-5045327'])
    def test_block_creative_tag_03(self, pub_app_id, placement):
        """
           pub account setting:
           creative_tag_blocklist:[]
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_not_exist(ext, 'btags')

    @allure.feature('Block Creative Tag')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify btags in bid request which setting in pub account via test mode')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_creative_tag_04(self, pub_app_id, placement):
        """
        pub account setting:
        creative_tag_blocklist:['creativeTag01', 'creativeTag02']
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        ext = bid_request['app']['ext']['vungle']
        assert_keys_exist(ext, 'btags')
        assert_that(ext['btags'], equal_to(['creativetag01', 'creativetag02']))



    @allure.feature('Block Creative Tag')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4286 Creative ID & Template ID&Creative Tag blocking at the publisher account and app level')
    @allure.description('Verify block is not for edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_block_not_for_edsp(self, pub_app_id, placement):
        """
        pub account setting:
        creative_tag_blocklist:['creativeTag01', 'creativeTag02']
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_liftoff, src_ip=au_ip,
                                          debug='jaeger', sdk_version='Vungle/6.10.6'))

        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        app = bid_request['app']
        assert_keys_not_exist(app, 'ext')