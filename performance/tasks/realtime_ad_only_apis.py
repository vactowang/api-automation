from locust import TaskSet
from performance.common.util import LocustBehaviors as LB
from utils.common import gen_device_id
from settings import *
from performance.common.config import PARTNER
from random import choice

realtime_tokens = LB().get_super_tokens()['real_time_only']


class vungle_mraid(TaskSet):


    def hb_video_meister(self):

        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(36),
                                                                       rtb=hb_meister_rtb_ids,
                                                                       placement_ref_id=common_test_real_time_placement, x=self,
                                                                       name='real time only/HBP+jaeger+meister+Bflat')

    def hb_banner_meister(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, pub_app_id=common_test_app,
                                                                       ordinal_view=11,
                                                                       rtb=hb_meister_rtb_ids,
                                                                       placement_ref_id=common_test_real_time_banner_placement,
                                                                       test_ifa=gen_device_id(), x=self,
                                                                       name='real time only/HBP+jaeger+meister+Bflat')

    def hb_mrec_meister(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(36),
                                                                       placement_ref_id=common_test_real_time_mrec_placement , x=self,
                                                                       name='real time only/HBP+jaeger+meister+Bflat')

    # only request hbp

    def hb_full_screen_hbp_kraken(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=test_mode_device_id,
                                                                       is_test=1,
                                                                       placement_ref_id=test_full_screen_placement, x=self,
                                                                       name='HBP')

    def hb_mrec_hbp_meister(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(36),
                                                                       is_test=1,
                                                                       placement_ref_id=common_test_real_time_mrec_placement, x=self,
                                                                       name='HBP')

    def hb_video_hbp_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              realTime_token=realtime_tokens["real_time_only_meister_video"],
                                              pub_app_id=common_test_app,
                                              test_ifa=gen_device_id(36),
                                              is_test=1,
                                              placement_ref_id=common_test_real_time_placement, x=self,
                                              name='HBP')



    def hb_banner_hbp_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER, pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["real_time_only_meister_banner"],
                                              placement_ref_id=common_test_real_time_banner_placement,
                                              test_ifa=gen_device_id(36), x=self,
                                              is_test=1,
                                              name='HBP')

    def hb_hbp_mrec_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["real_time_only_meister_mrec"],
                                              test_ifa=gen_device_id(36),
                                              is_test=1,
                                              placement_ref_id=common_test_real_time_mrec_placement, x=self,
                                              name='HBP')

    # data coming form Kraken

    def hb_video_kraken(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(),
                                                                       placement_ref_id=common_test_real_time_placement, x=self,
                                                                       rtb=non_test_mode_kraken_rtb_ids,
                                                                       name='HBP+jaeger+Bflat')

    def hb_banner_kraken(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, pub_app_id=common_test_app,
                                                                       ordinal_view=11,
                                                                       placement_ref_id=common_test_real_time_banner_placement,
                                                                       test_ifa=gen_device_id(), x=self,
                                                                       rtb=non_test_mode_kraken_rtb_ids,
                                                                       name='HBP+jaeger+Bflat')

    def hb_video_mrec_kraken(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(),
                                                                       placement_ref_id=common_test_real_time_mrec_placement, x=self,
                                                                       rtb=non_test_mode_kraken_rtb_ids,
                                                                       name='HBP+jaeger+Bflat')

    # request with precached token

    def hb_video_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              realTime_token=realtime_tokens["real_time_only_meister_video"],
                                              pub_app_id=common_test_app,
                                              test_ifa=gen_device_id(),
                                              rtb=hb_meister_rtb_ids,
                                              placement_ref_id=common_test_real_time_placement, x=self,
                                              name='real time only/HBP+jaeger+meister+Bflat')

    def hb_banner_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER, pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["real_time_only_meister_banner"],
                                              placement_ref_id=common_test_real_time_banner_placement,
                                              test_ifa=gen_device_id(), x=self,
                                              rtb=hb_meister_rtb_ids,
                                              name='real time only/HBP+jaeger+meister+Bflat')

    def hb_mrec_meister_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["real_time_only_meister_mrec"],
                                              test_ifa=gen_device_id(),
                                              rtb=hb_meister_rtb_ids,
                                              placement_ref_id=common_test_real_time_mrec_placement, x=self,
                                              name='real time only/HBP+jaeger+meister+Bflat')

    # request with kraken precached token

    def hb_video_kraken_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              realTime_token=realtime_tokens["real_time_only_kraken_video"],
                                              pub_app_id=common_test_app,
                                              test_ifa=gen_device_id(),
                                              rtb=non_test_mode_kraken_rtb_ids,
                                              placement_ref_id=common_test_real_time_placement, x=self,
                                              name='HBP+jaeger+Bflat')

    def hb_banner_kraken_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER, pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["real_time_only_kraken_banner"],
                                              placement_ref_id=common_test_real_time_banner_placement,
                                              test_ifa=gen_device_id(), x=self,
                                              name='HBP+jaeger+Bflat', rtb=non_test_mode_kraken_rtb_ids)

    def hb_video_mrec_kraken_precached(self):
        LB().request_hbp_with_real_time_token(supply=PARTNER,
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["real_time_only_kraken_mrec"],
                                              test_ifa=gen_device_id(),
                                              placement_ref_id=common_test_real_time_mrec_placement, x=self,
                                              rtb=non_test_mode_kraken_rtb_ids,
                                              name='HBP+jaeger+Bflat')

    # invalid token

    def hb_full_screen_invalid(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, ordinal_view=11,
                                                                       token=test_invalid_token,
                                                                       pub_app_id=common_test_app,
                                                                       placement_ref_id=test_full_screen_placement,
                                                                       test_ifa=test_mode_device_id, x=self,
                                                                       name='/HBP')

    def hb_banner_invalid(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, token=test_invalid_token,
                                                                       ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       placement_ref_id=test_banner_placement,
                                                                       test_ifa=test_mode_device_id, x=self,
                                                                       name='/HBP')

    def hb_video_mrec_invalid(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=PARTNER, token=test_invalid_token,
                                                                       pub_app_id=common_test_app,
                                                                       ordinal_view=11,
                                                                       placement_ref_id=test_video_placement,
                                                                       test_ifa=test_mode_device_id, x=self,
                                                                       name='/HBP')

    # Random partner

    def hb_video_meister_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list), ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(36),
                                                                       placement_ref_id=common_test_real_time_placement , x=self,
                                                                       name='real time only(mixed mediation)/HBP+jaeger+meister+Bflat')

    def hb_banner_meister_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list), pub_app_id=common_test_app,
                                                                       ordinal_view=11,
                                                                       placement_ref_id=common_test_real_time_banner_placement ,
                                                                       test_ifa=gen_device_id(36), x=self,

                                                                       name='real time only(mixed mediation)/HBP+jaeger+meister+Bflat')

    def hb_mrec_meister_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list), ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=gen_device_id(36),
                                                                       placement_ref_id=common_test_real_time_mrec_placement , x=self,
                                                                       name='real time only(mixed mediation)/HBP+jaeger+meister+Bflat')

    # Random kraken partner

    def hb_video_kraken_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list),
                                                                       ordinal_view=11,
                                                                       pub_app_id=test_full_screen_placement,
                                                                       test_ifa=test_mode_device_id,
                                                                       placement_ref_id=common_test_real_time_placement , x=self,
                                                                       name='real time only(mixed mediation)/HBP+jaeger+kraken+Bflat')

    def hb_banner_kraken_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list),
                                                                       pub_app_id=common_test_app,
                                                                       ordinal_view=11,
                                                                       placement_ref_id=common_test_real_time_banner_placement ,
                                                                       test_ifa=test_mode_device_id, x=self,
                                                                       name='real time only(mixed mediation)/HBP+jaeger+kraken+Bflat')

    def hb_mrec_kraken_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list),
                                                                       ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       test_ifa=test_mode_device_id,
                                                                       placement_ref_id=common_test_real_time_mrec_placement , x=self,
                                                                       name='real time only(mixed mediation)/HBP+jaeger+kraken+Bflat')

    # request with precached token

    def hb_full_screen_meister_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list),
                                              realTime_token=realtime_tokens["real_time_only_meister_video"],
                                              pub_app_id=common_test_app,
                                              test_ifa=gen_device_id(36),
                                              placement_ref_id=common_test_real_time_placement, x=self,
                                              name='real time only(mixed mediation)/HBP+jaeger+meister+Bflat')

    def hb_banner_meister_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list), pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["real_time_only_meister_banner"],
                                              placement_ref_id=common_test_real_time_banner_placement ,
                                              test_ifa=gen_device_id(36), x=self,
                                              name='real time only(mixed mediation)/HBP+jaeger+meister+Bflat')

    def hb_mrec_meister_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list),
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["real_time_only_meister_mrec"],
                                              test_ifa=gen_device_id(36),
                                              placement_ref_id=common_test_real_time_mrec_placement, x=self,
                                              name='real time only(mixed mediation)/HBP+jaeger+meister+Bflat')

    # request with precached kraken token

    def hb_video_kraken_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list),
                                              realTime_token=realtime_tokens["real_time_only_kraken_video"],
                                              pub_app_id=test_full_screen_placement,
                                              test_ifa=test_mode_device_id,
                                              placement_ref_id=common_test_real_time_placement , x=self,
                                              name='real time only(mixed mediation)/HBP+jaeger+kraken+Bflat')

    def hb_banner_kraken_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list), pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["real_time_only_kraken_banner"],
                                              placement_ref_id=common_test_real_time_banner_placement ,
                                              test_ifa=test_mode_device_id, x=self,
                                              name='real time only(mixed mediation)/HBP+jaeger+kraken+Bflat')

    def hb_mrec_kraken_precached_random(self):
        LB().request_hbp_with_real_time_token(supply=choice(hb_partner_list),
                                              pub_app_id=common_test_app,
                                              realTime_token=realtime_tokens["real_time_only_kraken_mrec"],
                                              test_ifa=test_mode_device_id,
                                              placement_ref_id=common_test_real_time_mrec_placement , x=self,
                                              name='real time only(mixed mediation)/HBP+jaeger+kraken+Bflat')

    # invalid token

    def hb_full_screen_invalid_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list), ordinal_view=11,
                                                                       token=test_invalid_token,
                                                                       pub_app_id=common_test_app,
                                                                       placement_ref_id=test_full_screen_placement,
                                                                       test_ifa=test_mode_device_id, x=self,
                                                                       name='real time only(mixed mediation)/HBP')

    def hb_banner_invalid_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list), token=test_invalid_token,
                                                                       ordinal_view=11,
                                                                       pub_app_id=common_test_app,
                                                                       placement_ref_id=test_banner_placement,
                                                                       test_ifa=test_mode_device_id, x=self,
                                                                       name='real time only(mixed mediation)/HBP')

    def hb_video_mrec_invalid_random(self):
        LB().request_hbp_with_real_time_token_with_non_precached_token(supply=choice(hb_partner_list), token=test_invalid_token,
                                                                       pub_app_id=common_test_app,
                                                                       ordinal_view=11,
                                                                       placement_ref_id=test_video_placement,
                                                                       test_ifa=test_mode_device_id, x=self,
                                                                       name='real time only(mixed mediation)/HBP')


