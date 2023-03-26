from locust import TaskSet
from performance.common.util import LocustBehaviors as LB
from utils.common import gen_device_id
from settings import *
from performance.common.config import PARTNER
from random import choice

realtime_tokens = LB().get_super_tokens()['hybrid']



class vungle_mraid(TaskSet):


    def hb_video_meister(self):

        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(36),
                                                                       placement_ref_id=common_test_hybrid_placement , x=self,
                                                                       name='hybrid/HBP+jaeger+meister+Bflat')

    def hb_banner_meister(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, pub_app_id=common_test_app,
                                                                       ordinal_view=11,
                                                                       placement_ref_id=common_test_hybrid_banner_placement ,
                                                                       test_ifa=gen_device_id(36), x=self,
                                                                       name='hybrid/HBP+jaeger+meister+Bflat')

    def hb_mrec_meister(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(36),
                                                                       placement_ref_id=common_test_hybrid_mrec_placement , x=self,
                                                                       name='hybrid/HBP+jaeger+meister+Bflat')


    # data coming form Kraken

    def hb_video_kraken(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(),
                                                                       rtb=non_test_mode_kraken_rtb_ids,
                                                                       placement_ref_id=common_test_hybrid_placement, x=self,
                                                                       name='hybrid/HBP+jaeger+kraken+Bflat')

    def hb_banner_kraken(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, pub_app_id=common_test_app,
                                                                       ordinal_view=11,
                                                                       placement_ref_id=common_test_hybrid_banner_placement,
                                                                       test_ifa=gen_device_id(), x=self,
                                                                       rtb=non_test_mode_kraken_rtb_ids,
                                                                       name='hybrid/HBP+jaeger+kraken+Bflat')

    def hb_mrec_kraken(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(),
                                                                       rtb=non_test_mode_kraken_rtb_ids,
                                                                       placement_ref_id=common_test_hybrid_mrec_placement, x=self,
                                                                       name='hybrid/HBP+jaeger+kraken+Bflat')

    # request with precached token

    def hb_video_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              realTime_token=realtime_tokens["hybrid_meister_video"],
                                              pub_app_id=common_test_app,
                                              test_ifa=gen_device_id(36),
                                              placement_ref_id=common_test_hybrid_placement , x=self,
                                              name='hybrid/HBP+jaeger+meister+Bflat')

    def hb_banner_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER, pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["hybrid_meister_banner"],
                                              placement_ref_id=common_test_hybrid_banner_placement,
                                              test_ifa=gen_device_id(36), x=self,
                                              name='hybrid/HBP+jaeger+meister+Bflat')

    def hb_mrec_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["hybrid_meister_mrec"],
                                              test_ifa=gen_device_id(36),
                                              placement_ref_id=common_test_hybrid_mrec_placement, x=self,
                                              name='hybrid/HBP+jaeger+meister+Bflat')

    # request with kraken precached token

    def hb_video_kraken_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              realTime_token=realtime_tokens["hybrid_kraken_video"],
                                              pub_app_id=common_test_app,
                                              test_ifa=gen_device_id(),
                                              rtb=non_test_mode_kraken_rtb_ids,
                                              placement_ref_id=common_test_hybrid_placement, x=self,
                                              name='HBP+jaeger+Bflat')

    def hb_banner_kraken_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER, pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["hybrid_kraken_banner"],
                                              placement_ref_id=common_test_hybrid_banner_placement,
                                              rtb=non_test_mode_kraken_rtb_ids,
                                              test_ifa=gen_device_id(), x=self,
                                              name='HBP+jaeger+Bflat')

    def hb_mrec_kraken_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["hybrid_kraken_mrec"],
                                              test_ifa=gen_device_id(),
                                              rtb=non_test_mode_kraken_rtb_ids,
                                              placement_ref_id=test_video_placement, x=self,
                                              name='HBP+jaeger+Bflat')


    # Random partner


    def hb_video_meister_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list), ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(36),
                                                                       placement_ref_id=common_test_hybrid_placement , x=self,
                                                                       name='hybrid(mixed mediation)/HBP+jaeger+meister+Bflat')

    def hb_banner_meister_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list), pub_app_id=common_test_app,
                                                                       ordinal_view=11,
                                                                       placement_ref_id=common_test_hybrid_banner_placement ,
                                                                       test_ifa=gen_device_id(36), x=self,

                                                                       name='hybrid(mixed mediation)/HBP+jaeger+meister+Bflat')

    def hb_mrec_meister_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list), ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(36),
                                                                       placement_ref_id=common_test_hybrid_mrec_placement , x=self,
                                                                       name='hybrid(mixed mediation)/HBP+jaeger+meister+Bflat')

    # Random kraken partner

    def hb_video_kraken_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list),
                                                                       ordinal_view=11,
                                                                       pub_app_id=test_full_screen_placement,
                                                                       test_ifa=test_mode_device_id,
                                                                       placement_ref_id=common_test_hybrid_placement, x=self,
                                                                       name='hybrid(mixed mediation)/HBP+jaeger+kraken+Bflat')

    def hb_banner_kraken_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list),
                                                                       pub_app_id=common_test_app,
                                                                       ordinal_view=11,
                                                                       placement_ref_id=common_test_hybrid_banner_placement ,
                                                                       test_ifa=test_mode_device_id, x=self,
                                                                       name='hybrid(mixed mediation)/HBP+jaeger+kraken+Bflat')

    def hb_mrec_kraken_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list),
                                                                       ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=test_mode_device_id,
                                                                       placement_ref_id=common_test_hybrid_mrec_placement , x=self,
                                                                       name='hybrid(mixed mediation)/HBP+jaeger+kraken+Bflat')

    # request with precached token

    def hb_video_meister_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list),
                                              realTime_token=realtime_tokens["hybrid_meister_video"],
                                              pub_app_id=common_test_app,
                                              test_ifa=gen_device_id(36),
                                              placement_ref_id=common_test_hybrid_placement, x=self,
                                              name='hybrid(mixed mediation)/HBP+jaeger+meister+Bflat')

    def hb_banner_meister_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list), pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["hybrid_meister_banner"],
                                              placement_ref_id=common_test_hybrid_banner_placement ,
                                              test_ifa=gen_device_id(36), x=self,
                                              name='hybrid(mixed mediation)/HBP+jaeger+meister+Bflat')

    def hb_mrec_meister_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list),
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["hybrid_meister_mrec"],
                                              test_ifa=gen_device_id(36),
                                              placement_ref_id=common_test_hybrid_mrec_placement , x=self,
                                              name='hybrid(mixed mediation)/HBP+jaeger+meister+Bflat')

    # request with precached kraken token

    def hb_video_kraken_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list),
                                              realTime_token=realtime_tokens["hybrid_kraken_video"],
                                              pub_app_id=test_full_screen_placement,
                                              test_ifa=test_mode_device_id,
                                              placement_ref_id=common_test_hybrid_placement , x=self,
                                              name='hybrid(mixed mediation)/HBP+jaeger+kraken+Bflat')

    def hb_banner_kraken_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list), pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["hybrid_kraken_banner"],
                                              placement_ref_id=test_banner_placement,
                                              test_ifa=test_mode_device_id, x=self,
                                              name='hybrid(mixed mediation)/HBP+jaeger+kraken+Bflat')

    def hb_mrec_kraken_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list),
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["hybrid_kraken_mrec"],
                                              test_ifa=test_mode_device_id,
                                              placement_ref_id=test_video_placement, x=self,
                                              name='hybrid(mixed mediation)/HBP+jaeger+kraken+Bflat')




