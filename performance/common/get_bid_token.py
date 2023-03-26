from performance.common.util import LocustBehaviors as LB
from performance.common.config import *
from performance.common.util import *
from collections import Counter
import json

env = "perf"

bid_tokens = multi_dismensions(3, Counter)

sdk_v_dict = test_common_versions[test_common_os]

multi_token_dict = {}

class vungle_mraid():

    def __init__(self):
        self.name = get_class_name(self)
        global name
        name = self.name

    class Kraken:

        def fullscreen(self):

            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app,
                                                           placement_ref_id=android_common_test_placement,
                                                           android_id=test_mode_device_id, rtb=test_mode_kraken_rtb_ids,
                                                           sdk_v=value)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_placement,
                                                   test_ifa=test_mode_device_id, rtb=non_test_mode_kraken_rtb_ids,
                                                   sdk_v=value)
                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump

        def banner(self):

            for key, value in sdk_v_dict.items():

                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app,
                                                           placement_ref_id=android_common_test_banner_placement,
                                                           android_id=test_mode_device_id,
                                                           rtb=get_rtb(env, test_mode_kraken_rtb_ids),
                                                           banner=True, sdk_v=value)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_banner_placement,
                                                   test_ifa=test_mode_device_id, rtb=get_rtb(env, test_mode_kraken_rtb_ids),
                                                   banner=True, sdk_v=value)
                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump

        def image_mrec(self):
            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app,
                                                           placement_ref_id=android_image_mrec_test_placement,
                                                           android_id=test_mode_device_id,
                                                           rtb=get_rtb(env, test_mode_kraken_rtb_ids),
                                                           sdk_v=value)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_image_mrec_placement,
                                                   test_ifa=gen_device_id(),
                                                   rtb=get_rtb(env, non_test_mode_kraken_rtb_ids),
                                                   sdk_v=value)

                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump

        def video_mrec(self):
            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app,
                                                           placement_ref_id=android_video_mrec_test_placement,
                                                           android_id=test_mode_device_id,
                                                           rtb=get_rtb(env, test_mode_kraken_rtb_ids),
                                                           sdk_v=value)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_video_mrec_placement,
                                                   test_ifa=test_mode_device_id,
                                                   rtb=get_rtb(env, test_mode_kraken_rtb_ids),
                                                   sdk_v=value)

                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump

    class meister:

        def fullscreen(self):
            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app,
                                                           placement_ref_id=android_common_test_placement,
                                                           sdk_v=value)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_placement, sdk_v=value)
                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump

        def banner(self):
            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app,
                                                           placement_ref_id=android_common_test_banner_placement,
                                                           banner=True,
                                                           rtb=meister_rtb_ids,
                                                           android_id=test_device_id, sdk_v=value)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_banner_placement, banner=True,
                                                   rtb=meister_rtb_ids,
                                                   test_ifa=test_device_id, sdk_v=value)
                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump

        def image_mrec(self):
            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app,
                                                           placement_ref_id=android_image_mrec_test_placement,
                                                           sdk_v=value)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_image_mrec_placement, sdk_v=value)
                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump

        def video_mrec(self):
            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app, sdk_v=value,
                                                           placement_ref_id=android_video_mrec_test_placement,
                                                           android_id='', src_ip=gb_ip)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_video_mrec_placement, sdk_v=value)
                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump


class legacy:

    def __init__(self):
        self.name = get_class_name(self)
        global name
        name = get_class_name(self)

    class meister:

        def video(self):
            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app, sdk_v=value,
                                                           placement_ref_id=android_common_test_placement_legacy)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_placement_legacy, sdk_v=value,
                                                   rtb=meister_rtb_ids)

                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump


class programmatic_vast:

    def __init__(self):
        self.name = get_class_name(self)
        global name
        name = get_class_name(self)

    class Kraken:

        def video(self):
            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app,
                                                           placement_ref_id=android_common_test_placement,
                                                           android_id=test_mode_device_id, sdk_v=value,
                                                           rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_vast))
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_placement,
                                                   test_ifa=test_mode_device_id, sdk_v=value,
                                                   rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_vast))
                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump


class programmatic_mraid:

    def __init__(self):
        self.name = get_class_name(self)
        global name
        name = get_class_name(self)

    class Kraken:

        def banner(self):
            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':

                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app,
                                                           placement_ref_id=android_common_test_banner_placement,
                                                           android_id=test_mode_device_id,
                                                           rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_mraid),
                                                           banner=True, sdk_v=value)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_banner_placement,
                                                   test_ifa=test_mode_device_id,
                                                   rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_mraid), banner=True,
                                                   sdk_v=value)
                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump

        def mrec(self):
            for key, value in sdk_v_dict.items():
                if test_common_os == 'android':
                    super_token = LB().super_token_android(ordinal_view_count=ORIDINAL_VIEW,
                                                           pub_app_id=android_common_test_app,
                                                           placement_ref_id=android_programmatic_mrec_test_placement,
                                                           android_id=test_mode_device_id,
                                                           rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_mraid),
                                                           sdk_v=value)
                else:
                    super_token = LB().super_token(ordinal_view_count=ORIDINAL_VIEW, pub_app_id=common_test_app,
                                                   placement_ref_id=common_test_programmatic_mrec_placement,
                                                   test_ifa=test_mode_device_id,
                                                   rtb=get_rtb(env, ext_test_mode_kraken_rtb_ids_mraid), sdk_v=value)

                bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
                bid_tokens_dump = json.loads(dumps(bid_tokens))
                multi_token_dict[key] = bid_tokens_dump


def exec_function():
    h = vungle_mraid()
    h.meister().fullscreen()
    # h.Kraken().fullscreen()
    # h.Kraken().banner()
    # h.Kraken().image_mrec()
    # h.Kraken().video_mrec()
    # h.meister().banner()
    # h.meister().banner()
    h.meister().video_mrec()
    h.meister().image_mrec()
    # l = legacy()
    # l.meister().video()
    # pv = programmatic_vast()
    # pv.Kraken().video()
    # pm = programmatic_mraid()
    # pm.Kraken().banner()
    # pm.Kraken().mrec()
    return multi_token_dict

