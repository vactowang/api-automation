
import allure
from utils.behaviors import  request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('Real-time imp')
class TestImp(object):
    @allure.feature('bid request details')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp')
    @allure.description('Verify imp details from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_details(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(bid_request['imp'][0]['displaymanager'], equal_to('Vungle'))
                assert_keys_exist(bid_request['imp'][0], 'displaymanagerver')
                assert_that(bid_request['imp'][0]['tagid'], equal_to(common_test_real_time_placement))
                assert_that('secure' in bid_request['imp'][0])

    @allure.feature('bid floor')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp')
    @allure.description('PBJ-3593 IAB bidfloor should not read from the CPM floor that was set up for'
                        ' rev share placements')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_bid_floor_for_test_mode_edsp(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=au_ip,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_test_mode_kraken_rtb_ids_vast)
                assert_that('bidfloor' in bid_request['imp'][0])
                assert_that(bid_request['imp'][0]['bidfloor'], equal_to(1))


    @allure.feature('bid floor')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp')
    @allure.description('PBJ-3593 IAB bidfloor should not read from the CPM floor that was set up for'
                        ' rev share placements')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_mrec_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_bid_floor_for_non_test_mode_edsp(self, pub_app_id, placement, sdk_v, partner):
        """

               Test country setting:

               {
                   "name" : "United Kingdom",
                   "iso_code2" : "AU",
                   "iso_code3" : "AUS",
                   "reserve_floor" : 1.0
                   "banner_reserve_floor: 30
               }

               Placement level setting:
               {
                   "default_flat_cpm": 0.8
                   "default_rev_share": 0.6
               }
        """

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=au_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_mraid)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_mraid)
                assert_that('bidfloor' in bid_request['imp'][0])
                assert_that(bid_request['imp'][0]['bidfloor'], equal_to(30))

    @allure.feature('bid floor')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-3593 IAB bidfloor should not read from the CPM floor that was set up for rev share placements')
    @allure.description('Verify no \'erpmtarget\' field from debug info for hb enabled test mode iDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_bid_floor_for_test_mode_idsp(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that('bidfloor' in bid_request['imp'][0])
                assert_keys_not_exist(bid_request['imp'][0]['ext']['vungle'], 'erpmtarget')


    @allure.feature('bid floor')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request imp')
    @allure.description('Verify imp bid floor from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_imp_bid_floor(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that('bidfloor' in bid_request['imp'][0])
                assert_that(bid_request['imp'][0]['bidfloorcur'], equal_to('USD'))

    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-2385 The instl field in bidrequest')
    @allure.description('Verify the instl field for non incentivized placement')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_instl_1(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip,
                                                rtb=test_mode_kraken_rtb_ids)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids)
                assert_that(bid_request['imp'][0]['instl'], equal_to(1))

    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-2385 The instl field in bidrequest')
    @allure.description('Verify the instl field for banner')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_instl_2(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip, banner=True,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_keys_not_exist(bid_request['imp'][0], 'instl')


    @allure.feature('instl')
    @allure.tag('basic', 'smoke')
    @allure.story('PBJ-2385 The instl field in bidrequest')
    @allure.description('Verify the instl field for mrecr')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_mrec_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_instl_3(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=au_ip, banner=True,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_keys_not_exist(bid_request['imp'][0], 'instl')

    @allure.feature('flat cpm')
    @allure.tag('normal')
    @allure.story('VM-54 extend external_dynamic_floor to Native')
    @allure.description('Verify that bid floor = THEN MAX(External Dynamic CPM Floor, 0.01) for native '
                        'placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_placement_real_time])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_ext_dynamtic_floor_01(self, pub_app_id, placement, sdk_v, partner):
        '''
            "is_flat_cpm_enabled": true
            "FR": {
                "nrg_multiplier": 1.7,
                "rev_share": 0.6,
                "dynamic_cpm_floor": 3.4884,
                "flat_cpm": 1.8,
                "external_dynamic_cpm_floor": 2
            }

            Fr reserve floor: 2.5

        '''
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=fr_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
                assert_that(bid_request['imp'][0]['bidfloor'], equal_to(2))



    @allure.feature('flat cpm')
    @allure.tag('normal')
    @allure.story('VM-54 extend external_dynamic_floor to Native')
    @allure.description('Verify that bid floor = THEN MAX(External Dynamic CPM Floor, 0.01) for native '
                        'placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [flatcpm_exp_test_app])
    @pytest.mark.parametrize('placement', [flatcpm_placement_real_time])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_ext_dynamtic_floor_02(self, pub_app_id, placement, sdk_v, partner):
        '''
              "is_flat_cpm_enabled": true
              "KP": {
                  "external_dynamic_cpm_floor": 0.001
              }

              kp reserve floor: 1

          '''
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=kp_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext_non_test_mode_kraken_rtb_ids_vast)
                assert_that(bid_request['imp'][0]['bidfloor'], equal_to(0.01))