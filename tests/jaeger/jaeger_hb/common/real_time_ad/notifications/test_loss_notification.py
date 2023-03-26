import pytest
import allure

from http import HTTPStatus

from data import request_payload, response_schema
from utils.behaviors import request_ads_ios, post_hbp_request, request_hbp, request_hbp_with_real_time_token, \
    get_bid_request_obj_from_jaeger_explain, get_bid_request_obj_from_hbp_explain
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('HBP external Notifications')
class TestExtLossNotification(object):

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario I: LO losses on Jaeger Auction, LO will receive loss notification')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['max'])
    def test_loss_notification_on_jaeger_auction(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            pass
            # check rtb id is 6246e6b95890c35df3ee9822
            # verifiy krakn-lo1 will receive log: Got notifications: /lurl?mbtw=98.000000000&exbtw=&exbtwv="}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario II: LO losses on HBP Auction, LO will receive loss notification:'
                        ' settlement_price<=hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_loss_notification_on_hbp_auction_w_o_burl_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']
            lurl = get(
                lurl.replace('${AUCTION_PRICE}', '0.5').replace('${AUCTION_LOSS}', '1').replace(hbp_ssl_host, hbp_host)
                .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # verifiy krakn-lo will receive log:
            # Got notifications: /lurl?mbtw=98.000000000&exbtw=0.500000000&exbtwv=98.000000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4516 high Min_bid_to_win price')
    @allure.description('Verify the max value of min_bid_to_win')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_loss_notification_on_hbp_auction_w_o_burl_11(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification,
                                               )
        if info['is_hbp_responded_200']:
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
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario II: LO losses on HBP Auction, LO will receive loss notification:'
                        ' settlement_price>hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_loss_notification_on_hbp_auction_w_o_burl_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']
            lurl = get(
                lurl.replace('${AUCTION_PRICE}', '100').replace('${AUCTION_LOSS}', '1').replace(hbp_ssl_host, hbp_host)
                .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # verifiy krakn-lo will receive log:
            # Got notifications: Got notifications: /lurl?mbtw=98.000000000&exbtw=100.000000000&exbtwv=144.927536232"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario III: LO losses on HBP Auction, LO will receive loss notification:'
                        ' settlement_price<=hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_loss_notification_on_hbp_auction_w_burl_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']
            lurl = get(lurl.replace('${AUCTION_PRICE}', '0.5').replace('${AUCTION_LOSS}', '1').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # verifiy krakn-lo will receive log:
            # Got notifications: /lurl?mbtw=98.000000000&exbtw=0.500000000&exbtwv=98.000000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario III: LO losses on HBP Auction, LO will receive loss notification:'
                        ' settlement_price>hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_loss_notification_on_hbp_auction_w_burl_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']
            lurl = get(lurl.replace('${AUCTION_PRICE}', '100').replace('${AUCTION_LOSS}', '1').replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # verifiy krakn-lo will receive log:
            # Got notifications: Got notifications: /lurl?mbtw=98.000000000&exbtw=100.000000000&exbtwv=144.927536232"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify admob external notification when settlement_price<=hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_loss_notification_on_hbp_auction_for_admob_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False, admob_status_code=79,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            request_payload = info['hbp_request']
            request_headers = info['hbp_request_headers']
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

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # Got notifications: /lurl?mbtw=98.000000000&exbtw=0.710000000&exbtwv=98.000000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify admob external notification when settlement_price > hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_loss_notification_on_hbp_auction_for_admob_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False, admob_status_code=79,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            request_payload = info['hbp_request']
            request_headers = info['hbp_request_headers']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                }
            }
            exmbtw = {
                "minimum_bid_to_win": 0.9
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)
            request_payload.get("ext").get("bid_feedback")[0].update(exmbtw)

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # Got notifications: /lurl?mbtw=98.000000000&exbtw=0.900000000&exbtwv=110.250000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario I: LO losses on Jaeger Auction, LO will receive loss notification')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_loss_notification_on_jaeger_auction_for_meister(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, ip=fr_ip,
                                                rtb=non_test_mode_kraken_int_mixed_rtb_ids)
        if info['is_hbp_responded_200']:
            pass
            # check rtb id is 6246e6b95890c35df3ee9822
            # verifiy krakn-lo1 will receive log: Got notifications: /lurl?mbtw=98.000000000&exbtw=&exbtwv="}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario II: LO losses on HBP Auction, LO will receive loss notification:'
                        ' settlement_price<=hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_loss_notification_on_hbp_auction_w_o_burl_01(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']
            lurl = get(
                lurl.replace('${AUCTION_PRICE}', '0.5').replace('${AUCTION_LOSS}', '1').replace(hbp_ssl_host, hbp_host)
                    .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # verifiy krakn-lo will receive log:
            # Got notifications: /lurl?mbtw=98.000000000&exbtw=0.500000000&exbtwv=98.000000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4115 Support external notification on Real-time mode')
    @allure.description('Verify User Scenario II: LO losses on HBP Auction, LO will receive loss notification:'
                        ' settlement_price>hbp price')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_old])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['adtiming'])
    def test_loss_notification_on_hbp_auction_w_o_burl_02(self, pub_app_id, placement, sdk_v, partner):
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=False,
                                                rtb=ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            lurl = bid_info['lurl']
            lurl = get(
                lurl.replace('${AUCTION_PRICE}', '100').replace('${AUCTION_LOSS}', '1').replace(hbp_ssl_host, hbp_host)
                    .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # verifiy krakn-lo will receive log:
            # Got notifications: Got notifications: /lurl?mbtw=98.000000000&exbtw=100.000000000&exbtwv=144.927536232"}

    # @allure.feature('external Notifications')
    # @allure.tag('normal')
    # @allure.story('PBJ-4523 Support external notification on Real-time mode')
    # @allure.description('Verify User Scenario I: LO losses on Jaeger Auction, LO will receive loss notification')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # @pytest.mark.parametrize('partner', ['adtiming'])
    # def test_loss_notification_on_jaeger_auction_meister(self, pub_app_id, placement, sdk_v, partner):
    #
    #     info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
    #                                             placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
    #                                             no_pre_cache_token=True, explain=True,
    #                                             rtb='60adc79dfb70f80016e36884,6246e6b95890c35df3ee9822')
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         bid_info = response_payload['seatbid'][0]['bid'][0]
    #         bid_id = bid_info['id']
    #         pass
    #         # check rtb id is 6246e6b95890c35df3ee9822
    #         # verifiy krakn-lo1 will receive log: Got notifications: /lurl?mbtw=98.000000000&exbtw=&exbtwv="}
    #
    # @allure.feature('external Notifications')
    # @allure.tag('normal')
    # @allure.story('PBJ-4115 Support external notification on Real-time mode')
    # @allure.description('Verify admob external notification when settlement_price > hbp price')
    # @allure.severity('normal')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    # @pytest.mark.parametrize('partner', ['admob'])
    # def test_loss_notification_on_hbp_auction_for_admob_meister(self, pub_app_id, placement, sdk_v, partner):
    #     info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
    #                                             placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
    #                                             no_pre_cache_token=True, explain=True, admob_status_code=79,
    #                                             rtb='60adc79dfb70f80016e36884,6246e6b95890c35df3ee9822')
    #     if info['is_hbp_responded_200']:
    #         response_payload = info['hbp_response']
    #         request_payload = info['hbp_request']
    #         request_headers = info['hbp_request_headers']
    #         bid_info = response_payload['seatbid'][0]['bid'][0]
    #         event_token = bid_info['ext']['event_notification_token']['payload']
    #         token_obj = {
    #             "event_notification_token": {
    #                 "payload": event_token
    #             }
    #         }
    #         exmbtw = {
    #             "minimum_bid_to_win": 0.9
    #         }
    #         request_payload.get("ext").get("bid_feedback")[0].update(token_obj)
    #         request_payload.get("ext").get("bid_feedback")[0].update(exmbtw)
    #
    #         r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
    #         assert_response_status_code_in(r.status_code, HTTPStatus.OK)
    #         # check rtb id is 624676875890c35df3ee981a
    #         # Got notifications: /lurl?mbtw=98.000000000&exbtw=0.900000000&exbtwv=110.250000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4612 Look into LO side questions about win notification')
    @allure.description('Verify the auction id fix on loss notification url for admob realtime mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_loss_notification_fix_1(self, pub_app_id, placement, sdk_v, partner):
        # mock lurl
        l_lurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?mbtw=${MIN_BID_TO_WIN}&exbtw=${EX_MIN_BID_TO_WIN}&exbtwv=${EX_MIN_BID_TO_WIN_V}&auction_id=${AUCTION_ID}"
        override_bid_response_any = 'seatbid.0.bid.0.lurl@"%s"' % (l_lurl)
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, admob_status_code=79,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            event_id = response_payload['ext']['debug']['auction_result']['id']
            # check nurl has been writen to redis
            checker_response = post(hbp_checker_qa % (event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_lurl'], equal_to(l_lurl.replace('${AUCTION_ID}', event_id)))
            request_payload = info['hbp_request']
            request_headers = info['hbp_request_headers']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_token = bid_info['ext']['event_notification_token']['payload']
            token_obj = {
                "event_notification_token": {
                    "payload": event_token
                }
            }
            request_payload.get("ext").get("bid_feedback")[0].update(token_obj)

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /lurl?mbtw=98.000000000&exbtw=1.090000000&exbtwv=98.000000000&auction_id=632ac1c6ffd35d35adb4e421"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4612 Look into LO side questions about win notification')
    @allure.description('Verify the auction id fix on loss notification url for realtime mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_loss_notification_fix_2(self, pub_app_id, placement, sdk_v, partner):
        # mock lurl
        l_lurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?mbtw=${MIN_BID_TO_WIN}&exbtw=${EX_MIN_BID_TO_WIN}&exbtwv=${EX_MIN_BID_TO_WIN_V}&auction_id=${AUCTION_ID}"
        override_bid_response_any = 'seatbid.0.bid.0.lurl@"%s"' % l_lurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            # check lurl has been writen to redis
            checker_response = post(hbp_checker_qa % (bid_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_lurl'], equal_to(l_lurl.replace('${AUCTION_ID}', bid_id)))
            lurl = bid_info['lurl']
            lurl = get(lurl.replace('${AUCTION_LOSS}', '1').replace('${AUCTION_MBR}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /lurl?mbtw=98.000000000&exbtw=1.090000000&exbtwv=98.000000000&auction_id=632ac1c6ffd35d35adb4e421"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-4612 Look into LO side questions about win notification')
    @allure.description('Verify the auction id fix on loss notification url for realtime mode with v3 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_multi_cache_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_loss_notification_fix_3(self, pub_app_id, placement, sdk_v, partner):
        # mock lurl
        l_lurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?mbtw=${MIN_BID_TO_WIN}&exbtw=${EX_MIN_BID_TO_WIN}&exbtwv=${EX_MIN_BID_TO_WIN_V}&auction_id=${AUCTION_ID}"
        override_bid_response_any = 'seatbid.0.bid.0.lurl@"%s"' % l_lurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, ads_debug='jaeger',
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            ads_response_payload = info['ads_response']
            hbp_response_payload = info['hbp_response']
            bid_info = hbp_response_payload['seatbid'][0]['bid'][0]
            event_id = ads_response_payload['ads'][0]['ad_markup']['id']
            # check lurl has been writen to redis
            checker_response = post(hbp_checker_qa % (event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_lurl'], equal_to(l_lurl.replace('${AUCTION_ID}', event_id)))
            lurl = bid_info['lurl']
            lurl = get(lurl.replace('${AUCTION_LOSS}', '1').replace('${AUCTION_MBR}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /lurl?mbtw=98.000000000&exbtw=1.090000000&exbtwv=98.000000000&auction_id=632ac1c6ffd35d35adb4e421"}


    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for loss notification url for realtime traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_loss_notification_ex_auction_01(self, pub_app_id, placement, sdk_v, partner):
        # mock lurl
        l_lurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?mbtw=${MIN_BID_TO_WIN}&ex_auction_mbtw=${EX_AUCTION_MIN_TO_WIN}&ex_auction_mbtwv=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}&hbPrice=${EX_BID_PRICE}"

        override_bid_response_any = 'seatbid.0.bid.0.price@3|||seatbid.0.bid.0.lurl@"%s"' % l_lurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            # check lurl has been writen to redis
            checker_response = post(hbp_checker_qa % (bid_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_lurl'], equal_to(l_lurl.replace('${AUCTION_ID}', bid_id)))
            lurl = bid_info['lurl']
            lurl = get(lurl.replace('${AUCTION_LOSS}', '1').replace('${AUCTION_MBR}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /lurl?mbtw=3.000000000&ex_auction_mbtw=2.100000000&ex_auction_mbtwv=3.000000000&partner=max&hbPrice=2.100000000"}

    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for loss notification url for realtime traffic')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['admob'])
    def test_real_time_loss_notification_ex_auction_02(self, pub_app_id, placement, sdk_v, partner):
        l_lurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?mbtw=${MIN_BID_TO_WIN}&ex_auction_mbtw=${EX_AUCTION_MIN_TO_WIN}&ex_auction_mbtwv=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}&hbPrice=${EX_BID_PRICE}"

        override_bid_response_any = 'seatbid.0.bid.0.lurl@"%s"' % (l_lurl)
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=True, explain=True, admob_status_code=79,
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            request_payload = info['hbp_request']
            request_headers = info['hbp_request_headers']
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

            r = post_hbp_request(hbp_admob_endpoint_qa, json=request_payload, headers=request_headers)
            assert_response_status_code_in(r.status_code, HTTPStatus.OK)
            # check rtb id is 624676875890c35df3ee981a
            # {"level":"info","msg":"Got notifications: /lurl?mbtw=158.000000000&ex_auction_mbtw=0.710000000&ex_auction_mbtwv=158.000000000&partner=admob&hbPrice=113.760000000"}


    @allure.feature('external Notifications')
    @allure.tag('normal')
    @allure.story('PBJ-5323 Support specified macro for Accelerate in external auction')
    @allure.description(
        'Verify new macros are added for loss notification url for realtime traffic(with v2 token)')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_pre_cache_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('partner', ['max'])
    def test_real_time_loss_notification_ex_auction_03(self, pub_app_id, placement, sdk_v, partner):
        # mock lurl
        l_lurl = "http://kraken-lo-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?mbtw=${MIN_BID_TO_WIN}&ex_auction_mbtw=${EX_AUCTION_MIN_TO_WIN}&ex_auction_mbtwv=${EX_AUCTION_MIN_TO_WIN_V}&partner=${MEDIATOR_NAME}&hbPrice=${EX_BID_PRICE}"
        override_bid_response_any = 'seatbid.0.bid.0.lurl@"%s"' % l_lurl
        info = request_hbp_with_real_time_token(partner, ordinal_view=19, pub_app_id=pub_app_id,
                                                placement_ref_id=placement, test_device_id=gen_device_id(), sdk_v=sdk_v,
                                                no_pre_cache_token=False, explain=True, ads_debug='jaeger',
                                                override_bid_response_any=override_bid_response_any,
                                                rtb=ext_non_test_mode_liftoff_01)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_id = bid_info['id']
            ads_response_payload = info['ads_response']
            hbp_response_payload = info['hbp_response']
            bid_info = hbp_response_payload['seatbid'][0]['bid'][0]
            ads_response_event_id = ads_response_payload['ads'][0]['ad_markup']['id']
            # check lurl has been writen to redis
            checker_response = post(hbp_checker_qa % (ads_response_event_id, "notice"), json="")
            assert_response_status_code(checker_response.status_code, HTTPStatus.OK)
            checker_response = checker_response.json()
            assert_that(checker_response['l_lurl'], equal_to(l_lurl.replace('${AUCTION_ID}', bid_id)))
            lurl = bid_info['lurl']
            lurl = get(lurl.replace('${AUCTION_LOSS}', '1').replace('${AUCTION_MBR}', '1')
                       .replace(hbp_ssl_host, hbp_host).replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(lurl.status_code, HTTPStatus.OK)
            # check the rtb id
            # verify the kraken-lo pod will receive log like:
            # {"level":"info","msg":"Got notifications: /lurl?mbtw=158.000000000&ex_auction_mbtw=116.920000000&ex_auction_mbtwv=158.000000000&partner=max&hbPrice=116.920000000"}
