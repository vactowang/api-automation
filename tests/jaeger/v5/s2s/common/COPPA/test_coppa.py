import pytest
import allure

from data.request_payload import s2s_partner
from utils.assertions import *
from utils.behaviors import request_s2s, get_bid_request_obj_from_jaeger_explain, get_device_info
from utils.common import *
from settings import *



@allure.epic('COPPA')
class TestCommonS2S(object):

    @allure.feature('S2S user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify coppa field with placement level true')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('coppa', [None, 0, 1])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_parse_bid_request_with_COPPA_01(self, pub_app_id, placement_id, coppa, s2s_partner):
        """

         App level setting:
         "isCoppaCompliant": true

         Placement level setting:
         "is_coppa": true

         """
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        if coppa == 0:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
        else:
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('S2S user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify coppa field with placement level false but app level true')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    @pytest.mark.parametrize('coppa', [None, 0, 1])
    def test_parse_bid_request_with_COPPA_02(self, pub_app_id, coppa, s2s_partner):
        """
        App level setting:
        "isCoppaCompliant": true

        Placement level setting:
        "is_coppa": false

        """
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id='AREYOUS82690', ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        if coppa is None or coppa == 0:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
        else:
            assert_that(bid_request['regs']['coppa'], equal_to(1))

    @allure.feature('S2S user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify coppa field with app level true and no placement level setting')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    @pytest.mark.parametrize('coppa', [None, 0, 1])
    def test_parse_bid_request_with_COPPA_03(self, pub_app_id, coppa, s2s_partner):
        """

        App level setting:
        "isCoppaCompliant": true

        """
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id='HJKM6GM50918', ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        if coppa == 0:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
        else:
            assert_that(bid_request['regs']['coppa'], equal_to(1))


    @allure.feature('S2S user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify coppa field with app level false and no placement level setting')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    @pytest.mark.parametrize('coppa', [None, 0, 1])
    def test_parse_bid_request_with_COPPA_04(self, pub_app_id, coppa, s2s_partner):
        """

        App level setting:
        "isCoppaCompliant": false

        """
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id='DEFAULT-5045327', ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        if coppa is None or coppa == 0:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
        else:
            assert_that(bid_request['regs']['coppa'], equal_to(1))



    @allure.feature('S2S user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify coppa field with app level false and placement level true')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    @pytest.mark.parametrize('coppa', [None, 0, 1])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_parse_bid_request_with_COPPA_05(self, pub_app_id, coppa, s2s_partner, rtb_ids):
        """

           App level setting:
           "isCoppaCompliant": false

           Placement level setting:
           "is_coppa": true

        """
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id='COPPA-TEST', ifa=test_ifa,
                        rtb=rtb_ids, coppa=coppa)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, rtb_ids)
        if coppa == 0:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
        else:
            assert_that(bid_request['regs']['coppa'], equal_to(1))


    @allure.feature('S2S user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify coppa field with placement level true')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [sigmob_placement_android_01])
    @pytest.mark.parametrize('coppa', [1])
    def test_zeroout_androidid_with_COPPA_1(self, pub_app_id, placement_id, coppa):
        """
            App level setting:
            "isCoppaCompliant": false
        """
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, platform='android', pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa="",
                        android_id=test_ifa, rtb=ext1_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)

        assert_that(bid_request['regs']['coppa'], equal_to(1))
        device_info = get_device_info(r)
        assert_that(device_info['source'], equal_to('Vungle_FP'))
        assert_that(device_info['id'] is not equal_to(test_ifa))

    #
    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('placement_id', [sigmob_placement_android_01])
    # @pytest.mark.parametrize('coppa', [1])
    # def test_zeroout_androidid_with_COPPA_2(self, pub_app_id, placement_id, coppa):
    #     """
    #         App level setting:
    #         "isCoppaCompliant": false
    #     """
    #     test_ifa = '00000000-0000-0000-0000-000000000000'
    #     r = request_s2s(s2s_partner, platform='android', pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
    #                     android_id="", rtb=ext1_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
    #
    #     assert_that(bid_request['regs']['coppa'], equal_to(1))
    #     device_info = get_device_info(r)
    #     assert_that(device_info['source'], equal_to('Vungle_FP'))
    #     assert_that(device_info['id'] is not equal_to(test_ifa))

    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('placement_id', [sigmob_placement_android_01])
    # @pytest.mark.parametrize('coppa', [1])
    # def test_zeroout_androidid_with_COPPA_3(self, pub_app_id, placement_id, coppa):
    #     """
    #         App level setting:
    #         "isCoppaCompliant": false
    #     """
    #     test_ifa = gen_device_id()
    #     r = request_s2s(s2s_partner, platform='android', pub_app_id=pub_app_id, placement_ref_id=placement_id,
    #                     ifa=test_ifa,
    #                     android_id="", rtb=ext1_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
    #
    #     assert_that(bid_request['regs']['coppa'], equal_to(1))
    #     device_info = get_device_info(r)
    #     assert_that(device_info['source'], equal_to('Vungle_FP'))
    #     assert_that(device_info['id'] is not equal_to(test_ifa))


    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('placement_id', [sigmob_placement_android_01])
    # @pytest.mark.parametrize('coppa', [0])
    # def test_normalize_androidid_with_COPPA_4(self, pub_app_id, placement_id, coppa):
    #     """
    #         App level setting:
    #         "isCoppaCompliant": false
    #     """
    #     test_ifa = gen_device_id()
    #     r = request_s2s(s2s_partner, platform='android', pub_app_id=pub_app_id, placement_ref_id=placement_id,
    #                     ifa=test_ifa,
    #                     android_id="", rtb=ext1_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
    #     device_info = get_device_info(r)
    #     assert_that(device_info['source'], equal_to('IFA'))
    #     assert_that(device_info['id'], equal_to(test_ifa))


    #
    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2 Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    # @pytest.mark.parametrize('placement_id', [sigmob_placement_android_01])
    # @pytest.mark.parametrize('coppa', [0])
    # def test_normalize_androidid_with_COPPA_2(self, pub_app_id, placement_id, coppa):
    #     """
    #       App level setting:
    #       "isCoppaCompliant": false
    #     """
    #     test_ifa = gen_device_id()
    #     r = request_s2s(s2s_partner, platform='android', pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa='',
    #                     android_id=test_ifa, rtb=ext1_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
    #     device_info = get_device_info(r)
    #     assert_that(device_info['source'], equal_to('IFA'))
    #     assert_that(device_info['id'], equal_to(test_ifa))



    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('placement_id', [amazon_common_test_placement])
    # @pytest.mark.parametrize('coppa', [1])
    # def test_zeroout_amazon_with_COPPA_1(self, pub_app_id, placement_id, coppa):
    #     """
    #         App level setting:
    #         "isCoppaCompliant": false
    #     """
    #     test_ifa = test_mode_device_id
    #     r = request_s2s(platform='amazon', pub_app_id=pub_app_id, placement_ref_id=placement_id,
    #                     ifa=test_ifa, ip=au_ip,
    #                     app_set_id="", rtb=ext_test_mode_kraken_rtb_ids_vast_1, coppa=coppa)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(r, ext_test_mode_kraken_rtb_ids_vast_1)
    #
    #     assert_that(bid_request['regs']['coppa'], equal_to(1))
    #     device_info = r['ext']['debug']['auction_result']['device_info']
    #     assert_that(device_info['source'], equal_to('Vungle_FP'))
    #     assert_that(device_info['id'] is not equal_to(test_ifa))

    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('placement_id', [amazon_common_test_placement])
    # @pytest.mark.parametrize('coppa', [1])
    # def test_zeroout_amazon_with_COPPA_2(self, pub_app_id, placement_id, coppa):
    #     """
    #         App level setting:
    #         "isCoppaCompliant": false
    #     """
    #     test_ifa = '00000000-0000-0000-0000-000000000000'
    #     r = request_s2s(platform='amazon', pub_app_id=pub_app_id, placement_ref_id=placement_id,
    #                     ifa=test_ifa, ip=au_ip,
    #                     app_set_id="", rtb=ext_test_mode_kraken_rtb_ids_vast_1, coppa=coppa)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(r, ext_test_mode_kraken_rtb_ids_vast_1)
    #
    #     assert_that(bid_request['regs']['coppa'], equal_to(1))
    #     device_info = r['ext']['debug']['auction_result']['device_info']
    #     assert_that(device_info['source'], equal_to('Vungle_FP'))
    #     assert_that(device_info['id'] is not equal_to(test_ifa))
    #
    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('placement_id', [amazon_common_test_placement])
    # @pytest.mark.parametrize('coppa', [0])
    # def test_normalize_device_id_amazon_with_COPPA_3(self, pub_app_id, placement_id, coppa):
    #     """
    #         App level setting:
    #         "isCoppaCompliant": false
    #     """
    #     test_ifa = test_mode_device_id
    #     r = request_s2s(platform='amazon', pub_app_id=pub_app_id, placement_ref_id=placement_id,
    #                     ifa=test_ifa, ip=au_ip,
    #                     app_set_id="", rtb=ext_test_mode_kraken_rtb_ids_vast_1, coppa=coppa)
    #     device_info = r['ext']['debug']['auction_result']['device_info']
    #     assert_that(device_info['source'], equal_to('IFA'))
    #     assert_that(device_info['id'], equal_to(test_ifa))


    # @allure.feature('S2S user privacy')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA'
    #               'PBJ-3792 S2S API phase 2  Implementation - Add normalize device id and hash logic')
    # @allure.description('Verify coppa field with placement level true')
    # @allure.severity('smoke')
    # @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    # @pytest.mark.parametrize('placement_id', [amazon_common_test_placement])
    # @pytest.mark.parametrize('coppa', [0])
    # def test_device_id_amazon_with_COPPA_4(self, pub_app_id, placement_id, coppa):
    #     """
    #         App level setting:
    #         "isCoppaCompliant": false
    #         if user only give app set id but no ifa, means that there is no device id in the request.
    #     """
    #     test_ifa = test_mode_device_id
    #     r = request_s2s(platform='amazon', pub_app_id=pub_app_id, placement_ref_id=placement_id,
    #                     ifa="", app_set_id=test_ifa, ip=au_ip,
    #                     rtb=ext_test_mode_kraken_rtb_ids_vast_1, coppa=coppa)
    #     device_info = r['ext']['debug']['auction_result']['device_info']
    #     assert_that(device_info['source'], equal_to('unknown'))
    #     assert_that(device_info['id'], equal_to(''))


    @allure.feature('S2S user privacy')
    @allure.tag('normal')
    @allure.story('PBJ-3803 For COPPA users, do not pass lat/long to downstream buyers (DSPs)')
    @allure.description('Verify the lat and lon will not be passed if COPPA is applied')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', ['HJKM6GM50919'])
    @pytest.mark.parametrize('coppa', [1])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_not_pass_lat_lon_1(self, pub_app_id, placement_id, coppa, s2s_partner):
        """

         App level setting:
         "isCoppaCompliant": true

         No placement level setting

         """
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, coppa=coppa)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        if coppa == 0:
            assert_keys_not_exist(bid_request['regs'], 'coppa')
        else:
            assert_that(bid_request['regs']['coppa'], equal_to(1))