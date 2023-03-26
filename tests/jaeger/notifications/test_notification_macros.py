from http import HTTPStatus

import allure

from data import request_payload, response_schema
from utils.common import *
from utils.assertions import *
from settings import *


@allure.epic('jaeger Notification macros')
class TestNotificationMacros(object):

    @allure.feature('Notification Macros')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5322 Support AUCTION_MIN_TO_WIN for Accelerate')
    @allure.description('Verify that {AUCTION_MIN_TO_WIN} is added for LO')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification_loss])
    def test_auction_min_to_win_01(self, pub_app_id, placement, rtb_ids, sdk_v):
        """
        :bill_notice_origin:sdk

        """
        burl = "http://kraken-ext.apiqa.svc.cluster.local:7700/burl?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN}"
        override_bid_response_any = 'seatbid.0.bid.0.price@3|||seatbid.0.bid.0.burl@"%s"' % burl
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v, override_bid_response_any=override_bid_response_any
                                           ))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        checkpoint0 = ad_markup['tpat']['checkpoint.0']
        burl = [x for i, x in enumerate(checkpoint0) if x.find('/burl') != -1][0]
        assert_that('auction_min=1.000000000' in burl)


    @allure.feature('Notification Macros')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5322 Support AUCTION_MIN_TO_WIN for Accelerate')
    @allure.description('Verify that {AUCTION_MIN_TO_WIN} is added for meister')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('rtb_ids', [test_mode_kraken_rtb_ids_1])
    def test_auction_min_to_win_02(self, pub_app_id, placement, rtb_ids, sdk_v):
        """
        :bill_notice_origin:sdk
        :win_notice_origin:sdk
        """
        burl = "http://kraken-ext.apiqa.svc.cluster.local:7700/burl?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN} "
        # over_ride_price = 'ext2:3.0,ext1:2'
        override_bid_response_any = 'seatbid.0.bid.0.price@1|||seatbid.0.bid.0.burl@"%s"' % burl
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v, override_bid_response_any=override_bid_response_any
                                           ))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        checkpoint0 = ad_markup['tpat']['checkpoint.0']
        burl = [x for i, x in enumerate(checkpoint0) if x.find('/burl') != -1][0]
        assert_that('auction_min=1.000000000' in burl)



    @allure.feature('Notification Macros')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5322 Support AUCTION_MIN_TO_WIN for Accelerate')
    @allure.description('Verify that {AUCTION_MIN_TO_WIN} is added for LO without {AUCTION_PRICE}')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification_loss])
    def test_auction_min_to_win_03(self, pub_app_id, placement, rtb_ids, sdk_v):
        """
        :bill_notice_origin:sdk
        :win_notice_origin:sdk
        """
        burl = "http://kraken-ext.apiqa.svc.cluster.local:7700/burl?&auction_min=${" \
               "AUCTION_MIN_TO_WIN} "
        # over_ride_price = 'ext2:3.0,ext1:2'
        override_bid_response_any = 'seatbid.0.bid.0.price@4|||seatbid.0.bid.0.burl@"%s"' % burl
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v, override_bid_response_any=override_bid_response_any
                                           ))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        checkpoint0 = ad_markup['tpat']['checkpoint.0']
        burl = [x for i, x in enumerate(checkpoint0) if x.find('/burl') != -1][0]
        assert_that('auction_min=1.000000000' in burl)


    @allure.feature('Notification Macros')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5322 Support AUCTION_MIN_TO_WIN for Accelerate')
    @allure.description('Verify that {AUCTION_MIN_TO_WIN} is added for below bidfloor')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification_loss])
    def test_auction_min_to_win_04(self, pub_app_id, placement, rtb_ids, sdk_v):
        """
        :bill_notice_origin:sdk
        :win_notice_origin:sdk
        """
        burl = "http://kraken-ext.apiqa.svc.cluster.local:7700/burl?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN} "
        # over_ride_price = 'ext2:3.0,ext1:2'
        override_bid_response_any = 'seatbid.0.bid.0.price@0.9|||seatbid.0.bid.0.burl@"%s"' % burl
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v, override_bid_response_any=override_bid_response_any
                                           ))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        checkpoint0 = ad_markup['tpat']['checkpoint.0']
        burl = [x for i, x in enumerate(checkpoint0) if x.find('/burl') != -1][0]
        assert_that('auction_min=' in burl)


    @allure.feature('Notification Macros')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5322 Support AUCTION_MIN_TO_WIN for Accelerate')
    @allure.description('Verify that {AUCTION_MIN_TO_WIN} is added for non hb')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification_loss])
    def test_auction_min_to_win_05(self, pub_app_id, placement, rtb_ids, sdk_v):
        """
        :bill_notice_origin:sdk

        """
        burl = "http://kraken-ext.apiqa.svc.cluster.local:7700/burl?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN} "
        nurl = "http://kraken-ext.apiqa.svc.cluster.local:7700/win?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN}"
        # over_ride_price = 'ext2:3.0,ext1:2'
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"|||seatbid.0.bid.0.price@3|||seatbid.0.bid.0.burl@"%s"' % (nurl,burl)
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v, override_bid_response_any=override_bid_response_any
                                           ))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        checkpoint0 = ad_markup['tpat']['checkpoint.0']
        burl = [x for i, x in enumerate(checkpoint0) if x.find('/burl') != -1][0]
        nurl = [x for i, x in enumerate(checkpoint0) if x.find('/win') != -1][0]
        assert_that('auction_min=1.000000000' in burl)
        assert_that('auction_min=1.000000000' in nurl)



    @allure.feature('Notification Macros')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5322 Support AUCTION_MIN_TO_WIN for Accelerate')
    @allure.description('Verify that {AUCTION_MIN_TO_WIN} is added for mutiple dsp auction')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('rtb_ids', [mixed_non_test_mode_rtb_auction_mbtw])
    def test_auction_min_to_win_06(self, pub_app_id, placement, rtb_ids, sdk_v):
        """
        :bill_notice_origin:sdk

        """
        burl = "http://kraken-ext.apiqa.svc.cluster.local:7700/burl?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN} "
        nurl = "http://kraken-ext.apiqa.svc.cluster.local:7700/win?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN}"
        over_ride_price = 'ext2:3.0'
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"|||seatbid.0.bid.0.burl@"%s"' % (nurl,burl)
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v, override_bid_response_any=override_bid_response_any
                                          ,override_bid_price=over_ride_price ))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        checkpoint0 = ad_markup['tpat']['checkpoint.0']
        burl = [x for i, x in enumerate(checkpoint0) if x.find('/burl') != -1][0]
        nurl = [x for i, x in enumerate(checkpoint0) if x.find('/win') != -1][0]
        assert_that('auction_min=3.000000000' in burl)
        assert_that('auction_min=3.000000000' in nurl)


    @allure.feature('Notification Macros')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5322 Support AUCTION_MIN_TO_WIN for Accelerate')
    @allure.description('Verify that {AUCTION_MIN_TO_WIN} is added for mutiple dsp auction')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('rtb_ids', [mixed_non_test_mode_rtb_auction_mbtw])
    def test_auction_min_to_win_07(self, pub_app_id, placement, rtb_ids, sdk_v):
        """
        :bill_notice_origin:sdk

        """
        burl = "http://kraken-ext.apiqa.svc.cluster.local:7700/burl?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN} "
        nurl = "http://kraken-ext.apiqa.svc.cluster.local:7700/win?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN}"
        over_ride_price = 'ext2:0.9'
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"|||seatbid.0.bid.0.burl@"%s"' % (nurl,burl)
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v, override_bid_response_any=override_bid_response_any
                                          ,override_bid_price=over_ride_price ))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        checkpoint0 = ad_markup['tpat']['checkpoint.0']
        burl = [x for i, x in enumerate(checkpoint0) if x.find('/burl') != -1][0]
        nurl = [x for i, x in enumerate(checkpoint0) if x.find('/win') != -1][0]
        assert_that('auction_min=1.000000000' in burl)
        assert_that('auction_min=1.000000000' in nurl)


    @allure.feature('Notification Macros')
    @allure.tag('basic', 'smoke', 'v1.259.2')
    @allure.story('PBJ-5322 Support AUCTION_MIN_TO_WIN for Accelerate')
    @allure.description('Verify that dont add {AUCTION_MIN_TO_WIN} for other edsp')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    @pytest.mark.parametrize('rtb_ids', [ext_non_test_mode_kraken_rtb_ids_vast])
    def test_auction_min_to_win_08(self, pub_app_id, placement, rtb_ids, sdk_v):
        """
        :bill_notice_origin:sdk

        """
        burl = "http://kraken-ext.apiqa.svc.cluster.local:7700/burl?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN} "
        nurl = "http://kraken-ext.apiqa.svc.cluster.local:7700/win?price=${AUCTION_PRICE}&auction_min=${" \
               "AUCTION_MIN_TO_WIN}"
        # over_ride_price = 'ext2:3.0,ext1:2'
        override_bid_response_any = 'seatbid.0.bid.0.nurl@"%s"|||seatbid.0.bid.0.price@5|||seatbid.0.bid.0.burl@"%s"' % (nurl,burl)
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=rtb_ids, sdk_version=sdk_v, override_bid_response_any=override_bid_response_any
                                           ))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        checkpoint0 = ad_markup['tpat']['checkpoint.0']
        burl = [x for i, x in enumerate(checkpoint0) if x.find('/burl') != -1][0]
        nurl = [x for i, x in enumerate(checkpoint0) if x.find('/win') != -1][0]
        assert_that('auction_min=' in burl)
        assert_that('auction_min=' in nurl)