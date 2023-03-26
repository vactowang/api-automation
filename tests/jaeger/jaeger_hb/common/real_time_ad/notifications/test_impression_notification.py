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
    @allure.feature('external Notifications')
    @allure.tag('normal', 'v1.259.2')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for bill notification url for v3 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_real_time_ext_auction_burl_1(self, pub_app_id, placement, sdk_v, partner):
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        l_burl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/burl?ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.burl@"%s"|||seatbid.0.bid.0.nurl@"%s"' % (l_burl, l_nurl)
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb='6246e6b95890c35df3ee9822,5fd965d7323580001628bf72')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            adm = json.loads(bid_info['adm'])
            impression_url = adm['impression'][0]
            # send impression url directly:
            impression_url_1 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl,
                                                                                          scrat_notification_host))
            assert_response_status_code(impression_url_1.status_code, HTTPStatus.OK)
            nurl = bid_info['nurl']
            # send win notification
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '10')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check SecondHighestPriceOnEX in redis
            # send bill notification
            # send impression url again
            impression_url_2 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl,
                                                                                          scrat_notification_host))
            assert_response_status_code(impression_url_2.status_code, HTTPStatus.OK)
            # check notification,



    @allure.feature('external Notifications')
    @allure.tag('normal', 'v1.259.2')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for bill notification url for v3 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_ext_auction_burl_2(self, pub_app_id, placement, sdk_v, partner):
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        l_burl = "https://review.free.beeceptor.com/burl?ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.burl@"%s"|||seatbid.0.bid.0.nurl@"%s"' % (l_burl, l_nurl)
        override_bid_price = 'ext2:5.0'
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=mixed_non_test_mode_rtb_auction_mbtw,
                                                override_bid_price=override_bid_price)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            adm = json.loads(bid_info['adm'])
            impression_url = adm['impression'][0]
            # send impression url directly:
            impression_url_1 = get(impression_url.replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(impression_url_1.status_code, HTTPStatus.OK)
            # validate the mock serve can receive notification:                                                                              scrat_notification_host))
            # /burl?ex_auction_price=&ex_auction_price_v=5.000000000&partner=max
            nurl = bid_info['nurl']
            # send win notification
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '10').replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check SecondHighestPriceOnEX in redis
            # send bill notification
            # send impression url again
            impression_url_2 = get(impression_url.replace(scrat_notification_host_ssl,
                                                                                          scrat_notification_host))
            assert_response_status_code(impression_url_2.status_code, HTTPStatus.OK)
            # check notification,
            # validate the mock serve can receive notification:                                                                              scrat_notification_host))
            # /burl?ex_auction_price=10.000000000&amp&ex_auction_price_v=13.698630137&partner=max

    @allure.feature('external Notifications')
    @allure.tag('normal', 'v1.259.2')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for bill notification url for v3 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_ext_auction_burl_3(self, pub_app_id, placement, sdk_v, partner):
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        l_burl = "https://review.free.beeceptor.com/burl?ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.burl@"%s"|||seatbid.0.bid.0.nurl@"%s"' % (l_burl, l_nurl)
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, admob_status_code=1,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb='6246e6b95890c35df3ee9822,5fd965d7323580001628bf72')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            request_payload = info['hbp_request']
            request_headers = info['hbp_request_headers']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            adm = json.loads(bid_info['ext']['sdk_rendered_ad']['rendering_data'])
            impression_url = adm['impression'][0]
            # send impression url directly:
            impression_url_1 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl,
                                                                                          scrat_notification_host))
            assert_response_status_code(impression_url_1.status_code, HTTPStatus.OK)

            # check notification,
            #/burl?ex_auction_price=&ex_auction_price_v=98.000000000&partner=admob
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                }
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)
            # send win notification
            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # send impression url again
            impression_url_2 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl,
                                                                           scrat_notification_host))
            assert_response_status_code(impression_url_2.status_code, HTTPStatus.OK)
            # check notification,
            #/ burl?ex_auction_price = 1.090000000 & ex_auction_price_v = 98.000000000 & partner = admob

    @allure.feature('external Notifications')
    @allure.tag('normal', 'v1.259.2')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for bill notification url for v3 token(with v2 token)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_ext_auction_burl_4(self, pub_app_id, placement, sdk_v, partner):
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        l_burl = "https://review.free.beeceptor.com/burl?ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.burl@"%s"|||seatbid.0.bid.0.nurl@"%s"' % (l_burl, l_nurl)
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, ads_debug='jaeger',
                                                override_bid_response_any=override_bid_response_any,
                                                rtb='6246e6b95890c35df3ee9822,5fd965d7323580001628bf72')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            adm = json.loads(bid_info['adm'])
            impression_url = adm['impression'][0]
            # send impression url directly:
            impression_url_1 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl,
                                                                                          scrat_notification_host))
            assert_response_status_code(impression_url_1.status_code, HTTPStatus.OK)
            # validate mock server notification
            # /burl?ex_auction_price=&ex_auction_price_v=98.000000000&partner=max
            nurl = bid_info['nurl']
            # send win notification
            nurl = get(nurl.replace('${AUCTION_PRICE}', '1').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '10')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(nurl.status_code, HTTPStatus.OK)
            # check SecondHighestPriceOnEX in redis
            # send bill notification
            # send impression url again
            impression_url_2 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl,
                                                                                          scrat_notification_host))
            assert_response_status_code(impression_url_2.status_code, HTTPStatus.OK)
            # validate mock server notification
            #/ burl?ex_auction_price = 10.000000000 & ex_auction_price_v = 98.000000000 & partner = max


    @allure.feature('external Notifications')
    @allure.tag('normal', 'v1.259.2')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for bill notification url for v3 token(with v2 token)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_ext_auction_burl_5(self, pub_app_id, placement, sdk_v, partner):
        l_nurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/nurl?price=${AUCTION_PRICE}&ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        l_burl = "https://review.free.beeceptor.com/burl?ex_auction_price=${EX_AUCTION_MIN_TO_WIN}&ex_auction_price_v=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}"
        override_bid_response_any = 'seatbid.0.bid.0.burl@"%s"|||seatbid.0.bid.0.nurl@"%s"' % (l_burl, l_nurl)
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, admob_status_code=1,
                                                ads_debug='jaeger',
                                                override_bid_response_any=override_bid_response_any,
                                                rtb='6246e6b95890c35df3ee9822,5fd965d7323580001628bf72')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            request_payload = info['hbp_request']
            request_headers = info['hbp_request_headers']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            adm = json.loads(bid_info['ext']['sdk_rendered_ad']['rendering_data'])
            impression_url = adm['impression'][0]
            # send impression url directly:
            impression_url_1 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl,
                                                                                          scrat_notification_host))
            assert_response_status_code(impression_url_1.status_code, HTTPStatus.OK)
            # check notification,
            # /burl?ex_auction_price=&ex_auction_price_v=98.000000000&partner=admob
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                }
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)
            # send win notification
            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # send impression url again
            impression_url_2 = get(impression_url.replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl,
                                                                                          scrat_notification_host))
            assert_response_status_code(impression_url_2.status_code, HTTPStatus.OK)
            # check notification,
            #/ burl?ex_auction_price = 1.090000000 & ex_auction_price_v = 98.000000000 & partner = admob