import pytest
import allure

from http import HTTPStatus

from data import request_payload, response_schema
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp, request_hbp_with_real_time_token
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('HBP Notifications')
class TestBillNotification(object):

    @allure.feature('real-time notification')
    @allure.tag('normal')
    @allure.story('PBJ-3964 Propagate `datasci_tags` into hbp-notifications topic')
    @allure.description('Verify the bflat_datasci_tags were added in ext')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement_10])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max', 'admob'])
    def test_real_time_burl_1(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                explain=True)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            burl = response_payload['seatbid'][0]['bid'][0]['burl']
            r_url = get(burl.replace('${AUCTION_PRICE}', '5.4').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            ext = decode_ext(burl)

            assert_keys_exist(ext, 'bflat_datasci_tags')
            bflat_datasci_tags = str_to_json(ext['bflat_datasci_tags'])
            assert_that(isinstance(bflat_datasci_tags['bp'], float))
            assert_that(isinstance(bflat_datasci_tags['b'], str))
            assert_that(isinstance(bflat_datasci_tags['e'], int))
            assert_that(bflat_datasci_tags['dsp_t'], 'edsp')
            assert_that(isinstance(bflat_datasci_tags['ad_t'], str))

    @allure.feature('real-time notification')
    @allure.tag('normal')
    @allure.story('PBJ-4404 [HAProxy][jaeger] Add notification ext with proxy & proxyenv flag')
    @allure.description('Verify X-Source, X-Env add in request header')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('header_dimension_source', ['', 'haproxy', 'akamai'])
    @pytest.mark.parametrize('header_dimension_env', ['', 'qa', 'stage', 'prod'])
    def test_real_time_header_source_add_in_url_01(self, pub_app_id, placement, sdk_v, partner, header_dimension_source,
                                                header_dimension_env):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=True,
                                                source=header_dimension_source, x_env=header_dimension_env,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            nurl = response_payload['seatbid'][0]['bid'][0]['nurl']
            ext = decode_ext(url=nurl)
            if header_dimension_source in ['', 'akamai']:
                assert_keys_not_exist(ext, 'pxs')
            if header_dimension_source == 'haproxy':
                assert_that(ext['pxs'], equal_to(1))
            if header_dimension_env in ['', 'prod']:
                assert_keys_not_exist(ext, 'pxe')
            if header_dimension_env == 'qa':
                assert_that(ext['pxe'], equal_to(1))
            if header_dimension_env == 'stage ':
                assert_that(ext['pxe'], equal_to(2))

            r_url = get(nurl.replace('${AUCTION_PRICE}', '0.67').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)



    @allure.feature('real-time notification')
    @allure.tag('normal')
    @allure.story('PBJ-4404 [HAProxy][jaeger] Add notification ext with proxy & proxyenv flag')
    @allure.description('Verify X-Source, X-Env add in request header')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.1'])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('header_dimension_source', ['', 'haproxy', 'akamai'])
    @pytest.mark.parametrize('header_dimension_env', ['', 'qa', 'stage', 'prod'])
    def test_real_time_header_source_add_in_url_02(self, pub_app_id, placement, sdk_v, partner, header_dimension_source,
                                                header_dimension_env):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, no_pre_cache_token=False,
                                                source=header_dimension_source, x_env=header_dimension_env,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            nurl = response_payload['seatbid'][0]['bid'][0]['nurl']
            ext = decode_ext(url=nurl)

            if header_dimension_source in ['', 'akamai']:
                assert_keys_not_exist(ext, 'pxs')
            if header_dimension_source == 'haproxy':
                assert_that(ext['pxs'], equal_to(1))
            if header_dimension_env in ['', 'prod']:
                assert_keys_not_exist(ext, 'pxe')
            if header_dimension_env == 'qa':
                assert_that(ext['pxe'], equal_to(1))
            if header_dimension_env == 'stage ':
                assert_that(ext['pxe'], equal_to(2))

            r_url = get(nurl.replace('${AUCTION_PRICE}', '0.67').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
