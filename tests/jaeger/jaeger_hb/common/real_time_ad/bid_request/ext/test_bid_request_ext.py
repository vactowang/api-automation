import allure

from utils.behaviors import request_hbp_with_real_time_token, \
    get_bid_request_obj_from_hbp_explain, get_ext_debug_from_jaeger_explain, request_hbp
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('Real-time bid request ext')
class TestBidRequestExt(object):
    @allure.feature('bid request details')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request ext')
    @allure.description('Verify bid request ext details from debug info')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_bid_request_ext_schain_details(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                assert_that(isinstance(bid_request['ext']['schain']['complete'], int))
                assert_that(isinstance(bid_request['ext']['schain']['ver'], str))
                assert_that(isinstance(bid_request['ext']['schain']['nodes'][0]['asi'], str))
                assert_that(isinstance(bid_request['ext']['schain']['nodes'][0]['sid'], str))
                assert_that(isinstance(bid_request['ext']['schain']['nodes'][0]['rid'], str))
                assert_that(isinstance(bid_request['ext']['schain']['nodes'][0]['name'], str))
                assert_that(isinstance(bid_request['ext']['schain']['nodes'][0]['hp'], int))

    @allure.feature('bid request details')
    @allure.tag('basic', 'smoke')
    @allure.story('seller.json')
    @allure.description('Test for supply chain obj - sid is not in seller.json')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_schain_obj_sid_not_in_seller_json(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                schain_obj = bid_request['ext']['schain']
                assert_that(schain_obj['ver'], not empty())
                assert_that(schain_obj['complete'], not empty())
                assert_that(schain_obj['nodes'][0]['asi'], not empty())
                assert_that(schain_obj['nodes'][0]['sid'], not empty())
                assert_that(schain_obj['nodes'][0]['name'], not empty())
                assert_that(schain_obj['nodes'][0]['rid'], bid_request['id'])
                assert_that(schain_obj['nodes'][0]['hp'], not empty())

    @allure.feature('bid request details')
    @allure.tag('basic', 'smoke')
    @allure.story('seller.json')
    @allure.description('Test for supply chain obj - sid in seller.json')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_schain_obj_sid_in_seller_json(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=test_mode_kraken_rtb_ids_1)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, test_mode_kraken_rtb_ids_1)
                schain_obj = bid_request['ext']['schain']
                assert_that(schain_obj['ver'], not empty())
                assert_that(schain_obj['complete'], not empty())
                assert_that(schain_obj['nodes'][0]['asi'], not empty())
                assert_that(schain_obj['nodes'][0]['sid'], not empty())
                assert_that(schain_obj['nodes'][0]['rid'], bid_request['id'])
                assert_that(schain_obj['nodes'][0]['hp'], not empty())

    @allure.feature('bid request details')
    @allure.tag('basic', 'smoke')
    @allure.description('Verify there is no user.ext.vungle from bid_request for XRTB')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_remove_ext_vungle_for_xrtb_01(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, banner=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext1_non_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext1_non_test_mode_kraken_rtb_ids_vast)
                user = bid_request['user']
                assert_keys_not_exist(user['ext'], 'vungle')

    @allure.feature('bid request details')
    @allure.tag('basic', 'smoke')
    @allure.story('seller.json')
    @allure.description('Verify there is no user.ext.vungle from bid_request for XRTB even visionEnabled = true')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_remove_ext_vungle_for_xrtb_02(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, banner=True,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext1_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext1_test_mode_kraken_rtb_ids_vast)
                user = bid_request['user']
                assert_keys_not_exist(user['ext'], 'vungle')

    @allure.feature('bid request details')
    @allure.tag('basic', 'smoke')
    @allure.story('seller.json')
    @allure.description('Verify there is no user.ext.vungle from bid_request for XRTB even visionEnabled = true')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_remove_ext_vungle_for_xrtb_02(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=test_mode_device_id, sdk_v=sdk_v, banner=True,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext1_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload, ext1_test_mode_kraken_rtb_ids_vast)
                user = bid_request['user']
                assert_keys_not_exist(user['ext'], 'vungle')

    @allure.feature('bid request details')
    @allure.tag('basic', 'smoke')
    @allure.story('bid request ext')
    @allure.description('PBJ-4476 Jaeger - Remove ext.region in bid request to LO')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_real_time_bid_request_no_regeion_LO(self, pub_app_id, placement, sdk_v, partner):

        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast_liftoff)
                assert_keys_not_exist(bid_request['ext'], 'region')

    @allure.feature('IP')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5305 [HB] Fallback lookup ip when no geo country in mediation bidrequest')
    @allure.description('Verify that will record bidrequest ip in cases of: ip not in V3, exist in bidreuqest.ip')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_fall_back_ip_01(self, pub_app_id, placement, sdk_v, partner):
        """

        ip not exist in V3 token
        ip exist in bid request:77.204.247.74(eu_country_ip)
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                geo_country = device['geo']['country']
                assert_that(device['ip'], equal_to(eu_country_ip))
                hb_transaction = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
                transaction_device_ip = hb_transaction['bidrequest_device_ip']
                transaction_geo_country = hb_transaction['bidrequest_geo_country']
                assert_that(transaction_device_ip, equal_to(eu_country_ip))
                assert_that(transaction_geo_country, equal_to(geo_country))
                assert_that(transaction_geo_country, equal_to('FRA'))
                # also validate that "bidrequest_geo_country":"FRA" pass to bflat requet
        else:
            assert False

    @allure.feature('IP')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5305 [HB] Fallback lookup ip when no geo country in mediation bidrequest')
    @allure.description('Verify that will record bidrequest ip in cases of: ip in V3 and bidRequest ip both existing')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_fall_back_ip_02(self, pub_app_id, placement, sdk_v, partner):
        """
        ip not exist in V3 token
        ip exist in bid request:77.204.247.74(eu_country_ip)
        ip in token: '117.136.240.121'(cn_ip)
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_cn_ip)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                geo_country = device['geo']['country']
                assert_that(device['ip'], equal_to(cn_ip))
                hb_transaction = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
                transaction_device_ip = hb_transaction['bidrequest_device_ip']
                transaction_geo_country = hb_transaction['bidrequest_geo_country']
                assert_that(transaction_device_ip, equal_to(cn_ip))
                assert_that(transaction_geo_country, equal_to(geo_country))
                assert_that(transaction_geo_country, equal_to('CHN'))
                # also validate that "bidrequest_geo_country":"CHN" pass to bflat requet
        else:
            assert False

    @allure.feature('IP')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5305 [HB] Fallback lookup ip when no geo country in mediation bidrequest')
    @allure.description('Verify that will record bidrequest ip in cases of: ip in token but not in bidrequest')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_fall_back_ip_03(self, pub_app_id, placement, sdk_v, partner):
        """
        ip not exist in V3 token
        ip exist in bid request:None
        ip in token: '117.136.240.121'(cn_ip)
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=None, header_ip=fr_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_cn_ip)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                geo_country = device['geo']['country']
                assert_that(device['ip'], equal_to(cn_ip))
                hb_transaction = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
                transaction_device_ip = hb_transaction['bidrequest_device_ip']
                transaction_geo_country = hb_transaction['bidrequest_geo_country']
                assert_that(transaction_device_ip, equal_to(cn_ip))
                assert_that(transaction_geo_country, equal_to(geo_country))
                assert_that(transaction_geo_country, equal_to('CHN'))
                # also validate that "bidrequest_geo_country":"CHN" pass to bflat requet
        else:
            assert False

    @allure.feature('IP')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5305 [HB] Fallback lookup ip when no geo country in mediation bidrequest')
    @allure.description('Verify that will record bidrequest ip in cases of: ip and bidRequest both not exist')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_fall_back_ip_04(self, pub_app_id, placement, sdk_v, partner):
        """
        ip not exist in V3 token
        ip exist in bid request:None
        ip in token: None
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=None, header_ip=fr_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_non_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                geo_country = device['geo']['country']
                assert_that(device['ip'], equal_to(cn_ip))
                hb_transaction = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
                transaction_device_ip = hb_transaction['bidrequest_device_ip']
                transaction_geo_country = hb_transaction['bidrequest_geo_country']
                assert_that(transaction_device_ip, equal_to(cn_ip))
                assert_that(transaction_geo_country, equal_to(geo_country))
                assert_that(transaction_geo_country, equal_to(''))
                # also validate that "bidrequest_geo_country":"" pass to bflat requet
        else:
            assert False

    @allure.feature('IP')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5305 [HB] Fallback lookup ip when no geo country in mediation bidrequest')
    @allure.description('Verify that will record bidrequest ip in cases of: ip not in V3, exist in bidreuqest.ip')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_fall_back_ip_precache_01(self, pub_app_id, placement, sdk_v, partner):
        """
        ip not exist in V3 token
        ip exist in bid request:77.204.247.74(eu_country_ip)
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                hb_transaction = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
                transaction_device_ip = hb_transaction['bidrequest_device_ip']
                transaction_geo_country = hb_transaction['bidrequest_geo_country']
                assert_that(transaction_device_ip, equal_to(eu_country_ip))
                assert_that(transaction_geo_country, equal_to('FRA'))
                # also validate that "bidrequest_geo_country":"FRA" pass to bflat requet
        else:
            assert False

    @allure.feature('IP')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5305 [HB] Fallback lookup ip when no geo country in mediation bidrequest')
    @allure.description('Verify that will record bidrequest ip in cases of: ip in V3 and bidRequest ip both existing')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_fall_back_ip_precache_02(self, pub_app_id, placement, sdk_v, partner):
        """
        ip not exist in V3 token
        ip exist in bid request:77.204.247.74(eu_country_ip)
        ip in token: '117.136.240.121'(cn_ip)
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False,
                                                explain=True, ip=eu_country_ip,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_cn_ip
                                                )

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                hb_transaction = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
                transaction_device_ip = hb_transaction['bidrequest_device_ip']
                transaction_geo_country = hb_transaction['bidrequest_geo_country']
                assert_that(transaction_device_ip, equal_to(cn_ip))
                assert_that(transaction_geo_country, equal_to('CHN'))
                # also validate that "bidrequest_geo_country":"CHN" pass to bflat requet
        else:
            assert False

    @allure.feature('IP')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5305 [HB] Fallback lookup ip when no geo country in mediation bidrequest')
    @allure.description('Verify that will record bidrequest ip in cases of: ip in V3 and bidRequest ip both existing')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_fall_back_ip_precache_03(self, pub_app_id, placement, sdk_v, partner):
        """
        ip not exist in V3 token
        ip exist in bid request:174.137.51.62
        """
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), sdk_v=sdk_v,
                           ip=eu_country_ip, ads_debug='jaeger',
                           rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                           config_extension=config_extension_cn_ip, debug='jaeger'
                           )

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                hb_transaction = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
                transaction_device_ip = hb_transaction['bidrequest_device_ip']
                transaction_geo_country = hb_transaction['bidrequest_geo_country']
                assert_that(transaction_geo_country, equal_to('USA'))
                # also validate that "bidrequest_geo_country":"USA" pass to bflat requet
        else:
            assert False

    @allure.feature('IP')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5305 [HB] Fallback lookup ip when no geo country in mediation bidrequest')
    @allure.description('Verify that will record bidrequest ip in cases of: ip in V3 and bidRequest ip both existing')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_fall_back_ip_t(self, pub_app_id, placement, sdk_v, partner):
        """
        ip not exist in V3 token
        ip exist in bid request:77.204.247.74(eu_country_ip)
        ip in token: '117.136.240.121'(cn_ip)
        """
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True,
                                                explain=True, ip=eu_country_ip, is_test=1,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast,
                                                config_extension=config_extension_cn_ip)

        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            if "err_msg" not in response_payload['ext']:
                bid_request = get_bid_request_obj_from_hbp_explain(response_payload,
                                                                   ext_test_mode_kraken_rtb_ids_vast)
                device = bid_request['device']
                geo_country = device['geo']['country']
                assert_that(device['ip'], equal_to(cn_ip))
                hb_transaction = get_ext_debug_from_jaeger_explain(response_payload, 'hb-transaction')
                transaction_device_ip = hb_transaction['bidrequest_device_ip']
                transaction_geo_country = hb_transaction['bidrequest_geo_country']
                assert_that(transaction_device_ip, equal_to(cn_ip))
                assert_that(transaction_geo_country, equal_to(geo_country))
                assert_that(transaction_geo_country, equal_to('CHN'))
        else:
            assert False
