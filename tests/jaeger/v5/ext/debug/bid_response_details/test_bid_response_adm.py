import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestBidResponseADM(object):

    @allure.feature('basic')
    @allure.tag('basic', 'smoke')
    @allure.story('bid response adm')
    @allure.description('Verify bid response adm details from debug info')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_bid_response_adm(self, pub_app_id):
        test_ifa = gen_device_id(digital=36)
        if env == 'ci':
            rtb = meister_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = meister_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, common_test_placement, ifa=test_ifa)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        for rtb_id in bid_response.keys():
            if 'seatbid' in bid_response[rtb_id]:
                campaign_id = str(ad_markup['campaign']).split('|')[0]
                creative_id = str(ad_markup['campaign']).split('|')[1]

                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_valid_schema(r.json(), response_schema.ads_v5_debug)
                assert_that(ad_markup['id'] in bid_response[rtb_id]['seatbid'][0]['bid'][0]['adm'])
                assert_that(campaign_id in bid_response[rtb_id]['seatbid'][0]['bid'][0]['adm'])
                assert_that(creative_id in bid_response[rtb_id]['seatbid'][0]['bid'][0]['adm'])
                assert_that(bid_response[rtb_id]['seatbid'][0]['seat']
                            in bid_response[rtb_id]['seatbid'][0]['bid'][0]['adm'])
                assert_that(bid_response[rtb_id]['seatbid'][0]['seat'] in ad_markup['app_id'])
                assert_that(ad_markup['adType'] in bid_response[rtb_id]['seatbid'][0]['bid'][0]['adm'])

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode')
    @allure.story('external support')
    @allure.description('Verify the bid response adm of programmatic banner')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_for_adm_of_programmatic_banner(self, pub_app_id, placement):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_mraid.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, banner=True, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' not in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_exist(bid_response[rtb]['seatbid'][0]['bid'][0], 'adm')
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['adm'], not empty())

    @allure.feature('test mode')
    @allure.tag('normal', 'test_mode')
    @allure.story('external support'
                  'PBJ-4204 Combine rtbVideo and rtbEndcard in Jaeger; remove rtbVideo')
    @allure.description('Verify the bid response adm of programmatic vast'
                        'Verify jaeger choose rtbEndcard template even dsp response rtb video vast')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_for_adm_of_programmatic_vast(self, pub_app_id, placement):
        override_adm = 'seatbid.0.bid.0.adm@"<?xml version=\\"1.0\\" encoding=\\"UTF-8\\"?><VAST version=\\"2.0\\"><Ad id=\\"39569\\"><InLine><AdSystem>Chartboost<\\/AdSystem><Error><\\/Error><AdTitle><\\/AdTitle><Impression><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/impression?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/Impression><Creatives><Creative><Linear><Duration>00:00:26<\\/Duration><MediaFiles><MediaFile bitrate=\\"906\\" delivery=\\"progressive\\" height=\\"1280\\" width=\\"720\\" maintainAspectRatio=\\"true\\" scalable=\\"true\\" type=\\"video\\/mp4\\"><![CDATA[https:\\/\\/v-ak.chartboost.com\\/videoads\\/617910ce629370079210e122_720-1635324110.mp4]]><\\/MediaFile><\\/MediaFiles><VideoClicks><ClickThrough><![CDATA[https:\\/\\/apps.apple.com\\/us\\/app\\/slots-cash-link-slot-machines\\/id1480805172?uo=4]]><\\/ClickThrough><ClickTracking><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/click?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/ClickTracking><\\/VideoClicks><TrackingEvents><Tracking event=\\"firstQuartile\\"><![CDATA[https:\\/\\/ssp-events.chartboost.com\\/completed_view?ssp=cbbidder&cpm_price=${AUCTION_PRICE}&pb=zp79Uvqi7NiZMlvdQpmd_BTU7IM0dYDH78R1RW3pHvVLrvg49L8C4XqrKt4w6F63UcfLQjm2FCUQ68FYBWSLOVbF9SA5t6EwyDK-2az0TvAhmqwjgmlq7BvAcU3YQX_GtH0wJJzJUU5Ll6JzaTXQH3dhgykkK9kcUYxeNfz_JRR3EnAwScLYCBgjsmX9tr3jTS73OEHo8DP-6DQCgTIr0KT9k04T-DSqkygj_nypohAu9JHNECeo1UoxySbym8ZG_8mFg0AfRKp1teKltpDWh-tGjuMRlBv9lL63h_b9M3TNKJwqJFOuoq6waH7Mk48jnrVlI5akVWK_g5jbAylT4-_-59Jn8Q4tZHy5Tioqa7Lj5qwuw75nvrejnzy4OGOFhUflQ1d0NkPySjhOrnd4RZMpveQP5hwhDgfmXRbcW81tnuPcKHJRXrI1JlrYtl4IVd4hmUHd8FzDuq7ArfkeRkBmeizNDRSbRT7ASYe5RvyRTn6IAUOYoxIwTPWex3FE20UYtM1XrQEb-L5C5Jk2ywzrVDV31wwwRd1tT065sduiQAquXNLJgA64zLKzgg2N2y7vMGk81QziXGZCVRSK6ND8U5NlvF1ijuN1oh4MAIX74kfXvHR-oWSkGAWzx_VPioiwjIhWWlEvwCFfYBq6oOB0iF0jDhps7Cq5VV_4QOPAsWPKLlSHWtes7sMpwsHqL7UWxW9qh7uN5TI5M_7lHXxjoswu6tEqMAThra0PTkmLyWoltJaM1gPo1xhj8WsS44cU0sK5yHLe11teGwKp9r76ufJeEwkbYeHiPFGnSkLSKvahgjTPu4hoKy0iQ941cIeI5iGDa6qnBeMOtvGbbYIq_vQ0mEwm0bREBbxFOrd3YO81mp0oRhtl7h3fnGh7a5xoUn-cHXk0_I_TT0gcCPKpn63jaBGUXg4XTUe6iHiao2AShCvBhUg3iRdHgYBf8v6PXhgRftwWlsuSEjaFsqUDw8Ec&iv=loiTEqdRZRLRs1yZ]]><\\/Tracking><\\/TrackingEvents><\\/Linear><\\/Creative><\\/Creatives><\\/InLine><\\/Ad><\\/VAST>"'
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb,
                                                                        src_ip=au_ip,
                                                                        override_bid_response_any=override_adm))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        templateURL = ad_markup['templateURL']
        assert_that("programmaticEndcard" in templateURL)
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']

        if 'VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm']:
            bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5_debug)
            assert_keys_exist(bid_response[rtb]['seatbid'][0]['bid'][0], 'adm')
            assert_that(bid_response[rtb]['seatbid'][0]['bid'][0]['adm'], not empty())
            assert_that('VAST' in bid_response[rtb]['seatbid'][0]['bid'][0]['adm'])




    @allure.feature('kraken')
    @allure.tag('normal', 'R_1.155.0')
    @allure.story('PBJ-2552 Kraken event id should be MongoID')
    @allure.description('Verify the event id from ADM is in format of mongo id')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_kraken_event_id_1(self, pub_app_id, placement):
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        adm = bid_response[rtb]['seatbid'][0]['bid'][0]['adm']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(len(str_to_json(adm)['id']), equal_to(24))
        assert_that(len(str_to_json(str_to_json(adm)['app_id'].replace('$0$', ''))['eventID']), equal_to(24))
        assert_that(str_to_json(str_to_json(adm)['app_id'].replace('$0$', ''))['eventID'], str_to_json(adm)['id'])

    @allure.feature('kraken')
    @allure.tag('normal', 'R_1.155.0')
    @allure.story('PBJ-2552 Kraken event id should be MongoID')
    @allure.description('Verify the event id from ADM matchs the one from ads response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_kraken_event_id_2(self, pub_app_id, placement):
        if env == 'ci':
            rtb = test_mode_kraken_rtb_ids.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = test_mode_kraken_rtb_ids.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(debug='jaeger', rtb_selector=rtb))

        response_payload = r.json()
        bid_response = response_payload['ext']['debug']['auction_result']['bid_response_details']
        adm = bid_response[rtb]['seatbid'][0]['bid'][0]['adm']
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5_debug)
        assert_that(str_to_json(adm)['id'], equal_to(ad_markup['id']))
        assert_that(str_to_json(adm)['app_id'], equal_to(ad_markup['app_id']))
        assert_that(str_to_json(adm)['campaign'], equal_to(ad_markup['campaign']))
