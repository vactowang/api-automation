import pytest
import allure

from utils.assertions import *
from http import HTTPStatus
from data import request_payload
from utils.behaviors import get_bid_request_obj_from_jaeger_explain
from utils.common import *
from settings import *


@allure.epic('Sigmob')
class TestSigmobS2S(object):

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions')
    @allure.description('Verify the Sigmob can parse bid request successfully')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_parse_bid_request(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid['bid'][0]['ext'], 'imptrackers')
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions')
    @allure.description('Verify the Sigmob can parse bid request with regs param successfully')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_parse_bid_request_with_regs(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa, regs=True)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid['bid'][0]['ext'], 'imptrackers')
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions')
    @allure.description('Verify the Sigmob can parse bid request successfully if test flag=0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_parse_bid_request_test_flag_0(self, pub_app_id, placement_id):
        is_test = {
            "test": 0
        }
        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa, is_test=is_test)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid['bid'][0]['ext'], 'imptrackers')
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))

    # @allure.feature('S2S')
    # @allure.tag('normal')
    # @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions')
    # @allure.description('Verify the Sigmob can\'t parse bid request successfully if test flag=1')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement_id', [common_test_placement])
    # def test_parse_bid_request_test_flag_1(self, pub_app_id, placement_id):
    #     is_test = {
    #         "test": 1
    #     }
    #     test_ifa = gen_device_id()
    #     req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa, is_test=is_test)
    #     r = post(s2s_v5_sigmob_endpoint_qa, json=req,
    #              headers=platform_headers(sdk_version=None,
    #                                       rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
    #     assert_that(r.status_code, equal_to(HTTPStatus.NO_CONTENT))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions')
    @allure.description('Verify the Sigmob can parse skadNetwork bid request successfully')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_parse_skadn_bid_request(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        skadn = {"skadn":
            {
                "version": "2.0",
                "versions": [
                    "2.0"
                ],
                "sourceapp": "1131184101",
                "skadnetids": []
            }
        }
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa, skadn=skadn)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        bid_ext = bid['bid'][0]['ext']
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid_ext, 'imptrackers')
        assert_keys_exist(bid_ext, 'skadn')
        assert_that(bid_ext['skadn']['version'], not empty())
        assert_that(bid_ext['skadn']['network'], not empty())
        assert_that(bid_ext['skadn']['campaign'], not empty())
        assert_that(bid_ext['skadn']['itunesitem'], not empty())
        assert_that(bid_ext['skadn']['nonce'], not empty())
        assert_that(bid_ext['skadn']['sourceapp'], not empty())
        assert_that(bid_ext['skadn']['timestamp'], not empty())
        assert_that(bid_ext['skadn']['signature'], not empty())
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions')
    @allure.description('Verify the Sigmob can parse skadNetwork which version >2.0 bid request successfully')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_parse_skadn_version_above_2_bid_request(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        skadn = {"skadn":
            {
                "version": "2.2",
                "versions": [
                    "2.2"
                ],
                "sourceapp": "1131184101",
                "skadnetids": []
            }
        }
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa, skadn=skadn
                                                     )
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        bid_ext = bid['bid'][0]['ext']
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid_ext, 'imptrackers')
        assert_keys_exist(bid_ext, 'skadn')
        assert_that(bid_ext['skadn']['version'], equal_to('2.2'))
        assert_that(bid_ext['skadn']['network'], not empty())
        assert_that(bid_ext['skadn']['campaign'], not empty())
        assert_that(bid_ext['skadn']['itunesitem'], not empty())
        assert_that(bid_ext['skadn']['sourceapp'], not empty())
        assert_that(bid_ext['skadn']['fidelities'][0]['fidelity'], equal_to(0))
        assert_that(bid_ext['skadn']['fidelities'][0]['nonce'], not empty())
        assert_that(bid_ext['skadn']['fidelities'][0]['timestamp'], not empty())
        assert_that(bid_ext['skadn']['fidelities'][0]['signature'], not empty())
        assert_that(bid_ext['skadn']['fidelities'][1]['fidelity'], equal_to(1))
        assert_that(bid_ext['skadn']['fidelities'][1]['nonce'], not empty())
        assert_that(bid_ext['skadn']['fidelities'][1]['timestamp'], not empty())
        assert_that(bid_ext['skadn']['fidelities'][1]['signature'], not empty())
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions'
                  'PBJ-3554 S2S - Update bid price')
    @allure.description('Verify the Sigmob can parse bid request successfully via test mode'
                        'Verify bid price is 0.01')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_parse_bid_request_test_mode(self, pub_app_id, placement_id):
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_mode_device_id)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid['bid'][0]['ext'], 'imptrackers')
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))
        assert_that(bid['bid'][0]['price'], equal_to(0.01))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions'
                  'PBJ-3554 S2S - Update bid price')
    @allure.description('Verify the Sigmob can parse bid request successfully via test mode and test_flag=0'
                        'Verify bid price is 0.01')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_parse_bid_request_test_mode_flag_0(self, pub_app_id, placement_id):
        is_test = {
            "test": 0
        }
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_mode_device_id, is_test=is_test)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid['bid'][0]['ext'], 'imptrackers')
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))
        assert_that(bid['bid'][0]['price'], equal_to(0.01))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions'
                  'PBJ-3554 S2S - Update bid price')
    @allure.description('Verify the Sigmob can parse bid request successfully via test mode and test_flag=1'
                        'Verify bid price is 0.01')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_parse_bid_request_test_mode_flag_1(self, pub_app_id, placement_id):
        is_test = {
            "test": 1
        }
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_mode_device_id, is_test=is_test)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid['bid'][0]['ext'], 'imptrackers')
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))
        assert_that(bid['bid'][0]['price'], equal_to(0.01))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions')
    @allure.description('Verify the Sigmob can parse skadNetwork bid request successfully via test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_parse_skadn_bid_request(self, pub_app_id, placement_id):
        skadn = {"skadn":
            {
                "version": "2.0",
                "versions": [
                    "2.0"
                ],
                "sourceapp": "1131184101",
                "skadnetids": []
            }
        }
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_mode_device_id, skadn=skadn)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        bid_ext = bid['bid'][0]['ext']
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid_ext, 'imptrackers')
        assert_keys_exist(bid_ext, 'skadn')
        assert_that(bid_ext['skadn']['version'], not empty())
        assert_that(bid_ext['skadn']['network'], not empty())
        assert_that(bid_ext['skadn']['campaign'], not empty())
        assert_that(bid_ext['skadn']['itunesitem'], not empty())
        assert_that(bid_ext['skadn']['nonce'], not empty())
        assert_that(bid_ext['skadn']['sourceapp'], not empty())
        assert_that(bid_ext['skadn']['timestamp'], not empty())
        assert_that(bid_ext['skadn']['signature'], not empty())
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions')
    @allure.description('Verify the Sigmob can parse skadNetwork bid request successfully via test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_parse_skadn_bid_request(self, pub_app_id, placement_id):
        skadn = {"skadn":
            {
                "version": "2.0",
                "versions": [
                    "2.0"
                ],
                "sourceapp": "1131184101",
                "skadnetids": []
            }
        }
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_mode_device_id, skadn=skadn
                                                     )
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        bid_ext = bid['bid'][0]['ext']
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid_ext, 'imptrackers')
        assert_keys_exist(bid_ext, 'skadn')
        assert_that(bid_ext['skadn']['version'], not empty())
        assert_that(bid_ext['skadn']['network'], not empty())
        assert_that(bid_ext['skadn']['campaign'], not empty())
        assert_that(bid_ext['skadn']['itunesitem'], not empty())
        assert_that(bid_ext['skadn']['nonce'], not empty())
        assert_that(bid_ext['skadn']['sourceapp'], not empty())
        assert_that(bid_ext['skadn']['timestamp'], not empty())
        assert_that(bid_ext['skadn']['signature'], not empty())
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))


    # ---------below are test cases for android---------------------------------------------------------------

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions'
                  'PBJ-3554 S2S - Update bid price')
    @allure.description('Verify the Sigmob can parse bid request successfully for android platform'
                        'Verify the bid price is 0.01')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    def test_parse_bid_request_android(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_android(pub_app_id, placement_id, ifa=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid['bid'][0]['ext'], 'imptrackers')
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))
        assert_that(bid['bid'][0]['price'], equal_to(0.01))

    @allure.feature('S2S')
    @allure.tag('normal')
    @allure.story('PBJ-3331 Implement - Spec - parse sigmob request extensions')
    @allure.description('Verify the Sigmob can parse bid request with regs successfully for android platform')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [android_common_test_placement])
    def test_parse_bid_request_with_regs_android(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_android(pub_app_id, placement_id, ifa=test_ifa, regs=True)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'id')
        assert_keys_exist(bid['bid'][0], 'impid')
        assert_keys_exist(bid['bid'][0], 'price')
        assert_keys_exist(bid['bid'][0], 'adm')
        assert_keys_exist(bid['bid'][0], 'bundle')
        assert_keys_exist(bid['bid'][0], 'crid')
        assert_keys_exist(bid['bid'][0], 'cat')
        assert_keys_exist(bid['bid'][0]['ext'], 'imptrackers')
        assert_keys_exist(response_payload, 'bidid')
        assert_that(response_payload['cur'], equal_to('USD'))



    @allure.feature('S2S')
    @allure.tag('normal', 'v1.192.0')
    @allure.story('PBJ-3626 Return a fixed price for sigmob testing but not using fix price for publisher payout')
    @allure.description('Verify return a fixed price for the specify placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [sigmob_placement_01])
    def test_fixed_price_ios_01(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()

        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'price')
        assert_that(bid['bid'][0]['price'], equal_to(9.39))

    @allure.feature('S2S')
    @allure.tag('normal', 'v1.192.0')
    @allure.story('PBJ-3626 Return a fixed price for sigmob testing but not using fix price for publisher payout')
    @allure.description('Verify return a fixed price for the specify placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [sigmob_placement_02])
    def test_fixed_price_ios_02(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'price')
        assert_that(bid['bid'][0]['price'], equal_to(6.26))


    @allure.feature('S2S')
    @allure.tag('normal', 'v1.192.0')
    @allure.story('PBJ-3626 Return a fixed price for sigmob testing but not using fix price for publisher payout')
    @allure.description('Verify return a fixed price for the specify placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [sigmob_placement_android_01])
    def test_fixed_price_android_01(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_android(pub_app_id, placement_id, ifa=test_ifa, regs=True)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast, debug='jaeger'))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'price')
        assert_that(bid['bid'][0]['price'], equal_to(3.91))

    @allure.feature('S2S')
    @allure.tag('normal', 'v1.192.0')
    @allure.story('PBJ-3626 Return a fixed price for sigmob testing but not using fix price for publisher payout')
    @allure.description('Verify return a fixed price for the specify placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement_id', [sigmob_placement_android_02])
    def test_fixed_price_android_02(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        req = request_payload.s2s_payload_sigmob_android(pub_app_id, placement_id, ifa=test_ifa, regs=True)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid = response_payload['seatbid'][0]
        assert_keys_exist(bid['bid'][0], 'price')
        assert_that(bid['bid'][0]['price'], equal_to(5.48))

    @allure.feature('S2S')
    @allure.tag('smoke')
    @allure.story('PBJ-3717 Jaeger - S2S fix Sigmob integration issue')
    @allure.description('Verify that the bid request id should be same as bid response id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    def test_integration_issue_fix_1(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        hbp_bid_request_id = gen_device_id()
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa,
                                                     bid_reqeust_id=hbp_bid_request_id)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_that(response_payload['id'], equal_to(hbp_bid_request_id))


    @allure.feature('S2S')
    @allure.tag('smoke')
    @allure.story('PBJ-3717 Jaeger - S2S fix Sigmob integration issue')
    @allure.description('Verify that the bidid should be same as Jaeger bid request id and DSP bid response id')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_programmatic_mrec_placement])
    def test_integration_issue_fix_2(self, pub_app_id, placement_id):
        test_ifa = gen_device_id()
        if env == 'ci':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext1_non_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.s2s_payload_sigmob_ios(pub_app_id, placement_id, ifa=test_ifa)
        r = post(s2s_v5_sigmob_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=None, debug='jaeger', rtb_selector=rtb))
        response_payload = r.json()
        bid_request = get_bid_request_obj_from_jaeger_explain(response_payload)
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        assert_that(response_payload['bidid'], equal_to(response_payload['ext']['debug']['auction_result']['id']))
        assert_that(response_payload['bidid'], equal_to(bid_request['id']))
        assert_that(response_payload['bidid'], equal_to(bid_response[rtb]['id']))
