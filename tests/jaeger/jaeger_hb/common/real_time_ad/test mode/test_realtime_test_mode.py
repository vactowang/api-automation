import allure

from utils.behaviors import request_hbp_with_real_time_token
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('HBP real time test mode')
class TestRealTimeTestMode(object):

    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=1" and "pub app=test mode, device id =test mode" is test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_4])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_4])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_real_time_test_mode_01(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=1)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], equal_to(1))



    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=1" and "pub app=test mode, device_id=non test mode" is no bid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_4])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_4])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_real_time_test_mode_02(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_keys_exist(response_payload, 'ext')


    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=1" and "pub app=active, device id =non test mode" is test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_real_time_test_mode_03(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'], equal_to(4999))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode refactor')
    @allure.tag('normal','v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=1" and "pub app=active", and device_id ="test mode device id" '
                        'is test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_real_time_test_mode_04(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=1)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=1" and "pub app=inactive and device_id ="test mode device id" '
                        ' will no bid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_7])
    @pytest.mark.parametrize('placement', [common_test_placement_real_time_7])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_real_time_test_mode_05(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, is_test=1)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload, 'ext')


    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=0" and "pub app=active, device = non test mode" '
                        'will serve live ads')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_real_time_test_mode_06(self, pub_app_id, placement, partner, sdk_v):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext1_non_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                is_test=0, override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'],  is_not(50.001))


    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=0" and "pub app=active, device=test mode" will serve test ads')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_real_time_test_mode_7(self, pub_app_id, placement, partner, sdk_v):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=False, explain=True,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                is_test=0, override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                assert_that(bid_info['price'], equal_to(4999))
            else:
                assert_that(bid_info['price'], equal_to(50.001))
            # assert_that(response_payload['ext']['test'], equal_to(1))


    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=0" and "pub app=test mode", test device=test mode'
                        ' will be test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_4])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_4])
    @pytest.mark.parametrize('partner', ['admob'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_real_time_test_mode_8(self, pub_app_id, placement, partner, sdk_v):
        override_bid_response_any = 'seatbid.0.bid.0.crid@"realTimeCid_%s"' % get_current_timestamp()
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_rtb_ids,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                is_test=0, override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'], equal_to(4999))
            # assert_that(response_payload['ext']['test'], '1')

    # @allure.feature('test mode refactor')
    # @allure.tag('normal')
    # @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    # @allure.description('Verify "mediation test=0" and "pub app=test mode", test device=non test mode'
    #                     ' will no bid')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_4])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement_4])
    # @pytest.mark.parametrize('partner', ['admob'])
    # @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    # def test_real_time_test_mode_9(self, pub_app_id, placement, partner, sdk_v):
    #     info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                                             rtb=ext_test_mode_kraken_rtb_ids_vast,
    #                                             no_pre_cache_token=True, explain=True,
    #                                             token_device_id=gen_device_id(), sdk_v=sdk_v,
    #                                             is_test=0)
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         bid_info = response_payload
    #         assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
    #         assert_keys_exist(bid_info['ext'], "err_msg")



    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=0" and "pub app=inactive", '
                        'device=non test mode device id will no bid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', ['5f83bcabe4a98ce0adf0d35c'])
    @pytest.mark.parametrize('placement', ['DEFAULT-4552747'])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    def test_real_time_test_mode_10(self, pub_app_id, placement, partner, sdk_v):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                is_test=0)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_keys_exist(response_payload['ext'], 'err_msg')

