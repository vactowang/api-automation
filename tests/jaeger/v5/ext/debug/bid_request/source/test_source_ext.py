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
class TestBidRequestSourceExt(object):

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the schain fields in openrtb25x - sid is not in seller.json')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_schain_info_openrtb25x_sid_not_in_seller_json(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        schain_obj = bid_request['source']['ext']['schain']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(schain_obj['ver'], not empty())
        assert_that(schain_obj['complete'], not empty())
        assert_that(schain_obj['nodes'][0]['asi'], not empty())
        assert_that(schain_obj['nodes'][0]['sid'], not empty())
        assert_that(schain_obj['nodes'][0]['name'], not empty())
        assert_that(schain_obj['nodes'][0]['rid'], bid_request['id'])
        assert_that(schain_obj['nodes'][0]['hp'], not empty())

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the schain fields in openrtb25x - sid is in seller.json')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [app_id_schain_test])
    def test_schain_info_openrtb25x_sid_in_seller_json(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id_schain_test, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        schain_obj = bid_request['source']['ext']['schain']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(schain_obj['ver'], not empty())
        assert_that(schain_obj['complete'], not empty())
        assert_that(schain_obj['nodes'][0]['asi'], not empty())
        assert_that(schain_obj['nodes'][0]['sid'], not empty())
        assert_keys_not_exist(schain_obj['nodes'][0], 'name')
        assert_that(schain_obj['nodes'][0]['rid'], bid_request['id'])
        assert_that(schain_obj['nodes'][0]['hp'], not empty())

    # --------------------------------------------- OM SDK -----------------------------------------------------------

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for om enabled app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_om_enabled_status_source_ext_app_enabled(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          vungle_version='5.7', debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['source']['ext']['omidpn'], equal_to('vungle'))
        assert_that(bid_request['source']['ext']['omidpv'], equal_to(test_default_sdk_version.split('/')[1]))

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for no om setting in app level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b4'])
    @pytest.mark.parametrize('placement', ['DEFAULT02024'])
    def test_om_enabled_status_source_ext_app_default_setting(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          vungle_version='5.7', debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['source']['ext']['omidpn'], equal_to('vungle'))
        assert_that(bid_request['source']['ext']['omidpv'], equal_to(test_default_sdk_version.split('/')[1]))

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for om disabled app')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b2'])
    @pytest.mark.parametrize('placement', ['DEFAULT02022'])
    def test_om_enabled_status_source_ext_app_disabled(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          vungle_version='5.7', debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['source']['ext'], 'omidpn')
        assert_keys_not_exist(bid_request['source']['ext'], 'omidpv')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for vungle api version < 5.7')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('apiv', ['5.6'])
    def test_om_enabled_status_source_ext_vungle_api_version_ctl_1(self, pub_app_id, placement, apiv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          vungle_version=apiv, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['source']['ext'], 'omidpn')
        assert_keys_not_exist(bid_request['source']['ext'], 'omidpv')

    @allure.feature('omsdk support')
    @allure.tag('normal', 'R_1.146.0', 'test_mode')
    @allure.story('PBJ-1978 Regression test for OMSDK feature')
    @allure.description('Verify the om enabled status for vungle api version >= 5.7')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('apiv', ['5.7', '5.8'])
    def test_om_enabled_status_source_ext_vungle_api_version_ctl_2(self, pub_app_id, placement, apiv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          vungle_version=apiv, debug='jaeger'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['source']['ext']['omidpn'], equal_to('vungle'))
        assert_that(bid_request['source']['ext']['omidpv'], equal_to(test_default_sdk_version.split('/')[1]))

    @allure.feature('liftoff support')
    @allure.tag('normal')
    @allure.story('PBJ-4041 Add Mediation Partner name to LO via source.ext.mediatorname')
    @allure.description('Verify the mediation name from the bid request via lo DSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('mediation', ['vunglehbs/3.0.0'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_mediation_name_lo_1(self, pub_app_id, placement, mediation, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb,
                                          debug='jaeger', sdk_version=test_default_sdk_version+';'+mediation))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_that(bid_request['source']['ext']['mediatorname'], equal_to('saygames'))

    @allure.feature('liftoff support')
    @allure.tag('normal')
    @allure.story('PBJ-4041 Add Mediation Partner name to LO via source.ext.mediatorname')
    @allure.description('Verify the mediation name from the bid request via lo DSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('mediation', ['mopub', 'test'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_mediation_name_lo_2(self, pub_app_id, placement, mediation, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb,
                                          debug='jaeger', sdk_version=test_default_sdk_version+';'+mediation))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_that(bid_request['source']['ext']['mediatorname'], equal_to(mediation))

    @allure.feature('liftoff support')
    @allure.tag('normal')
    @allure.story('PBJ-4041 Add Mediation Partner name to LO via source.ext.mediatorname')
    @allure.description('Verify the change does not impact the non-liftoff DSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('mediation', ['mopub'])
    def test_mediation_name_lo_3(self, pub_app_id, placement, mediation):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger', sdk_version=test_default_sdk_version+';'+mediation))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_keys_not_exist(bid_request['source']['ext'], 'mediatorname')

    @allure.feature('liftoff support')
    @allure.tag('normal')
    @allure.story('PBJ-4041 Add Mediation Partner name to LO via source.ext.mediatorname')
    @allure.description('Verify the change does not impact the non-hb traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('mediation', ['mopub'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_mediation_name_lo_4(self, pub_app_id, placement, mediation, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb,
                                          debug='jaeger', sdk_version=test_default_sdk_version+';'+mediation))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_keys_not_exist(bid_request['source']['ext'], 'mediatorname')


    # PBJ-4874 deprecate
    # @allure.feature('moloco support')
    # @allure.tag('normal', 'v1.229.0')
    # @allure.story('PBJ-4358 Header Bidding Flag')
    # @allure.description('Verify HB flag for Moloco with HB traffic')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_hb_flag_for_moloco_1(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_moloco,
    #                                       debug='jaeger', sdk_version=test_default_real_time_sdk_version))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_that(bid_request['source']['ext']['header_bidding'], equal_to(1))

    # @allure.feature('moloco support')
    # @allure.tag('normal', 'v1.229.0')
    # @allure.story('PBJ-4358 Header Bidding Flag')
    # @allure.description('Verify HB flag for Moloco with non-HB traffic')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_hb_flag_for_moloco_2(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_moloco,
    #                                       debug='jaeger', sdk_version=test_default_real_time_sdk_version))
    #
    #     response_payload = r.json()
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5_debug)
    #     assert_that(bid_request['source']['ext']['header_bidding'], equal_to(0))

    @allure.feature('moloco support')
    @allure.tag('normal', 'v1.229.0')
    @allure.story('PBJ-4358 Header Bidding Flag')
    @allure.description('Verify there will be no HB flag for the other eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    def test_hb_flag_for_moloco_3(self, pub_app_id, placement, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['source']['ext'], 'header_bidding')


    # PBJ-4874
    # @allure.feature('Aarki support')
    # @allure.tag('normal', 'v1.237.0')
    # @allure.story('PBJ-4722 Header Bidding Flag for Aarki DSP')
    # @allure.description('Verify header_bidding=1 for Aarki eDSP Heading bidding request')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_header_bidding_flag_for_aarki_1(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_aarki,
    #                                       debug='jaeger', sdk_version=test_default_real_time_sdk_version))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['source']['ext']['header_bidding'], equal_to(1))

    # PBJ-4874
    # @allure.feature('Aarki support')
    # @allure.tag('normal', 'v1.237.0')
    # @allure.story('PBJ-4722 Header Bidding Flag for Aarki DSP')
    # @allure.description('Verify header_bidding=0 for Aarki eDSP non-Heading bidding request')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # def test_header_bidding_flag_for_aarki_2(self, pub_app_id, placement):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_aarki,
    #                                       debug='jaeger'))
    #     response_payload = r.json()
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
    #     assert_that(bid_request['source']['ext']['header_bidding'], equal_to(0))


    @allure.feature('Aarki support')
    @allure.tag('normal', 'v1.237.0')
    @allure.story('PBJ-4722 Header Bidding Flag for Aarki DSP')
    @allure.description('Verify no header bidding field for non Aarki eDSP ')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('header_bidding', [True, False])
    def test_header_bidding_flag_for_aarki_3(self, pub_app_id, placement, header_bidding):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=header_bidding)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['source']['ext'], 'header_bidding')


