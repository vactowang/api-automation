# Private variables
_object_id_pattern = "^([0-9]|[a-f]){24}$"

empty_schema = {}

error_message = {
    "title": "Error message schema",
    "description" : "This is a schema that matches the error message",
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "properties":
    {
        "code": {
            "type": "integer",
            "title": "Error Code"
            },
        "message":{
            "type": "string",
            "title": "Error message"}
    },
    "required": ["message"]
}

config_v4 = {
    "connection": "string",
    "updateDelay": "number",
    "threshold": "number",
    "bufferStreamingWait": "number",
    "exceptionReportingEnabled": "boolean",
    "collectIDFV": "boolean",
    "vduid": "string",
    "optIn": "boolean"
}

config_v5 = {
    "endpoints": {
        "new": "string",
        "ads": "string",
        "will_play_ad": "string",
        "report_ad": "string",
        "log": "string",
        "ri": "string"
    },
    "placements": [
        {
            "id": "string",
            "reference_id": "string",
            "is_auto_cached": "boolean",
            "is_incentivized": "boolean",
            "supported_template_types": "array",
            "supported_ad_formats": "array"
        }
    ],
    "config": {
        "refresh_time": "number"
    },
    "will_play_ad": {
        "enabled": "boolean",
        "request_timeout": "number"
    },
    "playback": {
        "buffer_timeout": "number"
    },
    "viewability": {
        "moat": "boolean"
    },
    "exception_reporting": "boolean",
    "logging": {
        "enabled": "boolean"
    },
    "crash_report": {
        "max_send_amount": "number",
        "enabled": "boolean",
        "collect_filter": "string"
    },
    "vduid": "",
    "gdpr": {
        "is_country_data_protected": "boolean",
        "consent_title": "string",
        "consent_message": "string",
        "consent_message_version": "string",
        "button_accept": "string",
        "button_deny": "string"
    },
    "ri": {
        "enabled": "boolean"
    },
    "attribution_reporting": {
        "should_transmit_imei": "boolean"
    },
    "vision": {
        "enabled": "boolean",
        "aggregation_filters": "array",
        "aggregation_time_windows": "array",
        "view_limit": {
            "device": "number",
            "wifi": "number",
            "mobile": "number"
        }
    }
}

cache_bust = {
    "cache_bust": {
        "last_updated": "number",
        "campaign_ids": "array",
        "creative_ids": "array"
    }
}

token_verify = {
    "token": {
        "request": {
            "config_extension": "string",
            "ordinal_view": "number",
            "precached_tokens": "array",
            "sdk_user_agent": "string"
        },
        "device": {
            "battery_saver_enabled": "boolean",
            "language": "string",
            "time_zone": "string",
            "volume_level": "number",
            "extension": {
                "is_sideload_enabled": "boolean",
                "sd_card_available": "boolean",
                "sound_enabled": "boolean"
            }
        },
        "consent": {
            "us_ip": {
                "is_coppa": "boolean",
            },
            "ccpa": {
                "status": "number"
            },
            "gdpr": {
                "status": "string",
                "source": "string",
                "message_version": "string",
                "timestamp": "number"
            }
        }
    }
}

ads_v5 = {
    "ads": [
        {
            "placement_reference_id": "string",
            "ad_markup": {
                "id": "string",
                "campaign": "string",
                "app_id": "string",
                "expiry": "number",
                "tpat": {
                    "moat": {
                        "is_enabled": "boolean",
                        "extra_vast": "string"
                    },
                    "clickUrl": "array",
                    "checkpoint.0": "array",
                    "checkpoint.25": "array",
                    "checkpoint.50": "array",
                    "checkpoint.75": "array",
                    "checkpoint.100": "array",
                    "postroll.view": "array",
                    "postroll.click": "array",
                    "video.close": "array",
                    "video.unmute": "array",
                    "video.mute": "array"
                },
                "delay": "number",
                "showClose": "number",
                "showCloseIncentivized": "number",
                "countdown": "number",
                "url": "string",
                "videoWidth": "number",
                "videoHeight": "number",
                "md5": "string",
                "callToActionDest": "string",
                "callToActionUrl": "string",
                "adType": "string",
                "templateURL": "string",
                "templateSettings": {
                    "normal_replacements": {
                        "CLOSE_BUTTON_DELAY_SECONDS": "string",
                        "CTA_BUTTON_TEXT": "string",
                        "INCENTIVIZED_CONTINUE_TEXT": "string",
                        "CTA_BUTTON_BORDER": "string",
                        "CTA_BUTTON_URL": "string",
                        "FULL_CTA": "string",
                        "AUTO_LOCALIZE": "string",
                        "PRIVACY_CONTINUE_TEXT": "string",
                        "START_MUTED": "string",
                        "INCENTIVIZED_TITLE_TEXT": "string",
                        "VUNGLE_PRIVACY_URL": "string",
                        "CTA_BUTTON_BACKGROUND": "string",
                        "INCENTIVIZED_BODY_TEXT": "string",
                        "ACTION_TRACKING": "string",
                        "APP_NAME": "string",
                        "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "string",
                        "CTA_BUTTON_TEXT_COLOR": "string",
                        "PRIVACY_BODY_TEXT": "string",
                        "PRIVACY_CLOSE_TEXT": "string",
                        "APP_DESCRIPTION": "string",
                        "VIDEO_PROGRESS_BAR": "string",
                        "INCENTIVIZED_CLOSE_TEXT": "string"
                    },
                    "cacheable_replacements": {
                        "MAIN_VIDEO": {
                            "url": "string",
                            "extension": "string"
                        },
                        "POWERED_BY_VUNGLE": {
                            "url": "string",
                            "extension": "string"
                        },
                        "APP_ICON": {
                            "url": "string",
                            "extension": "string"
                        },
                        "APP_RATING": {
                            "url": "string",
                            "extension": "string"
                        },
                        "FONT_URL": {
                            "url": "string",
                            "extension": "string"
                        }
                    }
                },
                "templateId": "string",
                "template_type": "string",
                "ad_market_id": "string",
                "chk": "string",
                "retryCount": "number",
                "asyncThreshold": "number",
                "ad_token": "string",
                "video_object_id": "string",
                "requires_sideloading": "boolean",
                "bid_token": "string",
                "data_science_cache": "string",
                "timestamp": "number"
            }
        }
    ]
}

ads_v5_debug = {
    "ads": [
        {
            "placement_reference_id": "string",
            "ad_markup": {
                "id": "string",
                "campaign": "string",
                "app_id": "string",
                "expiry": "number",
                "tpat": {
                    "moat": {
                        "is_enabled": "boolean",
                        "extra_vast": "string"
                    },
                    "clickUrl": "array",
                    "checkpoint.0": "array",
                    "checkpoint.25": "array",
                    "checkpoint.50": "array",
                    "checkpoint.75": "array",
                    "checkpoint.100": "array",
                    "postroll.view": "array",
                    "postroll.click": "array",
                    "video.close": "array",
                    "video.unmute": "array",
                    "video.mute": "array"
                },
                "delay": "number",
                "showClose": "number",
                "showCloseIncentivized": "number",
                "countdown": "number",
                "url": "string",
                "videoWidth": "number",
                "videoHeight": "number",
                "md5": "string",
                "callToActionDest": "string",
                "callToActionUrl": "string",
                "adType": "string",
                "templateURL": "string",
                "templateSettings": {
                    "normal_replacements": {
                        "CLOSE_BUTTON_DELAY_SECONDS": "string",
                        "CTA_BUTTON_TEXT": "string",
                        "INCENTIVIZED_CONTINUE_TEXT": "string",
                        "CTA_BUTTON_BORDER": "string",
                        "CTA_BUTTON_URL": "string",
                        "FULL_CTA": "string",
                        "AUTO_LOCALIZE": "string",
                        "PRIVACY_CONTINUE_TEXT": "string",
                        "START_MUTED": "string",
                        "INCENTIVIZED_TITLE_TEXT": "string",
                        "VUNGLE_PRIVACY_URL": "string",
                        "CTA_BUTTON_BACKGROUND": "string",
                        "INCENTIVIZED_BODY_TEXT": "string",
                        "ACTION_TRACKING": "string",
                        "APP_NAME": "string",
                        "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "string",
                        "CTA_BUTTON_TEXT_COLOR": "string",
                        "PRIVACY_BODY_TEXT": "string",
                        "PRIVACY_CLOSE_TEXT": "string",
                        "APP_DESCRIPTION": "string",
                        "VIDEO_PROGRESS_BAR": "string",
                        "INCENTIVIZED_CLOSE_TEXT": "string"
                    },
                    "cacheable_replacements": {
                        "MAIN_VIDEO": {
                            "url": "string",
                            "extension": "string"
                        },
                        "POWERED_BY_VUNGLE": {
                            "url": "string",
                            "extension": "string"
                        },
                        "APP_ICON": {
                            "url": "string",
                            "extension": "string"
                        },
                        "APP_RATING": {
                            "url": "string",
                            "extension": "string"
                        },
                        "FONT_URL": {
                            "url": "string",
                            "extension": "string"
                        }
                    }
                },
                "templateId": "string",
                "template_type": "string",
                "ad_market_id": "string",
                "chk": "string",
                "retryCount": "number",
                "asyncThreshold": "number",
                "ad_token": "string",
                "video_object_id": "string",
                "requires_sideloading": "boolean",
                "bid_token": "string",
                "data_science_cache": "string",
                "adSource": "string",
                "timestamp": "number"
            }
        }
    ],
    "ext": {
        "debug": {
            "id": "string",
            "timestamp": "string",
            "duration": "number",
            "bid_request": {
                "id": "number",
                "imp": [
                    {
                        "id": "string",
                        "video": {
                            "mimes": [
                                "string"
                            ],
                            "minduration": "number",
                            "maxduration": "number",
                            "protocols": "array",
                            "w": "number",
                            "h": "number",
                            "linearity": "number",
                            "minbitrate": "number",
                            "maxbitrate": "number",
                            "boxingallowed": "number",
                            "playbackmethod": "array",
                            "delivery": "array",
                            "pos": "number",
                            "ext": {}
                        },
                        "displaymanager": "string",
                        "displaymanagerver": "string",
                        "instl": "number",
                        "tagid": "string",
                        "bidfloor": "number",
                        "bidfloorcur": "string",
                        "secure": "number",
                        "ext": {
                            "vungle": {
                                "placement_id": "string",
                                "placement_reference_id": "string",
                                "erpmtarget": "number",
                                "rewarded": "number",
                                "templatetypes": [
                                    "number"
                                ],
                                "allowed_ad_types": [
                                    "number"
                                ],
                                "orientation": "number",
                                "delivery_ordinal": "number",
                                "is_flat_cpm_enabled": "boolean",
                                "cpm_floor": "number",
                                "revenue_share": "number",
                                "serving_cost": "number"
                            },
                            "openrtb25x": {
                                "skip": "number"
                            },
                            "metric": [
                                {
                                    "type": "string",
                                    "vendor": "string"
                                }
                            ]
                        }
                    }
                ],
                "app": {
                    "id": "string",
                    "name": "string",
                    "bundle": "string",
                    "storeurl": "string",
                    "cat": "array",
                    "privacypolicy": "number",
                    "publisher": {
                        "id": "string",
                        "cat": "array"
                    },
                    "keywords": "string",
                    "ext": {
                        "vungle": {
                            "altid": "string",
                            "templates": "array",
                            "wtags": "array",
                            "forceView": "number",
                            "forceViewIncentivized": "number",
                            "wadvid": "array",
                            "badvid": "array",
                            "sdk": {
                                "name": "string",
                                "ver": "string"
                            },
                            "bundleid": "string"
                        }
                    }
                },
                "device": {
                    "ua": "string",
                    "geo": {
                        "lat": "number",
                        "lon": "number",
                        "type": "number",
                        "country": "string",
                        "region": "string",
                        "city": "string",
                        "zip": "string"
                    },
                    "dnt": "number",
                    "lmt": "number",
                    "ip": "string",
                    "devicetype": "number",
                    "make": "string",
                    "model": "string",
                    "os": "string",
                    "osv": "string",
                    "h": "number",
                    "w": "number",
                    "language": "string",
                    "carrier": "string",
                    "connectiontype": "number",
                    "ifa": "string",
                    "dpidsha1": "string",
                    "ext": {
                        "vungle": {
                            "isu": "string",
                            "vungleua": "string",
                            "timezone": "string",
                            "tz": "string",
                            "idfv": "string",
                            "id": "string",
                            "id_source": "string",
                            "marketplace": "string"
                        }
                    }
                },
                "user": {
                    "ext": {
                        "consent": "number"
                    }
                },
                "test": "number",
                "at": "number",
                "tmax": "number",
                "cur": "array",
                "bcat": [
                    "string"
                ],
                "regs": {
                    "ext": {
                        "gdpr": "number"
                    }
                },
                "ext": {
                    "schain": {
                        "complete": "number",
                        "nodes": [
                            {
                                "asi": "string",
                                "sid": "string",
                                "rid": "string",
                                "name": "string",
                                "hp": "string"
                            }
                        ],
                        "ver": "string"
                    }
                }
            }
            },
            "bid_response_details": {
                "string": {
                    "id": "string",
                    "seatbid": [
                        {
                            "bid": [
                                {
                                    "id": "string",
                                    "impid": "string",
                                    "price": "number",
                                    "nurl": "string",
                                    "adm": "string",
                                    "ext": {
                                        "vungle": {
                                            "ad_app_object_id": "string",
                                            "ad_app_store_id": "string",
                                            "vid": "string"
                                        }
                                    },
                                    "adomain": "array",
                                    "bundle": "string",
                                    "iurl": "string",
                                    "cid": "string",
                                    "crid": "string"
                                }
                            ]
                        }
                    ],
                    "bidid": "string",
                    "cur": "string",
                    "ext": {
                        "vungle": {
                            "ignoredevicehistory": "boolean"
                        }
                    }
                },
            "device_info": {
                "id": "string",
                "source": "string"
            }
        }
    }
}


def get_hbp_partner_schema(partner):
    if partner == 'mopub':
        return hbp_mopub
    elif partner == 'max':
        return hbp_max
    elif partner == 'adtiming':
        return hbp_adtiming
    elif partner == 'ironsource':
        return hbp_ironsource
    elif partner == 'ohayoo':
        return hbp_ohayoo
    elif partner == 'saygames':
        return hbp_saygames
    elif partner == 'aequus':
        return hbp_aequus
    elif partner == 'charboost':
        return hbp_charboost
    elif partner == 'unity':
        return hbp_unity
    elif partner == 'fyber':
        return hbp_fyber
    elif partner == 'topon':
        return hbp_topon
    elif partner == 'admob':
        return hbp_admob
    else:
        return hbp_common

hbp_error_realtime = {
    "id": "string",
    "nbr": "number",
    "ext": {
        "err_msg": "string"
    }
}

hbp_error_precache = {
    "id": "string",
    "ext": {
        "err_info": {
            "nsr": "string"
        }
    }
}

hbp_common = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_mopub = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_max = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "burl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_ohayoo = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_saygames = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_aequus = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_adtiming = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_ironsource = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_charboost = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_unity = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_fyber = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_topon = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "nurl": "string",
                    "burl": "string",
                    "lurl": "string",
                    "adm": "string"
                }
            ],
            "seat": "string"
        }
    ]
}

hbp_admob = {
    "id": "string",
    "seatbid": [
        {
            "bid": [
                {
                    "id": "string",
                    "impid": "string",
                    "price": "number",
                    "burl": "string",
                    "adm": "string",
                    "ext": {
                        "event_notification_token": {
                            "payload": "string"
                        },
                        "sdk_rendered_ad": {
                            "id": "string",
                            "rendering_data": "string"
                        },
                        "billing_id": "number"
                    }
                }
            ],
            "seat": "string"
        }
    ],
    "bidid": "string",
    "cur": "string"
}

report_ad_v5_debug = {
    "msg": "string",
    "code": "number",
    "ext": {
        "debug": {
            "device": {
                "id": "string",
                "id_source": "string"
            },
            "idfv_view_message": {
                "device_id": "string",
                "device_id_source": "string",
                "ifa": "string",
                "isu": "string",
                "viewed_timestamp": "number",
                "campaign_id": "string",
                "creative_id": "string",
                "store_id": "string",
                "os": "string",
                "is_external_dsp": "boolean",
                "app_version": "string",
                "level": "string",
                "host": "string",
                "message": "string",
                "timestamp": "string"
            },
            "report_ad_message": {
                "plays": "array",
                "clickedThrough": "array",
                "vungleType": "string",
                "country": "string",
                "region": "string",
                "city": "string",
                "device_language": "string",
                "do_not_track": "boolean",
                "iso2_language": "string",
                "device_user_agent": "string",
                "device_make": "string",
                "device_model": "string",
                "device_height": "number",
                "device_width": "number",
                "os_version": "string",
                "platform": "string",
                "volume": "number",
                "battery_optimization": "boolean",
                "device_id": "string",
                "device_id_source": "string",
                "ifa": "string",
                "isu": "string",
                "timezone": "string",
                "ip_address": "string",
                "connection": "string",
                "network_operator": "string",
                "user_agent": "string",
                "pub_app_id": "string",
                "pub_app_bundle_id": "string",
                "pub_app_market_id": "string",
                "placement_reference_id": "string",
                "ad_app_id": "string",
                "ad_app_object_id": "string",
                "campaign_id": "string",
                "creative_id": "string",
                "event_id": "string",
                "strategy": "string",
                "ad_start_time": "number",
                "ad_duration": "number",
                "ad_clicked": "boolean",
                "ad_size": "string",
                "ad_type": "string",
                "completed_view": "boolean",
                "view": "boolean",
                "ordinal_view": "number",
                "time_to_download": "number",
                "init_time": "number",
                "download_start_time": "number",
                "incentivized": "number",
                "video_id": "string",
                "video_object_id": "string",
                "is_header_bidding": "boolean",
                "hbp_bid_timestamp": "string",
                "campaign_rate": "number",
                "campaign_rate_type": "string",
                "is_demand_third_party": "boolean",
                "scrat_version": "string",
                "scrat_cloud_provider": "string",
                "app_version": "string",
                "level": "string",
                "host": "string",
                "message": "string",
                "timestamp": "string"
            },
            "user_action_message": {
                "event_id": "string",
                "user_actions": "array",
                "app_version": "string",
                "level": "string",
                "host": "string",
                "message": "string",
                "timestamp": "string"
            },
            "view_message": {
                "device_id": "string",
                "device_id_source": "string",
                "ifa": "string",
                "isu": "string",
                "viewed_timestamp": "number",
                "campaign_id": "string",
                "creative_id": "string",
                "store_id": "string",
                "os": "string",
                "is_external_dsp": "boolean",
                "app_version": "string",
                "level": "string",
                "host": "string",
                "message": "string",
                "timestamp": "string"
            }
        }
    }
}

bflat_bid_response = {
    "event_id": "string",
    "bidid": "string",
    "bid_price": "number",
    "ds_ext": {
        "success": "boolean",
        "mu": "number",
        "sigma": "number",
        "win_rate_pred": "number",
        "margin": "number",
        "create_datetime": "string",
        "_bid_price": "number",
        "bidder": "string",
        "experiment_number": "number",
        "weight": "number",
        "bflat_version": "string"
    }
}

recommendation_response = {
    "level": None,
    "recommendations": [
        {
            "rec_id": "string",
            "rec_feature": "string",
            "resource_id": "string",
            "ext": {
                "new_value": "string",
                "old_value": "string"
            }
        }
    ],
    "total_count": "number"
}