import allure

from utils.behaviors import request_hbp
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('HBP test mode')
class TestTestMode(object):

    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=1" and "pub app=test mode, device id =test mode" is test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_4])
    @pytest.mark.parametrize('placement', [common_test_placement_4])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_test_mode_01(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=test_mode_device_id, rtb=test_mode_kraken_rtb_ids,
                           sdk_v=sdk_v, is_test=1, debug='jaeger')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                assert_that(bid_info['price'], equal_to(4999))
            else:
                assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], equal_to(1))
    # jaeger no ads
    # @allure.feature('test mode refactor')
    # @allure.tag('normal')
    # @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    # @allure.description('Verify "mediation test=1" and "pub app=test mode, device_id=non test mode" is test mode')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_4])
    # @pytest.mark.parametrize('placement', [common_test_placement_4])
    # @pytest.mark.parametrize('partner', hb_partner_list)
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    # def test_test_mode_02(self, pub_app_id, placement, partner, sdk_v):
    #     info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                        test_device_id=gen_device_id(), rtb=ext_non_test_mode_kraken_rtb_ids_vast,
    #                        sdk_v=sdk_v, is_test=1)
    #
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         bid_info = response_payload['seatbid'][0]['bid'][0]
    #         assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
    #         if partner == 'admob':
    #             assert_that(bid_info['price'], equal_to(4999))
    #         else:
    #             assert_that(bid_info['price'], equal_to(50))
    #         assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=1" and "pub app=active, device id =non test mode" is test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_test_mode_03(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                           sdk_v=sdk_v, is_test=1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                assert_that(bid_info['price'], equal_to(4999))
            else:
                assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=1" and "pub app=active, device id = test mode" is test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_test_mode_04(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=test_mode_device_id, rtb=test_mode_kraken_rtb_ids,
                           sdk_v=sdk_v, is_test=1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                assert_that(bid_info['price'], equal_to(4999))
            else:
                assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=1" and "pub app=active, device id = non test mode" is test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_test_mode_05(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                           sdk_v=sdk_v, is_test=1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                assert_that(bid_info['price'], equal_to(4999))
            else:
                assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=0" and "pub app=active, device = non test mode" '
                        'will serve live ads')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_test_mode_06(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v=sdk_v, is_test=0)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'], not equal_to(50.001))
            assert_keys_not_exist(response_payload, 'ext')

    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=0" and "pub app=active, device = test mode" '
                        'will serve test ads')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_test_mode_07(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=test_mode_device_id, rtb=test_mode_kraken_rtb_ids,
                           sdk_v=sdk_v, is_test=0)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                assert_that(bid_info['price'], equal_to(4999))
            else:
                assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], equal_to(1))

    @allure.feature('test mode refactor')
    @allure.tag('normal', 'v0.98.0')
    @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    @allure.description('Verify "mediation test=0" and "pub app=test mode", test device=test mode'
                        ' will serve test ads')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_4])
    @pytest.mark.parametrize('placement', [common_test_placement_4])
    @pytest.mark.parametrize('partner', hb_partner_list)
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_test_mode_08(self, pub_app_id, placement, partner, sdk_v):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=test_mode_device_id, rtb=test_mode_kraken_rtb_ids,
                           sdk_v=sdk_v, is_test=0)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            if partner == 'admob':
                assert_that(bid_info['price'], equal_to(4999))
            else:
                assert_that(bid_info['price'], equal_to(50.001))
            # assert_that(response_payload['ext']['test'], equal_to(1))

    # no bid
    # @allure.feature('test mode refactor')
    # @allure.tag('normal')
    # @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    # @allure.description('Verify "mediation test=0" and "pub app=test mode", test device=non test mode'
    #                     ' will no bid')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_4])
    # @pytest.mark.parametrize('placement', [common_test_placement_4])
    # @pytest.mark.parametrize('partner', hb_partner_list)
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    # def test_test_mode_12(self, pub_app_id, placement, partner, sdk_v):
    #     info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                        test_device_id=gen_device_id(), rtb=ext_non_test_mode_kraken_rtb_ids_vast,
    #                        sdk_v=sdk_v, is_test=0)
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         bid_info = response_payload['seatbid'][0]['bid'][0]
    #         assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
    #         assert_that(bid_info['price'], not equal_to(50))
    #         assert_keys_not_exist(response_payload, 'ext')




    # jaeger no serve
    # @allure.feature('test mode refactor')
    # @allure.tag('normal')
    # @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    # @allure.description('Verify "mediation test=0" and "pub app=inactive", '
    #                     'device=test mode device id will no bid')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_7])
    # @pytest.mark.parametrize('placement', [common_test_placement_7])
    # @pytest.mark.parametrize('partner', ['max'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    # def test_test_mode_16(self, pub_app_id, placement, partner, sdk_v):
    #     info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                        test_device_id=test_mode_device_id, rtb=ext_test_mode_kraken_rtb_ids_vast,
    #                        sdk_v=sdk_v, is_test=0)
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         bid_info = response_payload['seatbid'][0]['bid'][0]
    #         assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
    #         assert_that(bid_info['price'], not equal_to(50))
    #         assert_keys_not_exist(response_payload, 'ext')


    # jaeger no serve
    # @allure.feature('test mode refactor')
    # @allure.tag('normal')
    # @allure.story('PBJ-4603 Publisher Test Mode Enhancement')
    # @allure.description('Verify "mediation test=0" and "pub app=inactive", '
    #                     'device=non test mode device id will no bid')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app_7])
    # @pytest.mark.parametrize('placement', [common_test_placement_7])
    # @pytest.mark.parametrize('partner', ['max'])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    # def test_test_mode_17(self, pub_app_id, placement, partner, sdk_v):
    #     info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                        test_device_id=gen_device_id(), rtb=ext_non_test_mode_kraken_rtb_ids_vast,
    #                        sdk_v=sdk_v, is_test=0)
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         bid_info = response_payload['seatbid'][0]['bid'][0]
    #         assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
    #         assert_that(bid_info['price'], not equal_to(50))
    #         assert_keys_not_exist(response_payload, 'ext')

