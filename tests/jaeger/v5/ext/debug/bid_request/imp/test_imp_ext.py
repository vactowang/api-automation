import pytest
import allure
import math

from http import HTTPStatus

from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain, get_bid_response_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestImpExt(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp ext')
    @allure.description('Verify imp ext vungle details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_ext_vungle_details(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['placement_reference_id'], equal_to(common_test_placement))
        assert_that('placement_id' in bid_request['imp'][0]['ext']['vungle'])
        assert_that('erpmtarget' in bid_request['imp'][0]['ext']['vungle'])
        assert_that(set(bid_request['imp'][0]['ext']['vungle']['templatetypes']).issubset([0, 1, 2, 3, 4, 5, 6, 7, 8]))
        assert_that(set(bid_request['imp'][0]['ext']['vungle']['allowed_ad_types']).issubset([1, 2, 3]))
        assert_that(bid_request['imp'][0]['ext']['vungle']['rewarded'], equal_to(1))
        assert_that('orientation' in bid_request['imp'][0]['ext']['vungle'])
        assert_that(isinstance(bid_request['imp'][0]['ext']['vungle']['is_flat_cpm_enabled'], bool))
        assert_that('flat_cpm' in bid_request['imp'][0]['ext']['vungle'])
        assert_that('cpm_floor' in bid_request['imp'][0]['ext']['vungle'])
        assert_that('revenue_share' in bid_request['imp'][0]['ext']['vungle'])
        assert_that('serving_cost' in bid_request['imp'][0]['ext']['vungle'])

    @allure.feature('basic')
    @allure.tag('basic', 'normal')
    @allure.story('sdk version')
    @allure.description('Test for mrec serve on windowns 10 with SDK 6.4.0 and above')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5b8d17307ad5a86fc53c7c8a'])
    @pytest.mark.parametrize('placement', ['MREC-WINDOWS-TEST'])
    def test_for_mrec_serve_windows(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='VungleWindows/6.4.0 (Windows 10; native)', debug='jaeger',
                                          rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['templatetypes'], equal_to([6, 7]))
        assert_that(bid_request['imp'][0]['ext']['vungle']['allowed_ad_types'], equal_to([2]))

    @allure.feature('basic')
    @allure.tag('basic', 'normal')
    @allure.story('sdk version')
    @allure.description('Test for mrec does not serve on windowns 10 with SDK below 6.4.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5b8d17307ad5a86fc53c7c8a'])
    @pytest.mark.parametrize('placement', ['MREC-WINDOWS-TEST'])
    def test_for_mrec_not_serve_windows_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='VungleWindows/6.3.9 (Windows 10; native)', debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['ads'][0]['ad_markup']['info'], 'impression auctioned but unsold')

    @allure.feature('basic')
    @allure.tag('basic', 'normal')
    @allure.story('sdk version')
    @allure.description('Test for mrec does not serve on windowns version expect 10')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5b8d17307ad5a86fc53c7c8a'])
    @pytest.mark.parametrize('placement', ['MREC-WINDOWS-TEST'])
    def test_for_mrec_not_serve_windows_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='VungleWindows/6.4.0 (Windows 8; native)', debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['ads'][0]['ad_markup']['info'], 'impression auctioned but unsold')

    @allure.feature('bid request flat cpm')
    @allure.tag('smoke')
    @allure.story('flat cpm adjuster')
    @allure.description('Test for flat cpm adjuster works for flat cpm enabled placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_flat_cpm_adjuster_flat_cpm_enabled(self, pub_app_id):
        '''
        Data value from MongoDB, will be replaced by DB data connector in the future.

        rev_share = 0.5
        serving_cost = 0.05
        flat_cpm = 0.3
        cpm_floor = 0.1
        reserve_floor = 1.0
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=gb_ip, sdk_version='Vungle/6.3.2', debug='jaeger',
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        rev_share = 0.5
        serving_cost = 0.05
        flat_cpm = 0.3
        cpm_floor = 0.1
        reserve_floor = 1.0

        bid_floor = flat_cpm / (1 - serving_cost) / (rev_share * jaeger_adjuster)
        erpm_target = cpm_floor / (1 - serving_cost) / (rev_share * jaeger_adjuster)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if bid_floor < reserve_floor:
            assert_that(bid_request['imp'][0]['bidfloor'], equal_to(reserve_floor))
        else:
            assert_that(math.isclose(bid_request['imp'][0]['bidfloor'], bid_floor))
        assert_that(math.isclose(bid_request['imp'][0]['ext']['vungle']['erpmtarget'], erpm_target))
        assert_that(bid_request['imp'][0]['ext']['vungle']['revenue_share'], equal_to(rev_share * jaeger_adjuster))

    @allure.feature('bid request flat cpm')
    @allure.tag('smoke')
    @allure.story('flat cpm adjuster')
    @allure.description('Test for flat cpm adjuster works for flat cpm not enabled placement')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_flat_cpm_adjuster_flat_cpm_not_enabled(self, pub_app_id):
        '''
        Data value from MongoDB, will be replaced by DB data connector in the future.

        rev_share = 0.5
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'AREYOUS82690', ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=gb_ip, sdk_version='Vungle/6.3.2', debug='jaeger',
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        rev_share = 0.5

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['bidfloor'], bid_request['imp'][0]['ext']['vungle']['erpmtarget'])
        assert_that(bid_request['imp'][0]['ext']['vungle']['revenue_share'], equal_to(rev_share))

    @allure.feature('bid request flat cpm')
    @allure.tag('smoke')
    @allure.story('flat cpm adjuster')
    @allure.description('Test for flat cpm adjuster revenue share limitation')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_flat_cpm_adjuster_revenue_share_limitation(self, pub_app_id):
        '''
        The rev_share value of this placement is '1.2', it's only for revenue_share calculation testing.
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50918', ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=gb_ip, sdk_version='Vungle/5.0.9', debug='jaeger',
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['revenue_share'], equal_to(0.95))

    @allure.feature('bid request flat cpm')
    @allure.tag('smoke')
    @allure.story('flat cpm adjuster')
    @allure.description('Test for flat cpm adjuster works for app level settings')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_flat_cpm_adjuster_in_app_level(self, pub_app_id):
        '''
        Data value from MongoDB, will be replaced by DB data connector in the future.

        App level settings:

        rev_share = 0.6
        serving_cost = 0.05
        flat_cpm = 0.3
        cpm_floor = 0.1
        reserve_floor = 1.0
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'FLAT_CPM_TEST_01', ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=gb_ip, sdk_version='Vungle/6.3.2', debug='jaeger',
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        rev_share = 0.6
        serving_cost = 0.05
        flat_cpm = 0.3
        cpm_floor = 0.1
        reserve_floor = 1.0

        bid_floor = flat_cpm / (1 - serving_cost) / (rev_share * jaeger_adjuster)
        erpm_target = cpm_floor / (1 - serving_cost) / (rev_share * jaeger_adjuster)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        if bid_floor < reserve_floor:
            assert_that(bid_request['imp'][0]['bidfloor'], equal_to(reserve_floor))
        else:
            assert_that(math.isclose(bid_request['imp'][0]['bidfloor'], bid_floor))
        assert_that(math.isclose(bid_request['imp'][0]['ext']['vungle']['erpmtarget'], erpm_target))
        assert_that(bid_request['imp'][0]['ext']['vungle']['revenue_share'], equal_to(rev_share * jaeger_adjuster))

    @allure.feature('impression type')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1506 Update the logic to get placement type.')
    @allure.description('Verify impType for mrec placement which no type in placement level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_type_no_type_in_placement(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'INTER-MREC-001', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # impType won't display from the bid request, from v1.250.0
        # assert_that(bid_request['imp'][0]['ext']['impType'], equal_to('MREC'))

    @allure.feature('impression type')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1506 Update the logic to get placement type.')
    @allure.description(
        'Verify impType for mrec placement which no supported_template_types in placement level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_type_no_template_type_in_placement(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'INTER-MREC-002', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # impType won't display from the bid request, from v1.250.0
        # assert_that(bid_request['imp'][0]['ext']['impType'], equal_to('MREC'))

    @allure.feature('impression type')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1506 Update the logic to get placement type.')
    @allure.description('Verify impType for mrec placement with type mrec in placement level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_type_mrec_type_in_placement(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'INTER-MREC-003', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # impType won't display from the bid request, from v1.250.0
        # assert_that(bid_request['imp'][0]['ext']['impType'], equal_to('MREC'))

    @allure.feature('impression type')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1506 Update the logic to get placement type.')
    @allure.description('Verify impType for mrec placement in legacy format with type mrec in placement level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_type_mrec_type_in_placement_legacy(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'INTER-MREC-004', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.3.9',
                                          rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        # impType won't display from the bid request, from v1.250.0
        # assert_that(bid_request['imp'][0]['ext']['impType'], equal_to('MREC'))

    @allure.feature('impression type')
    @allure.tag('normal', 'test mode', 'R_1.124.0')
    @allure.story('PBJ-1506 Update the logic to get placement type.')
    @allure.description('Verify impType for mrec placement which type is not mrec in placement level setting')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_imp_type_type_not_mrec(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'INTER-MREC-005', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'impType')

    @allure.feature('image mrec support')
    @allure.tag('normal', 'test mode', 'R_1.125.0')
    @allure.story('PBJ-1528 support image mrec in jaeger')
    @allure.description('Verify the template type in bid request for image mrec ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_template_type_for_image_mrec(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'IMAGE-MREC-001', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(9 in bid_request['imp'][0]['ext']['vungle']['templatetypes'])
        # impType won't display from the bid request, from v1.250.0
        # assert_that(bid_request['imp'][0]['ext']['impType'], equal_to('MREC'))

    @allure.feature('image mrec support')
    @allure.tag('normal', 'test mode', 'R_1.125.0')
    @allure.story('PBJ-1528 support image mrec in jaeger')
    @allure.description('Verify the template type for image mrec in bid request ad with external Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_template_type_for_image_mrec_ext_kraken(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'IMAGE-MREC-001', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'vungle')
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'impType')

    @allure.feature('image mrec support')
    @allure.tag('normal', 'R_1.125.0')
    @allure.story('PBJ-1548 Verify template type when ads returns an image_mrec ad.')
    @allure.description('Verify the template type for image mrec ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_image_mrec_placement])
    def test_template_type_for_image_mrec_non_test_mode(self, pub_app_id, placement):
        test_ifa = gen_device_id(36)
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(9 in bid_request['imp'][0]['ext']['vungle']['templatetypes'])

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0', 'test_mode')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the skip field in openrtb25x for skippable ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_skippable_ad_openrtb25x(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'HJKM6GM50918', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['openrtb25x']['skip'], equal_to(1))

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0', 'test_mode')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the skip field in openrtb25x for skippable banner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_skippable_banner_openrtb25x(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'BANNER-TEST-01', ifa=test_mode_device_id, banner=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(
            debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['openrtb25x']['skip'], equal_to(1))

    @allure.feature('openrtb 2.5 support')
    @allure.tag('normal', 'R_1.126.0', 'test_mode')
    @allure.story('PBJ-1571 Apply OpenRTB 2.5 on Jaeger')
    @allure.description('Verify the skip field in openrtb25x for non skippable ad')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_non_skippable_ad_openrtb25x(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['openrtb25x']['skip'], equal_to(0))

    @allure.feature('bid request flat cpm')
    @allure.tag('smoke', 'R_1.131.0', 'test_mode')
    @allure.story(
        'PBJ-1752 Serve FlatCPM placements with geo-level dynamic floors even when geo-level flat_cpm does not exist')
    @allure.description('Test for flat cpm geo level change - flat cpm not enabled')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_flat_cpm_geo_change_1(self, pub_app_id):
        '''
        Placement level setting:

        "is_flat_cpm_enabled": false,
        "default_cpm_floor": 1,
        "default_flat_cpm": 0.4,
        "default_dynamic_cpm_floor": 0.2,
        "default_dynamic_cpm_floor_strategies": [],
        "geo_configs": {
            "DE": {
                "flat_cpm": 0.3,
                "dynamic_cpm_floor": 0.1,
                "dynamic_cpm_floor_strategies": []
            }
        },
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'FLAT_CPM_TEST_02', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=de_ip, debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['cpm_floor'], equal_to(1))

    @allure.feature('bid request flat cpm')
    @allure.tag('smoke', 'R_1.131.0', 'test_mode')
    @allure.story(
        'PBJ-1752 Serve FlatCPM placements with geo-level dynamic floors even when geo-level flat_cpm does not exist')
    @allure.description('Test for flat cpm geo level change - no flat cpm in placement geo config')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_flat_cpm_geo_change_2(self, pub_app_id):
        '''
        Placement level setting:

        "is_flat_cpm_enabled": true,
        "default_cpm_floor": 1,
        "default_dynamic_cpm_floor": 0.2,
        "default_dynamic_cpm_floor_strategies": [],
        "geo_configs": {
            "DE": {
                "dynamic_cpm_floor": 0.1,
                "dynamic_cpm_floor_strategies": []
            }
        },
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'FLAT_CPM_TEST_03', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=de_ip, debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['cpm_floor'], equal_to(1))

    @allure.feature('bid request flat cpm')
    @allure.tag('smoke', 'R_1.131.0', 'test_mode')
    @allure.story(
        'PBJ-1752 Serve FlatCPM placements with geo-level dynamic floors even when geo-level flat_cpm does not exist')
    @allure.description('Test for flat cpm geo level change - '
                        'no flat cpm and dynamic cpm floor strategies in placement geo config')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_flat_cpm_geo_change_3(self, pub_app_id):
        '''
        Placement level setting:

            "is_flat_cpm_enabled": true,
            "default_cpm_floor": 1,
            "default_flat_cpm": 0.1,
            "default_dynamic_cpm_floor": 0.6,
            "default_dynamic_cpm_floor_strategies": [{
                "name": "flatcpm_default_model",
                "floor": 1.3
            }],
            "geo_configs": {
                "DE": {
                    "dynamic_cpm_floor": 0.5
                }
            },
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'FLAT_CPM_TEST_04', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=de_ip, debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['cpm_floor'], equal_to(0.5))

    @allure.feature('bid request flat cpm')
    @allure.tag('smoke', 'R_1.131.0', 'test_mode')
    @allure.story(
        'PBJ-1752 Serve FlatCPM placements with geo-level dynamic floors even when geo-level flat_cpm does not exist')
    @allure.description('Test for flat cpm geo level change - '
                        'no flat but cpm dynamic cpm floor strategies in placement geo config')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_flat_cpm_geo_change_4(self, pub_app_id):
        '''
        Placement level setting:

            "is_flat_cpm_enabled": true,
            "default_cpm_floor": 1,
            "default_flat_cpm": 0.1,
            "default_dynamic_cpm_floor": 0.3,
            "default_dynamic_cpm_floor_strategies": [],
            "geo_configs": {
                "DE": {
                    "dynamic_cpm_floor": 0.4,
                    "dynamic_cpm_floor_strategies": [{
                        "name": "flatcpm_default_model",
                        "floor": 1.3
                    }]
                }
            },
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'FLAT_CPM_TEST_05', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=de_ip, debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['cpm_floor'], equal_to(1.3))

    @allure.feature('bid request flat cpm')
    @allure.tag('smoke', 'R_1.131.0', 'test_mode')
    @allure.story(
        'PBJ-1752 Serve FlatCPM placements with geo-level dynamic floors even when geo-level flat_cpm does not exist')
    @allure.description('Test for flat cpm geo level change - '
                        'flat cpm and dynamic cpm floor in but no dynamic flat cpm strategies in placement geo config')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_flat_cpm_geo_change_6(self, pub_app_id):
        '''
        Placement level setting:

            "is_flat_cpm_enabled": true,
            "default_cpm_floor": 1,
            "default_flat_cpm": 0.2,
            "default_dynamic_cpm_floor": 0.3,
            "default_dynamic_cpm_floor_strategies": [],
            "geo_configs": {
                "DE": {
                    "flat_cpm": 0.1,
                    "dynamic_cpm_floor": 1.8
                }
            },
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'FLAT_CPM_TEST_07', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=de_ip, debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['cpm_floor'], equal_to(1.8))

    @allure.feature('bid request flat cpm')
    @allure.tag('smoke', 'R_1.131.0', 'test_mode')
    @allure.story(
        'PBJ-1752 Serve FlatCPM placements with geo-level dynamic floors even when geo-level flat_cpm does not exist')
    @allure.description('Test for flat cpm geo level change - '
                        'no geo config but flat cpm floor and dynamic flat cpm floor in placement default setting')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_flat_cpm_geo_change_9(self, pub_app_id):
        '''
        Placement level setting:

            "is_flat_cpm_enabled": true,
            "default_cpm_floor": 1,
            "default_flat_cpm": 0.2,
            "default_dynamic_cpm_floor": 0.3,
            "geo_configs": {
                "DE": {}
            },
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, 'FLAT_CPM_TEST_10', ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=de_ip, debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['cpm_floor'], equal_to(0.3))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0')
    @allure.story('PBJ-1893 SKAdNetwork support - Jaeger passes network id list to Meister'
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger pass network id to Meister')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_skadnetwork_id_1(self, pub_app_id):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['test.ad.nw.001', 'test.nw.45646546', 'GTA9LK7P23.skadnetwork']
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0')
    @allure.story('PBJ-1893 SKAdNetwork support - Jaeger passes network id list to Meister'
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger pass network id without checking on db')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_skadnetwork_id_2(self, pub_app_id):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc']
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0')
    @allure.story('PBJ-1893 SKAdNetwork support - Jaeger passes network id list to Meister'
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for SDK does not pass any network id to Jaeger')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_skadnetwork_id_3(self, pub_app_id):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = []
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0', 'test_mode')
    @allure.story('PBJ-1893 SKAdNetwork support - Jaeger passes network id list to Meister'
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger pass network id to DSP side in test mode')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_skadnetwork_id_4(self, pub_app_id):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0', 'R_1.136.0', 'test_mode')
    @allure.story('PBJ-1908 SKAdNetwork support - Pass down sknetwork attribution and enable flag to delivery message',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled',
                  'PBJ-1933 SKAdNetwork support - Testing SKAdNetwork enable flag change from placement to application')
    @allure.description('Test for Jaeger pass network id to DSP side when SDK >= 6.8.0 and skadnetwork enabled '
                        'in app level')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0', 'Vungle/6.8.1'])
    def test_for_jaeger_pass_sk_ad_network_condition_1(self, pub_app_id, sdk_v):
        '''
        App level setting:

        "skadnetwork_placements": [{
            "$oid": "59786bc2a43b3a0862002774"   // "reference_id": "DEFAULT02021"
        }]
        
        app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0', 'test_mode')
    @allure.story('PBJ-1908 SKAdNetwork support - Pass down sknetwork attribution and enable flag to delivery message',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will not pass network id to DSP side when SDK < 6.8.0 and skadnetwork enabled'
                        'in app level')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.7.9'])
    def test_for_jaeger_pass_sk_ad_network_condition_2(self, pub_app_id, sdk_v):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0', 'test_mode')
    @allure.story('PBJ-1908 SKAdNetwork support - Pass down sknetwork attribution and enable flag to delivery message',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger pass network id to DSP side when SDK >= 6.8.0 and skadnetwork enabled '
                        'in app level, but no id list from request')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_sk_ad_network_condition_3(self, pub_app_id):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0', 'test_mode')
    @allure.story('PBJ-1908 SKAdNetwork support - Pass down sknetwork attribution and enable flag to delivery message',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger does not pass network id to DSP side when SDK >= 6.8.0 '
                        'but skadnetwork is not enabled in app level')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement_id', [common_test_placement_2, 'AREYOUS82694'])
    def test_for_jaeger_pass_sk_ad_network_condition_4(self, pub_app_id, placement_id):
        '''
            app level: skadnetwork_pub_enabled = false
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.135.0', 'test_mode')
    @allure.story('PBJ-1908 SKAdNetwork support - Pass down sknetwork attribution and enable flag to delivery message',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger does not pass network id to DSP side for Android in case of skadnetwork'
                        'enabled on app level')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    def test_for_jaeger_pass_sk_ad_network_condition_5(self, pub_app_id):
        '''
            app level: skadnetwork_pub_enabled = false
        '''
        network_ids = [kraken_served_ad_network_id, '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_android(pub_app_id, android_common_test_placement,
                                                android_id=test_mode_device_id, skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.136.0', 'test_mode')
    @allure.story('PBJ-1933 SKAdNetwork support - Testing SKAdNetwork enable flag change from placement to application',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger passes in case of placement not on the list in app level but the '
                        'skadnetwork_pub_enabled flag is enabled')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', ['HJKM6GM50918'])
    def test_for_skadnetwork_flag_change_to_app_1(self, pub_app_id, placement_id):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = [kraken_served_ad_network_id, '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.136.0', 'test_mode')
    @allure.story('PBJ-1933 SKAdNetwork support - Testing SKAdNetwork enable flag change from placement to application',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger pass network id in case of placement on the list in app level and the '
                        'previous flag is disabled, skadnetwork_pub_enabled is enabled')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', ['HJKM6GM50911'])
    def test_for_skadnetwork_flag_change_to_app_2(self, pub_app_id, placement_id):
        '''
        App level setting:

        "skadnetwork_placements": [{
            "$oid": "5e144d12b026b9fb214c3b7f"   // "reference_id": "HJKM6GM50911"
        }]

        skadnetwork_pub_enabled = true
        '''
        network_ids = [kraken_served_ad_network_id, '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('smoke', 'R_1.136.0', 'test_mode')
    @allure.story('PBJ-1933 SKAdNetwork support - Testing SKAdNetwork enable flag change from placement to application',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger does not pass network id to DSP side for Android in case of skadnetwork flag '
                        'enabled on app level')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_for_skadnetwork_flag_change_to_app_3(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = [kraken_served_ad_network_id, '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    # -------------------------------------------- skadnetwork programmatic -------------------------------------------

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-2627 Jaeger should only pass the adnetwork id list specific for the eDSP')
    @allure.description('Test for Jaeger pass network id to external VAST Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_skadnetwork_id_ext_vast(self, pub_app_id):
        '''
        RTB connection:
            "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
        '''
        network_ids = ['test.ad.nw.001', 'test.nw.45646546', 'GTA9LK7P23.skadnetwork']
        expected_skadn_ids = ["GTA9LK7P23.skadnetwork", "test.ad.nw.001"]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(isinstance(bid_request['imp'][0]['ext']['skadn']['version'], str))
        assert_that(bid_request['imp'][0]['ext']['skadn']['sourceapp'], equal_to(common_test_app_market_id))
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(expected_skadn_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-2627 Jaeger should only pass the adnetwork id list specific for the eDSP')
    @allure.description('Test for Jaeger pass network id to external VAST Kraken in non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_skadnetwork_id_ext_vast_non_test_mode(self, pub_app_id):
        '''
        RTB connection:
            "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
        '''
        network_ids = ['test.ad.nw.001', 'test.nw.45646546', 'GTA9LK7P23.skadnetwork']
        expected_skadn_ids = ["GTA9LK7P23.skadnetwork", "test.ad.nw.001"]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.8.0', src_ip=jp_ip))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(isinstance(bid_request['imp'][0]['ext']['skadn']['version'], str))
        assert_that(bid_request['imp'][0]['ext']['skadn']['sourceapp'], equal_to(common_test_app_market_id))
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(expected_skadn_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-2627 Jaeger should only pass the adnetwork id list specific for the eDSP')
    @allure.description('Test for Jaeger pass network id to external MRAID Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_ref_id', ['BANNER-TEST-01'])
    def test_for_jaeger_pass_skadnetwork_id_ext_mraid(self, pub_app_id, placement_ref_id):
        '''
        RTB connection:
            "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
        '''
        network_ids = ['test.ad.nw.001', 'test.nw.45646546', 'GTA9LK7P23.skadnetwork']
        expected_skadn_ids = ["GTA9LK7P23.skadnetwork", "test.ad.nw.001"]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_mraid,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(isinstance(bid_request['imp'][0]['ext']['skadn']['version'], str))
        assert_that(bid_request['imp'][0]['ext']['skadn']['sourceapp'], equal_to(common_test_app_market_id))
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(expected_skadn_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-2627 Jaeger should only pass the adnetwork id list specific for the eDSP')
    @allure.description('Test for Jaeger pass network id to external MRAID Kraken in non test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_ref_id', ['BANNER-TEST-01'])
    def test_for_jaeger_pass_skadnetwork_id_ext_mraid_non_test_mode(self, pub_app_id, placement_ref_id):
        '''
        RTB connection:
            "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
        '''
        network_ids = ['test.ad.nw.001', 'test.nw.45646546', 'GTA9LK7P23.skadnetwork']
        expected_skadn_ids = ["GTA9LK7P23.skadnetwork", "test.ad.nw.001"]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid,
                                          sdk_version='Vungle/6.8.0', src_ip=au_ip))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(isinstance(bid_request['imp'][0]['ext']['skadn']['version'], str))
        assert_that(bid_request['imp'][0]['ext']['skadn']['sourceapp'], equal_to(common_test_app_market_id))
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(expected_skadn_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-2627 Jaeger should only pass the adnetwork id list specific for the eDSP')
    @allure.description('Test for Jaeger pass network id to external Kraken without checking on db')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_skadnetwork_id_ext_2(self, pub_app_id):
        '''
        RTB connection:
            "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc']
        expected_skadn_ids = ['GTA9LK7P23.skadnetwork']
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(expected_skadn_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support')
    @allure.description('Test for SDK does not pass any network id to Jaeger, external Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_skadnetwork_id_ext_3(self, pub_app_id):
        network_ids = []
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'R_1.139.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support')
    @allure.description('Test for SDK does not pass any network id to Jaeger in non test mode, external Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_skadnetwork_id_ext_3_non_test_mode(self, pub_app_id):
        network_ids = []
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.8.0', src_ip=jp_ip))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled',
                  'PBJ-2627 Jaeger should only pass the adnetwork id list specific for the eDSP')
    @allure.description('Test for Jaeger pass network id to external Kraken side when SDK >= 6.8.0 '
                        'and skadnetwork enabled in app level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0', 'Vungle/6.8.1'])
    def test_for_jaeger_pass_sk_ad_network_condition_ext_1(self, pub_app_id, sdk_v):
        '''
        App level setting:

        "skadnetwork_placements": [{
            "$oid": "59786bc2a43b3a0862002774"   // "reference_id": "DEFAULT02021"
        }]

        skadnetwork_pub_enabled = true

        RTB connection:
        "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        expected_skadn_ids = ["GTA9LK7P23.skadnetwork", "test.ad.nw.001"]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(expected_skadn_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger not pass network id to external Kraken side when SDK < 6.8.0 '
                        'and skadnetwork enabled in app level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.7.9'])
    def test_for_jaeger_pass_sk_ad_network_condition_ext_2(self, pub_app_id, sdk_v):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'skadn')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger does not pass network id to external Kraken side when SDK >= 6.8.0 and '
                        'skadnetwork enabled in app level, but no id list from request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_for_jaeger_pass_sk_ad_network_condition_ext_3(self, pub_app_id):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger passes network id to external Kraken side when SDK >= 6.8.0 '
                        'and skadnetwork is not enabled in app level')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement_id', [common_test_placement_2, 'AREYOUS82694'])
    def test_for_jaeger_pass_sk_ad_network_condition_ext_4(self, pub_app_id, placement_id):
        '''
            app level: skadnetwork_pub_enabled = false
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        expected_skadn_ids = ["GTA9LK7P23.skadnetwork", "test.ad.nw.001"]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(expected_skadn_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.170.0')
    @allure.story('PBJ-3001 only iOS bid request should contain skadnetwork data')
    @allure.description('Test that there is no skadn obj from Android bid request for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_no_skadnetwork_data_android_1(self, pub_app_id, placement):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'skadn')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.170.0')
    @allure.story('PBJ-3001 only iOS bid request should contain skadnetwork data')
    @allure.description('Test that there is no skadn obj from Android bid request for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_no_skadnetwork_data_android_2(self, pub_app_id, placement):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled',
                  'PBJ-2627 Jaeger should only pass the adnetwork id list specific for the eDSP')
    @allure.description('Test for Jaeger will pass in case of placement not on the list in app level, the'
                        ' previous flag is enabled, and skadnetwork enabled for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', ['HJKM6GM50918'])
    def test_for_skadnetwork_flag_change_to_app_ext_1(self, pub_app_id, placement_id):
        '''
        RTB connection:
            "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]

        app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        expected_skadn_ids = ["GTA9LK7P23.skadnetwork", "test.ad.nw.001"]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(expected_skadn_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'R_1.139.0', 'v1.159.0')
    @allure.story('PBJ-2004 SKAdNetwork support - programmatic support',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled',
                  'PBJ-2627 Jaeger should only pass the adnetwork id list specific for the eDSP')
    @allure.description('Test for Jaeger pass network id in case of placement on the list in app level, the '
                        'previous flag is disabled, and skadnetwork enabled for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', ['HJKM6GM50911'])
    def test_for_skadnetwork_flag_change_to_app_ext_2(self, pub_app_id, placement_id):
        '''
        App level setting:

        "skadnetwork_placements": [{
            "$oid": "5e144d12b026b9fb214c3b7f"   // "reference_id": "HJKM6GM50911"
        }]

        skadnetwork_pub_enabled = true

        RTB connection:
            "adnetwork_ids": ["GTA9LK7P23.skadnetwork", "edsp.test", "test.ad.nw.001"]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        expected_skadn_ids = ["GTA9LK7P23.skadnetwork", "test.ad.nw.001"]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(expected_skadn_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.170.0')
    @allure.story('PBJ-3001 only iOS bid request should contain skadnetwork data')
    @allure.description('Test that there is no skadn obj from Android bid request for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', ['CC4RVAN74965'])
    def test_no_skadnetwork_data_android_3(self, pub_app_id, placement):
        network_ids = ['APZHY3VA96.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'skadn')

    @allure.feature('header bidding')
    @allure.tag('normal', 'v1.153.0')
    @allure.story('PBJ-2429 Jaeger pass down HBP flag to DSP')
    @allure.description('Verify the value of is_header_bidding is true via hb request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_header_bidding_flag_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['is_header_bidding'], equal_to(True))

    @allure.feature('header bidding')
    @allure.tag('normal', 'v1.153.0')
    @allure.story('PBJ-2429 Jaeger pass down HBP flag to DSP')
    @allure.description('Verify the value of is_header_bidding is true via hb request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_header_bidding_flag_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['ext']['vungle'], 'is_header_bidding')

    @allure.feature('header bidding')
    @allure.tag('normal', 'test_mode', 'v1.153.0')
    @allure.story('PBJ-2429 Jaeger pass down HBP flag to DSP')
    @allure.description('Verify the value of is_header_bidding is true via hb request in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_header_bidding_flag_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['is_header_bidding'], equal_to(True))

    @allure.feature('header bidding')
    @allure.tag('normal', 'test_mode', 'v1.153.0')
    @allure.story('PBJ-2429 Jaeger pass down HBP flag to DSP')
    @allure.description('Verify the value of is_header_bidding is true via hb request in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_header_bidding_flag_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['ext']['vungle'], 'is_header_bidding')

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will pass plist with skadnetwork enabled placement for eDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_for_no_skadnetwork_enabled_check_edsp_1(self, pub_app_id, placement):
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will pass plist with skadnetwork enabled placement for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_for_no_skadnetwork_enabled_check_edsp_2(self, pub_app_id, placement):
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will pass plist with skadnetwork not enabled app for eDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    def test_for_no_skadnetwork_enabled_check_edsp_3(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = false
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will pass plist with skadnetwork not enabled app for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    def test_for_no_skadnetwork_enabled_check_edsp_4(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = false
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will pass plist with skadnetwork enabled but placement not on the '
                        'skadnetwork_placements list for eDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50918'])
    def test_for_no_skadnetwork_enabled_check_edsp_3_1(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will pass plist with skadnetwork enabled but placement not on the '
                        'skadnetwork_placements list for eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50918'])
    def test_for_no_skadnetwork_enabled_check_edsp_4_1(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=jp_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['skadnetids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will not pass plist with skadnetwork not enabled app for iDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    def test_for_no_skadnetwork_enabled_check_edsp_5_1(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = false
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will not pass plist with skadnetwork not enabled app for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    def test_for_no_skadnetwork_enabled_check_edsp_6_1(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = false
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will pass plist with skadnetwork enabled but placement not on the '
                        'skadnetwork_placements list for iDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50918'])
    def test_for_no_skadnetwork_enabled_check_edsp_5(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will pass plist with skadnetwork enabled but placement not on the '
                        'skadnetwork_placements list for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50918'])
    def test_for_no_skadnetwork_enabled_check_edsp_6(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will pass plist with skadnetwork enabled app and placment in the old list '
                        'for iDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_for_no_skadnetwork_enabled_check_edsp_7(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.159.0')
    @allure.story('PBJ-2632 Jaeger should not check the skadnetwork enabled or not for eDSP',
                  'PBJ-3262 Don\'t look at placement level skadnetworkenabled')
    @allure.description('Test for Jaeger will pass plist with skadnetwork enabled app and placement in the old list '
                        'for iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_for_no_skadnetwork_enabled_check_edsp_8(self, pub_app_id, placement):
        '''
            app level: skadnetwork_pub_enabled = true
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', 'edsp.test', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.160.0')
    @allure.story('PBJ-2665 Support extending SKAdNetwork enablement to all placements in an app')
    @allure.description('Test for all placement will be applied when skadnetwork_pub_enabled is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', ['HJKM6GM509080'])
    def test_for_skadnetwork_enable_flag_1(self, pub_app_id, placement_id):
        '''
        App level setting:

        "skadnetwork_pub_enabled": true,
        "skadnetwork_placements": [{
            "$oid": "5f0dbd204bd09d05f8bb7464"          // not the test placement
        }]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.160.0', 'test_mode')
    @allure.story('PBJ-2665 Support extending SKAdNetwork enablement to all placements in an app')
    @allure.description('Test for all placement will be applied when skadnetwork_pub_enabled is true in idsp test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', ['HJKM6GM509080'])
    def test_for_skadnetwork_enable_flag_2(self, pub_app_id, placement_id):
        '''
        App level setting:

        "skadnetwork_pub_enabled": true,
        "skadnetwork_placements": [{
            "$oid": "5f0dbd204bd09d05f8bb7464"          // not the test placement
        }]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal')
    @allure.story("PBJ-3262 Don't look at placement level skadnetworkenabled")
    @allure.description('Test for all placement will be applied when skadnetwork_pub_enabled is true '
                        'and will not look at placement setting any more')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['59786bc2a43b3a08620026b9'])
    @pytest.mark.parametrize('placement_id', ['DEFAULT02029'])
    def test_for_skadnetwork_enable_flag_3(self, pub_app_id, placement_id):
        '''
        App level setting:

        "skadnetwork_pub_enabled": true,

        Placement level setting:
        "is_skadnetwork_enabled": false,
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.160.0')
    @allure.story('PBJ-2665 Support extending SKAdNetwork enablement to all placements in an app')
    @allure.description('Test for all placement will not be applied when skadnetwork_pub_enabled is true'
                        'but SDK version < 6.8.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', ['HJKM6GM509080'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.7.9'])
    def test_for_skadnetwork_enable_flag_4(self, pub_app_id, placement_id, sdk_v):
        '''
        App level setting:

        "skadnetwork_pub_enabled": true,
        "skadnetwork_placements": [{
            "$oid": "5f0dbd204bd09d05f8bb7464"          // not the test placement
        }]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.160.0')
    @allure.story('PBJ-2665 Support extending SKAdNetwork enablement to all placements in an app')
    @allure.description('Test for all placement will be applied when skadnetwork_pub_enabled is true'
                        'and SDK version >= 6.8.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement_id', ['HJKM6GM509080'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0', 'Vungle/6.8.1'])
    def test_for_skadnetwork_enable_flag_5(self, pub_app_id, placement_id, sdk_v):
        '''
        App level setting:

        "skadnetwork_pub_enabled": true,
        "skadnetwork_placements": [{
            "$oid": "5f0dbd204bd09d05f8bb7464"          // not the test placement
        }]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to(network_ids))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.160.0', 'test_mode')
    @allure.story('PBJ-2665 Support extending SKAdNetwork enablement to all placements in an app')
    @allure.description('Test for all placement will not be applied for Android when skadnetwork_pub_enabled is true')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_for_skadnetwork_enable_flag_6(self, pub_app_id, placement):
        '''
        App level setting:

        "skadnetwork_pub_enabled": true
        '''
        network_ids = ['APZHY3VA96.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.160.0')
    @allure.story('PBJ-2665 Support extending SKAdNetwork enablement to all placements in an app')
    @allure.description('Test for all placement will not be applied when skadnetwork_pub_enabled is false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement_id', [common_test_placement_2])
    def test_for_skadnetwork_enable_flag_7(self, pub_app_id, placement_id):
        '''
        App level setting:

        "skadnetwork_pub_enabled": false,
        "skadnetwork_placements": [{
            "$oid": "5f68be4ed5ba35022aeace75"          // the test placement
        }]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.160.0', 'test_mode')
    @allure.story('PBJ-2665 Support extending SKAdNetwork enablement to all placements in an app')
    @allure.description('Test for all placement will not be applied when skadnetwork_pub_enabled is false'
                        'in idsp test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement_id', [common_test_placement_2])
    def test_for_skadnetwork_enable_flag_8(self, pub_app_id, placement_id):
        '''
        App level setting:

        "skadnetwork_pub_enabled": false,
        "skadnetwork_placements": [{
            "$oid": "5f68be4ed5ba35022aeace75"          // the test placement
        }]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1,
                                          sdk_version='Vungle/6.8.0'))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.160.0')
    @allure.story('PBJ-2665 Support extending SKAdNetwork enablement to all placements in an app')
    @allure.description('Test for all placement will not be applied when skadnetwork_pub_enabled is false'
                        'but SDK version < 6.8.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement_id', [common_test_placement_2])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.7.9'])
    def test_for_skadnetwork_enable_flag_10(self, pub_app_id, placement_id, sdk_v):
        '''
        App level setting:

        "skadnetwork_pub_enabled": false,
        "skadnetwork_placements": [{
            "$oid": "5f68be4ed5ba35022aeace75"          // the test placement
        }]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.160.0')
    @allure.story('PBJ-2665 Support extending SKAdNetwork enablement to all placements in an app')
    @allure.description('Test for all placement will not be applied when skadnetwork_pub_enabled is false'
                        'and SDK version >= 6.8.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement_id', [common_test_placement_2])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0', 'Vungle/6.8.1'])
    def test_for_skadnetwork_enable_flag_11(self, pub_app_id, placement_id, sdk_v):
        '''
        App level setting:

        "skadnetwork_pub_enabled": false,
        "skadnetwork_placements": [{
            "$oid": "5f68be4ed5ba35022aeace75"          // the test placement
        }]
        '''
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=meister_rtb_ids,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['skadnetwork']['adnetworkids'], equal_to([]))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for idsp when sdk >= 6.9.2 and osv >= 14.5 '
                        'in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_for_skadimpression_version_1(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.2'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0', '2.2']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for idsp when sdk < 6.9.2 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_for_skadimpression_version_2(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for idsp when osv < 14.5 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_for_skadimpression_version_3(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids_1,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0']))


    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for idsp when sdk < 6.9.2 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_for_skadimpression_version_2_e(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_mraid,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0']))




    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for idsp when sdk >= 6.9.2 and osv >= 14.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5', '14.6'])
    def test_for_skadimpression_version_4(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=non_test_mode_kraken_rtb_ids,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.2'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0', '2.2']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for idsp when sdk < 6.9.2')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_for_skadimpression_version_5(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=non_test_mode_kraken_rtb_ids,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for idsp when osv < 14.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_for_skadimpression_version_6(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=non_test_mode_kraken_rtb_ids,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0']))


    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for idsp when osv < 14.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_for_skadimpression_version_6_e(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0']))


    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for edsp when sdk >= 6.9.2 and osv >= 14.5 '
                        'in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5', '14.6'])
    def test_for_skadimpression_version_7(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.2'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0', '2.2']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for edsp when sdk < 6.9.2 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_for_skadimpression_version_8(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0', 'test_mode')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for edsp when osv < 14.5 in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_for_skadimpression_version_9(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for edsp when sdk >= 6.9.2 and osv >= 14.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5', '14.6'])
    def test_for_skadimpression_version_10(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.2'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0', '2.2']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for edsp when sdk < 6.9.2')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('osv', ['14.5'])
    def test_for_skadimpression_version_11(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.161.0')
    @allure.story('PBJ-2681 Jaeger should support SKAdImpression for both internal and external ads')
    @allure.description('Test for skadn version from bid request for edsp when osv < 14.5')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.4'])
    def test_for_skadimpression_version_12(self, pub_app_id, placement_id, sdk_v, osv):
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0']))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.212.0')
    @allure.story('PBJ-4065 Bigabid - NO SKAN Attribution')
    @allure.description('Test jaeger will parse new skadn obj and add to attribution')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5', '14.6'])
    def test_for_parse_skadn_obj_for_edsp_01(self, pub_app_id, placement_id, sdk_v, osv):
        skadn_obj = 'seatbid.0.bid.0.ext.skadn@{"version":"2.2","network":"cDkw7geQsH.skadnetwork","campaign":"45",' \
                    '"itunesitem":"880047117","sourceapp":"123456789","fidelities":[{"fidelity":0,' \
                    '"signature":"MEQCIEQlmZRNfYzKa","nonce":"473b1a16-b4ef-43ad-9591-fcf3aefa82a7","timestamp":"1594406341232"},' \
                    '{"fidelity":1,"signature":"MEQCIEQlmZRNfYzLa","nonce":"e650de09-2a9f-4dc3-a4d1-544c402e9095",' \
                    '"timestamp":"1594406341455"}],"ext":{}}'
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(),
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, sdk_version=sdk_v, override_bid_response_any=skadn_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.2'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0', '2.2']))
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.2'))
        storekit = ad_markup['attribution']['skadnetwork']['storekit']
        assert_that(storekit['fidelity_type'], equal_to(1))
        assert_that(storekit['ad_network_id'], equal_to('cDkw7geQsH.skadnetwork'))
        assert_that(storekit['source_app_id'],equal_to(123456789))
        assert_that(storekit['itunes_item_id'],equal_to(880047117))
        assert_that(storekit['signature'], equal_to('MEQCIEQlmZRNfYzLa'))
        assert_that(storekit['campaign_id'], equal_to(45))
        assert_that(storekit['nonce'], equal_to('e650de09-2a9f-4dc3-a4d1-544c402e9095'))
        assert_that(storekit['timestamp'], equal_to(1594406341455))
        viewthrough = ad_markup['attribution']['skadnetwork']['viewthrough']
        assert_that(viewthrough['fidelity_type'], equal_to(0))
        assert_that(viewthrough['signature'], equal_to('MEQCIEQlmZRNfYzKa'))
        assert_that(viewthrough['nonce'], equal_to('473b1a16-b4ef-43ad-9591-fcf3aefa82a7'))
        assert_that(viewthrough['timestamp'], equal_to(1594406341232))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.212.0')
    @allure.story('PBJ-4065 Bigabid - NO SKAN Attribution')
    @allure.description('Test jaeger will parse new skadn obj and add to attribution')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('osv', ['14.5', '14.6'])
    def test_for_parse_skadn_obj_for_edsp_02(self, pub_app_id, placement_id, sdk_v, osv):
        skadn_obj = 'seatbid.0.bid.0.ext.skadn@{"version":"2.2","network":"cDkw7geQsH.skadnetwork","campaign":"45",' \
                    '"itunesitem":"880047117","sourceapp":"123456789","fidelities":[{"fidelity":0,' \
                    '"signature":"MEQCIEQlmZRNfYzKa","nonce":"473b1a16-b4ef-43ad-9591-fcf3aefa82a7","timestamp":"1594406341232"},' \
                    '{"fidelity":1,"signature":"MEQCIEQlmZRNfYzLa","nonce":"e650de09-2a9f-4dc3-a4d1-544c402e9095",' \
                    '"timestamp":"1594406341455"}],"ext":{}}'
        network_ids = ['GTA9LK7P23.skadnetwork', '12234233.aasdfcbc', 'test.ad.nw.001']
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id,
                                            skadnetwork_ids=network_ids, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, sdk_version=sdk_v, override_bid_response_any=skadn_obj))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('2.2'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0', '2.2']))
        assert_keys_exist(ad_markup, 'attribution')
        assert_that(ad_markup['attribution']['method'], equal_to('skadnetwork'))
        assert_that(ad_markup['attribution']['skadnetwork']['version'], equal_to('2.2'))
        storekit = ad_markup['attribution']['skadnetwork']['storekit']
        assert_that(storekit['fidelity_type'], equal_to(1))
        assert_that(storekit['ad_network_id'], equal_to('cDkw7geQsH.skadnetwork'))
        assert_that(storekit['source_app_id'],equal_to(123456789))
        assert_that(storekit['itunes_item_id'],equal_to(880047117))
        assert_that(storekit['signature'], equal_to('MEQCIEQlmZRNfYzLa'))
        assert_that(storekit['campaign_id'], equal_to(45))
        assert_that(storekit['nonce'], equal_to('e650de09-2a9f-4dc3-a4d1-544c402e9095'))
        assert_that(storekit['timestamp'], equal_to(1594406341455))
        viewthrough = ad_markup['attribution']['skadnetwork']['viewthrough']
        assert_that(viewthrough['fidelity_type'], equal_to(0))
        assert_that(viewthrough['signature'], equal_to('MEQCIEQlmZRNfYzKa'))
        assert_that(viewthrough['nonce'], equal_to('473b1a16-b4ef-43ad-9591-fcf3aefa82a7'))
        assert_that(viewthrough['timestamp'], equal_to(1594406341232))

    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.216.0')
    @allure.story('PBJ-4183 Add support for SKAN 3.0 Attribution')
    @allure.description('Test jaeger will support SKAN 3.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['14.6', '15.1'])
    def test_for_support_skan_3_0_e_t(self, pub_app_id, placement_id, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('3.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0', '2.2','3.0']))
        bid_response = get_bid_response_obj_from_jaeger_explain(response_payload)
        seatbid = bid_response['seatbid']
        ext = seatbid[0]['bid'][0]['ext']
        assert_that(ext['skadn']['version'], equal_to('3.0'))


    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.216.0')
    @allure.story('PBJ-4183 Add support for SKAN 3.0 Attribution')
    @allure.description('Test jaeger will support SKAN 3.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['14.6', '15.1'])
    def test_for_support_skan_3_0_e(self, pub_app_id, placement_id, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('3.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0', '2.2', '3.0']))
        bid_response = get_bid_response_obj_from_jaeger_explain(response_payload)
        seatbid = bid_response['seatbid']
        ext = seatbid[0]['bid'][0]['ext']
        assert_that(ext['skadn']['version'], equal_to('3.0'))


    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'test_mode', 'v1.216.0')
    @allure.story('PBJ-4183 Add support for SKAN 3.0 Attribution')
    @allure.description('Test jaeger will support SKAN 3.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['14.6', '15.1'])
    def test_for_support_skan_3_0_i_t(self, pub_app_id, placement_id, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=test_mode_device_id, os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=test_mode_kraken_rtb_ids,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('3.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0', '2.2', '3.0']))


    @allure.feature('skadnetwork support')
    @allure.tag('normal', 'v1.216.0')
    @allure.story('PBJ-4183 Add support for SKAN 3.0 Attribution')
    @allure.description('Test jaeger will support SKAN 3.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('osv', ['14.6', '15.1'])
    def test_for_support_skan_3_0_i(self, pub_app_id, placement_id, sdk_v, osv):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(), os_version=osv)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=non_test_mode_kraken_rtb_ids,
                                          src_ip=au_ip, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['skadn']['version'], equal_to('3.0'))
        assert_that(bid_request['imp'][0]['ext']['skadn']['versions'], equal_to(['2.0', '2.2', '3.0']))




    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.167.0', 'v1.170.0')
    @allure.story('PBJ-2930 hb_partner in the bidrequest that sent to meister')
    @allure.description('Verify the hb partner name from imp ext for hb traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.8.0;Mopub', 'Vungle/6.8.0;vunglehbs/3.0.0',
                                       'Vungle/6.8.0;vunglehbs/4.0.0', 'Vungle/6.8.0;vunglehbs/5.0.0',
                                       'Vungle/6.8.0;vunglehbs/6.0.0', 'Vungle/6.9.0;vunglehbs/9.0.0',
                                       'Vungle/6.9.0;vunglehbs/10.0.0'])
    def test_imp_ext_hb_partner_1(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=sdk_v,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        data = {
            'Vungle/6.8.0;Mopub': 'mopub',
            'Vungle/6.8.0;vunglehbs/3.0.0': 'saygames',
            'Vungle/6.8.0;vunglehbs/4.0.0': 'ohayoo',
            'Vungle/6.8.0;vunglehbs/5.0.0': 'aequus',
            'Vungle/6.8.0;vunglehbs/6.0.0': 'charboost',
            'Vungle/6.9.0;vunglehbs/9.0.0': 'rovio',
            'Vungle/6.9.0;vunglehbs/10.0.0': 'admost'
        }
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['ext']['vungle']['hb_partner'], equal_to(data[sdk_v]))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.167.0')
    @allure.story('PBJ-2930 hb_partner in the bidrequest that sent to meister')
    @allure.description('Verify the hb partner name from imp ext for hb traffic in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_imp_ext_hb_partner_1t(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.8.0;Mopub',
                                          rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['ext']['vungle']['hb_partner'], equal_to('mopub'))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.167.0')
    @allure.story('PBJ-2930 hb_partner in the bidrequest that sent to meister')
    @allure.description('Verify there is no hb partner name from imp ext for non-hb traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_imp_ext_hb_partner_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.8.0;Mopub',
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['imp'][0]['ext']['vungle'], 'hb_partner')

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.167.0')
    @allure.story('PBJ-2930 hb_partner in the bidrequest that sent to meister')
    @allure.description('Verify there is no hb partner name from imp ext if there the sdk version has no partner info')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_imp_ext_hb_partner_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.8.0',
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['imp'][0]['ext']['vungle'], 'hb_partner')

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.167.0')
    @allure.story('PBJ-2930 hb_partner in the bidrequest that sent to meister')
    @allure.description('Verify there is no hb partner name from imp ext for edsp')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_imp_ext_hb_partner_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version='Vungle/6.8.0;Mopub', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'vungle')

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0')
    @allure.story('PBJ-3035 Supported template types for native placement')
    @allure.description('Verify the template type in bid request for native type placement via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(10 in bid_request['imp'][0]['ext']['vungle']['templatetypes'])

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.170.0', 'test_mode')
    @allure.story('PBJ-3035 Supported template types for native placement')
    @allure.description('Verify the template type in bid request for native type placement via iDSP in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_native_placement_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(10 in bid_request['imp'][0]['ext']['vungle']['templatetypes'])

    @allure.feature('HBP partner name')
    @allure.tag('smoke', 'v1.173.0')
    @allure.story('PBJ-3027 hb plugin version mapping name')
    @allure.description('Verify hb partners plugin version mapping from mongodb setting for in house type')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_plugin_mapping_in_house_mapping(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.10.1;' + test_in_house_plugin_name, debug='jaeger',
                                          rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        hb_partner = bid_request['imp'][0]['ext']['vungle']['hb_partner']
        assert_that(hb_partner, equal_to(test_in_house_partner))

    @allure.feature('HBP partner name')
    @allure.tag('smoke', 'v1.173.0')
    @allure.story('PBJ-3027 hb plugin version mapping name')
    @allure.description('Verify hb partners plugin version mapping from mongodb setting for commercial type')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_plugin_mapping_commercial_mapping(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.10.1;' + test_commercial_plugin_name, debug='jaeger',
                                          rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        hb_partner = bid_request['imp'][0]['ext']['vungle']['hb_partner']
        assert_that(hb_partner, equal_to(test_commercial_partner))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.173.0')
    @allure.story('PBJ-3027 hb plugin version mapping name')
    @allure.description('Verify hb partners plugin version mapping for non-existing in house partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_plugin_mapping_plugin_not_existing_db(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.10.1;vunglehbs/9999.0.0', debug='jaeger',
                                          rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        hb_partner = bid_request['imp'][0]['ext']['vungle']['hb_partner']
        assert_that(hb_partner, equal_to('vunglehbs'))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.173.0')
    @allure.story('PBJ-3027 hb plugin version mapping name')
    @allure.description('Verify hb partners plugin version mapping for non-existing commercial partner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_plugin_mapping_plugin_not_existing_db_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.10.1;abcd', debug='jaeger',
                                          rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        hb_partner = bid_request['imp'][0]['ext']['vungle']['hb_partner']
        assert_that(hb_partner, equal_to('abcd'))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.173.0')
    @allure.story('PBJ-3027 hb plugin version mapping name')
    @allure.description('Verify hb partners plugin version mapping for an invalid plugin')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_hb_plugin_mapping_plugin_invalid_plugin(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.10.1;vunglehbs/mopub', debug='jaeger',
                                          rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        hb_partner = bid_request['imp'][0]['ext']['vungle']['hb_partner']
        assert_that(hb_partner, equal_to('vunglehbs'))

    @allure.feature('HBP partner name')
    @allure.tag('normal', 'v1.173.0')
    @allure.story('PBJ-3027 hb plugin version mapping name')
    @allure.description('Verify there is no hb_parnter field from bid response for non-hb traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1;' + test_in_house_plugin_name,
                                       'Vungle/6.10.1;' + test_commercial_plugin_name])
    def test_hb_plugin_mapping_plugin_non_hb_traffic(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['imp'][0]['ext']['vungle'], 'hb_partner')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid request via sdv version >=6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_bid_request_traffic(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v, debug='jaeger',
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        deeplink = bid_request['imp'][0]['ext']['deeplink']
        assert_that(deeplink, equal_to(1))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid request via sdv version < 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_no_deeplink_in_bid_request_traffic(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'deeplink')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid request for test mode via sdv version >=6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_bid_request_traffic_test_mode(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        deeplink = bid_request['imp'][0]['ext']['deeplink']
        assert_that(deeplink, equal_to(1))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid request for test mode iDSP when sdk version >=6.11.0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids])
    def test_deeplink_in_bid_request_idsp_test_mode(self, pub_app_id, placement, sdk_v, hb, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=ca_us_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        deeplink = bid_request['imp'][0]['ext']['deeplink']
        assert_that(deeplink, equal_to(1))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid request for non test mode iDSP when sdk version >=6.11.0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_deeplink_in_bid_request_idsp_non_test_mode(self, pub_app_id, placement, sdk_v, hb, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        deeplink = bid_request['imp'][0]['ext']['deeplink']
        assert_that(deeplink, equal_to(1))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid request for test mode iDSP when sdk version <6.11.0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids])
    def test_no_deeplink_in_bid_request_idsp_test_mode(self, pub_app_id, placement, sdk_v, hb, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(src_ip=ca_us_ip, sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'deeplink')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid request for test mode via sdv version >=6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_deeplink_in_bid_request_traffic_test_mode(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=hb, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version=sdk_v, debug='jaeger',
                                                                        rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'deeplink')

# ------------------------------------------- deeplink for android --------------------------------------------------

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid request via sdv version >=6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_bid_request_android(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v, debug='jaeger',
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        deeplink = bid_request['imp'][0]['ext']['deeplink']
        assert_that(deeplink, equal_to(1))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid request via sdv version < 6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_no_deeplink_in_bid_request_android(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=jp_ip, sdk_version=sdk_v, debug='jaeger',
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'deeplink')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid request for test mode via sdv version >=6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_deeplink_in_bid_request_traffic_test_mode_android_1(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb,
                                                android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, debug='jaeger',
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        deeplink = bid_request['imp'][0]['ext']['deeplink']
        assert_that(deeplink, equal_to(1))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid request for test mode iDSP when sdk >=6.11.0')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids])
    def test_deeplink_in_bid_request_idsp_test_mode_android(self, pub_app_id, placement, sdk_v, hb, rtb):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb,
                                                android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=ca_us_ip, sdk_version=sdk_v, debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        deeplink = bid_request['imp'][0]['ext']['deeplink']
        assert_that(deeplink, equal_to(1))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is deeplink field from bid request for non test mode iDSP when sdk >=6.11.0')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_deeplink_in_bid_request_idsp_non_test_mode_android(self, pub_app_id, placement, sdk_v, hb, rtb):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v, debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        deeplink = bid_request['imp'][0]['ext']['deeplink']
        assert_that(deeplink, equal_to(1))

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid request for test mode iDSP when sdk <6.11.0')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('rtb', [test_mode_kraken_rtb_ids])
    def test_no_deeplink_in_bid_request_idsp_test_mode_android(self, pub_app_id, placement, sdk_v, hb, rtb):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb,
                                                android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=ca_us_ip, sdk_version=sdk_v, debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'deeplink')

    @allure.feature('Deeplink')
    @allure.story('PBJ-3237 Implement DeepLink logic in Supply side')
    @allure.description('Verify there is no deeplink field from bid request for test mode via sdv version >=6.11.0'
                        ' and eDSP')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('hb', [True, False])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_deeplink_in_bid_request_traffic_test_mode_android_2(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, header_bidding=hb,
                                                android_id=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, debug='jaeger',
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'deeplink')

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for rewarded via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_instl_rewarded_flag_1(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['rewarded'], equal_to(1))

    @allure.feature('interstitial flag')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3311 Align "Instl" with oRTB standeard')
    @allure.description('Verify the instl value without override for interstitial via idsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_instl_rewarded_flag_2(self, pub_app_id, placement, rtb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))

        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['vungle']['rewarded'], equal_to(0))

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.179.0')
    @allure.story('PBJ-3340 Pass the following signals to LiftOff for an experiment '
                  'PBJ-3434 Pass flatCPM value to liftoff')
    @allure.description('Verify the pptype value of app bidding for vast liftoff rtb connection'
                        'Verify existing  imp[].ext.fcv field in bid request for vast lift rtb connection ')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_liftoff_rtb_1(self, pub_app_id, placement, rtb):

        """
        flat_cpm_setting_in_placement=
        {
            "is_flat_cpm_enable": True,
            "default_flat_cpm": 0.4
        }
        """

        if env == 'ci':
            rtb = rtb.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=False, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['ext']['pptype'], equal_to(1))
        assert_keys_exist(bid_request['imp'][0]['ext'], 'fcv')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.179.0')
    @allure.story('PBJ-3340 Pass the following signals to LiftOff for an experiment '
                  'PBJ-3434 Pass flatCPM value to liftoff')
    @allure.description('Verify the pptype value of app bidding for mraid liftoff rtb connection'
                        'Verify not existing  imp[].ext.fcv field in bid request for mraid liftoff rtb connection')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_liftoff_rtb_2(self, pub_app_id, placement):
        """
             flat_cpm_setting_in_placement=
             {
                 "is_flat_cpm_enable": False,
             }
        """
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid_liftoff.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True, ifa=gen_device_id(),
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['ext']['pptype'], equal_to(3))
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'fcv')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.179.0')
    @allure.story('PBJ-3340 Pass the following signals to LiftOff for an experiment '
                  'PBJ-3434 Pass flatCPM value to liftoff')
    @allure.description('Verify the pptype value of flatcpm for vast liftoff rtb connection'
                        'Verify existing  imp[].ext.fcv field in bid request for vast liftoff rtb connection')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_liftoff_rtb_3(self, pub_app_id, placement, rtb):
        """
              flat_cpm_setting_in_placement=
              {
                  "is_flat_cpm_enable": True,
                  "default_flat_cpm": 0.4
              }
              """
        if env == 'ci':
            rtb = rtb.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['ext']['pptype'], equal_to(1))
        assert_keys_exist(bid_request['imp'][0]['ext'], 'fcv')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.179.0')
    @allure.story('PBJ-3340 Pass the following signals to LiftOff for an experiment '
                  'PBJ-3434 Pass flatCPM value to liftoff')
    @allure.description('Verify the pptype value of flatcpm for vast liftoff rtb connection'
                        'Verify existing  imp[].ext.fcv field in bid request for vast liftoff rtb connection')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['Emily_flat_cpm'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_liftoff_rtb_4(self, pub_app_id, placement, rtb):
        """
              flat_cpm_setting_in_placement=
              {
                  "is_flat_cpm_enable": True,
                  "default_flat_cpm": 0.0004
              }
              """
        if env == 'ci':
            rtb = rtb.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['ext']['pptype'], equal_to(1))
        assert_keys_exist(bid_request['imp'][0]['ext'], 'fcv')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.179.0')
    @allure.story('PBJ-3340 Pass the following signals to LiftOff for an experiment '
                  'PBJ-3434 Pass flatCPM value to liftoff')
    @allure.description('Verify the pptype value of flatcpm for mraid liftoff rtb connection'
                        'Verify existing  imp[].ext.fcv field in bid request for mraid liftoff connection')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['BANNER-TEST-02'])
    def test_liftoff_rtb_4(self, pub_app_id, placement):
        """
         flat_cpm_setting_in_placement=
         {
             "is_flat_cpm_enable": True,
             "default_flat_cpm": 0.4
         }
        """
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid_liftoff.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(),
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['ext']['pptype'], equal_to(1))
        assert_keys_exist(bid_request['imp'][0]['ext'], 'fcv')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.179.0')
    @allure.story('PBJ-3340 Pass the following signals to LiftOff for an experiment ')
    @allure.description('Verify the pptype value of revshare for vast liftoff rtb connection')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['AREYOUS82690'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_liftoff_rtb_5(self, pub_app_id, placement, rtb):
        if env == 'ci':
            rtb = rtb.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['ext']['pptype'], equal_to(2))

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.179.0')
    @allure.story('PBJ-3340 Pass the following signals to LiftOff for an experiment ')
    @allure.description('Verify the pptype value of revshare for mraid liftoff rtb connection')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [test_banner_placement])
    def test_liftoff_rtb_6(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid_liftoff.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid_liftoff.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(),
                                            banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_that(bid_request['imp'][0]['ext']['pptype'], equal_to(2))

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.179.0', 'test_mode')
    @allure.story('PBJ-3340 Pass the following signals to LiftOff for an experiment '
                  'PBJ-3434 Pass flatCPM value to liftoff')
    @allure.description('Verify that there should be not pptype via rtb with no liftoff extension type setting'
                        'Verify that no imp[].ext.fcv field from bid request with no liftoff extension type setting')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_liftoff_rtb_7(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_banner_xapi.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_banner_xapi.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'pptype')
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'fcv')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.179.0', 'test_mode')
    @allure.story('PBJ-3340 Pass the following signals to LiftOff for an experiment '
                  'PBJ-3434 Pass flatCPM value to liftoff')
    @allure.description('Verify that there should be not pptype via rtb with no supported extension type setting'
                        'Verify that no imp[].ext.fcv field from bid request with no liftoff extension type setting')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_liftoff_rtb_8(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'pptype')
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'fcv')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.179.0', 'test_mode')
    @allure.story('PBJ-3340 Pass the following signals to LiftOff for an experiment '
                  'PBJ-3434 Pass flatCPM value to liftoff')
    @allure.description('Verify that there should be not pptype via rtb with null supported extension type setting'
                        'Verify that no imp[].ext.fcv field from bid request with no liftoff extension type setting')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_liftoff_rtb_9(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_1.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_non_test_mode_kraken_rtb_ids_vast_1.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'pptype')
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'fcv')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the value of fcv is the same as erpmtarget for vast liftoff rtb connection')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_liftoff_rtb_fcv_value(self, pub_app_id, placement, rtb):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }

            country reserve floor = 1
        """
        if env == 'ci':
            rtb = rtb.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        serving_cost = 0.05
        flat_cpm = 2.0
        erpm_target = flat_cpm / (1 - serving_cost)
        assert_that(bid_request['imp'][0]['ext']['fcv'], equal_to(erpm_target))

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the value of fcv is the exp floor value for vast liftoff rtb connection')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM5092901'])
    @pytest.mark.parametrize('factor', [1])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_liftoff_rtb_exp_fcv_value(self, pub_app_id, placement, factor, rtb):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }

            country reserve floor = 1
        """
        if env == 'ci':
            rtb = rtb.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)

        serving_cost = 0.05
        flat_cpm = 2.0
        reserved_bid_floor = 1
        erpm_target = flat_cpm / (1 - serving_cost)

        # if flat_cpm * factor > reserved_bid_floor:
        #     exp_ext_floor = flat_cpm * factor
        # else:
        #     exp_ext_floor = reserved_bid_floor
        #
        # if exp_ext_floor < erpm_target:
        #     fcv = exp_ext_floor
        # else:
        #     fcv = erpm_target

        assert_that(bid_request['imp'][0]['ext']['fcv'], equal_to(erpm_target))

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the value of fcv is the erpm target value for vast liftoff rtb connection')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_exp_test_placement_in_config])
    @pytest.mark.parametrize('flat_cpm', [1.8])
    @pytest.mark.parametrize('factor', [1.5])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_liftoff_rtb_trarget_fcv_value(self, pub_app_id, placement, flat_cpm, factor, rtb):
        '''
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2
            }
        '''
        if env == 'ci':
            rtb = rtb.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = rtb.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        serving_cost = 0.05
        flat_cpm = 2
        reserved_bid_floor = 1
        erpm_target = flat_cpm / (1 - serving_cost)

        # if flat_cpm * factor > reserved_bid_floor:
        #     exp_ext_floor = flat_cpm * factor
        # else:
        #     exp_ext_floor = reserved_bid_floor
        #
        # if exp_ext_floor < erpm_target:
        #     fcv = exp_ext_floor
        # else:
        #     fcv = erpm_target


        assert_that(bid_request['imp'][0]['ext']['fcv'], equal_to(erpm_target))

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the idsp will win when bid price of idsp is the most high')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_margin_experiment_3_bidders_meister_win01(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:5.0,ext2:3.0,ext1:4.0'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that('test-ads' in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the liftoff will win when bid price of liftoff is the most high')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_margin_experiment_3_bidders_liftoff_win(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:5.0,ext2:6.0,ext1:4.0'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb, override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb.split(',')[1] in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the edsp will win when bid price of external rtb is the most high')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_margin_experiment_3_bidders_ext_win_00(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:5.0,ext2:3.0,ext1:7.0'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb.split(',')[2] in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify edsp will win when bid price of external rtb is more high and idsp no bid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_margin_experiment_3_bidders_ext_win_01(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:0.5,ext2:3.0,ext1:7.0'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb.split(',')[2] in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the meister will win when bid price of external rtb is more high and idsp no bid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_margin_experiment_3_bidders_ext_win_02(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:0.5,ext2:3.0,ext1:7.0'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb.split(',')[2] in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the liftoff will win when bid price of lift off is more high and edsp no bid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_margin_experiment_3_bidders_Liftoff_win_01(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:5.0,ext2:6.0,ext1:2.5'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb.split(',')[1] in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the liftoff will win when bid price of idsp is more high and edsp no bid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_margin_experiment_3_bidders_idsp_win_01(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:5.0,ext2:4.0,ext1:2.5'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that('test-ads' in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the idsp will win when bid price of idsp larger than bidfloor and edsp no bid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_margin_experiment_3_bidders_idsp_win_02(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:1.1,ext2:2.2,ext1:2.5'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that('test-ads' in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the idsp will win when bid price of idsp larger than bidfloor and edsp no bid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    def test_margin_experiment_3_bidders_idsp_win_03(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:2.2,ext2:2.3,ext1:2.5'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that('test-ads' in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the idsp will win when bid price of lift larger than edsp\'s bidfloor and edsp no bid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50929'])
    def test_margin_experiment_3_bidders_liftoff_win_02(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:1,ext2:2.7,ext1:2.5'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb.split(',')[1] in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the liftoff will win when only lift off bid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50929'])
    def test_margin_experiment_3_bidders_liftoff_win_03(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:0.5,ext2:2.2,ext1:2.5'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb.split(',')[1] in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the no winner when all rtb price less than bidfloor')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50929'])
    def test_margin_experiment_3_bidders_no_winer(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:0.5,ext2:2.0,ext1:2.5'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        assert_keys_exist(response_payload['ads'][0]['ad_markup'], 'sleep')

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify the lift off win  when edsp price less than bid floor and idsp no bid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50929'])
    def test_margin_experiment_3_bidders_no_winer(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        over_ride_price = 'int1:0.5,ext2:2.2,ext1:2.5'
        rtb = mixed_participate_rtbids
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb.split(',')[1] in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify only lift off attend auction')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50929'])
    def test_margin_experiment_only_lift_off_auction(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        rtb = liftoff_rtbids_bid
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=cn_ip, rtb_selector=rtb))
        response_payload = r.json()

        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb.split(',')[0] in campaign)

    @allure.feature('Liftoff rtb')
    @allure.tag('normal', 'v1.186.0')
    @allure.story('PBJ-3471 Change bid floor on LiftOff to the same bidfloor as Vungle')
    @allure.description('Verify only lift off attend auction and bid_price >=fcv but less than bidfloor')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50929'])
    def test_margin_experiment_only_lift_off_auction_01(self, pub_app_id, placement):
        """
            "AU": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 0.58,
                "flat_cpm": 2.0
            }
         """
        rtb = liftoff_rtbids_bid.split(',')[0]
        overide_bid_price = "ext2:2.2"
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=cn_ip, rtb_selector=rtb,
                                          override_bid_price=overide_bid_price))
        response_payload = r.json()

        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb.split(',')[0] in campaign)

    @allure.feature('eDSP price')
    @allure.tag('normal' , 'v1.245.0')
    @allure.story('PBJ-4753 Expand eDSP bid response validation from auction winner to top 3 eDSP bids')
    @allure.description('Verify the 1st highest bid will win if the 2 auction rtbs both are valid.')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_expand_bid_response_for_edsp_01(self, pub_app_id, placement):
        """
           rtb1:105
           rtb2:103
         """
        rtb_ids = '6177d4ca2c6975035fee7568,6363d7e41fbec347625200fc'
        over_ride_price = 'ext1:105,ext2:103'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb_ids,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        # verified that rtb2 will receive loss notification
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb_ids.split(',')[0] in campaign)

    @allure.feature('eDSP price')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4753 Expand eDSP bid response validation from auction winner to top 3 eDSP bids')
    @allure.description('Verify the 2nd highest bid will win if the 1st rtb is invalid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_expand_bid_response_for_edsp_02(self, pub_app_id, placement):
        """
           rtb1:105 (invalid)
           rtb2:103
         """
        rtb_ids = '636b5acaed3faf1dd779391f,6363d7e41fbec347625200fc'
        over_ride_price = 'ext5:105,ext2:103'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb_ids,
                                          override_bid_price=over_ride_price))
        response_payload = r.json()
        # verified that rtb1 will receive loss notification loss reason 204, rtb2 will win the auction
        campaign = response_payload['ads'][0]['ad_markup']['campaign']
        assert_that(rtb_ids.split(',')[1] in campaign)


    @allure.feature('eDSP price')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4753 Expand eDSP bid response validation from auction winner to top 3 eDSP bids')
    @allure.description('Verify the 2 bid\'s  vast are both invalid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_expand_bid_response_for_edsp_03(self, pub_app_id, placement):
        """
           rtb1:158 (invalid)
           rtb2:98 (invalid)
         """
        rtb_ids = '636b5acaed3faf1dd779391f,636b5c10ed3faf1dd7793923'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb_ids))
        response_payload = r.json()
        # verified that rtb1 will receive the loss notification, loss reason=204
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['info'], equal_to('invalid VAST'))


    @allure.feature('eDSP price')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4753 Expand eDSP bid response validation from auction winner to top 3 eDSP bids')
    @allure.description('Verify the 3rd bid is valid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_expand_bid_response_for_edsp_04(self, pub_app_id, placement):
        """
           rtb1:105 (invalid)
           rtb2:103 (invalid)
           rtb3:98 (valid)
         """
        rtb_ids = '636b5acaed3faf1dd779391f,636b5c10ed3faf1dd7793923,60a2773fb3bbef2c0884d8bb'
        over_ride_bid_price = 'ext5:105,ext6:103,ext1:98'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb_ids,
                                          override_bid_price=over_ride_bid_price))
        response_payload = r.json()
        # verified that rtb1. rtb3 will receive the loss notification, rtb1 loss reason:204, rtb3 loss reason:102
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')
        assert_that(ad_markup['sleep'], 50)
        assert_that(ad_markup['info'], equal_to('invalid VAST'))

    @allure.feature('eDSP price')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4753 Expand eDSP bid response validation from auction winner to top 3 eDSP bids')
    @allure.description('Verify the 3rd bid is valid')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_expand_bid_response_for_edsp_05(self, pub_app_id, placement):
        """
           rtb1:105 (invalid)
           rtb2:98 (invalid)
           rtb3:103 (valid)
         """
        rtb_ids = '636b5acaed3faf1dd779391f,636b5c10ed3faf1dd7793923,60a2773fb3bbef2c0884d8bb'
        over_ride_bid_price = 'ext5:105,ext6:98,ext1:103'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb_ids,
                                          override_bid_price=over_ride_bid_price))
        response_payload = r.json()
        # verified that rtb1. rtb2 will receive the loss notification, rtb1 loss reason:204, rtb2 loss reason:102
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_not_exist(ad_markup, 'sleep')



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
        assert_that(bid_request['imp'][0]['ext']['rp']['zone_id'], equal_to('2262356'))

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
        assert_that(bid_request['imp'][0]['ext']['rp']['zone_id'], equal_to('2262356'))

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
        assert_that(bid_request['imp'][0]['ext']['rp']['zone_id'], equal_to('2262356'))

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
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'rp')

    @allure.feature('inmobi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-3252 RTB :: Support bidrequest.imp.ext.placementid')
    @allure.description('Verify the placementid of Vungle_InterstitialVideo_iOS for InMobi eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    def test_inmobi_bid_request_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_inmobi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['ext']['placementid'], '1645632767278')

    @allure.feature('inmobi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-3252 RTB :: Support bidrequest.imp.ext.placementid')
    @allure.description('Verify the placementid of Vungle_Video_Rewarded_iOS for InMobi eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_inmobi_bid_request_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_inmobi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['ext']['placementid'], '1642239775447')

    @allure.feature('inmobi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-3252 RTB :: Support bidrequest.imp.ext.placementid')
    @allure.description('Verify the placementid of Vungle_Banner_iOS for InMobi eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_inmobi_bid_request_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_inmobi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['ext']['placementid'], '1642988054140')

    @allure.feature('inmobi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-3252 RTB :: Support bidrequest.imp.ext.placementid')
    @allure.description('Verify the placementid of Vungle_InterstitialVideo_Android for InMobi eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    def test_inmobi_bid_request_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_inmobi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['ext']['placementid'], '1646081465058')

    @allure.feature('inmobi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-3252 RTB :: Support bidrequest.imp.ext.placementid')
    @allure.description('Verify the placementid of Vungle_Android_Rewarded_Video for InMobi eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement_rewarded])
    def test_inmobi_bid_request_5(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_inmobi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['ext']['placementid'], '1645656656109')

    @allure.feature('inmobi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-3252 RTB :: Support bidrequest.imp.ext.placementid')
    @allure.description('Verify the placementid of Vungle_Banner_Android for InMobi eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_banner_placement])
    def test_inmobi_bid_request_6(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_inmobi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['ext']['placementid'], '1644379127118')

    @allure.feature('inmobi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-4921 Fix inMobi bidrequest for MREC')
    @allure.description('Verify the placementid of Vungle_Mrec_android for InMobi eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_preCache_mrec_test_placement])
    def test_inmobi_bid_request_7(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_inmobi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['ext']['placementid'], '1644379127118')

    @allure.feature('inmobi suuport')
    @allure.tag('normal')
    @allure.story('PBJ-4921 Fix inMobi bidrequest for MREC')
    @allure.description('Verify the placementid of Vungle_Mrec_ios for InMobi eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_image_mrec_placement])
    def test_inmobi_bid_request_8(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_inmobi))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_valid_schema(response_payload, response_schema.ads_v5)

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_that(bid_request['imp'][0]['ext']['placementid'], '1642988054140')



    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_adv_pref_skfsc_default.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_adv_pref_skfsc_default.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_1(self, pub_app_id, placement, rtb):
        """
            app level: FSC=adv_pref, SK_FSC=default
            placement level: FSC=inherit
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('default'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('adv_pref'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_fsc_on_skfsc_default.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_fsc_on_skfsc_default.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_2(self, pub_app_id, placement, rtb):
        """
            app level: FSC=fsc_off, SK_FSC=default
            placement level: FSC=fsc_on
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('default'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('fsc_on'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_fsc_off_skfsc_default.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_fsc_off_skfsc_default.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_3(self, pub_app_id, placement, rtb):
        """
            app level: FSC=fsc_off, SK_FSC=default
            placement level: FSC=inherit
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('default'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('fsc_off'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_adv_pref_skfsc_product_view.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_adv_pref_skfsc_product_view.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_4(self, pub_app_id, placement, rtb):
        """
            app level: FSC=adv_pref, SK_FSC=product_view
            placement level: FSC=inherit
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('product_view'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('adv_pref'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_fsc_on_skfsc_product_view.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_fsc_on_skfsc_product_view.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_5(self, pub_app_id, placement, rtb):
        """
            app level: FSC=adv_pref, SK_FSC=product_view
            placement level: FSC=fsc_on
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('product_view'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('fsc_on'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_fsc_off_skfsc_product_view.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_fsc_off_skfsc_product_view.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_6(self, pub_app_id, placement, rtb):
        """
            app level: FSC=adv_pref, SK_FSC=product_view
            placement level: FSC=fsc_off
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('product_view'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('fsc_off'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_adv_pref_skfsc_overlay_view.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_adv_pref_skfsc_overlay_view.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_7(self, pub_app_id, placement, rtb):
        """
            app level: FSC=adv_pref, SK_FSC=overlay_view
            placement level: FSC=inherit
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('overlay_view'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('adv_pref'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_fsc_on_skfsc_overlay_view.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_fsc_on_skfsc_overlay_view.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_8(self, pub_app_id, placement, rtb):
        """
            app level: FSC=adv_pref, SK_FSC=overlay_view
            placement level: FSC=fsc_on
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('overlay_view'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('fsc_on'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_fsc_off_skfsc_overlay_view.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_fsc_off_skfsc_overlay_view.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_9(self, pub_app_id, placement, rtb):
        """
            app level: FSC=adv_pref, SK_FSC=overlay_view
            placement level: FSC=fsc_off
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('overlay_view'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('fsc_off'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_adv_pref_skfsc_off.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_adv_pref_skfsc_off.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_10(self, pub_app_id, placement, rtb):
        """
            app level: FSC=adv_pref, SK_FSC=off
            placement level: FSC=inherit
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('off'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('adv_pref'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_fsc_on_skfsc_off.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_fsc_on_skfsc_off.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_11(self, pub_app_id, placement, rtb):
        """
            app level: FSC=adv_pref, SK_FSC=off
            placement level: FSC=fsc_on
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('off'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('fsc_on'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens for the SKO related singles')
    @pytest.mark.parametrize('pub_app_id', [test_fsc_fsc_off_skfsc_off.split('|')[0]])
    @pytest.mark.parametrize('placement', [test_fsc_fsc_off_skfsc_off.split('|')[1]])
    @pytest.mark.parametrize('rtb', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff,
                                     ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us])
    def test_sko_liftoff_12(self, pub_app_id, placement, rtb):
        """
            app level: FSC=adv_pref, SK_FSC=off
            placement level: FSC=fsc_off
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['sk_experience'], equal_to('off'))
        assert_that(bid_request['imp'][0]['ext']['pub_experience']['video_click_area'], equal_to('fsc_off'))

    @allure.feature('Liftoff support')
    @allure.tag('normal', 'v1.207.0')
    @allure.story('PBJ-3965 Pass \"is SKO Auto Allowed\" and other SKO related signals to Liftoff in the Bid Request')
    @allure.description('Verify the pub experiment tokens will not be existing for the non-Liftoff DSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_sko_liftoff_13(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_keys_not_exist(bid_request['imp'][0]['ext'], 'pub_experience')


    @allure.feature('BidSwitch')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-4864 BidSwitch Expired Impression Fix')
    @allure.description('Verify imp ext vungle details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('rtb_id', [ext_non_test_mode_kraken_rtb_ids_bidSwitch])
    def test_bidSwitch_imp_exp(self, pub_app_id, placement_id, rtb_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id(digital=36))
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger',
                                                                        rtb_selector=ext_non_test_mode_kraken_rtb_ids_bidSwitch))

        response_payload = r.json()

        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request_imp = bid_request['imp']
        assert_keys_exist(bid_request_imp[0], 'exp')
        assert_that(bid_request_imp[0]['exp'], equal_to(3600))



    @allure.feature('Accelarate')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-5202 Add floor info to Acc bid Request')
    @allure.description('Verify that bidrequest.imp[].ext.publisher_flat_cpm pass to dsp for rev_share mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_pass_cpm_floor_to_dsp_flatMode(self, pub_app_id, placement):
        """
            "is_flat_cpm_enable": True,
            "default_flat_cpm": 0.4
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=liftoff_rtbids_liftoff_dup,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, liftoff_rtbids_liftoff_dup)
        imp_ext = bid_request['imp'][0]['ext']
        assert_that(imp_ext['pptype'], equal_to(1))
        assert_keys_exist(imp_ext, 'publisher_flat_cpm')
        assert_that(imp_ext['publisher_flat_cpm'], equal_to(0.4))



    @allure.feature('Accelarate')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-5202 Add floor info to Acc bid Request')
    @allure.description('Verify that bidrequest.imp[].ext.publisher_flat_cpm pass to dsp for rev_share mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ["AREYOUS82690"])
    def test_pass_cpm_floor_to_dsp_revShare_Mode(self, pub_app_id, placement):
        """
            "default_cpm_floor": 1
            "default_rev_share: 0.6
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=liftoff_rtbids_liftoff_dup,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, liftoff_rtbids_liftoff_dup)
        imp_ext = bid_request['imp'][0]['ext']
        assert_that(imp_ext['pptype'], equal_to(2))
        assert_keys_exist(imp_ext, 'publisher_cpm_floor')
        assert_keys_exist(imp_ext, 'rev_share')
        assert_that(imp_ext['publisher_cpm_floor'], equal_to(1))
        assert_that(imp_ext['rev_share'], equal_to(0.6))


    @allure.feature('Accelarate')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-5202 Add floor info to Acc bid Request')
    @allure.description('Verify that does not pass bidrequest.imp[].ext.publisher_flat_cpm pass to others')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_not_pass_field_for_not_acc(self, pub_app_id, placement):
        """
            "is_flat_cpm_enable": True,
            "default_flat_cpm": 0.4
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
        imp_ext = bid_request['imp'][0]['ext']
        assert_keys_not_exist(imp_ext, 'publisher_flat_cpm')

    @allure.feature('Accelarate')
    @allure.tag('normal', 'v1.260.0')
    @allure.story('PBJ-5369 Revenue_share is 0 in some cases when payout time is REVENUE_SHARE')
    @allure.description('Verify that RevShare value pass to A should be correct when no cpm floor.')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ["AREYOUS826901"])
    def test_revshare_edge_case(self, pub_app_id, placement):
        """
            "default_cpm_floor": null
            "default_rev_share: 0.6
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=liftoff_rtbids_liftoff_dup,
                                          debug='jaeger', sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, liftoff_rtbids_liftoff_dup)
        imp_ext = bid_request['imp'][0]['ext']
        assert_that(imp_ext['pptype'], equal_to(2))
        assert_keys_exist(imp_ext, 'rev_share')
        assert_that(imp_ext['rev_share'], equal_to(0.6))



    @allure.feature('erpmtarget')
    @allure.tag('normal')
    @allure.story('PBJ-5211 set $0.01 as minimum floor for Direct DSP')
    @allure.description('Verify imp.ext.vungle.erpmtarget=0.01 for hb idsp request')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_erpmtarget_idsp_hb(self, pub_app_id, placement, rtb):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        vungle = bid_request['imp'][0]['ext']['vungle']
        assert_that(vungle['erpmtarget'], equal_to(0.01))



    @allure.feature('erpmtarget')
    @allure.tag('normal')
    @allure.story('PBJ-5211 set $0.01 as minimum floor for Direct DSP')
    @allure.description('Verify imp.ext.vungle.erpmtarget=0.01 for rev_share mode idsp request')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_erpmtarget_idsp_rev_share(self, pub_app_id, placement, rtb):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        vungle = bid_request['imp'][0]['ext']['vungle']
        assert_that(vungle['erpmtarget'], equal_to(0.01))




    @allure.feature('erpmtarget')
    @allure.tag('normal')
    @allure.story('PBJ-5211 set $0.01 as minimum floor for Direct DSP')
    @allure.description('Verify imp.ext.vungle.erpmtarget!=0.01 for non hb idsp request')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    @pytest.mark.parametrize('rtb', [meister_rtb_ids])
    def test_erpmtarget_idsp_non_hb(self, pub_app_id, placement, rtb):

        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip, rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload, rtb)
        vungle = bid_request['imp'][0]['ext']['vungle']
        assert_that(vungle['erpmtarget'], not equal_to(0.01))

