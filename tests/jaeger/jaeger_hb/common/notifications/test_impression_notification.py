import pytest
import allure

from http import HTTPStatus

from data import request_payload, response_schema
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('HBP Notifications')
class TestBillNotification(object):

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

    @allure.feature('external Notifications')
    @allure.tag('normal', 'v1.259.2')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for bill notification url for V2 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_ex_auction_mbtw_burl_01(self, pub_app_id, placement, sdk_v, partner):
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        l_burl = "https://review.free.beeceptor.com/burl?ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.burl@"%s"|||seatbid.0.bid.0.nurl@"%s"' % (l_burl, l_nurl)
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext_non_test_mode_liftoff_01, ads_debug='jaeger',
                           override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid_info = response_payload['seatbid'][0]['bid'][0]
            adm = json.loads(bid_info['adm'])
            nurl = bid_info['nurl']
            impression_url = adm['impression'][0]
            # send impression url directly:
            impression_url_1 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(impression_url_1.status_code, HTTPStatus.OK)
            # check notification,
            #/ burl?ex_auction_price = & ex_auction_price_v = 4.000000000 & partner = adtiming
            # send win notification
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)

            # send impression url again
            impression_url_2 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(impression_url_2.status_code, HTTPStatus.OK)
            # check notification,
            #/ burl?ex_auction_price = & ex_auction_price_v = 4.000000000 & partner = adtiming



    @allure.feature('external Notifications')
    @allure.tag('normal', 'v1.259.2')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for bill notification url for V2 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_ex_auction_mbtw_burl_02(self, pub_app_id, placement, sdk_v, partner):
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        l_burl = "https://review.free.beeceptor.com/burl?ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.burl@"%s"|||seatbid.0.bid.0.nurl@"%s"' % (l_burl, l_nurl)
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext_non_test_mode_liftoff_01, ads_debug='jaeger',
                           override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid_info = response_payload['seatbid'][0]['bid'][0]
            adm = json.loads(bid_info['adm'])
            nurl = bid_info['nurl']
            impression_url = adm['impression'][0]
            # send impression url directly:
            impression_url_1 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(impression_url_1.status_code, HTTPStatus.OK)
            # check notification,
            #/ burl?ex_auction_price = & ex_auction_price_v = 4.000000000 & partner = max
            # send win notification
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)

            # send impression url again
            impression_url_2 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(impression_url_2.status_code, HTTPStatus.OK)
            # check notification,
            #/ burl?ex_auction_price = 1.000000000 & ex_auction_price_v = 4.000000000 & partner = max


    @allure.feature('external Notifications')
    @allure.tag('normal', 'v1.259.2')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for bill notification url for V2 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_ex_auction_mbtw_burl_03(self, pub_app_id, placement, sdk_v, partner):
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        l_burl = "https://review.free.beeceptor.com/burl?ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.burl@"%s"|||seatbid.0.bid.0.nurl@"%s"' % (l_burl, l_nurl)
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext_non_test_mode_liftoff_01, ads_debug='jaeger',
                           override_bid_response_any=override_bid_response_any)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            bid_info = response_payload['seatbid'][0]['bid'][0]
            adm = json.loads(bid_info['ext']['sdk_rendered_ad']['rendering_data'])
            impression_url = adm['impression'][0]
            # send impression url directly:
            impression_url_1 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl,
                                                                                          scrat_notification_host))
            assert_response_status_code(impression_url_1.status_code, HTTPStatus.OK)
            # check notification,
            #/ burl?ex_auction_price = & ex_auction_price_v = 4.000000000 & partner = admob
            request_payload = info['hbp_request']
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                },
                "creative_status_code":1
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)
            burl = bid_info['burl']
            # send win notification

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=platform_headers())
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check SecondHighestPriceOnEX in redis
            # send impression url again
            impression_url_2 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl,
                                                                                          scrat_notification_host))
            assert_response_status_code(impression_url_2.status_code, HTTPStatus.OK)
            # check notification,
            # /burl?ex_auction_price=1.090000000&ex_auction_price_v=4.000000000&partner=admob