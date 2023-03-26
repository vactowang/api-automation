import pytest
import allure

from utils.assertions import *
from utils.behaviors import request_s2s, get_bid_request_obj_from_jaeger_explain, get_device_info
from utils.common import *
from settings import *


@allure.epic('GDPR')
class TestCommonS2S(object):

    @allure.feature('S2S user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-3700 S2S API phase 2  Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify the gdpr flag when bid request regs.ext.gdpr=1 '
                        'for en country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('placement_id', ['DEFAULT-5045327'])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_parse_bid_request_with_GDPR_01(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, gdpr=1, ip=eu_country_ip, consent=1)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        assert_that(bid_request['user']['ext']['consent'], equal_to(1))
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))

    @allure.feature('S2S user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-3700 S2S API phase 2  Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify the gdpr flag when bid request regs.ext.gdpr=1 '
                        'for en country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('placement_id', ['DEFAULT-5045327'])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_parse_bid_request_with_GDPR_01(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, gdpr=1, ip=eu_country_ip, consent=1)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        assert_that(bid_request['user']['ext']['consent'], equal_to(1))
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))


    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3700 S2S API phase 2  Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify the gdpr flag bid request regs.ext.gdpr=0 '
                        'for en country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('placement_id', ['DEFAULT-5045327'])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_parse_bid_request_with_GDPR_02(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, gdpr=0, ip=eu_country_ip)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        assert_keys_not_exist(bid_request['user'], 'ext')
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))


    @allure.feature('S2S user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-3712 RTB :: Change user.ext.consent to string')
    @allure.description('Verify user.ext.consent support string')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('placement_id', ['DEFAULT-5045327'])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_consent_support_string_01(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=ext_non_test_mode_kraken_rtb_consentString, gdpr=1, ip=eu_country_ip, consent=1)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext_non_test_mode_kraken_rtb_consentString)
        # PBJ-4874 depracate
        assert_that(bid_request['user']['ext']['consent'], equal_to(1))
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))


    @allure.feature('S2S user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-3712 RTB :: Change user.ext.consent to string')
    @allure.description('Verify user.ext.consent support string')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    @pytest.mark.parametrize('placement_id', ['DEFAULT-5045327'])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_consent_support_string_02(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=ext_non_test_mode_kraken_rtb_consentString, gdpr=1, ip=eu_country_ip, consent=0)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext_non_test_mode_kraken_rtb_consentString)
        # pbj-4874 Deprecate legacy supported extension
        # assert_that(bid_request['user']['ext']['consent'], equal_to("0"))

        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))



    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3700 S2S API phase 2  Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify the gdpr flag when no regs.ext.gdpr of bid request'
                        'for en country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_parse_bid_request_with_GDPR_03(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, ip=eu_country_ip)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        assert_keys_not_exist(bid_request['user'], 'ext')
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))



    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3700 S2S API phase 2  Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify the gdpr flag when bid request regs.ext.gdpr=1 for non en country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_parse_bid_request_with_GDPR_04(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, gdpr=1, ip=fr_ip)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        assert_that(bid_request['user']['ext']['consent'], equal_to(1))
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(1))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3700 S2S API phase 2  Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify the gdpr flag bid request regs.ext.gdpr=0 for non en country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_parse_bid_request_with_GDPR_05(self, pub_app_id, placement_id, s2s_partner, rtb_ids):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=rtb_ids, gdpr=0, ip=fr_ip)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, rtb_ids)
        assert_keys_not_exist(bid_request['user'], 'ext')
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3700 S2S API phase 2  Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify the gdpr flag when no regs.ext.gdpr of bid request'
                        'for non en country')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_parse_bid_request_with_GDPR_06(self, pub_app_id, placement_id, s2s_partner):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, ip=fr_ip)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        assert_keys_not_exist(bid_request['user'], 'ext')
        assert_that(bid_request['regs']['ext']['gdpr'], equal_to(0))

    # @allure.feature('s2s device id')
    # @allure.tag('normal')
    # @allure.story('PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify hash device id if gdpr')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    # @pytest.mark.parametrize('placement_id', ['DEFAULT-5045327'])
    # @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    # @pytest.mark.parametrize('consent', [0, 1])
    # def test_s2s_device_id(self, pub_app_id, placement_id, s2s_partner, consent):
    #
    #     test_ifa = gen_device_id()
    #     r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
    #                     rtb=ext1_non_test_mode_kraken_rtb_ids_vast, gdpr=1, ip=eu_country_ip, consent=consent)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
    #     device_info = get_device_info(r)
    #     if consent is 0:
    #         assert_keys_not_exist(bid_request['device'], 'ifa')
    #         assert_that(device_info['source'], equal_to('GDPR'))
    #         assert_that(device_info['id'] is not equal_to(test_ifa))
    #     else:
    #         assert_keys_exist(bid_request['device'], 'ifa')
    #         assert_that(bid_request['device']['ifa'], equal_to(test_ifa))
    #         assert_that(device_info['source'], equal_to('IFA'))
    #         assert_that(device_info['id'], equal_to(test_ifa))


    # @allure.feature('s2s device id')
    # @allure.tag('normal')
    # @allure.story('PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify hash device id if ifa is ZERO')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    # @pytest.mark.parametrize('placement_id', ['DEFAULT-5045327'])
    # @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    # @pytest.mark.parametrize('consent', [0, 1])
    # def test_hash_device_id_for_ifa_zero(self, pub_app_id, placement_id, s2s_partner, consent):
    #     test_ifa = '00000000-0000-0000-0000-000000000000'
    #     r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa, idfv='',
    #                     rtb=ext1_non_test_mode_kraken_rtb_ids_vast, gdpr=1, ip=eu_country_ip, consent=consent)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
    #     device_info = get_device_info(r)
    #     if consent == 1:
    #         assert_that(device_info['source'], equal_to('unknown'))
    #         assert_that(device_info['id'],  equal_to(""))
    #     else:
    #         assert_keys_not_exist(bid_request['device'], 'ifa')
    #         assert_that(device_info['source'], equal_to('Vungle_FP'))
    #         assert_that(device_info['id'] is not equal_to(test_ifa))



    # @allure.feature('s2s device id')
    # @allure.tag('normal')
    # @allure.story('PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify normalize device id when ifa is null but has ifv in device.ext')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    # @pytest.mark.parametrize('placement_id', ['DEFAULT-5045327'])
    # @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    # @pytest.mark.parametrize('consent', [0, 1])
    # def test_device_id_with_ifv(self, pub_app_id, placement_id, s2s_partner, consent):
    #     test_ifa = gen_device_id()
    #     r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa='', idfv=test_ifa,
    #                     rtb=ext1_non_test_mode_kraken_rtb_ids_vast, gdpr=1, ip=eu_country_ip, consent=consent)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
    #     device_info = get_device_info(r)
    #     if consent == 1:
    #         assert_that(device_info['source'], equal_to('IDFV'))
    #         assert_that(device_info['id'], equal_to(test_ifa))
    #     else:
    #         assert_keys_not_exist(bid_request['device'], 'ifa')
    #         assert_that(device_info['source'], equal_to('GDPR'))
    #         assert_that(device_info['id'] is not equal_to(test_ifa))


    # @allure.feature('s2s device id')
    # @allure.tag('normal')
    # @allure.story('PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify normalize device id when ifv and idfv are null')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', ['5c003b9a3933314cf38ff7f3'])
    # @pytest.mark.parametrize('placement_id', ['DEFAULT-5045327'])
    # @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    # @pytest.mark.parametrize('consent', [0, 1])
    # def test_hash_device_id_for_no_ifv_and_no_idfv(self, pub_app_id, placement_id, s2s_partner, consent):
    #     r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa='', idfv='',
    #                     rtb=ext1_non_test_mode_kraken_rtb_ids_vast, gdpr=1, ip=eu_country_ip, consent=consent)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
    #     device_info =get_device_info(r)
    #     if consent == 1:
    #         assert_that(device_info['source'], equal_to('unknown'))
    #         assert_that(device_info['id'], equal_to(""))
    #     else:
    #         assert_keys_not_exist(bid_request['device'], 'ifa')
    #         assert_that(device_info['source'], equal_to('Vungle_FP'))
    #         assert_that(device_info['id'] is not None)



    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    # @pytest.mark.parametrize('placement_id', [windows_common_test_placement])
    # @pytest.mark.parametrize('consent', [0, 1])
    # def test_device_id_windows_with_GDPR_1(self, pub_app_id, placement_id, consent):
    #
    #     test_ifa = test_mode_device_id
    #     r = request_s2s(platform='windows', pub_app_id=pub_app_id, placement_ref_id=placement_id,
    #                     ifa=test_ifa, ip=eu_country_ip, gdpr=1, consent=consent,
    #                     ashwid="", rtb=ext_test_mode_kraken_rtb_ids_vast)
    #     device_info = get_device_info(r)
    #     if consent == 0:
    #         assert_that(device_info['source'], equal_to('GDPR'))
    #         assert_that(device_info['id'] is not equal_to(test_ifa))
    #     else:
    #         assert_that(device_info['source'], equal_to('IFA'))
    #         assert_that(device_info['id'], equal_to(test_ifa))

    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    # @pytest.mark.parametrize('placement_id', [windows_common_test_placement])
    # @pytest.mark.parametrize('consent', [0, 1])
    # def test_device_id_windows_with_no_ifv(self, pub_app_id, placement_id, consent):
    #
    #     test_ifa = test_mode_device_id
    #     r = request_s2s(platform='windows', pub_app_id=pub_app_id, placement_ref_id=placement_id,
    #                     ifa='', ip=eu_country_ip, gdpr=1, consent=consent,
    #                     ashwid=test_ifa, rtb=ext_test_mode_kraken_rtb_ids_vast)
    #     device_info = get_device_info(r)
    #     if consent == 0:
    #         assert_that(device_info['source'], equal_to('GDPR'))
    #         assert_that(device_info['id'] is not equal_to(test_ifa))
    #     else:
    #         assert_that(device_info['source'], equal_to('ASHWID'))
    #         assert_that(device_info['id'], equal_to(test_ifa))

    #
    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    # @pytest.mark.parametrize('placement_id', [windows_common_test_placement])
    # @pytest.mark.parametrize('consent', [0])
    # def test_device_id_windows_with_no_ifv_no_ashwid(self, pub_app_id, placement_id, consent):
    #
    #     test_ifa = ''
    #     r = request_s2s(platform='windows', pub_app_id=pub_app_id, placement_ref_id=placement_id,
    #                     ifa='', ip=fr_ip, gdpr=1, consent=consent,
    #                     ashwid='', rtb=ext_test_mode_kraken_rtb_ids_vast)
    #     device_info = get_device_info(r)
    #     assert_that(device_info['source'], equal_to('Vungle_FP'))
    #     assert_that(device_info['id'] is not equal_to(test_ifa))




