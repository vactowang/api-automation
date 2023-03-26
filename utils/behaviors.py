import gzip
from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *


def request_ads_ios_no_retry(pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                             test_ifa=gen_device_id(), rtb=meister_rtb_ids, hb=True, banner=False, ip=ca_us_ip,
                             sdk_v=test_default_sdk_version, perf=False, coppa=None, is_hb=False,
                             override_bid_response_any=None, debug=None, ext=None):
    req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=test_ifa, header_bidding=hb, banner=banner,
                                        coppa=coppa, ext=ext)

    if perf:
        endpoint = ads_v5_endpoint_qa0
    else:
        endpoint = ads_v5_endpoint_qa

    r = post(endpoint, json=req,
             headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v, is_hb=is_hb, debug=debug,
                                      override_bid_response_any=override_bid_response_any))
    assert_response_status_code(r.status_code, HTTPStatus.OK)
    response_payload = r.json()

    return response_payload


def request_ads_android_no_retry(pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                                 rtb=meister_rtb_ids, hb=True, banner=False, ip=ca_us_ip, coppa=None,
                                 sdk_v=test_default_sdk_version, perf=False, test_android_id=gen_device_id(),
                                 is_hb=False, override_bid_response_any=None, debug=None):
    req = request_payload.jaeger_v5_android(pub_app_id, placement_ref_id, geo=True, header_bidding=hb, banner=banner,
                                            android_id=test_android_id, coppa=coppa)

    if perf:
        endpoint = ads_v5_endpoint_qa0
    else:
        endpoint = ads_v5_endpoint_qa

    r = post(endpoint, json=req,
             headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v, is_hb=is_hb, debug=debug,
                                      override_bid_response_any=override_bid_response_any))
    assert_response_status_code(r.status_code, HTTPStatus.OK)
    response_payload = r.json()

    return response_payload


def request_ads_windows_no_retry(pub_app_id=windows_common_test_app, placement_ref_id=windows_common_test_placement,
                                 rtb=meister_rtb_ids, hb=True, banner=False, ip=ca_us_ip, coppa=None,
                                 sdk_v=test_default_sdk_version, perf=False, ifa=gen_device_id(),
                                 is_hb=False, override_bid_response_any=None, debug=None):
    req = request_payload.jaeger_v5_windows(pub_app_id, placement_ref_id, header_bidding=hb, banner=banner,
                                            ifa=ifa, coppa=coppa)

    if perf:
        endpoint = ads_v5_endpoint_qa0
    else:
        endpoint = ads_v5_endpoint_qa

    r = post(endpoint, json=req,
             headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v, is_hb=is_hb, debug=debug,
                                      override_bid_response_any=override_bid_response_any))
    assert_response_status_code(r.status_code, HTTPStatus.OK)
    response_payload = r.json()

    return response_payload


def request_ads_ios(pub_app_id=common_test_app, placement_ref_id=common_test_placement, test_ifa=gen_device_id(),
                    rtb=meister_rtb_ids, hb=True, banner=False, ip=ca_us_ip, sdk_v=test_default_sdk_version, coppa=None,
                    perf=False, is_hb=False, retry_mode='kraken', override_bid_response_any=None, ext=None,
                    debug=None):
    req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=test_ifa, header_bidding=hb, banner=banner,
                                        coppa=coppa, ext=ext)

    if perf:
        endpoint = ads_v5_endpoint_qa0
    else:
        endpoint = ads_v5_endpoint_qa
    r = post(endpoint, json=req,
             headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v, is_hb=is_hb, debug=debug,
                                      override_bid_response_any=override_bid_response_any))
    assert_response_status_code(r.status_code, HTTPStatus.OK)
    response_payload = r.json()

    if 'sleep' in response_payload['ads'][0]['ad_markup'] and test_ifa != test_mode_device_id:
        # Retry to get bid token from Meister (retry_mode='meister')
        # Retry to get bid token from external Kraken in non-test mode (retry_mode='kraken')
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=test_ifa, header_bidding=hb,
                                            banner=banner, ext=ext)
        if banner:
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid if retry_mode == 'kraken' else meister_rtb_ids
            r = post(endpoint, json=req,
                     headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v,
                                              override_bid_response_any=override_bid_response_any))
        else:
            rtb = ext_non_test_mode_kraken_rtb_ids_vast if retry_mode == 'kraken' else meister_rtb_ids
            r = post(endpoint, json=req,
                     headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v,
                                              override_bid_response_any=override_bid_response_any))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()

    return response_payload


def request_ads_android(pub_app_id=common_test_app, placement_ref_id=common_test_placement, rtb=meister_rtb_ids,
                        hb=True, banner=False, ip=ca_us_ip, coppa=None, retry_mode='kraken', debug=None,
                        sdk_v=test_default_sdk_version, perf=False, test_android_id=gen_device_id(), is_hb=False,
                        override_bid_response_any=None, ext=None):
    req = request_payload.jaeger_v5_android(pub_app_id, placement_ref_id, geo=True, header_bidding=hb, banner=banner,
                                            android_id=test_android_id, coppa=coppa, ext=ext)

    if perf:
        endpoint = ads_v5_endpoint_qa0
    else:
        endpoint = ads_v5_endpoint_qa
    r = post(endpoint, json=req,
             headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v, is_hb=is_hb, debug=debug,
                                      override_bid_response_any=override_bid_response_any))
    assert_response_status_code(r.status_code, HTTPStatus.OK)
    response_payload = r.json()

    if 'sleep' in response_payload['ads'][0]['ad_markup'] and test_android_id != test_mode_device_id:
        # Retry to get bid token from Meister (retry_mode='meister')
        # Retry to get bid token from external Kraken in non-test mode (retry_mode='kraken')
        req = request_payload.jaeger_v5_android(pub_app_id, placement_ref_id, android_id=test_android_id, geo=True,
                                                header_bidding=hb, banner=banner, coppa=coppa)
        if banner:
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid if retry_mode == 'kraken' else meister_rtb_ids
            r = post(endpoint, json=req,
                     headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v,
                                              override_bid_response_any=override_bid_response_any))
        else:
            rtb = ext_non_test_mode_kraken_rtb_ids_vast if retry_mode == 'kraken' else meister_rtb_ids
            r = post(endpoint, json=req,
                     headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v,
                                              override_bid_response_any=override_bid_response_any))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()

    return response_payload


def request_ads_windows(pub_app_id=windows_common_test_app, placement_ref_id=windows_common_test_placement,
                        rtb=meister_rtb_ids, hb=True, banner=False, ip=ca_us_ip, coppa=None, retry_mode='kraken',
                        sdk_v=test_default_sdk_version, perf=False, ifa=gen_device_id(), is_hb=False,
                        override_bid_response_any=None, debug=None):
    req = request_payload.jaeger_v5_windows(pub_app_id, placement_ref_id, header_bidding=hb, banner=banner,
                                            ifa=ifa, coppa=coppa)

    if perf:
        endpoint = ads_v5_endpoint_qa0
    else:
        endpoint = ads_v5_endpoint_qa
    r = post(endpoint, json=req,
             headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v, is_hb=is_hb, debug=debug,
                                      override_bid_response_any=override_bid_response_any))
    assert_response_status_code(r.status_code, HTTPStatus.OK)
    response_payload = r.json()

    if 'sleep' in response_payload['ads'][0]['ad_markup'] and ifa != test_mode_device_id:
        # Retry to get bid token from Meister (retry_mode='meister')
        # Retry to get bid token from external Kraken in non-test mode (retry_mode='kraken')
        req = request_payload.jaeger_v5_windows(pub_app_id, placement_ref_id, ifa=ifa,
                                                header_bidding=hb, banner=banner, coppa=coppa)
        if banner:
            rtb = ext_non_test_mode_kraken_rtb_ids_mraid if retry_mode == 'kraken' else meister_rtb_ids
            r = post(endpoint, json=req,
                     headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v,
                                              override_bid_response_any=override_bid_response_any))
        else:
            rtb = ext_non_test_mode_kraken_rtb_ids_vast if retry_mode == 'kraken' else meister_rtb_ids
            r = post(endpoint, json=req,
                     headers=platform_headers(rtb_selector=rtb, src_ip=ip, sdk_version=sdk_v,
                                              override_bid_response_any=override_bid_response_any))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()

    return response_payload


def request_hbp(supply, ordinal_view, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                test_device_id=gen_device_id(36), sdk_v=test_default_sdk_version, notification_token=None,
                banner=False, platform='ios', rtb=meister_rtb_ids, is_test=0, hb=True, status_code=79,
                post_retry=True, ads_retry_mode='kraken', imp=1, ads_debug=None, debug=None, source=None, X_Env=None,
                override_bid_response_any=None, is_hb=False, buyer_creative_id="test_creative_id_854943",
                ip=ca_us_ip, config_extension=None):
    endpoint = get_hbp_partner_endpoint(supply)
    if platform == 'android':
        ads_response = request_ads_android(pub_app_id, placement_ref_id, sdk_v=sdk_v, banner=banner, rtb=rtb,
                                           test_android_id=test_device_id, hb=hb, retry_mode=ads_retry_mode,
                                           is_hb=is_hb, override_bid_response_any=override_bid_response_any,
                                           debug=ads_debug, ip=ip, ext=config_extension)
    else:
        ads_response = request_ads_ios(pub_app_id, placement_ref_id, test_ifa=test_device_id, sdk_v=sdk_v, rtb=rtb,
                                       hb=hb, banner=banner, retry_mode=ads_retry_mode, debug=ads_debug,
                                       override_bid_response_any=override_bid_response_any, is_hb=is_hb,
                                       ip=ip, ext=config_extension)

    ordinal_view_count = ordinal_view

    bid_token = ads_response['ads'][0]['ad_markup']['bid_token']
    bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
    super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')

    req = request_payload.hbp_partner(supply, pub_app_id, placement_ref_id, ifa=test_device_id, bid_token=super_token,
                                      notification_token=notification_token, is_test=is_test, status_code=status_code,
                                      imp=imp, platform=platform, buyer_creative_id=buyer_creative_id)
    r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug=debug, Source=source,
                                                     X_Env=X_Env))
    if r.status_code == HTTPStatus.NO_CONTENT and post_retry:
        r = post(endpoint, json=req, headers=hbp_headers(openrtb='2.5', sdk_version=sdk_v, debug=debug, Source=source,
                                                         X_Env=X_Env))

    if r.status_code == HTTPStatus.OK:
        response_payload = r.json()
        if debug is not None and 'nbr' in response_payload:
            responses = {
                "error_info": response_payload["ext"]["err_msg"],
                "is_hbp_responded_200": True
            }
        else:
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            if supply != 'admob':
                assert_keys_exist(response_payload['seatbid'][0]['bid'][0], 'nurl')
            responses = {
                "ads_response": dict(ads_response),
                "hbp_response": dict(response_payload),
                "hbp_request": dict(req),
                "super_token": super_token,
                "is_hbp_responded_200": True
            }
    else:
        responses = {
            "ads_response": dict(ads_response),
            "hbp_response": None,
            "hbp_request": dict(req),
            "super_token": super_token,
            "is_hbp_responded_200": False
        }

    return responses


def request_s2s(supply='sigmob', platform='ios', pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                ifa=gen_device_id(),
                rtb=meister_rtb_ids, is_test=0, ip=ca_us_ip, gdpr=None, coppa=None, ccpa=None, consent=1, idfv=None,
                android_id=None, app_set_id=None, ashwid=None, banner_format=None, override_price_any=None):
    endpoint = get_s2s_partner_endpoint(supply)
    if platform == 'ios':
        req = request_payload.s2s_partner(supply, pub_app_id, placement_ref_id, ifa=ifa, idfv=idfv,
                                          banner_format=banner_format,
                                          is_test=is_test, ip=ip, gdpr=gdpr, coppa=coppa, ccpa=ccpa, consent=consent)
    elif platform == 'android':
        req = request_payload.s2s_partner_android(supply, pub_app_id, placement_ref_id, ifa=ifa,
                                                  banner_format=banner_format, app_set_id=app_set_id,
                                                  is_test=is_test, ip=ip, gdpr=gdpr, coppa=coppa, ccpa=ccpa,
                                                  consent=consent, android_id=android_id)
    elif platform == 'amazon':
        req = request_payload.s2s_partner_amazon(supply, pub_app_id, placement_ref_id, ifa=ifa,
                                                 banner_format=banner_format,
                                                 is_test=is_test, ip=ip, gdpr=gdpr, coppa=coppa, ccpa=ccpa,
                                                 consent=consent, app_set_id=None)
    elif platform == 'windows':
        req = request_payload.s2s_partner_windows(supply, pub_app_id, placement_ref_id, ifa=ifa,
                                                  banner_format=banner_format,
                                                  is_test=is_test, ip=ip, gdpr=gdpr, coppa=coppa, ccpa=ccpa,
                                                  consent=consent, ashwid=ashwid)
    r = post(endpoint, json=req,
             headers=platform_headers(sdk_version='', debug='jaeger', rtb_selector=rtb,
                                      override_price_any=override_price_any))
    if r.status_code == HTTPStatus.OK:
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)

    return response_payload


def request_hbp_no_notification(supply, ordinal_view, pub_app_id=common_test_app, sdk_v=test_default_sdk_version,
                                placement_ref_id=common_test_placement, test_device_id=gen_device_id(36),
                                ads_retry_mode='kraken', platform='ios', ads_debug=None):
    up_responses = request_hbp(supply, ordinal_view, pub_app_id, placement_ref_id, test_device_id=test_device_id,
                               sdk_v=sdk_v, ads_retry_mode=ads_retry_mode, platform=platform, ads_debug=ads_debug)
    event_id = up_responses['ads_response']['ads'][0]['ad_markup']['id']
    campaign = up_responses['ads_response']['ads'][0]['ad_markup']['campaign']
    app_id = up_responses['ads_response']['ads'][0]['ad_markup']['app_id']
    ad_token = up_responses['ads_response']['ads'][0]['ad_markup']['ad_token']
    hbp_request = up_responses['hbp_request']
    hbp_response_flag = up_responses['is_hbp_responded_200']
    bid_price = None
    bid_id = None

    if hbp_response_flag:
        bid_price = up_responses['hbp_response']['seatbid'][0]['bid'][0]['price']
        bid_id = up_responses['hbp_response']['seatbid'][0]['bid'][0]['id']

    info = {
        "event_id": event_id,
        "campaign": campaign,
        "app_id": app_id,
        "ad_token": ad_token,
        "bid_price": bid_price,
        "supply_name": supply,
        "ordinal_view": ordinal_view,
        "bid_id": bid_id,
        "hbp_request": hbp_request,
        "is_hbp_responded_200": hbp_response_flag
    }

    return info


def request_hb_win_notification(supply, ordinal_view, pub_app_id=common_test_app, sdk_v=test_default_sdk_version,
                                placement_ref_id=common_test_placement, test_device_id=gen_device_id(36),
                                ads_retry_mode='kraken', platform='ios', rtb=meister_rtb_ids, ads_debug=None):
    up_responses = request_hbp(supply, ordinal_view, pub_app_id, placement_ref_id, test_device_id=test_device_id,
                               sdk_v=sdk_v, ads_retry_mode=ads_retry_mode, platform=platform, rtb=rtb,
                               ads_debug=ads_debug, debug='jaeger')
    event_id = up_responses['ads_response']['ads'][0]['ad_markup']['id']
    campaign = up_responses['ads_response']['ads'][0]['ad_markup']['campaign']
    app_id = up_responses['ads_response']['ads'][0]['ad_markup']['app_id']
    ad_token = up_responses['ads_response']['ads'][0]['ad_markup']['ad_token']
    bid_token = up_responses['ads_response']['ads'][0]['ad_markup']['bid_token']
    hbp_request = up_responses['hbp_request']
    hbp_response = up_responses['hbp_response']
    hbp_response_flag = up_responses['is_hbp_responded_200']
    bid_price = None
    bid_id = None
    ordinal_view = None

    if hbp_response_flag:
        if supply == 'admob':
            notification_token = hbp_response['seatbid'][0]['bid'][0]['ext']['event_notification_token']['payload']
            # Send win notification
            request_hbp('admob', 1, status_code=1, notification_token=notification_token, post_retry=False,
                        ads_retry_mode='meister', platform=platform, rtb=ext1_non_test_mode_kraken_rtb_ids_vast)
        else:
            nurl = up_responses['hbp_response']['seatbid'][0]['bid'][0]['nurl']
            r = get(nurl.replace('${AUCTION_PRICE}', '5.6')
                    .replace(hbp_ssl_host, hbp_host)
                    .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_price = up_responses['hbp_response']['seatbid'][0]['bid'][0]['price']
            ext = decode_ext(url=nurl)
            ordinal_view = ext['ordinal']
            bid_id = ext['bid']

    info = {
        "event_id": event_id,
        "campaign": campaign,
        "app_id": app_id,
        "ad_token": ad_token,
        "bid_token": bid_token,
        "bid_price": bid_price,
        "supply_name": supply,
        "ordinal_view": ordinal_view,
        "bid_id": bid_id,
        "hbp_request": hbp_request,
        "is_hbp_responded_200": hbp_response_flag
    }

    return info


def request_hb_loss_notification(supply, ordinal_view, pub_app_id=common_test_app, sdk_v=test_default_sdk_version,
                                 placement_ref_id=common_test_placement, test_device_id=gen_device_id(36),
                                 ads_retry_mode='kraken', platform='ios', ads_debug=None):
    up_responses = request_hbp(supply, ordinal_view, pub_app_id, placement_ref_id, test_device_id=test_device_id,
                               sdk_v=sdk_v, ads_retry_mode=ads_retry_mode, platform=platform, ads_debug=ads_debug)
    event_id = up_responses['ads_response']['ads'][0]['ad_markup']['id']
    campaign = up_responses['ads_response']['ads'][0]['ad_markup']['campaign']
    app_id = up_responses['ads_response']['ads'][0]['ad_markup']['app_id']
    ad_token = up_responses['ads_response']['ads'][0]['ad_markup']['ad_token']
    bid_token = up_responses['ads_response']['ads'][0]['ad_markup']['bid_token']
    hbp_request = up_responses['hbp_request']
    hbp_response_flag = False
    bid_price = None
    bid_id = None
    ordinal_view = None

    if up_responses['hbp_response'] is not None:
        lurl = up_responses['hbp_response']['seatbid'][0]['bid'][0]['lurl']
        r = get(lurl.replace('${AUCTION_LOSS}', '1').replace('${AUCTION_MBR}', '2').replace('${AUCTION_PRICE}', '1')
                .replace(hbp_ssl_host, hbp_host)
                .replace(scrat_notification_host_ssl, scrat_notification_host))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        bid_price = up_responses['hbp_response']['seatbid'][0]['bid'][0]['price']
        ext = decode_ext(url=lurl)
        ordinal_view = ext['ordinal']
        bid_id = ext['bid']
        hbp_response_flag = True

    info = {
        "event_id": event_id,
        "campaign": campaign,
        "app_id": app_id,
        "ad_token": ad_token,
        "bid_token": bid_token,
        "bid_price": bid_price,
        "supply_name": supply,
        "ordinal_view": ordinal_view,
        "bid_id": bid_id,
        "hbp_request": hbp_request,
        "is_hbp_responded_200": hbp_response_flag
    }

    return info


def post_hbp_request(endpoint, json, headers):
    r = post(endpoint, json=json, headers=headers)
    if r.status_code == HTTPStatus.NO_CONTENT:
        r = post(endpoint, json=json, headers=headers)

    return r


def post_hbp_request_no_retry(endpoint, json, headers):
    r = post(endpoint, json=json, headers=headers)

    return r


def verify_real_time_token(token=None):
    if token is None:
        token = ''
    url = realtime_token_verify_endpoint_qa + '?token=' + token
    r = post(url, json=None, headers=platform_headers())

    return r


def encode_real_time_token(json_token=None):
    if isinstance(json_token, dict):
        json_token = dict_to_str(json_token)

    if json_token is None or not isinstance(json_token, str):
        raise Exception("The json_token must be a string!")
    else:
        gzip_token = gzip.compress(json_token.encode('utf-8'))
        base64_token = base64.b64encode(gzip_token).decode('utf-8')
        token = '3:' + base64_token

        return token


def decode_real_time_adunit(origin_str):
    if origin_str is None or not isinstance(origin_str, str):
        raise Exception("The origin_str must be a string!")
    else:
        base64_decoded_str = base64.b64decode(origin_str)
        gunzipped_str = gzip.decompress(base64_decoded_str).decode('utf-8')
        adunit_json = json.loads(gunzipped_str)

        return adunit_json


def generate_real_time_token(ordinal_view, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                             test_device_id=gen_device_id(36), sdk_v=test_default_real_time_sdk_version, banner=False,
                             no_pre_cache_token=False, ip=ca_us_ip, rtb=meister_rtb_ids, perf=False, platform='ios',
                             coppa=None, gdpr_status='opted_in', is_hb=False, ccpa='opted_in', ads_retry_mode='kraken',
                             sound_enabled=True, existing_precache_bid_token=None, ads_debug=None,
                             config_extension=config_extension_RTA, token_device_id=None, token_ios_device_id=None,
                             token_android_device_id=None, token_app_set_id=None, token_amazon_device_id=None,
                             token_amazon_app_set_id=None, token_windows_device_id=None, override_bid_response_any=None,
                             ext=None):
    if no_pre_cache_token:
        ads_response = {}
        pre_cached_tokens = []
    else:
        if platform == 'android':
            ads_response = request_ads_android(pub_app_id, placement_ref_id, sdk_v=sdk_v, ip=ip, banner=banner,
                                               rtb=rtb, perf=perf, test_android_id=test_device_id, coppa=coppa,
                                               is_hb=is_hb, retry_mode=ads_retry_mode, debug=ads_debug,
                                               override_bid_response_any=override_bid_response_any,
                                               ext=ext)
        elif platform == 'ios':
            ads_response = request_ads_ios(pub_app_id, placement_ref_id, test_ifa=test_device_id, sdk_v=sdk_v, ip=ip,
                                           coppa=coppa, banner=banner, rtb=rtb, perf=perf, is_hb=is_hb,
                                           retry_mode=ads_retry_mode, ext=config_extension, debug=ads_debug,
                                           override_bid_response_any=override_bid_response_any)
        elif platform == 'windows':
            ads_response = request_ads_windows(pub_app_id, placement_ref_id, ifa=test_device_id, sdk_v=sdk_v,
                                               ip=ip, coppa=coppa, banner=banner, rtb=rtb, perf=perf, is_hb=is_hb,
                                               retry_mode=ads_retry_mode, debug=ads_debug,
                                               override_bid_response_any=override_bid_response_any)
        if existing_precache_bid_token is not None:
            bid_token = existing_precache_bid_token
        elif 'sleep' in ads_response['ads'][0]['ad_markup']:
            # Get the bid token by non-test mode from Kraken after the failure of 2-times of ads request retry
            if platform == 'android':
                ads_response = request_ads_android_no_retry(pub_app_id, placement_ref_id, banner=banner, ip=ip,
                                                            test_android_id=test_device_id, sdk_v=sdk_v,
                                                            rtb=ext_non_test_mode_kraken_rtb_ids_vast, perf=perf,
                                                            coppa=coppa, is_hb=is_hb, debug=ads_debug,
                                                            override_bid_response_any=override_bid_response_any)
            elif platform == 'ios':
                ads_response = request_ads_ios_no_retry(pub_app_id, placement_ref_id, test_ifa=test_device_id,
                                                        sdk_v=sdk_v, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                        banner=banner, coppa=coppa, is_hb=is_hb, ip=ip, perf=perf,
                                                        override_bid_response_any=override_bid_response_any,
                                                        debug=ads_debug, ext=config_extension)
            elif platform == 'windows':
                ads_response = request_ads_windows_no_retry(pub_app_id, placement_ref_id, ifa=test_device_id,
                                                            sdk_v=sdk_v, rtb=ext_non_test_mode_kraken_rtb_ids_vast,
                                                            banner=banner, coppa=coppa, is_hb=is_hb, ip=ip, perf=perf,
                                                            override_bid_response_any=override_bid_response_any,
                                                            debug=ads_debug)
            bid_token = ads_response['ads'][0]['ad_markup']['bid_token']
        else:
            bid_token = ads_response['ads'][0]['ad_markup']['bid_token']
        pre_cached_tokens = [bid_token]

    token_json = request_payload.real_time_token_json(pre_cached_tokens=pre_cached_tokens, orinal_view=ordinal_view,
                                                      sdk_user_agent=sdk_v, is_coppa=coppa, gdpr_status=gdpr_status,
                                                      ccpa_status=ccpa, sound_enabled=sound_enabled,
                                                      config_extension=config_extension,
                                                      token_device_id=token_device_id,
                                                      token_ios_device_id=token_ios_device_id,
                                                      token_android_device_id=token_android_device_id,
                                                      token_app_set_id=token_app_set_id,
                                                      token_amazon_device_id=token_amazon_device_id,
                                                      token_amazon_app_set_id=token_amazon_app_set_id,
                                                      token_windows_device_id=token_windows_device_id)
    super_token_v3 = encode_real_time_token(token_json)
    data = {
        "ads_response": ads_response,
        "super_token_v3": super_token_v3
    }

    return data


def request_hbp_with_real_time_token(supply, ordinal_view, pub_app_id=common_test_app, test_device_id=gen_device_id(36),
                                     partner_android_id=None, partner_app_set_id=None, ads_debug=None,
                                     placement_ref_id=common_test_placement, sdk_v=test_default_real_time_sdk_version,
                                     notification_token=None, no_pre_cache_token=False, banner=False, explain=False,
                                     rtb=meister_rtb_ids, ip=ca_us_ip, perf=False, coppa=None, is_hb=False, geo=None,
                                     banner_format=None, is_test=0, platform='ios', gdpr_status='opted_in',
                                     ccpa='opted_in', device_ext=None, ads_retry_mode='kraken', make='Apple',
                                     model='iPhone11,8', ua=None, lmt=0, sound_enabled=True, skadnetids=None,
                                     Content_Type_uft8=None, imp=1, post_retry=True, existing_precache_bid_token=None,
                                     override_bid_response_any=None, config_extension=config_extension_RTA_1, idfv='',
                                     compress=None, stream=False, source=None, x_env=None, atts=0, token_device_id=None,
                                     token_android_device_id=None, token_ios_device_id=None, token_app_set_id=None,
                                     token_amazon_device_id=None, token_amazon_app_set_id=None, header_ip=None,
                                     token_windows_device_id=None, provide_token=None, video_flag=True, ext=None,
                                     banner_flag=True, demoApp_DSPkey=None, demoApp_Response=None, demoApp_Explain=None,
                                     admob_status_code=79, override_bid_price=None,
                                     buyer_creative_id="test_creative_id_854943"):
    if provide_token is not None:
        data = {
            "ads_response": None,
            "super_token_v3": provide_token
        }
    else:
        data = generate_real_time_token(ordinal_view, pub_app_id, placement_ref_id, test_device_id, sdk_v,
                                        no_pre_cache_token=no_pre_cache_token, banner=banner, ip=ip, rtb=rtb, perf=perf,
                                        platform=platform, coppa=coppa, gdpr_status=gdpr_status, is_hb=is_hb, ccpa=ccpa,
                                        ads_retry_mode=ads_retry_mode, sound_enabled=sound_enabled, ads_debug=ads_debug,
                                        existing_precache_bid_token=existing_precache_bid_token,
                                        config_extension=config_extension,
                                        token_device_id=token_device_id,
                                        token_ios_device_id=token_ios_device_id,
                                        token_android_device_id=token_android_device_id,
                                        token_app_set_id=token_app_set_id,
                                        token_amazon_device_id=token_amazon_device_id,
                                        token_amazon_app_set_id=token_amazon_app_set_id,
                                        token_windows_device_id=token_windows_device_id,
                                        override_bid_response_any=override_bid_response_any,
                                        ext=ext)

    if perf:
        return data['super_token_v3']

    endpoint = get_hbp_partner_endpoint(supply)
    req = request_payload.hbp_partner(supply, pub_app_id, placement_ref_id, ifa=test_device_id, ip=ip,
                                      android_id=partner_android_id, app_set_id=partner_app_set_id,
                                      banner_format=banner_format, bid_token=data['super_token_v3'], idfv=idfv,
                                      platform=platform, notification_token=notification_token, make=make,
                                      model=model, is_test=is_test, device_ext=device_ext, geo=geo, ua=ua, lmt=lmt,
                                      skadnetids=skadnetids, imp=imp, atts=atts, status_code=admob_status_code,
                                      buyer_creative_id=buyer_creative_id, video_flag=video_flag,
                                      banner_flag=banner_flag)

    hbp_header = hbp_headers(debug='jaeger' if explain else None, openrtb='2.5', sdk_version=sdk_v, src_ip=ip if ip else header_ip,
                             rtb_selector=rtb, Content_Type_uft8=Content_Type_uft8, accept_encoding=compress,
                             content_encoding=compress, override_bid_response_any=override_bid_response_any,
                             Source=source, X_Env=x_env, demoApp_DSPkey=demoApp_DSPkey,
                             demoApp_Response=demoApp_Response, demoApp_Explain=demoApp_Explain,
                             override_bid_price=override_bid_price)
    gzip_length = 0
    if compress == 'gzip':
        res = post_gzip(endpoint, data=gzip_encode(req), headers=hbp_header, stream=stream)
        r = res[0]
        gzip_length = res[1]
    else:
        r = post(endpoint, json=req, headers=hbp_header)
    if post_retry and (r.status_code == HTTPStatus.NO_CONTENT or not is_json(r.text)):
        hbp_header = hbp_headers(debug='jaeger' if explain else None, openrtb='2.5', sdk_version=sdk_v,
                                 src_ip=ip, Content_Type_uft8=Content_Type_uft8, accept_encoding=compress,
                                 content_encoding=compress, override_bid_response_any=override_bid_response_any,
                                 Source=source, X_Env=x_env)
        if compress == 'gzip':
            r = post_gzip(endpoint, data=gzip_encode(req), headers=hbp_header)
        else:
            r = post(endpoint, json=req, headers=hbp_header)

    if r.status_code == HTTPStatus.OK:
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        responses = {
            "ads_response": dict(data['ads_response']) if data['ads_response'] is not None else None,
            "hbp_response": dict(response_payload),
            "hbp_request": dict(req),
            "hbp_request_headers": dict(hbp_header),
            "hbp_response_headers": dict(r.headers),
            "is_hbp_responded_200": True,
            "super_token": data['super_token_v3'],
            "gzip_length": gzip_length
        }
    else:
        responses = {
            "ads_response": dict(data['ads_response']) if data['ads_response'] is not None else None,
            "hbp_response": None,
            "hbp_request": dict(req),
            "hbp_request_headers": dict(hbp_header),
            "hbp_response_headers": dict(r.headers),
            "is_hbp_responded_200": False,
            "super_token": data['super_token_v3'],
            "hbp_response_status_code": r.status_code,
            "gzip_length": gzip_length
        }

    return responses


def request_realtime_win_notification(supply, ordinal_view, pub_app_id=common_test_app, ads_retry_mode='kraken',
                                      test_device_id=gen_device_id(36), placement_ref_id=common_test_placement,
                                      sdk_v=test_default_real_time_sdk_version, notification_token=None,
                                      no_pre_cache_token=False, banner=False, explain=False, rtb=meister_rtb_ids,
                                      ip=ca_us_ip, perf=False, banner_format=None, is_test=0, platform='ios',
                                      existing_precache_bid_token=None, ads_debug=None):
    up_responses = request_hbp_with_real_time_token(supply, ordinal_view, pub_app_id, placement_ref_id=placement_ref_id,
                                                    test_device_id=test_device_id, sdk_v=sdk_v, is_test=is_test,
                                                    no_pre_cache_token=no_pre_cache_token, platform=platform,
                                                    rtb=rtb, ip=ip, banner=banner, banner_format=banner_format,
                                                    explain=explain, notification_token=notification_token,
                                                    perf=perf, ads_retry_mode=ads_retry_mode, ads_debug=ads_debug,
                                                    existing_precache_bid_token=existing_precache_bid_token)
    if no_pre_cache_token:
        event_id = None
        campaign = None
        app_id = None
        ad_token = None
        bid_token = None
    else:
        event_id = up_responses['ads_response']['ads'][0]['ad_markup']['id']
        campaign = up_responses['ads_response']['ads'][0]['ad_markup']['campaign']
        app_id = up_responses['ads_response']['ads'][0]['ad_markup']['app_id']
        ad_token = up_responses['ads_response']['ads'][0]['ad_markup']['ad_token']
        bid_token = up_responses['ads_response']['ads'][0]['ad_markup']['bid_token']
    hbp_request = up_responses['hbp_request']
    hbp_response_flag = up_responses['is_hbp_responded_200']
    hbp_response = up_responses['hbp_response']
    bid_price = None
    bid_id = None
    ordinal_view = None
    ext = None
    super_token = up_responses['super_token']

    if hbp_response_flag:
        if supply == 'admob':
            notification_token = hbp_response['seatbid'][0]['bid'][0]['ext']['event_notification_token']['payload']
            # Send win notification
            request_hbp('admob', 1, status_code=1, notification_token=notification_token, post_retry=False,
                        ads_retry_mode='meister', platform=platform, debug='jaeger', rtb=ext1_non_test_mode_kraken_rtb_ids_vast)
        else:
            nurl = up_responses['hbp_response']['seatbid'][0]['bid'][0]['nurl']
            if supply == 'max':
                # add second_highest_price={AUCTION_MIN_BID_TO_WIN} in notification url, this is only for MAX
                r = get(nurl.replace('${AUCTION_PRICE}', '5.6').replace('${AUCTION_MINIMUM_BID_TO_WIN}', '5.3').replace(
                    hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            else:
                r = get(nurl.replace('${AUCTION_PRICE}', '5.6')
                        .replace(hbp_ssl_host, hbp_host)
                        .replace(scrat_notification_host_ssl, scrat_notification_host))
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            bid_price = up_responses['hbp_response']['seatbid'][0]['bid'][0]['price']
            ext = decode_ext(url=nurl)
            ordinal_view = ext['ordinal']
            bid_id = ext['bid']
    info = {
        "event_id": event_id,
        "campaign": campaign,
        "app_id": app_id,
        "ad_token": ad_token,
        "bid_token": bid_token,
        "bid_price": bid_price,
        "supply_name": supply,
        "ordinal_view": ordinal_view,
        "bid_id": bid_id,
        "hbp_request": hbp_request,
        "hbp_response": hbp_response,
        "is_hbp_responded_200": hbp_response_flag,
        "super_token": super_token,
        'ext': ext
    }

    return info


def get_bid_request_obj_from_jaeger_explain(jaeger_response=None, rtb_ids=None, content='PayLoad'):
    if jaeger_response is None or not isinstance(jaeger_response, dict):
        raise Exception("The jaeger_response must be a dict!")

    if rtb_ids is None:
        bid_requests = jaeger_response['ext']['debug']['auction_result']['bid_requests']
        random_rtb_id = random.choice(list(bid_requests.keys()))
        return bid_requests[random_rtb_id][content]

    if isinstance(rtb_ids, list):
        rtb_list = rtb_ids
    else:
        rtb_list = rtb_ids.split(',')

    for rtb in rtb_list:
        if rtb in meister_rtb_ids_list:
            bid_requests = jaeger_response['ext']['debug']['auction_result']['bid_requests']
            return bid_requests[list(bid_requests.keys())[0]][content]

    if len(rtb_list) == 1:
        rtb_id = rtb_list[0]
        return jaeger_response['ext']['debug']['auction_result']['bid_requests'][rtb_id][content]
    elif len(rtb_list) == 2:
        if env == 'ci':
            rtb_id = rtb_list[0]
        elif env == 'qa' or env == 'regression':
            rtb_id = rtb_list[1]
        return jaeger_response['ext']['debug']['auction_result']['bid_requests'][rtb_id][content]
    else:
        bid_requests = jaeger_response['ext']['debug']['auction_result']['bid_requests']
        random_rtb_id = random.choice(list(bid_requests.keys()))
        return bid_requests[random_rtb_id][content]


def get_bid_request_obj_from_hbp_explain(hbp_response=None, rtb_ids=None, content='PayLoad'):
    if hbp_response is None or not isinstance(hbp_response, dict):
        raise Exception("The hbp_response must be a dict!")

    if rtb_ids is None:
        bid_requests = hbp_response['ext']['debug']['auction_result']['bid_requests']
        random_rtb_id = random.choice(list(bid_requests.keys()))
        return bid_requests[random_rtb_id][content]

    rtb_list = rtb_ids.split(',')

    for rtb in rtb_list:
        if rtb in meister_rtb_ids_list:
            bid_requests = hbp_response['ext']['debug']['auction_result']['bid_requests']
            return bid_requests[list(bid_requests.keys())[0]][content]

    if len(rtb_list) == 1:
        rtb_id = rtb_list[0]
        return hbp_response['ext']['debug']['auction_result']['bid_requests'][rtb_id][content]
    elif len(rtb_list) == 2:
        if env == 'ci':
            rtb_id = rtb_list[0]
        elif env == 'qa' or env == 'regression':
            rtb_id = rtb_list[1]
        return hbp_response['ext']['debug']['auction_result']['bid_requests'][rtb_id][content]
    else:
        bid_requests = hbp_response['ext']['debug']['auction_result']['bid_requests']
        random_rtb_id = random.choice(list(bid_requests.keys()))
        return bid_requests[random_rtb_id][content]


def get_bid_response_obj_from_jaeger_explain(jaeger_response=None, rtb_ids=None):
    if jaeger_response is None or not isinstance(jaeger_response, dict):
        raise Exception("The jaeger_response must be a dict!")

    if rtb_ids is None:
        bid_response = jaeger_response['ext']['debug']['auction_result']['bid_response_details']
        for x in range(len(bid_response.keys())):
            random_rtb_id = list(bid_response.keys())[x]
            if 'seatbid' in bid_response[random_rtb_id]:
                return bid_response[random_rtb_id]
            else:
                continue

    if isinstance(rtb_ids, list):
        rtb_list = rtb_ids
    else:
        rtb_list = rtb_ids.split(',')

    for rtb in rtb_list:
        if rtb in meister_rtb_ids_list:
            bid_response = jaeger_response['ext']['debug']['auction_result']['bid_response_details']
            return bid_response

    if len(rtb_list) == 1:
        rtb_id = rtb_list[0]
        return jaeger_response['ext']['debug']['auction_result']['bid_response_details'][rtb_id]
    elif len(rtb_list) == 2:
        if env == 'ci':
            rtb_id = rtb_list[0]
        elif env == 'qa' or env == 'regression':
            rtb_id = rtb_list[1]
        return jaeger_response['ext']['debug']['auction_result']['bid_response_details'][rtb_id]
    else:
        bid_response = jaeger_response['ext']['debug']['auction_result']['bid_response_details']
        random_rtb_id = random.choice(list(bid_response.keys()))
        return bid_response[random_rtb_id]


def get_ext_debug_from_jaeger_explain(response_payload=None, message_type='ex-jaeger-transaction'):
    if response_payload is None or not isinstance(response_payload, dict):
        raise Exception("The response payload must be a dict!")
    ext_debug = response_payload['ext']['debug']
    return ext_debug[message_type]



def get_device_info(response=None):
    if response is None or not isinstance(response, dict):
        raise Exception("The response must be a dict!")
    return response['ext']['debug']['auction_result']['device_info']


def get_bflat_exp_list(type=None, imp_type=None):
    exp_list1 = []
    exp_list2 = []
    r = get(bflat_get_exp_list_endpoint_qa)
    response_payload = r.json()
    for key in response_payload.keys():
        if type is None and imp_type is None:
            exp_list2.append(key)
        elif type in key and imp_type is None:
            num = key.split('_')[1]
            exp_list1.append(int(num))
    if type is not None:
        exp_list = exp_list1
    else:
        exp_list = exp_list2
    return exp_list


def decode_admob_event_token_legacy(ori_token, event_id_end=16, app_id_end=32, bid_id_end=54, mode_end=55):
    tokens = {}
    if '2:' in ori_token:
        token = ori_token.split('2:')[1]
    # eventIDEnd = 16, appIDEnd = 32, v3BidIDEnd = 48, v3ModeEnd = 49, v3Prefix   = "3:", ordinalMax = 16
    if '3:' in ori_token:
        token = ori_token.split('3:')[1]
        bid_id_end = 48
        mode_end = 49

    bts = bytes(token, encoding="utf8")
    is_test, is_internal = decode_modes(bts[bid_id_end:mode_end])

    bid_id_str = bts[app_id_end:bid_id_end]
    bid_id_bytes = decode_base64(bid_id_str)

    app_id_str = bts[event_id_end:app_id_end]
    app_id_bytes = decode_base64(app_id_str)

    event_id_str = bts[:event_id_end]
    event_id_bytes = decode_base64(event_id_str)

    ordinal_str = bts[mode_end:]

    if '2:' in ori_token:
        bid_id = str(uuid.UUID(bytes=bid_id_bytes))
    if '3:' in ori_token:
        bid_id = str(ObjectId(bid_id_bytes))
    tokens["is_test"] = is_test
    tokens["adv_is_internal"] = is_internal
    tokens["bidid"] = bid_id
    tokens["event_id"] = str(ObjectId(event_id_bytes))
    tokens["pub_app_obj_id"] = str(ObjectId(app_id_bytes))
    tokens["n_ordinal_view"] = int(ordinal_str, 16)

    return tokens


def decode_admob_event_token(token):
    param = {
        "token": token
    }
    r = get(hbp_admob_event_token_decoder_qa, params=param)
    assert_response_status_code(r.status_code, HTTPStatus.OK)
    response_payload = r.json()

    return response_payload
