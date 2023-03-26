import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import post_hbp_request, request_hb_win_notification, post_hbp_request_no_retry
from utils.common import *
from utils.assertions import *
from settings import *
import time


@allure.epic('HBP Max')
class TestMax(object):

    @allure.feature('ttl')
    @allure.tag('normal', 'R_v0.30.0')
    @allure.story('PBJ-2104 Event ID Win TTL')
    @allure.description('Verify that it will not auction again in 1 hour for specific pub')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.9', 'Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_no_auction_again(self, pub_app_id, placement, sdk_v):
        info = request_hb_win_notification('max', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                                           test_device_id=gen_device_id(), sdk_v=sdk_v)
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_max_endpoint_qa, json=req, headers=hbp_headers())

            assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('win ttl experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4208 Reduce the WinTTL for MAX')
    @allure.description('Verify max will enter the experiment and winTTL experiment Tag is added in bidtoken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1;Max'])
    def test_max_winTTL_experiment_01(self, pub_app_id, placement, sdk_v):
        """
        experiment setting:
        db.experiments.insert({
          "_id": ObjectId("628c4a47f31e79397580797b"),
          "name": "win_ttl",
          "mutual_id": "62849ee7d5cddc18beb8cad7",
          "allocate_strategy": "hash_device_id",
          "salt": "628c4a4f42ba066ee9827c22",
          "countries": [],
          "is_all_countries": true,
          "is_all_applications": true,
          "traffic_percentage": 10000,
          "scope": "jaeger",
          "start_date": ISODate("2019-03-01T00:00:00.000Z"),
          "end_date": ISODate("2099-12-31T23:59:59.999Z"),
          "enabled": true,
          "ext": {
                "partners": ["max"]
          },
          "buckets": [
            {
              "_id": ObjectId("628c4ad16fa1bba9c86f6f50"),
              "name": "15_mins",
              "weight": 25,
              "ext": {
                "minutes": 15
              }
            },
            {
              "_id": ObjectId("628c4b19ba9b2605c84cf642"),
              "name": "30_mins",
              "weight": 25,
              "ext": {
                "minutes": 30
              }
            },
            {
              "_id": ObjectId("628c4b1fa1c9d38be93fedaf"),
              "name": "45_mins",
              "weight": 25,
              "ext": {
                "minutes": 45
              }
            },
            {
              "_id": ObjectId("628c4b241f934b681eaefa11"),
              "name": "60_mins",
              "weight": 25,
              "ext": {
                "minutes": 60
              }
            }
          ],
          "app_whitelist": [],
          "placement_whitelist": []
        })
        """
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        # verify experiment info added in jaeger transaction & deliveriy
        # exp_to_bucket":"{\\"win_ttl\\":\\"X_mins\\"}
        response_payload = r.json()
        bid_token = response_payload['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(11)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        req = request_payload.hbp_max(pub_app_id, placement, ifa=gen_device_id(), bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req,
                             headers=hbp_headers(openrtb='2.5', rtb_selector=meister_rtb_ids,
                                                 debug='jaeger'))

        response_payload = r.json()
        bid_info = response_payload['seatbid'][0]['bid'][0]
        nurl = bid_info['nurl']
        ext = decode_ext(url=nurl)
        r = get(nurl.replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '5.5')
                .replace(hbp_ssl_host, hbp_host)
                .replace(scrat_notification_host_ssl, scrat_notification_host))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        # Verify scrat send win ttl and apply the experiment
        assert_keys_exist(ext, 'exp_win_ttl')
        assert_that(ext['exp_win_ttl'] in [15, 30, 45, 60])
        # Verify exp tag is added in hb-transaction
        hb_transaction = response_payload['ext']['debug']['hb-transaction']
        assert_keys_exist(hb_transaction, 'exp_win_ttl')
        assert_that(ext['exp_win_ttl'], equal_to(hb_transaction['exp_win_ttl']))
        # Verify hp notification

    @allure.feature('win ttl experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4208 Reduce the WinTTL for MAX')
    @allure.description('Verify saygames w/ plugin in UA will enter the experiment and winTTL experiment Tag is added '
                        'in bidtoken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.3;vunglehbs/3.0.0'])
    def test_winTTL_experiment_01(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_token = response_payload['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(11)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        req = request_payload.hbp_saygames(pub_app_id, placement, ifa=gen_device_id(), bid_token=super_token)
        r = post_hbp_request(hbp_saygames_endpoint_qa, json=req,
                             headers=hbp_headers(openrtb='2.5', rtb_selector=meister_rtb_ids,
                                                 debug='jaeger'))

        response_payload = r.json()
        bid_info = response_payload['seatbid'][0]['bid'][0]
        nurl = bid_info['nurl']
        ext = decode_ext(url=nurl)
        r = get(nurl.replace('${AUCTION_PRICE}', '5.6')
                .replace(hbp_ssl_host, hbp_host)
                .replace(scrat_notification_host_ssl, scrat_notification_host))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        # Verify scrat send win ttl and apply the experiment
        assert_keys_exist(ext, 'exp_win_ttl')
        assert_that(ext['exp_win_ttl'] in [15, 30, 45, 60])
        # Verify exp tag is added in hb-transaction
        hb_transaction = response_payload['ext']['debug']['hb-transaction']
        assert_keys_exist(hb_transaction, 'exp_win_ttl')
        assert_that(ext['exp_win_ttl'], equal_to(hb_transaction['exp_win_ttl']))
        # Verify hp notification

    @allure.feature('win ttl experiment')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4208 Reduce the WinTTL for MAX')
    @allure.description('Verify max will enter the experiment and winTTL experiment Tag is added in bidtoken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6;Max'])
    def test_max_winTTL_experiment_02_t(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, debug='jaeger', src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        bid_token = response_payload['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(11)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        req = request_payload.hbp_max(pub_app_id, placement, ifa=gen_device_id(), bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req,
                             headers=hbp_headers(openrtb='2.5', rtb_selector=meister_rtb_ids,
                                                 debug='jaeger'))

        response_payload = r.json()
        bid_info = response_payload['seatbid'][0]['bid'][0]
        nurl = bid_info['nurl']
        r = get(nurl.replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '5.5')
                .replace(hbp_ssl_host, hbp_host)
                .replace(scrat_notification_host_ssl, scrat_notification_host))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        # Verify scrat send win ttl and apply the experiment
        ext = decode_ext(url=bid_info['nurl'])
        assert_keys_exist(ext, 'exp_win_ttl')
        assert_that(ext['exp_win_ttl'] in [15, 30, 45, 60])
        # Verify exp tag is added in hb-transaction
        hb_transaction = response_payload['ext']['debug']['hb-transaction']
        assert_keys_exist(hb_transaction, 'exp_win_ttl')
        assert_that(ext['exp_win_ttl'], equal_to(hb_transaction['exp_win_ttl']))
        # Verify hp notification

    @allure.feature('win ttl experiment')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4208 Reduce the WinTTL for MAX')
    @allure.description('Verify max will enter the experiment and winTTL experiment Tag is added in bidtoken '
                        'for v1 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['HJKM6GM50919'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0;Max'])
    def test_max_winTTL_experiment_03(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        bid_token = response_payload['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token
        super_token = "1:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        req = request_payload.hbp_max(pub_app_id, placement, ifa=gen_device_id(), bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req,
                             headers=hbp_headers(openrtb='2.5', rtb_selector=meister_rtb_ids,
                                                 debug='jaeger'))

        response_payload = r.json()
        bid_info = response_payload['seatbid'][0]['bid'][0]
        nurl = bid_info['nurl']
        r = get(nurl.replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '5.5')
                .replace(hbp_ssl_host, hbp_host)
                .replace(scrat_notification_host_ssl, scrat_notification_host))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        # Verify scrat send win ttl and apply the experiment
        ext = decode_ext(url=nurl)
        assert_keys_exist(ext, 'exp_win_ttl')
        assert_that(ext['exp_win_ttl'] in [15, 30, 45, 60])
        # Verify exp tag is added in hb-transaction
        hb_transaction = response_payload['ext']['debug']['hb-transaction']
        assert_keys_exist(hb_transaction, 'exp_win_ttl')
        assert_that(ext['exp_win_ttl'], equal_to(hb_transaction['exp_win_ttl']))
        # Verify hp notification

    @allure.feature('win ttl experiment')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4208 Reduce the WinTTL for MAX')
    @allure.description('Verify the traffic without partner name in UA'
                        ' will not enter the experiment and winTTL experiment Tag is added in bidtoken '
                        'for v1 token')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.4'])
    def test_max_winTTL_experiment_04(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, debug='jaeger', src_ip=au_ip,
                                          rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        bid_token = response_payload['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token
        super_token = "1:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        req = request_payload.hbp_max(pub_app_id, placement, ifa=gen_device_id(), bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req,
                             headers=hbp_headers(openrtb='2.5', rtb_selector=meister_rtb_ids,
                                                 debug='jaeger'))

        response_payload = r.json()
        bid_info = response_payload['seatbid'][0]['bid'][0]
        ext = decode_ext(url=bid_info['burl'])
        assert_keys_not_exist(ext, 'exp_win_ttl')

    @allure.feature('win ttl experiment')
    @allure.tag('normal')
    @allure.story('PBJ-4208 Reduce the WinTTL for MAX')
    @allure.description('Verify ironsource will not enter the experiment')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6;ironsource'])
    def test_max_winTTL_experiment_05(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, header_bidding=True, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, debug='jaeger', src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        bid_token = response_payload['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(11)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        req = request_payload.hbp_max(pub_app_id, placement, ifa=gen_device_id(), bid_token=super_token)
        r = post_hbp_request(hbp_max_endpoint_qa, json=req,
                             headers=hbp_headers(openrtb='2.5', rtb_selector=meister_rtb_ids,
                                                 debug='jaeger'))

        response_payload = r.json()
        bid_info = response_payload['seatbid'][0]['bid'][0]
        ext = decode_ext(url=bid_info['burl'])
        assert_keys_not_exist(ext, 'exp_win_ttl')
