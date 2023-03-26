import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('scrat - ri')
class TestRIBasic(object):

    @allure.feature('ri v5')
    @allure.tag('basic', 'smoke')
    @allure.story('ri v5')
    @allure.description('Verify the ri v5 endpoint work fine')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_ri_v5_basic(self, pub_app_id):
        test_ifa = gen_device_id()
        req = request_payload.ri_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(ri_v5_endpoint_qa, json=req, headers=platform_headers(debug='scrat'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))
        assert_that(response_payload['ext']['debug']['device']['DeviceID'], equal_to(test_ifa))
        assert_that(response_payload['ext']['debug']['device']['DeviceIDSource'], equal_to('IFA'))

    # -------------------------below cases are for disable_ad_id_if_coppa=False-----------------------------------------
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # def test_zero_out_gaid_for_android_01_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     test_id = ''
    #     ifa = ''
    #     req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
    #                                         android_id=test_id, ifa=ifa)
    #     r = post(ri_v5_endpoint_qa, json=req, headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], is_not(ifa))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # def test_zero_out_gaid_for_android_02_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     test_id = ''
    #     ifa = ''
    #     req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                         android_id=test_id, ifa=ifa)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], is_not(ifa))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # def test_zero_out_gaid_for_android_03_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
    #                                         android_id=test_id, ifa=ifa)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], equal_to(ifa))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    # def test_zero_out_gaid_for_android_04_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                         android_id=test_id, ifa=ifa)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], equal_to(ifa))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_07_false(self, pub_app_id, sdk_v):
    #     """
    #
    #    App level setting:
    #    "isCoppaCompliant": false
    #    """
    #     test_id = ''
    #     req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement, coppa=False,
    #                                         android_id=test_id, ifa='')
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], is_not(''))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_08_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                         android_id='', ifa=device_id, coppa=False)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], is_not(''))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify non zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_09_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     ifa = test_device_id = gen_device_id()
    #     req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
    #                                         android_id=test_device_id, ifa=ifa, coppa=False)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], equal_to(ifa))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_10_false(self, pub_app_id, sdk_v):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     ifa = test_device_id = gen_device_id()
    #     req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                         android_id=test_device_id, ifa=ifa, coppa=False)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], equal_to(ifa))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    # def test_zero_out_gaid_for_android_11_false(self, pub_app_id, sdk_v):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     ifa = test_device_id = gen_device_id()
    #     req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
    #                                         android_id=test_device_id, ifa=ifa, coppa=True)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], equal_to(ifa))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))

    # -------------------------below cases are for disable_ad_id_if_coppa=False and GDPR exists------------------------

    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    # def test_zero_out_gaid_with_gdpr_for_android_01_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     test_id = ''
    #     req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
    #                                         android_id=test_id, ifa='', gdpr=consent_status)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], is_not(''))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    # def test_zero_out_gaid_with_gdpr_for_android_02_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     test_id = ''
    #     req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                         android_id=test_id, ifa='', gdpr=consent_status)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceID'], is_not(''))
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    # def test_zero_out_gaid_with_gdpr_for_android_03_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
    #                                         android_id=test_id, ifa=ifa, gdpr=consent_status)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('GDPR'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=N/A,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    # def test_zero_out_gaid_with_gdpr_for_android_04_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
    #                                         android_id=test_id, ifa=ifa, gdpr=consent_status)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('GDPR'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_zero_out_gaid_with_gdpr_for_android_07_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #
    #    App level setting:
    #    "isCoppaCompliant": false
    #    """
    #     test_id = ''
    #     req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement, coppa=False,
    #                                         android_id=test_id, ifa="", gdpr=consent_status)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_zero_out_gaid_with_gdpr_for_android_08_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa', gdpr=consent_status,
    #                                         android_id='', ifa=device_id, coppa=False)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify non zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_zero_out_gaid_with_gdpr_for_android_09_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement, gdpr=consent_status,
    #                                         android_id=test_id, ifa=ifa, coppa=False)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('GDPR'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=F, is_coppa from SDK=F,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_zero_out_gaid_with_gdpr_for_android_10_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     Placement level setting:
    #     "is_coppa": true
    #     """
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa', gdpr=consent_status,
    #                                         android_id=test_id, ifa=ifa, coppa=False)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('GDPR'))
    #
    # @allure.feature('Extending coppa support')
    # @allure.tag('normal')
    # @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    # @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
    #                     'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('consent_status', ['opted_out'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    # def test_zero_out_gaid_with_gdpr_for_android_11_false(self, pub_app_id, sdk_v, consent_status):
    #     """
    #     App level setting:
    #     "isCoppaCompliant": false
    #     """
    #     ifa = test_id = gen_device_id()
    #     req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
    #                                         android_id=test_id, ifa=ifa, coppa=True, gdpr=consent_status)
    #     r = post(ri_v5_endpoint_qa, json=req,
    #              headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
    #     response_payload = r.json()
    #     debug = response_payload['ext']['debug']
    #     assert_that(debug['device']['DeviceIDSource'], equal_to('GDPR'))

    # -------------------------below cases are for disable_ad_id_if_coppa=True------------------------------------------

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_for_android_01_true(self, pub_app_id, sdk_v):
        """

        App level setting:
        "isCoppaCompliant": false
        """
        ifa = test_id = ''
        req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
                                            android_id=test_id, ifa=ifa, app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_for_android_02_true(self, pub_app_id, sdk_v):
        """
        Placement level setting:
        "is_coppa": true
        """

        ifa = test_id = ''
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                            android_id=test_id, ifa=ifa, app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_for_android_05_true(self, pub_app_id, sdk_v):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        ifa = test_id = gen_device_id()
        req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement, ifa=ifa,
                                            android_id=test_id, app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_for_android_06_true(self, pub_app_id, sdk_v):
        """
           Placement level setting:
           "is_coppa": true
        """
        ifa = test_id = gen_device_id()
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                            android_id=test_id, ifa=ifa, app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    def test_zero_out_gaid_for_android_07_true(self, pub_app_id, sdk_v):
        """

       App level setting:
       "isCoppaCompliant": false
       """
        ifa = test_id = ''
        req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement, coppa=False,
                                            android_id=test_id, ifa=ifa, app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    def test_zero_out_gaid_for_android_08_true(self, pub_app_id, sdk_v):
        """
        Placement level setting:
        "is_coppa": true
        """
        ifa = test_id = ''
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa', android_id=test_id, ifa=ifa,
                                            coppa=False, app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'v0.154.0')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag'
                  'PBJ-4452 Scrat - Treat 0000-0000 as empty IFA')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_for_android_12_true(self, pub_app_id, sdk_v, device_id):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
                                            ifa=device_id, android_id='', coppa=True)
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal', 'v0.154.0')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag'
                  'PBJ-4452 Scrat - Treat 0000-0000 as empty IFA')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_for_android_12_1_true(self, pub_app_id, sdk_v, device_id):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                            ifa=device_id, android_id='', coppa=True, app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    # ------- below test cases are for coppa_preference=2 (means prefer api's value) and sdk_v>=6.10.4------------------
    @allure.feature('coppa 6.11.x')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag'
                  'PBJ-3880 [Scrat][COPPA] compliance scrat behavior for coppa in 6.10.4 android and 6.11.0 for others')
    @allure.description('Verify scrat work well for coppa flag on android platform when sdk version >= 6.10.4')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_coppa_perference2_android_1(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:
        "isCoppaCompliant": false
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
        """
        ifa = test_id = gen_device_id()
        req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement, coppa=coppa,
                                            android_id=test_id, ifa=ifa)
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        if coppa:
            assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
        else:
            assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))

    @allure.feature('coppa 6.11.x')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag'
                  'PBJ-3880 [Scrat][COPPA] compliance scrat behavior for coppa in 6.10.4 android and 6.11.0 for others')
    @allure.description('Verify scrat work well for coppa flag on android platform when sdk version >= 6.10.4')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_coppa_perference2_android_2(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:
        "isCoppaCompliant": true
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
        """
        ifa = test_id = gen_device_id()
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa', coppa=coppa,
                                            android_id=test_id, ifa=ifa)
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        if coppa is False:
            assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))
        else:
            assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('coppa 6.11.x')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag'
                  'PBJ-3880 [Scrat][COPPA] compliance scrat behavior for coppa in 6.10.4 android and 6.11.0 for others')
    @allure.description('Verify scrat work well for coppa flag on android platform when sdk version >= 6.10.4')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_coppa_perference2_zero_ifa_android_2(self, pub_app_id, sdk_v, coppa, device_id):
        """
        application coppa setting:
        "isCoppaCompliant": true
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
        """
        ifa = device_id
        test_id = ''
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa', coppa=coppa,
                                            android_id=test_id, ifa=ifa)
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']

        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('coppa 6.11.x')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag'
                  'PBJ-3880 [Scrat][COPPA] compliance scrat behavior for coppa in 6.10.4 android and 6.11.0 for others')
    @allure.description('Verify scrat work well for coppa flag on ios platform when sdk version >= 6.11.0')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0 ', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_coppa_perference2_ios_1(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:
        "isCoppaCompliant": true
        case:
        coppa_preference:2; "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
        """
        ifa = gen_device_id()
        req = request_payload.ri_v5_ios(pub_app_id, common_test_placement, coppa=coppa,
                                        ifa=ifa)
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))



    # --------------------------------------below test cases are for  sdk_v< 6.10.4-------------------------------------

    @allure.feature('coppa 6.11.x')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag'
                  'PBJ-3880 [Scrat][COPPA] compliance scrat behavior for coppa in 6.10.4 android and 6.11.0 for others')
    @allure.description('Verify scrat work well for coppa flag on android platform when sdk version < 6.10.4')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_coppa_android_6103_1(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:
        "isCoppaCompliant": false
        case:
        "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):false;
        """
        ifa = test_id = gen_device_id()
        req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement, coppa=coppa,
                                            android_id=test_id, ifa=ifa)
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        if coppa:
            assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
        else:
            assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))

    @allure.feature('coppa 6.11.x')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag'
                  'PBJ-3880 [Scrat][COPPA] compliance scrat behavior for coppa in 6.10.4 android and 6.11.0 for others')
    @allure.description('Verify scrat work well for coppa flag on android platform when sdk version < 6.10.4')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_coppa_android_6103_2(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:
        "isCoppaCompliant": true
        case:
        "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
        """
        ifa = test_id = gen_device_id()
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa', coppa=coppa,
                                            android_id=test_id, ifa=ifa)
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        if coppa is False:
            assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))
        else:
            assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('coppa 6.11.x')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag'
                  'PBJ-3880 [Scrat][COPPA] compliance scrat behavior for coppa in 6.10.4 android and 6.11.0 for others')
    @allure.description('Verify scrat work well for coppa flag on ios platform when sdk version < 6.10.4')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('coppa', ["", True, False])
    def test_coppa_ios_6103_2(self, pub_app_id, sdk_v, coppa):
        """
        application coppa setting:
        "isCoppaCompliant": true
        case:
        "coppa":["android", "ios"]; is_coppa(api):% coppa; is_coppa(dashboard):true;
        """
        ifa = test_id = gen_device_id()
        req = request_payload.ri_v5_ios(pub_app_id, common_test_placement, coppa=coppa,
                                        ifa=ifa)
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('IFA'))

    # --------------------below cases are for disable_ad_id_if_coppa=True and GDPR exists-------------------------------
    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3'
                        'and GDPR exists')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_01_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
                                            android_id='', ifa=device_id, gdpr=consent_status, app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_02_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                            android_id='', ifa=device_id, gdpr=consent_status, app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_zero_out_gaid_with_gdpr_for_android_05_true(self, pub_app_id, sdk_v, consent_status):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        ifa = test_id = gen_device_id()
        req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
                                            android_id=test_id, ifa=ifa, gdpr=consent_status, app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v, src_ip=fr_ip))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('GDPR'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=N/A,'
                        'Non-Zeroed IFA/GAID from SDK=Y,dashboard is_coppa=F, is_coppa to DSP=F when SDV_v<6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.2'])
    def test_zero_out_gaid_with_gdpr_for_android_06_true(self, pub_app_id, sdk_v, consent_status):
        """
           Placement level setting:
           "is_coppa": true
        """
        ifa = test_id = gen_device_id()
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                            android_id=test_id, ifa=ifa, gdpr=consent_status,
                                            app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=T, is_coppa to DSP=F when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3', 'Vungle/6.11.0'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_07_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """

       App level setting:
       "isCoppaCompliant": false
       """
        req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement, coppa=False,
                                            android_id='', ifa=device_id, gdpr=consent_status)
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify no IFA/GAID zero out for disable_ad_id_if_coppa=T/F, is_coppa from SDK=F,'
                        'Non-Zeroed IFA/GAID from SDK=N/A,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_08_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                            android_id='', ifa=device_id, gdpr=consent_status,
                                            app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=F, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_12_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """
        App level setting:
        "isCoppaCompliant": false
        """
        req = request_payload.ri_v5_android(pub_app_id, android_common_test_placement,
                                            android_id='', ifa=device_id, coppa=True, gdpr=consent_status)
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))

    @allure.feature('Extending coppa support')
    @allure.tag('normal')
    @allure.story('PBJ-3580 [COPPA][Scrat]zero out GAID for COPPA case compliance with disable_ad_id_if_coppa flag')
    @allure.description('Verify zero out IFA/GAID for disable_ad_id_if_coppa=T, is_coppa from SDK=T,'
                        'Non-Zeroed IFA/GAID from SDK=zeroed-IFA/GAID,dashboard is_coppa=T, is_coppa to DSP=T when SDV_v>=6.10.3')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('consent_status', ['opted_out'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3'])
    @pytest.mark.parametrize('device_id', ['00000000-0000-0000-0000-000000000000', '0000-0000', '-', ''])
    def test_zero_out_gaid_with_gdpr_for_android_12_1_true(self, pub_app_id, sdk_v, consent_status, device_id):
        """
        Placement level setting:
        "is_coppa": true
        """
        req = request_payload.ri_v5_android(pub_app_id, 'DEFAULT95027_coppa',
                                            android_id='', ifa=device_id, coppa=True, gdpr=consent_status,
                                            app_id=gen_test_app_id('android'))
        r = post(ri_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='scrat', sdk_version=sdk_v))
        response_payload = r.json()
        debug = response_payload['ext']['debug']
        assert_that(debug['device']['DeviceIDSource'], equal_to('Vungle_FP'))
