import sys
from http import HTTPStatus
from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from collections import defaultdict
from utils.behaviors import generate_real_time_token, encode_real_time_token


def load_json_payload(payload_path):
    with open(payload_path, 'r') as payload:
        return json.load(payload)


def get_rtb(env, types):
    if env == 'ci':
        rtb = types.split(',')[0]
    elif env == 'qa' or env == 'perf':
        rtb = types.split(',')[1]

    return rtb


# Get method name
def get_method_name():
    return format(sys._getframe().f_code.co_name)


# Get class name
def get_class_name(x):
    return format(x.__class__.__name__)


def multi_dismensions(n, type):
    if n <= 1:
        return type()
    return defaultdict(lambda: multi_dismensions(n - 1, type))


class LocustBehaviors:

    def request_ads(self, x, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                    test_ifa=gen_device_id(),
                    rtb=meister_rtb_ids, hb=True, banner=False, ip=ca_us_ip,
                    sdk_v='Vungle/6.10.1', locust_call=False, nick_name=None):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_ref_id, ifa=test_ifa, header_bidding=hb,
                                            banner=banner)
        if locust_call:
            r = x.client.post(ads_path, json=req, headers=platform_headers(rtb_selector=rtb, src_ip=ip,
                                                                                      sdk_version=sdk_v),
                              name=nick_name, verify=False)

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            return r
        else:
            r = post(ads_v5_endpoint_qa0, json=req, headers=platform_headers(rtb_selector=rtb, src_ip=ip,

                                                                             sdk_version=sdk_v))
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            return response_payload

    def super_token(self, ordinal_view_count, pub_app_id, placement_ref_id, rtb=meister_rtb_ids,
                    test_ifa=gen_device_id(), banner=False, sdk_v='Vungle/6.10.1'):

        ads_response = self.request_ads('1', pub_app_id, placement_ref_id, rtb=rtb, test_ifa=test_ifa, banner=banner,
                                        sdk_v=sdk_v)

        bid_token = ads_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        return super_token

    def request_hbp(self, x, supply, super_token, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                    test_ifa=gen_device_id(36), is_test=0, nick_name=None, ):

        endpoint = get_hbp_partner_endpoint(supply, perf=True)
        req = request_payload.hbp_partner(supply, pub_app_id, placement_ref_id, ifa=test_ifa, bid_token=super_token,
                                          is_test=is_test)
        r = x.client.post(endpoint, json=req, headers=hbp_headers(openrtb='2.5'), name=nick_name)
        assert_response_status_code_in(r.status_code, HTTPStatus.NO_CONTENT, HTTPStatus.OK)

    def request_bflat(self, x, event_id='604777abcf9272000148c0dd', bidid='82317317-7e72-4927-8a0f-28f4b9c41251',
                      pub_app_id=common_test_app, placement=common_test_placement, nick_name=True, experiment=None):
        req = request_payload.bflat_bid_request(pub_app_id, placement, event_id=event_id, bidid=bidid,
                                                experiment=experiment)
        r = x.client.post(bflat_bid_request, json=req, name=nick_name)
        assert_response_status_code(r.status_code, HTTPStatus.OK)

    def request_ads_android(self, x, pub_app_id=android_common_test_app, placement_ref_id=android_common_test_placement,
                            skadnetwork_ids=None, android_id=gen_device_id(),
                            rtb=meister_rtb_ids, hb=True, banner=False, sdk_v='VungleDroid/6.10.0',
                            locust_call=False, src_ip=non_eu_country_ip):

        req = request_payload.jaeger_v5_android(pub_app_id, placement_ref_id, skadnetwork_ids,
                                                android_id, header_bidding=hb, banner=banner)
        if locust_call:
            r = x.client.post(ads_v5_endpoint_qa0, json=req, headers=platform_headers(rtb_selector=rtb,
                                                                                      sdk_version=sdk_v))
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            return r

        else:
            r = post(ads_v5_endpoint_qa0, json=req, headers=platform_headers(rtb_selector=rtb, sdk_version=sdk_v,
                                                                             src_ip=src_ip))
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            return response_payload

    def super_token_android(self, ordinal_view_count, pub_app_id, placement_ref_id, rtb=meister_rtb_ids,
                            android_id=gen_device_id(), banner=False, sdk_v='VungleDroid/6.10.0',
                            src_ip=non_eu_country_ip):

        ads_response = self.request_ads_android('1', pub_app_id, placement_ref_id, rtb=rtb, android_id=android_id,
                                                banner=banner, sdk_v=sdk_v, src_ip=src_ip)
        bid_token = ads_response['ads'][0]['ad_markup']['bid_token']
        bid_tokens_with_ordinal_view_count = bid_token + ':' + str(ordinal_view_count)
        super_token = "2:" + base64.b64encode(bid_tokens_with_ordinal_view_count.encode('ascii')).decode('ascii')
        return super_token

    def get_real_time_token(self, ordinal_view, pub_app_id=common_test_app,
                            placement_ref_id=common_test_placement, test_ifa=gen_device_id(36),
                            sdk_v=test_default_real_time_sdk_version, banner=False, no_pre_cache_token=False,
                            perf=False):

        data = generate_real_time_token(ordinal_view, pub_app_id, placement_ref_id, test_ifa, sdk_v, banner=banner,
                                        no_pre_cache_token=no_pre_cache_token, perf=perf)
        return data['super_token_v3']


    def request_hbp_with_real_time_token_with_non_precached_token(self, x, supply, ordinal_view,
                                                                  pub_app_id=common_test_app,
                                                                  placement_ref_id=common_test_placement,
                                                                  test_ifa=gen_device_id(36),
                                                                  sdk_v=test_default_real_time_sdk_version,
                                                                  notification_token=None, rtb=meister_rtb_ids,
                                                                  name=None, token=None, is_test=0):

        endpoint = get_hbp_partner_endpoint(supply, perf=True)
        if token is None:
            token_json = request_payload.real_time_token_json(pre_cached_tokens=[], orinal_view=ordinal_view,
                                                              sdk_user_agent=sdk_v)
            super_token_v3 = encode_real_time_token(token_json)
        else:
            super_token_v3 = token
        req = request_payload.hbp_partner(supply, pub_app_id, placement_ref_id, ifa=test_ifa,
                                          bid_token=super_token_v3, notification_token=notification_token,
                                          is_test=is_test)

        r = x.client.post(endpoint, json=req, headers=hbp_headers(openrtb='2.5', rtb_selector=rtb), name=name)
        assert_response_status_code_in(r.status_code, HTTPStatus.OK, HTTPStatus.NO_CONTENT)

    def request_hbp_with_real_time_token(self, x, supply, realTime_token, pub_app_id=common_test_app,
                                         placement_ref_id=common_test_placement, test_ifa=gen_device_id(36)
                                         , notification_token=None, name=None, is_test=0, rtb=meister_rtb_ids):
        endpoint = get_hbp_partner_endpoint(supply, perf=True)
        # endpoint = 'http://internal-a06907b3a41964bc881660966bed9cec-249035833.us-west-2.elb.amazonaws.com:7000/bid/t/34dec8a'
        req = request_payload.hbp_partner(supply, pub_app_id, placement_ref_id, ifa=test_ifa,
                                          bid_token=realTime_token, notification_token=notification_token,
                                          is_test=is_test)


        r = x.client.post(endpoint, json=req,
                          headers=hbp_headers(openrtb='2.5', sdk_version=test_default_real_time_sdk_version, rtb_selector=rtb), name=name)

        assert_response_status_code_in(r.status_code, HTTPStatus.OK, HTTPStatus.NO_CONTENT)

    def get_super_tokens(self):
        super_tokens = {}

        performance_file_root = get_root + '/performance/'

        files = os.listdir(performance_file_root)
        for i in files:
            if test_common_os in i:
                token_type = i[len(test_common_os) + 1:]
                token_type = token_type[:-15]
                _json_bid_token_file = performance_file_root + '/%s' % i

                if os.path.exists(_json_bid_token_file):

                    with open(_json_bid_token_file) as config_file:
                        config = json.load(config_file)
                    if token_type in ["real_time_only", "hybrid", "pre_cache"]:
                        super_tokens[token_type] = {
                            token_type + "_kraken_video": config["kraken"]["video"],
                            token_type + "_kraken_banner": config["kraken"]["banner"],
                            token_type + "_kraken_mrec": config["kraken"]["mrec"],
                            token_type + "_meister_video": config["meister"]["video"],
                            token_type + "_meister_banner": config["meister"]["banner"],
                            token_type + "_meister_mrec": config["meister"]["mrec"]

                        }
                    else:
                        super_tokens[token_type] = {
                            # "Vungle_Mraid_Kraken_Fullscreen_Token": config["vungle_mraid"]["Kraken"]["fullscreen"],
                            # "Vungle_Mraid_Kraken_Banner_Token": config["vungle_mraid"]["Kraken"]["banner"],
                            # "Vungle_Mraid_Kraken_image_mrec_Token": config["vungle_mraid"]["Kraken"]["image_mrec"],
                            # "Vungle_Mraid_Kraken_video_mrec_Token": config["vungle_mraid"]["Kraken"]["video_mrec"],
                            "Vungle_Mraid_Meister_Fullscreen_Token": config["vungle_mraid"]["meister"]["fullscreen"],
                            # "Vungle_Mraid_Meister_Banner_Token": config["vungle_mraid"]["meister"]["banner"],
                            "Vungle_Mraid_Meister_image_mrec_Token": config["vungle_mraid"]["meister"]["image_mrec"],
                            "Vungle_Mraid_Meister_video_mrec_Token": config["vungle_mraid"]["meister"]["video_mrec"],
                            # # "Legacy_Meister_video_Token": config["legacy"]["meister"]["video"],
                            # "programmatic_vast_Kraken_video_Token": config["programmatic_vast"]["Kraken"]["video"],
                            # "programmatic_mraid_Kraken_banner_Token": config["programmatic_mraid"]["Kraken"]["banner"]
                        }
        return super_tokens


if __name__ == '__main__':
    #     multiple_tokens = LocustBehaviors().get_super_tokens()["multiple_cache"]
    #     non_multiple_tokens = LocustBehaviors().get_super_tokens()["non_multiple_cache"]
    #     LocustBehaviors().request_hbp(supply="mopub", super_token=non_multiple_tokens["Vungle_Mraid_Kraken_Fullscreen_Token"],
    #                      pub_app_id=common_test_app, test_ifa=test_mode_device_id, is_test=1,
    #                      placement_ref_id=common_test_placement, x='a', nick_name='HBP')
    realtime_tokens = LocustBehaviors().get_super_tokens()['real_time_only']
    # multiple_tokens = LocustBehaviors().get_super_tokens()["multiple_cache"]
    # non_multiple_tokens = LocustBehaviors().get_super_tokens()["non_multiple_cache"]
    realtime_token = "3:H4sIAHiF1GAC/3WRW0sDMRCF/4rkWdrutl4Q+rBKn0RBBUFFwnQzZmOzScxltbb7351sFYriWzhnbufLhnl8SxgiOzvYsNqaFyU5fkQ0QVlDIruoFjeVqs4v5XXz0F6tq/JWP8r5nB0eMOuFMqB5p/CdaouCNOexhrpBwaNd0RjSn1i5LYuFc9S2radwCqk4eVVm1srJ5GjpJHumxiBWPAX0HCSafA+7T0ZqHB+PimI0YT3VCOxUjcOtS4gR/ZoH6KgHDSw1CnKiT0iVGoxMNCnPQZPytVG1yD+tGbQqKBjfNVTVgMpuZ3UiX2OHOmehpSXJ+yw2TAUelEBtQfxdGQSvwQsOHSidvT3LJvO7o8+BiHjYpSX6tYPhESLElMEx6yKBVGYIL4Xz//m7HX5gw1xaahUa9FluMQTiwInSz5dmmt88aFTrctxyWs6ms2nf91+wqzTfEwIAAA=="

    LocustBehaviors().request_hbp_with_real_time_token_with_non_precached_token(supply='mopub', ordinal_view=11,
                                                                   token=realtime_token,
                                                                   pub_app_id=common_test_app,
                                                                   test_ifa=gen_device_id(36),
                                                                   placement_ref_id=common_test_pre_cache_mrec_placement,
                                                                   x='a',
                                                                   name='HBP+jaeger+Bflat')