import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import post_hbp_request, request_hb_win_notification, request_hbp, request_hb_loss_notification
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('HBP Multi-cache Ads')
class TestMultiCacheAdsCommon(object):

    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal', 'v0.55.0')
    @allure.story('PBJ-3132 Cover corner cases for real-time ads and multi-token')
    @allure.description('Verify the SDK version will not impact the multi-cache serving on SSP side')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.1', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_multi_cache_ads_sdk_version_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), sdk_v=sdk_v)

        assert_that(info['is_hbp_responded_200'], equal_to(True))

    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal')
    @allure.story('PBJ-3325 Test mode improvement for app bidding ')
    @allure.description('Verify test mode for app bidding when app test mode = OFF and is_test=1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.1', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_test_mode_for_app_bidding_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1)
        assert_that(info['is_hbp_responded_200'], equal_to(True))
        hbp_response = info['hbp_response']
        price = hbp_response['seatbid'][0]['bid'][0]['price']
        test_flag = hbp_response['ext']['test']
        if partner == 'admob':
            assert_that(price, equal_to(4999))
        else:
            assert_that(price, equal_to(50.001))
        assert_that(test_flag, equal_to(1))

    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal')
    @allure.story('PBJ-3325 Test mode improvement for app bidding ')
    @allure.description('Verify test mode for app bidding when app test mode = OFF and is_test=0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.1', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_test_mode_for_app_bidding_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=0)
        assert_that(info['is_hbp_responded_200'], equal_to(True))

        hbp_response = info['hbp_response']
        price = hbp_response['seatbid'][0]['bid'][0]['price']
        assert_that(price, is_not(50.001))

    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal')
    @allure.story('PBJ-3325 Test mode improvement for app bidding ')
    @allure.description('Verify test mode for app bidding when app test mode = on and is_test=1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.1', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_test_mode_for_app_bidding_03(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=1, rtb=test_mode_kraken_rtb_ids)
        assert_that(info['is_hbp_responded_200'], equal_to(True))
        hbp_response = info['hbp_response']
        price = hbp_response['seatbid'][0]['bid'][0]['price']
        test_flag = hbp_response['ext']['test']
        if partner == 'admob':
            assert_that(price, equal_to(4999))
        else:
            assert_that(price, equal_to(50.001))
        assert_that(test_flag, equal_to(1))

    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal')
    @allure.story('PBJ-3325 Test mode improvement for app bidding ')
    @allure.description('Verify test mode for app bidding when app test mode = on and is_test=0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.1', 'Vungle/6.9.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_test_mode_for_app_bidding_04(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=0, rtb=test_mode_kraken_rtb_ids)
        assert_that(info['is_hbp_responded_200'], equal_to(True))
        hbp_response = info['hbp_response']
        price = hbp_response['seatbid'][0]['bid'][0]['price']
        if partner == 'admob':
            assert_that(price, equal_to(4999))
        else:
            assert_that(price, equal_to(50.001))


    @allure.feature('hbp multi-cache ads')
    @allure.tag('normal', 'v0.69.0')
    @allure.story('PBJ-3540 Bidding should Accept both V2 and V3 supertoken for SDK 6.11.0-early1')
    @allure.description('Verify the updated adm via SDK version >= 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_updated_adm_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), sdk_v=sdk_v)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.hbp_max)

            if partner == 'admob':
                adm = response_payload['seatbid'][0]['bid'][0]['ext']['sdk_rendered_ad']
                assert_that(str_to_json(adm['rendering_data'])['event_id'],
                            equal_to(info['ads_response']['ads'][0]['ad_markup']['id']))
                assert_that(scrat_impression_endpoint_qa('qa') in str_to_json(adm['rendering_data'])['impression'][0])
                assert_that(str_to_json(adm['rendering_data'])['version'], equal_to(1))
            else:
                adm = response_payload['seatbid'][0]['bid'][0]['adm']
                assert_that(str_to_json(adm)['event_id'], equal_to(info['ads_response']['ads'][0]['ad_markup']['id']))
                assert_that(scrat_impression_endpoint_qa('qa') in str_to_json(adm)['impression'][0])
                assert_that(str_to_json(adm)['version'], equal_to(1))