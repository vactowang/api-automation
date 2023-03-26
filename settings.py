from datetime import datetime, timedelta

import bson
from bson.objectid import ObjectId
import json
import os

# Get Project Root
import random

from bson import ObjectId

get_root = os.path.dirname(os.path.abspath(__file__))

# Load config
config = None

_json_config_file = get_root + '/config.json'

with open(_json_config_file) as config_file:
    config = json.load(config_file)

# Common
env = config['env']
prefEnv = config['perfEnv']

if config['skip_int'] == 'yes':
    skip_int = True
else:
    skip_int = False


def get_ip_random():
    return str(random.randint(0, 255))


eu_country_ip = '77.204.247.74'
gb_ip = '92.11.160.0'
in_ip = '43.239.80.68'
us_ip = '72.229.28.185'
non_eu_country_ip = '45.117.100.153'
jp_ip = '161.202.226.195'
ca_us_ip = '174.137.51.62'
ru_ip = '5.3.255.211'
ua_ip = '46.202.175.0'
kr_ip = '1.16.63.252'
de_ip = '84.145.77.194'
fr_ip = '37.164.162.171'
it_ip = '151.95.219.6'
au_ip = '45.117.100.153'
blocked_ip = '77.204.247.76'
cn_ip = '117.136.240.121'
ao_ip = '154.127.207.1'
et_ip = '102.218.48.0'
cu_ip = '57.74.110.0'
kp_ip = '175.45.176.0'
sy_ip = '178.218.252.0'
lb_ip = '109.110.96.1'
by_ip = '46.191.0.0'
ir_ip = '103.216.60.0'
ipv6_example_01 = '2603:6081:3b08:6400:5814:455b:c12:5fee'
ipv6_example_02 = '2600:1003:b02f:12be:20e8:205:77f3:a3e5'
ipv6_example_03 = '2001:48f8:b007:780:34c2:596d:bcad:ce17'


# Bastion
config_host_qa = config['endpoints']['config'][env]
config_v5_endpoint_qa = '%s/api/v5/config' % config_host_qa
config_v4_endpoint_qa = '%s/api/v4/config' % config_host_qa
config_status_endpoint_qa = '%s/status' % config_host_qa

# Jaeger
ads_v5_host_qa = config['endpoints']['ads'][env]
ads_v5_endpoint_qa = '%s/api/v5/ads' % ads_v5_host_qa
ads_v5_endpoint_qa0 = '%s/api/v5/ads' % config['endpoints']['ads'][prefEnv]
jaeger_status_endpoint_qa = '%s/status' % ads_v5_host_qa
jaeger_notification_timeout = '%s/timeout' % ads_v5_host_qa
jaeger_demoApp_login = '%s/demoAppLogin' % ads_v5_host_qa
ads_v5_endpoint_qa_real_adbuilder = 'http://adex.ads-qa.vungle.com/api/v5/ads'
s2s_v5_standard_endpoint_qa = '%s/api/s2s/3d517f8' % ads_v5_host_qa
s2s_v5_sigmob_endpoint_qa = '%s/api/s2s/0c23f9e' % ads_v5_host_qa
s2s_v5_active_endpoint_qa = '%s/api/s2s/27da060' % ads_v5_host_qa
s2s_v5_onboarding_endpoint_qa = '%s/api/s2s/c3a4355' % ads_v5_host_qa
s2s_v5_inactive_endpoint_qa = '%s/api/s2s/99a2f3d' % ads_v5_host_qa
s2s_v5_invalid_endpoint_qa = '%s/api/s2s/tta2f3d' % ads_v5_host_qa
ads_path = '/api/v5/ads'
realtime_token_verify_endpoint_qa = '%s/api/v5/token_verify' % ads_v5_host_qa


def get_s2s_partner_endpoint(partner):
    if partner == 'sigmob':
        return s2s_v5_sigmob_endpoint_qa
    else:
        return s2s_v5_standard_endpoint_qa


# HBP
hbp_host = ads_v5_host_qa
hbp_tool_host = config['endpoints']['hbp'][env]
hbp_host_qa0 = config['endpoints']['hbp'][prefEnv]
hbp_status_endpoint_qa = '%s/status' % hbp_host
hbp_max_endpoint_qa = '%s/bid/t/2ffe4e7' % hbp_host
hbp_adtiming_endpoint_qa = '%s/bid/t/428d94f' % hbp_host
hbp_ironsource_endpoint_qa = '%s/bid/t/f03ca20' % hbp_host
hbp_ohayoo_endpoint_qa = '%s/bid/t/348b764' % hbp_host
hbp_saygames_endpoint_qa = '%s/bid/t/8f878c0' % hbp_host
hbp_test_endpoint_qa = '%s/bid/t/test' % hbp_host
hbp_aequus_endpoint_qa = '%s/bid/t/69fcd92' % hbp_host
hbp_charboost_endpoint_qa = '%s/bid/t/1e9ddf6' % hbp_host
hbp_unity_endpoint_qa = '%s/bid/t/439b3a2' % hbp_host
hbp_fyber_endpoint_qa = '%s/bid/t/3a78b0a' % hbp_host
hbp_topon_endpoint_qa = '%s/bid/t/1aee677' % hbp_host
hbp_wildlife_endpoint_qa = '%s/bid/t/fce889a' % hbp_host
hbp_appodeal_endpoint_qa = '%s/bid/t/8ea3e9a' % hbp_host
hbp_fb_test_endpoint_qa = '%s/bid/t/fb_test' % hbp_host
hbp_admob_endpoint_qa = '%s/bid/t/81106a3' % hbp_host
hbp_not_exist_endpoint_qa = '%s/bid/t/811eeee' % hbp_host
hbp_ssl_host = config['endpoints']['hbp_ssl'][env]
hbp_nurl_endpoint = '%s/win' % hbp_ssl_host
hbp_burl_endpoint = '%s/bill' % hbp_ssl_host
hbp_lurl_endpoint = '%s/loss' % hbp_ssl_host
hbp_admob_event_token_decoder_qa = '%s/eventtoken_decode' % hbp_host
hbp_checker_qa = hbp_host+'/check?key=%s&type=%s'

# HBP perf endpoint
hbp_max_endpoint = '/bid/t/2ffe4e7'
hbp_adtiming_endpoint = '/bid/t/428d94f'
hbp_ironsource_endpoint = '/bid/t/f03ca20'
hbp_ohayoo_endpoint = '/bid/t/348b764'
hbp_saygames_endpoint = '/bid/t/8f878c0'
hbp_test_endpoint = '/bid/t/test'
hbp_aequus_endpoint = '/bid/t/69fcd92'
hbp_charboost_endpoint = '/bid/t/1e9ddf6'
hbp_unity_endpoint = '/bid/t/439b3a2'
hbp_fyber_endpoint = '/bid/t/3a78b0a'
hbp_topon_endpoint = '/bid/t/1aee677'
hbp_wildlife_endpoint = '/bid/t/fce889a'
hbp_appodeal_endpoint = '/bid/t/8ea3e9a'
hbp_fb_test_endpoint = '/bid/t/fb_test'
hbp_admob_endpoint = '/bid/t/81106a3'

hbp_lurl_notification_endpoint_qa = '%s/lurl/34dec8a' % hbp_host
hb_partner_list = config['hb_partners']
burl_hb_partners = config['burl_hb_partners']
hbp_timeout_url = '%s/timeout?auction_id=${AUCTION_ID}&loss_reason=${AUCTION_LOSS}&partner=topon' % \
                  config['endpoints']['hbp_notification'][env]

hbp_admob_encrypted_price = ['vLubnKBBps0EDvy9O4XFcZd4C4qyQQeDtHxA7g']


def get_hbp_partner_endpoint(partner, perf=False):
    if partner == 'max':
        if perf is True:
            return hbp_max_endpoint
        return hbp_max_endpoint_qa
    elif partner == 'adtiming':
        if perf is True:
            return hbp_adtiming_endpoint
        return hbp_adtiming_endpoint_qa
    elif partner == 'ironsource':
        if perf is True:
            return hbp_ironsource_endpoint
        return hbp_ironsource_endpoint_qa
    elif partner == 'ohayoo':
        if perf is True:
            return hbp_ohayoo_endpoint
        return hbp_ohayoo_endpoint_qa
    elif partner == 'saygames':
        if perf is True:
            return hbp_saygames_endpoint
        return hbp_saygames_endpoint_qa
    elif partner == 'aequus':
        if perf is True:
            return hbp_aequus_endpoint
        return hbp_aequus_endpoint_qa
    elif partner == 'charboost':
        if perf is True:
            return hbp_charboost_endpoint
        return hbp_charboost_endpoint_qa
    elif partner == 'unity':
        if perf is True:
            return hbp_unity_endpoint
        return hbp_unity_endpoint_qa
    elif partner == 'fyber':
        if perf is True:
            return hbp_fyber_endpoint
        return hbp_fyber_endpoint_qa
    elif partner == 'topon':
        if perf is True:
            return hbp_topon_endpoint
        return hbp_topon_endpoint_qa
    elif partner == 'test':
        if perf is True:
            return hbp_test_endpoint
        return hbp_test_endpoint_qa
    elif partner == 'wildlife':
        if perf is True:
            return hbp_wildlife_endpoint
        return hbp_wildlife_endpoint_qa
    elif partner == 'appodeal':
        if perf is True:
            return hbp_appodeal_endpoint
        return hbp_appodeal_endpoint_qa
    elif partner == 'fb_test':
        if perf is True:
            return hbp_fb_test_endpoint
        return hbp_fb_test_endpoint_qa
    elif partner == 'admob':
        if perf is True:
            return hbp_admob_endpoint
        return hbp_admob_endpoint_qa
    elif partner == 'not_exist':
        return hbp_not_exist_endpoint_qa
    else:
        return ''


# Scrat
scrat_all_host = config['endpoints']['scrat_all'][env]
scrat_status_endpoint_qa = '%s/status' % scrat_all_host
ri_v5_endpoint_qa = '%s/api/v5/ri' % scrat_all_host
sdk_logging_endpoint_qa = '%s/sdk' % scrat_all_host
sdk_error_logging_endpoint_qa = '%s/sdk/error_logs' % scrat_all_host
sdk_metrics_logging_endpoint_qa = '%s/sdk/metrics' % scrat_all_host
sdk_bi_endpoint_qa = '%s/api/v5/sdk_bi' % config['endpoints']['sdk_bi'][env]
tpat_endpoint_qa = '%s/api/v5/tpat' % config['endpoints']['tpat'][env]
tpat_endpoint_v7_qa = '%s/api/v7/tpat' % config['endpoints']['tpat'][env]
scrat_sdk_notification_endpoint_qa = '%s/api/v5/load_ad' % config['endpoints']['load_ad'][env]
scrat_timeout_endpoint_qa = '%s/api/v5/timeout?auction_id=${AUCTION_ID}&loss_reason=${AUCTION_LOSS}&partner=topon' % scrat_all_host
scrat_notification_host = config['endpoints']['scrat_notification'][env]
scrat_notification_win_endpoint_qa = '%s/api/v5/win' % scrat_notification_host
scrat_notification_loss_endpoint_qa = '%s/api/v5/loss' % scrat_notification_host
scrat_notification_bill_endpoint_qa = '%s/api/v5/bill' % scrat_notification_host
scrat_notification_host_ssl = config['endpoints']['scrat_notification_ssl'][env]
scrat_notification_win_endpoint_qa_ssl = '%s/api/v5/win' % scrat_notification_host_ssl
scrat_notification_loss_endpoint_qa_ssl = '%s/api/v5/loss' % scrat_notification_host_ssl
scrat_notification_bill_endpoint_qa_ssl = '%s/api/v5/bill' % scrat_notification_host_ssl
cache_bust_endpoint_qa = '%s/api/v5/cache_bust' % config['endpoints']['cache_bust'][env]


def scrat_impression_endpoint_qa(replace_env=None):
    if replace_env is None:
        return '%s/api/v5/impression' % config['endpoints']['impression'][env]
    else:
        return '%s/api/v5/impression' % config['endpoints']['impression'][replace_env]


# Bflat
bflat_host = config['endpoints']['bflat'][env]
bflat_host_qa0 = config['endpoints']['bflat'][prefEnv]
bflat_bid_request_endpoint_qa = '%s/bid_request' % bflat_host
bflat_get_exp_list_endpoint_qa = '%s/debug/experiments' % bflat_host
bflat_bid_request = '/bid_request'
bflat_idsp_experiments = config['bflat']['idsp_exp_list']
bflat_edsp_experiments = config['bflat']['edsp_exp_list']
bflat_random_experiments = config['bflat']['random_exp_list']


# now dsp value are 'idsp, edsp, random'
def get_specify_bflat_exp_list(dsp='idsp', placement_type='banner'):
    if dsp == 'idsp':
        specify_bflat_exp_list = [dsp + '_' + placement_type + '_' + str(x) for x in
                                  bflat_idsp_experiments[placement_type]]
    elif dsp == 'edsp':
        specify_bflat_exp_list = [dsp + '_' + placement_type + '_' + str(x) for x in
                                  bflat_edsp_experiments[placement_type]]
    elif dsp == 'random':
        specify_bflat_exp_list = [dsp + '_' + str(x) for x in bflat_random_experiments]
    return specify_bflat_exp_list


def get_new_endpoint_qa(version):
    url = '%s/api/v%s/new' % (scrat_all_host, version)
    return url


def get_report_ad_endpoint_qa(version):
    if version == '5':
        url = '%s/api/v5/report_ad' % scrat_all_host
    else:
        url = '%s/api/v%s/reportAd' % (scrat_all_host, version)
    return url


def get_session_start_endpoint_qa(version):
    url = '%s/api/v%s/sessionStart' % (scrat_all_host, version)
    return url


def get_session_end_endpoint_qa(version):
    url = '%s/api/v%s/sessionEnd' % (scrat_all_host, version)
    return url


test_app_id_ios = '$0${\"app_id\":\"5f0821744fd1310016fd4bd1\",\"eventID\":\"5fe4586f775977000126f603\"}'
test_campaign_ios = '5f08238f4fd1310016fd4d09|5f0ba9b9cd6e3746d385298f|datasci--blr_20200201_lat_new_platform_isolat' \
                    'ed_sgd_exploit--success--meister|5fe4586f775977000126f603'
test_campaign_edsp_ios = '591007e887faec9f44000018|574351a9740cf4426b30d030|dsp-5fd21b43c80cb9051249a6ae|5fe4586f775977000126f603'
test_ad_token_ios = 'eyJjYW1wYWlnbiI6IjVmMDgyMzhmNGZkMTMxMDAxNmZkNGQwOXw1ZjBiYTliOWNkNmUzNzQ2ZDM4NTI5OGZ8ZGF0YXNjaS0' \
                    'tYmxyXzIwMjAwMjAxX2xhdF9uZXdfcGxhdGZvcm1faXNvbGF0ZWRfc2dkX2V4cGxvaXQtLXN1Y2Nlc3MtLW1laXN0ZXJ8NW' \
                    'ZlNDU4NmY3NzU5NzcwMDAxMjZmNjAzIn0='
test_app_id_android = '$0${\"app_id\":\"5bfe9fc5c009327c413e5da8\",\"eventID\":\"5f54f5eecf0f3500016d5e37\"}'
test_campaign_android = '5efe3f1a00bd700feb093d9e|5f2c0caeb3f535000f02cccf|datasci--blr_20191101_view_cts_365_hdw_' \
                        'lat_sgd_exploit--success|5f54f5eecf0f3500016d5e37'
test_ad_token_android = 'eyJjYW1wYWlnbiI6IjVlZmUzZjFhMDBiZDcwMGZlYjA5M2Q5ZXw1ZjJjMGNhZWIzZjUzNTAwMGYwMmNjY2Z8ZGF0YX' \
                        'NjaS0tYmxyXzIwMTkxMTAxX3ZpZXdfY3RzXzM2NV9oZHdfbGF0X3NnZF9leHBsb2l0LS1zdWNjZXNzfDVmNTRmNWVl' \
                        'Y2YwZjM1MDAwMTZkNWUzNyJ9'
test_app_id_windows = '$0${\"app_id\":\"5dc452d7e2339d5a363d1b67\",\"eventID\":\"btafg7qvsp461bgcg0ng\"}'
test_campaign_windows = '5dc453234f6fa55a4fa9ba52|5dc4663212e87e5a3d9e3f4b|datasci--blr_20190601_view_cts_365_hdw_' \
                        'lat_explore02--success--meister|btafg7qvsp461bgcg0ng'
test_ad_token_windows = 'eyJjYW1wYWlnbiI6IjVkYzQ1MzIzNGY2ZmE1NWE0ZmE5YmE1Mnw1ZGM0NjYzMjEyZTg3ZTVhM2Q5ZTNmNGJ8ZGF0' \
                        'YXNjaS0tYmxyXzIwMTkwNjAxX3ZpZXdfY3RzXzM2NV9oZHdfbGF0X2V4cGxvcmUwMi0tc3VjY2Vzcy0tbWVpc3Rl' \
                        'cnxidGFmZzdxdnNwNDYxYmdjZzBuZyJ9'
test_campaign_default_edsp = '5cd92b2661a35300113a8487_591007e887faec9f44000018|5cd92b2661a35300113a8487_574351a9740cf4426b30d030|dsp-5fd21b43c80cb9051249a6ae|6321a67729ee4b5672395ccd'
test_campaign_edsp_not_in_db = '5cd92b2661a35300113a8487_emilycid|5cd92b2661a35300113a8487_emilycrid|dsp-5fd21b43c80cb9051249a6ae|6321a67729ee4b5672395ccd'

# test data
block_low_power_mode_apps = [
    ('5db379f3db8e200011927b68', 'DEFAULT02022_TEST01'),
    ('5d81337b1f888100188de147', 'INTERSTITIAL_TOP-5293737'),
    ('6047f876cc123b37c465206d', 'INTERSTITIAL_15-9302886'),
    ('5f0e15b139d7fe0001b1ee39', 'INTERSTITIAL_16-4601772'),
    ('5f0e3df96f35ef0001e1f0ee', 'INTERSTITIAL_17-9534054'),
    ('6047f8b8cc123b37c4652072', 'INTERSTITIAL_18-3140925'),
    ('556f747e67c16c382100006e', 'IOS_INTERSTITIAL_HIGH-3871950')
]

common_test_app = '59786bc2a43b3a08620026b1'  # app status: ACTIVE; test devices: is_test_devices_enabled: true
common_test_app_realtime_exp = '59786bc2a43b3a08620086b1'
common_test_app_no_coppa = '5c003b9a3933314cf38ff7f3'
common_test_no_coppa_placement = 'DEFAULT-5045327'
common_test_realtime_coppa_placement_1 ='VIDEO_REALTIME_coppa_01'
common_test_realtime_coppa_placement_2 ='VIDEO_REALTIME_coppa_02'
common_test_realtime_coppa_placement_3 ='VIDEO_REALTIME_coppa_03'
common_test_s2s_instl_placement = 'HJKM6GM50916IMA'
common_test_app_market_id = '1131184101'
common_test_placement = 'DEFAULT02021'
common_test_s2s_placement = 's2s-DEFAULT02022'
common_test_placement_instl = 'HJKM6GM50916IMA'
common_test_placement_instl2 = 'HJKM6GM50916IMA2'
common_test_placement_instl3 = 'HJKM6GM50916IMA3'
common_test_placement_instl4 = 'HJKM6GM50916IMA4'
common_test_placement_instl5 = 'HJKM6GM50916IMA5'
common_test_placement_single_page = 'AREYOUS82690'
common_test_placement_id = '59786bc2a43b3a0862002774'
common_test_placement_legacy = 'DEFAULT02021-LOCAL'
common_test_banner_placement = 'BANNER-TEST-01'
common_test_banner_placement_id = '5e1595f0b026b9fb2164110a'
common_test_image_mrec_placement = 'IMAGE_MREC_TEST_001-8365312'
common_test_programmatic_mrec_placement = 'PROG_MREC_TEST_001-8657322'
common_test_video_mrec_placement = 'VIDEO_MREC_TEST_001-2549736'
common_test_native_placement = 'NATIVE-001'
common_test_TCPI_1 = 'TCPI_TEST_1'
common_test_TCPI_2 = 'TCPI_TEST_2'
common_test_TCPI_3 = 'TCPI_TEST_3'
sigmob_placement_01 = 'sigmob_placement_ios_01'
sigmob_placement_02 = 'sigmob_placement_ios_02'
common_test_app_old = 'com.lo.ssp-test-1'
common_test_placement_old = 'DEFAULT02071'
common_test_throttle_placement = 'DEFAULT02021_throttle'
common_test_throttle_placement_false = 'DEFAULT02021_throttle_false'
common_test_app_9 = '6371e27998147a228aa55077'
common_test_placement_playable = 'EMILY_THIRD_PARTY_01'
common_test_app_other_account = '632bc8f2bd506689036b24c3'
common_test_other_placement = 'VIDEO_REALTIME_TEST-3176921'

common_test_app_10 = '616699e51546249caaf3a96a'
common_test_real_time_placement_10 = 'DEFAULT-0072717'
common_test_placement_10 = 'DEFAULT-0072717-1'
common_test_hybrid_placement_10 = 'DEFAULT-0072717-2'
common_test_real_time_mrec_placement_10 = 'MREC_REALTIME_TEST_22'


edsp_exp_test_app = '59786bc2a43b3a08620026a2'
edsp_exp_test_placement = 'DEFAULT020A2'

common_test_vungle_mraid_third_party_placement = 'THIRD_PARTY_PLAYABLE'
common_test_third_party_placement_04 = 'THIRD_PARTY_PLAYABLE_MREC'
common_test_third_party_placement_crtype_01 = 'THIRD_PARTY_PLAYABLE_REWARDED_CRTYPE_2'
common_test_third_party_placement_crtype_02 = 'THIRD_PARTY_PLAYABLE_INSTL_CRTYPE_2'
common_test_third_party_placement_crtype_03 = 'THIRD_PARTY_PLAYABLE_BANNER_CRTYPE_2'
common_test_third_party_placement_attr_01 = 'THIRD_PARTY_PLAYABLE_REWARDED_ATTR_13'
common_test_third_party_placement_attr_02 = 'THIRD_PARTY_PLAYABLE_INSTL_ATTR_13'
common_test_third_party_placement_attr_03 = 'THIRD_PARTY_PLAYABLE_BANNER_ATTR_13'
common_test_third_party_crtype_attr_01 = 'EMILY_THIRD_PARTY_PLAYABLE_INST_CRTYPE_2_ATTR_13'
common_test_third_party_crtype_attr_02 = 'EMILY_THIRD_PARTY_PLAYABLE_REWARDED_CRTYPE_2_ATTR_13'

# real-time ad test data
common_test_real_time_placement = 'VIDEO_REALTIME_TEST-3176951'
common_test_real_time_rewarded_placement = 'real_time_HJKM6GM50908'
common_test_real_time_native_placement = 'realTime-NATIVE-001'
common_test_pre_cache_placement = 'VIDEO_PRECACHE_TEST-0848213'
common_test_hybrid_placement = 'VIDEO_HYBRID_TEST-8126185'
common_test_real_time_banner_placement = 'BANNER_REALTIME_TEST_1-9633704'
common_test_pre_cache_banner_placement = 'BANNER_PRECACHE_TEST_1-4101050'
common_test_hybrid_banner_placement = 'BANNER_HYBRID_TEST_1-0837077'
common_test_real_time_mrec_placement = 'MREC_REALTIME_TEST_21'
common_test_pre_cache_mrec_placement = 'MREC_PERCACHE_TEST-4192481'
common_test_hybrid_mrec_placement = 'MREC_HYBRID_TEST-5086331'
common_test_real_time_ddl_placement = 'VIDEO_REALTIME_DDL_TEST'
common_test_no_hb_cache_type_placement = 'NO_HB_CACHE_TYPE_TEST'
common_test_real_time_no_coppa_placement = 'VIDEO_REALTIME_coppa_01'
common_test_real_time_playable_placement = 'Realtime_THIRD_PARTY_PLAYABLE_REWARDED_CRTYPE_2'
common_test_real_time_placement_throttle = 'VIDEO_REALTIME_TEST-throttle'
common_test_real_time_placement_throttle_false = 'VIDEO_REALTIME_TEST-throttle-false'
common_test_hybrid_placement_throttle = 'VIDEO_HYBRID_TEST-throttle'

common_test_marid_placement = 'INTER-MREC-004'

common_test_app_1 = '59786bc2a43b3a08620026b2'
common_test_placement_1 = 'DEFAULT02022'
common_test_placement_1_instl = 'HJKM6GM50916IMP0'
common_test_placement_1_instl1 = 'HJKM6GM50916IMP01'
common_test_placement_1_instl2 = 'HJKM6GM50916IMP02'
common_test_real_time_placement_1 = 'DEFAULT02137'
common_test_banner_placement_1 = 'BANNER-TEST-22'
common_test_app_2 = '59786bc2a43b3a08620026b4'
common_test_placement_2 = 'DEFAULT02024'
common_test_placement_21 = 'DEFAULT02024_1'

common_test_app_t = '59786bc2a43b3a08620026b3'
common_test_placement_t = 'DEFAULT02023'

# test devices flag
common_test_app_3 = '61c415de532682513658a21f'  # app status: ACTIVE; test devices: is_test_devices_enabled: false
common_test_placement_3 = 'INTSL_PLACEMENT_01-3147706'

common_test_app_4 = '61c416f1532682513658a220'  # app status: test mode; test devices: is_test_devices_enabled: false
common_test_placement_4 = 'INTER_PLACEMENT_02-9763004'
common_test_real_time_placement_4 = 'VIDEO_REALTIME_TEST_MODE-3176951'

common_test_app_5 = '61c4186d532682513658a221'  # app status: test mode; test devices: is_test_devices_enabled: true
common_test_placement_5 = 'INTER_PLACEMENT_03-3854568'

common_test_app_6 = '60e8193e279e10832585edcb'  # app status: test mode;
common_test_placement_6 = 'CLONE_DEFAULT-3548917'
common_test_placement_real_time_6 = 'DEFAULT-5295434'

common_test_app_7 = '5f83bcabe4a98ce0adf0d35c'  # app status: inactive;
common_test_placement_7 = 'CLONE_DEFAULT-3747685'
common_test_placement_real_time_7 = 'DEFAULT-4552747'

android_common_test_app_rta = '59e781de7fff7cb02500ca2e'
android_common_test_placement_rta = 'DEFAULT95027_rta'
android_common_test_app = '59e781de7fff7cb02500ca0e'
android_common_test_placement = 'DEFAULT95027'
android_common_test_rewarded_placement = 'DEFAULT_REWARDED-3605411'
android_common_test_placement_rewarded = 'CC4RVAN74965'
android_common_coppa_app = '61efb2209164cc60d4a59a7b'
android_common_coppa_placememt = 'coppa_DEFAULT95027'
android_common_bcat_app = '623c5a9faad52f0140a6fe37'
android_common_bcat_placement = 'bcat_coppa_DEFAULT95027'
android_fullscreen_inter_playable_placement = 'DEFAULT_FULLSCREEN_PLAYABLE-3221628'
android_fullscreen_reward_playable_placement = 'DEFAULT_FULLSCREEN_REWARD_PLAYABLE-1349101'
android_video_mrec_test_placement = 'VIDEO_MREC_TEST_ANDROID-001'
android_image_mrec_test_placement = 'IMAGE_MREC_TEST_ANDROID-001'
android_common_test_banner_placement = 'BANNER-TEST-ANDROID-01'
android_programmatic_mrec_test_placement = 'PROG_MREC_TEST_ANDROID_001'
android_common_test_placement_legacy = 'DEFAULT95027-LOCAL'
sigmob_placement_android_01 = 'sigmob_placement_android_01'
sigmob_placement_android_02 = 'sigmob_placement_android_02'
android_common_test_third_party_placement = 'ANDROID_THIRD_PARTY_PLAYABLE'
android_common_ddl_placement = 'DEFAULT1117'
# real time for android
android_realtime_video_test_placement = 'VIDEO_REALTIME_TEST-8577399'
android_realtime_banner_test_placement = 'BANNER_REALTIME_TEST-5167578'
android_realtime_mrec_test_placement = 'MREC_REALTIME_TEST-5709523'
android_hybrid_mrec_test_placement = 'MREC_HYBRID_TEST-6222138'
android_hybrid_banner_test_placement = 'BANNER_HYBRID_TEST-0839472'
android_hybrid_video_test_placement = 'VIDEO_HYBRID_TEST-3831116'
android_preCache_video_test_placement = 'VIDEO_PRECACHE_TEST-6775988'
android_preCache_banner_test_placement = 'BANNER_PRECACHE_TEST-8956978'
android_preCache_mrec_test_placement = 'MREC_PRECACHE_TEST-7674767'

windows_common_test_app = '5dd72ebf001c531f8cf48083'
windows_common_test_placement = 'REWARDEDDT-0648490'
windows_common_realtime_placement = 'REALTIME-REWARDEDDT-0648490'
windows_image_mrec_test_placement = 'IMAGE_MREC_TEST_WINDOWS_001'
windows_common_test_placement_legacy = 'DEFAULT-0024862'
windows_common_test_third_party_placement = 'WINDOWS_THIRD_PARTY_PLAYABLE'
windows_common_specify_block_app = '57979405fb0fb7fc6e0000a2'
windows_common_specify_block_placement = 'SOLDEFA62646'

amazon_common_test_app = '5bebe77a598bee2c619dca28'
amazon_common_test_placement = 'DEFAULT-8228620'
amazon_image_mrec_test_placement = 'IMAGE-MREC-TEST-AMAZON-001'

mrec_test_app = '5b35341e3bf1d54695e8f642'
programmatic_mrec_placement = 'PROG_MREC_AUTOMATION_USED-7106378'
image_mrec_placement = 'MREC_IMG_PLACE1-6363700'
mrec_placement = 'MREC_AUTOMATION_USED-2026794'

full_screen_clickable_app_f = '59786bc2a43b3a08620026b1'
full_screen_clickable_app_f_placement_n = 'DEFAULT02021'
full_screen_clickable_app_f_placement_t_local = 'HJKM6GM50919'
full_screen_clickable_app_f_placement_t_mraid = 'AREYOUS82690'

full_screen_clickable_app_t = '5c003b9a3933314cf38ff7f3'
full_screen_clickable_app_t_placement_n = 'DEFAULT-5045327'
full_screen_clickable_app_t_placement_f_local = 'LOCAL-8330758'
full_screen_clickable_app_t_placement_f_mraid = 'MRAID-3843518'

gdpr_external_consents_opted_in_device_id = '4423DD36-2738-46DC-84D1-02A47F95320D37'
gdpr_external_consents_opted_out_device_id = '4423DD36-2738-46DC-84D1-02A47F95320D38'
ccpa_external_consents_opted_out_device_id = '4423DD36-2738-46DC-84D1-02A47F95320D16'

app_id_schain_test = '5a79f754cb770f302f008a89'
placement_id_schain_test = 'REWARDP46778'

event_id_ttl_pub_app = '5f5c060b4134eb000108cf6f'
event_id_ttl_placement = 'DEFAULT02021X'

gdpr_gdpr_delegate_f_legitimate_interest_f_app = '5c003b9a3933314cf38ff7f3'
gdpr_gdpr_delegate_n_legitimate_interest_t_app = '59786bc2a43b3a08620026b1'
gdpr_gdpr_delegate_t_legitimate_interest_f_app = '5a721e0fd135f57d0c009569'
gdpr_gdpr_delegate_t_legitimate_interest_t_app = '5a721e0fd135f57d0c009570'

rtb_exclusion_test_app = '59786bc2a43b3a08620026b6'
rtb_exclusion_test_placement = 'DEFAULT02026'

flatcpm_exp_test_app = '5eecd03e4314cc0001b4fdeb'
flatcpm_exp_test_placement = 'HJKM6GM50919F'
flatcpm_exp_test_placement_in_config = 'FLATCPM-EXP-V7'
flatcpm_exp_test_placement_not_in_config = 'FLATCPM-EXP-V7-NOT-IN-CONFIG'
flatcpm_placement_native = 'Native-001-flatCpm'
flatcpm_placement_real_time = 'flatCpm_realTime-NATIVE-001'
# meister rtb ids
meister_rtb_ids = '5fd2181dc80cb9051249a6aa,59128f4fa8e4b2cbcb250c87,60adc79dfb70f80016e36884'
meister_rtb_ids_list = ['5fd2181dc80cb9051249a6aa', '59128f4fa8e4b2cbcb250c87', '60adc79dfb70f80016e36884',
                        '60e43247e0199d8ef532306d', '620f5aa9e27258bed30d662f']
hb_meister_rtb_ids = '60adc79dfb70f80016e36884'
meister_s2s_rtb_id = '620f5aa9e27258bed30d662f'
legacy_meister_rtb_ids = '5fd2181dc80cb9051249a6aa,59128f4fa8e4b2cbcb250c87'
win_notification_meister_rtb_ids = '61422c2f757479816492b84e,60e43247e0199d8ef532306d'
meister_rtb_ids_default_hb = '634cc4d398c5395c9f094d59'  # supported_extension_type:default_hb
meister_rtb_ids_default_default_consentstring = '634cc5d698c5395c9f094d5b'  # supported_extension_type# :default_consentstring
meister_rtb_ids_vungle_dup = '634cc6ea98c5395c9f094d61'  # supported_extension_type:vungle_dup

# meister rtb ids - perf
legacy_meister_rtb_ids_qa0 = '60ad885858faa5723c43328b'

# kraken rtb ids - internal
test_mode_kraken_rtb_ids = '5d4ce4726f4447f538dfd7e9,5fd219d7c80cb9051249a6ab'  # "bill_notice_origin": "exchange", "interstitial": true
test_mode_kraken_rtb_ids_1 = '5d4ce4726f4447f538dfd7e8,5fd21a5fc80cb9051249a6ac'  # "bill_notice_origin": "sdk", no native type support, "interstitial": false
test_mode_kraken_rtb_ids_2 = '6110c913ed008cf4af37a511,6110c927ed008cf4af37a513'  # "bill_notice_origin": "disabled", no set on interstitial, no allow_idfv
test_mode_kraken_rtb_ids_3 = '6110cbe7ed008cf4af37a515,6110cbfbed008cf4af37a517'  # "bill_notice_origin": "abcd", "interstitial": false, no allow_idfv
test_mode_kraken_rtb_ids_4 = '6112236309ef564172e38103,6112238509ef564172e38105'  # "allow_min_bid_to_win": true
test_mode_kraken_rtb_ids_5 = '61c33fce98abea236ced43c5,61c3400798abea236ced43c7'  # "bill_notice_origin": "disabled", "interstitial": false, no allow_idfv
test_mode_kraken_int1_rtb_ids = '6142408a757479816492b859,60f7f91f3dc4c168b724ea49'  # no "allow_min_bid_to_win"
test_mode_kraken_int2_rtb_ids = '61423e96757479816492b857,61138b0e09ef564172e38111'  # "allow_min_bid_to_win": true
test_mode_kraken_int2_rtb_ids_1 = '6142408a757479816492b859,6163cf1dbaa635aa082e946d'  # no "allow_min_bid_to_win"
test_mode_kraken_int3_rtb_ids = '616688bea8b9cb5bb376c9c7'  # for OMSDK test
test_mode_kraken_int4_rtb_ids = '6142408a757479816492b859,6195e72d01064518120ed36a'  # no "KRAKEN_ADS_OMID_ADM_URL" setting
test_mode_kraken_rtb_support_extension = '634d186a98c5395c9f094d73'  # supported_extension_type: "vungle_DUP"
non_test_mode_kraken_rtb_ids = '5fd21c53c80cb9051249a6af,5ea0f98dcd192603f1743120'
non_test_mode_kraken_rtb_ids_no_adomain_block = '623ab4c134756201c16fb015'
test_mode_kraken_rtb_ids_no_adomain_block = '623ab8e034756201c16fb016'
non_test_mode_kraken_int1_rtb_ids = '5fd21c53c80cb9051249a6af,60f7f51d3dc4c168b724ea47'
non_test_mode_kraken_int1_rtb_ids_01 = '628233a228c6521a8b5be494'
non_test_mode_kraken_int2_rtb_ids_01 = '6282340c28c6521a8b5be495'
non_test_mode_kraken_int_mixed_rtb_ids = '6282340c28c6521a8b5be495,628233a228c6521a8b5be494'
test_mode_kraken_rtb_ids_banner_xapi = '60ed32008e007e8aac99c801,60ed32748e007e8aac99c805'
test_mode_kraken_rtb_ids_gzip = '60f51bff3dc4c168b724ea2e,60f51c8d3dc4c168b724ea31'
test_mode_same_setting_rtb_ids_gzip = '60f51c8d3dc4c168b724ea31,621dc8e859561900639680e7'
non_test_mode_same_setting_rtb_ids_gzip = '60f51d373dc4c168b724ea35,621dd13359561900639680e8'
non_test_mode_kraken_rtb_ids_gzip = '60f51d1b3dc4c168b724ea33,60f51d373dc4c168b724ea35'
test_mode_kraken_rtb_ids_uri_decode = '5fd85b0af20710001613f7ea'

# kraken rtb ids - (external notification meister)
test_mode_kraken_ext_notification_01 = '61138b0e09ef564172e38111,5fd219d7c80cb9051249a6ab'
# kraken rtb ids - external
ext_test_mode_kraken_rtb_ids_vast = '5e4249cd9a33f696c14e9bcd,5fd21adbc80cb9051249a6ad'  # "bill_notice_origin": null, no set on interstitial
ext_test_mode_kraken_rtb_ids_wurfl = '616148ed9f47415dad743a16,616149379f47415dad743a17'  # "device_detect_strategies: 'WURFL'"
ext_test_mode_kraken_rtb_ids_OSAPI = '61614a239f47415dad743a18,61614a529f47415dad743a19'  # "device_detect_strategies: 'OSAPI'"
# r2: allow_idfv=true, device_detect_strategies:{windows:wrful}; r1: allow_idfv=false, device_detect_strategies:''
ext_test_mode_kraken_mixedRTB_wurfl = '5fd21adbc80cb9051249a6ad,616149379f47415dad743a17'
ext_test_mode_kraken_mixedRTB_wurfl_ci = '5e4249cd9a33f696c14e9bcd,616148ed9f47415dad743a16'

ext_test_mode_kraken_rtb_ids_mraid = '5e5f66f346572b9c88caebfd,5fd21b43c80cb9051249a6ae'
ext_test_mode_kraken_rtb_ids_vast_1 = '614162fe757479816492b844,614162c1757479816492b842'  # "interstitial": false, no allow_idfv
ext1_test_mode_kraken_rtb_ids_vast = '60e2e990e0199d8ef532305f,60a27657b3bbef2c0884d8b9'  # no native type support
ext1_test_mode_kraken_rtb_ids_mraid = '60e2ea05e0199d8ef5323061,60a276d5b3bbef2c0884d8ba'
ext_non_test_mode_kraken_rtb_ids_mraid = '5ea13e3bcd192603f1743121,5fd21ceac80cb9051249a6b0'  # third_party_playable support
ext_non_test_mode_kraken_rtb_ids_wurfl = '61614acc9f47415dad743a1a,61614b189f47415dad743a1b'  # "device_detect_strategies: 'WURFL'"
ext_non_test_mode_kraken_rtb_ids_OSAPI = '61614b7a9f47415dad743a1c,61614bda9f47415dad743a1e'  # "device_detect_strategies: 'OSAPI'"
ext_non_test_mode_kraken_rtb_ids_vast = '5ec4f75047e96807f30455f6,5fd21d91c80cb9051249a6b1'  # "bill_notice_origin": "sdk", no third_party_playable support
ext_non_test_mode_kraken_rtb_block_adomain = '620366692b623fd7eeec445a'  # "blocked_adomains:{"ios":[glu.com,testabc.com], "windows":[glu.com]}"
ext_non_test_mode_kraken_rtb_ids_mraid_1 = '610bc61aed008cf4af37a4f7,610bc6d6ed008cf4af37a500'  # "interstitial": false
ext_non_test_mode_kraken_rtb_ids_vast_1 = '610bc634ed008cf4af37a4f9,610bc646ed008cf4af37a4fb'  # "bill_notice_origin": "exchange", devosv exp blocks
ext_non_test_mode_kraken_rtb_ids_vast_2 = '6112240b09ef564172e38107,6112243a09ef564172e38109'  # "allow_min_bid_to_win": true
ext1_non_test_mode_kraken_rtb_ids_mraid = '60e2ea78e0199d8ef5323065,60a2773fb3bbef2c0884d8bb'
ext1_non_test_mode_kraken_rtb_ids_vast = '60e2eab4e0199d8ef5323067,60a277a5b3bbef2c0884d8bc'  # "allow_min_bid_to_win": false, "allow_idfv": false
ext2_non_test_mode_kraken_rtb_ids_mraid = '61121012ed008cf4af37a519,61121028ed008cf4af37a51b'
ext2_non_test_mode_kraken_rtb_ids_vast = '61121061ed008cf4af37a51d,61121075ed008cf4af37a51f'
ext2_non_test_mode_kraken_rtb_ids_vast_ll = '639976e2acbe3e770ca85c5c'  # last look target edsp
ext_non_test_mode_kraken_rtb_ids_1 = '5fbb893acf4d4c02e0b92030,5fd21f83c80cb9051249a6b4'
ext_non_test_mode_kraken_rtb_ids_2 = '5fbb893acf4d4c02e0b92031,5fd22257c80cb9051249a6b5'
ext_non_test_mode_kraken_rtb_ids_3 = '5fbb92b3cf4d4c02e0b92032,5fd222efc80cb9051249a6b6'
ext_non_test_mode_kraken_rtb_ids_vast_no_iab11 = '601bb358fafd9b03bec173ef,601bb3c8fafd9b03bec173f0'
ext_test_mode_kraken_rtb_ids_vast_no_html_ec = '60bef14625d34102de230faf,60bef18825d34102de230fb0'
ext_test_mode_kraken_rtb_ids_vast_no_iab11 = '601bb4cffafd9b03bec173f1,601bb50afafd9b03bec173f2'
ext_test_mode_kraken_rtb_ids_banner_xapi = '60ed334d8e007e8aac99c807,60ed337d8e007e8aac99c809'
ext_non_test_mode_kraken_rtb_ids_vast_xapi = '620224da80e219160471d166,6202249580e219160471d164'
ext_non_test_mode_kraken_rtb_ids_vast_inmobi = '6215ec0c80e219160471d185,6215ec4080e219160471d187'
ext_non_test_mode_kraken_rtb_ids_mraid_block_optedout = '5f6828d1d5ba35022aeace72,5fd21e1fc80cb9051249a6b3'
ext_non_test_mode_kraken_rtb_ids_vast_block_optedout = '5f681dcdd5ba35022aeace71,5fd21deec80cb9051249a6b2'
ext_non_test_mode_kraken_rtb_ids_vast_gzip = '60f51aa83dc4c168b724ea28,60f51a403dc4c168b724ea24'
ext_test_mode_kraken_rtb_ids_vast_gzip = '60f51b843dc4c168b724ea2a,60f51bb33dc4c168b724ea2c'
ext_non_test_mode_kraken_same_setting_rtb_ids_vast_gzip = '60f51a403dc4c168b724ea24,621dd23a59561900639680e9'
ext_test_mode_kraken_same_setting_rtb_ids_vast_gzip = '60f51bb33dc4c168b724ea2c,621dd25859561900639680ea'
ext_test_mode_kraken_vast_rtb_ids_tencent = '5df9726443db1a0016e67126'
ext_test_mode_kraken_rtb_ids_vast_uri_decode = '5fd73e352753900016c80c27'
ext1_non_test_mode_kraken_rtb_ids_vast_playable = '6177d4ca2c6975035fee7568'  # no third_party_playable support
ext1_non_test_mode_kraken_rtb_ids_mraid_playable = '60a2773fb3bbef2c0884d8bb'
ext_non_test_mode_kraken_rtb_ids_mraid_playable = '618b8887247db04b60a7b0ec'
ext1_non_kraken_test_mode_default_hb = '634cc42b98c5395c9f094d55'  # supported_extension_type:default_hb
ext1_non_kraken_test_mode_default_consentstring = '634cc64798c5395c9f094d5d'  # supported_extension_type:default_consentstring allow_hb_flag=true
ext2_non_kraken_test_mode_default_dup = '634cc68f98c5395c9f094d5f,6363d7e41fbec347625200fc'  # supported_extension_type:default_dup
ext2_non_kraken_test_mode_spec_default_dup = '636dea4131cc74fcc2717bdc'  # supported_extension_type:default_dup=specifyDefalut
ext2_non_kraken_test_mode_spec_default_mutiple_category = '636df35731cc74fcc2717be2'  # supported_extension_type:default_dup=specifyDefalut_hb
ext1_non_test_mode_kraken_networkID = '6385b7f6c465da8bc7d04430'  # supported_extension_type:default_networkid
ext1_non_kraken_test_mode_mutiple_category = '634d152998c5395c9f094d6f'  # supported_extension_type:default_hb_dup
ext_non_test_mode_kraken_rtb_consentString = '61d3efbed456f8ca150cd399'  # supported_extension_type:ConsentString
ext_test_mode_kraken_rtb_consentString = '61d3f151d456f8ca150cd39e'  # supported_extension_type:ConsentString
ext_non_test_mode_kraken_rtb_ids_vast_aarki = '5f9b33d146a46f00108de996'  # supported_extension_type:headerbidding
ext_non_test_mode_kraken_rtb_ids_block_crid = '62398afb7240231f0711cf2f'
ext_test_mode_kraken_rtb_ids_block_crid = '623998777240231f0711cf32'
ext_test_mode_kraken_rtb_ids_mutiple_category = '634d178e98c5395c9f094d71'  # supported_extension_type:default_hb_dup
ext4_test_mode_kraken_rtb_ids_vast = '5e4249cd9a33f696c14e9bcd,6242b0f15890c35df3ee97fa'
ext4_test_mode_kraken_rtb_ids_mraid = '5e5f66f346572b9c88caebfd,6242b1185890c35df3ee97fc'
ext_non_test_mode_kraken_rtb_ids_bidSwitch = '6375d0b2159c4f16d7541675'  # supported_extension_type:default_exp
ext1_non_test_mode_kraken_block_ip_01 = '5fd965d7323580001628bf72'
# demo app kraken
ext_test_mode_kraken_demo_app = '63db1e290799b83c8d6301bb'
ext_non_test_mode_kraken_demo_app = '63db2b400799b83c8d6301be'

# Liftoff simulation rtbs
ext_non_test_mode_kraken_rtb_ids_vast_liftoff = '6114e00b09ef564172e38115,6114dfcd09ef564172e38113'  # "supported_extension_type": "LiftOff", "allow_idfv":true, "bill_notice_origin": "exchange"
ext_non_test_mode_kraken_rtb_ids_mraid_liftoff = '6114f75d09ef564172e38119,6114f72009ef564172e38117'  # "supported_extension_type": "LiftOff", "allow_idfv":false
ext_test_mode_kraken_rtb_ids_vast_liftoff_notification = '624593905890c35df3ee9818,62458e1e5890c35df3ee9816'  # "supported_extension_type": "LiftOff", "allow_idfv":true, "win_notice_origin": "sdk", "bill_notice_origin": "sdk"
ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification = '624677235890c35df3ee981c,624676875890c35df3ee981a'  # "supported_extension_type": "LiftOff", "allow_idfv":true, "win_notice_origin": "sdk", "bill_notice_origin": "sdk"
ext_non_test_mode_kraken_rtb_ids_vast_liftoff_notification_loss = '6246e6b95890c35df3ee9822'  # "supported_extension_type": "LiftOff", "allow_idfv":true, "win_notice_origin": "sdk", "bill_notice_origin": "sdk", pric=1.0
ext_non_test_mode_kraken_rtb_ids_vast_liftoff_mixed_notification = '624676875890c35df3ee981a,6246e6b95890c35df3ee9822'
ext_non_test_mode_kraken_rtb_ids_vast_liftoff_us = '62553a085890c35df3ee9850,625539b15890c35df3ee984e'  # "supported_extension_type": "LiftOff", "allow_idfv":true, "bill_notice_origin": "exchange"
ext_test_mode_kraken_rtb_ids_vast_liftoff_us = '62555a665890c35df3ee9852,62555a9b5890c35df3ee9854'  # "supported_extension_type": "LiftOff", "allow_idfv":true, "bill_notice_origin": "exchange"
ext_non_test_mode_liftoff_01 = '624676875890c35df3ee981a'
ext1_non_test_mode_liftoff_01 = '5fd965d7323580001628bf72'
# Moloco simulation rtbs
ext_non_test_mode_kraken_rtb_ids_vast_moloco = '62d8a9339fa3e5efd7bf3f01,62d8a95e9fa3e5efd7bf3f03'

# PreFiltering  ext rtbids
ext1_non_test_mode_kraken_rtb_prefiltering_01 = '61cbfd6f507ffeaf0b7df96e'  # allow_platform:{ios:true, android:false, windows: true, amazon: true}; block_consent_optout:false
ext1_non_test_mode_kraken_rtb_prefiltering_02 = '61cc12f0507ffeaf0b7df96f'  # allow_platform:{ios:true, android:false, windows: true, amazon: true}; block_consent_optout:true
ext1_non_test_mode_kraken_rtb_prefiltering_03 = '61cc454a8e4ee4e608b5be5e'  # allow_platform:{ios:true, android:false, windows: true, amazon: true};
ext1_non_test_mode_kraken_rtb_prefiltering_04 = '61cc49c78e4ee4e608b5be5f'  # allow_lat: false
ext1_non_test_mode_kraken_rtb_prefiltering_05 = '61cc4a128e4ee4e608b5be60'  # allow_lat: true
ext1_non_test_mode_kraken_rtb_prefiltering_06 = '62441b3d5961fca0b01f440a'  # allow_banner_size: { "300x50":true, "320x50":true,  "728x90":false, "300x250":true}
ext1_non_test_mode_kraken_rtb_prefiltering_07 = '62442ac25961fca0b01f440b'  # block_bid_floor
ext1_non_test_mode_kraken_rtb_prefiltering_08 = '62454a2bfcc689050988e056'  # block_bid_floor, allow_banner_size
# Margin Experiment win mixed rtb ids
mixed_participate_rtbids = '60f7f51d3dc4c168b724ea47,61544ea663244e95d2626a49,60a277a5b3bbef2c0884d8bc'
liftoff_rtbids_bid = '61544ea663244e95d2626a49,615464e663244e95d2626a4f'
liftoff_rtbids_liftoff_dup = '634cc7a998c5395c9f094d63'  # "supported_extension_type": "liftoff_dup",
liftoff_rtbids_liftoff_dup_01 = '634d125e98c5395c9f094d6d'  # "supported_extension_type": "liftoff_DUP",
liftoff_rtbids_liftoff_specify_dup = '636def3b31cc74fcc2717be0'  # "supported_extension_type": "liftoff_dup=123",
liftoff_rtbids_liftoff_specify_mutiple_category = '636df46d31cc74fcc2717be4'  # "supported_extension_type": "liftoff_dup=123_hb",

# refactor bidder package rtb ids (mixed ids)
mixed_non_test_mode_edsp = '6112243a09ef564172e38109,610bc646ed008cf4af37a4fb,5fd21d91c80cb9051249a6b1'  # interstial:null, false, true
mixed_non_test_mode_edsp_with_playable = '6177d4ca2c6975035fee7568,60a2773fb3bbef2c0884d8bb'  # playable:no, yes
mixed_non_test_mode_rtb_ids = '5ea0f98dcd192603f1743120,60a2773fb3bbef2c0884d8bb,6114dfcd09ef564172e38113'  # internal, external, liftoff
mixed_test_mode_rtb_banner = '614162c1757479816492b842,60ed337d8e007e8aac99c809'  # ext_rtb, xapi_rtb
mixed_non_test_rtbs_gzip = '60f51a403dc4c168b724ea24,621dd13359561900639680e8'
mixed_non_test_mode_rtb_auction_mbtw = '6246e6b95890c35df3ee9822,61121075ed008cf4af37a51f'
mixed_test_mode_rtb_auction_mbtw_01 = '60f7f91f3dc4c168b724ea49,62458e1e5890c35df3ee9816'
mixed_non_test_mode_rtb_auction_mbtw_02 = '5fd965d7323580001628bf72,61121075ed008cf4af37a51f'


# serve with grabed ads kraken
ext_grab_online_rtb = '63aa88ad45766b87d7c46608'
int_grab_online_rtb = '63aa88ad45766b87d7c46609'

# kraken rtb ids - perf
test_mode_kraken_rtb_id_qa0 = '613717881b222199f4652717,613717881b222199f4555555'
test_mode_kraken_rtb_id_qa0_1 = '613717cc1b222199f4652719,613717881b222199f4555555'
test_mode_kraken_rtb_id_qa0_2 = '613717d91b222199f465271b,613717881b222199f4555555'
ext_non_test_mode_kraken_rtb_ids_vast_gzip_perf = '614afdc5757479816492b862,613717881b222199f4555555'
ext_test_mode_kraken_rtb_ids_vast_gzip_perf = '614afdf6757479816492b864,613717881b222199f4555555'
test_mode_kraken_rtb_ids_gzip_perf = '614afe7f757479816492b866,613717881b222199f4555555'
non_test_mode_kraken_rtb_ids_gzip_perf = '614afe99757479816492b868,613717881b222199f4555555'

# one service kraken
test_mode_kraken_default_int = '63e345bd231af78e88c88109'
non_test_mode_kraken_default_int = '63e3462d231af78e88c8810c'
test_mode_kraken_default_ext = '63e34694231af78e88c8810e'
non_test_mode_kraken_default_ext = '63e346e5231af78e88c88110'
test_mode_kraken_default_demoApp = '63e34b96231af78e88c88112'
default_onlinefeeder_ext = '63e34ec1231af78e88c88114'
default_onlinefeeder_int = '63e34f12231af78e88c88116'
ext_non_test_mode_kraken_default_InMobi = '63eb5bdbc8ae25a642511d0f'
ext_test_mode_kraken_default_InMobi = '63eb5c9ac8ae25a642511d12'

jaeger_adjuster = 1.3

test_mode_device_id = '4423DD36-2738-46DC-84D1-02A47F95320D'

test_device_id = '4423DD36-2738-46DC-84D1-02A47F95320D88'
default_non_match_super_token = '1:MXw3NGIyYjgzYjAwMGQxMTRhZDUzMzQzYTU4MjMwZmY0MzM0NTZmNGVjfGJxdWR2b2MxYjRjcDdibjdxcmVn'
test_mode_super_token_v1 = '1:MXw3MjA4ZTQ3YzdkYTMxYWIxNTFjMzVjYWEzNzI1MmZjZGRkY2U3YjI1fGJ0YmI4dG9vNzFhbWs1aW1idGZn'
test_mode_super_token_v2 = '2:MXw3MjA4ZTQ3YzdkYTMxYWIxNTFjMzVjYWEzNzI1MmZjZGRkY2U3YjI1fGJ0Zmo0b2ttb25zcGQ0ZmZzdTBnOjEx'
s2s_test_mode_token = 'server-to-server'
test_hbp_impression_ext_param = 'Khd6Z7WLkYZMsj-DAj1MmgGxkK_PGadBMtDyq6YoxO8OjUfB2xW1MAEuHSabI6PAX7LekQWarl0i_6rQn-r' \
                                '9kodJzGwbEfauXTl3QFZmr9FQG-M5-8nKY9L_0bcFmntEzdSppli4nifp9sjsPJbP9PHd4QRu-TYyG1as-qrE' \
                                'Rfi-x76xvG6WC3PJABWr7tyZqf7awWzQpqrXSIL5nytq9WzQUtUW94aA8wgenFKyuuS2lxUrR5tnf5uTMkAcp' \
                                'RJeLLN2j6POGJRoV_jqUn0zb_PyxhbZjdYwMYrtWrO-iqsDv-gZEHYTBi2f_QvfFq3O_B2-y7o0kL9hkCKR-P' \
                                'Zo&f=b'
test_hbp_impression_no_f_b_param = 'aG7cGdIZdP_A2SWGQ21byFMfc6PtUlptKhsxQuqCW-Ygj_ZdhEWvWFMC1r6K9wl-FuWTwBlgRZOfKVVSYbTGP8cnLwzd1unFcUoz73KNPai4APfZ1NhlZQEtoceLT6-723Kf0z3B6DU_1iZ9vWSBOuNFGvL8jtz5_zpaSbjioF4vubCj2ydTwK14u5uz9Rb0FxtIqw3o0ZE1tSL-3UKmhMcVc4YkWGojeD31uFnkmSNc2AYVkCSjFD0sMq8saDLDiSSIuSO3r4UbTmHjSRt0qLRdDl73tqsEAK9zQZImen5C4tyB-gWId83JyoUd2ikY2UQAcydnddZv2MO2RQIP_Rcnmw=='
test_sdk_notification_ext_param = 'yI-g5OlQV1eLdEQJQQBO5mlCd1b4GJszi5MO7u6SeTyk0M56nbsdx85TkNDMAGze5sAgL3UGPI4XLM1wMsWBxeeHpfr7aSKgiyw0TDz3tkUveJvPWLCEugt5aKDQJDMhKhQNnlIPMsHB7pKahRj5ybrFt0ub4NH0-W4igroKO0lRMb22JcAf1m8Kpyh_IhcKuOx_ZOZDfanu3xIkAz-K_ZicmwmBf-bKjosOa-PwophTy33V2yrfAletS_108VAHT36Wpyp3xDQPK5INyJo2dGXbV7iohQ877JlYCXihy9Njlvgq2ROX7NO5kyLtWJImDDMURh8dj7-wxG17r9-dPSIb6p-2lRBQOuWZDX4='
test_deal_id = '5ba3e9bbc57a320010d8f9f0'
test_real_time_token = '3%3AH4sIAEsFamMC/72WWZOqOBSA/8otnqe6WVynah4AN2xQURRwaooKEFmMgOza3f99gqZv3ZrJPPTL%2BAIkX75zkpwyeWdyeK1gUTK//3hnvDQ5RYED2xImRZQmuJGRY3GnBulxOx8L7qWtbXO78RbbzDXRwLbwk%2B%2BftFi8aaGyMQSJBSaXwcsMP8eVxY7Xc3G6m8Q6p8bTdnXrtdpErDRjf1cC8SoE0zeJn1XHxbIGpr4T716lteliz89KTzhUx5ui7DlJUfeNgGNcz/ps5QpZ5s7bUL3vK00WU2OOKt8Khsr0pydYyT1WjZWhMlvpO5nTVnelUaZLDpjtWWXLzWGi93fyOdAtqXHnB%2BtoLlVg6fXK0AQ11nhFDtXdbLsy5CZw5yg/7qTF0Vzl7u0cHC6Hm8ej2o1GOIYY6Hx4c3kOqXetwd84px6OxdX2BRV4nGGbx9C7nH%2B6NUXU1oqo24H9Js385faMrlKQTg8smu8sZSnr4vO3EV9hYCuBItthM/qD%2Be0Hk%2BZ%2BlADk1BFs8N4McVOWQw94IfSdMj3jXcPNfzL8xzrLVWswXH14/BhBFoX9oh%2B7bJSmo5DtVPzHTD7YpZXwNCR4IrGroOHVuFOQiFgk01yr8DChIcRiZG1xH8ZjChITy7aftiOOH9EQYtEjGKi9Q0xBzsRy5696uzueaAix3CWJF%2BqUFgh9WSp15inLGQ0hFmT7HNsvIwpyIZbVadSw81qmIcSyyWq%2B7Im0XBJisU%2BhP7LdAQ0hFmXYVOLOpgVKiYWrg6M1F3MaQiyBJKWDcv9GQTJiGXpTbTLndBpCLO5efLMHDS3QlVhE2zjJs4tLQ4gFXNHhnsGCguTEsjhxal8%2B0Sw5schv7m3a6ikFKYglzmz8R4IWNIRYzhcZTdoebadLYonGe9YK3B4NIRZ7GZ8OfA0pSEUs3sioWNW1aAixWM1ppIhJSEHqr3VZK%2BZYMDwaQiyrPXfm9YxSdWOWWNjCVMxqiWhIwPyFmcI/O1UBcwcEMOnODuZQJQGCr4MXjnvhmE/M%2BLCOPPg4V1xQljC/OQWo8RiYABdBH/eUeQUxiUASVNjUeWBSdUmU0QU69zR5tIlFBF53IaZCEHW9dYoq3I9gDREGcESOx80g8fM08h8hybvz%2BGS049pYqIJmHEVjI6725kY3hPVuLenLpWkt5vulPOjEIMucApbfGdVNFVzA/XFa/s9xfz2o35mocIrIhygF/r/XuPAdD%2BS%2BA2oQoa7vl660Sv45orNHJ/CdOURp8UzDP9XfmkUTJX7aPAeDImy%2BswjdeHxrKZ5ViG8wXgYeL0UJyqpzMmlW4tMxrcpHsMDP8v8EnouRP6qWySoXRUUI8675AosCV6iD6/frYsS9sF%2BVil2XrCtEXuB7Qk94ZpU9U/n8/PwbB9A842YJAAA%3D'
test_demoApp_response = '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'

# test_real_time_token = '3:H4sIAAAAAAAAE21Sy27CMBD8lz0TSAIESE+ojx+o1EuprCVegoWxUz9CW8S\/dw1UakV9sC3PeD0z6yM01ngyAeojNE2HafUBQ\/RQg+0CSaEMnAbQys79AaPZGXswMICg9sTH+w7qfAC899iS6Ml5ZQ0zmeJtdA3xvotrrfyWHJy4qKRepePjuYb4siZxll7havS8RdNuUfFtZX3iKLnpGa6Kx2VRjqtsnBezbLJY3mfz5WyRlZMqr55m5eJhOk+K1xgCuU\/hkaUIMrjWJKHeoPbENTfsFfLryP6ZfgYL0Cwlsim+Qclxb3VkvZp60mx6WF2Y5Xg+KebT2aIYAH0EMpcAjsm+kbcSvPBKkrZ4i3kpGnRSYI9KJ+iKpNQcvUcO\/NwyazaqFb8eS2lbJ5VBLXpFB6hZTOeowWbLzQx2x0yoX9\/SGzsRPWfDztIPgJdoWk2rUTUsymF+ZzConrhR3yRGw50mAgAA'

# Feature switch flags
wurfl_flag = False
new_gdpr_flag = False

# AWS
kraken_s3_bucket_qa = 'vungle2-cdn-qa'

kraken_served_ad_network_id = 'APZHY3VA96.skadnetwork'

# Device related
test_common_os = 'ios'
test_common_versions = {
    "ios": {
        "multiple_cache": "Vungle/6.10.1",
        "non_multiple_cache": "Vungle/6.10.0"
    },
    "android": {
        "multiple_cache": "VungleDroid/6.10.1",
        "non_multiple_cache": "VungleDroid/6.10.0"
    },
}
test_default_sdk_version = 'Vungle/6.10.0'
test_default_multi_cache_sdk_version = 'Vungle/6.10.1'
test_default_real_time_sdk_version = 'Vungle/6.12.0'
pre_real_time_sdk_version = 'Vungle/6.11.0'

# invalid token
test_common_invalid_token = 'abc123:2'

# real-time ad
test_config_extension = 'CjASLgoZRG93bmxvYWRPcHRpbWl6YXRpb25fMjAyMhIPT3B0aW1pemF0aW9uX09OGAESDjQ1LjExNy4xMDAuMTUzIgAq' \
                        '3gEKB2FuZHJvaWQSAzcuMxoHU2Ftc3VuZyIIU1BILUw3MjAqkQFNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNC40' \
                        'LjI7IFNQSC1MNzIwIEJ1aWxkL0tPVDQ5SCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVy' \
                        'c2lvbi80LjAgQ2hyb21lLzMwLjAuMC4wIE1vYmlsZSBTYWZhcmkvNTM3LjM2MIAMOIAQYgYKBFdJRklqBgoEV0lGSXIJ' \
                        'CQAAAAAAAPA/egYIgICYhw8='
test_pre_cached_tokens = [
    "2|OprLX67N|c29le0lh5s5jb0ioo8h0",
    "2|FCVYtXn2|c29le0lh5s5jb0ioo8hg",
    "2|jbIl7qTz|c29le0lh5s5jb0ioo8i0",
    "2|BWWOLeVD|c29le0lh5s5jb0ioo8ig",
    "2|Tpxsz7j9|c29le0lh5s5jb0ioo8j0",
    "2|R5ox8128|c29le0lh5s5jb0ioo8jg",
    "2|QiegL4Vj|c29le0lh5s5jb0ioo8k0",
    "2|z2qQxSZf|c29le0lh5s5jb0ioo8kg",
    "2|zBB23vo8|c29le0lh5s5jb0ioo8l0",
    "2|zuLFcIJF|c29le0lh5s5jb0ioo8lg",
    "2|lYd105ti|c29le0lh5s5jb0ioo8m0",
    "2|Nf8w0GvC|c29le0lh5s5jb0ioo8mg",
    "2|Ppv2t4A8|c29le0lh5s5jb0ioo8n0",
    "2|Yfhd8Yb6|c29le0lh5s5jb0ioo8ng",
    "2|I7wuASYC|c29le0lh5s5jb0ioo8o0",
    "2|1vgZXGAr|c29le0lh5s5jb0ioo8og",
    "2|gBBo6tUK|c29le0lh5s5jb0ioo8p0",
    "2|7cEMDG1Q|c29le0lh5s5jb0ioo8pg",
    "2|bUAKY6wr|c29le0lh5s5jb0ioo8q0",
    "2|AYTfCFmb|c29le0lh5s5jb0ioo8qg",
    "2|aqlVzpes|c29le0lh5s5jb0ioo8r0",
    "2|Hf1L5Cfb|c29le0lh5s5jb0ioo8rg",
    "2|CKbyExQo|c29le0lh5s5jb0ioo8s0",
    "2|jpYGxhlH|c29le0lh5s5jb0ioo8sg",
    "2|kmClDx4i|c29le0lh5s5jb0ioo8t0",
    "2|i9U0Xgb4|c29le0lh5s5jb0ioo8tg",
    "2|YJjfV2ve|c29le0lh5s5jb0ioo8u0",
    "2|c8Tu0LbX|c29le0lh5s5jb0ioo8ug",
    "2|Xwf8IAnh|c29le0lh5s5jb0ioo8v0",
    "2|HOIW93Tc|c29le0lh5s5jb0ioo8vg",
    "2|NU1k2Qp8|c29le0lh5s5jb0ioo900",
    "2|0sWIWuJl|c29le0lh5s5jb0ioo90g"
]

# plugin name and version
test_in_house_plugin_name = 'vunglehbs/108.0.0'
test_in_house_partner = 'vacto_test'
test_commercial_plugin_name = 'adtoapp'
test_commercial_partner = 'adtoapp'

# real time perf test data
test_full_screen_placement = 'REALTIME-FULLSCREEN-1'
test_banner_placement = 'BANNER_REALTIME_TEST_1-9633704'
test_video_placement = 'VIDEO_REALTIME_TEST-3176951'
test_legacy_placement = 'DEFAULT02021-LOCAL-1'

# real time invalid token
test_invalid_token = '3:abc123erefeeo'

# override bid.ext
test_default_bid_ext = {
    "vungle": {
        "ad_app_object_id": "4ee19fb8121ae61a03000022",
        "ad_app_store_id": "adv-store-id",
        "vid": "562721e66ddcba3a68000053",
        "attribution_method": "skadnetwork",
        "conv_rate": 0.002,
        "erpm": 1,
        "no_override": False
    }
}
# new app devices make& model info
new_app_devices = [
    {"make": "13 Pro", "model": "iPhone14,2"},
    {"make": "13 Pro Max", "model": "iPhone14,3"},
    {"make": "13 Mini", "model": "iPhone14,4"},
    {"make": "Air (4th generation)", "model": "iPad13,1"},
    {"make": "Air (4th generation)", "model": "iPad13,2"},
    {"make": "Pro 11 (3rd generation)", "model": "iPad13,4"},
    {"make": "Pro 11 (3rd generation)", "model": "iPad13,5"},
    {"make": "Pro 11 (3rd generation)", "model": "iPad13,6"},
    {"make": "Pro 11 (3rd generation)", "model": "iPad13,7"},
    {"make": "Pro 12.9 (5th generation)", "model": "iPad13,8"},
    {"make": "Pro 12.9 (5th generation)", "model": "iPad13,9"},
    {"make": "Pro 12.9 (5th generation)", "model": "iPad13,10"},
    {"make": "Pro 12.9 (5th generation)", "model": "iPad13,11"},
    {"make": "Mini (6th generation)", "model": "iPad14,1"},
    {"make": "Mini (6th generation)", "model": "iPad14,2"},
]

# block ios 15 apps
block_ios_15_apps = [
    {"pub_app": "5dd7f2e50f531500173c99a0", "placement": "INTERSTITIALMID-5352130"}
]
block_ios_15_conflict_test_app = '612c37d512e73fc3801ac47a'
block_ios_15_conflict_test_placement = 'DEFAULT02021222'
block_ios_15_all_version_test_app = '59786bc2a43b3a08620026d1'
block_ios_15_all_version_test_placement = 'DEFAULT02021333'

# bCAT Rollour Beta Apps
bCAT_beta_apps = [

    {
        "pub_app": "5bfdd57d5a379f6a39dd658f",
        "placement": "DEFAULT-9694334",
        "merged_iab": ['IAB7-3', 'IAB7-5', 'IAB7-28', 'IAB7-29', 'IAB7-30', 'IAB7-39', 'IAB7-41', 'IAB7-42', 'IAB8-5',
                       'IAB8-18', 'IAB9-9', 'IAB11', 'IAB14-2', 'IAB14-3', 'IAB14-4',
                       'IAB14-8', 'IAB18-2', 'IAB23', 'IAB25-1', 'IAB25-2', 'IAB25-3', 'IAB25-4', 'IAB25-5',
                       'IAB25-6', 'IAB26']
    },
    {
        "pub_app": "5e6868c8ffd487601beebc7a",
        "placement": "bcat_DEFAULT02021",
        "merged_iab": ["IAB8-18", "IAB8-5", "IAB25-6", "IAB25-1", "IAB25-2", "IAB25-3", "IAB25-4", "IAB25-5", "IAB26",
                       "IAB7-42", "IAB7-3", "IAB7-5", "IAB7-28", "IAB7-29", "IAB7-30", "IAB7-39", "IAB7-41", "IAB18-2",
                       "IAB23", "IAB9-9", "IAB9-7", "IAB9-30", "IAB11", "IAB14-2", "IAB14-3", "IAB14-4", "IAB14-8",
                       "IAB14-1", "IAB24"]
    },
    {
        "pub_app": "556f747e67c16c382100006e",
        "placement": "IOS_INTERSTITIAL_HIGH-3871950",
        "merged_iab": ["IAB8-18", "IAB8-5", "IAB25-6", "IAB25-1", "IAB25-2", "IAB25-3", "IAB25-4", "IAB25-5", "IAB26",
                       "IAB7-42", "IAB7-3", "IAB7-5", "IAB7-28", "IAB7-29", "IAB7-30", "IAB7-39", "IAB7-41", "IAB18-2",
                       "IAB23", "IAB9-9", "IAB9-7", "IAB9-30", "IAB11", "IAB14-2", "IAB14-3", "IAB14-4", "IAB14-8",
                       "IAB14-1"]
    },
    {
        "pub_app": "59e7db9b598ece421700ded4",
        "placement": "DEFAULT39798",
        "merged_iab": ["IAB8-18", "IAB8-5", "IAB25-6", "IAB25-1", "IAB25-2", "IAB25-3", "IAB25-4", "IAB25-5", "IAB26",
                       "IAB7-42", "IAB7-3", "IAB7-5", "IAB7-28", "IAB7-29", "IAB7-30", "IAB7-39", "IAB7-41", "IAB18-2",
                       "IAB23", "IAB9-9", "IAB9-7", "IAB9-30", "IAB11", "IAB14-2", "IAB14-3", "IAB14-4", "IAB14-8",
                       "IAB14-1", "IAB24"]
    },
]

bCAT_beta_windows_apps = [
    {
        "pub_app": "57979405fb0fb7fc6e0000a2",
        "placement": "TEST_PLACEMENT-5724472",
        "merged_iab": ['IAB7-3', 'IAB7-5', 'IAB7-28', 'IAB7-29', 'IAB7-30', 'IAB7-39', 'IAB7-41', 'IAB7-42', 'IAB8-5',
                       'IAB8-18', 'IAB9-9', 'IAB11', 'IAB14-1', 'IAB14-2', 'IAB14-3', 'IAB14-4',
                       'IAB14-8', 'IAB18-2', 'IAB23', 'IAB25-1', 'IAB25-2', 'IAB25-3', 'IAB25-4', 'IAB25-5',
                       'IAB25-6', 'IAB26', 'IAB24']
    }
]

bCAT_block_android_apps = [
    {
        "pub_app": "5ae1d7c5cf3ad762761bbca1",
        "placement": "DEFAULT-2761168",
        "merged_iab": ['IAB7-3', 'IAB7-5', 'IAB7-28', 'IAB7-29', 'IAB7-30', 'IAB7-39', 'IAB7-41', 'IAB7-42', 'IAB8-5',
                       'IAB8-18', 'IAB9-9', 'IAB11', 'IAB14-2', 'IAB14-3', 'IAB14-4', 'IAB14-8', 'IAB18-2', 'IAB23',
                       'IAB25-1', 'IAB25-2', 'IAB25-3', 'IAB25-4', 'IAB25-5', 'IAB25-6', 'IAB26', 'IAB7-25', 'IAB7-26',
                       'IAB9-7', 'IAB14-1', 'IAB14-6', 'IAB24', 'IAB25-7']
    },
]

bCAT_block_ios_apps = [
    {
        "pub_app": "5aafe5c62567717fa575bfc1",
        "placement": "DEFAULT-7568220",
        "merged_iab": ["IAB7-3", "IAB7-5", "IAB7-26", "IAB7-28", "IAB7-29", "IAB7-30", "IAB7-39", "IAB7-41", "IAB7-42",
                       "IAB8-5", "IAB8-18", "IAB9-7", "IAB9-9", "IAB11", "IAB14", "IAB18-2", "IAB23", "IAB24",
                       "IAB25-1", "IAB25-2", "IAB25-3", "IAB25-4", "IAB25-5", "IAB25-6", "IAB25-7", "IAB26", ]
    },
]

# max duration test apps
max_duration_apps_skippable_true = [
    {"pub_app": "605dde0782080856bc7cee61",
     "placement": "add_SOLITAIRE_AND_24",
     },
]

max_duration_apps_skippable_false = [

    {"pub_app": "605dde0782080856bc7cee61",
     "placement": "add_SOLITAIRE_AND",
     },
]

max_duration_apps_skippable_true_with_duration = [
    {"pub_app": "5f2e8f265177fa00011048d0",
     "placement": "Sad_OLITAIRE_ANDROID_MIDDLE",
     }
]

max_duration_rewarded_apps = [
    {"pub_app": "5587c25959b1a0201a0001ad",
     "placement": "RV_TOPCPM-7972055",
     },
    {
        "pub_app": "5587c25959b1a0201a0001ad",
        "placement": "MJP_IPAD_MAX-0402488",
    },
    {
        "pub_app": "5587c25959b1a0201a0001ad",
        "placement": "MIDDLE_REWARDED-5381261",
    },
    {
        "pub_app": "61f4280b84c6b60a3a481d4a",
        "placement": "RV_TOPCPM-7972055_1",
    }
]

max_duration_apps = [
    {"pub_app": "60a4d2c2cf4957c21093d8b5",
     "placement": "MJP_IPAD_INTERS_01",
     },
    {"pub_app": "5f08659e0897e90001009cd9",
     "placement": "MJP_IPAD_INTERS_03",
     },
    {"pub_app": "5e591bfbb818d51acfbab923",
     "placement": "MJP_IPAD_INTERS_04",
     },
    {"pub_app": "611bbee5350eb6e37c140bf6",
     "placement": "MJP_IPAD_INTERS_05",
     },
    {"pub_app": "61e67d8580084a20aace19e4",
     "placement": "MJP_IPAD_INTERS_06",
     },
    {"pub_app": "5ebe454758afe50001bcabe7",
     "placement": "MJP_IPAD_INTERS_07",
     },
    {"pub_app": "5fb248e5e318e5949e7f5b7b",
     "placement": "MJP_IPAD_INTERS_08",
     },
]
# max duration data
max_duration_app_exp1 = '5587c25959b1a0201a0001ad'
max_duration_placement_exp1 = 'MJP_IPAD_INTERS_MAX-4859284'
max_duration_app_skipable_false_exp1 = '5c093910a4a7ea3d70999820'
max_duration_placement_skipable_exp1 = 'SOLITAIRE_AND_13-3715085'
max_duration_apps_skippable_true_with_duration_exp1 = '5c093910a4a7ea3d70999820'
max_duration_placement_skippable_true_with_duration_exp1 = 'SOLITAIRE_ANDROID_MIDDLE-6186301'
max_duration_app_skippable_true_exp1 = '5c093910a4a7ea3d70999820'
max_duration_placement_skippable_true_exp1 = 'SOLITAIRE_AND_23-1199646'
max_duration_app_rewarded_exp1 = '5c093910a4a7ea3d70999820'
max_duration_placement_rewarded_exp1 = 'SOLITARIER-5577962'

# blocks ads for specify countries
block_specify_country = [
    {"pub_app": "6285f9081f830de563bea707",
     "placement": "DEFAULT02021_10",
     }
]
block_specify_country_android = [
    {"pub_app": "5c59c48d1c97903089cff8cc",
     "placement": "DEFAULT-2760075",
     },
    {"pub_app": "58a1c10244dfb6ec57000178",
     "placement": "REDMINOTE4-6436938",
     },
    {"pub_app": "59384c8dfa7de1c1580000ff",
     "placement": "REDMINOTE4-6436938-copy",
     },
    {"pub_app": "62945e6888f882e710178fe6",
     "placement": "REDMINOTE4-6436938-copy-1",
     },
]
# device mapping

device_mapping_android_path = get_root + '/data/device_mapping/Vungle Size Consolidation to Liftoff DSP - Android Sizes .csv'
device_mapping_ios_path = get_root + '/data/device_mapping/Vungle Size Consolidation to Liftoff DSP - IOSizes.csv'

default_ios_test_ad_size = {
    "h": 1792,
    "w": 828
}

default_android_test_ad_size = {
    "h": 1920,
    "w": 1080
}

default_windows_test_ad_size = {
    "h": 1200,
    "w": 900
}

# SKO related test data
test_fsc_adv_pref_skfsc_default = '59786bc2a43b3a08620016b1|DEFAULT02021'
test_fsc_fsc_on_skfsc_default = '59786bc2a43b3a08620026b1|HJKM6GM50919'
test_fsc_fsc_off_skfsc_default = '59786bc2a43b3a08620026b1|DEFAULT02021'

test_fsc_adv_pref_skfsc_product_view = '59786bc2a43b3a08620016b2|DEFAULT02021'
test_fsc_fsc_on_skfsc_product_view = '59786bc2a43b3a08620016b2|DEFAULT02022'
test_fsc_fsc_off_skfsc_product_view = '59786bc2a43b3a08620016b2|DEFAULT02023'

test_fsc_adv_pref_skfsc_overlay_view = '59786bc2a43b3a08620016b3|DEFAULT02021'
test_fsc_fsc_on_skfsc_overlay_view = '59786bc2a43b3a08620016b3|DEFAULT02022'
test_fsc_fsc_off_skfsc_overlay_view = '59786bc2a43b3a08620016b3|DEFAULT02023'

test_fsc_adv_pref_skfsc_off = '59786bc2a43b3a08620016b4|DEFAULT02021'
test_fsc_fsc_on_skfsc_off = '59786bc2a43b3a08620016b4|DEFAULT02022'
test_fsc_fsc_off_skfsc_off = '59786bc2a43b3a08620016b4|DEFAULT02023'

# kona exp releated:
config_extension_cn_ip = 'Eg8xMTcuMTM2LjI0MC4xMjEiACrJAQoDaU9TEgQxMi40GgVBcHBsZSIKaVBob25lMTUsNiptTW96aWxsYS81LjAgKGlQaG9uZTsgQ1BVIGlQaG9uZSBPUyAxMl80IGxpa2UgTWFjIE9TIFgpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgTW9iaWxlLzE1RTE0ODDaCTiAFVoOCgxlbWlseV9tb2JpbGViBgoEd2lmaWoICgZ3aWZpQUFyCQkAAAAAAADwv3oHCICgtvrSBjICCAE='
config_extension = "CiQKIgoUS09OQVZlcmlmeUFCXzAzMjlfMTASCm5vX0tPTkFBQjI="
config_extension_1 = "CkYSJAoVQXV0b0NhY2hlXzIwMjJfUGhhc2UxEglBdXRvQ2FjaGUYARIeChFLT05BVmVyaWZ5QUJfNDA2OBIHS09OQUFCMhgB"
real_time_config_extension_noCache = "CjQSMgoZUmVhbF9UaW1lX0Fkc18yMDIyX1BoYXNlMBITUmVhbFRpbWVBZHNfTm9DYWNoZRgB"
real_time_config_extension_1 = 'Ch8SHQoZUmVhbF9UaW1lX0Fkc18yMDIyX1BoYXNlMBgC'
real_time_config_extension_disabled = "CjUSMwoZUmVhbF9UaW1lX0Fkc18yMDIyX1BoYXNlMBIUUmVhbFRpbWVBZHNfRGlzYWJsZWQYAQ=="
config_extension_ip = 'Eg4zNy4xNjQuMTYyLjE3MQ=='
config_extension_do_exp_with_on = 'CjASLgoZRG93bmxvYWRPcHRpbWl6YXRpb25fMjAyMhIPT3B0aW1pemF0aW9uX09OGAESDDE1MS45NS4yMTkuNg=='
config_extension_do_exp_with_off = 'CjESLwoZRG93bmxvYWRPcHRpbWl6YXRpb25fMjAyMhIQT3B0aW1pemF0aW9uX09GRhgBEgwxNTEuOTUuMjE5LjY='
real_time_config_extension_SKAN_ids = 'Eg8xMTcuMTM2LjI0MC4xMjEaDnRlc3QuYWQubncuMDAxGhB0ZXN0Lm53LjQ1NjQ2NTQ2'
config_extension_lmt_flag_0 = 'CjASLgoZRG93bmxvYWRPcHRpbWl6YXRpb25fMjAyMhIPT3B0aW1pemF0aW9uX09OGAESDjQ1LjExNy4xMDAuMTUzIgA='
config_extension_lmt_flag_1 = 'CjASLgoZRG93bmxvYWRPcHRpbWl6YXRpb25fMjAyMhIPT3B0aW1pemF0aW9uX09OGAESDjQ1LjExNy4xMDAuMTUzIgIIAQ=='
config_extension_RTA = 'Eg03Mi4yMjkuMjguMTg1IgAqyQEKA2lPUxIEMTIuNBoFQXBwbGUiCmlQaG9uZTE1LDYqbU1vemlsbGEvNS4wIChpUGhvbmU7IENQVSBpUGhvbmUgT1MgMTJfNCBsaWtlIE1hYyBPUyBYKSBBcHBsZVdlYktpdC82MDUuMS4xNSAoS0hUTUwsIGxpa2UgR2Vja28pIE1vYmlsZS8xNUUxNDgw2gk4gBVaDgoMZW1pbHlfbW9iaWxlYgYKBHdpZmlqCAoGd2lmaUFBcgkJAAAAAAAA8L96BwiAoLb60gY='
config_extension_android = 'Ch4SHAoRS09OQVZlcmlmeUFCXzQwNjgSB0tPTkFBQjISDjM3LjE2NC4xNjIuMTcxIgAq4AEKB2FuZHJvaWQSAzcuMxoHU2Ftc3VuZyIIU1BILUw3MjAqkQFNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNC40LjI7IFNQSC1MNzIwIEJ1aWxkL0tPVDQ5SCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzMwLjAuMC4wIE1vYmlsZSBTYWZhcmkvNTM3LjM2MIAMOIAQWgBiBgoEV0lGSWoGCgRXSUZJcgkJAAAAAAAA8D96BgiAgJiHDw=='
config_extension_RTA_1 = 'IgAqyQEKA2lPUxIEMTIuNBoFQXBwbGUiCmlQaG9uZTE1LDYqbU1vemlsbGEvNS4wIChpUGhvbmU7IENQVSBpUGhvbmUgT1MgMTJfNCBsaWtlIE1hYyBPUyBYKSBBcHBsZVdlYktpdC82MDUuMS4xNSAoS0hUTUwsIGxpa2UgR2Vja28pIE1vYmlsZS8xNUUxNDgw2gk4gBVaDgoMZW1pbHlfbW9iaWxlYgYKBHdpZmlqCAoGd2lmaUFBcgkJAAAAAAAA8L96BwiAoLb60gY='
config_extension_RTA_disabled_ad_id = 'Ch4SHAoRS09OQVZlcmlmeUFCXzQwNjgSB0tPTkFBQjISDjM3LjE2NC4xNjIuMTcxIgAq4AEKB2FuZHJvaWQSAzcuMxoHU2Ftc3VuZyIIU1BILUw3MjAqkQFNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNC40LjI7IFNQSC1MNzIwIEJ1aWxkL0tPVDQ5SCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzMwLjAuMC4wIE1vYmlsZSBTYWZhcmkvNTM3LjM2MIAMOIAQWgBiBgoEV0lGSWoGCgRXSUZJcgkJAAAAAAAA8D96BgiAgJiHDzIA'
config_extension_RTA_android_disabled = 'Cj8SPQojUmVhbF9UaW1lX0Fkc18yMDIyX0RlY19BbmRyb2lkXzEyMDcSFFJlYWxUaW1lQWRzX0Rpc2FibGVkGAESDjQ1LjExNy4xMDAuMTUzIgAq4AEKB2FuZHJvaWQSAzcuMxoHU2Ftc3VuZyIIU1BILUw3MjAqkQFNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgNC40LjI7IFNQSC1MNzIwIEJ1aWxkL0tPVDQ5SCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzMwLjAuMC4wIE1vYmlsZSBTYWZhcmkvNTM3LjM2MIAMOIAQWgBiBgoEV0lGSWoGCgRXSUZJcgkJAAAAAAAA8D96BgiAgJiHDzIA'
config_extension_RTA_android_realtime = 'Cj4SPAojUmVhbF9UaW1lX0Fkc18yMDIyX0RlY19BbmRyb2lkXzEyMDcSE1JlYWxUaW1lQWRzX05vQ2FjaGUYARIONDUuMTE3LjEwMC4xNTMiACrgAQoHYW5kcm9pZBIDNy4zGgdTYW1zdW5nIghTUEgtTDcyMCqRAU1vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA0LjQuMjsgU1BILUw3MjAgQnVpbGQvS09UNDlIKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvMzAuMC4wLjAgTW9iaWxlIFNhZmFyaS81MzcuMzYwgAw4gBBaAGIGCgRXSUZJagYKBFdJRklyCQkAAAAAAADwP3oGCICAmIcPMgA='
