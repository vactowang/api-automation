from locust import TaskSet
from performance.common.config import *
from performance.common.util import LocustBehaviors as LB
from utils.common import gen_device_id


class Jaeger(TaskSet):

    def on_start(self):
        """ on_start is called when the TaskSet is starting """
        print("---start up a user")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("---tear down a user")

    def request_jaeger_qa0(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=test_mode_kraken_rtb_id_qa0, hb=True, banner=False, ip=au_ip,
                         sdk_v=test_default_sdk_version,
                         locust_call=True, nick_name="Jaeger")

    def test_jaeger_with_app_mesh(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_native_placement,
                         test_ifa='4423DD36-2738-46DC-84D1-02A47F95320D1',
                         rtb='610cf812a15921c3d486b998', hb=False, banner=False, ip=au_ip,
                         sdk_v='Vungle/6.11.0',
                         locust_call=True, nick_name="Jaeger")


    def request_jaeger_qa02(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=test_mode_kraken_rtb_id_qa0_2, hb=True, banner=False, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")

    def request_jaeger_real_time_banner(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_real_time_banner_placement,
                         test_ifa=test_mode_device_id,
                         rtb=test_mode_kraken_rtb_ids, hb=True, banner=True, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")

    def request_jaeger_hybrid_banner(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                         test_ifa=gen_device_id(),
                         rtb=ext_non_test_mode_kraken_rtb_ids_vast_gzip, hb=True, banner=True, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")

    def request_jaeger_qa0_ext(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=ext_test_mode_kraken_rtb_ids_vast_gzip_perf, hb=True, banner=False, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")

    def request_jaeger_qa0_ext_non_test_mode(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                         test_ifa=gen_device_id(),
                         rtb=ext_non_test_mode_kraken_rtb_ids_vast_gzip_perf, hb=True, banner=False, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")

    def request_jaeger_qa0_test_mode_kraken(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=test_mode_kraken_rtb_ids_gzip_perf , hb=True, banner=False, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")


    def request_jaeger_qa0_non_test_mode_kraken(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=non_test_mode_kraken_rtb_ids_gzip_perf, hb=True, banner=False, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")

    # -----------------------------------------------below are non hb traffics------------------------------------------


    def request_jaeger_qa01(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_placement,
                         test_ifa=test_mode_device_id,
                         rtb=test_mode_kraken_rtb_id_qa0_1, hb=False, banner=False, ip=au_ip,
                         sdk_v=test_default_sdk_version,
                         locust_call=True, nick_name="Jaeger")

    def request_jaeger_real_time_mrec_non_hb(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_real_time_mrec_placement,
                         test_ifa=test_mode_device_id,
                         rtb=test_mode_kraken_rtb_ids, hb=False, banner=False, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")

    def request_jaeger_real_time_banner_non_hb(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_real_time_banner_placement,
                         test_ifa=test_mode_device_id,
                         rtb=test_mode_kraken_rtb_ids, hb=False, banner=True, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")

    def request_jaeger_hybrid_banner_non_hb(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_hybrid_banner_placement,
                         test_ifa=test_mode_device_id,
                         rtb=test_mode_kraken_rtb_ids, hb=False, banner=True, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")

    def request_jaeger_hybrid_mrec(self):
        LB().request_ads(x=self, pub_app_id=common_test_app, placement_ref_id=common_test_hybrid_mrec_placement,
                         test_ifa=test_mode_device_id,
                         rtb=test_mode_kraken_rtb_ids, hb=False, banner=False, ip=au_ip,
                         sdk_v=test_default_sdk_version, locust_call=True, nick_name="Jaeger")