from performance.common.util import *
from collections import Counter
import json
from utils.behaviors import *

env = "qa"

ORIDINAL_VIEW = 11

PARTNER = 'mopub'

bid_tokens = multi_dismensions(3, Counter)

multi_token_dict = {}


class hybrid():

    def __init__(self):
        self.name = get_class_name(self)
        global name
        name = self.name

    class kraken:

        def video(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_hybrid_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(),
                                                           rtb=non_test_mode_kraken_rtb_ids,
                                                           no_pre_cache_token=False, perf=True,
                                                          )
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def banner(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_hybrid_banner_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(), banner=True,
                                                           rtb=non_test_mode_kraken_rtb_ids,
                                                           no_pre_cache_token=False, perf=True,
                                                           )
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def mrec(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_hybrid_mrec_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(),
                                                           rtb=non_test_mode_kraken_rtb_ids,
                                                           no_pre_cache_token=False, perf=True)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

    class meister:

        def video(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_hybrid_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(), perf=True
                                                           )
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def banner(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_hybrid_banner_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(), banner=True, perf=True
                                                           )
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def mrec(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_hybrid_mrec_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(36), perf=True
                                                           )
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)


class pre_cache():

    def __init__(self):
        self.name = get_class_name(self)
        global name
        name = self.name

    class kraken:

        def video(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_pre_cache_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(),
                                                           rtb=non_test_mode_kraken_rtb_ids,
                                                           no_pre_cache_token=False, perf=True)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def banner(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_pre_cache_banner_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           rtb=non_test_mode_kraken_rtb_ids,
                                                           test_device_id=gen_device_id(), banner=True,
                                                           no_pre_cache_token=False, perf=True)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def mrec(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_pre_cache_mrec_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           rtb=non_test_mode_kraken_rtb_ids,
                                                           test_device_id=gen_device_id(),
                                                           no_pre_cache_token=False, perf=True)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

    class meister:

        def video(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_pre_cache_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(), perf=True,
                                                           rtb=hb_meister_rtb_ids
                                                           )
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def banner(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_pre_cache_banner_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           rtb=hb_meister_rtb_ids,
                                                           test_device_id=gen_device_id(), banner=True
                                                           , perf=True)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def mrec(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_pre_cache_mrec_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           rtb=hb_meister_rtb_ids,
                                                           test_device_id=gen_device_id(), perf=True,
                                                           )
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)


class real_time_only():

    def __init__(self):
        self.name = get_class_name(self)
        global name
        name = self.name

    class kraken:

        def video(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_real_time_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           rtb=non_test_mode_kraken_rtb_ids,
                                                           test_device_id=gen_device_id(), perf=True,
                                                           no_pre_cache_token=False)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def banner(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_real_time_banner_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(), banner=True,
                                                           rtb=non_test_mode_kraken_rtb_ids,

                                                           no_pre_cache_token=False, perf=True)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def mrec(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_real_time_mrec_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(),
                                                           rtb=non_test_mode_kraken_rtb_ids,

                                                           no_pre_cache_token=False, perf=True)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

    class meister:

        def video(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_real_time_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(), perf=True,
                                                           rtb=hb_meister_rtb_ids)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def banner(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_real_time_banner_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(), banner=True
                                                           , perf=True,
                                                           rtb=hb_meister_rtb_ids)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)

        def mrec(self):
            super_token = request_hbp_with_real_time_token(supply=PARTNER, ordinal_view=ORIDINAL_VIEW,
                                                           pub_app_id=common_test_app,
                                                           placement_ref_id=common_test_real_time_mrec_placement,
                                                           sdk_v=test_default_real_time_sdk_version,
                                                           test_device_id=gen_device_id(36), perf=True,
                                                           rtb=hb_meister_rtb_ids)
            bid_tokens[name][get_class_name(self)][sys._getframe().f_code.co_name] = super_token
            bid_tokens_dump = json.loads(dumps(bid_tokens))
            multi_token_dict.update(bid_tokens_dump)


def exec_function():
    hybrid_kraken = hybrid().kraken()
    hybrid_kraken.video()
    hybrid_kraken.banner()
    hybrid_kraken.mrec()
    hybrid_meister = hybrid().meister()
    hybrid_meister.mrec()
    hybrid_meister.banner()
    hybrid_meister.video()

    pre_cache_kraken = pre_cache().kraken()
    pre_cache_kraken.video()
    pre_cache_kraken.banner()
    pre_cache_kraken.mrec()
    pre_cache_meister = pre_cache().meister()
    pre_cache_meister.mrec()
    pre_cache_meister.banner()
    pre_cache_meister.video()

    real_time_only_kraken = real_time_only().kraken()
    real_time_only_kraken.video()
    real_time_only_kraken.banner()
    real_time_only_kraken.mrec()
    real_time_only_meister = real_time_only().meister()
    real_time_only_meister.video()
    real_time_only_meister.banner()
    real_time_only_meister.mrec()

    return multi_token_dict


if __name__ == '__main__':
    print(exec_function())
