import pytest
import allure

from http import HTTPStatus

from data import request_payload, response_schema
from utils.behaviors import generate_real_time_token, request_hbp, request_ads_android, request_ads_ios, \
    post_hbp_request, post_hbp_request_no_retry, request_hb_win_notification

from utils.common import *
from utils.assertions import *
from settings import *
import time


@allure.epic('HBP Admob')
class TestAdmob(object):

    @allure.feature('bid feedback')
    @allure.tag('normal', 'v0.52.0')
    @allure.story('PBJ-2998 Real-time feedback for admob'
                  'PBJ-3945 How to use minimum_bid_to_win comes from admob feedback')
    @allure.description('Verify to send the real-time feedback notification'
                        'Verified that HBP should set the minimum_bid_to_win to the settlement_price'
                        ' for loss notificaiton message.')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_bid_feedback(self, pub_app_id, placement):
        info = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), debug='jaeger',
                           sdk_v='Vungle/6.10.1')
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            token = response_payload['seatbid'][0]['bid'][0]['burl'].split('ext=')[1]
            info_1 = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                                 test_device_id=gen_device_id(), sdk_v='Vungle/6.10.1', notification_token=token)
            time.sleep(0.1)
            if info_1['is_hbp_responded_200']:
                response_payload = info_1['hbp_response']
                assert_that(response_payload['seatbid'][0]['bid'][0]['ext']['event_notification_token']['payload'],
                            not equal_to(token))
            event_notification_token = response_payload['seatbid'][0]['bid'][0]['ext']['event_notification_token'][
                'payload']
            # Verify that set the minimum_bid_to_win to the settlement_price
            info_2 = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                                 test_device_id=gen_device_id(), sdk_v='Vungle/6.10.1',
                                 notification_token=event_notification_token, status_code=79)
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3984 Add WinTTL for Admob app bidding application')
    @allure.description('Verify it will not bid again for the token which has already win on admob,'
                        'pub apps added in db')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_admob_winttl_1(self, pub_app_id, placement, sdk_v):
        """
            restrict_apps = ['59786bc2a43b3a08620026b2', '59786bc2a43b3a08620026b4']
        """
        info = request_hb_win_notification('admob', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                           test_device_id=gen_device_id(), sdk_v=sdk_v)
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(debug='jaeger'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.hbp_error_precache)
            assert_that(response_payload['ext']['err_msg'], equal_to('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL'))

    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3984 Add WinTTL for Admob app bidding application')
    @allure.description('Verify it will bid again for the token which has already win on admob,'
                        'pub apps not added in db')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_admob_winttl_2(self, pub_app_id, placement, sdk_v):
        """
            restrict_apps = ['59786bc2a43b3a08620026b2', '59786bc2a43b3a08620026b4']
        """
        info = request_hb_win_notification('admob', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                           test_device_id=gen_device_id(), sdk_v=sdk_v)
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(debug='jaeger'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            if 'ext' in response_payload:
                assert_keys_exist(response_payload['ext']['debug'], 'recommender_info')
                assert_keys_exist(response_payload['ext']['debug'], 'hb-transaction')


    @allure.feature('hbp winttl')
    @allure.tag('normal')
    @allure.story('PBJ-3984 Add WinTTL for Admob app bidding application')
    @allure.description('Verify the winttl should be deleted if the hit count meets the preserve count limit')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1'])
    def test_admob_winttl_3(self, pub_app_id, placement, sdk_v):
        """
            preserve_count_limit = 1
            restrict_apps = ['59786bc2a43b3a08620026b2', '59786bc2a43b3a08620026b4']
        """
        info = request_hb_win_notification('admob', 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                           test_device_id=gen_device_id(), sdk_v=sdk_v)
        time.sleep(0.1)
        if info['is_hbp_responded_200']:
            req = info['hbp_request']
            r = post_hbp_request_no_retry(hbp_admob_endpoint_qa, json=req, headers=hbp_headers(debug='jaeger'))

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            assert_valid_schema(r.json(), response_schema.hbp_error_precache)
            assert_that(response_payload['ext']['err_msg'], equal_to('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL'))
            # The 2nd time request
            r = post_hbp_request_no_retry(hbp_admob_endpoint_qa, json=req,
                                          headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug='jaeger'))
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            response_payload = r.json()
            if 'err_msg' in response_payload['ext']:
                assert_that(response_payload['ext']['err_msg'], is_not('16: NSR: NO_SERV_EVENT_ID_WIN_IN_TTL'))

    @allure.feature('bid price')
    @allure.tag('test mode', 'v0.72.0')
    @allure.story('PBJ-3761 Temp change admob test mode bidprice to 4999')
    @allure.description('Verify bid price is 4999')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_temp_price(self, pub_app_id, placement):
        info = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v='Vungle/6.10.1', is_test=1)
        bid = info['hbp_response']['seatbid'][0]['bid']
        price = bid[0]['price']
        assert_that(price, equal_to(4999))

    @allure.feature('bid price')
    @allure.tag('normal', 'v0.72.0')
    @allure.story('PBJ-3761 Temp change admob test mode bidprice to 4999')
    @allure.description('Verify bid price is not 4999')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_temp_price_01(self, pub_app_id, placement):
        info = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(),
                           sdk_v='Vungle/6.10.1')
        bid = info['hbp_response']['seatbid'][0]['bid']
        price = bid[0]['price']
        assert_that(price, is_not(4999))

    @allure.feature('bid request')
    @allure.tag('normal', 'v0.55.0')
    @allure.story(
        'PBJ-3127 Real-time Ad Test - Req 1 - Test for mapping the data to the HB bid request field for admob')
    @allure.description('Verify the mapping data to the hb bid request')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_bid_request_mapping_for_real_time(self, pub_app_id, placement):
        test_ifa = gen_device_id(36)
        endpoint = get_hbp_partner_endpoint('admob')
        data = generate_real_time_token(11, pub_app_id, placement, test_ifa)
        req = request_payload.hbp_partner('admob', pub_app_id, placement, ifa=test_ifa,
                                          bid_token=data['super_token_v3'])
        r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        assert_response_status_code_in(r.status_code, HTTPStatus.NO_CONTENT, HTTPStatus.OK)

        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid_info['burl'].count('https://'), equal_to(1))

    @allure.feature('hbp bid response')
    @allure.tag('normal')
    @allure.description('Verify the response field "bidid" for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement,
                                           android_hybrid_video_test_placement,
                                           android_realtime_mrec_test_placement,
                                           android_hybrid_mrec_test_placement,
                                           android_preCache_video_test_placement,
                                           android_preCache_mrec_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0', 'Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.11.0'])
    def test_admob_bidid_android_v2(self, pub_app_id, placement, sdk_v):
        info = request_hbp('admob', 11, pub_app_id=pub_app_id, placement_ref_id=placement, ads_retry_mode='meister',
                           test_device_id=gen_device_id(), sdk_v=sdk_v, platform='android')
        if info['is_hbp_responded_200']:
            ad_markup = info['ads_response']['ads'][0]['ad_markup']
            campaign = ad_markup['campaign']

            response_payload = info['hbp_response']
            crid = response_payload['seatbid'][0]['bid'][0]['crid']
            assert_valid_schema(response_payload, response_schema.hbp_admob)
            assert_keys_exist(response_payload, 'bidid')
            assert_that(crid, is_in(campaign))
            assert_keys_exist(response_payload, 'id')
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('hbp bid response')
    @allure.tag('normal')
    @allure.description('Verify the response field "bidid" of placement which type is banner for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_banner_test_placement,
                                           android_hybrid_banner_test_placement,
                                           android_preCache_banner_test_placement
                                           ])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2'])
    def test_admob_bidid_banner_android_v2(self, pub_app_id, placement, sdk_v):
        info = request_hbp('admob', 11, pub_app_id=pub_app_id, placement_ref_id=placement, ads_retry_mode='meister',
                           test_device_id=gen_device_id(), sdk_v=sdk_v, platform='android', banner=True)
        if info['is_hbp_responded_200']:
            ad_markup = info['ads_response']['ads'][0]['ad_markup']
            campaign = ad_markup['campaign']
            response_payload = info['hbp_response']
            crid = response_payload['seatbid'][0]['bid'][0]['crid']
            assert_valid_schema(response_payload, response_schema.hbp_admob)
            assert_keys_exist(response_payload, 'bidid')
            assert_that(crid, is_in(campaign))
            assert_keys_exist(response_payload, 'id')
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('hbp bid response')
    @allure.tag('normal')
    @allure.description('Verify the response field "bidid" for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_video_test_placement,
                                           android_hybrid_video_test_placement,
                                           android_realtime_mrec_test_placement,
                                           android_hybrid_mrec_test_placement,
                                           android_preCache_video_test_placement,
                                           android_preCache_mrec_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2'])
    def test_admob_bidid_android_v1(self, pub_app_id, placement, sdk_v):
        jaeger_response = request_ads_android(pub_app_id=pub_app_id, placement_ref_id=placement,
                                              rtb=meister_rtb_ids, ip=ca_us_ip,
                                              sdk_v=sdk_v, test_android_id=gen_device_id())

        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token
        super_token = "1:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        req = request_payload.hbp_admob(pub_app_id, placement, bid_token=super_token, platform='android')
        endpoint = get_hbp_partner_endpoint('admob')
        r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid_info['burl'].count('https://'), equal_to(1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('hbp bid response')
    @allure.tag('normal')
    @allure.description('Verify the response field "bidid" of placement which type is banner for android')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_realtime_banner_test_placement,
                                           android_hybrid_banner_test_placement,
                                           android_preCache_banner_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.10.0', 'Vungle/6.10.1', 'Vungle/6.10.2'])
    def test_admob_bidid_banner_android_v1(self, pub_app_id, placement, sdk_v):
        jaeger_response = request_ads_android(pub_app_id=pub_app_id, placement_ref_id=placement,
                                              rtb=meister_rtb_ids, ip=ca_us_ip,
                                              sdk_v=sdk_v, banner=True, test_android_id=gen_device_id())

        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token
        super_token = "1:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        req = request_payload.hbp_admob(pub_app_id, placement, bid_token=super_token, platform='android')
        endpoint = get_hbp_partner_endpoint('admob')
        r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid_info['burl'].count('https://'), equal_to(1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('hbp bid response')
    @allure.tag('normal')
    @allure.description('Verify update the key "application_id" to "appid" in adunit but the user stay as before')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_bid_response_update_1(self, pub_app_id, endpoint, placement):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id(), rtb=meister_rtb_ids)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        keyvals = [
            {
                "key": "appid",
                "value": pub_app_id
            },
            {
                "key": "placementID",
                "value": placement
            }
        ]
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, bid_token=super_token, keyvals=keyvals,
                                        is_test=0)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid_info['burl'].count('https://'), equal_to(1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('hbp bid response')
    @allure.tag('normal')
    @allure.description('Verify update the key "application_id" to "appid" both in adunit and user')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_bid_response_update_2(self, pub_app_id, endpoint, placement):
        jaeger_response = request_ads_ios(test_ifa=gen_device_id(), rtb=meister_rtb_ids)
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        keyvals = [
            {
                "key": "appid",
                "value": pub_app_id
            },
            {
                "key": "placementID",
                "value": placement
            }
        ]
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, bid_token=super_token, keyvals=keyvals,
                                        segment=keyvals)
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('hbp bid response')
    @allure.tag('normal')
    @allure.description('Verify update the key appid to "application_id" in adunit but the user stay as before')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_hybrid_mrec_test_placement])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_bid_response_update_android_1(self, pub_app_id, endpoint, placement):
        jaeger_response = request_ads_android(pub_app_id=pub_app_id, placement_ref_id=placement,
                                              rtb=meister_rtb_ids, ip=ca_us_ip,
                                              test_android_id=gen_device_id())
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        keyvals = [
            {
                "key": "application_id",
                "value": pub_app_id
            },
            {
                "key": "placementID",
                "value": placement
            }
        ]
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, bid_token=super_token,
                                        keyvals=keyvals, is_test=0, platform='android')
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_that(bid_info['burl'].count('https://'), equal_to(1))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('hbp bid response')
    @allure.tag('normal')
    @allure.description('Verify update the key "appid" to "application_id" both in adunit and user')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_hybrid_mrec_test_placement])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_bid_response_update_android_2(self, pub_app_id, endpoint, placement):
        jaeger_response = request_ads_android(pub_app_id=pub_app_id, placement_ref_id=placement,
                                              rtb=meister_rtb_ids, ip=ca_us_ip,
                                              test_android_id=gen_device_id())
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        keyvals = [
            {
                "key": "application_id",
                "value": pub_app_id
            },
            {
                "key": "placementID",
                "value": placement
            }
        ]
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, bid_token=super_token,
                                        keyvals=keyvals, segment=keyvals, platform='android')
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        assert_response_status_code(r.status_code, HTTPStatus.NO_CONTENT)

    @allure.feature('event token')
    @allure.tag('normal')
    @allure.story('PBJ-4229 Add impType & os name for win rate metric for admob')
    @allure.description('Verify event token include the imp type for admob')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_hybrid_mrec_test_placement])
    @pytest.mark.parametrize('endpoint', [hbp_admob_endpoint_qa])
    def test_admob_event_token_include_imp_type_01(self, pub_app_id, endpoint, placement):
        jaeger_response = request_ads_android(pub_app_id=pub_app_id, placement_ref_id=placement,
                                              rtb=meister_rtb_ids, ip=ca_us_ip, test_android_id=gen_device_id())
        ordinal_view_count = 7
        bid_token = jaeger_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        keyvals = [
            {
                "key": "application_id",
                "value": pub_app_id
            },
            {
                "key": "placementID",
                "value": placement
            }
        ]
        req = request_payload.hbp_admob(pub_app_id, common_test_placement, bid_token=super_token, keyvals=keyvals,
                                        is_test=0, platform='android')
        r = post_hbp_request(endpoint, json=req, headers=hbp_headers(openrtb='2.5'))
        if r.status_code == HTTPStatus.OK:
            response_payload = r.json()
            bid_info = response_payload['seatbid'][0]['bid'][0]
            event_token = bid_info['ext']['event_notification_token']['payload']
            decode_event_token = get(hbp_admob_event_token_decoder_qa + '?token='+event_token)
            assert_response_status_code(decode_event_token.status_code, HTTPStatus.OK)
            decode_info = decode_event_token.json()
            assert_that(decode_info['impression_type'], equal_to('banner'))
        else:
            assert_that(True, equal_to(False), 'No bid response, please check!')

    @allure.feature('event token')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4229 Add impType & os name for win rate metric for admob')
    @allure.description('Verify event token include the imp type for admob on test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_admob_event_token_include_imp_type_02(self, pub_app_id, placement):
        info = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=test_mode_device_id, rtb=ext_test_mode_kraken_rtb_ids_mraid,
                           sdk_v='Vungle/6.10.1', is_test=1)
        bid = info['hbp_response']['seatbid'][0]['bid'][0]
        event_token = bid['ext']['event_notification_token']['payload']
        decode_event_token = get(hbp_admob_event_token_decoder_qa + '?token=' + event_token)
        assert_response_status_code(decode_event_token.status_code, HTTPStatus.OK)
        decode_info = decode_event_token.json()
        assert_that(decode_info['impression_type'], equal_to('video'))


    @allure.feature('Google Api Integration')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob '
                  'feedback')
    @allure.description('Verify redis key is correct when creative_status_code=7/131 via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('creative_status_code', [7, 131])
    def test_google_api_integration_creative_status_7_131(self, pub_app_id, placement, creative_status_code):
        info = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=test_mode_device_id, rtb=ext_test_mode_kraken_rtb_ids_mraid, is_test=1,
                           sdk_v='Vungle/6.10.6', is_hb='admob', status_code=creative_status_code)
        bid = info['hbp_response']['seatbid'][0]['bid'][0]

        # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that submit ' key: of
        # cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.ALL/RUS/CHN, with the TTL=32 min' to redis , value=1

    @allure.feature('Google Api Integration')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob '
                  'feedback')
    @allure.description('Verify redis key is correct when creative_status_code=7/131 via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('creative_status_code', [7, 131])
    def test_google_api_integration_creative_status_7_131_i(self, pub_app_id, placement, creative_status_code):
        info = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=test_mode_device_id, rtb=test_mode_kraken_rtb_ids,
                           sdk_v='Vungle/6.10.6', is_hb='admob', status_code=creative_status_code)
        bid = info['hbp_response']['seatbid'][0]['bid'][0]

        # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that submit ' key: of
        # cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.ALL/RUS/CHN, with the TTL=32 min' to redis , value=1


    @allure.feature('Google Api Integration')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob '
                  'feedback')
    @allure.description('Verify redis key is correct when creative_status_code=129/130/205/10 via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('creative_status_code', [129, 130, 205, 10])
    def test_google_api_integration_creative_status_others_e(self, pub_app_id, placement, creative_status_code):
        info = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                           sdk_v='Vungle/6.10.6', is_hb='admob', status_code=creative_status_code)
        bid = info['hbp_response']['seatbid'][0]['bid'][0]

        # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that submit ' key: of
        # cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.<Region>, with the TTL=168 hours' to redis
        # Note, 129 -> region=CHN; 130 -> region=RUS; others -> ALL, value=0



    @allure.feature('Google Api Integration')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob '
                  'feedback')
    @allure.description('Verify redis key is correct when creative_status_code=129/130/205/10 via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('creative_status_code', [129, 130, 205, 10])
    def test_google_api_integration_creative_status_others_i(self, pub_app_id, placement, creative_status_code):
        info = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), rtb=non_test_mode_kraken_rtb_ids,
                           buyer_creative_id="ext62623ad",
                           sdk_v='Vungle/6.10.6', is_hb='admob', status_code=creative_status_code)
        bid = info['hbp_response']['seatbid'][0]['bid'][0]

        # Verify that submit message to kafka topic: ex-jaeger-admob-creatives Verify that submit ' key: of
        # cr-rev-res.<murmur3sum32 of ([rtbAccountID]_[creativeID]>.<Region>, with the TTL=168 hours' to redis
        # Note, 129 -> region=CHN; 130 -> region=RUS; others -> ALL, value=0



    @allure.feature('Google Api Integration')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4337 Google Creative API Integration - [Jaeger&HBP]Update Creative status in Redis from Admob '
                  'feedback')
    @allure.description('Verify hbp will serve for key existing in redis for waterfull')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('creative_status_code', [7, 131, 129, 130, 205, 10])
    def test_google_api_integration_creative_status_not_block_waterfull(self, pub_app_id, placement, creative_status_code):
        info = request_hbp('admob', 7, pub_app_id=pub_app_id, placement_ref_id=placement,
                           test_device_id=gen_device_id(), rtb=non_test_mode_kraken_rtb_ids,
                           buyer_creative_id="ext62623ad",
                           sdk_v='Vungle/6.10.6', is_hb='admob', status_code=creative_status_code)
        bid = info['hbp_response']['seatbid'][0]['bid'][0]
        assert_keys_exist(bid, 'price')
