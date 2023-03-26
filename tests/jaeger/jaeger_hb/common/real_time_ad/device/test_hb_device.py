import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import post_hbp_request, request_hb_win_notification, request_hbp, request_hb_loss_notification, \
    request_hbp_with_real_time_token, get_bid_request_obj_from_hbp_explain, request_realtime_win_notification
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema
import time


@allure.epic('Real-time device ')
class TestHBPRealtimeDevice(object):

    @allure.feature('real-time device')
    @allure.tag('normal')
    @allure.story('PBJ-3793 [Jaeger HB realtime - Add normalize device id and hash logic')
    @allure.description('Verify device id is hashed when GDPR in token is opted out for eu country ip')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('gdpr_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_real_time_device_id_01(self, pub_app_id, placement, sdk_v, partner, gdpr_status):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip, is_hb=partner, rtb=test_mode_kraken_rtb_ids_1,
                                                gdpr_status=gdpr_status)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                if gdpr_status == 'opted_out':
                    assert_that(bid_request['device']['ext']['vungle']['id'], not equal_to(test_mode_device_id))
                    assert_that(bid_request['device']['ext']['vungle']['id_source'], equal_to_ignoring_case('GDPR'))
                else:
                    assert_that(bid_request['device']['ext']['vungle']['id'], equal_to(test_mode_device_id))
                    assert_that(bid_request['device']['ext']['vungle']['id_source'], equal_to('IFA'))


    @allure.feature('real-time device')
    @allure.tag('normal')
    @allure.story('PBJ-3793 [Jaeger HB realtime - Add normalize device id and hash logic')
    @allure.description('Verify device id is hashed when GDPR in token is opted out for eu country ip')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('gdpr_status', [None, 'unknown', 'opted_out_by_timeout'])
    @pytest.mark.parametrize('ip', [eu_country_ip, non_eu_country_ip])
    def test_real_time_gdpr_legitimate_interest_true(self, pub_app_id, placement, sdk_v, partner, gdpr_status, ip):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, ip=ip, is_hb=partner, rtb=test_mode_kraken_rtb_ids_1,
                                                gdpr_status=gdpr_status)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
            assert_that(bid_request['device']['ext']['vungle']['id'], equal_to(test_mode_device_id))
            assert_that(bid_request['device']['ext']['vungle']['id_source'], equal_to('IFA'))


    @allure.feature('real-time device')
    @allure.tag('normal')
    @allure.story('PBJ-3793 [Jaeger HB realtime - Add normalize device id and hash logic')
    @allure.description('Verify device id is ifa when GDPR in token is opted out for non-eu country ip')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('gdpr_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_real_time_device_id_02(self, pub_app_id, placement, sdk_v, partner, gdpr_status):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=non_eu_country_ip, is_hb=partner,
                                                rtb=test_mode_kraken_rtb_ids_1,
                                                gdpr_status=gdpr_status)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
            assert_that(bid_request['device']['ext']['vungle']['id'], equal_to(test_mode_device_id))
            assert_that(bid_request['device']['ext']['vungle']['id_source'], equal_to('IFA'))



    @allure.feature('real-time device')
    @allure.tag('normal')
    @allure.story('PBJ-3793 [Jaeger HB realtime - Add normalize device id and hash logic')
    @allure.description('Verify device id is hashed when GDPR in token is opted out for eu country ip')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('gdpr_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_real_time_device_id_03(self, pub_app_id, placement, sdk_v, partner, gdpr_status):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip, is_hb=partner,
                                                rtb=test_mode_kraken_rtb_ids_1,
                                                gdpr_status=gdpr_status)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                if gdpr_status == 'opted_out':
                    assert_that(bid_request['device']['ext']['vungle']['id'], not equal_to(test_mode_device_id))
                    assert_that(bid_request['device']['ext']['vungle']['id_source'], equal_to_ignoring_case('GDPR'))
                else:
                    assert_that(bid_request['device']['ext']['vungle']['id'], equal_to(test_mode_device_id))
                    assert_that(bid_request['device']['ext']['vungle']['id_source'], equal_to('IFA'))
                assert_that(bid_request['ext']['vungle']['src'], equal_to('hb'))



    @allure.feature('real-time device')
    @allure.tag('normal')
    @allure.story('PBJ-3793 [Jaeger HB realtime - Add normalize device id and hash logic')
    @allure.description('Verify device id in the bid request when request with null device id')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('gdpr_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_real_time_device_id_04(self, pub_app_id, placement, sdk_v, partner, gdpr_status):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id='', sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=non_eu_country_ip, is_hb=partner,
                                                rtb=meister_rtb_ids,
                                                gdpr_status=gdpr_status)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, meister_rtb_ids)
                assert_that(bid_request['device']['ext']['vungle']['id'], not equal_to(test_mode_device_id))
                assert_that(bid_request['device']['ext']['vungle']['id_source'], equal_to('Vungle_FP'))





    @allure.feature('real-time device')
    @allure.tag('normal')
    @allure.story('PBJ-3793 [Jaeger HB realtime - Add normalize device id and hash logic')
    @allure.description('Verify coppa exist when app and placement both true')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('coppa', [None, True, False])
    def test_real_time_device_id_coppa_ios_01(self, pub_app_id, placement, sdk_v, partner, coppa):
        """

          App level setting:
          "isCoppaCompliant": true

          Placement level setting:
          "is_coppa": true

        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip, is_hb=partner,
                                                rtb=test_mode_kraken_rtb_ids_1, platform='ios', coppa=coppa
                                                )

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
            if coppa is False:
                assert_keys_not_exist(bid_request['regs'], 'coppa')
            else:
                assert_that(bid_request['regs']['coppa'],  equal_to(1))


    @allure.feature('real-time device')
    @allure.tag('normal')
    @allure.story('PBJ-3793 [Jaeger HB realtime - Add normalize device id and hash logic')
    @allure.description('Verify coppa field with placement level false but app level true')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_mrec_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('coppa', [None, True, False])
    def test_real_time_device_id_coppa_ios_02(self, pub_app_id, placement, sdk_v, partner, coppa):
        """
            App level setting:
            "isCoppaCompliant": true

            Placement level setting:
            "is_coppa": false

        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip, is_hb=partner,
                                                rtb=meister_rtb_ids, platform='ios', coppa=coppa
                                                )

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload, meister_rtb_ids)
            if coppa is True:
                assert_that(bid_request['regs']['coppa'], equal_to(1))
            else:
                assert_keys_not_exist(bid_request['regs'], 'coppa')



    @allure.feature('real-time device')
    @allure.tag('normal')
    @allure.story('PBJ-3793 [Jaeger HB realtime - Add normalize device id and hash logic')
    @allure.description('Verify device id is zero out when coppa is exist')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_mrec_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('coppa', [None, True, False])
    def test_real_time_device_id_coppa_01(self, pub_app_id, placement, sdk_v, partner, coppa):
        """

          App level setting:
          "isCoppaCompliant": false

        """
        test_id = gen_device_id()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, ip=cn_ip,
                                                explain=True,  is_hb=partner, platform='android',
                                                rtb=meister_rtb_ids, coppa=coppa, config_extension=test_config_extension,
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload, meister_rtb_ids)
            if coppa:
                assert_that(bid_request['device']['ext']['vungle']['id'], not equal_to(test_id))
                assert_that(bid_request['device']['ext']['vungle']['id_source'],  equal_to("Vungle_FP"))
            else:
                assert_that(bid_request['device']['ext']['vungle']['id'],  equal_to(test_id))
                assert_that(bid_request['device']['ext']['vungle']['id_source'], equal_to("IFA"))



    @allure.feature('real-time device')
    @allure.tag('normal')
    @allure.story('PBJ-3793 [Jaeger HB realtime - Add normalize device id and hash logic')
    @allure.description('Verify device id in bid request when request with null device id')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_mrec_test_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('coppa', [None, True, False])
    def test_real_time_device_id_coppa_02(self, pub_app_id, placement, sdk_v, partner, coppa):
        """

          App level setting:
          "isCoppaCompliant": false

        """
        test_id = ''
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, ip=cn_ip,
                                                explain=True,  is_hb=partner, platform='android',
                                                rtb=meister_rtb_ids, coppa=coppa, config_extension=test_config_extension,
                                                )
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_request = get_bid_request_obj_from_hbp_explain(response_payload, meister_rtb_ids)
            assert_that(bid_request['device']['ext']['vungle']['id'], not equal_to(test_id))
            assert_that(bid_request['device']['ext']['vungle']['id_source'],  equal_to("Vungle_FP"))


    @allure.feature('real-time device')
    @allure.tag('normal')
    @allure.story('PBJ-3712 RTB :: Change user.ext.consent to string')
    @allure.description('Verify user.ext.consent support string')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('gdpr_status', [None, 'opted_in', 'opted_out', 'unknown', 'opted_out_by_timeout'])
    def test_real_time_consent_support_string(self, pub_app_id, placement, sdk_v, partner, gdpr_status):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip, is_hb=partner,
                                                rtb=ext_test_mode_kraken_rtb_consentString,
                                                gdpr_status=gdpr_status)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_test_mode_kraken_rtb_consentString)

                assert_that(bid_request['user']['ext']['consent'], equal_to("1"))




    @allure.feature('realTime IP')
    @allure.tag('smoke')
    @allure.story('PBJ-4408 Realtime - Add IP to config extension in Bastion')
    @allure.description('Verify jaeger use ip in config extension to look for GEO')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_real_ip_from_token_01(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_ip)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)

                device = bid_request['device']
                assert_that(device['geo']['country'], equal_to('FRA'))
                assert_that(device['ip'], equal_to(fr_ip))



    @allure.feature('realTime IP')
    @allure.tag('smoke')
    @allure.story('PBJ-4408 Realtime - Add IP to config extension in Bastion')
    @allure.description('Verify jaeger use ip in config extension to look for GEO for iDSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_real_ip_from_token_02(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=non_test_mode_kraken_rtb_ids,
                                                config_extension=config_extension_ip)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, non_test_mode_kraken_rtb_ids)

                device = bid_request['device']
                assert_that(device['geo']['country'], equal_to('FRA'))
                assert_that(device['ip'], equal_to(fr_ip))



    @allure.feature('realTime IP')
    @allure.tag('smoke')
    @allure.story('PBJ-4408 Realtime - Add IP to config extension in Bastion')
    @allure.description('Verify jaeger use ip in config extension to look for GEO for eDSP')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_hybrid_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_real_ip_from_token_03(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True, coppa=True, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_ip, ip=eu_country_ip)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)

                device = bid_request['device']
                assert_that(device['geo']['country'], equal_to('FRA'))
                assert_that(device['ip'], equal_to(fr_ip))




