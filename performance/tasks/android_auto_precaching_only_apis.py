from locust import TaskSet
from performance.common.config import *
from performance.common.util import get_rtb, LocustBehaviors as LB
from utils.common import gen_device_id

multiple_tokens = LB().get_super_tokens()["multiple_cache"]
non_multiple_tokens = LB().get_super_tokens()["non_multiple_cache"]


class vungle_mraid(TaskSet):

    # non multiple cache valid token
    def hb_full_screen_kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Kraken_Fullscreen_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement,
                         test_ifa=test_mode_device_id, x=self, nick_name='pre_cached/HBP+Bflat')

    def hb_full_screen_meister(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Meister_Fullscreen_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement, x=self,
                         nick_name='pre_cached/HBP+Bflat',
                         test_ifa=gen_device_id(36))

    def hb_banner_kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Kraken_Banner_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement,
                         test_ifa=test_mode_device_id, x=self, nick_name='pre_cached/HBP+Bflat')

    def hb_banner_meister(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Meister_Banner_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement,
                         test_ifa=gen_device_id(36), x=self, nick_name='pre_cached/HBP+Bflat')

    def hb_image_mrec_kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Kraken_image_mrec_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_image_mrec_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP+Bflat')

    def hb_image_mrec_meister(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Kraken_image_mrec_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_image_mrec_test_placement, x=self, test_ifa=gen_device_id(36),
                         nick_name='pre_cached/HBP+Bflat')

    def hb_video_mrec_kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Kraken_video_mrec_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_video_mrec_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP+Bflat')

    def hb_video_mrec_meister(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Meister_video_mrec_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_video_mrec_test_placement, x=self, test_ifa=gen_device_id(36),
                         nick_name='pre_cached/HBP+Bflat')

    # only call hbp

    def hb_full_screen_hbp_kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Kraken_Fullscreen_Token"],
                         pub_app_id=android_common_test_app, is_test=1,
                         placement_ref_id=android_common_test_placement,
                         test_ifa=test_mode_device_id, x=self, nick_name='pre_cached/HBP')

    def hb_full_screen_hbp_meister(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Meister_Fullscreen_Token"],
                         pub_app_id=android_common_test_app, is_test=1,
                         placement_ref_id=android_common_test_placement, x=self,
                         nick_name='HBP',
                         test_ifa=gen_device_id(36))

    def hb_banner_hbp_kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Kraken_Banner_Token"],
                         pub_app_id=android_common_test_app, is_test=1,
                         placement_ref_id=android_common_test_banner_placement,
                         test_ifa=test_mode_device_id, x=self, nick_name='pre_cached/HBP')

    def hb_banner_hbp_meister(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Meister_Banner_Token"],
                         pub_app_id=android_common_test_app, is_test=1,
                         placement_ref_id=android_common_test_banner_placement,
                         test_ifa=gen_device_id(36), x=self, nick_name='pre_cached/HBP')

    def hb_image_mrec_hbp_kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Kraken_image_mrec_Token"],
                         pub_app_id=android_common_test_app, is_test=1,
                         placement_ref_id=android_image_mrec_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    def hb_image_mrec_hbp_meister(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Kraken_image_mrec_Token"],
                         pub_app_id=android_common_test_app, is_test=1,
                         placement_ref_id=android_image_mrec_test_placement, x=self, test_ifa=gen_device_id(36),
                         nick_name='pre_cached/HBP')

    def hb_video_mrec_hbp_kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Kraken_video_mrec_Token"],
                         pub_app_id=android_common_test_app, is_test=1,
                         placement_ref_id=android_video_mrec_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    def hb_video_mrec_hbp_meister(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Vungle_Mraid_Meister_video_mrec_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_video_mrec_test_placement, is_test=1, x=self,
                         test_ifa=gen_device_id(36),
                         nick_name='pre_cached/HBP')

    # multiple cache valid token
    def hb_full_screen_kraken_multiple_cache(self):
        LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["Vungle_Mraid_Kraken_Fullscreen_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement,
                         test_ifa=test_mode_device_id, x=self, nick_name='pre_cached/HBP+Bflat')

    def hb_full_screen_meister_multiple_cache(self):
        LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["Vungle_Mraid_Meister_Fullscreen_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement, x=self, test_ifa=gen_device_id(36),
                         nick_name='pre_cached/HBP+Bflat')

    def hb_banner_kraken_multiple_cache(self):
        LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["Vungle_Mraid_Kraken_Banner_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement,
                         test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP+Bflat')

    def hb_banner_meister_multiple_cache(self):
        LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["Vungle_Mraid_Meister_Banner_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement, test_ifa=gen_device_id(36), x=self,
                         nick_name='pre_cached/HBP+Bflat')

    def hb_image_mrec_kraken_multiple_cache(self):
        LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["Vungle_Mraid_Kraken_image_mrec_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_image_mrec_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP+Bflat')

    def hb_image_mrec_meister_multiple_cache(self):
        LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["Vungle_Mraid_Kraken_image_mrec_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_image_mrec_test_placement, x=self, test_ifa=gen_device_id(36),
                         nick_name='pre_cached/HBP+Bflat')

    def hb_video_mrec_kraken_multiple_cache(self):
        LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["Vungle_Mraid_Kraken_video_mrec_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_video_mrec_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP+Bflat')

    def hb_video_mrec_meister_multiple_cache(self):
        LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["Vungle_Mraid_Meister_video_mrec_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_video_mrec_test_placement, x=self, test_ifa=gen_device_id(36),
                         nick_name='pre_cached/HBP+Bflat')

    # invalid token
    def hb_full_screen_invalid(self):
        LB().request_hbp(supply=PARTNER, super_token=test_common_invalid_token,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement,
                         test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP'
                         )

    def hb_banner_invalid(self):
        LB().request_hbp(supply=PARTNER, super_token=test_common_invalid_token,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement,
                         test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    def hb_image_mrec_invalid(self):
        LB().request_hbp(supply=PARTNER, super_token=test_common_invalid_token,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_image_mrec_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    def hb_video_mrec_invalid(self):
        LB().request_hbp(supply=PARTNER, super_token=test_common_invalid_token,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_video_mrec_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    # expiry token

    def hb_full_screen_expiry(self):
        LB().request_hbp(supply=PARTNER, super_token=test_mode_super_token_v1,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement,
                         test_ifa=test_mode_device_id, x=self, nick_name='pre_cached/HBP')

    def hb_banner_expiry(self):
        LB().request_hbp(supply=PARTNER, super_token=test_mode_super_token_v1,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement,
                         test_ifa=test_mode_device_id, x=self, nick_name='pre_cached/HBP')

    def hb_image_mrec_expiry(self):
        LB().request_hbp(supply=PARTNER, super_token=test_mode_super_token_v1,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_image_mrec_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    def hb_video_mrec_expiry(self):
        LB().request_hbp(supply=PARTNER, super_token=test_mode_super_token_v1,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_video_mrec_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    # support head bidding call jaeger
    def hb_full_screen_jaeger_kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_placement,
                         test_ifa=test_mode_device_id, rtb=test_mode_kraken_rtb_ids, hb=True, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+kraken')

    def hb_full_screen_jaeger_meister(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_placement,
                         hb=True, locust_call=True, x=self, test_ifa=gen_device_id(36),
                         nick_name='pre_cached/jaeger+meister')

    def hb_banner_jaeger_kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_banner_placement,
                         test_ifa=test_mode_device_id, rtb=test_mode_kraken_rtb_ids,
                         banner=True, hb=True, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+kraken')

    def hb_banner_jaeger_meister(self):
        LB().request_ads(pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement,
                         test_ifa=gen_device_id(36), rtb=get_rtb(env, meister_rtb_ids), banner=True,
                         hb=True, locust_call=True, x=self, nick_name='pre_cached/jaeger+meister')

    def hb_image_mrec_jaeger_kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_image_mrec_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=get_rtb(env, test_mode_kraken_rtb_ids), hb=True, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+kraken')

    def hb_image_mrec_jaeger_meister(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_image_mrec_test_placement,
                         hb=True,
                         test_ifa=gen_device_id(36),
                         locust_call=True, x=self, nick_name='pre_cached/jaeger+meister')

    def hb_video_mrec_jaeger_kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_video_mrec_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=get_rtb(env, test_mode_kraken_rtb_ids), hb=True, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+kraken')

    def hb_video_mrec_jaeger_meister(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_video_mrec_test_placement,
                         hb=True,
                         test_ifa=gen_device_id(36), locust_call=True, x=self, nick_name='pre_cached/jaeger+meister')

    # dont support head bidding call jaeger
    def non_hb_full_screen_kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_placement,
                         test_ifa=test_mode_device_id, rtb=test_mode_kraken_rtb_ids, hb=False, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+kraken')

    def non_hb_full_screen_meister(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_placement,
                         hb=False, locust_call=True, x=self, test_ifa=gen_device_id(36),
                         nick_name='pre_cached/jaeger+meister')

    def non_hb_banner_kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_banner_placement,
                         test_ifa=test_mode_device_id, rtb=test_mode_kraken_rtb_ids,
                         banner=True, hb=False, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+kraken')

    def non_hb_banner_meister(self):
        LB().request_ads(pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement,
                         test_ifa=gen_device_id(36), rtb=get_rtb(env, meister_rtb_ids), banner=True,
                         hb=False, locust_call=True, x=self, nick_name='pre_cached/jaeger+meister')

    def non_hb_image_mrec_kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_image_mrec_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=get_rtb(env, test_mode_kraken_rtb_ids), hb=False, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+kraken')

    def non_hb_image_mrec_meister(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_image_mrec_test_placement,
                         hb=False,
                         test_ifa=gen_device_id(36),
                         locust_call=True, x=self, nick_name='pre_cached/jaeger+meister')

    def non_hb_video_mrec_kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_video_mrec_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=get_rtb(env, test_mode_kraken_rtb_ids), hb=False, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+kraken')

    def non_hb_video_mrec_meister(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_video_mrec_test_placement,
                         hb=False,
                         test_ifa=gen_device_id(36), locust_call=True, x=self, nick_name='pre_cached/jaeger+meister')


class legacy(TaskSet):

    # non multiple cache valid token
    # def hb_video_meister(self):
    #     LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Legacy_Meister_video_Token"],
    #                      pub_app_id=android_common_test_app,
    #                      placement_ref_id=android_common_test_placement_legacy, x=self,
    #                      test_ifa=gen_device_id(36), nick_name='pre_cached/HBP+Bflat')

    # multiple cache valid token
    # def hb_video_meister_multiple_cache(self):
    #     LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["Legacy_Meister_video_Token"],
    #                      pub_app_id=android_common_test_app,
    #                      placement_ref_id=android_common_test_placement_legacy, x=self,
    #                      test_ifa=gen_device_id(36), nick_name='pre_cached/HBP+Bflat')

    # only call hbp
    # def hb_video_hbp_meister(self):
    #     LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["Legacy_Meister_video_Token"],
    #                      pub_app_id=android_common_test_app,
    #                      placement_ref_id=android_common_test_placement_legacy, x=self, is_test=1,
    #                      test_ifa=gen_device_id(36), nick_name='pre_cached/HBP')

    # invalid token

    def hb_video_invalid(self):
        LB().request_hbp(supply=PARTNER, super_token=test_common_invalid_token, pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement_legacy, x=self,
                         test_ifa=gen_device_id(36),
                         nick_name='pre_cached/HBP')

    # expiry token

    def hb_video_expiry(self):
        LB().request_hbp(supply=PARTNER, super_token=test_mode_super_token_v1, pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement_legacy, x=self,
                         test_ifa=gen_device_id(36),
                         nick_name='pre_cached/HBP')

    # dont support head bidding call jaeger
    def non_hb_video_meister(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_placement_legacy,
                         test_ifa=gen_device_id(36), hb=True, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+meister')

    # support head bidding call jaeger
    def hb_video_jaeger_meister(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_placement_legacy,
                         test_ifa=gen_device_id(36), hb=False, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+meister')


class programmatic_vast(TaskSet):

    # non multiple cache valid token
    def hb_video_Kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["programmatic_vast_Kraken_video_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP+Bflat')

    # only call hbp
    def hb_video_hbp_Kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["programmatic_vast_Kraken_video_Token"],
                         pub_app_id=android_common_test_app, is_test=1,
                         placement_ref_id=android_common_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    # multiple cache valid token
    def hb_video_Kraken_multiple_cache(self):
        LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["programmatic_vast_Kraken_video_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP+Bflat')

    # invalid token

    def hb_video_Kraken_invalid(self):
        LB().request_hbp(supply=PARTNER, super_token=test_common_invalid_token,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    # expiry token

    def hb_video_Kraken_expiry(self):
        LB().request_hbp(supply=PARTNER, super_token=test_mode_super_token_v1,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    def non_hb_video_Kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_placement,
                         test_ifa=test_mode_device_id, rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_vast), hb=False,
                         locust_call=True,
                         x=self, nick_name='pre_cached/jaeger+kraken')

    # support head bidding
    def hb_video_jaeger_Kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_placement,
                         test_ifa=test_mode_device_id, rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_vast), hb=True,
                         locust_call=True,
                         x=self, nick_name='pre_cached/jaeger+kraken')


class programmatic_mraid(TaskSet):
    # non multiple cache valid token
    def hb_banner_Kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["programmatic_mraid_Kraken_banner_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP+Bflat')

    # def hb_mrec_Kraken(self):
    #     LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["programmatic_mraid_Kraken_mrec_Token"],
    #                      pub_app_id=android_common_test_app,
    #                      placement_ref_id=android_programmatic_mrec_test_placement, test_ifa=test_mode_device_id, x=self
    #                      , nick_name='pre_cached/HBP+Bflat')

    # only call hbp

    def hb_banner_hbp_Kraken(self):
        LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["programmatic_mraid_Kraken_banner_Token"],
                         pub_app_id=android_common_test_app, is_test=1,
                         placement_ref_id=android_common_test_banner_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')
    #
    # def hb_mrec_hbp_Kraken(self):
    #     LB().request_hbp(supply=PARTNER, super_token=non_multiple_tokens["programmatic_mraid_Kraken_mrec_Token"],
    #                      pub_app_id=android_common_test_app, is_test=1,
    #                      placement_ref_id=android_programmatic_mrec_test_placement, test_ifa=test_mode_device_id, x=self
    #                      , nick_name='pre_cached/HBP')


    # multiple cache valid token
    def hb_banner_Kraken_multiple_cache(self):
        LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["programmatic_mraid_Kraken_banner_Token"],
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement, test_ifa=test_mode_device_id,
                         x=self, nick_name='pre_cached/HBP+Bflat')
    #
    # def hb_mrec_Kraken_multiple_cache(self):
    #     LB().request_hbp(supply=PARTNER, super_token=multiple_tokens["programmatic_mraid_Kraken_mrec_Token"],
    #                      pub_app_id=android_common_test_app,
    #                      placement_ref_id=android_programmatic_mrec_test_placement, test_ifa=test_mode_device_id,
    #                      x=self, nick_name='pre_cached/HBP+Bflat')

    # invalid token

    def hb_banner_Kraken_invalid(self):
        LB().request_hbp(supply=PARTNER, super_token=test_common_invalid_token,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    def hb_mrec_Kraken_invalid(self):
        LB().request_hbp(supply=PARTNER, super_token=test_common_invalid_token,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_programmatic_mrec_test_placement, test_ifa=test_mode_device_id,
                         x=self, nick_name='pre_cached/HBP')

    # expiry token

    def hb_banner_Kraken_expiry(self):
        LB().request_hbp(supply=PARTNER, super_token=test_mode_super_token_v1,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_common_test_banner_placement, test_ifa=test_mode_device_id, x=self,
                         nick_name='pre_cached/HBP')

    def hb_mrec_Kraken_expiry(self):
        LB().request_hbp(supply=PARTNER, super_token=test_mode_super_token_v1,
                         pub_app_id=android_common_test_app,
                         placement_ref_id=android_programmatic_mrec_test_placement, test_ifa=test_mode_device_id,
                         x=self, nick_name='pre_cached/HBP')

    def non_hb_banner_Kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_banner_placement,
                         test_ifa=test_mode_device_id,
                         rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_mraid), banner=True, hb=False, locust_call=True,
                         x=self, nick_name='pre_cached/jaeger+kraken')

    def non_hb_mrec_Kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_programmatic_mrec_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_mraid), hb=False, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+kraken')

    # support head bidding call jaeger
    def hb_banner_jaeger_Kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_common_test_banner_placement,
                         test_ifa=test_mode_device_id,
                         rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_mraid), banner=True, hb=True, locust_call=True,
                         x=self, nick_name='pre_cached/jaeger+kraken')

    def hb_mrec_jaeger_Kraken(self):
        LB().request_ads(pub_app_id=android_common_test_app, placement_ref_id=android_programmatic_mrec_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_mraid), hb=True, locust_call=True, x=self,
                         nick_name='pre_cached/jaeger+kraken')

