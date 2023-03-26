from utils.common import gen_device_id, generate_unique_objId, gen_test_app_id
from settings import *


def config_v4_ios(pub_app_id='59786bc2a43b3a08620026b1'):
    data = {
        "isu": "a316243b6ae0739e",
        "pubAppId": pub_app_id
    }
    return data


def config_v5_ios(pub_app_id='59786bc2a43b3a08620026b1', placement_id=None, auto_cached=None, skadnetwork_ids=None,
                  gdpr='opted_in', coppa=None, ext=None, ifa=gen_device_id(), idfv=gen_device_id(), lmt=0):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.ios-sdk-app.qa",
            "ver": "14f1cf7"
        },
        "system": {
            "cache": []
        },
        "device": {
            "make": "Apple",
            "os": "ios",
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "h": 2688,
            "model": "iPhone15,6",
            "osv": "12.4",
            "ext": {
                "vungle": {
                    "ios": {
                        "volume": 0.60000002384185791,
                        "battery_state": "unknown",
                        "idfa": "",
                        "vduid": "",
                        "battery_level": -1,
                        "locale": "en_US",
                        "connection_type": "wifi",
                        "connection_type_detail": "wifiAA",
                        "language": "en",
                        "storage_bytes_available": 228426878976,
                        "idfv": idfv,
                        "battery_saver_enabled": 0,
                        "time_zone": "Asia/Shanghai"
                    }
                }
            },
            "connection_type": "wifi",
            "connection_type_detail": "wifiAA",
            "carrier": "emily_mobile",
            "ifa": ifa,
            "w": 1242,
            "lmt": lmt
        },
        "ext": {
        },
        "user": {
            "gdpr": {
                "consent_timestamp": 1565346845,
                "consent_status": gdpr,
                "consent_message_version": "publisher_version_v1.0",
                "consent_source": "publisher"
            }
        }
    }

    request_obj = {}
    if placement_id is not None:
        request_obj.update({
            "placements": [
                placement_id
            ]
        })
    if auto_cached is not None:
        request_obj.update({
            "is_auto_cached_enforced": auto_cached
        })
    if skadnetwork_ids is not None:
        request_obj.update({
            "skadnetwork": {
                "plist_adnetwork_ids": skadnetwork_ids
            }
        })
    else:
        request_obj.update({
            "skadnetwork": {
                "plist_adnetwork_ids": []
            }
        })
    data.update(request=request_obj)
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    if ext is not None:
        data.get("ext").update({"config_extension": ext})
    return data


def cache_bust_ios(pub_app_id='59786bc2a43b3a08620026b1', last_cache_bust=0):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.ios-sdk-app.qa",
            "ver": "14f1cf7"
        },
        "device": {
            "make": "Apple",
            "os": "ios",
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "h": 2688,
            "model": "x86_64",
            "osv": "12.4",
            "ext": {
                "vungle": {
                    "ios": {
                        "volume": 0.60000002384185791,
                        "battery_state": "unknown",
                        "idfa": "4423DD36-2738-46DC-84D1-02A47F95320C",
                        "vduid": "",
                        "battery_level": -1,
                        "locale": "en_US",
                        "connection_type": "wifi",
                        "language": "en",
                        "storage_bytes_available": 228426878976,
                        "idfv": "C8360A3F-81C3-4DC5-99FD-B5B28A161A6D",
                        "battery_saver_enabled": 0,
                        "time_zone": "Asia/Shanghai"
                    }
                }
            },
            "carrier": "",
            "ifa": "4423DD36-2738-46DC-84D1-02A47F95320C",
            "w": 1242,
            "lmt": 0
        },
        "request": {}
    }

    request_obj = {}
    if last_cache_bust is not None:
        request_obj.update({
            "last_cache_bust": last_cache_bust
        })
    data.update(request=request_obj)

    return data


def cache_bust_android(pub_app_id='61efb2209164cc60d4a59a7b', last_cache_bust=0):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.runscopetest",
            "ver": "1"
        },
        "device": {
            "ua": "Mozilla/5.0 (Linux; Android 4.4.2; SPH-L720 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36",
            "h": 2048,
            "make": "Samsung",
            "model": "SPH-L720",
            "os": "android",
            "osv": "7.3",
            "ext": {
                "vungle": {
                    "android": {
                        "android_id": "C8360A3F-81C3-4DC5-99FD-B5B28A161A6D",
                        "data_saver_status": "NOT_APPLICABLE",
                        "sound_enabled": 0,
                        "gaid": "",
                        "connection_type_detail": "WIFI",
                        "locale": "en_US",
                        "sd_card_available": 1,
                        "battery_level": 1,
                        "storage_bytes_available": 4041605120,
                        "connection_type": "WIFI",
                        "battery_state": "BATTERY_PLUGGED_USB",
                        "time_zone": "America/Los_Angeles",
                        "os_name": "SWDD5908",
                        "volume_level": 0,
                        "language": "en",
                        "network_metered": 0
                    }
                }
            },
            "carrier": "",
            "ifa": "C8360A3F-81C3-4DC5-99FD-B5B28A161A6D",
            "w": 1536,
            "lmt": 0
        },
        "request": {}
    }

    request_obj = {}
    if last_cache_bust is not None:
        request_obj.update({
            "last_cache_bust": last_cache_bust
        })
    data.update(request=request_obj)

    return data


def config_v5_android(pub_app_id='5a55162ccbc18a63250138c6', placement_id=None, gdpr='opted_in', auto_cached=None,
                      skadnetwork_ids=None, coppa=None, ext=None, ifa=gen_device_id(), android_id=gen_device_id()):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.runscopetest",
            "ver": "1"
        },
        "system": {
            "cache": []
        },
        "device": {
            "ua": "Mozilla/5.0 (Linux; Android 4.4.2; SPH-L720 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36",
            "h": 2048,
            "make": "Samsung",
            "model": "SPH-L720",
            "os": "android",
            "osv": "7.3",
            "ext": {
                "vungle": {
                    "android": {
                        "android_id": android_id,
                        "data_saver_status": "NOT_APPLICABLE",
                        "sound_enabled": 0,
                        "gaid": "",
                        "connection_type_detail": "WIFI",
                        "locale": "en_US",
                        "sd_card_available": 1,
                        "battery_level": 1,
                        "storage_bytes_available": 4041605120,
                        "connection_type": "WIFI",
                        "battery_state": "BATTERY_PLUGGED_USB",
                        "time_zone": "America/Los_Angeles",
                        "os_name": "SWDD5908",
                        "volume_level": 0,
                        "language": "en",
                        "network_metered": 0
                    }
                }
            },
            "carrier": "",
            "ifa": ifa,
            "w": 1536,
            "lmt": 0
        },
        "ext": {},
        "request": {},
        "user": {
            "gdpr": {
                "consent_timestamp": 1565346845,
                "consent_status": gdpr,
                "consent_message_version": "publisher_version_v1.0",
                "consent_source": "publisher"
            }
        }
    }

    request_obj = {}
    if placement_id is not None:
        request_obj.update({
            "placements": [
                placement_id
            ]
        })
    if auto_cached is not None:
        request_obj.update({
            "is_auto_cached_enforced": auto_cached
        })
    if skadnetwork_ids is not None:
        request_obj.update({
            "skadnetwork": {
                "plist_adnetwork_ids": skadnetwork_ids
            }
        })
    else:
        request_obj.update({
            "skadnetwork": {
                "plist_adnetwork_ids": []
            }
        })
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    if ext is not None:
        data.get("ext").update({"config_extension": ext})
    data.update(request=request_obj)

    return data


def config_v5_amazon(pub_app_id='5bebe77a598bee2c619dca28', placement_id=None, gdpr='opted_in', auto_cached=None,
                     skadnetwork_ids=None, coppa=None):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.runscopetest",
            "ver": "1"
        },
        "system": {
            "cache": []
        },
        "device": {
            "make": "samsung",
            "model": "SM-G973U1",
            "osv": "10.0",
            "carrier": "",
            "lmt": 1,
            "os": "Amazon",
            "ifa": "df4f1de5-9225-46f5-b363-f8d776934da9",
            "ua": "Mozilla/5.0 (Linux; Android 9; SM-G973U1 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/73.0.3683.90 Mobile Safari/537.36",
            "w": 1080,
            "h": 1920,
            "ext": {
                "vungle": {
                    "amazon": {
                        "gaid": "",
                        "battery_level": 0.93,
                        "battery_state": "BATTERY_PLUGGED_USB",
                        "battery_saver_enabled": 0,
                        "connection_type": "WIFI",
                        "connection_type_detail": "WIFI",
                        "data_saver_status": "NOT_APPLICABLE",
                        "network_metered": 0,
                        "locale": "en_US",
                        "language": "en",
                        "time_zone": "Asia/Seoul",
                        "volume_level": 0.0,
                        "sd_card_available": 1,
                        "os_name": "samsung/beyond1qlteue/beyond1q:9/PPR1.180610.011/G973U1UEU1ASBA:user/release-keys",
                        "storage_bytes_available": 109420306432,
                        "vduid": "",
                        "os_api_level": 28,
                        "is_tv": False,
                        "is_sideload_enabled": False
                    }
                }
            }
        },
        "ext": {},
        "request": {},
        "user": {
            "gdpr": {
                "consent_timestamp": 1565346845,
                "consent_status": gdpr,
                "consent_message_version": "publisher_version_v1.0",
                "consent_source": "publisher"
            }
        }
    }

    request_obj = {}
    if placement_id is not None:
        request_obj.update({
            "placements": [
                placement_id
            ]
        })
    if auto_cached is not None:
        request_obj.update({
            "is_auto_cached_enforced": auto_cached
        })
    if skadnetwork_ids is not None:
        request_obj.update({
            "skadnetwork": {
                "plist_adnetwork_ids": skadnetwork_ids
            }
        })
    else:
        request_obj.update({
            "skadnetwork": {
                "plist_adnetwork_ids": []
            }
        })
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    data.update(request=request_obj)

    return data


def config_v5_windows(pub_app_id='5c6c73d75e80a00c9fb0b31e', placement_id=None, gdpr='opted_in', auto_cached=None,
                      skadnetwork_ids=None, coppa=None):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.windows.TestApp.App",
            "ver": "6.5.13"
        },
        "device": {
            "osv": "10.0.17763.437",
            "os": "windows",
            "h": 1536,
            "w": 2048,
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; WebView/3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
            "model": "Surface Pro",
            "ifa": "3ee2d5004d82eb31db7ea9b65cb3e515",
            "lmt": 0,
            "make": "Microsoft Corporation",
            "ext": {
                "vungle": {
                    "windows": {
                        "locale": "en-US",
                        "msaid": "3ee2d5004d82eb31db7ea9b65cb3e515",
                        "ashwid": "0300cee308007c5b0500d21c0500419205004fe0060001000400da020400f05204007ab9040058ba01007efb020060100900c290",
                        "language": "en",
                        "connection_type": "wifi",
                        "battery_state": "Charging",
                        "battery_saver_enabled": 0,
                        "battery_level": 0.98,
                        "storage_bytes_available": 60895637504,
                        "time_zone": "America/Los_Angeles",
                        "os_name": "WINDOWS"
                    }
                }
            }
        },
        "user": {
            "gdpr": {
                "consent_status": gdpr,
                "consent_source": "publisher",
                "consent_message_version": "",
                "consent_timestamp": 1565346845
            }
        },
        "request": {}
    }

    request_obj = {}
    if placement_id is not None:
        request_obj.update({
            "placements": [
                placement_id
            ]
        })
    if auto_cached is not None:
        request_obj.update({
            "is_auto_cached_enforced": auto_cached
        })
    if skadnetwork_ids is not None:
        request_obj.update({
            "skadnetwork": {
                "plist_adnetwork_ids": skadnetwork_ids
            }
        })
    else:
        request_obj.update({
            "skadnetwork": {
                "plist_adnetwork_ids": []
            }
        })

    data.update(request=request_obj)
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    return data


def jaeger_v5_ios(pub_app_id='59786bc2a43b3a08620026b1', placement_id=None, gdpr=None,
                  ifa=gen_device_id(), idfv='', header_bidding=False, banner=False, ccpa=None, coppa=None, ext=None,
                  os_version='13', h=default_ios_test_ad_size['h'], w=default_ios_test_ad_size['w'],
                  skadnetwork_ids=None, vision=False, make='Apple', model='iPhone11,8', lmt=0, sound_enabled=0,
                  banner_type='banner_leaderboard', battery_saver_enabled=1, atts=0, device_connection_type='wifi',
                  ua='Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                     ' Mobile/15E148'):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.ios-sdk-app.qa",
            "ver": "1.0.9"
        },
        "system": {
            "cache": []
        },
        "device": {
            "make": make,
            "os": "ios",
            "ua": ua,
            "h": h,
            "w": w,
            "model": model,
            "osv": os_version,
            "ext": {
                "vungle": {
                    "ios": {
                        "volume": 0.5625,
                        "battery_state": "unplugged",
                        "idfa": "",
                        "vduid": "",
                        "battery_level": 0.54000002145767231,
                        "locale": "en_US",
                        "connection_type": device_connection_type,
                        "language": "en-US",
                        "storage_bytes_available": 9223372036854775807,
                        "idfv": idfv,
                        "battery_saver_enabled": battery_saver_enabled,
                        "time_zone": "America/Los_Angeles",
                        "sound_enabled": sound_enabled,
                        "atts": atts
                    }
                },

            },
            "carrier": "T-Mobile",
            "ifa": ifa,
            "lmt": lmt
        },

        "request": {},
        "user": {}
    }

    request_obj = {}
    if placement_id is not None:
        request_obj.update({
            "placements": [
                placement_id
            ]
        })
    if header_bidding:
        request_obj.update({"header_bidding": True})
    if banner:
        request_obj.update({"ad_size": banner_type})
    if skadnetwork_ids is not None:
        request_obj.update({
            "skadnetwork": {
                "matched_adnetwork_ids": skadnetwork_ids
            }
        })
    else:
        request_obj.update({
            "skadnetwork": {
                "matched_adnetwork_ids": []
            }
        })
    data.update(request=request_obj)

    gdpr_obj = {}
    if gdpr is not None:
        gdpr_obj.update({
            "gdpr": {
                "consent_timestamp": 1,
                "consent_status": gdpr,
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        })
    data.get("user").update(gdpr_obj)

    ccpa_obj = {}
    if ccpa is not None:
        ccpa_obj.update({
            "ccpa": {
                "status": ccpa
            }
        })
    data.get("user").update(ccpa_obj)
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    ext_obj = {}
    if ext is not None:
        ext_obj.update({
            "ext": {
                "config_extension": ext
            }
        })
        data.update(ext_obj)
    if vision:
        vision = {
            "vision": {
                "data_science_cache": "",
                "aggregate": [
                    {
                        "window": 3,
                        "last_viewed_creative_id": "",
                        "total_view_count": 7,
                        "creative_details": [
                            {
                                "view_count": 1,
                                "creative_id": "5fce479352a4d9001688f120",
                                "last_time_viewed": 1629154430
                            }
                        ],
                        "campaign_details": [
                            {
                                "view_count": 3,
                                "campaign_id": "60f82d4c97599e0010813443",
                                "last_time_viewed": 1629154562
                            }
                        ],
                        "advertiser_details": [
                            {
                                "view_count": 3,
                                "advertiser_id": "561941526",
                                "last_time_viewed": 1629154562
                            }
                        ]
                    }
                ]
            }
        }
        data.get("user").update(vision)

    return data


def jaeger_v5_android(pub_app_id='59e781de7fff7cb02500ca0e', placement_id=None, skadnetwork_ids=None,
                      android_id=gen_device_id(), geo=False, make='cool', model='q10',
                      h=default_android_test_ad_size['h'], w=default_android_test_ad_size['w'],
                      ua='CoolPad8190Q_CMCC_TD/1.0 Linux/3.4.5 Android/4.1 Release/03.31.2013 Browser/AppleWebkit534.3',
                      header_bidding=False, banner=False, ccpa=None, gdpr=None, coppa=None, sound_enabled=0,
                      app_set_id='', ifa='', ext=None, os_version='7.2.0'):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "1",
            "ver": "1.0.0"
        },
        "request": {},
        "device": {
            "ua": ua,
            "make": make,
            "model": model,
            "os": "android",
            "osv": os_version,
            "h": h,
            "w": w,
            "ifa": ifa,
            "ext": {
                "vungle": {
                    "android": {
                        "android_id": android_id,
                        "gaid": "",
                        "app_set_id": app_set_id,
                        "battery_level": 0.98,
                        "battery_state": "BATTERY_PLUGGED_AC",
                        "battery_saver_enabled": 0,
                        "connection_type": "MOBILE",
                        "connection_type_detail": "WIFI",
                        "data_saver_status": "DISABLED",
                        "network_metered": 1,
                        "locale": "en_GB",
                        "language": "en",
                        "time_zone": "Asia/Calcutta",
                        "volume_level": 0,
                        "sound_enabled": sound_enabled,
                        "sd_card_available": 1,
                        "os_name": "xiaomi/vince/vince:7.1.2/N2G47H/V9.5.12.0.NEGMIFA:user/release-keys",
                        "storage_bytes_available": 43734888448,
                        "vduid": "",
                        "os_api_level": 25,
                        "is_tv": False,
                        "is_sideload_enabled": True,
                        "idfv": ""
                    }
                }
            }
        },
        "ext": {},
        "user": {
            "gdpr": {
                "consent_status": "opted_in",
                "consent_source": "publisher",
                "consent_message_version": "1",
                "consent_timestamp": 1584932835
            }
        }
    }

    if geo:
        location_obj = {
            "location": {
                "latitude": "54.9735",
                "longitude": "-1.5673"
            }
        }
        data.get("device").get("ext").get("vungle").get("android").update(location_obj)

    request_obj = {}
    if placement_id is not None:
        request_obj.update({
            "placements": [
                placement_id
            ]
        })
    if header_bidding:
        request_obj.update({"header_bidding": True})
    if banner:
        request_obj.update({"ad_size": "banner_leaderboard"})
    if skadnetwork_ids is not None:
        request_obj.update({
            "skadnetwork": {
                "matched_adnetwork_ids": skadnetwork_ids
            }
        })
    else:
        request_obj.update({
            "skadnetwork": {
                "matched_adnetwork_ids": []
            }
        })
    data.update(request=request_obj)
    if ext is not None:
        data.get("ext").update({"config_extension": ext})
    gdpr_obj = {}
    if gdpr is not None:
        gdpr_obj.update({
            "gdpr": {
                "consent_timestamp": 1,
                "consent_status": gdpr,
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        })
    data.get("user").update(gdpr_obj)

    ccpa_obj = {}
    if ccpa is not None:
        ccpa_obj.update({
            "ccpa": {
                "status": ccpa
            }
        })
    data.get("user").update(ccpa_obj)
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    return data


def jaeger_v5_windows(pub_app_id='5dd72ebf001c531f8cf48083', placement_id=None, ifa='',
                      ashwid=gen_device_id(), skadnetwork_ids=None, w=default_windows_test_ad_size['w'],
                      h=default_windows_test_ad_size['h'], ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64; WebView/3.0) '
                                                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.353'
                                                              '8.102 Safari/537.36 Edge/18.18362',
                      header_bidding=False, banner=False, ccpa=None, gdpr=None, model='GL752VW',
                      make='ASUSTeK COMPUTER INC.', coppa=None):
    data = {
        "device": {
            "osv": "10.0.18362.592",
            "os": "windows",
            "h": h,
            "w": w,
            "ua": ua,
            "model": model,
            "ifa": ifa,
            "lmt": 0,
            "make": make,
            "ext": {
                "vungle": {
                    "windows": {
                        "locale": "en-US",
                        "msaid": "3e09bc404f16b2e32de056b8216388c7",
                        "ashwid": ashwid,
                        "language": "en",
                        "connection_type": "wifi",
                        "battery_state": "Discharging",
                        "battery_saver_enabled": 0,
                        "battery_level": 0.66,
                        "storage_bytes_available": 782966620160,
                        "time_zone": "America/Los_Angeles",
                        "os_name": "WINDOWS"
                    }
                }
            }
        },
        "app": {
            "id": pub_app_id,
            "bundle": "CS_sample.App",
            "ver": "1.0.0"
        },
        "user": {
            "gdpr": {
                "consent_status": "opted_in",
                "consent_source": "publisher",
                "consent_message_version": "1.0",
                "consent_timestamp": 1584932835
            }
        },
        "request": {}
    }

    request_obj = {}
    if placement_id is not None:
        request_obj.update({
            "placements": [
                placement_id
            ]
        })
    if header_bidding:
        request_obj.update({"header_bidding": True})
    if banner:
        request_obj.update({"ad_size": "banner_leaderboard"})
    if skadnetwork_ids is not None:
        request_obj.update({
            "skadnetwork": {
                "matched_adnetwork_ids": skadnetwork_ids
            }
        })
    else:
        request_obj.update({
            "skadnetwork": {
                "matched_adnetwork_ids": []
            }
        })
    data.update(request=request_obj)

    gdpr_obj = {}
    if gdpr is not None:
        gdpr_obj.update({
            "gdpr": {
                "consent_timestamp": 1,
                "consent_status": gdpr,
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        })
    data.get("user").update(gdpr_obj)

    ccpa_obj = {}
    if ccpa is not None:
        ccpa_obj.update({
            "ccpa": {
                "status": ccpa
            }
        })
    data.get("user").update(ccpa_obj)
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    return data


def jaeger_v5_amazon(pub_app_id='5bebe77a598bee2c619dca28', placement_id=None, ifa=gen_device_id(),
                     skadnetwork_ids=None,
                     ua='Mozilla/5.0 (Linux; Android 9; SM-G973U1 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/73.0.3683.90 Mobile Safari/537.36',
                     header_bidding=False, banner=False, ccpa=None, gdpr=None, sound_enabled=0,
                     make='samsung', model='SM-G973U1', coppa=None, app_set_id=None):
    data = {
        "device": {
            "make": make,
            "model": model,
            "osv": "10.0",
            "carrier": "",
            "lmt": 1,
            "os": "amazon",
            "ifa": ifa,
            "ua": ua,
            "w": 1080,
            "h": 1920,
            "ext": {
                "vungle": {
                    "amazon": {
                        "gaid": "",
                        "app_set_id": app_set_id,
                        "battery_level": 0.93,
                        "battery_state": "BATTERY_PLUGGED_USB",
                        "battery_saver_enabled": 0,
                        "connection_type": "WIFI",
                        "connection_type_detail": "WIFI",
                        "data_saver_status": "NOT_APPLICABLE",
                        "network_metered": 0,
                        "locale": "en_US",
                        "language": "en",
                        "time_zone": "Asia/Seoul",
                        "volume_level": 0.0,
                        "sound_enabled": sound_enabled,
                        "sd_card_available": 1,
                        "os_name": "samsung/beyond1qlteue/beyond1q:9/PPR1.180610.011/G973U1UEU1ASBA:user/release-keys",
                        "storage_bytes_available": 109420306432,
                        "vduid": "",
                        "os_api_level": 28,
                        "is_tv": False,
                        "is_sideload_enabled": False
                    }
                }
            }
        },
        "app": {
            "id": pub_app_id,
            "bundle": "com.publisher.test",
            "ver": "repoTag:16f43be-versionTag:5.3.2-RC3"
        },
        "user": {
            "gdpr": {
                "consent_status": "opted_in",
                "consent_source": "publisher",
                "consent_message_version": "1.0",
                "consent_timestamp": 1584932835
            }
        },
        "request": {}
    }

    request_obj = {}
    if placement_id is not None:
        request_obj.update({
            "placements": [
                placement_id
            ]
        })
    if header_bidding:
        request_obj.update({"header_bidding": True})
    if banner:
        request_obj.update({"ad_size": "banner_leaderboard"})
    if skadnetwork_ids is not None:
        request_obj.update({
            "skadnetwork": {
                "matched_adnetwork_ids": skadnetwork_ids
            }
        })
    else:
        request_obj.update({
            "skadnetwork": {
                "matched_adnetwork_ids": []
            }
        })
    data.update(request=request_obj)

    gdpr_obj = {}
    if gdpr is not None:
        gdpr_obj.update({
            "gdpr": {
                "consent_timestamp": 1,
                "consent_status": gdpr,
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        })
    data.get("user").update(gdpr_obj)

    ccpa_obj = {}
    if ccpa is not None:
        ccpa_obj.update({
            "ccpa": {
                "status": ccpa
            }
        })
    data.get("user").update(ccpa_obj)
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)

    return data


def s2s_payload_ios(pub_app_id='', placement_id=None, ifa=gen_device_id(), ip=jp_ip, banner_format=None,
                    skadn=None, regs=True, is_test=None, bid_reqeust_id='6110d1c4883cf2ae0b7c8915',
                    gdpr=None, coppa=None, consent=None, ccpa=None, idfv=None):
    data = {
        "id": bid_reqeust_id,
        "imp": [
            {
                "id": "1",
                "video": {
                    "mimes": [
                        "video/mp4"
                    ],
                    "minduration": 0,
                    "maxduration": 46,
                    "protocols": [
                        2,
                        5
                    ],
                    "w": 828,
                    "h": 1792,
                    "linearity": 1,
                    "minbitrate": 250,
                    "maxbitrate": 15000,
                    "boxingallowed": 1,
                    "playbackmethod": [
                        1,
                        2,
                        3,
                        4
                    ],
                    "delivery": [
                        2,
                        1
                    ],
                    "pos": 7,
                    "api": [
                        7
                    ],
                    "companiontype": [
                        1,
                        2
                    ],
                    "ext": {
                        "skip": 0,
                        "videotype": "rewarded",
                        "rewarded": 1
                    }
                },
                "displaymanager": "Vungle",
                "displaymanagerver": "6.10.0",
                "instl": 1,
                "tagid": placement_id,
                "bidfloor": 1,
                "bidfloorcur": "USD",
                "secure": 1,
                "ext": {
                    "metric": [
                        {
                            "type": "viewability",
                            "vendor": "moat"
                        }
                    ],
                    "skadn": {
                        "version": "2.0",
                        "versions": [
                            "2.0"
                        ],
                        "sourceapp": "1131184101",
                        "skadnetids": []
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "u5f69u7ea2u7adeu731c1",
            "bundle": "1131184101",
            "storeurl": "https://itunes.apple.com/cn/app/id1131184101",
            "cat": [
                "IAB1",
                "IAB9"
            ],
            "ver": "1.0.9",
            "privacypolicy": 1,
            "publisher": {
                "id": "597565c6c5511a1b62000990",
                "cat": [
                    "IAB1",
                    "IAB9"
                ]
            },
            "keywords": "app,account,managed"
        },
        "device": {
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "geo": {
                "lat": 35.6887,
                "lon": 139.745,
                "type": 2,
                "ipservice": 3,
                "country": "JPN",
                "region": "13",
                "city": "Tokyo",
                "zip": "102-0082"
            },
            "dnt": 0,
            "lmt": 0,
            "ip": ip,
            "devicetype": 4,
            "make": "Apple",
            "model": "iPhone",
            "os": "iOS",
            "osv": "13",
            "hwv": "XR",
            "h": 1792,
            "w": 828,
            "language": "en",
            "carrier": "T-Mobile",
            "connectiontype": 2,
            "ifa": ifa,
            "dpidsha1": "cf6bb0b5283b4fbe852e6ad22319c85dcd67c37b",
            "ext": {
                "atts": 3,
                "time_zone": "Asia/Shanghai",
                "volume_level": 0.47500002384185791,
                "battery_saver_enabled": 0,
                "muted": 1,
                "orientation": 0,
                "mac": "1121212",
                "ifv": idfv,
            }
        },
        "user": {
            "ext": {

            }
        },
        "at": 1,
        "tmax": 1500,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB7-3",
            "IAB7-5",
            "IAB7-28",
            "IAB7-29",
            "IAB7-30",
            "IAB7-39",
            "IAB7-41",
            "IAB7-42",
            "IAB8-5",
            "IAB8-18",
            "IAB9-9",
            "IAB11",
            "IAB14-2",
            "IAB14-3",
            "IAB14-4",
            "IAB14-8",
            "IAB18-2",
            "IAB23",
            "IAB25-1",
            "IAB25-2",
            "IAB25-3",
            "IAB25-4",
            "IAB25-5",
            "IAB25-6",
            "IAB26"
        ],
        "badv": [
            "domain2.com",
            "domain3.com",
            "domain4.com"
        ],
        "bapp": [
            "618783545"
        ],
        "source": {
            "ext": {
                "schain": {
                    "complete": 1,
                    "nodes": [
                        {
                            "asi": "vungle.com",
                            "sid": "597565c6c5511a1b62000990",
                            "rid": "6110d1c4883cf2ae0b7c8915",
                            "name": "u4e50u4e16u80dcu8c6a",
                            "hp": 1
                        }
                    ],
                    "ver": "1.0"
                },
                "omidpn": "vungle",
                "omidpv": "6.10.0"
            }
        },
        "ext": {
            "schain": {
                "complete": 1,
                "nodes": [
                    {
                        "asi": "vungle.com",
                        "sid": "597565c6c5511a1b62000990",
                        "rid": "6110d1c4883cf2ae0b7c8915",
                        "name": "u4e50u4e16u80dcu8c6a",
                        "hp": 1
                    }
                ],
                "ver": "1.0"
            },
            "moat_sdk": 1
        }
    }
    if banner_format is not None:
        data['imp'][0].update({'banner': data['imp'][0].pop('video')})
        data['imp'][0]['banner'] = banner_format
    if skadn is not None:
        data['imp'][0].get('ext').update(skadn)
    if is_test is not None:
        data.update({'is_test': is_test})
    if regs:
        data.update({'regs': {
            "ext": {

            }
        }})
    if consent is not None:
        data['user'].update({"ext": {"consent": consent}})
    if gdpr is not None:
        data['regs'].update({"ext": {"gdpr": gdpr}})

    if ccpa is not None:
        data['regs']['ext'].update({"us_privacy": ccpa})

    if coppa is not None:
        data['regs'].update({"coppa": coppa})

    return data


def s2s_payload_android(pub_app_id='', placement_id=None, ifa=gen_device_id(), ip=jp_ip, banner_format=None,
                        is_test=None, bid_reqeust_id='6110d1c4883cf2ae0b7c8915',
                        skadn=None, regs=True, gdpr=None, coppa=None, ccpa=None, consent=0, android_id=None,
                        app_set_id=None):
    data = {
        "id": bid_reqeust_id,
        "imp": [
            {
                "id": "1",
                "video": {
                    "mimes": [
                        "video/mp4"
                    ],
                    "minduration": 0,
                    "maxduration": 46,
                    "protocols": [
                        2,
                        5
                    ],
                    "w": 1080,
                    "h": 1920,
                    "linearity": 1,
                    "skip": 1,
                    "minbitrate": 250,
                    "maxbitrate": 15000,
                    "boxingallowed": 1,
                    "playbackmethod": [
                        1,
                        2,
                        3,
                        4
                    ],
                    "delivery": [
                        2,
                        1
                    ],
                    "pos": 7,
                    "api": [
                        7
                    ],
                    "companiontype": [
                        1,
                        2
                    ],
                    "ext": {}
                },
                "displaymanager": "Vungle",
                "displaymanagerver": "6.10.0",
                "instl": 1,
                "tagid": placement_id,
                "bidfloor": 4,
                "bidfloorcur": "USD",
                "secure": 1,
                "ext": {
                    "vungle": {
                        "placement_id": "60c1892f35a07f38d0a3cbb0",
                        "placement_reference_id": placement_id,
                        "rewarded": 0,
                        "templatetypes": [
                            0,
                            1
                        ],
                        "allowed_ad_types": [
                            3,
                            2
                        ],
                        "orientation": 1,
                        "is_flat_cpm_enabled": False,
                        "skadnetwork": {
                            "adnetworkids": []
                        }
                    },
                    "openrtb25x": {
                        "skip": 1
                    },
                    "metric": [
                        {
                            "type": "viewability",
                            "vendor": "moat"
                        }
                    ]
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "ct_and_pub_app2",
            "bundle": "com.stahmoby.chowstahm",
            "storeurl": "https://play.google.com/store/apps/details?id=com.stahmoby.chowstahm",
            "cat": [
                "IAB1",
                "IAB9"
            ],
            "privacypolicy": 1,
            "publisher": {
                "id": "5c18310ab314d945cb99393f",
                "cat": [
                    "IAB1",
                    "IAB9"
                ]
            },
            "keywords": "Everyone",
            "ext": {
                "vungle": {
                    "altid": pub_app_id,
                    "forceViewIncentivized": 1,
                    "wadvid": [
                        "60c4cb1668341600164dbf91"
                    ],
                    "sdk": {
                        "name": "Vungle",
                        "ver": "6.10.0",
                        "plugin": "native"
                    },
                    "bundleid": "1",
                    "accountid": "5c18310ab314d945cb99393f"
                }
            }
        },
        "device": {
            "ua": "CoolPad8190Q_CMCC_TD/1.0 Linux/3.4.5 Android/4.1 Release/03.31.2013 Browser/AppleWebkit534.3",
            "geo": {
                "lat": 54.9735,
                "lon": -1.5673,
                "type": 1,
                "country": "USA",
                "region": "CA",
                "city": "Fremont",
                "zip": "94539"
            },
            "dnt": 0,
            "lmt": 0,
            "ip": ip,
            "devicetype": 1,
            "model": "q10",
            "os": "android",
            "osv": "7.2.0",
            "h": 1920,
            "w": 1080,
            "language": "en",
            "connectiontype": 3,
            "dpidsha1": "f2f596c4db6654f30dd89a5bec0fdc7c22a50137",
            "ifa": ifa,
            "ext": {
                "android_id": android_id,
                "app_set_id": app_set_id,
                "atts": 3,
                "time_zone": "Asia/Shanghai",
                "volume_level": 0.47500002384185791,
                "battery_saver_enabled": 0,
                "muted": 1,
                "orientation": 0,
                "mac": "1121212"
            }
        },
        "user": {
            "ext": {

            }
        },
        "at": 1,
        "tmax": 1500,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB7-3",
            "IAB7-5",
            "IAB7-28",
            "IAB7-29",
            "IAB7-30",
            "IAB7-39",
            "IAB7-41",
            "IAB7-42",
            "IAB8-5",
            "IAB8-18",
            "IAB9-9",
            "IAB11",
            "IAB14-2",
            "IAB14-3",
            "IAB14-4",
            "IAB14-8",
            "IAB18-2",
            "IAB23",
            "IAB25-1",
            "IAB25-2",
            "IAB25-3",
            "IAB25-4",
            "IAB25-5",
            "IAB25-6",
            "IAB26"
        ],
        "source": {
            "ext": {
                "schain": {
                    "complete": 1,
                    "nodes": [
                        {
                            "asi": "vungle.com",
                            "sid": "5c18310ab314d945cb99393f",
                            "rid": "6114c699936c886e984cb000",
                            "name": "Emily Vungle",
                            "hp": 1
                        }
                    ],
                    "ver": "1.0"
                },
                "omidpn": "vungle",
                "omidpv": "6.10.0"
            }
        },
        "ext": {
            "schain": {
                "complete": 1,
                "nodes": [
                    {
                        "asi": "vungle.com",
                        "sid": "5c18310ab314d945cb99393f",
                        "rid": "6114c699936c886e984cb000",
                        "name": "Emily Vungle",
                        "hp": 1
                    }
                ],
                "ver": "1.0"
            },
            "moat_sdk": 1
        }
    }
    if banner_format is not None:
        data['imp'][0].update({'banner': data['imp'][0].pop('video')})
        data['imp'][0]['banner'] = banner_format
    if skadn is not None:
        data['imp'][0].get('ext').update(skadn)
    if is_test is not None:
        data.update({'is_test': is_test})
    if regs:
        data.update({'regs': {
            "ext": {

            }
        }})
    if consent is not None:
        data['user'].update({"ext": {"consent": consent}})
    if gdpr is not None:
        data['regs'].update({"ext": {"gdpr": gdpr}})

    if ccpa is not None:
        data['regs']['ext'].update({"ext": {"us_privacy": ccpa}})

    if coppa is not None:
        data['regs'].update({"coppa": coppa})

    return data


def s2s_payload_sigmob_ios(pub_app_id='', placement_id=None, ifa=gen_device_id(), ip=jp_ip, banner_format=None,
                           consent=0,
                           skadn=None, regs=True, gdpr=None, coppa=None, ccpa=None, is_test=None,
                           bid_reqeust_id='6110d1c4883cf2ae0b7c8915', ifv=None,
                           ):
    data = {
        "id": bid_reqeust_id,
        "imp": [
            {
                "id": "1",
                "video": {
                    "mimes": [
                        "video/mp4"
                    ],
                    "minduration": 0,
                    "maxduration": 46,
                    "protocols": [
                        2,
                        5
                    ],
                    "w": 828,
                    "h": 1792,
                    "linearity": 1,
                    "minbitrate": 250,
                    "maxbitrate": 15000,
                    "boxingallowed": 1,
                    "playbackmethod": [
                        1,
                        2,
                        3,
                        4
                    ],
                    "delivery": [
                        2,
                        1
                    ],
                    "pos": 7,
                    "api": [
                        7
                    ],
                    "companiontype": [
                        1,
                        2
                    ],
                    "ext": {
                        "skip": 0,
                        "videotype": "rewarded",
                        "rewarded": 1
                    }
                },
                "displaymanager": "Vungle",
                "displaymanagerver": "6.10.3",
                "instl": 1,
                "tagid": placement_id,
                "bidfloor": 1.001,
                "bidfloorcur": "USD",
                "secure": 1,
                "ext": {

                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "u5f69u7ea2u7adeu731c1",
            "bundle": "1131184101",
            "storeurl": "https://itunes.apple.com/cn/app/id1131184101",
            "cat": [
                "IAB1",
                "IAB9"
            ],
            "ver": "1.0.9",
            "privacypolicy": 1,
            "publisher": {
                "id": "597565c6c5511a1b62000990",
                "cat": [
                    "IAB1",
                    "IAB9"
                ]
            },
            "keywords": "app,account,managed"
        },
        "device": {
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "geo": {
                "lat": 35.6887,
                "lon": 139.745,
                "type": 2,
                "ipservice": 3,
                "country": "JPN",
                "region": "13",
                "city": "Tokyo",
                "zip": "102-0082"
            },
            "dnt": 0,
            "lmt": 0,
            "ip": ip,
            "devicetype": 4,
            "make": "Apple",
            "model": "iPhone",
            "os": "iOS",
            "osv": "13",
            "hwv": "XR",
            "h": 1792,
            "w": 828,
            "language": "en",
            "carrier": "T-Mobile",
            "connectiontype": 2,
            "ifa": ifa,
            "dpidsha1": "cf6bb0b5283b4fbe852e6ad22319c85dcd67c37b",
            "ext": {
                "atts": 3,
                "time_zone": "Asia/Shanghai",
                "volume_level": 0.47500002384185791,
                "battery_saver_enabled": 0,
                "muted": 1,
                "orientation": 0,
                "mac": "1121212",
                "ifv": ifv,
            }
        },
        "user": {
            "ext": {

            }
        },
        "at": 1,
        "tmax": 1500,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB7-3",
            "IAB7-5",
            "IAB7-28",
            "IAB7-29",
            "IAB7-30",
            "IAB7-39",
            "IAB7-41",
            "IAB7-42",
            "IAB8-5",
            "IAB8-18",
            "IAB9-9",
            "IAB11",
            "IAB14-2",
            "IAB14-3",
            "IAB14-4",
            "IAB14-8",
            "IAB18-2",
            "IAB23",
            "IAB25-1",
            "IAB25-2",
            "IAB25-3",
            "IAB25-4",
            "IAB25-5",
            "IAB25-6",
            "IAB26"
        ],
        "badv": [
            "domain2.com",
            "domain3.com",
            "domain4.com"
        ],
        "bapp": [
            "618783545"
        ],
        "source": {
            "ext": {
                "schain": {
                    "complete": 1,
                    "nodes": [
                        {
                            "asi": "vungle.com",
                            "sid": "597565c6c5511a1b62000990",
                            "rid": "6110d1c4883cf2ae0b7c8915",
                            "hp": 1
                        }
                    ],
                    "ver": "1.0"
                },
                "omidpn": "vungle",
                "omidpv": "6.10.0"
            }
        },
        "ext": {
            "moat_sdk": 1
        }

    }
    if banner_format is not None:
        data['imp'][0].update({'banner': data['imp'][0].pop('video')})
        data['imp'][0]['banner'] = banner_format
    if skadn is not None:
        data['imp'][0].get('ext').update(skadn)
    if is_test is not None:
        data.update({'is_test': is_test})
    if regs:
        data.update({'regs': {
            "ext": {

            }
        }})
    if consent is not None:
        data['user'].update({"ext": {"consent": consent}})
    if gdpr is not None:
        data['regs'].update({"ext": {"gdpr": gdpr}})

    if ccpa is not None:
        data['regs']['ext'].update({"ext": {"us_privacy": ccpa}})

    if coppa is not None:
        data['regs'].update({"coppa": coppa})

    return data


def s2s_payload_sigmob_android(pub_app_id='', placement_id=None, ifa=gen_device_id(), ip=jp_ip, banner_format=None,
                               skadn=None, is_test=None, consent=0, regs=True, gdpr=None, coppa=None, ccpa=None,
                               bid_reqeust_id='6110d1c4883cf2ae0b7c8915', android_id=None, app_set_id=None):
    data = {
        "id": bid_reqeust_id,
        "imp": [
            {
                "id": "1",
                "video": {
                    "mimes": [
                        "video/mp4"
                    ],
                    "minduration": 0,
                    "maxduration": 46,
                    "protocols": [
                        2,
                        5
                    ],
                    "w": 1080,
                    "h": 1920,
                    "linearity": 1,
                    "skip": 1,
                    "minbitrate": 250,
                    "maxbitrate": 15000,
                    "boxingallowed": 1,
                    "playbackmethod": [
                        1,
                        2,
                        3,
                        4
                    ],
                    "delivery": [
                        2,
                        1
                    ],
                    "pos": 7,
                    "api": [
                        7
                    ],
                    "companiontype": [
                        1,
                        2
                    ],
                    "ext": {}
                },
                "displaymanager": "Vungle",
                "displaymanagerver": "6.10.0",
                "instl": 1,
                "tagid": placement_id,
                "bidfloor": 4,
                "bidfloorcur": "USD",
                "secure": 1,
                "ext": {
                    "reward": 0
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "ct_and_pub_app2",
            "bundle": "com.stahmoby.chowstahm",
            "storeurl": "https://play.google.com/store/apps/details?id=com.stahmoby.chowstahm",
            "cat": [
                "IAB1",
                "IAB9"
            ],
            "privacypolicy": 1,
            "publisher": {
                "id": "5c18310ab314d945cb99393f",
                "cat": [
                    "IAB1",
                    "IAB9"
                ]
            },
            "keywords": "Everyone"
        },
        "device": {
            "ua": "CoolPad8190Q_CMCC_TD/1.0 Linux/3.4.5 Android/4.1 Release/03.31.2013 Browser/AppleWebkit534.3",
            "geo": {
                "lat": 54.9735,
                "lon": -1.5673,
                "type": 1,
                "country": "USA",
                "region": "CA",
                "city": "Fremont",
                "zip": "94539"
            },
            "dnt": 0,
            "lmt": 0,
            "ip": ip,
            "devicetype": 1,
            "model": "q10",
            "os": "android",
            "osv": "7.2.0",
            "h": 1920,
            "w": 1080,
            "language": "en",
            "connectiontype": 3,
            "dpidsha1": "f2f596c4db6654f30dd89a5bec0fdc7c22a50137",
            "ifa": ifa,
            "ext": {
                "android_id": android_id,
                "app_set_id": app_set_id,
                "atts": 3,
                "time_zone": "Asia/Shanghai",
                "volume_level": 0.47500002384185791,
                "battery_saver_enabled": 0,
                "muted": 1,
                "orientation": 0,
                "mac": "1121212"
            }
        },
        "user": {
            "ext": {

            }
        },
        "at": 1,
        "tmax": 1500,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB7-3",
            "IAB7-5",
            "IAB7-28",
            "IAB7-29",
            "IAB7-30",
            "IAB7-39",
            "IAB7-41",
            "IAB7-42",
            "IAB8-5",
            "IAB8-18",
            "IAB9-9",
            "IAB11",
            "IAB14-2",
            "IAB14-3",
            "IAB14-4",
            "IAB14-8",
            "IAB18-2",
            "IAB23",
            "IAB25-1",
            "IAB25-2",
            "IAB25-3",
            "IAB25-4",
            "IAB25-5",
            "IAB25-6",
            "IAB26"
        ],
        "source": {
            "ext": {
                "schain": {
                    "complete": 1,
                    "nodes": [
                        {
                            "asi": "vungle.com",
                            "sid": "5c18310ab314d945cb99393f",
                            "rid": "6114c699936c886e984cb000",
                            "name": "Emily Vungle",
                            "hp": 1
                        }
                    ],
                    "ver": "1.0"
                },
                "omidpn": "vungle",
                "omidpv": "6.10.0"
            }
        },
        "ext": {
            "moat_sdk": 1
        }
    }
    if banner_format is not None:
        data['imp'][0].update({'banner': data['imp'][0].pop('video')})
        data['imp'][0]['banner'] = banner_format
    if skadn is not None:
        data['imp'][0].get('ext').update(skadn)
    if is_test is not None:
        data.update({'is_test': is_test})
    if regs:
        data.update({'regs': {
            "ext": {

            }
        }})
    if consent is not None:
        data['user'].update({"ext": {"consent": consent}})
    if gdpr is not None:
        data['regs'].update({"ext": {"gdpr": gdpr}})

    if ccpa is not None:
        data['regs']['ext'].update({"ext": {"us_privacy": ccpa}})

    if coppa is not None:
        data['regs'].update({"coppa": coppa})
    return data


def s2s_payload_sigmob_amazon(pub_app_id='', placement_id=None, ifa=gen_device_id(), ip=jp_ip, banner_format=None,
                              skadn=None, is_test=None, consent=0, regs=True, gdpr=None, coppa=None, ccpa=None,
                              bid_reqeust_id='6110d1c4883cf2ae0b7c8915', app_set_id=None):
    data = {
        "id": bid_reqeust_id,
        "imp": [
            {
                "id": "1",
                "video": {
                    "mimes": [
                        "video/mp4"
                    ],
                    "minduration": 0,
                    "maxduration": 46,
                    "protocols": [
                        2,
                        5
                    ],
                    "w": 1080,
                    "h": 1920,
                    "linearity": 1,
                    "skip": 1,
                    "minbitrate": 250,
                    "maxbitrate": 15000,
                    "boxingallowed": 1,
                    "playbackmethod": [
                        1,
                        2,
                        3,
                        4
                    ],
                    "delivery": [
                        2,
                        1
                    ],
                    "pos": 7,
                    "api": [
                        7
                    ],
                    "companiontype": [
                        1,
                        2
                    ],
                    "ext": {}
                },
                "displaymanager": "Vungle",
                "displaymanagerver": "6.10.0",
                "instl": 1,
                "tagid": placement_id,
                "bidfloor": 4,
                "bidfloorcur": "USD",
                "secure": 1,
                "ext": {
                    "reward": 0
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "365: My Daily Hidden",
            "bundle": "com.stahmoby.chowstahm",
            "storeurl": "https://play.google.com/store/apps/details?id=com.stahmoby.chowstahm",
            "cat": [
                "IAB1",
                "IAB9"
            ],
            "privacypolicy": 1,
            "publisher": {
                "id": "5c18310ab314d945cb99393f",
                "cat": [
                    "IAB1",
                    "IAB9"
                ]
            },
            "keywords": "Everyone"
        },
        "device": {
            "ua": "Mozilla/5.0 (Linux; Android 9; SM-G973U1 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/73.0.3683.90 Mobile Safari/537.36",
            "geo": {
                "lat": -33.8601,
                "lon": 151.2101,
                "type": 2,
                "ipservice": 3,
                "country": "AUS",
                "region": "NSW",
                "city": "Sydney",
                "zip": "2000"
            },
            "dnt": 1,
            "lmt": 1,
            "ip": ip,
            "devicetype": 4,
            "make": "samsung",
            "model": "SM-G973U1",
            "hwv": "Galaxy S10",
            "os": "amazon",
            "osv": "10.0",
            "devicetype": 4,
            "h": 1920,
            "w": 1080,
            "language": "en",
            "connectiontype": 3,
            "dpidsha1": "f2f596c4db6654f30dd89a5bec0fdc7c22a50137",
            "ifa": ifa,
            "ext": {
                "app_set_id": app_set_id,
                "atts": 3,
                "time_zone": "Asia/Shanghai",
                "volume_level": 0.4,
                "battery_saver_enabled": 0,
                "muted": 1,
                "orientation": 0,
                "mac": "1121212"
            }
        },
        "user": {
            "ext": {

            }
        },
        "at": 1,
        "tmax": 1500,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB7-3",
            "IAB7-5",
            "IAB7-28",
            "IAB7-29",
            "IAB7-30",
            "IAB7-39",
            "IAB7-41",
            "IAB7-42",
            "IAB8-5",
            "IAB8-18",
            "IAB9-9",
            "IAB11",
            "IAB14-2",
            "IAB14-3",
            "IAB14-4",
            "IAB14-8",
            "IAB18-2",
            "IAB23",
            "IAB25-1",
            "IAB25-2",
            "IAB25-3",
            "IAB25-4",
            "IAB25-5",
            "IAB25-6",
            "IAB26"
        ],
        "source": {
            "ext": {
                "schain": {
                    "complete": 1,
                    "nodes": [
                        {
                            "asi": "vungle.com",
                            "sid": "5c18310ab314d945cb99393f",
                            "rid": "6114c699936c886e984cb000",
                            "name": "Emily Vungle",
                            "hp": 1
                        }
                    ],
                    "ver": "1.0"
                },
                "omidpn": "vungle",
                "omidpv": "6.10.0"
            }
        },
        "ext": {
            "moat_sdk": 1
        }
    }
    if banner_format is not None:
        data['imp'][0].update({'banner': data['imp'][0].pop('video')})
        data['imp'][0]['banner'] = banner_format
    if skadn is not None:
        data['imp'][0].get('ext').update(skadn)
    if is_test is not None:
        data.update({'is_test': is_test})
    if regs:
        data.update({'regs': {
            "ext": {

            }
        }})
    if consent is not None:
        data['user'].update({"ext": {"consent": consent}})
    if gdpr is not None:
        data['regs'].update({"ext": {"gdpr": gdpr}})

    if ccpa is not None:
        data['regs']['ext'].update({"ext": {"us_privacy": ccpa}})

    if coppa is not None:
        data['regs'].update({"coppa": coppa})
    return data


def s2s_payload_sigmob_windows(pub_app_id='', placement_id=None, ifa=gen_device_id(), ip=jp_ip, banner_format=None,
                               skadn=None, is_test=None, consent=0, regs=True, gdpr=None, coppa=None, ccpa=None,
                               bid_reqeust_id='6110d1c4883cf2ae0b7c8915', ashwid=None):
    data = {
        "id": bid_reqeust_id,
        "imp": [
            {
                "id": "1",
                "video": {
                    "mimes": [
                        "video/mp4"
                    ],
                    "minduration": 0,
                    "maxduration": 46,
                    "protocols": [
                        2,
                        5
                    ],
                    "w": 1080,
                    "h": 1920,
                    "linearity": 1,
                    "skip": 1,
                    "minbitrate": 250,
                    "maxbitrate": 15000,
                    "boxingallowed": 1,
                    "playbackmethod": [
                        1,
                        2,
                        3,
                        4
                    ],
                    "delivery": [
                        2,
                        1
                    ],
                    "pos": 7,
                    "api": [
                        7
                    ],
                    "companiontype": [
                        1,
                        2
                    ],
                    "ext": {}
                },
                "displaymanager": "Vungle",
                "displaymanagerver": "6.10.0",
                "instl": 1,
                "tagid": placement_id,
                "bidfloor": 4,
                "bidfloorcur": "USD",
                "secure": 1,
                "ext": {
                    "reward": 0
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "365: My Daily Hidden",
            "bundle": "com.stahmoby.chowstahm",
            "storeurl": "https://play.google.com/store/apps/details?id=com.stahmoby.chowstahm",
            "cat": [
                "IAB1",
                "IAB9"
            ],
            "privacypolicy": 1,
            "publisher": {
                "id": "5c18310ab314d945cb99393f",
                "cat": [
                    "IAB1",
                    "IAB9"
                ]
            },
            "keywords": "Everyone"
        },
        "device": {
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; WebView/3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362",
            "geo": {
                "lat": -33.8601,
                "lon": 151.2101,
                "type": 2,
                "ipservice": 3,
                "country": "AUS",
                "region": "NSW",
                "city": "Sydney",
                "zip": "2000"
            },
            "dnt": 1,
            "lmt": 1,
            "ip": ip,
            "devicetype": 4,
            "osv": "10.0.18362.592",
            "os": "windows",
            "h": 1920,
            "w": 1080,
            "language": "en",
            "connectiontype": 3,
            "dpidsha1": "f2f596c4db6654f30dd89a5bec0fdc7c22a50137",
            "ifa": ifa,
            "ext": {
                "ashwid": ashwid,
                "atts": 3,
                "time_zone": "Asia/Shanghai",
                "volume_level": 0.4,
                "battery_saver_enabled": 0,
                "muted": 1,
                "orientation": 0,
                "mac": "1121212"
            }
        },
        "user": {
            "ext": {

            }
        },
        "at": 1,
        "tmax": 1500,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB7-3",
            "IAB7-5",
            "IAB7-28",
            "IAB7-29",
            "IAB7-30",
            "IAB7-39",
            "IAB7-41",
            "IAB7-42",
            "IAB8-5",
            "IAB8-18",
            "IAB9-9",
            "IAB11",
            "IAB14-2",
            "IAB14-3",
            "IAB14-4",
            "IAB14-8",
            "IAB18-2",
            "IAB23",
            "IAB25-1",
            "IAB25-2",
            "IAB25-3",
            "IAB25-4",
            "IAB25-5",
            "IAB25-6",
            "IAB26"
        ],
        "source": {
            "ext": {
                "schain": {
                    "complete": 1,
                    "nodes": [
                        {
                            "asi": "vungle.com",
                            "sid": "5c18310ab314d945cb99393f",
                            "rid": "6114c699936c886e984cb000",
                            "name": "Emily Vungle",
                            "hp": 1
                        }
                    ],
                    "ver": "1.0"
                },
                "omidpn": "vungle",
                "omidpv": "6.10.0"
            }
        },
        "ext": {
            "moat_sdk": 1
        }
    }
    if banner_format is not None:
        data['imp'][0].update({'banner': data['imp'][0].pop('video')})
        data['imp'][0]['banner'] = banner_format
    if skadn is not None:
        data['imp'][0].get('ext').update(skadn)
    if is_test is not None:
        data.update({'is_test': is_test})
    if regs:
        data.update({'regs': {
            "ext": {

            }
        }})
    if consent is not None:
        data['user'].update({"ext": {"consent": consent}})
    if gdpr is not None:
        data['regs'].update({"ext": {"gdpr": gdpr}})

    if ccpa is not None:
        data['regs']['ext'].update({"ext": {"us_privacy": ccpa}})

    if coppa is not None:
        data['regs'].update({"coppa": coppa})
    return data


def s2s_payload_windows(pub_app_id='', placement_id=None, ifa=gen_device_id(), ip=jp_ip, banner_format=None,
                        skadn=None, is_test=None, consent=0, regs=True, gdpr=None, coppa=None, ccpa=None,
                        bid_reqeust_id='6110d1c4883cf2ae0b7c8915', ashwid=None):
    data = {
        "id": bid_reqeust_id,
        "imp": [
            {
                "id": "1",
                "video": {
                    "mimes": [
                        "video/mp4"
                    ],
                    "minduration": 0,
                    "maxduration": 46,
                    "protocols": [
                        2,
                        5
                    ],
                    "w": 1080,
                    "h": 1920,
                    "linearity": 1,
                    "skip": 1,
                    "minbitrate": 250,
                    "maxbitrate": 15000,
                    "boxingallowed": 1,
                    "playbackmethod": [
                        1,
                        2,
                        3,
                        4
                    ],
                    "delivery": [
                        2,
                        1
                    ],
                    "pos": 7,
                    "api": [
                        7
                    ],
                    "companiontype": [
                        1,
                        2
                    ],
                    "ext": {}
                },
                "displaymanager": "Vungle",
                "displaymanagerver": "6.10.0",
                "instl": 1,
                "tagid": placement_id,
                "bidfloor": 4,
                "bidfloorcur": "USD",
                "secure": 1,
                "ext": {
                    "reward": 0
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "365: My Daily Hidden",
            "bundle": "com.stahmoby.chowstahm",
            "storeurl": "https://play.google.com/store/apps/details?id=com.stahmoby.chowstahm",
            "cat": [
                "IAB1",
                "IAB9"
            ],
            "privacypolicy": 1,
            "publisher": {
                "id": "5c18310ab314d945cb99393f",
                "cat": [
                    "IAB1",
                    "IAB9"
                ]
            },
            "keywords": "Everyone"
        },
        "device": {
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; WebView/3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362",
            "geo": {
                "lat": -33.8601,
                "lon": 151.2101,
                "type": 2,
                "ipservice": 3,
                "country": "AUS",
                "region": "NSW",
                "city": "Sydney",
                "zip": "2000"
            },
            "dnt": 1,
            "lmt": 1,
            "ip": ip,
            "devicetype": 4,
            "osv": "10.0.18362.592",
            "os": "windows",
            "h": 1920,
            "w": 1080,
            "language": "en",
            "connectiontype": 3,
            "dpidsha1": "f2f596c4db6654f30dd89a5bec0fdc7c22a50137",
            "ifa": ifa,
            "ext": {
                "ashwid": ashwid,
                "atts": 3,
                "time_zone": "Asia/Shanghai",
                "volume_level": 0.4,
                "battery_saver_enabled": 0,
                "muted": 1,
                "orientation": 0,
                "mac": "1121212"
            }
        },
        "user": {
            "ext": {

            }
        },
        "at": 1,
        "tmax": 1500,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB7-3",
            "IAB7-5",
            "IAB7-28",
            "IAB7-29",
            "IAB7-30",
            "IAB7-39",
            "IAB7-41",
            "IAB7-42",
            "IAB8-5",
            "IAB8-18",
            "IAB9-9",
            "IAB11",
            "IAB14-2",
            "IAB14-3",
            "IAB14-4",
            "IAB14-8",
            "IAB18-2",
            "IAB23",
            "IAB25-1",
            "IAB25-2",
            "IAB25-3",
            "IAB25-4",
            "IAB25-5",
            "IAB25-6",
            "IAB26"
        ],
        "source": {
            "ext": {
                "schain": {
                    "complete": 1,
                    "nodes": [
                        {
                            "asi": "vungle.com",
                            "sid": "5c18310ab314d945cb99393f",
                            "rid": "6114c699936c886e984cb000",
                            "name": "Emily Vungle",
                            "hp": 1
                        }
                    ],
                    "ver": "1.0"
                },
                "omidpn": "vungle",
                "omidpv": "6.10.0"
            }
        },
        "ext": {
            "moat_sdk": 1
        }
    }
    if banner_format is not None:
        data['imp'][0].update({'banner': data['imp'][0].pop('video')})
        data['imp'][0]['banner'] = banner_format
    if skadn is not None:
        data['imp'][0].get('ext').update(skadn)
    if is_test is not None:
        data.update({'is_test': is_test})
    if regs:
        data.update({'regs': {
            "ext": {

            }
        }})
    if consent is not None:
        data['user'].update({"ext": {"consent": consent}})
    if gdpr is not None:
        data['regs'].update({"ext": {"gdpr": gdpr}})

    if ccpa is not None:
        data['regs']['ext'].update({"ext": {"us_privacy": ccpa}})

    if coppa is not None:
        data['regs'].update({"coppa": coppa})
    return data


def hbp_new_lurl(bid_request_id='bid_request_id', bid_id='bid_id', latency=0.139, bid_price=0.51,
                 loss_reason=1, loss_reason_value='bidder,network,line item', loss_reason_des='outbid'):
    data = {
        "latency": latency,
        "seatbid": [{
            "bid": [{
                "reason": {
                    "description": loss_reason_des,
                    "value": loss_reason_value,
                    "id": loss_reason
                },
                "impid": "1",
                "price": bid_price,
                "adid": "3141592",
                "id": bid_id
            }],
            "seat": "seat1"
        }],
        "bidfloor": 0.1,
        "http_status": 200,
        "bidid": bid_request_id,
        "id": bid_request_id
    }

    return data


# general device model
def device_ios(ifa=gen_device_id(), make='Apple', model='iPhone11,8', device_ip=ca_us_ip, idfv='', lmt=0, device_ext=None,
               geo=None, ua=None, atts=0):
    data = {
        "connectiontype": 1,
        "dnt": 0,
        "h": 1136,
        "ifa": ifa,
        "js": 1,
        "make": make,
        "model": model,
        "language": "en",
        "os": "ios",
        "osv": "13",
        "pxratio": 2.0,
        "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
              "Mobile/15E148",
        "w": 640,
        "lmt": lmt,
        "ext": {
            "volume": 0.5625,
            "battery_state": "unplugged",
            "idfa": "",
            "vduid": "",
            "battery_level": 0.54000002145767231,
            "locale": "en_US",
            "connection_type": '',
            "language": "en-US",
            "storage_bytes_available": 9223372036854775807,
            "ifv": idfv,
            "battery_saver_enabled": 1,
            "time_zone": "America/Los_Angeles",
            "sound_enabled": 1,
            "atts": atts,
        },
        "ip": device_ip,
        "carrier": "china mobile",
    }

    geo_obj = {
        "lat": 54.9735,
        "lon": -1.5673,
        "type": 1,
        "country": "USA",
        "region": "CA",
        "city": "Fremont",
        "zip": "94539"
    }
    if ua is not None:
        data.update({"ua": ua})
    if geo is not None:
        data.update(geo=geo_obj)
    device_ext_obj = {}
    if device_ext is not None:
        device_ext_obj.update(ext=device_ext)
        data.update(device_ext_obj)

    return data


def device_android(ifa=gen_device_id(), app_set_id='', android_id='', device_ip=ca_us_ip, device_ext=None, geo=None,
                   ua=None):
    data = {
        "connectiontype": 2,
        "make": "android",
        "model": "generic",
        "os": "android",
        "osv": "11",
        "devicetype": 4,
        "dnt": 0,
        "h": 1136,
        "lmt": 1,
        "language": "en",
        "pxratio": 3,
        "ua": "Mozilla/5.0 (Linux; Android 11; sdk_gphone_x86_arm Build/RPB2.200611.012; wv) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36 "
              "(Mobile; afma-sdk-a-v201817022.201817022.0)",
        "w": 640,
        "ifa": ifa,
        "ext": {
            "gaid": "",
            "android_id": android_id,
            "app_set_id": app_set_id,
            "battery_level": 0.93,
            "battery_state": "BATTERY_PLUGGED_USB",
            "battery_saver_enabled": 0,
            "connection_type": "WIFI",
            "connection_type_detail": "WIFI",
            "data_saver_status": "NOT_APPLICABLE",
            "network_metered": 0,
            "locale": "en_US",
            "language": "en",
            "time_zone": "Asia/Seoul",
            "volume_level": 0.0,
            "sound_enabled": 0,
            "sd_card_available": 1,
            "os_name": "samsung/beyond1qlteue/beyond1q:9/PPR1.180610.011/G973U1UEU1ASBA:user/release-keys",
            "storage_bytes_available": 109420306432,
            "vduid": "",
            "os_api_level": 28,
            "is_tv": False,
            "is_sideload_enabled": False
        },
        "ip": device_ip,
    }

    geo_obj = {
        "lat": 54.9735,
        "lon": -1.5673,
        "type": 1,
        "country": "USA",
        "region": "CA",
        "city": "Fremont",
        "zip": "94539"
    }
    if ua is not None:
        data.update({"ua": ua})
    if geo is not None:
        data.update(geo=geo_obj)
    device_ext_obj = {}
    if device_ext is not None:
        device_ext_obj.update(ext=device_ext)
        data.update(device_ext_obj)

    return data


def device_windows(ifa=gen_device_id(), device_ip=ca_us_ip, device_ext=None, geo=None, ua=None):
    data = {
        "osv": "10.0.18362.592",
        "os": "windows",
        "w": 1536,
        "h": 2048,
        "ua": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; WebView/3.0) '
              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.353'
              '8.102 Safari/537.36 Edge/18.18362',
        "model": 'GL752VW',
        "make": 'ASUSTeK COMPUTER INC.',
        "ifa": ifa,
        "lmt": 0,
        "ip": device_ip,
    }

    geo_obj = {
        "lat": 54.9735,
        "lon": -1.5673,
        "type": 1,
        "country": "USA",
        "region": "CA",
        "city": "Fremont",
        "zip": "94539"
    }
    if ua is not None:
        data.update({"ua": ua})
    if geo is not None:
        data.update(geo=geo_obj)
    device_ext_obj = {}
    if device_ext is not None:
        device_ext_obj.update(ext=device_ext)
        data.update(device_ext_obj)

    return data


def device_amazon(ifa=gen_device_id(), device_ip=ca_us_ip, device_ext=None, geo=None, ua=None):
    data = {
        "connectiontype": 2,
        "make": "android",
        "model": "generic",
        "os": "Amazon",
        "osv": "10.0",
        "devicetype": 4,
        "dnt": 0,
        "h": 1136,
        "lmt": 1,
        "language": "en",
        "pxratio": 3,
        "ua": "Mozilla/5.0 (Linux; Android 9; SM-G973U1 Build/PPR1.180610.011; wv) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Version/4.0 Chrome/73.0.3683.90 Mobile Safari/537.36",
        "w": 640,
        "ifa": ifa,
        "geo": {
            "lat": -33.8601,
            "lon": 151.2101,
            "type": 2,
            "ipservice": 3,
            "country": "AUS",
            "region": "NSW",
            "city": "Sydney",
            "zip": "2000"
        },
        "ip": device_ip
    }

    geo_obj = {
        "lat": 54.9735,
        "lon": -1.5673,
        "type": 1,
        "country": "USA",
        "region": "CA",
        "city": "Fremont",
        "zip": "94539"
    }
    if ua is not None:
        data.update({"ua": ua})
    if geo is not None:
        data.update(geo=geo_obj)
    device_ext_obj = {}
    if device_ext is not None:
        device_ext_obj.update(ext=device_ext)
        data.update(device_ext_obj)

    return data


def generate_device_obj(platform, ifa=gen_device_id(), make='Apple', model='iPhone11,8', device_ip=ca_us_ip, idfv='',
                        lmt=0, device_ext=None, geo=None, ua=None, app_set_id='', android_id='', atts=0):
    switcher = {
        "ios": device_ios(ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv, lmt=lmt,
                          device_ext=device_ext, geo=geo, ua=ua, atts=atts),
        "android": device_android(ifa=ifa, app_set_id=app_set_id, android_id=android_id,
                                  device_ip=device_ip, device_ext=device_ext, geo=geo, ua=ua),
        "amazon": device_amazon(ifa=ifa, device_ip=device_ip, device_ext=device_ext, geo=geo, ua=ua),
        "windows": device_windows(ifa=ifa, device_ip=device_ip, device_ext=device_ext, geo=geo, ua=ua)
    }

    return switcher.get(platform)


def generate_banner_obj(banner_flag=True):
    banner = {
        "api": [
            3,
            5
        ],
        "battr": [
            3,
            8,
            9,
            10,
            14
        ],
        "btype": [
            4
        ],
        "h": 50,
        "pos": 1,
        "w": 320
    }
    if banner_flag:
        return banner
    else:
        return None


def generate_video_obj(video_flag=True):
    video = {
        "mimes": [
            "video/mp4"
        ],
        "minduration": 0,
        "maxduration": 1234,
        "w": 1536,
        "h": 2048,
        "linearity": 1,
        "pos": 7,
        "battr": [
            1,
            2,
            5,
            8,
            9,
            14,
            16,
            17
        ],
        "ext": {
            "videotype": "rewarded"
        }
    }

    if video_flag:
        return video
    else:
        return None


def hbp_max(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
            is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
            make='Apple', model='iPhone11,8', skadnetids=None, imp=1, platform='ios', app_set_id='', android_id='',
            atts=0, video_flag=True, banner_flag=True):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104b",
                "video": generate_video_obj(video_flag),
                "banner": generate_banner_obj(banner_flag),
                "displaymanager": "Vungle",
                "displaymanagerver": "5.0.0",
                "tagid": placement_id,
                "placement": 5,
                "secure": 1,
                "instl": 1,
                "bidfloor": 1,
                "ext": {
                    "brsrclk": 1,
                    "dlp": 1,
                    "metric": [
                        {
                            "type": "viewability",
                            "vendor": "ias"
                        },
                        {
                            "type": "viewability",
                            "vendor": "moat"
                        }
                    ],
                    "vungle": {
                        "bid_token": bid_token
                    },
                    "skadn": {
                        "version": "2.0",
                        "versions": [
                            "2.0"
                        ],
                        "sourceapp": "1131184101",
                        "skadnetids": skadnetids
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "App Name",
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa",
            "cat": [
                "IAB9-30"
            ],
            "publisher": {
                "id": "345678",
                "ext": {
                    "installed_sdk": {
                        "id": "vacto_test",
                        "sdk_version": {
                            "major": 6,
                            "minor": 0,
                            "micro": 3
                        },
                        "adapter_version": {
                            "major": 1,
                            "minor": 0,
                            "micro": 0
                        }
                    }
                }
            }
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua, atts=atts),
        "at": 1,
        "tmax": 10000,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB8-5",
            "IAB8-18"
        ],
        "badv": [

        ],
        "regs": {
            "coppa": 1
        },
        "user": {
            "data": [{
                "id": "1",
                "name": "Publisher Passed"
            }],
            "ext": {
                "test": "emily"
            }
        },
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})
    if imp is None:
        data.get('imp')[0].update({"banner": None})
        data.get('imp')[0].update({"video": None})

    return data


def hbp_adtiming(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
                 is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
                 make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104",
                "tagid": placement_id,
                "banner": {
                    "w": 320,
                    "h": 50
                },
                "native": {
                    "w": 1024,
                    "h": 768
                },
                "video": {
                    "w": 1080,
                    "h": 1920
                },
                "ext": {
                    "vungle": {
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa"
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "regs": {
            "coppa": 1,
            "ext": {
                "gdpr": 1,
                "ccpa": 1
            }
        },
        "at": 1,
        "tmax": 1000,
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


def hbp_ironsource(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(),
                   bid_token='',
                   is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
                   make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104",
                "tagid": placement_id,
                "banner": {
                    "w": 320,
                    "h": 50
                },
                "native": {
                    "w": 1024,
                    "h": 768
                },
                "video": {
                    "w": 1080,
                    "h": 1920
                },
                "ext": {
                    "vungle": {
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa"
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "regs": {
            "coppa": 1,
            "ext": {
                "gdpr": 1,
                "ccpa": 1
            }
        },
        "at": 1,
        "tmax": 1000,
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


def hbp_charboost(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
                  is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
                  make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104",
                "tagid": placement_id,
                "banner": {
                    "w": 320,
                    "h": 50
                },
                "native": {
                    "w": 1024,
                    "h": 768
                },
                "video": {
                    "w": 1080,
                    "h": 1920
                },
                "ext": {
                    "vungle": {
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa"
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "regs": {
            "coppa": 1,
            "ext": {
                "gdpr": 1,
                "ccpa": 1
            }
        },
        "at": 1,
        "tmax": 1000,
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


# def get_random_event_id(platform = 'ios'):
#     random_event_id = generate_unique_objId()
#     if platform == 'ios':
#         app_id = test_app_id_ios.replace("5fe4586f775977000126f603", str(random_event_id))
#     elif platform == 'android':
#         app_id = test_app_id_android.replace("5fe4586f775977000126f603", str(random_event_id))
#     return app_id


def report_ad_v5_ios(pub_app_id=None, placement_id=None, gdpr=None, ifa=gen_device_id(), header_bidding=False,
                     ccpa=None, os_version='13', app_id=gen_test_app_id(), ad_token=test_ad_token_ios,
                     campaign=test_campaign_ios, viewed=True, completed_viewed=False, idfv='', download=1,
                     deeplink='deeplinkSuccess', skoAutoshow=None, video_len=37986, play_remote_assets=None,
                     config_extension=None):
    video_len = video_len
    if completed_viewed is True:
        viewed_len = video_len * 0.8 + 1
    else:
        viewed_len = 1

    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.ios-sdk-app.qa",
            "ver": "4310d55"
        },
        "system": {
            "cache": []
        },
        "device": {
            "make": "Apple",
            "os": "ios",
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)"
                  " Mobile/15E148",
            "h": 2688,
            "model": "iPhone12,5",
            "osv": os_version,
            "ext": {
                "vungle": {
                    "ios": {
                        "battery_state": "unplugged",
                        "idfa": "",
                        "vduid": "",
                        "battery_level": 0.86000001430511475,
                        "locale": "en_CN",
                        "volume_level": 0.47500002384185791,
                        "connection_type_detail": "lte",
                        "language": "zh-Hans-CN",
                        "storage_bytes_available": 63913914368,
                        "idfv": idfv,
                        "battery_saver_enabled": 0,
                        "connection_type": "wifi",
                        "time_zone": "Asia/Shanghai"
                    }
                }
            },
            "carrier": "中国联通",
            "ifa": ifa,
            "w": 1242,
            "lmt": 0
        },
        "ext": {},
        "request": {
            "app_id": app_id,
            "ordinal_view": 1,
            "clickedThrough": ["videoLength", "videoViewed", "download", "mraidOpen", "mraidClose"],
            "incentivized": 1,
            "templateId": "5d7936a80ed7e506be620bf0",
            "adStartTime": 1595826614000,
            "play_remote_assets": play_remote_assets,
            "plays": [{
                "userActions": [{
                    "value": video_len,
                    "action": "videoLength",
                    "timestamp_millis": 1595826615000
                }, {
                    "value": viewed_len,
                    "action": "videoViewed",
                    "timestamp_millis": 1595826615000
                }, {
                    "value": download,
                    "action": "download",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidOpen",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidClose",
                    "timestamp_millis": 1595826662000
                }, {
                    "action": deeplink,
                    "timestamp_millis": 1503075311000
                }],
                "startTime": 1595826614000
            }],
            "ad_token": ad_token,
            "adDuration": 46000,
            "ttDownload": 4000,
            "init_timestamp": 1595826498000,
            "adType": "vungle_mraid",
            "campaign": campaign,
            "asset_download_duration": 1000,
            "placement_reference_id": placement_id,
            "ad_size": "unknown",
            "header_bidding": header_bidding,
            "errors": []
        },
        "user": {
            "gdpr": {
                "consent_timestamp": 0,
                "consent_status": "opted_in",
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        }
    }

    gdpr_obj = {}
    if gdpr is not None:
        gdpr_obj.update({
            "gdpr": {
                "consent_timestamp": 1,
                "consent_status": gdpr,
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        })
    data.get("user").update(gdpr_obj)

    ccpa_obj = {}
    if ccpa is not None:
        ccpa_obj.update({
            "ccpa": {
                "status": ccpa
            }
        })
    if viewed is False:
        data.get("request").update({
            "clickedThrough": ["videoLength", "download", "mraidOpen", "mraidClose"]
        })
        data.get("request").update({
            "plays": [{
                "userActions": [{
                    "value": video_len,
                    "action": "videoLength",
                    "timestamp_millis": 1595826615000
                }, {
                    "value": download,
                    "action": "download",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidOpen",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidClose",
                    "timestamp_millis": 1595826662000
                }],
                "startTime": 1595826614000
            }]
        })
    if download is None:
        data.get("request").update({
            "clickedThrough": ["videoLength", "mraidOpen", "mraidClose"]
        })
        data.get("request").update({
            "plays": [{
                "userActions": [{
                    "value": video_len,
                    "action": "videoLength",
                    "timestamp_millis": 1595826615000
                }, {
                    "action": "mraidOpen",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidClose",
                    "timestamp_millis": 1595826662000
                }],
                "startTime": 1595826614000
            }]
        })

    if skoAutoshow is True:
        data.get("request").update({
            "clickedThrough": ["videoLength", "videoViewed", "download", "mraidOpen", "mraidClose", "skoAutoShow"]
        })
        data.get("request").update({
            "plays": [{
                "userActions": [{
                    "value": video_len,
                    "action": "videoLength",
                    "timestamp_millis": 1595826615000
                }, {
                    "value": viewed_len,
                    "action": "videoViewed",
                    "timestamp_millis": 1595826615000
                }, {
                    "value": 2,
                    "action": "skoAutoShow",
                    "timestamp_millis": 1595826627010
                },
                    {
                        "value": download,
                        "action": "download",
                        "timestamp_millis": 1595826627000
                    }, {
                        "action": "mraidOpen",
                        "timestamp_millis": 1595826627000
                    }, {
                        "action": "mraidClose",
                        "timestamp_millis": 1595826662000
                    }, {
                        "action": deeplink,
                        "timestamp_millis": 1503075311000
                    }],
                "startTime": 1595826614000
            }]
        }
        )

    if config_extension is not None:
        config_extension_obj = {
            "config_extension": config_extension
        }
        data.get("ext").update(config_extension_obj)

    return data


def report_ad_v5_android(pub_app_id=None, placement_id=None, android_id=gen_device_id(), header_bidding=False,
                         gdpr=None, ccpa=None, app_id=test_app_id_android, ad_token=test_ad_token_android,
                         campaign=test_campaign_android, completed_viewed=True, viewed=True, download=1,
                         deeplink='deeplinkSuccess', ifa='', coppa=None, app_set_id=''):
    video_len = 37986
    if completed_viewed is True:
        viewed_len = video_len * 0.8 + 1
    else:
        viewed_len = 1
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "1",
            "ver": "1.0.0"
        },
        "system": {
            "cache": []
        },
        "device": {
            "ua": 'CoolPad8190Q_CMCC_TD/1.0 Linux/3.4.5 Android/4.1 Release/03.31.2013 Browser/AppleWebkit534.3',
            "make": 'cool',
            "model": 'q10',
            "os": "android",
            "osv": "7.2.0",
            "h": 1920,
            "w": 1080,
            "ifa": ifa,
            "ext": {
                "vungle": {
                    "android": {
                        "android_id": android_id,
                        "app_set_id": app_set_id,
                        "gaid": "",
                        "battery_level": 0.98,
                        "battery_state": "BATTERY_PLUGGED_AC",
                        "battery_saver_enabled": 0,
                        "connection_type": "MOBILE",
                        "connection_type_detail": "WIFI",
                        "data_saver_status": "DISABLED",
                        "network_metered": 1,
                        "locale": "en_GB",
                        "language": "en",
                        "time_zone": "Asia/Calcutta",
                        "volume_level": 0,
                        "sound_enabled": 0,
                        "sd_card_available": 1,
                        "os_name": "xiaomi/vince/vince:7.1.2/N2G47H/V9.5.12.0.NEGMIFA:user/release-keys",
                        "storage_bytes_available": 43734888448,
                        "vduid": "",
                        "os_api_level": 25,
                        "is_tv": False,
                        "is_sideload_enabled": True,
                        "idfv": ""
                    }
                }
            }
        },
        "ext": {},
        "request": {
            "app_id": app_id,
            "ordinal_view": 1,
            "clickedThrough": ["videoLength", "videoViewed", "download", "mraidOpen", "mraidClose"],
            "incentivized": 1,
            "templateId": "5d7936a80ed7e506be620bf0",
            "adStartTime": 1595826614000,
            "plays": [{
                "userActions": [{
                    "value": "162",
                    "action": "videoLength",
                    "timestamp_millis": 1595826615000
                }, {
                    "value": "163",
                    "action": "videoViewed",
                    "timestamp_millis": 1595826615000
                }, {
                    "action": "download",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidOpen",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidClose",
                    "timestamp_millis": 1595826662000
                }, {
                    "action": deeplink,
                    "timestamp_millis": 1503075311000
                }
                ],
                "startTime": 1595826614000
            }],
            "ad_token": ad_token,
            "adDuration": 46000,
            "ttDownload": 4000,
            "init_timestamp": 1595826498000,
            "adType": "vungle_mraid",
            "campaign": campaign,
            "asset_download_duration": 1000,
            "placement_reference_id": placement_id,
            "ad_size": "unknown",
            "header_bidding": header_bidding,
            "errors": []
        },
        "user": {
            # "gdpr": {
            #     "consent_timestamp": 0,
            #     "consent_status": "opted_in",
            #     "consent_message_version": "",
            #     "consent_source": "publisher"
            # }
        },
    }
    if viewed is False:
        data.get("request").update({
            "clickedThrough": ["videoLength", "download", "mraidOpen", "mraidClose"]
        })
        data.get("request").update({
            "plays": [{
                "userActions": [{
                    "value": video_len,
                    "action": "videoLength",
                    "timestamp_millis": 1595826615000
                }, {
                    "value": download,
                    "action": "download",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidOpen",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidClose",
                    "timestamp_millis": 1595826662000
                }],
                "startTime": 1595826614000
            }]
        })

    gdpr_obj = {}
    if gdpr is not None:
        gdpr_obj.update({
            "gdpr": {
                "consent_timestamp": 1,
                "consent_status": gdpr,
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        })
    data.get("user").update(gdpr_obj)

    ccpa_obj = {}
    if ccpa is not None:
        ccpa_obj.update({
            "ccpa": {
                "status": ccpa
            }
        })
    data.get("user").update(ccpa_obj)
    coppa_obj = {}
    if coppa is not None:
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    return data


def report_ad_v5_windows(pub_app_id=None, placement_id=None, ashwid=gen_device_id(), ifa=gen_device_id(),
                         header_bidding=False, gdpr=None, ccpa=None, app_id=gen_test_app_id('windows'),
                         ad_token=test_ad_token_windows, campaign=test_campaign_windows):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "CS_sample.App",
            "ver": "1.0.0"
        },
        "system": {
            "cache": []
        },
        "device": {
            "osv": "10.0.18362.592",
            "os": "windows",
            "h": 900,
            "w": 1200,
            "ua": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; WebView/3.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
            "model": "GL752VW",
            "ifa": ifa,
            "lmt": 0,
            "make": "ASUSTeK COMPUTER INC.",
            "ext": {
                "vungle": {
                    "windows": {
                        "locale": "en-US",
                        "msaid": "3e09bc404f16b2e32de056b8216388c7",
                        "ashwid": ashwid,
                        "language": "en",
                        "connection_type": "wifi",
                        "battery_state": "Discharging",
                        "battery_saver_enabled": 0,
                        "battery_level": 0.66,
                        "storage_bytes_available": 782966620160,
                        "time_zone": "America/Los_Angeles",
                        "os_name": "WINDOWS"
                    }
                }
            }
        },
        "ext": {},
        "request": {
            "app_id": app_id,
            "ordinal_view": 1,
            "clickedThrough": ["videoLength", "videoViewed", "download", "mraidOpen", "mraidClose"],
            "incentivized": 1,
            "templateId": "5d7936a80ed7e506be620bf0",
            "adStartTime": 1595826614000,
            "plays": [{
                "userActions": [{
                    "value": "37986",
                    "action": "videoLength",
                    "timestamp_millis": 1595826615000
                }, {
                    "value": "163",
                    "action": "videoViewed",
                    "timestamp_millis": 1595826615000
                }, {
                    "action": "download",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidOpen",
                    "timestamp_millis": 1595826627000
                }, {
                    "action": "mraidClose",
                    "timestamp_millis": 1595826662000
                }],
                "startTime": 1595826614000
            }],
            "ad_token": ad_token,
            "adDuration": 46000,
            "ttDownload": 4000,
            "init_timestamp": 1595826498000,
            "adType": "vungle_mraid",
            "campaign": campaign,
            "asset_download_duration": 1000,
            "placement_reference_id": placement_id,
            "ad_size": "unknown",
            "header_bidding": header_bidding,
            "errors": []
        },
        "user": {
            "gdpr": {
                "consent_timestamp": 0,
                "consent_status": "opted_in",
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        }
    }

    gdpr_obj = {}
    if gdpr is not None:
        gdpr_obj.update({
            "gdpr": {
                "consent_timestamp": 1,
                "consent_status": gdpr,
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        })
    data.get("user").update(gdpr_obj)

    ccpa_obj = {}
    if ccpa is not None:
        ccpa_obj.update({
            "ccpa": {
                "status": ccpa
            }
        })
    data.get("user").update(ccpa_obj)

    return data


def report_ad_legacy_android(pub_app_id=None, ifa=gen_device_id(), app_id=test_app_id_android,
                             campaign=test_campaign_android):
    data = {
        "plays": [
            {
                "userActions": [
                    {
                        "action": "volume",
                        "timestamp_millis": 1507411769483,
                        "value": "0"
                    }
                ],
                "videoLength": 30059,
                "videoViewed": 30059
            }
        ],
        "adDuration": 39082,
        "campaign": campaign,
        "url": "https://cdn-lb.vungle.com/zen/Vungle_30s_Legendary_Instructional_EN_170914_Portrait-720x1280-Q2.mp4",
        "demo": {},
        "deviceInfo": {
            "soundEnabled": False,
            "dim": {
                "width": 720,
                "height": 1280
            },
            "networkOperator": "TURKCELL",
            "volume": 0,
            "platform": "android",
            "connection": "wifi",
            "userAgent": "Mozilla/5.0 (Linux; Android 6.0.1; SM-J700F Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like "
                         "Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36",
            "model": "samsung,SM-J700F",
            "osVersion": "6.0.1",
            "isSdCardAvailable": 1
        },
        "pubAppId": pub_app_id,
        "isu": "",
        "app_id": app_id,
        "adStartTime": 1507411769375,
        "ttDownload": 17595,
        "incentivized": 0,
        "ifa": ifa,
        "isIFA": True,
        "clickedThrough": [],
        "ordinal_view": 1
    }

    return data


def sdk_logging():
    data = {
        "batch_id": 0,
        "device_guid": "ssp-automation-test",
        "payload": [
            {
                "raw_log": "'2017-08-23 00:03:44','C562A43B-4771-472B-ACBD-DF4F0118F9F6','debug','User Agent "
                           "request sent.','SDK Initialization','','','com.vungle.ios-sdk-app.qa','America/Chicago'",
                "metadata": {
                    "device_timestamp": "2020-08-23 00:03:44",
                    "raw_log": "User Agent request sent.",
                    "bundle_id": "com.vungle.ios-sdk-app.qa",
                    "log_level": "debug",
                    "time_zone": "America/Chicago",
                    "context": "SDK Initialization",
                    "sdk_user_agent": "",
                    "event_id": "5f54a320537a7700012c74c6"
                }
            }
        ]
    }

    return data


def sdk_error_logging(reason=2, message='sdk error log', eventID="5f54a320537a7700012c74c6"):
    data = {
        "errors": [
            {
                "at": 1657696701,
                "reason": 2,
                "message": 'error_log1',
                "eventId": '5f54a320537a7700012c74c6',
                "make": "Apple",
                "model": "iPhone11,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily1",
                "connectionTypeDetail": "test01",
                "placementReferenceId": "placementId01",
                "creativeId": "creativeId01",
                "connectionTypeDetailAndroid":"testAndroid"
            },
            {
                "at": 165765000,
                "reason": 3,
                "message": "error_log2",
                "eventId": "5f54a320537a7700012c74c99",
                "make": "Apple",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13.4',
                "connectionType": "emily",
                "connectionTypeDetail": "test02",
                "placementReferenceId": "placementId02",
                "creativeId": "creativeId02",
                "connectionTypeDetailAndroid": "testAndroid1"
            }
        ]
    }
    return data


def sdk_metrics_logging():
    data = {
        "metrics": [
            {
                "type": 0,
                "value": 0,
                "meta": '/url0',
                "make": "UNKNOWN_METRIC_TYPE",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily3",
                "connectionTypeDetail": "test00",
                "placementReferenceId": "placementId00",
                "creativeId": "creativeId00"
            },
            {
                "type": 1,
                "value": 1,
                "meta": '/url1',
                "make": "AD_REQUEST_TO_RESPONSE_DURATION_MS",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily3",
                "connectionTypeDetail": "test01",
                "placementReferenceId": "placementId01",
                "creativeId": "creativeId01"
            },
            {
                "type": 2,
                "value": 2,
                "meta": '/url2',
                "make": "AD_RESPONSE_TO_SHOW_DURATION_MS",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily3",
                "connectionTypeDetail": "test02",
                "placementReferenceId": "placementId02",
                "creativeId": "creativeId02"
            },
            {
                "type": 3,
                "value": 3,
                "meta": '/url3',
                "make": "AD_SHOW_TO_DISPLAY_DURATION_MS",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily3",
                "connectionTypeDetail": "test03",
                "placementReferenceId": "placementId03",
                "creativeId": "creativeId03"
            },
            {
                "type": 4,
                "value": 4,
                "meta": '/url4',
                "make": "AD_DISPLAY_TO_CLICK_DURATION_MS",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily3",
                "connectionTypeDetail": "test04",
                "placementReferenceId": "placementId04",
                "creativeId": "creativeId04"
            },
            {
                "type": 5,
                "value": 5,
                "meta": '/url5',
                "make": "IOS_STORE_KIT_LOAD_TIME_MS",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily3",
                "connectionTypeDetail": "test05",
                "placementReferenceId": "placementId05",
                "creativeId": "creativeId05"
            },
            {
                "type": 6,
                "value": 6,
                "meta": '/url6',
                "make": "INIT_REQUEST_TO_RESPONSE_DURATION_MS",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily3",
                "connectionTypeDetail": "test06",
                "placementReferenceId": "placementId06",
                "creativeId": "creativeId06"
            },
            {
                "type": 7,
                "value": 7,
                "meta": '/url7',
                "make": "ASSET_DOWNLOAD_DURATION_MS",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily3",
                "connectionTypeDetail": "test07",
                "placementReferenceId": "placementId07",
                "creativeId": "creativeId07"
            },
            {
                "type": 8,
                "value": 8,
                "meta": '/url8',
                "make": "LOCAL_ASSETS_USED",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily3",
                "connectionTypeDetail": "test08",
                "placementReferenceId": "placementId08",
                "creativeId": "creativeId08"
            },
            {
                "type": 9,
                "value": 9,
                "meta": '/url9',
                "make": "REMOTE_ASSETS_USED",
                "model": "iPhone12,8",
                "os": "ios",
                "osVersion": '13',
                "connectionType": "emily3",
                "connectionTypeDetail": "test09",
                "placementReferenceId": "placementId09",
                "creativeId": "creativeId09"
            },
            {
                "type": 10,
                "value": 10,
                "meta": '/url10',
                "make": "TEMPLATE_DOWNLOAD_DURATION_MS",
                "model": "iPhone11,8",
                "os": "ios",
                "osVersion": '13.2',
                "connectionType": "emily3",
                "connectionTypeDetail": "test10",
                "placementReferenceId": "placementId10",
                "creativeId": "creativeId10"
            },
            {
                "type": 11,
                "value": 11,
                "meta": '/url11',
                "make": "AD_REQUEST_TO_CALLBACK_DURATION_MS",
                "model": "iPhone11,8",
                "os": "ios",
                "osVersion": '13.2',
                "connectionType": "emily3",
                "connectionTypeDetail": "test11",
                "placementReferenceId": "placementId11",
                "creativeId": "creativeId11"
            },
            {
                "type": 12,
                "value": 12,
                "meta": '/url12',
                "make": "AD_REQUEST_TO_CALLBACK_ADO_DURATION_MS",
                "model": "iPhone11,8",
                "os": "ios",
                "osVersion": '13.2',
                "connectionType": "emily3",
                "connectionTypeDetail": "test12",
                "placementReferenceId": "placementId12",
                "creativeId": "creativeId12"
            },
            {
                "type": 13,
                "value": 13,
                "meta": '/url13',
                "make": "ASSET_FILE_SIZE",
                "model": "iPhone11,8",
                "os": "ios",
                "osVersion": '13.2',
                "connectionType": "emily3",
                "connectionTypeDetail": "test12",
                "placementReferenceId": "placementId12",
                "creativeId": "creativeId12"
            },
            {
                "type": 14,
                "value": 14,
                "meta": '/url14',
                "make": "USER_AGENT_LOAD_DURATION_MS",
                "model": "iPhone11,8",
                "os": "ios",
                "osVersion": '13.2',
                "connectionType": "emily3",
                "connectionTypeDetail": "test12",
                "placementReferenceId": "placementId12",
                "creativeId": "creativeId12"
            },
            {
                "type": 15,
                "value": 15,
                "meta": '/url15',
                "make": "TEMPLATE_ZIP_SIZE",
                "model": "iPhone11,8",
                "os": "ios",
                "osVersion": '13.2',
                "connectionType": "emily3",
                "connectionTypeDetail": "test12",
                "placementReferenceId": "placementId12",
                "creativeId": "creativeId12"
            },
            {
                "type": 2000,
                "value": 16,
                "meta": '/url16',
                "make": "SKOVERLAY_PRESENTED_FOR_AD",
                "model": "iPhone11,8",
                "os": "ios",
                "osVersion": '13.2',
                "connectionType": "emily3",
                "connectionTypeDetail": "test12",
                "placementReferenceId": "placementId12",
                "creativeId": "creativeId12"
            },
            {
                "type": 2001,
                "value": 17,
                "meta": '/url17',
                "make": "SAFARI_PRESENTED_FOR_AD",
                "model": "iPhone11,8",
                "os": "ios",
                "osVersion": '13.2',
                "connectionType": "emily3",
                "connectionTypeDetail": "test12",
                "placementReferenceId": "placementId12",
                "creativeId": "creativeId12"
            },
            {
                "type": 2002,
                "value": 18,
                "meta": '/url17',
                "make": "STORE_KIT_PRESENTED_FOR_AD",
                "model": "iPhone11,8",
                "os": "ios",
                "osVersion": '13.2',
                "connectionType": "emily3",
                "connectionTypeDetail": "test12",
                "placementReferenceId": "placementId12",
                "creativeId": "creativeId12"
            },
        ]
    }
    return data


def session_end(pub_app_id=None, ifa=gen_device_id()):
    data = {
        "start": 1447651822967,
        "end": 1447651862662,
        "pubAppId": pub_app_id,
        "ifa": ifa
    }

    return data


def ri_v5_ios(pub_app_id=None, placement_id=None, gdpr=None, ifa=gen_device_id(), os_version='13',
              app_id=test_app_id_ios, coppa=None):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.test",
            "ver": "1"
        },
        "system": {
            "cache": []
        },
        "device": {
            "make": "Apple",
            "os": "ios",
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko)"
                  " Mobile/14A345",
            "h": 1334,
            "model": "x86_64",
            "osv": os_version,
            "ext": {
                "vungle": {
                    "ios": {
                        "volume": 1,
                        "battery_state": "unknown",
                        "idfa": "",
                        "vduid": "",
                        "battery_level": -1,
                        "locale": "en_US",
                        "connection_type": "wifi",
                        "language": "en",
                        "storage_bytes_available": 302327201792,
                        "idfv": "",
                        "battery_saver_enabled": 0,
                        "time_zone": "America/Los_Angeles"
                    }
                }
            },
            "carrier": "",
            "ifa": ifa,
            "w": 750,
            "lmt": 0
        },
        "ext": {},
        "request": {
            "user": "mUser",
            "placement_reference_id": placement_id,
            "app_id": app_id,
            "adStartTime": 1526889372188
        },
        "user": {
            "gdpr": {
                "consent_status": "opted_in",
                "consent_source": "publisher",
                "consent_timestamp": 1526889421
            }
        }
    }

    gdpr_obj = {}
    if gdpr is not None:
        gdpr_obj.update({
            "gdpr": {
                "consent_timestamp": 1,
                "consent_status": gdpr,
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        })
    data.get("user").update(gdpr_obj)
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)
    return data


def ri_v5_android(pub_app_id=None, placement_id=None, gdpr=None, android_id=gen_device_id(),
                  app_id=gen_test_app_id('android'), ifa='', coppa=None):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.test",
            "ver": "1"
        },
        "system": {
            "cache": []
        },
        "device": {
            "ua": 'CoolPad8190Q_CMCC_TD/1.0 Linux/3.4.5 Android/4.1 Release/03.31.2013 Browser/AppleWebkit534.3',
            "make": 'cool',
            "model": 'q10',
            "os": "android",
            "osv": "7.2.0",
            "h": 1920,
            "w": 1080,
            "ifa": ifa,
            "ext": {
                "vungle": {
                    "android": {
                        "android_id": android_id,
                        "gaid": "",
                        "battery_level": 0.98,
                        "battery_state": "BATTERY_PLUGGED_AC",
                        "battery_saver_enabled": 0,
                        "connection_type": "MOBILE",
                        "connection_type_detail": "WIFI",
                        "data_saver_status": "DISABLED",
                        "network_metered": 1,
                        "locale": "en_GB",
                        "language": "en",
                        "time_zone": "Asia/Calcutta",
                        "volume_level": 0,
                        "sound_enabled": 0,
                        "sd_card_available": 1,
                        "os_name": "xiaomi/vince/vince:7.1.2/N2G47H/V9.5.12.0.NEGMIFA:user/release-keys",
                        "storage_bytes_available": 43734888448,
                        "vduid": "",
                        "os_api_level": 25,
                        "is_tv": False,
                        "is_sideload_enabled": True,
                        "idfv": ""
                    }
                }
            }
        },
        "ext": {},
        "request": {
            "user": "mUser",
            "placement_reference_id": placement_id,
            "app_id": app_id,
            "adStartTime": 1526889372188
        },
        "user": {
            # "gdpr": {
            #     "consent_status": "opted_in",
            #     "consent_source": "publisher",
            #     "consent_timestamp": 1526889421
            # }
        }
    }

    gdpr_obj = {}
    if gdpr is not None:
        gdpr_obj.update({
            "gdpr": {
                "consent_timestamp": 1,
                "consent_status": gdpr,
                "consent_message_version": "",
                "consent_source": "publisher"
            }
        })
    data.get("user").update(gdpr_obj)
    coppa_obj = {}
    if coppa is not None and coppa != "":
        coppa_obj.update({
            "coppa": {
                "is_coppa": coppa
            }
        })
    data.get("user").update(coppa_obj)

    return data


def sdk_bi_ios(pub_app_id=None, ifa=gen_device_id(), os_version='13', cache_bust=1, target='', id='', event_id=''):
    data = {
        "app": {
            "id": pub_app_id,
            "bundle": "com.vungle.test",
            "ver": "1"
        },
        "device": {
            "make": "Apple",
            "os": "ios",
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko)"
                  " Mobile/14A345",
            "h": 1334,
            "model": "x86_64",
            "osv": os_version,
            "ext": {
                "vungle": {
                    "ios": {
                        "volume": 1,
                        "battery_state": "unknown",
                        "idfa": "",
                        "vduid": "",
                        "battery_level": -1,
                        "locale": "en_US",
                        "connection_type": "wifi",
                        "language": "en",
                        "storage_bytes_available": 302327201792,
                        "idfv": "",
                        "battery_saver_enabled": 0,
                        "time_zone": "America/Los_Angeles"
                    }
                }
            },
            "carrier": "",
            "ifa": ifa,
            "w": 750,
            "lmt": 0
        },
        "cache_bust": []
    }

    if cache_bust is not None:
        data.get("cache_bust").append({
            "target": target,
            "id": id,
            "event_id": event_id
        })

    return data


def tpat(adv='4ee19fb8121ae61a03000022', cid='5eb9877e136f432531e6f285', crid='5eb9a49a5ddc02539da7c732',
         event_id='601766a22438f133b8d98f9a', event_type='click', hb=True, int=True, os='iOS',
         pid='5c0040e936a9c14cefbd6f44', pub='59786bc2a43b3a08620026b1', test=False,
         vid='1E6A997F-E325-4C45-9E0D-86128D89FA36', vid_type='IFA', ic=None):
    data = {
        "adv": adv,
        "cid": cid,
        "crid": crid,
        "event_id": event_id,
        "event_type": event_type,
        "hb": hb,
        "int": int,
        "os": os,
        "pid": pid,
        "pub": pub,
        "test": test,
        "vid": vid,
        "vid_type": vid_type,
    }
    if ic is not None:
        data.update({"ic": ic})
    return data


def hbp_impression(ext=None):
    if ext is not None:
        data = {
            "ext": ext
        }

        return data
    else:
        return None


def hbp_load_ad(ext=None):
    if ext is not None:
        data = {
            "ext": ext
        }

        return data
    else:
        return None


def hbp_ohayoo(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
               is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
               make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104b",
                "video": {
                    "mimes": [
                        "video/mp4"
                    ],
                    "minduration": 0,
                    "maxduration": 1234,
                    "w": 1536,
                    "h": 2048,
                    "linearity": 1,
                    "pos": 7,
                    "battr": [
                        1,
                        2,
                        5,
                        8,
                        9,
                        14,
                        16,
                        17
                    ],
                    "ext": {
                        "videotype": "rewarded"
                    }
                },
                "banner": {
                    "api": [
                        3,
                        5
                    ],
                    "battr": [
                        3,
                        8,
                        9,
                        10,
                        14
                    ],
                    "btype": [
                        4
                    ],
                    "h": 50,
                    "pos": 1,
                    "w": 320
                },
                "displaymanager": "Vungle",
                "displaymanagerver": "5.0.0",
                "tagid": placement_id,
                "placement": 5,
                "secure": 1,
                "instl": 1,
                "bidfloor": 1,
                "ext": {
                    "vungle": {
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "App Name",
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa",
            "cat": [
                "IAB9-30"
            ],
            "publisher": {
                "id": "345678",
                "ext": {
                    "installed_sdk": {
                        "id": "vacto_test",
                        "sdk_version": {
                            "major": 6,
                            "minor": 0,
                            "micro": 3
                        },
                        "adapter_version": {
                            "major": 1,
                            "minor": 0,
                            "micro": 0
                        }
                    }
                }
            }
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "at": 1,
        "tmax": 1000,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB8-5",
            "IAB8-18"
        ],
        "badv": [

        ],
        "regs": {
            "coppa": 1
        },
        "user": {
            "data": [{
                "id": "1",
                "name": "Publisher Passed"
            }]
        },
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


def hbp_saygames(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
                 is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
                 make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104b",
                "video": {
                    "mimes": [
                        "video/mp4"
                    ],
                    "minduration": 0,
                    "maxduration": 1234,
                    "w": 1536,
                    "h": 2048,
                    "linearity": 1,
                    "pos": 7,
                    "battr": [
                        1,
                        2,
                        5,
                        8,
                        9,
                        14,
                        16,
                        17
                    ],
                    "ext": {
                        "videotype": "rewarded"
                    }
                },
                "banner": {
                    "api": [
                        3,
                        5
                    ],
                    "battr": [
                        3,
                        8,
                        9,
                        10,
                        14
                    ],
                    "btype": [
                        4
                    ],
                    "h": 50,
                    "pos": 1,
                    "w": 320
                },
                "displaymanager": "Vungle",
                "displaymanagerver": "5.0.0",
                "tagid": placement_id,
                "placement": 5,
                "secure": 1,
                "instl": 1,
                "bidfloor": 1,
                "ext": {
                    "vungle": {
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "App Name",
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa",
            "cat": [
                "IAB9-30"
            ],
            "publisher": {
                "id": "345678",
                "ext": {
                    "installed_sdk": {
                        "id": "vacto_test",
                        "sdk_version": {
                            "major": 6,
                            "minor": 0,
                            "micro": 3
                        },
                        "adapter_version": {
                            "major": 1,
                            "minor": 0,
                            "micro": 0
                        }
                    }
                }
            }
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "at": 1,
        "tmax": 1000,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB8-5",
            "IAB8-18"
        ],
        "badv": [

        ],
        "regs": {
            "coppa": 1
        },
        "user": {
            "data": [{
                "id": "1",
                "name": "Publisher Passed"
            }]
        },
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


def hbp_aequus(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
               is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
               make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104b",
                "video": {
                    "mimes": [
                        "video/mp4"
                    ],
                    "minduration": 0,
                    "maxduration": 1234,
                    "w": 1536,
                    "h": 2048,
                    "linearity": 1,
                    "pos": 7,
                    "battr": [
                        1,
                        2,
                        5,
                        8,
                        9,
                        14,
                        16,
                        17
                    ],
                    "ext": {
                        "videotype": "rewarded"
                    }
                },
                "banner": {
                    "api": [
                        3,
                        5
                    ],
                    "battr": [
                        3,
                        8,
                        9,
                        10,
                        14
                    ],
                    "btype": [
                        4
                    ],
                    "h": 50,
                    "pos": 1,
                    "w": 320
                },
                "displaymanager": "Vungle",
                "displaymanagerver": "5.0.0",
                "tagid": placement_id,
                "placement": 5,
                "secure": 1,
                "instl": 1,
                "bidfloor": 1,
                "ext": {
                    "vungle": {
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "name": "App Name",
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa",
            "cat": [
                "IAB9-30"
            ],
            "publisher": {
                "id": "345678",
                "ext": {
                    "installed_sdk": {
                        "id": "vacto_test",
                        "sdk_version": {
                            "major": 6,
                            "minor": 0,
                            "micro": 3
                        },
                        "adapter_version": {
                            "major": 1,
                            "minor": 0,
                            "micro": 0
                        }
                    }
                }
            }
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "at": 1,
        "tmax": 1000,
        "cur": [
            "USD"
        ],
        "bcat": [
            "IAB8-5",
            "IAB8-18"
        ],
        "badv": [

        ],
        "regs": {
            "coppa": 1
        },
        "user": {
            "data": [{
                "id": "1",
                "name": "Publisher Passed"
            }]
        },
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


def hbp_unity(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
              is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
              make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104",
                "tagid": placement_id,
                "banner": {
                    "w": 320,
                    "h": 50
                },
                "native": {
                    "w": 1024,
                    "h": 768
                },
                "video": {
                    "w": 1080,
                    "h": 1920
                },
                "ext": {
                    "vungle": {
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa"
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "regs": {
            "coppa": 1,
            "ext": {
                "gdpr": 1,
                "ccpa": 1
            }
        },
        "at": 1,
        "tmax": 1000,
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


def hbp_fyber(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
              is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
              make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104",
                "tagid": placement_id,
                "banner": {
                    "w": 320,
                    "h": 50
                },
                "native": {
                    "w": 1024,
                    "h": 768
                },
                "video": {
                    "w": 1080,
                    "h": 1920
                },
                "ext": {
                    "vungle": {
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa"
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "regs": {
            "coppa": 1,
            "ext": {
                "gdpr": 1,
                "ccpa": 1
            }
        },
        "at": 1,
        "tmax": 1000,
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


def hbp_topon(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
              is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
              make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104",
                "tagid": placement_id,
                "banner": {
                    "w": 320,
                    "h": 50
                },
                "native": {
                    "w": 1024,
                    "h": 768
                },
                "video": {
                    "w": 1080,
                    "h": 1920
                },
                "ext": {
                    "vungle": {
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa"
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "regs": {
            "coppa": 1,
            "ext": {
                "gdpr": 1,
                "ccpa": 1
            }
        },
        "at": 1,
        "tmax": 1000,
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


def hbp_appodeal(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
                 is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
                 make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104",
                "tagid": placement_id,
                "banner": {
                    "w": 320,
                    "h": 50
                },
                "native": {
                    "w": 1024,
                    "h": 768
                },
                "video": {
                    "w": 1080,
                    "h": 1920
                },
                "ext": {
                    "vungle": {
                        "placement_reference_id": placement_id,
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa"
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "regs": {
            "coppa": 1,
            "ext": {
                "gdpr": 1,
                "ccpa": 1
            }
        },
        "at": 1,
        "tmax": 1000,
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


def hbp_admob(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
              is_test=0, status_code=79, notification_token=None, banner_format=None, keyvals=None, segment=None,
              device_ip=ca_us_ip, device_ext=None, lmt=0, bid_price=0.8, minimum_bid_to_win=1.09, platform='ios',
              app_set_id='', android_id='', make='Apple', model='iPhone11,8', geo=None, ua=None, idfv='',
              buyer_creative_id="test_creative_id_854943"):
    data = {
        "id": "40iE2yI41tvziw91lKs93d",
        "app": {
            "name": "Tiles-Template-Test-App",
            "storeurl": "http://www.vungle.com",
            "privacypolicy": 1,
            "publisher": {
                "id": "pub-7319269804560504"
            },
            "ext": {
                "installed_sdk": [
                    {
                        "id": 'emily_test',
                        "sdk_version": {
                            "major": 6,
                            "minor": 0,
                            "micro": 3
                        },
                        "adapter_version": {
                            "major": 1,
                            "minor": 0,
                            "micro": 0
                        }
                    }
                ]

            },
            "ver": "1.0"
        },
        "imp": [
            {
                "id": "1",
                "instl": 1,
                "banner": {
                    "w": 320,
                    "h": 50,
                    "pos": 3,
                    "expdir": [
                        1,
                        2,
                        3,
                        4
                    ]
                },
                "video": {
                    "api": [
                        3,
                        5
                    ],
                    "battr": [
                        3,
                        8,
                        9,
                        10,
                        14
                    ],
                    "companiontype": [
                        1,
                        2,
                        3
                    ],
                    "h": 480,
                    "linearity": 1,
                    "maxduration": 120,
                    "mimes": [
                        "video/mp4",
                        "video/3gpp"
                    ],
                    "minduration": 0,
                    "protocols": [
                        2,
                        5,
                        3,
                        6
                    ],
                    "startdelay": 0,
                    "w": 320
                },
                "tagid": "5854260354",
                "bidfloor": 0.79,
                "bidfloorcur": "USD",
                "secure": 1,
                "metric": [
                    {
                        "type": "click_through_rate",
                        "value": 0.0003375268424861133,
                        "vendor": "EXCHANGE"
                    },
                    {
                        "type": "viewability",
                        "value": 0.96,
                        "vendor": "EXCHANGE"
                    }
                ],
                "ext": {
                    "billing_id": [
                        '92233720368'
                    ],
                    "dfp_ad_unit_code": "/9795538/google/test",
                    "ampad": 3,
                    "open_bidding": {
                        "is_open_bidding": True,
                        "adunit_mappings": [
                            {
                                "keyvals": [
                                    {
                                        "key": "application_id",
                                        "value": pub_app_id
                                    },
                                    {
                                        "key": "placementID",
                                        "value": placement_id
                                    }
                                ]
                            }
                        ]
                    },
                    "buyer_generated_request_data": [
                        {
                            "data": bid_token
                        }
                    ]
                }
            }
        ],
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "user": {
            "data": [
                {
                    "id": "pub-7319269804560504",
                    "name": "Publisher Passed",
                    "segment": [
                        {
                            "name": "appid" if platform == 'android' else "application_id",
                            "value": pub_app_id
                        },
                        {
                            "name": "placementID",
                            "value": placement_id
                        }
                    ]
                }
            ],
            "ext": {}
        },
        "at": 1,
        "tmax": 16200,
        "cur": [
            "USD"
        ],
        "regs": {
            "coppa": 1,
            "ext": {
                "gdpr": 1,
                "ccpa": 1
            }
        },
        "ext": {
            "bid_feedback": [
                {
                    "request_id": "40iE2yI41tvziw91lKs93d",
                    "creative_status_code": status_code,
                    "buyer_creative_id": buyer_creative_id,
                    "minimum_bid_to_win": minimum_bid_to_win,
                    "sampled_mediation_cpm_ahead_of_auction_winner": 1.2
                }
            ],
            "google_query_id": "ANy-zUF198-d9cYo4j1m1rSmvT2rk8ru9d5e901BI39p389875OeJ8iT0P77289XD97A50fh"
        },
        "test": is_test
    }

    if notification_token is not None:
        token_obj = {
            "event_notification_token": {
                "payload": notification_token
            }
        }
        data.get("ext").get("bid_feedback")[0].update(token_obj)

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    if keyvals is not None:
        data.get('imp')[0].get('ext').get('open_bidding').get('adunit_mappings')[0].update({"keyvals": keyvals})

    if segment is not None:
        data.get('user').get('data')[0].update({"segment": keyvals})

    return data


def hbp_common(pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021', ifa=gen_device_id(), bid_token='',
               is_test=0, banner_format=None, device_ip=ca_us_ip, idfv='', device_ext=None, geo=None, ua=None, lmt=0,
               make='Apple', model='iPhone11,8', platform='ios', app_set_id='', android_id=''):
    data = {
        "id": "ac58e7b8f4614177a53f75681fbc104a",
        "imp": [
            {
                "id": "ac58e7b8f4614177a53f75681fbc104",
                "tagid": placement_id,
                "banner": {
                    "w": 320,
                    "h": 50
                },
                "native": {
                    "w": 1024,
                    "h": 768
                },
                "video": {
                    "w": 1080,
                    "h": 1920
                },
                "ext": {
                    "vungle": {
                        "bid_token": bid_token
                    }
                }
            }
        ],
        "app": {
            "id": pub_app_id,
            "ver": "13.3",
            "bundle": "com.vungle.ios-sdk-app.qa"
        },
        "device": generate_device_obj(platform, ifa=ifa, make=make, model=model, device_ip=device_ip, idfv=idfv,
                                      lmt=lmt, app_set_id=app_set_id, android_id=android_id, device_ext=device_ext,
                                      geo=geo, ua=ua),
        "regs": {
            "coppa": 1,
            "ext": {
                "gdpr": 1,
                "ccpa": 1
            }
        },
        "at": 1,
        "tmax": 1000,
        "test": is_test
    }

    if banner_format is not None:
        data.get('imp')[0].get('banner').update({"format": banner_format})

    return data


def hbp_partner(partner='max', pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021',
                ifa=gen_device_id(), bid_token='', is_test=0, notification_token=None, banner_format=None,
                ip=ca_us_ip, platform='ios', status_code=79, device_ext=None, geo=None, ua=None, lmt=0, make='Apple',
                model='iPhone11,8', skadnetids=None, imp=1, idfv='', app_set_id='', android_id='', atts=0,
                video_flag=True, banner_flag=True, bid_request_ip=None,
                buyer_creative_id="test_creative_id_854943"):
    if partner == 'max':
        return hbp_max(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                       lmt=0, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                       geo=geo, make=make, model=model, idfv=idfv, skadnetids=skadnetids, imp=imp, platform=platform,
                       app_set_id=app_set_id, android_id=android_id, atts=atts,
                       video_flag=video_flag, banner_flag=banner_flag)
    elif partner == 'adtiming':
        return hbp_adtiming(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                            lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                            geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                            app_set_id=app_set_id, android_id=android_id)
    elif partner == 'ironsource':
        return hbp_ironsource(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                              lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip,
                              device_ext=device_ext, geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                              app_set_id=app_set_id, android_id=android_id)
    elif partner == 'ohayoo':
        return hbp_ohayoo(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                          lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                          geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                          app_set_id=app_set_id, android_id=android_id)
    elif partner == 'saygames':
        return hbp_saygames(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                            lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                            geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                            app_set_id=app_set_id, android_id=android_id)
    elif partner == 'aequus':
        return hbp_aequus(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                          lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                          geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                          app_set_id=app_set_id, android_id=android_id)
    elif partner == 'charboost':
        return hbp_charboost(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                             lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                             geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                             app_set_id=app_set_id, android_id=android_id)
    elif partner == 'unity':
        return hbp_unity(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                         lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                         geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                         app_set_id=app_set_id, android_id=android_id)
    elif partner == 'fyber':
        return hbp_fyber(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                         lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                         geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                         app_set_id=app_set_id, android_id=android_id)
    elif partner == 'topon':
        return hbp_topon(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                         lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                         geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                         app_set_id=app_set_id, android_id=android_id)
    elif partner == 'appodeal':
        return hbp_appodeal(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                            lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                            geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                            app_set_id=app_set_id, android_id=android_id)
    elif partner == 'admob':
        return hbp_admob(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                         lmt=lmt, is_test=is_test, notification_token=notification_token, banner_format=banner_format,
                         device_ip=ip, device_ext=device_ext, status_code=status_code, geo=geo, make=make, model=model,
                         idfv=idfv, platform=platform, app_set_id=app_set_id, android_id=android_id,
                         buyer_creative_id=buyer_creative_id)
    else:
        return hbp_common(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa, bid_token=bid_token, ua=ua,
                          lmt=lmt, is_test=is_test, banner_format=banner_format, device_ip=ip, device_ext=device_ext,
                          geo=geo, make=make, model=model, idfv=idfv, platform=platform,
                          app_set_id=app_set_id, android_id=android_id)


def s2s_partner(partner='sigmob', pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021',
                ifa=gen_device_id(), is_test=0, banner_format=None, gdpr=None, coppa=None, ccpa=None, ip=ca_us_ip,
                consent=None, idfv=None):
    if partner == 'sigmob':
        return s2s_payload_sigmob_ios(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa,
                                      is_test=is_test, banner_format=banner_format, ip=ip, gdpr=gdpr, coppa=coppa,
                                      ccpa=ccpa, consent=consent, ifv=idfv)
    else:
        return s2s_payload_ios(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa,
                               is_test=is_test, banner_format=banner_format, ip=ip, gdpr=gdpr, coppa=coppa, ccpa=ccpa,
                               consent=consent, idfv=idfv)


def s2s_partner_android(partner='sigmob', pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021',
                        ifa=gen_device_id(), is_test=0, banner_format=None, gdpr=None, coppa=None, ccpa=None, ip=ca_us_ip,
                        consent=None, android_id=None, app_set_id=None):
    if partner == 'sigmob':
        return s2s_payload_sigmob_android(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa,
                                          is_test=is_test, banner_format=banner_format, ip=ip, gdpr=gdpr, coppa=coppa,
                                          ccpa=ccpa, consent=consent, android_id=android_id, app_set_id=app_set_id)
    else:
        return s2s_payload_android(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa,
                                   is_test=is_test, banner_format=banner_format, ip=ip, gdpr=gdpr, coppa=coppa,
                                   ccpa=ccpa,
                                   consent=consent, android_id=android_id, app_set_id=app_set_id)


def s2s_partner_amazon(partner='sigmob', pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021',
                       ifa=gen_device_id(), is_test=0, banner_format=None, gdpr=None, coppa=None, ccpa=None, ip=ca_us_ip,
                       consent=None, app_set_id=None):
    if partner == 'sigmob':
        return s2s_payload_sigmob_amazon(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa,
                                         is_test=is_test, banner_format=banner_format, ip=ip, gdpr=gdpr, coppa=coppa,
                                         ccpa=ccpa, consent=consent, app_set_id=app_set_id)


def s2s_partner_windows(partner='sigmob', pub_app_id='59786bc2a43b3a08620026b1', placement_id='DEFAULT02021',
                        ifa=gen_device_id(), is_test=0, banner_format=None, gdpr=None, coppa=None, ccpa=None, ip=ca_us_ip,
                        consent=None, ashwid=None):
    if partner == 'sigmob':
        return s2s_payload_sigmob_windows(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa,
                                          is_test=is_test, banner_format=banner_format, ip=ip, gdpr=gdpr, coppa=coppa,
                                          ccpa=ccpa, consent=consent, ashwid=ashwid)
    else:
        return s2s_payload_windows(pub_app_id=pub_app_id, placement_id=placement_id, ifa=ifa,
                                   is_test=is_test, banner_format=banner_format, ip=ip, gdpr=gdpr, coppa=coppa,
                                   ccpa=ccpa, consent=consent, ashwid=ashwid)


def bflat_bid_request(adv_is_internal=True, pub_app_id='59786bc2a43b3a08620026b1',
                      placement_id='59786bc2a43b3a0862002774', event_id='604777abcf9272000148c0dd',
                      bidid='82317317-7e72-4927-8a0f-28f4b9c41251', adv_predicted_cvr=0.3, adv_erpm=3,
                      nostr_bid_price=2, do_not_track=True, supply_fee=0, max_bid_price=5,
                      adv_campaign_id="5f654d27c48c9d000ff772b7", os='iOS', hb_nrg_override=None, country='USA',
                      imp_type='video', rtb_account_id='5cd92b2661a35300113a8487', experiment=None,
                      campaign_rate_type=None, is_dynamic_rate=None):
    data = {
        "adv_is_internal": adv_is_internal,
        "adx_bid_price": '4',
        "bidder_id": '545dfdfdfdfdfdfdf',
        "adv_predicted_cvr": adv_predicted_cvr,
        "adv_erpm": adv_erpm,
        "nostr_bid_price": nostr_bid_price,
        "do_not_track": do_not_track,
        "event_id": event_id,
        "supply_fee": supply_fee,
        "max_bid_price": max_bid_price,
        "bidid": bidid,
        "pub_app_bundle_id": pub_app_id,
        "placement_id": placement_id,
        "adv_campaign_id": adv_campaign_id,
        "bidrequest_device_os": os,
        "bidrequest_geo_country": country,
        "extra_data": {},
        "hb_nrg_override": hb_nrg_override,
        "rtb_account_id": rtb_account_id
    }

    obj = {}
    if experiment is not None:
        obj.update({
            "experiment_number": experiment
        })

    data.update(extra_data=obj)

    obj = {}
    if imp_type is not None:
        obj.update({
            "bidrequest_imp_type": imp_type
        })
    data.update(obj)

    if campaign_rate_type is not None:
        data.update({"campaign_rate_type": campaign_rate_type})

    if is_dynamic_rate is not None:
        data.update({"is_dynamic_rate": is_dynamic_rate})

    return data


def recommendations(account_ids=None, application_ids=None, placement_ids=None, item_count=100, item_skip=0,
                    rec_features=None):
    data = {
        "item_count": item_count,
        "item_skip": item_skip
    }

    if account_ids is not None:
        data.update({"account_ids": account_ids})
    if application_ids is not None:
        data.update({"application_ids": application_ids})
    if placement_ids is not None:
        data.update({"placement_ids": placement_ids})
    if rec_features is not None:
        data.update({"rec_features": rec_features})

    return data


def token_verify(token=None):
    data = {
        "token": token
    }

    return data


def real_time_token_json(config_extension=config_extension_RTA, orinal_view=7,
                         pre_cached_tokens=test_pre_cached_tokens, is_coppa=None,
                         gdpr_status='opted_out', ccpa_status='opted_out',
                         token_device_id=None, token_ios_device_id=None, token_android_device_id=None,
                         token_app_set_id=None, token_amazon_device_id=None, token_amazon_app_set_id=None,
                         token_windows_device_id=None, sdk_user_agent="Vungle/6.11.1", sound_enabled=True):
    data = {
        "request": {
            "config_extension": config_extension,
            "ordinal_view": orinal_view,
            "precached_tokens": pre_cached_tokens,
            "sdk_user_agent": sdk_user_agent
        },
        "device": {
            "battery_saver_enabled": True,
            "language": "enu",
            "time_zone": "Asia/Shanghai",
            "volume_level": 1.112,
            "android": {
                "android_id": token_android_device_id,
                "app_set_id": token_app_set_id
            },
            "amazon": {
                "android_id": token_amazon_device_id,
                "app_set_id": token_amazon_app_set_id
            },
            "extension": {
                "is_sideload_enabled": True,
                "sd_card_available": True,
                "sound_enabled": sound_enabled
            },
        },
        "consent": {
            "ccpa": {
                "status": ccpa_status
            },
            "gdpr": {
                "status": gdpr_status,
                "source": "publisher",
                "message_version": "1.0",
                "timestamp": 12324343
            },
            "coppa": {}
        }
    }

    if is_coppa is not None:
        data.get("consent").get("coppa").update({"is_coppa": is_coppa})

    if token_device_id is not None:
        data.get("device").update({"ifa": token_device_id})

    if token_ios_device_id is not None:
        data.get("device").update({"ios": {"idfv": token_ios_device_id}})


    if token_windows_device_id is not None:
        data.get("device").update({"windows": {"ashwid": token_windows_device_id}})

    return data
