import pytest
import allure

from http import HTTPStatus

from data import request_payload, response_schema
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('HBP Notifications')
class TestWinNotification(object):

    @pytest.fixture(scope="class", autouse=True)
    def get_jaeger_response_bid_token(self):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id())
        global ordinal_view_count
        ordinal_view_count = 7
        global bid_token
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        global super_token
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        global event_id
        event_id = jaeger_response['ads'][0]['ad_markup']['id']

    @allure.feature('hbp notifications')
    @allure.tag('smoke')
    @allure.story('win notification'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the NURL normal response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_nurl_normal_response(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']

            r_url = get(nurl.replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '5.6').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal')
    @allure.story('win notification'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the NURL error response, empty settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_nurl_response_empty_settlement_price(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']

            r_url = get(nurl.replace('${AUCTION_PRICE}', '').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'R_v0.34.0')
    @allure.story('PBJ-2192 HBP notification urls when no settlement price')
    @allure.description('Verify the NURL error response, invalid settlement price value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('param', ['${AUCTION_PRICE}', 'abcdefg123', ' '])
    def test_nurl_error_response(self, pub_app_id, param):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']

            r_url = get(nurl.replace('${AUCTION_PRICE}', param).replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            msg = 'Request invalid: convert settlement_price error with \'%s\'.' % param
            assert_that(response_payload_url['msg'], equal_to(msg))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'R_v0.34.0')
    @allure.story('PBJ-4400 [HAProxy][HBP] Read request header and add to metrics')
    @allure.description('Verify X-Source, X-Env add in request header')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('header_dimension_source', ['haproxy', 'akamai', ''])
    @pytest.mark.parametrize('header_dimension_env', ['qa', 'stage', 'prod', ''])
    def test_header_source_add_in_url(self, pub_app_id, header_dimension_source, header_dimension_env):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(Source=header_dimension_source,
                                                                                X_Env=header_dimension_env))
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(Source=header_dimension_source,
                                                                                    X_Env=header_dimension_env))
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            nurl = bid_info['nurl']
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
        # Verify record x_source and x_env in 'ssp_scrat_notification_total' metric after send notification.

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4516 high Min_bid_to_win price')
    @allure.description(
        'Verify User Scenario II: Meister losses on HBP Auction, Meister will receive loss notification:'
        ' settlement_price<=hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_win_notification_on_hbp_auction_w_o_burl_01_meister(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb='60adc79dfb70f80016e36884,6246e6b95890c35df3ee9822')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]

            nurl = bid_info['nurl']
            nurl = get(
                nurl.replace('${AUCTION_PRICE}', '0.01').replace(hbp_ssl_host, hbp_host)
                    .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check rtb id is 60adc79dfb70f80016e36884
            # verifiy krakn-int2 will receive log:
            # Got notifications:Got notifications: "msg":"Won on ,  at 89.000000!"
            # lo1 will also receive the lurl:
            # "Got notifications: /lurl?mbtw=89.000000000&exbtw=&exbtwv="}
            # "Got notifications: /lurl?mbtw=89.000000000&exbtw=0.010000000&exbtwv=89.000000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4612 Look into LO side questions about win notification')
    @allure.description('Verify the auction id fix on win notification url for precache mode with v2 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_win_notification_precache_fix_1(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_price=${EX_AUCTION_PRICE}&auction_id=${AUCTION_ID}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' % l_nurl
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, ads_debug='jaeger',
                           test_device_id=gen_device_id(), sdk_v=sdk_v, hb=True,
                           override_bid_response_any=override_bid_response_any,
                           rtb=ext_non_test_mode_liftoff_01)

        if info['is_hbp_responded_200']:
            ads_response_payload = info['ads_response']
            hbp_response_payload = info['hbp_response']
            bid_info = hbp_response_payload['seatbid'][0]['bid'][0]
            ads_response_event_id = ads_response_payload['ads'][0]['ad_markup']['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (ads_response_event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl.replace('${AUCTION_ID}', ads_response_event_id)))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /nurl?price=98.000000000&ex_price=&auction_id=632ac1c6ffd35d35adb4e421"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description('Verify new macros are added for win notification url v2 token)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_win_notification_ex_auction_01(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"' %(l_nurl)

        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, ads_debug='jaeger',
                           test_device_id=gen_device_id(), sdk_v=sdk_v, hb=True,
                           override_bid_response_any=override_bid_response_any,
                           rtb=ext_non_test_mode_liftoff_01)

        if info['is_hbp_responded_200']:
            ads_response_payload = info['ads_response']
            hbp_response_payload = info['hbp_response']
            bid_info = hbp_response_payload['seatbid'][0]['bid'][0]
            ads_response_event_id = ads_response_payload['ads'][0]['ad_markup']['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (ads_response_event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_nurl'], equal_to(l_nurl.replace('${AUCTION_ID}', ads_response_event_id)))
            nurl = bid_info['nurl']
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '10')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /nurl?price=98.000000000&ex_auction_price=10.000000000&ex_auction_price_v=13.513513514&partner=max"}
