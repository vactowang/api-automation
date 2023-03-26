import pytest
import allure

from http import HTTPStatus

from data import request_payload, response_schema
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('HBP Notifications')
class TestLossNotification(object):

    @pytest.fixture(scope="class", autouse=True)
    def get_jaeger_response_bid_token(self):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id(),rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
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
    @allure.story('loss notification'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the LURL normal response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_lurl_normal_response(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers(rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification))

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']

            r_url = get(lurl.replace('${AUCTION_LOSS}', '1')
                        .replace('${AUCTION_MBR}', '100').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal')
    @allure.story('loss notification'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the LURL error response, empty loss reason value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_lurl_response_empty_value_1(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']

            r_url = get(lurl.replace('${AUCTION_LOSS}', '')
                        .replace('${AUCTION_MBR}', '5.6').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal')
    @allure.story('loss notification'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the LURL error response, empty auction mbr value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_lurl_response_empty_value_2(self, pub_app_id):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']

            r_url = get(lurl.replace('${AUCTION_LOSS}', '1')
                        .replace('${AUCTION_MBR}', '').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()
            assert_that(response_payload_url['msg'], equal_to('ok'))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'R_v0.34.0')
    @allure.story('PBJ-2192 HBP notification urls when no settlement price'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the LURL error response, invalid loss reason value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('param', ['${AUCTION_LOSS}', 'abcdefg123', ' '])
    def test_lurl_error_response_1(self, pub_app_id, param):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']

            r_url = get(lurl.replace('${AUCTION_LOSS}', param)
                        .replace('${AUCTION_MBR}', '5.6').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            msg = 'Request invalid: convert loss_reason error with \'%s\'.' % param
            assert_that(response_payload_url['msg'], equal_to(msg))
            assert_that(response_payload_url['code'], equal_to(200))

    @allure.feature('hbp notifications')
    @allure.tag('normal', 'R_v0.34.0')
    @allure.story('PBJ-2192 HBP notification urls when no settlement price'
                  'PBJ-3741 Let Scrat handle the HBP notification event')
    @allure.description('Verify the LURL error response, invalid auction mbr value')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('param', ['${AUCTION_MBR}', 'abcdefg123', ' '])
    def test_lurl_error_response_2(self, pub_app_id, param):
        test_ifa = gen_device_id(36)
        req = request_payload.hbp_max(pub_app_id, common_test_placement, ifa=test_ifa, bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())
        if r.status_code == HTTPStatus.NO_CONTENT:
            r = post_hbp_request(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']

            r_url = get(lurl.replace('${AUCTION_LOSS}', '1')
                        .replace('${AUCTION_MBR}', param).replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r_url.status_code, HTTPStatus.OK)
            response_payload_url = r_url.json()

            msg = 'Request invalid: convert auction_mbr error with \'%s\'.' % param
            assert_that(response_payload_url['msg'], equal_to(msg))
            assert_that(response_payload_url['code'], equal_to(200))
    #
    # @allure.feature('external Notifications')
    # @allure.tag('normal')
    # @allure.story('PBJ-4516 high Min_bid_to_win price')
    # @allure.description('Verify User Scenario I: Meister losses on Jaeger Auction, Meister will receive loss notification')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    # @pytest.mark.parametrize('partner', ['max'])
    # def test_loss_notification_on_jaeger_auction_meister(self, pub_app_id, placement, sdk_v, partner):
    #     '''
    #
    #     meister: 60adc79dfb70f80016e36884:89
    #     lo: 624676875890c35df3ee981a: 98
    #     lo1: 6246e6b95890c35df3ee9822: 1
    #     '''
    #     info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
    #                        sdk_v=sdk_v, rtb='60adc79dfb70f80016e36884,624676875890c35df3ee981a')
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            #  check rtb id is 60adc79dfb70f80016e36884
            #  verifiy krakn-int2 will receive log: Got notifications: /lurl?mbtw=98.000000000&exbtw=&ebp="}

    # @allure.feature('external Notifications')
    # @allure.tag('normal')
    # @allure.story('PBJ-4516 high Min_bid_to_win price')
    # @allure.description('Verify User Scenario II: Meister losses on HBP Auction, Meister will receive loss notification:'
    #                     ' settlement_price<=hbp price')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # @pytest.mark.parametrize('partner', ['adtiming'])
    # def test_loss_notification_on_hbp_auction_w_o_burl_01_meister(self, pub_app_id, placement, sdk_v, partner):
    #     info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                        test_device_id=gen_device_id(),
    #                        sdk_v=sdk_v, rtb='60adc79dfb70f80016e36884,6246e6b95890c35df3ee9822')
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
    #         response_payload = info['hbp_response']
    #         bid_info = response_payload['seatbid'][0]['bid'][0]
    #         lurl = bid_info['lurl']
    #         lurl = get(
    #             lurl.replace('${AUCTION_PRICE}', '100').replace('${AUCTION_LOSS}', '1').replace(hbp_ssl_host, hbp_host)
    #                 .replace(scrat_notification_host_ssl, scrat_notification_host))
    #         assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check rtb id is 60adc79dfb70f80016e36884
            # verifiy krakn-int2 will receive log:
            # Got notifications:Got notifications: /lurl?mbtw=89.000000000&exbtw=0.010000000&ebp=0.800000000"}
            # lo1 will also receive the lurl:
            # "Got notifications: /lurl?mbtw=89.000000000&exbtw=&exbtwv="}
            # "Got notifications: /lurl?mbtw=89.000000000&exbtw=0.010000000&exbtwv=89.000000000"}

    #
    # @allure.feature('external Notifications')
    # @allure.tag('normal')
    # @allure.story('PBJ-4516 high Min_bid_to_win price')
    # @allure.description('Verify admob external notification when settlement_price<=hbp price')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # @pytest.mark.parametrize('partner', ['admob'])
    # def test_loss_notification_on_hbp_auction_w_o_burl_admob_meister(self, pub_app_id, placement, sdk_v, partner):
    #     info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                        test_device_id=gen_device_id(),
    #                        sdk_v=sdk_v, rtb='60adc79dfb70f80016e36884,6246e6b95890c35df3ee9822')
    #     if info['is_hbp_responded_200']:
    #
    #         response_payload = info['hbp_response']
    #         request_payload = info['hbp_request']
    #         bid_info = response_payload['seatbid'][0]['bid'][0]
    #         event_token = bid_info['ext']['event_notification_token']['payload']
    #         token_obj = {
    #             "event_notification_token": {
    #                 "payload": event_token
    #             }
    #         }
    #         exmbtw = {
    #             "minimum_bid_to_win": 0.71
    #         }
    #         request_payload.get("ext").get("bid_feedback")[0].update(token_obj)
    #         request_payload.get("ext").get("bid_feedback")[0].update(exmbtw)
    #
    #         r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=platform_headers())
    #         assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check rtb id is 60adc79dfb70f80016e36884
            # Got notifications: /lurl?mbtw=89.000000000&exbtw=0.710000000&ebp=0.800000000"}
            # check rtb id is: 6246e6b95890c35df3ee9822
            # Got notifications: /lurl?mbtw=89.000000000&exbtw=&exbtwv="}
            # /lurl?mbtw=89.000000000&exbtw=0.710000000&exbtwv=89.000000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4516 high Min_bid_to_win price')
    @allure.description('Verify User Scenario I: LO losses on Jaeger Auction, LO will receive loss notification')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_loss_notification_on_jaeger_auction(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            #  check rtb id is 6246e6b95890c35df3ee9822
            #  verifiy krakn-lo1 will receive log: Got notifications: /lurl?mbtw=98.000000000&exbtw=&exbtwv="}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4516 high Min_bid_to_win price')
    @allure.description('Verify User Scenario II: LO losses on HBP Auction, LO will receive loss notification:'
                        ' settlement_price<=hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_loss_notification_on_hbp_auction_w_o_burl_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']
            lurl = get(
                lurl.replace('${AUCTION_PRICE}', '0.01').replace('${AUCTION_LOSS}', '1').replace(hbp_ssl_host, hbp_host)
                    .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # verifiy krakn-lo will receive log:
            # Got notifications: /lurl?mbtw=98.000000000&exbtw=0.010000000&exbtwv=98.000000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4516 high Min_bid_to_win price')
    @allure.description('Verify the max value of min_bid_to_win')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_loss_notification_on_hbp_auction_w_o_burl_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']
            lurl = get(
                lurl.replace('${AUCTION_PRICE}', '100').replace('${AUCTION_LOSS}', '1').replace(hbp_ssl_host, hbp_host)
                    .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)

            # check rtb id is 624676875890c35df3ee981a
            # check when (HB Settlement price * Adx Settlement Price)/(HB bid price) > max ((10*HB settlement price, 10*Jaeger settlement price))
            # will not display exbtwv
            # verifiy krakn-lo will receive log: (mock bflat bid price =0.01)
            # Got notifications: /lurl?mbtw=98.000000000&exbtw=100.000000000&exbtwv="}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4516 high Min_bid_to_win price')
    @allure.description('Verify admob external notification when settlement_price<=hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_loss_notification_on_hbp_auction_w_o_burl_admob_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:

            response_payload = info['hbp_response']
            request_payload = info['hbp_request']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                }
            }
            exmbtw = {
                "minimum_bid_to_win": 0.71
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)
            request_payload.get("ext").get("bid_feedback")[0].update(exmbtw)

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=platform_headers())
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # Got notifications: /lurl?mbtw=98.000000000&exbtw=0.710000000&exbtwv=98.000000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4516 high Min_bid_to_win price')
    @allure.description('Verify admob external notification when settlement_price > hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_loss_notification_on_hbp_auction_w_o_burl_admob_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v=sdk_v, rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:

            response_payload = info['hbp_response']
            request_payload = info['hbp_request']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                }
            }
            exmbtw = {
                "minimum_bid_to_win": 100
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)
            request_payload.get("ext").get("bid_feedback")[0].update(exmbtw)

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=platform_headers())
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # check when (HB Settlement price * Adx Settlement Price)/(HB bid price) > max ((10*HB settlement price, 10*Jaeger settlement price))
            # will not display exbtwv
            # verifiy krakn-lo will receive log: (mock bflat bid price =0.01)
            # Got notifications: /lurl?mbtw=98.000000000&exbtw=100.000000000&exbtwv="}

    # @allure.feature('external Notifications')
    # @allure.tag('normal')
    # @allure.story('PBJ-4516 high Min_bid_to_win price')
    # @allure.description('Verify admob external notification when settlement_price > hbp price')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # @pytest.mark.parametrize('partner', ['admob'])
    # def test_loss_notification_on_hbp_auction_w_o_burl_admob_meister_02(self, pub_app_id, placement, sdk_v, partner):
    #     info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
    #                        test_device_id=gen_device_id(),
    #                        sdk_v=sdk_v, rtb='60adc79dfb70f80016e36884,6246e6b95890c35df3ee9822')
    #     if info['is_hbp_responded_200']:
    #
    #         response_payload = info['hbp_response']
    #         request_payload = info['hbp_request']
    #         bid_info = response_payload['seatbid'][0]['bid'][0]
    #         event_token = bid_info['ext']['event_notification_token']['payload']
    #         token_obj = {
    #             "event_notification_token": {
    #                 "payload": event_token
    #             }
    #         }
    #         exmbtw = {
    #             "minimum_bid_to_win": 100
    #         }
    #         request_payload.get("ext").get("bid_feedback")[0].update(token_obj)
    #         request_payload.get("ext").get("bid_feedback")[0].update(exmbtw)
    #
    #         r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=platform_headers())
    #         assert_response_status_code_in(r.status_code, HTTPStatus.OK)

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4612 Look into LO side questions about win notification')
    @allure.description('Verify the auction id fix on loss notification url for precache mode with v2 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_loss_notification_precache_fix_1(self, pub_app_id, placement, sdk_v, partner):
        # mock nurl
        l_lurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?mbtw=${MIN_BID_TO_WIN}&exbtw=${EX_MIN_BID_TO_WIN}&exbtwv=${EX_MIN_BID_TO_WIN_V}&auction_id=${AUCTION_ID}"
        override_bid_response_any = 'seatbid.0.bid.0.lurl@"%s"' % l_lurl
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, ads_debug='jaeger',
                           test_device_id=gen_device_id(), sdk_v=sdk_v, hb=True,
                           override_bid_response_any=override_bid_response_any,
                           rtb=ext_non_test_mode_liftoff_01)

        if info['is_hbp_responded_200']:
            ads_response_payload = info['ads_response']
            hbp_response_payload = info['hbp_response']
            bid_info = hbp_response_payload['seatbid'][0]['bid'][0]
            ads_response_event_id = ads_response_payload['ads'][0]['ad_markup']['id']
            # check lurl has been writen to redis
            checker_response = post(hbp_checker_qa % (ads_response_event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_lurl'], equal_to(l_lurl.replace('${AUCTION_ID}', ads_response_event_id)))
            lurl = bid_info['lurl']
            lurl = get(lurl.replace('${AUCTION_LOSS}', '1').replace('${AUCTION_MBR}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check the rtb id verify the kraken-lo pod will receive log like: {"level":"info","msg":"Got
            # notifications: /lurl?mbtw=98.000000000&exbtw=1.090000000&exbtwv=98.000000000&auction_id
            # =632ac1c6ffd35d35adb4e421"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description('Verify new macros are added for loss notification url for precache mode with v2 token:hb request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_loss_notification_ex_auction_1(self, pub_app_id, placement, sdk_v, partner):
        # mock lurl
        l_lurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?mbtw=${" \
                 "MIN_BID_TO_WIN}&ex_auction_mbtw=${EX_AUCTION_MIN_TO_WIN}&ex_auction_mbtwv=${" \
                 "EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}&hbPrice=${EX_BID_PRICE} "
        override_bid_response_any = 'seatbid.0.bid.0.price@3|||seatbid.0.bid.0.lurl@"%s"' % l_lurl
        info = request_hbp(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement, ads_debug='jaeger',
                           test_device_id=gen_device_id(), sdk_v=sdk_v, hb=True,
                           override_bid_response_any=override_bid_response_any,
                           rtb=ext_non_test_mode_liftoff_01)

        if info['is_hbp_responded_200']:
            ads_response_payload = info['ads_response']
            hbp_response_payload = info['hbp_response']
            bid_info = hbp_response_payload['seatbid'][0]['bid'][0]
            ads_response_event_id = ads_response_payload['ads'][0]['ad_markup']['id']
            # check lurl has been writen to redis
            checker_response = post(hbp_checker_qa % (ads_response_event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_lurl'], equal_to(l_lurl.replace('${AUCTION_ID}', ads_response_event_id)))
            lurl = bid_info['lurl']
            lurl = get(lurl.replace('${AUCTION_LOSS}', '1').replace('${AUCTION_MBR}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /lurl?mbtw=3.000000000&ex_auction_mbtw=2.220000000&ex_auction_mbtwv=3.000000000&partner=max&hbPrice=2.220000000"}

