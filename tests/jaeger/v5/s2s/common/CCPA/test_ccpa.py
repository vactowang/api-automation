import pytest
import allure

from data.request_payload import s2s_partner
from utils.assertions import *
from utils.behaviors import request_s2s, get_bid_request_obj_from_jaeger_explain
from utils.common import *
from settings import *



@allure.epic('CCPA')
class TestCommonS2S(object):

    @allure.feature('S2S user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify us_privacy in case of CCPA status opted out')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('ip', [ca_us_ip])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_parse_bid_request_with_CCPA_01(self, pub_app_id, placement_id, ip, s2s_partner, rtb_ids):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_ifa,
                        rtb=rtb_ids, ccpa='1-Y-', ip=ip)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, rtb_ids)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-Y-'))


    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify us_privacy in case of CCPA status opted out by location')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_parse_bid_request_with_CCPA_02(self, pub_app_id, placement_id, s2s_partner):
        '''
        Account level setting:
        "is_ccpa_opt_out": true
        '''
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=gen_device_id(),
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, ccpa='1---', ip=ca_us_ip)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-Y-'))



    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify us_privacy in case of CCPA status opted in by location')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_parse_bid_request_with_CCPA_03(self, pub_app_id, s2s_partner, rtb_ids):
        '''
        Account level setting:
        "is_ccpa_opt_out": false
        '''
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id='DEFAULT-5045327', ifa=gen_device_id(),
                        rtb=rtb_ids, ccpa='1---', ip=ca_us_ip)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, rtb_ids)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-N-'))


    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('PBJ-3700 S2S API phase 2 Implementation - Make sure compliant with privacy GDPR/CCPA/COPPA')
    @allure.description('Verify us_privacy in case of CCPA status repect the external consent')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_parse_bid_request_with_CCPA_04(self, pub_app_id, s2s_partner):
        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id='DEFAULT-5045327',
                        ifa=ccpa_external_consents_opted_out_device_id, ip=eu_country_ip,
                        rtb=ext1_non_test_mode_kraken_rtb_ids_vast, ccpa='1-N-')
        if 'nbr' in r:
            return
        else:
            bid_request = get_bid_request_obj_from_jaeger_explain(r, ext1_non_test_mode_kraken_rtb_ids_vast)
            assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1-Y-'))


    @allure.feature('user privacy')
    @allure.tag('smoke')
    @allure.story('CCPA support')
    @allure.description('Verify us_privacy in case of CCPA status not exist')
    @allure.severity('smoke')
    @pytest.mark.parametrize('data', [{"app": common_test_app, "placement": common_test_placement},
                                      {"app": "5c003b9a3933314cf38ff7f3", "placement": "DEFAULT-5045327"}])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    @pytest.mark.parametrize('rtb_ids', [ext1_non_test_mode_kraken_rtb_ids_vast])
    def test_ccpa_status_not_exist(self, data, s2s_partner, rtb_ids):
        test_ifa = gen_device_id()
        r = request_s2s(s2s_partner, pub_app_id=data['app'], placement_ref_id=data['placement'], ifa=test_ifa,
                        rtb=rtb_ids, ip=eu_country_ip)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, rtb_ids)
        assert_that(bid_request['regs']['ext']['us_privacy'], equal_to('1---'))

    @allure.feature('S2S')
    @allure.tag('smoke', 'test mode')
    @allure.story('PBJ-3778 S2S API phase 2 Implementation - Add traffic source flag')
    @allure.description('Verify the traffic source flag is s2s')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    def test_s2s_traffic_flag(self, pub_app_id, placement_id, s2s_partner):

        r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=test_mode_device_id,
                        rtb=test_mode_kraken_rtb_ids)
        bid_request = get_bid_request_obj_from_jaeger_explain(r, test_mode_kraken_rtb_ids)
        assert_that(bid_request['ext']['vungle']['src'], equal_to('s2s'))

    # @allure.feature('S2S')
    # @allure.tag('smoke')
    # @allure.story('PBJ-3778 S2S API phase 2 Implementation - Add traffic source flag')
    # @allure.description('Verify the traffic source flag is s2s')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement_id', [common_test_placement])
    # @pytest.mark.parametrize('s2s_partner', config['s2s_partners'])
    # def test_s2s_traffic_flag_meister(self, pub_app_id, placement_id, s2s_partner):
    #
    #     r = request_s2s(s2s_partner, pub_app_id=pub_app_id, placement_ref_id=placement_id, ifa=gen_device_id(),
    #                     rtb=win_notification_meister_rtb_ids)
    #     bid_request = get_bid_request_obj_from_jaeger_explain(r, win_notification_meister_rtb_ids)
    #     assert_that(bid_request['ext']['vungle']['src'], equal_to('s2s'))

