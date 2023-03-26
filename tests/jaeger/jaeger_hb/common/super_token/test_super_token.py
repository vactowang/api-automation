import pytest
import allure


from utils.behaviors import request_ads_ios, post_hbp_request
from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *



@allure.epic('HBP SUPER TOKEN')
class TestHBPSUPERTOKEN(object):

    @allure.feature('hbp invalid super token')
    @allure.tag('normal', 'v0.65.0')
    @allure.story('PBJ-3476 HBP - Add one nsr for invalid super token')
    @allure.description('Verify the response code is 204 when super token is null')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_super_token_is_null(self, pub_app_id, placement, sdk_v, partner):
        endpoint = get_hbp_partner_endpoint(partner)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=gen_device_id(),
                                          bid_token='')
        r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v))
        assert_that(r.status_code, equal_to(204))

    @allure.feature('hbp invalid super token')
    @allure.tag('normal', 'v0.65.0')
    @allure.story('PBJ-3476 HBP - Add one nsr for invalid super token')
    @allure.description('Verify the response code is 204 when super token is no version')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_super_token_no_version_1(self, pub_app_id, placement, sdk_v, partner):
        ads_response = request_ads_ios(pub_app_id, placement, test_ifa=test_device_id, sdk_v=sdk_v)
        ordinal_view_count = 7
        bid_token = ads_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        endpoint = get_hbp_partner_endpoint(partner)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=gen_device_id(),
                                          bid_token=super_token)
        r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v))
        assert_that(r.status_code, equal_to(204))

    @allure.feature('hbp invalid super token')
    @allure.tag('normal', 'v0.65.0')
    @allure.story('PBJ-3476 HBP - Add one nsr for invalid super token')
    @allure.description('Verify the response code is 204 when super token is no version')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_super_token_no_version_2(self, pub_app_id, placement, sdk_v, partner):
        ads_response = request_ads_ios(pub_app_id, placement, test_ifa=test_device_id, sdk_v=sdk_v)
        ordinal_view_count = 7
        bid_token = ads_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = ':'+base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        endpoint = get_hbp_partner_endpoint(partner)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=gen_device_id(),
                                          bid_token=super_token)
        r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v))
        assert_that(r.status_code, equal_to(204))


    @allure.feature('hbp invalid super token')
    @allure.tag('normal', 'v0.65.0')
    @allure.story('PBJ-3476 HBP - Add one nsr for invalid super token')
    @allure.description('Verify the response code is 204 when super token without colon')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_super_token_without_colon(self, pub_app_id, placement, sdk_v, partner):
        ads_response = request_ads_ios(pub_app_id, placement, test_ifa=test_device_id, sdk_v=sdk_v)
        ordinal_view_count = 7
        bid_token = ads_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = '2'+base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        endpoint = get_hbp_partner_endpoint(partner)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=gen_device_id(),
                                          bid_token=super_token)
        r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v))
        assert_that(r.status_code, equal_to(204))

    @allure.feature('hbp invalid super token')
    @allure.tag('normal', 'v0.65.0')
    @allure.story('PBJ-3868 HBP - Add a new NBR for empty token')
    @allure.description('Verify bid_nbr in hb transaction is 8 when bid token is null')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.2'])
    @pytest.mark.parametrize('partner', config['hb_partners'])
    def test_bid_nbr_for_no_bid_token(self, pub_app_id, placement, sdk_v, partner):
        ordinal_view_count = 7
        bid_tokens_with_ordinal_view_count = ':' + str(ordinal_view_count)
        super_token = '2:' + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        endpoint = get_hbp_partner_endpoint(partner)
        req = request_payload.hbp_partner(partner, pub_app_id, placement, ifa=gen_device_id(),
                                          bid_token=super_token)
        r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v))
        assert_that(r.status_code, equal_to(204))
