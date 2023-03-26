from locust import TaskSet
from performance.common.util import LocustBehaviors as LB
from utils.common import gen_device_id
from settings import *
from performance.common.config import PARTNER

realtime_tokens = LB().get_super_tokens()['pre_cache']


class vungle_mraid(TaskSet):


    # request with precached token

    def hb_video_meister_non_precached(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER,
                                              pub_app_id=common_test_app,
                                              test_ifa=gen_device_id(36),
                                              placement_ref_id=common_test_pre_cache_placement, x=self,
                                              name='HBP+jaeger+Bflat')

    def hb_banner_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER, pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["pre_cache_meister_banner"],
                                              placement_ref_id=common_test_pre_cache_banner_placement,
                                              test_ifa=gen_device_id(), x=self,
                                              rtb=hb_meister_rtb_ids,
                                              name='pre cache/HBP+jaeger+meister+Bflat')

    def hb_video_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["pre_cache_meister_video"],
                                              test_ifa=gen_device_id(),
                                              rtb=hb_meister_rtb_ids,
                                              placement_ref_id=common_test_pre_cache_placement, x=self,
                                              name='pre cache/HBP+jaeger+meister+Bflat')

    def hb_mrec_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["pre_cache_meister_mrec"],
                                              test_ifa=gen_device_id(),
                                              rtb=hb_meister_rtb_ids,
                                              placement_ref_id=common_test_pre_cache_mrec_placement, x=self,
                                              name='pre cache/HBP+jaeger+meister+Bflat')

    # request with kraken precached token

    def hb_video_kraken_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              realTime_token=realtime_tokens["pre_cache_kraken_video"],
                                              pub_app_id=common_test_app,
                                              rtb=non_test_mode_kraken_rtb_ids,
                                              test_ifa=gen_device_id(),
                                              placement_ref_id=common_test_pre_cache_placement, x=self,
                                              name='HBP+jaeger+Bflat')

    def hb_banner_kraken_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER, pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["pre_cache_kraken_banner"],
                                              placement_ref_id=common_test_pre_cache_banner_placement,
                                              rtb=non_test_mode_kraken_rtb_ids,
                                              test_ifa=gen_device_id(), x=self,
                                              name='HBP+jaeger+Bflat')

    def hb_mrec_kraken_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["pre_cache_kraken_mrec"],
                                              test_ifa=gen_device_id(),
                                              rtb=non_test_mode_kraken_rtb_ids,
                                              placement_ref_id=common_test_pre_cache_mrec_placement, x=self,
                                              name='HBP+jaeger+Bflat')
