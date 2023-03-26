import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
class TestNormalReplacementsTriplePageIdsp(object):
    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4628 [Platform] - Allow/Disallow 3page so creative can be served in either AC format')
    @allure.description('Verify 3 page new tokens')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl5])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_01(self, pub_app_id, placement, sdk_v):
        """

        app setting:
        allow_static_endcard: true
        allow_skip_button: true
        allow_storekit_transition:true
        static_ec_close_button_delay:25

        placement no setting

        advertiser setting:
        THIRD_PAGE_STATIC_ENDCARD: true
        VIDEO_CLOSE_BUTTON_AS_SKIP: true
        SKP_AFTER_VIDEO: true
        """
        adm = {"id": "5ebac6da3fb76400016f26e3",
               "campaign": "5eb9877e136f432531e6f285|5eb9a49a5ddc02539da7c732|test-ads|5ebac6da3fb76400016f26e3",
               "app_id": "$0${\"app_id\":\"5dc44eacf080325a55721f8f\",\"eventID\":\"5ebac6da3fb76400016f26e3\"}",
               "expiry": 1589903706, "tpat": {"moat": {"is_enabled": False, "extra_vast": ""}, "clickUrl": [
                "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4"], "checkpoint.0": [
                "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0",
                "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=start"],
                                              "checkpoint.25": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.25",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=firstQuartile"],
                                              "checkpoint.50": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.5",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=midpoint"],
                                              "checkpoint.75": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.75",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=thirdQuartile"],
                                              "checkpoint.100": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=1",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=complete"],
                                              "postroll.view": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_VIEW",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_view"],
                                              "postroll.click": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_CLICK",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_click"],
                                              "video.close": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=VIDEO_CLOSE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=video_close"],
                                              "video.unmute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=UNMUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=unmute"],
                                              "video.mute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=MUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=mute"],
                                              "closeButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=close_button_click"],
                                              "nearCloseButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=near_close_button_click"],
                                              "download.ctaClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=cta_click"],
                                              "download.fullScreenClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=fullscreen_click"],
                                              "muteButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=mute_button_click"],
                                              "privacyButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=privacy_button_click"],
                                              "storeKitOverlay.autoOpen.storeEndcardTimer": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=store_kit_overlay_auto_open"],
                                              "playableEndcardClick": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=playable_endcard_click"],
                                              "download.ASOIInteraction": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_interaction"],
                                              "download.ASOIComplete": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_complete"]},
               "delay": 0, "showClose": 0, "showCloseIncentivized": 0, "countdown": 0, "url": "", "videoWidth": 0,
               "videoHeight": 0, "md5": "fake_md5",
               "callToActionDest": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4&ppid=313f8c39-0eb3-45ad-88ff-891559d47302",
               "callToActionUrl": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4",
               "adType": "vungle_mraid",
               "templateURL": "https://cdn-lb.vungle.com/templates/88f37b43a983d8700fc2b7a0ca4b5a37.zip",
               "templateSettings": {"normal_replacements": {"APP_DESCRIPTION": "Vungle", "FULL_CTA": "true",
                                                            "INCENTIVIZED_CONTINUE_TEXT": "Continue",
                                                            "PRIVACY_CLOSE_TEXT": "Read Vungle's Privacy Policy",
                                                            "VUNGLE_PRIVACY_URL": "https://privacy.vungle.com/",
                                                            "ACTION_TRACKING": "false", "AUTO_LOCALIZE": "true",
                                                            "CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "INCENTIVIZED_CLOSE_TEXT": "Close",
                                                            "INCENTIVIZED_TITLE_TEXT": "Close this ad?",
                                                            "PRIVACY_BODY_TEXT": "Vungle, Inc. understands the importance of privacy. Vungle operates a mobile ad network (the 'Ad Network' or the 'Services') through which Vungle displays targeted, contextual ads.",
                                                            "PRIVACY_CONTINUE_TEXT": "Close", "THEME": "dark",
                                                            "APP_NAME": "Toss a Coin",
                                                            "CTA_BUTTON_BACKGROUND": "#01b27a",
                                                            "CTA_BUTTON_TEXT": "Download",
                                                            "CTA_BUTTON_URL": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302&durl=https%3A%2F%2Fapp.adjust.com",
                                                            "INCENTIVIZED_BODY_TEXT": "Are you sure you want to skip this ad? You must finish watching to claim your reward.",
                                                            "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "START_MUTED": "true", "VIDEO_PROGRESS_BAR": "true",
                                                            "SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN": "false",
                                                            "SHOW_EC_CLOSE_BUTTON_COUNTDOWN": "true",
                                                            "THIRD_PAGE_STATIC_ENDCARD": "true",
                                                            "VIDEO_CLOSE_BUTTON_AS_SKIP": "true",
                                                            "ENDCARD_CLOSE_BUTTON_AS_SKIP": "true",
                                                            "SKP_AFTER_ENDCARD": "true",
                                                            "SKP_AFTER_VIDEO": "true", "SK_CTA_ONLY": "product_view",
                                                            "SK_ASOI_COMPLETE": "off", "SK_ASOI_AGGRESSIVE": "default",
                                                            "SK_FSC": "overlay_view"}, "cacheable_replacements": {
                   "POWERED_BY_VUNGLE": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/vungle.svg",
                                         "extension": "svg"}, "APP_ICON": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224409047-Toss-a-coin_icon_copy.png",
                       "extension": "png"},
                   "APP_RATING": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/4.5-stars.svg",
                                  "extension": "svg"}, "CAROUSEL_IMAGE_1": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224575863-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_2": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224584145-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_3": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224580023-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"},
                   "MAIN_VIDEO": {"url": "https://cdn-lb.vungle.com/zen/OYOC0703-720x1280-Q2.mp4", "extension": "mp4"},
                   "FONT_URL": {
                       "url": "https://fonts.gstatic.com/s/opensans/v13/cJZKeOuBrn4kERxqtaUH3SZ2oysoEQEeKwjgmXLRnTc.ttf",
                       "extension": "ttf"}}}, "templateId": "58c2f62c34f5e387180003fa",
               "template_type": "multi_page_fullscreen", "ad_market_id": "", "chk": "fake_chk", "retryCount": 3,
               "asyncThreshold": 40,
               "ad_token": "eyJjYW1wYWlnbiI6IjVlYjk4NzdlMTM2ZjQzMjUzMWU2ZjI4NXw1ZWI5YTQ5YTVkZGMwMjUzOWRhN2M3MzJ8ZGF0YXNjaS0tYmxyXzIwMTkxMTAxX3ZpZXdfY3RzXzM2NV9oZHdfbGF0X3NnZF9leHBsb2l0LS1zdWNjZXNzLS1tZWlzdGVyfDVlYmFjNmRhM2ZiNzY0MDAwMTZmMjZlMyJ9",
               "video_object_id": "5eb98e4ba71f20254c64ada9", "requires_sideloading": False,
               "bid_token": "1|af323095b110e88d45cb30ee2b9dc07bf6f4ea17|bqtcdmi70cliis1a9io0", "data_science_cache": ""}
        adm_str = json.dumps(json.dumps(adm))
        over_ride_adm = 'seatbid.0.bid.0.adm@"' + adm_str + '"'
        over_ride_adm = over_ride_adm.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "THIRD_PAGE_STATIC_ENDCARD")
        assert_that(normal_replacements['THIRD_PAGE_STATIC_ENDCARD'], equal_to("true"))
        assert_keys_exist(normal_replacements, "VIDEO_CLOSE_BUTTON_AS_SKIP")
        assert_that(normal_replacements['VIDEO_CLOSE_BUTTON_AS_SKIP'], equal_to("true"))
        assert_that(normal_replacements['ENDCARD_CLOSE_BUTTON_AS_SKIP'], equal_to("true"))
        assert_keys_exist(normal_replacements, "SKP_AFTER_VIDEO")
        assert_that(normal_replacements['SKP_AFTER_VIDEO'], equal_to("true"))
        assert_that(normal_replacements['SKP_AFTER_ENDCARD'], equal_to("true"))
        # assert_keys_exist(normal_replacements, "STATIC_EC_CLOSE_BUTTON_DELAY_SECONDS")
        # assert_that(normal_replacements['STATIC_EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to("25"))
        # verify "static_endcard_served":true in delivery

        # Verified in delivery:
        #   "allow_static_endcard":true,
        #   "allow_skip_button":true,
        #   "allow_storekit_transition":true,
        #   "static_ec_close_button_delay":25

    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4628 [Platform] - Allow/Disallow 3page so creative can be served in either AC format'
                  'PBJ-5194 Support 3 page setting at placement level PRD')
    @allure.description('Verify 3 page new tokens'
                        'Verify that both setting to true on app & placement level')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_02(self, pub_app_id, placement, sdk_v):
        """

        app setting:
        allow_static_endcard: true
        allow_skip_button: true
        allow_storekit_transition:true
        static_ec_close_button_delay:25

        placement setting:
        static_ec_close_button_delay:3

        advertiser setting:
        THIRD_PAGE_STATIC_ENDCARD: true
        VIDEO_CLOSE_BUTTON_AS_SKIP: true
        SKP_AFTER_VIDEO: true
        """
        adm = {
            "adType": "vungle_mraid",
            "app_id": "$0${\"app_id\":\"61658220698efa001620a6b7\",\"eventID\":\"63e04282181aae3d03ed2c53\"}",
            "campaign": "6286221c8f04540017a4f16a|637f7fa661edc400170f63ad|datasci--blr_ohe_ado_explore_genre_coldstart--{\"skan-model\":\"blr_skandwich_v2_1001\"}--success--meister|63e04282181aae3d03ed2c53",
            "callToActionDest": "https://apps.apple.com/us/app/number-match-logic-puzzle/id1545567989?uo=4",
            "callToActionUrl": "https://app.adjust.com/ah0oncr?campaign=NumberMatch_iOS_US_001_18.05.22_6286221c8f04540017a4f16a&adgroup=Toy%20Blast_626841d0d03ae7f7395fdc62&creative=NM_pt_video_177_playable_4.0_241122_3P&s2s=0&idfa=00000000-0000-0000-0000-000000000000&os_name=iOS&gps_adid=&language=en&win_adid=00000000-0000-0000-0000-000000000000&android_id=00000000-0000-0000-0000-000000000000&os_version=16.0.0&impression_id=63e04282181aae3d03ed2c53&vungle_click_id=63e04282181aae3d03ed2c53&cost_type=install&cost_amount=3.94&cost_currency=USD&label=626841d0d03ae7f7395fdc62",
            "expiry": 1676246274,
            "id": "63e04282181aae3d03ed2c53",
            "video_object_id": "633d9d866509a9001721e041",
            "requires_sideloading": False,
            "data_science_cache": "",
            "videoHeight": 0,
            "videoWidth": 0,
            "attribution": {
                "method": "skadnetwork",
                "skadnetwork": {
                    "version": "3.0",
                    "storekit": {
                        "ad_network_id": "gta9lk7p23.skadnetwork",
                        "source_app_id": 890378044,
                        "itunes_item_id": 1545567989,
                        "signature": "MDUCGQCxyDJeqTDCEhO2HQXSaALbk+sdduv4SQcCGA9XGGh6luvU1cpFgJSwYlzzs79OuZsJsQ==",
                        "campaign_id": 8,
                        "nonce": "27614f4c-a81a-4dac-8a24-65fe8d54120d",
                        "timestamp": 1675641474541,
                        "version": "3.0",
                        "fidelity_type": 1
                    },
                    "viewthrough": {
                        "ad_network_id": "gta9lk7p23.skadnetwork",
                        "source_app_id": 890378044,
                        "itunes_item_id": 1545567989,
                        "signature": "MDYCGQDcs0052tGcgNXUO1Iu+8KZ0jJ2TzWNBgACGQC3h+UADvUoGnBSGhe07r7W1Sj+P27czl8=",
                        "campaign_id": 8,
                        "nonce": "27614f4c-a81a-4dac-8a24-65fe8d54120d",
                        "timestamp": 1675641474541,
                        "version": "3.0",
                        "ad_type": "",
                        "ad_description": "",
                        "ad_purchaser_name": "",
                        "fidelity_type": 0
                    }
                }
            },
            "asyncThreshold": 40,
            "chk": "fake_chk",
            "delay": 0,
            "md5": "fake_md5",
            "retryCount": 3,
            "templateId": "6387d4ed6ad1659bdfdff4d4",
            "templateSettings": {
                "normal_replacements": {
                    "APP_DESCRIPTION": "Easybrain",
                    "APP_NAME": "Number Match iOS",
                    "ASOI_SETTINGS": "complete",
                    "CLOSE_BUTTON_DELAY_SECONDS": "0",
                    "CREATIVE_VIEW_TYPE": "video_and_endcard",
                    "CTA_BUTTON_TEXT": "GET",
                    "CTA_BUTTON_URL": "https://apps.apple.com/us/app/number-match-numbers-game/id1545567989?uo=4",
                    "DEVICE_ID": "208077A9-F1BD-4911-AED5-BEC987E41E19",
                    "DEVICE_ID_SOURCE": "IDFV",
                    "DOWNLOAD_BUTTON_DELAY_SECONDS": "3.5",
                    "EC_CLOSE_BUTTON_DELAY_SECONDS": "0",
                    "ENDCARD_CLOSE_BUTTON_AS_SKIP": "true",
                    "ENDCARD_ONLY_DURATION_SECONDS": "25",
                    "FULL_CTA": "true",
                    "HAS_ENDCARD": "true",
                    "INCENTIVIZED_BODY_TEXT": "Are you sure you want to skip this ad? You must finish watching to claim your reward.",
                    "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "0",
                    "INCENTIVIZED_CLOSE_TEXT": "Close",
                    "INCENTIVIZED_CONTINUE_TEXT": "Continue",
                    "INCENTIVIZED_TITLE_TEXT": "Close this ad?",
                    "INTERACTIVE_VIDEO": "false",
                    "MMP_AUTO_CLICK": "false",
                    "RICH_CTA_AUTO": "false",
                    "SESSION_ID": "63e04282181aae3d03ed2c53",
                    "SHOW_EC_CLOSE_BUTTON_COUNTDOWN": "true",
                    "SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN": "false",
                    "SKOVERLAY_AUTO": "true",
                    "SKOVERLAY_DISMISSIBLE": "default",
                    "SKOVERLAY_POSITION": "default",
                    "SKP_AFTER_ENDCARD": "true",
                    "SKP_AFTER_VIDEO": "true",
                    "SK_ASOI_AGGRESSIVE": "default",
                    "SK_ASOI_COMPLETE": "default",
                    "SK_CTA_ONLY": "default",
                    "SK_FSC": "default",
                    "START_MUTED": "false",
                    "THIRD_PAGE_STATIC_ENDCARD": "true",
                    "VIDEO_CLOSE_BUTTON_AS_SKIP": "true",
                    "VIDEO_CLOSE_BUTTON_DELAY_SECONDS": "0",
                    "VIDEO_PROGRESS_BAR": "true",
                    "VIDEO_SHOW_CTA": "false"
                },
                "cacheable_replacements": {
                    "APP_ICON": {
                        "url": "https://cdn-lb.vungle.com/assets/61658220698efa001620a6b7/icon.png",
                        "extension": "png"
                    },
                    "MAIN_VIDEO": {
                        "url": "https://cdn-lb.vungle.com/zen/e7c8222848b95598670161e2bc6d7451.mp4-720x1280-hevc-Q2.mp4",
                        "extension": "mp4"
                    }
                }
            },
            "template_type": "multi_page_fullscreen",
            "templateURL": "https://cdn-lb.vungle.com/templates/custom_creative_bundles/62b32d28114acd0017b258ab/1675343284119/1675343284119-4.1.7.zip",
            "tpat": {
                "moat": {
                    "is_enabled": False,
                    "extra_vast": ""
                },
                "clickUrl": [
                    "https://app.adjust.com/ah0oncr?campaign=NumberMatch_iOS_US_001_18.05.22_6286221c8f04540017a4f16a&adgroup=Toy%20Blast_626841d0d03ae7f7395fdc62&creative=NM_pt_video_177_playable_4.0_241122_3P&s2s=0&idfa=00000000-0000-0000-0000-000000000000&os_name=iOS&gps_adid=&language=en&win_adid=00000000-0000-0000-0000-000000000000&android_id=00000000-0000-0000-0000-000000000000&os_version=16.0.0&impression_id=63e04282181aae3d03ed2c53&vungle_click_id=63e04282181aae3d03ed2c53&cost_type=install&cost_amount=3.94&cost_currency=USD&label=626841d0d03ae7f7395fdc62"
                ],
                "checkpoint.0": [
                    "https://view.adjust.com/impression/ah0oncr?campaign=NumberMatch_iOS_US_001_18.05.22_6286221c8f04540017a4f16a&adgroup=Toy%20Blast_626841d0d03ae7f7395fdc62&creative=NM_pt_video_177_playable_4.0_241122_3P&s2s=0&idfa=00000000-0000-0000-0000-000000000000&os_name=iOS&gps_adid=&language=en&win_adid=00000000-0000-0000-0000-000000000000&android_id=00000000-0000-0000-0000-000000000000&os_version=16.0.0&impression_id=63e04282181aae3d03ed2c53&vungle_click_id=63e04282181aae3d03ed2c53&cost_type=install&cost_amount=3.94&cost_currency=USD&label=626841d0d03ae7f7395fdc62",
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&adv_app_store_id=61658220698efa001620a6b7&placement_type=fullscreen&event_type=start&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "checkpoint.25": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=firstQuartile&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "checkpoint.50": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=midpoint&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "checkpoint.75": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=thirdQuartile&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "checkpoint.100": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=complete&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "postroll.click": [
                    "https://app.adjust.com/ah0oncr?campaign=NumberMatch_iOS_US_001_18.05.22_6286221c8f04540017a4f16a&adgroup=Toy%20Blast_626841d0d03ae7f7395fdc62&creative=NM_pt_video_177_playable_4.0_241122_3P&s2s=0&idfa=00000000-0000-0000-0000-000000000000&os_name=iOS&gps_adid=&language=en&win_adid=00000000-0000-0000-0000-000000000000&android_id=00000000-0000-0000-0000-000000000000&os_version=16.0.0&impression_id=63e04282181aae3d03ed2c53&vungle_click_id=63e04282181aae3d03ed2c53&cost_type=install&cost_amount=3.94&cost_currency=USD&label=626841d0d03ae7f7395fdc62",
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=endcard_click&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "postroll.close": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=endcard_close&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "postroll.view": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=endcard_view&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "video.close": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=video_close&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "video.mute": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=mute&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "video.unmute": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=unmute&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "closeButtonClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=close_button_click&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "nearCloseButtonClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=near_close_button_click&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "download.ctaClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=cta_click&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "download.fullScreenClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=fullscreen_click&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "download.ASOIInteraction": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=asoi_interaction&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "download.ASOIComplete": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=asoi_complete&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "storeKitOverlay.autoOpen.storeEndcardTimer": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=store_kit_overlay_auto_open&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "muteButtonClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=mute_button_click&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "privacyButtonClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=privacy_button_click&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ],
                "playableEndcardClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63e04282181aae3d03ed2c53&cid=6286221c8f04540017a4f16a&crid=637f7fa661edc400170f63ad&ifa=00000000-0000-0000-0000-000000000000&test=0&dsp_version=v3.103.0%2C4.186.0%2CPR-384-b5c8443569afb75fd0cea52d5bf2961da4529d0d&os=iOS&event_type=playable_endcard_click&adv_obj=61658220698efa001620a6b7&adv_market=1545567989&pub_obj=626841d0d03ae7f7395fdc62&pub_market=890378044&skcid=8"
                ]
            }
        }
        adm_str = json.dumps(json.dumps(adm))
        over_ride_adm = 'seatbid.0.bid.0.adm@"' + adm_str + '"'
        over_ride_adm = over_ride_adm.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "THIRD_PAGE_STATIC_ENDCARD")
        assert_that(normal_replacements['THIRD_PAGE_STATIC_ENDCARD'], equal_to("true"))
        assert_keys_exist(normal_replacements, "VIDEO_CLOSE_BUTTON_AS_SKIP")
        assert_that(normal_replacements['VIDEO_CLOSE_BUTTON_AS_SKIP'], equal_to("true"))
        assert_that(normal_replacements['ENDCARD_CLOSE_BUTTON_AS_SKIP'], equal_to("true"))
        assert_keys_exist(normal_replacements, "SKP_AFTER_VIDEO")
        assert_that(normal_replacements['SKP_AFTER_VIDEO'], equal_to("true"))
        assert_that(normal_replacements['SKP_AFTER_ENDCARD'], equal_to("true"))
        assert_keys_exist(normal_replacements, "STATIC_EC_CLOSE_BUTTON_DELAY_SECONDS")
        assert_that(normal_replacements['STATIC_EC_CLOSE_BUTTON_DELAY_SECONDS'], equal_to("3"))

        # verify "static_endcard_served":true in delivery

        # Verified in delivery:
        #   "allow_static_endcard":true,
        #   "allow_skip_button":true,
        #   "allow_storekit_transition":true,
        #   "static_ec_close_button_delay": 3

    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4628 [Platform] - Allow/Disallow 3page so creative can be served in either AC format'
                  'PBJ-5194 Support 3 page setting at placement level PRD')
    @allure.description('Verify 3 page new tokens'
                        'Verify that app=true & placement=false')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl2])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_app_t_placment_f(self, pub_app_id, placement, sdk_v):
        """

        app setting:
        allow_static_endcard: true
        allow_skip_button: true
        allow_storekit_transition:true
        static_ec_close_button_delay:25

        placement setting:
        allow_static_endcard: false
        allow_skip_button: false
        allow_storekit_transition:false
        static_ec_close_button_delay:3

        advertiser setting:
        THIRD_PAGE_STATIC_ENDCARD: true
        VIDEO_CLOSE_BUTTON_AS_SKIP: true
        SKP_AFTER_VIDEO: true
        """
        adm = {"id": "5ebac6da3fb76400016f26e3",
               "campaign": "5eb9877e136f432531e6f285|5eb9a49a5ddc02539da7c732|test-ads|5ebac6da3fb76400016f26e3",
               "app_id": "$0${\"app_id\":\"5dc44eacf080325a55721f8f\",\"eventID\":\"5ebac6da3fb76400016f26e3\"}",
               "expiry": 1589903706, "tpat": {"moat": {"is_enabled": False, "extra_vast": ""}, "clickUrl": [
                "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4"], "checkpoint.0": [
                "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0",
                "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=start"],
                                              "checkpoint.25": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.25",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=firstQuartile"],
                                              "checkpoint.50": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.5",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=midpoint"],
                                              "checkpoint.75": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.75",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=thirdQuartile"],
                                              "checkpoint.100": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=1",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=complete"],
                                              "postroll.view": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_VIEW",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_view"],
                                              "postroll.click": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_CLICK",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_click"],
                                              "video.close": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=VIDEO_CLOSE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=video_close"],
                                              "video.unmute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=UNMUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=unmute"],
                                              "video.mute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=MUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=mute"],
                                              "closeButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=close_button_click"],
                                              "nearCloseButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=near_close_button_click"],
                                              "download.ctaClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=cta_click"],
                                              "download.fullScreenClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=fullscreen_click"],
                                              "muteButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=mute_button_click"],
                                              "privacyButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=privacy_button_click"],
                                              "storeKitOverlay.autoOpen.storeEndcardTimer": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=store_kit_overlay_auto_open"],
                                              "playableEndcardClick": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=playable_endcard_click"],
                                              "download.ASOIInteraction": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_interaction"],
                                              "download.ASOIComplete": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_complete"]},
               "delay": 0, "showClose": 0, "showCloseIncentivized": 0, "countdown": 0, "url": "", "videoWidth": 0,
               "videoHeight": 0, "md5": "fake_md5",
               "callToActionDest": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4&ppid=313f8c39-0eb3-45ad-88ff-891559d47302",
               "callToActionUrl": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4",
               "adType": "vungle_mraid",
               "templateURL": "https://cdn-lb.vungle.com/templates/88f37b43a983d8700fc2b7a0ca4b5a37.zip",
               "templateSettings": {"normal_replacements": {"APP_DESCRIPTION": "Vungle", "FULL_CTA": "true",
                                                            "INCENTIVIZED_CONTINUE_TEXT": "Continue",
                                                            "PRIVACY_CLOSE_TEXT": "Read Vungle's Privacy Policy",
                                                            "VUNGLE_PRIVACY_URL": "https://privacy.vungle.com/",
                                                            "ACTION_TRACKING": "false", "AUTO_LOCALIZE": "true",
                                                            "CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "INCENTIVIZED_CLOSE_TEXT": "Close",
                                                            "INCENTIVIZED_TITLE_TEXT": "Close this ad?",
                                                            "PRIVACY_BODY_TEXT": "Vungle, Inc. understands the importance of privacy. Vungle operates a mobile ad network (the 'Ad Network' or the 'Services') through which Vungle displays targeted, contextual ads.",
                                                            "PRIVACY_CONTINUE_TEXT": "Close", "THEME": "dark",
                                                            "APP_NAME": "Toss a Coin",
                                                            "CTA_BUTTON_BACKGROUND": "#01b27a",
                                                            "CTA_BUTTON_TEXT": "Download",
                                                            "CTA_BUTTON_URL": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302&durl=https%3A%2F%2Fapp.adjust.com",
                                                            "INCENTIVIZED_BODY_TEXT": "Are you sure you want to skip this ad? You must finish watching to claim your reward.",
                                                            "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "START_MUTED": "true", "VIDEO_PROGRESS_BAR": "true",
                                                            "SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN": "false",
                                                            "SHOW_EC_CLOSE_BUTTON_COUNTDOWN": "true",
                                                            "THIRD_PAGE_STATIC_ENDCARD": "true",
                                                            "VIDEO_CLOSE_BUTTON_AS_SKIP": "true",
                                                            "ENDCARD_CLOSE_BUTTON_AS_SKIP": "true",
                                                            "SKP_AFTER_ENDCARD": "true",
                                                            "SKP_AFTER_VIDEO": "true", "SK_CTA_ONLY": "product_view",
                                                            "SK_ASOI_COMPLETE": "off", "SK_ASOI_AGGRESSIVE": "default",
                                                            "SK_FSC": "overlay_view"}, "cacheable_replacements": {
                   "POWERED_BY_VUNGLE": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/vungle.svg",
                                         "extension": "svg"}, "APP_ICON": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224409047-Toss-a-coin_icon_copy.png",
                       "extension": "png"},
                   "APP_RATING": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/4.5-stars.svg",
                                  "extension": "svg"}, "CAROUSEL_IMAGE_1": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224575863-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_2": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224584145-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_3": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224580023-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"},
                   "MAIN_VIDEO": {"url": "https://cdn-lb.vungle.com/zen/OYOC0703-720x1280-Q2.mp4", "extension": "mp4"},
                   "FONT_URL": {
                       "url": "https://fonts.gstatic.com/s/opensans/v13/cJZKeOuBrn4kERxqtaUH3SZ2oysoEQEeKwjgmXLRnTc.ttf",
                       "extension": "ttf"}}}, "templateId": "58c2f62c34f5e387180003fa",
               "template_type": "multi_page_fullscreen", "ad_market_id": "", "chk": "fake_chk", "retryCount": 3,
               "asyncThreshold": 40,
               "ad_token": "eyJjYW1wYWlnbiI6IjVlYjk4NzdlMTM2ZjQzMjUzMWU2ZjI4NXw1ZWI5YTQ5YTVkZGMwMjUzOWRhN2M3MzJ8ZGF0YXNjaS0tYmxyXzIwMTkxMTAxX3ZpZXdfY3RzXzM2NV9oZHdfbGF0X3NnZF9leHBsb2l0LS1zdWNjZXNzLS1tZWlzdGVyfDVlYmFjNmRhM2ZiNzY0MDAwMTZmMjZlMyJ9",
               "video_object_id": "5eb98e4ba71f20254c64ada9", "requires_sideloading": False,
               "bid_token": "1|af323095b110e88d45cb30ee2b9dc07bf6f4ea17|bqtcdmi70cliis1a9io0", "data_science_cache": ""}
        adm_str = json.dumps(json.dumps(adm))
        over_ride_adm = 'seatbid.0.bid.0.adm@"' + adm_str + '"'
        over_ride_adm = over_ride_adm.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "THIRD_PAGE_STATIC_ENDCARD")
        assert_that(normal_replacements['THIRD_PAGE_STATIC_ENDCARD'], equal_to("false"))  # follow placement level setting
        assert_keys_exist(normal_replacements, "VIDEO_CLOSE_BUTTON_AS_SKIP")
        assert_that(normal_replacements['VIDEO_CLOSE_BUTTON_AS_SKIP'], equal_to("false"))
        assert_that(normal_replacements['ENDCARD_CLOSE_BUTTON_AS_SKIP'], equal_to("false"))  # follow placement level setting
        assert_keys_exist(normal_replacements, "SKP_AFTER_VIDEO")
        assert_that(normal_replacements['SKP_AFTER_VIDEO'], equal_to("false"))
        assert_that(normal_replacements['SKP_AFTER_ENDCARD'], equal_to("false"))  # follow placement level setting

        # verify "static_endcard_served":false in delivery

        # Verified in delivery:
        #   "allow_static_endcard":false,
        #   "allow_skip_button":false,
        #   "allow_storekit_transition":false,
        #   "static_ec_close_button_delay": 3

    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4628 [Platform] - Allow/Disallow 3page so creative can be served in either AC format'
                  'PBJ-5194 Support 3 page setting at placement level PRD')
    @allure.description('Verify 3 page new tokens')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_2])
    @pytest.mark.parametrize('placement', [common_test_placement_2])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_3(self, pub_app_id, placement, sdk_v):
        """

        app no setting:


        placement setting:



        advertiser setting:
        THIRD_PAGE_STATIC_ENDCARD: true
        VIDEO_CLOSE_BUTTON_AS_SKIP: true
        SKP_AFTER_VIDEO: true
        """
        adm = {"id": "5ebac6da3fb76400016f26e3",
               "campaign": "5eb9877e136f432531e6f285|5eb9a49a5ddc02539da7c732|test-ads|5ebac6da3fb76400016f26e3",
               "app_id": "$0${\"app_id\":\"5dc44eacf080325a55721f8f\",\"eventID\":\"5ebac6da3fb76400016f26e3\"}",
               "expiry": 1589903706, "tpat": {"moat": {"is_enabled": False, "extra_vast": ""}, "clickUrl": [
                "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4"], "checkpoint.0": [
                "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0",
                "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=start"],
                                              "checkpoint.25": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.25",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=firstQuartile"],
                                              "checkpoint.50": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.5",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=midpoint"],
                                              "checkpoint.75": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.75",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=thirdQuartile"],
                                              "checkpoint.100": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=1",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=complete"],
                                              "postroll.view": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_VIEW",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_view"],
                                              "postroll.click": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_CLICK",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_click"],
                                              "video.close": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=VIDEO_CLOSE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=video_close"],
                                              "video.unmute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=UNMUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=unmute"],
                                              "video.mute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=MUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=mute"],
                                              "closeButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=close_button_click"],
                                              "nearCloseButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=near_close_button_click"],
                                              "download.ctaClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=cta_click"],
                                              "download.fullScreenClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=fullscreen_click"],
                                              "muteButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=mute_button_click"],
                                              "privacyButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=privacy_button_click"],
                                              "storeKitOverlay.autoOpen.storeEndcardTimer": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=store_kit_overlay_auto_open"],
                                              "playableEndcardClick": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=playable_endcard_click"],
                                              "download.ASOIInteraction": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_interaction"],
                                              "download.ASOIComplete": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_complete"]},
               "delay": 0, "showClose": 0, "showCloseIncentivized": 0, "countdown": 0, "url": "", "videoWidth": 0,
               "videoHeight": 0, "md5": "fake_md5",
               "callToActionDest": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4&ppid=313f8c39-0eb3-45ad-88ff-891559d47302",
               "callToActionUrl": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4",
               "adType": "vungle_mraid",
               "templateURL": "https://cdn-lb.vungle.com/templates/88f37b43a983d8700fc2b7a0ca4b5a37.zip",
               "templateSettings": {"normal_replacements": {"APP_DESCRIPTION": "Vungle", "FULL_CTA": "true",
                                                            "INCENTIVIZED_CONTINUE_TEXT": "Continue",
                                                            "PRIVACY_CLOSE_TEXT": "Read Vungle's Privacy Policy",
                                                            "VUNGLE_PRIVACY_URL": "https://privacy.vungle.com/",
                                                            "ACTION_TRACKING": "false", "AUTO_LOCALIZE": "true",
                                                            "CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "INCENTIVIZED_CLOSE_TEXT": "Close",
                                                            "INCENTIVIZED_TITLE_TEXT": "Close this ad?",
                                                            "PRIVACY_BODY_TEXT": "Vungle, Inc. understands the importance of privacy. Vungle operates a mobile ad network (the 'Ad Network' or the 'Services') through which Vungle displays targeted, contextual ads.",
                                                            "PRIVACY_CONTINUE_TEXT": "Close", "THEME": "dark",
                                                            "APP_NAME": "Toss a Coin",
                                                            "CTA_BUTTON_BACKGROUND": "#01b27a",
                                                            "CTA_BUTTON_TEXT": "Download",
                                                            "CTA_BUTTON_URL": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302&durl=https%3A%2F%2Fapp.adjust.com",
                                                            "INCENTIVIZED_BODY_TEXT": "Are you sure you want to skip this ad? You must finish watching to claim your reward.",
                                                            "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "START_MUTED": "true", "VIDEO_PROGRESS_BAR": "true",
                                                            "SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN": "false",
                                                            "SHOW_EC_CLOSE_BUTTON_COUNTDOWN": "true",
                                                            "THIRD_PAGE_STATIC_ENDCARD": "true",
                                                            "VIDEO_CLOSE_BUTTON_AS_SKIP": "true",
                                                            "ENDCARD_CLOSE_BUTTON_AS_SKIP": "true",
                                                            "SKP_AFTER_ENDCARD": "true",
                                                            "SKP_AFTER_VIDEO": "true", "SK_CTA_ONLY": "product_view",
                                                            "SK_ASOI_COMPLETE": "off", "SK_ASOI_AGGRESSIVE": "default",
                                                            "SK_FSC": "overlay_view"}, "cacheable_replacements": {
                   "POWERED_BY_VUNGLE": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/vungle.svg",
                                         "extension": "svg"}, "APP_ICON": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224409047-Toss-a-coin_icon_copy.png",
                       "extension": "png"},
                   "APP_RATING": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/4.5-stars.svg",
                                  "extension": "svg"}, "CAROUSEL_IMAGE_1": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224575863-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_2": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224584145-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_3": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224580023-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"},
                   "MAIN_VIDEO": {"url": "https://cdn-lb.vungle.com/zen/OYOC0703-720x1280-Q2.mp4", "extension": "mp4"},
                   "FONT_URL": {
                       "url": "https://fonts.gstatic.com/s/opensans/v13/cJZKeOuBrn4kERxqtaUH3SZ2oysoEQEeKwjgmXLRnTc.ttf",
                       "extension": "ttf"}}}, "templateId": "58c2f62c34f5e387180003fa",
               "template_type": "multi_page_fullscreen", "ad_market_id": "", "chk": "fake_chk", "retryCount": 3,
               "asyncThreshold": 40,
               "ad_token": "eyJjYW1wYWlnbiI6IjVlYjk4NzdlMTM2ZjQzMjUzMWU2ZjI4NXw1ZWI5YTQ5YTVkZGMwMjUzOWRhN2M3MzJ8ZGF0YXNjaS0tYmxyXzIwMTkxMTAxX3ZpZXdfY3RzXzM2NV9oZHdfbGF0X3NnZF9leHBsb2l0LS1zdWNjZXNzLS1tZWlzdGVyfDVlYmFjNmRhM2ZiNzY0MDAwMTZmMjZlMyJ9",
               "video_object_id": "5eb98e4ba71f20254c64ada9", "requires_sideloading": False,
               "bid_token": "1|af323095b110e88d45cb30ee2b9dc07bf6f4ea17|bqtcdmi70cliis1a9io0", "data_science_cache": ""}
        adm_str = json.dumps(json.dumps(adm))
        over_ride_adm = 'seatbid.0.bid.0.adm@"' + adm_str + '"'
        over_ride_adm = over_ride_adm.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "THIRD_PAGE_STATIC_ENDCARD")
        assert_that(normal_replacements['THIRD_PAGE_STATIC_ENDCARD'], equal_to("true"))
        assert_keys_exist(normal_replacements, "VIDEO_CLOSE_BUTTON_AS_SKIP")
        assert_that(normal_replacements['VIDEO_CLOSE_BUTTON_AS_SKIP'], equal_to("true"))
        assert_that(normal_replacements['ENDCARD_CLOSE_BUTTON_AS_SKIP'], equal_to("true"))
        assert_keys_exist(normal_replacements, "SKP_AFTER_VIDEO")
        assert_that(normal_replacements['SKP_AFTER_VIDEO'], equal_to("true"))
        assert_that(normal_replacements['SKP_AFTER_ENDCARD'], equal_to("true"))
        # Verified  'static_endcard_served'= true in delivery
        # Verified in delivery:
        #   "allow_static_endcard":true (default),
        #   "allow_skip_button":true (default),
        #   "allow_storekit_transition":true (default),
        #   "static_ec_close_button_delay": 16

    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4628 [Platform] - Allow/Disallow 3page so creative can be served in either AC format'
                  'PBJ-5194 Support 3 page setting at placement level PRD')
    @allure.description('Verify 3 page new tokens')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_for_android(self, pub_app_id, placement, sdk_v):
        """
        app no setting:
        allow_static_endcard: true
        allow_skip_button: true
        allow_storekit_transition: true
        static_ec_close_button_delay: 15

        placement setting:
        allow_static_endcard: false
        allow_skip_button: false
        allow_storekit_transition: false
        static_ec_close_button_delay: 3


        advertiser setting:
        THIRD_PAGE_STATIC_ENDCARD: true
        VIDEO_CLOSE_BUTTON_AS_SKIP: true
        SKP_AFTER_VIDEO: true
        """
        adm = {
            "adType": "vungle_mraid",
            "app_id": "$0${\"app_id\":\"62bab038fa8b3132066286ff\",\"eventID\":\"63ea75c33690d6f387112fcd\"}",
            "campaign": "63e241d8dfae4f12b3c40162|63e2406973da5000176807d7|datasci--blr_ohe_ado_explore_staging--{\"skan-model\":null}--success--meister|63ea75c33690d6f387112fcd",
            "callToActionDest": "https://play.google.com/store/apps/details?id=com.os.space.force.galaxy.alien",
            "callToActionUrl": "https://app.appsflyer.com/com.os.space.force.galaxy.alien?pid=vungle_int&af_siteid=6111ed034fa8e426cba05ace&c=Galaxiga_AND_VU_TW_XY_290622&af_cost_model=CPI&af_cost_value=0.15&af_cost_currency=USD&af_c_id=63e241d8dfae4f12b3c40162&af_ad=Galaxiga_EN_ThangVD_01e23_ThePN_01j23_070223&af_ad_id=63e2406973da5000176807d7&af_click_lookback=7d&android_id=&advertising_id=d33fe168-ddfd-434b-bb2d-60eb1f974514&clickid=63ea75c33690d6f387112fcd&vungleappid=62bab038fa8b3132066286ff&af_ref=Vungle_63ea75c33690d6f387112fcd&is_lat=false&af_model=&af_os=11.0.0",
            "expiry": 1676914755,
            "id": "63ea75c33690d6f387112fcd",
            "video_object_id": "63d8f3c98a39b100172dfb6b",
            "requires_sideloading": False,
            "data_science_cache": "",
            "videoHeight": 0,
            "videoWidth": 0,
            "asyncThreshold": 40,
            "chk": "fake_chk",
            "delay": 0,
            "md5": "fake_md5",
            "retryCount": 3,
            "templateId": "6387d4ed6ad1659bdfdff4d4",
            "templateSettings": {
                "normal_replacements": {
                    "APP_DESCRIPTION": "ONESOFT GLOBAL PTE. LTD.",
                    "APP_NAME": "Galaxiga Arcade Shooting Game_Adv_And",
                    "ASOI_SETTINGS": "complete",
                    "CLOSE_BUTTON_DELAY_SECONDS": "10",
                    "CREATIVE_VIEW_TYPE": "video_and_endcard",
                    "CTA_BUTTON_TEXT": "GET",
                    "CTA_BUTTON_URL": "https://play.google.com/store/apps/details?id=com.os.space.force.galaxy.alien",
                    "DEVICE_ID": "d33fe168-ddfd-434b-bb2d-60eb1f974514",
                    "DEVICE_ID_SOURCE": "IFA",
                    "DOWNLOAD_BUTTON_DELAY_SECONDS": "3.5",
                    "EC_CLOSE_BUTTON_DELAY_SECONDS": "0",
                    "ENDCARD_ONLY_DURATION_SECONDS": "25",
                    "FULL_CTA": "true",
                    "INCENTIVIZED_BODY_TEXT": "Are you sure you want to skip this ad? You must finish watching to claim your reward.",
                    "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "0",
                    "INCENTIVIZED_CLOSE_TEXT": "Close",
                    "INCENTIVIZED_CONTINUE_TEXT": "Continue",
                    "INCENTIVIZED_TITLE_TEXT": "Close this ad?",
                    "INTERACTIVE_VIDEO": "true",
                    "MMP_AUTO_CLICK": "false",
                    "RICH_CTA_AUTO": "false",
                    "SESSION_ID": "63ea75c33690d6f387112fcd",
                    "SHOW_EC_CLOSE_BUTTON_COUNTDOWN": "true",
                    "SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN": "false",
                    "SKOVERLAY_AUTO": "false",
                    "SKOVERLAY_DISMISSIBLE": "default",
                    "SKOVERLAY_POSITION": "default",
                    "SK_ASOI_AGGRESSIVE": "default",
                    "SK_ASOI_COMPLETE": "default",
                    "SK_CTA_ONLY": "default",
                    "SK_FSC": "default",
                    "START_MUTED": "false",
                    "SKP_AFTER_VIDEO": "true",
                    "SKP_AFTER_ENDCARD": "true",
                    "THIRD_PAGE_STATIC_ENDCARD": "true",
                    "VIDEO_CLOSE_BUTTON_AS_SKIP": "true",
                    "VIDEO_CLOSE_BUTTON_DELAY_SECONDS": "0",
                    "VIDEO_PROGRESS_BAR": "true",
                    "VIDEO_SHOW_CTA": "false",
                    "ENDCARD_CLOSE_BUTTON_AS_SKIP": "true",
                },
                "cacheable_replacements": {
                    "AC_CONTENT_AD_HTML": {
                        "url": "https://s3.amazonaws.com/vungle2-cdn-prod/assets/62bab038fa8b3132066286ff/89762774a6d88554a9f593d2e16b35b6/ad.html",
                        "extension": "html"
                    },
                    "APP_ICON": {
                        "url": "https://cdn-lb.vungle.com/assets/62bab038fa8b3132066286ff/icon.png",
                        "extension": "png"
                    },
                    "MAIN_VIDEO": {
                        "url": "https://cdn-lb.vungle.com/zen/7a746b7672d70ae5815cb6430d60b934.mp4-720x1280-h264-Q2.mp4",
                        "extension": "mp4"
                    }
                }
            },
            "template_type": "multi_page_fullscreen",
            "templateURL": "https://cdn-lb.vungle.com/templates/custom_creative_bundles/63d8f70377154d00173bcb6f/1675691673073/1675691673073-4.1.7.zip",
            "tpat": {
                "moat": {
                    "is_enabled": False,
                    "extra_vast": ""
                },
                "clickUrl": [
                    "https://app.appsflyer.com/com.os.space.force.galaxy.alien?pid=vungle_int&af_siteid=6111ed034fa8e426cba05ace&c=Galaxiga_AND_VU_TW_XY_290622&af_cost_model=CPI&af_cost_value=0.15&af_cost_currency=USD&af_c_id=63e241d8dfae4f12b3c40162&af_ad=Galaxiga_EN_ThangVD_01e23_ThePN_01j23_070223&af_ad_id=63e2406973da5000176807d7&af_click_lookback=7d&android_id=&advertising_id=d33fe168-ddfd-434b-bb2d-60eb1f974514&clickid=63ea75c33690d6f387112fcd&vungleappid=62bab038fa8b3132066286ff&af_ref=Vungle_63ea75c33690d6f387112fcd&is_lat=false&af_model=&af_os=11.0.0"
                ],
                "checkpoint.0": [
                    "https://impression.appsflyer.com/com.os.space.force.galaxy.alien?pid=vungle_int&af_siteid=6111ed034fa8e426cba05ace&c=Galaxiga_AND_VU_TW_XY_290622&af_cost_model=CPI&af_cost_value=0.15&af_cost_currency=USD&af_c_id=63e241d8dfae4f12b3c40162&af_ad=Galaxiga_EN_ThangVD_01e23_ThePN_01j23_070223&af_ad_id=63e2406973da5000176807d7&af_viewthrough_lookback=24h&android_id=&advertising_id=d33fe168-ddfd-434b-bb2d-60eb1f974514&clickid=63ea75c33690d6f387112fcd&vungleappid=62bab038fa8b3132066286ff&af_ref=Vungle_63ea75c33690d6f387112fcd&is_lat=false&af_model=&af_os=11.0.0",
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&adv_app_store_id=62bab038fa8b3132066286ff&placement_type=fullscreen&event_type=start"
                ],
                "checkpoint.25": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=firstQuartile"
                ],
                "checkpoint.50": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=midpoint"
                ],
                "checkpoint.75": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=thirdQuartile"
                ],
                "checkpoint.100": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=complete"
                ],
                "postroll.click": [
                    "https://app.appsflyer.com/com.os.space.force.galaxy.alien?pid=vungle_int&af_siteid=6111ed034fa8e426cba05ace&c=Galaxiga_AND_VU_TW_XY_290622&af_cost_model=CPI&af_cost_value=0.15&af_cost_currency=USD&af_c_id=63e241d8dfae4f12b3c40162&af_ad=Galaxiga_EN_ThangVD_01e23_ThePN_01j23_070223&af_ad_id=63e2406973da5000176807d7&af_click_lookback=7d&android_id=&advertising_id=d33fe168-ddfd-434b-bb2d-60eb1f974514&clickid=63ea75c33690d6f387112fcd&vungleappid=62bab038fa8b3132066286ff&af_ref=Vungle_63ea75c33690d6f387112fcd&is_lat=false&af_model=&af_os=11.0.0",
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=endcard_click"
                ],
                "postroll.close": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=endcard_close"
                ],
                "postroll.view": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=endcard_view"
                ],
                "video.close": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=video_close"
                ],
                "video.mute": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=mute"
                ],
                "video.unmute": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=unmute"
                ],
                "closeButtonClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=close_button_click"
                ],
                "nearCloseButtonClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=near_close_button_click"
                ],
                "download.ctaClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=cta_click"
                ],
                "download.fullScreenClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=fullscreen_click"
                ],
                "download.ASOIInteraction": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=asoi_interaction"
                ],
                "download.ASOIComplete": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=asoi_complete"
                ],
                "storeKitOverlay.autoOpen.storeEndcardTimer": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=store_kit_overlay_auto_open"
                ],
                "muteButtonClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=mute_button_click"
                ],
                "privacyButtonClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=privacy_button_click"
                ],
                "playableEndcardClick": [
                    "https://tpat.api.vungle.com/v1/tpat?event_id=63ea75c33690d6f387112fcd&cid=63e241d8dfae4f12b3c40162&crid=63e2406973da5000176807d7&ifa=d33fe168-ddfd-434b-bb2d-60eb1f974514&test=0&dsp_version=v3.103.0%2C4.186.0%2Cv1.36.0&os=android&event_type=playable_endcard_click"
                ]
            }
        }
        adm_str = json.dumps(json.dumps(adm))
        over_ride_adm = 'seatbid.0.bid.0.adm@"' + adm_str + '"'
        over_ride_adm = over_ride_adm.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_android(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "THIRD_PAGE_STATIC_ENDCARD")
        assert_that(normal_replacements['THIRD_PAGE_STATIC_ENDCARD'], equal_to("false"))  # follow placement level setting
        assert_keys_exist(normal_replacements, "VIDEO_CLOSE_BUTTON_AS_SKIP")
        assert_that(normal_replacements['VIDEO_CLOSE_BUTTON_AS_SKIP'], equal_to("false"))
        assert_that(normal_replacements['ENDCARD_CLOSE_BUTTON_AS_SKIP'], equal_to("false"))  # follow placement level setting
        assert_keys_exist(normal_replacements, "SKP_AFTER_VIDEO")
        assert_that(normal_replacements['SKP_AFTER_VIDEO'], equal_to("false"))
        assert_that(normal_replacements['SKP_AFTER_ENDCARD'], equal_to("false"))  # follow placement level setting
        # Verified  'static_endcard_served'= true in delivery
        # Verified in delivery:
        #   "allow_static_endcard":true (default),
        #   "allow_skip_button":true (default),
        #   "allow_storekit_transition":true (default),
        #   "static_ec_close_button_delay": 16

    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4628 [Platform] - Allow/Disallow 3page so creative can be served in either AC format')
    @allure.description('Verify 3 page new tokens')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_05(self, pub_app_id, placement, sdk_v):
        """

        app setting:
        allow_static_endcard: true
        allow_skip_button: true
        allow_storekit_transition:true
        static_ec_close_button_delay:25

        placement no setting

        advertiser setting:
        THIRD_PAGE_STATIC_ENDCARD: false
        VIDEO_CLOSE_BUTTON_AS_SKIP: false
        SKP_AFTER_VIDEO: false
        """
        adm = {"id": "5ebac6da3fb76400016f26e3",
               "campaign": "5eb9877e136f432531e6f285|5eb9a49a5ddc02539da7c732|test-ads|5ebac6da3fb76400016f26e3",
               "app_id": "$0${\"app_id\":\"5dc44eacf080325a55721f8f\",\"eventID\":\"5ebac6da3fb76400016f26e3\"}",
               "expiry": 1589903706, "tpat": {"moat": {"is_enabled": False, "extra_vast": ""}, "clickUrl": [
                "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4"], "checkpoint.0": [
                "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0",
                "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=start"],
                                              "checkpoint.25": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.25",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=firstQuartile"],
                                              "checkpoint.50": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.5",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=midpoint"],
                                              "checkpoint.75": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.75",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=thirdQuartile"],
                                              "checkpoint.100": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=1",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=complete"],
                                              "postroll.view": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_VIEW",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_view"],
                                              "postroll.click": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_CLICK",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_click"],
                                              "video.close": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=VIDEO_CLOSE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=video_close"],
                                              "video.unmute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=UNMUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=unmute"],
                                              "video.mute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=MUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=mute"],
                                              "closeButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=close_button_click"],
                                              "nearCloseButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=near_close_button_click"],
                                              "download.ctaClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=cta_click"],
                                              "download.fullScreenClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=fullscreen_click"],
                                              "muteButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=mute_button_click"],
                                              "privacyButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=privacy_button_click"],
                                              "storeKitOverlay.autoOpen.storeEndcardTimer": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=store_kit_overlay_auto_open"],
                                              "playableEndcardClick": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=playable_endcard_click"],
                                              "download.ASOIInteraction": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_interaction"],
                                              "download.ASOIComplete": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_complete"]},
               "delay": 0, "showClose": 0, "showCloseIncentivized": 0, "countdown": 0, "url": "", "videoWidth": 0,
               "videoHeight": 0, "md5": "fake_md5",
               "callToActionDest": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4&ppid=313f8c39-0eb3-45ad-88ff-891559d47302",
               "callToActionUrl": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4",
               "adType": "vungle_mraid",
               "templateURL": "https://cdn-lb.vungle.com/templates/88f37b43a983d8700fc2b7a0ca4b5a37.zip",
               "templateSettings": {"normal_replacements": {"APP_DESCRIPTION": "Vungle", "FULL_CTA": "true",
                                                            "INCENTIVIZED_CONTINUE_TEXT": "Continue",
                                                            "PRIVACY_CLOSE_TEXT": "Read Vungle's Privacy Policy",
                                                            "VUNGLE_PRIVACY_URL": "https://privacy.vungle.com/",
                                                            "ACTION_TRACKING": "false", "AUTO_LOCALIZE": "true",
                                                            "CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "INCENTIVIZED_CLOSE_TEXT": "Close",
                                                            "INCENTIVIZED_TITLE_TEXT": "Close this ad?",
                                                            "PRIVACY_BODY_TEXT": "Vungle, Inc. understands the importance of privacy. Vungle operates a mobile ad network (the 'Ad Network' or the 'Services') through which Vungle displays targeted, contextual ads.",
                                                            "PRIVACY_CONTINUE_TEXT": "Close", "THEME": "dark",
                                                            "APP_NAME": "Toss a Coin",
                                                            "CTA_BUTTON_BACKGROUND": "#01b27a",
                                                            "CTA_BUTTON_TEXT": "Download",
                                                            "CTA_BUTTON_URL": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302&durl=https%3A%2F%2Fapp.adjust.com",
                                                            "INCENTIVIZED_BODY_TEXT": "Are you sure you want to skip this ad? You must finish watching to claim your reward.",
                                                            "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "START_MUTED": "true", "VIDEO_PROGRESS_BAR": "true",
                                                            "SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN": "false",
                                                            "SHOW_EC_CLOSE_BUTTON_COUNTDOWN": "true",
                                                            "THIRD_PAGE_STATIC_ENDCARD": "false",
                                                            "VIDEO_CLOSE_BUTTON_AS_SKIP": "false",
                                                            "SKP_AFTER_VIDEO": "false", "SK_CTA_ONLY": "product_view",
                                                            "SK_ASOI_COMPLETE": "off", "SK_ASOI_AGGRESSIVE": "default",
                                                            "SK_FSC": "overlay_view"}, "cacheable_replacements": {
                   "POWERED_BY_VUNGLE": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/vungle.svg",
                                         "extension": "svg"}, "APP_ICON": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224409047-Toss-a-coin_icon_copy.png",
                       "extension": "png"},
                   "APP_RATING": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/4.5-stars.svg",
                                  "extension": "svg"}, "CAROUSEL_IMAGE_1": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224575863-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_2": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224584145-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_3": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224580023-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"},
                   "MAIN_VIDEO": {"url": "https://cdn-lb.vungle.com/zen/OYOC0703-720x1280-Q2.mp4", "extension": "mp4"},
                   "FONT_URL": {
                       "url": "https://fonts.gstatic.com/s/opensans/v13/cJZKeOuBrn4kERxqtaUH3SZ2oysoEQEeKwjgmXLRnTc.ttf",
                       "extension": "ttf"}}}, "templateId": "58c2f62c34f5e387180003fa",
               "template_type": "multi_page_fullscreen", "ad_market_id": "", "chk": "fake_chk", "retryCount": 3,
               "asyncThreshold": 40,
               "ad_token": "eyJjYW1wYWlnbiI6IjVlYjk4NzdlMTM2ZjQzMjUzMWU2ZjI4NXw1ZWI5YTQ5YTVkZGMwMjUzOWRhN2M3MzJ8ZGF0YXNjaS0tYmxyXzIwMTkxMTAxX3ZpZXdfY3RzXzM2NV9oZHdfbGF0X3NnZF9leHBsb2l0LS1zdWNjZXNzLS1tZWlzdGVyfDVlYmFjNmRhM2ZiNzY0MDAwMTZmMjZlMyJ9",
               "video_object_id": "5eb98e4ba71f20254c64ada9", "requires_sideloading": False,
               "bid_token": "1|af323095b110e88d45cb30ee2b9dc07bf6f4ea17|bqtcdmi70cliis1a9io0", "data_science_cache": ""}
        adm_str = json.dumps(json.dumps(adm))
        over_ride_adm = 'seatbid.0.bid.0.adm@"' + adm_str + '"'
        over_ride_adm = over_ride_adm.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "THIRD_PAGE_STATIC_ENDCARD")
        assert_that(normal_replacements['THIRD_PAGE_STATIC_ENDCARD'], equal_to("false"))
        assert_keys_exist(normal_replacements, "VIDEO_CLOSE_BUTTON_AS_SKIP")
        assert_that(normal_replacements['VIDEO_CLOSE_BUTTON_AS_SKIP'], equal_to("false"))
        assert_keys_exist(normal_replacements, "SKP_AFTER_VIDEO")
        assert_that(normal_replacements['SKP_AFTER_VIDEO'], equal_to("false"))
        assert_keys_not_exist(normal_replacements, "STATIC_EC_CLOSE_BUTTON_DELAY_SECONDS")
        # Verified  no 'static_endcard_served' in delivery

    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4628 [Platform] - Allow/Disallow 3page so creative can be served in either AC format')
    @allure.description('Verify 3 page new tokens')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_instl])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_06(self, pub_app_id, placement, sdk_v):
        """

        app setting:
        allow_static_endcard: true
        allow_skip_button: true
        allow_storekit_transition:true
        static_ec_close_button_delay:25

        placement setting:
        static_ec_close_button_delay:3


        advertiser setting:
        THIRD_PAGE_STATIC_ENDCARD: false
        VIDEO_CLOSE_BUTTON_AS_SKIP: false
        SKP_AFTER_VIDEO: false
        """
        adm = {"id": "5ebac6da3fb76400016f26e3",
               "campaign": "5eb9877e136f432531e6f285|5eb9a49a5ddc02539da7c732|test-ads|5ebac6da3fb76400016f26e3",
               "app_id": "$0${\"app_id\":\"5dc44eacf080325a55721f8f\",\"eventID\":\"5ebac6da3fb76400016f26e3\"}",
               "expiry": 1589903706, "tpat": {"moat": {"is_enabled": False, "extra_vast": ""}, "clickUrl": [
                "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4"], "checkpoint.0": [
                "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0",
                "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=start"],
                                              "checkpoint.25": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.25",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=firstQuartile"],
                                              "checkpoint.50": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.5",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=midpoint"],
                                              "checkpoint.75": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.75",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=thirdQuartile"],
                                              "checkpoint.100": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=1",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=complete"],
                                              "postroll.view": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_VIEW",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_view"],
                                              "postroll.click": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_CLICK",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_click"],
                                              "video.close": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=VIDEO_CLOSE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=video_close"],
                                              "video.unmute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=UNMUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=unmute"],
                                              "video.mute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=MUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=mute"],
                                              "closeButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=close_button_click"],
                                              "nearCloseButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=near_close_button_click"],
                                              "download.ctaClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=cta_click"],
                                              "download.fullScreenClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=fullscreen_click"],
                                              "muteButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=mute_button_click"],
                                              "privacyButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=privacy_button_click"],
                                              "storeKitOverlay.autoOpen.storeEndcardTimer": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=store_kit_overlay_auto_open"],
                                              "playableEndcardClick": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=playable_endcard_click"],
                                              "download.ASOIInteraction": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_interaction"],
                                              "download.ASOIComplete": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_complete"]},
               "delay": 0, "showClose": 0, "showCloseIncentivized": 0, "countdown": 0, "url": "", "videoWidth": 0,
               "videoHeight": 0, "md5": "fake_md5",
               "callToActionDest": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4&ppid=313f8c39-0eb3-45ad-88ff-891559d47302",
               "callToActionUrl": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4",
               "adType": "vungle_mraid",
               "templateURL": "https://cdn-lb.vungle.com/templates/88f37b43a983d8700fc2b7a0ca4b5a37.zip",
               "templateSettings": {"normal_replacements": {"APP_DESCRIPTION": "Vungle", "FULL_CTA": "true",
                                                            "INCENTIVIZED_CONTINUE_TEXT": "Continue",
                                                            "PRIVACY_CLOSE_TEXT": "Read Vungle's Privacy Policy",
                                                            "VUNGLE_PRIVACY_URL": "https://privacy.vungle.com/",
                                                            "ACTION_TRACKING": "false", "AUTO_LOCALIZE": "true",
                                                            "CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "INCENTIVIZED_CLOSE_TEXT": "Close",
                                                            "INCENTIVIZED_TITLE_TEXT": "Close this ad?",
                                                            "PRIVACY_BODY_TEXT": "Vungle, Inc. understands the importance of privacy. Vungle operates a mobile ad network (the 'Ad Network' or the 'Services') through which Vungle displays targeted, contextual ads.",
                                                            "PRIVACY_CONTINUE_TEXT": "Close", "THEME": "dark",
                                                            "APP_NAME": "Toss a Coin",
                                                            "CTA_BUTTON_BACKGROUND": "#01b27a",
                                                            "CTA_BUTTON_TEXT": "Download",
                                                            "CTA_BUTTON_URL": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302&durl=https%3A%2F%2Fapp.adjust.com",
                                                            "INCENTIVIZED_BODY_TEXT": "Are you sure you want to skip this ad? You must finish watching to claim your reward.",
                                                            "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "START_MUTED": "true", "VIDEO_PROGRESS_BAR": "true",
                                                            "SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN": "false",
                                                            "SHOW_EC_CLOSE_BUTTON_COUNTDOWN": "true",
                                                            "THIRD_PAGE_STATIC_ENDCARD": "false",
                                                            "VIDEO_CLOSE_BUTTON_AS_SKIP": "false",
                                                            "SKP_AFTER_VIDEO": "false", "SK_CTA_ONLY": "product_view",
                                                            "SK_ASOI_COMPLETE": "off", "SK_ASOI_AGGRESSIVE": "default",
                                                            "SK_FSC": "overlay_view"}, "cacheable_replacements": {
                   "POWERED_BY_VUNGLE": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/vungle.svg",
                                         "extension": "svg"}, "APP_ICON": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224409047-Toss-a-coin_icon_copy.png",
                       "extension": "png"},
                   "APP_RATING": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/4.5-stars.svg",
                                  "extension": "svg"}, "CAROUSEL_IMAGE_1": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224575863-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_2": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224584145-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_3": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224580023-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"},
                   "MAIN_VIDEO": {"url": "https://cdn-lb.vungle.com/zen/OYOC0703-720x1280-Q2.mp4", "extension": "mp4"},
                   "FONT_URL": {
                       "url": "https://fonts.gstatic.com/s/opensans/v13/cJZKeOuBrn4kERxqtaUH3SZ2oysoEQEeKwjgmXLRnTc.ttf",
                       "extension": "ttf"}}}, "templateId": "58c2f62c34f5e387180003fa",
               "template_type": "multi_page_fullscreen", "ad_market_id": "", "chk": "fake_chk", "retryCount": 3,
               "asyncThreshold": 40,
               "ad_token": "eyJjYW1wYWlnbiI6IjVlYjk4NzdlMTM2ZjQzMjUzMWU2ZjI4NXw1ZWI5YTQ5YTVkZGMwMjUzOWRhN2M3MzJ8ZGF0YXNjaS0tYmxyXzIwMTkxMTAxX3ZpZXdfY3RzXzM2NV9oZHdfbGF0X3NnZF9leHBsb2l0LS1zdWNjZXNzLS1tZWlzdGVyfDVlYmFjNmRhM2ZiNzY0MDAwMTZmMjZlMyJ9",
               "video_object_id": "5eb98e4ba71f20254c64ada9", "requires_sideloading": False,
               "bid_token": "1|af323095b110e88d45cb30ee2b9dc07bf6f4ea17|bqtcdmi70cliis1a9io0", "data_science_cache": ""}
        adm_str = json.dumps(json.dumps(adm))
        over_ride_adm = 'seatbid.0.bid.0.adm@"' + adm_str + '"'
        over_ride_adm = over_ride_adm.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "THIRD_PAGE_STATIC_ENDCARD")
        assert_that(normal_replacements['THIRD_PAGE_STATIC_ENDCARD'], equal_to("false"))
        assert_keys_exist(normal_replacements, "VIDEO_CLOSE_BUTTON_AS_SKIP")
        assert_that(normal_replacements['VIDEO_CLOSE_BUTTON_AS_SKIP'], equal_to("false"))
        assert_keys_exist(normal_replacements, "SKP_AFTER_VIDEO")
        assert_that(normal_replacements['SKP_AFTER_VIDEO'], equal_to("false"))
        assert_keys_not_exist(normal_replacements, "STATIC_CLOSE_BUTTON_DELAY_SECONDS")
        # Verified  no 'static_endcard_served' in delivery
        # Verified in delivery:
        #   "allow_static_endcard":true,
        #   "allow_skip_button":true,
        #   "allow_storekit_transition":true,
        #   "static_ec_close_button_delay": 3

    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4628 [Platform] - Allow/Disallow 3page so creative can be served in either AC format')
    @allure.description('Verify 3 page new tokens')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_1])
    @pytest.mark.parametrize('placement', [common_test_placement_1])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_07(self, pub_app_id, placement, sdk_v):
        """

        app setting:
        allow_static_endcard: false
        allow_skip_button: false
        allow_storekit_transition:false


         placement setting:
         static_ec_close_button_delay:13

        advertiser setting:
        THIRD_PAGE_STATIC_ENDCARD: false
        VIDEO_CLOSE_BUTTON_AS_SKIP: false
        SKP_AFTER_VIDEO: false
        """
        adm = {"id": "5ebac6da3fb76400016f26e3",
               "campaign": "5eb9877e136f432531e6f285|5eb9a49a5ddc02539da7c732|test-ads|5ebac6da3fb76400016f26e3",
               "app_id": "$0${\"app_id\":\"5dc44eacf080325a55721f8f\",\"eventID\":\"5ebac6da3fb76400016f26e3\"}",
               "expiry": 1589903706, "tpat": {"moat": {"is_enabled": False, "extra_vast": ""}, "clickUrl": [
                "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4"], "checkpoint.0": [
                "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0",
                "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=start"],
                                              "checkpoint.25": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.25",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=firstQuartile"],
                                              "checkpoint.50": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.5",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=midpoint"],
                                              "checkpoint.75": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.75",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=thirdQuartile"],
                                              "checkpoint.100": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=1",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=complete"],
                                              "postroll.view": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_VIEW",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_view"],
                                              "postroll.click": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_CLICK",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_click"],
                                              "video.close": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=VIDEO_CLOSE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=video_close"],
                                              "video.unmute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=UNMUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=unmute"],
                                              "video.mute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac6da3fb76400016f26e3&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=MUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac6da3fb76400016f26e3&cid=5eb9877e136f432531e6f285&crid=5eb9a49a5ddc02539da7c732&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=mute"],
                                              "closeButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=close_button_click"],
                                              "nearCloseButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=near_close_button_click"],
                                              "download.ctaClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=cta_click"],
                                              "download.fullScreenClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=fullscreen_click"],
                                              "muteButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=mute_button_click"],
                                              "privacyButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=privacy_button_click"],
                                              "storeKitOverlay.autoOpen.storeEndcardTimer": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=store_kit_overlay_auto_open"],
                                              "playableEndcardClick": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=playable_endcard_click"],
                                              "download.ASOIInteraction": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_interaction"],
                                              "download.ASOIComplete": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_complete"]},
               "delay": 0, "showClose": 0, "showCloseIncentivized": 0, "countdown": 0, "url": "", "videoWidth": 0,
               "videoHeight": 0, "md5": "fake_md5",
               "callToActionDest": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4&ppid=313f8c39-0eb3-45ad-88ff-891559d47302",
               "callToActionUrl": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4",
               "adType": "vungle_mraid",
               "templateURL": "https://cdn-lb.vungle.com/templates/88f37b43a983d8700fc2b7a0ca4b5a37.zip",
               "templateSettings": {"normal_replacements": {"APP_DESCRIPTION": "Vungle", "FULL_CTA": "true",
                                                            "INCENTIVIZED_CONTINUE_TEXT": "Continue",
                                                            "PRIVACY_CLOSE_TEXT": "Read Vungle's Privacy Policy",
                                                            "VUNGLE_PRIVACY_URL": "https://privacy.vungle.com/",
                                                            "ACTION_TRACKING": "false", "AUTO_LOCALIZE": "true",
                                                            "CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "INCENTIVIZED_CLOSE_TEXT": "Close",
                                                            "INCENTIVIZED_TITLE_TEXT": "Close this ad?",
                                                            "PRIVACY_BODY_TEXT": "Vungle, Inc. understands the importance of privacy. Vungle operates a mobile ad network (the 'Ad Network' or the 'Services') through which Vungle displays targeted, contextual ads.",
                                                            "PRIVACY_CONTINUE_TEXT": "Close", "THEME": "dark",
                                                            "APP_NAME": "Toss a Coin",
                                                            "CTA_BUTTON_BACKGROUND": "#01b27a",
                                                            "CTA_BUTTON_TEXT": "Download",
                                                            "CTA_BUTTON_URL": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302&durl=https%3A%2F%2Fapp.adjust.com",
                                                            "INCENTIVIZED_BODY_TEXT": "Are you sure you want to skip this ad? You must finish watching to claim your reward.",
                                                            "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "1",
                                                            "START_MUTED": "true", "VIDEO_PROGRESS_BAR": "true",
                                                            "SHOW_VIDEO_CLOSE_BUTTON_COUNTDOWN": "false",
                                                            "SHOW_EC_CLOSE_BUTTON_COUNTDOWN": "true",
                                                            "THIRD_PAGE_STATIC_ENDCARD": "false",
                                                            "VIDEO_CLOSE_BUTTON_AS_SKIP": "false",
                                                            "SKP_AFTER_VIDEO": "false", "SK_CTA_ONLY": "product_view",
                                                            "SK_ASOI_COMPLETE": "off", "SK_ASOI_AGGRESSIVE": "default",
                                                            "SK_FSC": "overlay_view"}, "cacheable_replacements": {
                   "POWERED_BY_VUNGLE": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/vungle.svg",
                                         "extension": "svg"}, "APP_ICON": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224409047-Toss-a-coin_icon_copy.png",
                       "extension": "png"},
                   "APP_RATING": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/4.5-stars.svg",
                                  "extension": "svg"}, "CAROUSEL_IMAGE_1": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224575863-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_2": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224584145-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"}, "CAROUSEL_IMAGE_3": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb9a49a5ddc02539da7c732/1589224580023-Screen_Shot_2020-05-11_at_12.16.02_PM.png",
                       "extension": "png"},
                   "MAIN_VIDEO": {"url": "https://cdn-lb.vungle.com/zen/OYOC0703-720x1280-Q2.mp4", "extension": "mp4"},
                   "FONT_URL": {
                       "url": "https://fonts.gstatic.com/s/opensans/v13/cJZKeOuBrn4kERxqtaUH3SZ2oysoEQEeKwjgmXLRnTc.ttf",
                       "extension": "ttf"}}}, "templateId": "58c2f62c34f5e387180003fa",
               "template_type": "multi_page_fullscreen", "ad_market_id": "", "chk": "fake_chk", "retryCount": 3,
               "asyncThreshold": 40,
               "ad_token": "eyJjYW1wYWlnbiI6IjVlYjk4NzdlMTM2ZjQzMjUzMWU2ZjI4NXw1ZWI5YTQ5YTVkZGMwMjUzOWRhN2M3MzJ8ZGF0YXNjaS0tYmxyXzIwMTkxMTAxX3ZpZXdfY3RzXzM2NV9oZHdfbGF0X3NnZF9leHBsb2l0LS1zdWNjZXNzLS1tZWlzdGVyfDVlYmFjNmRhM2ZiNzY0MDAwMTZmMjZlMyJ9",
               "video_object_id": "5eb98e4ba71f20254c64ada9", "requires_sideloading": False,
               "bid_token": "1|af323095b110e88d45cb30ee2b9dc07bf6f4ea17|bqtcdmi70cliis1a9io0", "data_science_cache": ""}
        adm_str = json.dumps(json.dumps(adm))
        over_ride_adm = 'seatbid.0.bid.0.adm@"' + adm_str + '"'
        over_ride_adm = over_ride_adm.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "THIRD_PAGE_STATIC_ENDCARD")
        assert_that(normal_replacements['THIRD_PAGE_STATIC_ENDCARD'], equal_to("false"))
        assert_keys_exist(normal_replacements, "VIDEO_CLOSE_BUTTON_AS_SKIP")
        assert_that(normal_replacements['VIDEO_CLOSE_BUTTON_AS_SKIP'], equal_to("false"))
        assert_keys_exist(normal_replacements, "SKP_AFTER_VIDEO")
        assert_that(normal_replacements['SKP_AFTER_VIDEO'], equal_to("false"))
        assert_keys_not_exist(normal_replacements, "STATIC_EC_CLOSE_BUTTON_DELAY_SECONDS")
        # Verified  no 'static_endcard_served' in delivery
        # Verified in delivery:
        #   "allow_static_endcard":false,
        #   "allow_skip_button":false,
        #   "allow_storekit_transition":fasle,
        #   "static_ec_close_button_delay": 13

    @allure.feature('3 page')
    @allure.tag('basic')
    @allure.story('PBJ-4628 [Platform] - Allow/Disallow 3page so creative can be served in either AC format')
    @allure.description('Verify 3 page new tokens')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6'])
    def test_record_publish_setting_sigle_page_01(self, pub_app_id, placement, sdk_v):
        """
        app setting:
        allow_static_endcard: true
        allow_skip_button: true
        allow_storekit_transition:true
        static_ec_close_button_delay:25

        placement no setting

        advertiser setting:
        THIRD_PAGE_STATIC_ENDCARD: true
        ENDCARD_CLOSE_BUTTON_AS_SKIP: true
        SKP_AFTER_ENDCARD: true
        """
        adm = {"id": "5ebac332a0304d0001c04bd9",
               "campaign": "5eb9877e136f432531e6f285|5eb9a49a5ddc02539da7c732|test-ads|5ebac332a0304d0001c04bd9",
               "app_id": "$0${\"app_id\":\"5dc44eacf080325a55721f8f\",\"eventID\":\"5ebac332a0304d0001c04bd9\"}",
               "expiry": 1589902770, "tpat": {"moat": {"is_enabled": False, "extra_vast": ""}, "clickUrl": [
                "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4"], "checkpoint.0": [
                "https://ingest.vungle.com/tpat?event_id=5ebac332a0304d0001c04bd9&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0",
                "https://events.api.vungle.com/v1/tpat?event_id=5ebac332a0304d0001c04bd9&cid=5eb9877e136f432531e6f285&crid=5eb990f85ddc02539da7c715&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=start"],
                                              "checkpoint.25": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac332a0304d0001c04bd9&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.25",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac332a0304d0001c04bd9&cid=5eb9877e136f432531e6f285&crid=5eb990f85ddc02539da7c715&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=firstQuartile"],
                                              "checkpoint.50": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac332a0304d0001c04bd9&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.5",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac332a0304d0001c04bd9&cid=5eb9877e136f432531e6f285&crid=5eb990f85ddc02539da7c715&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=midpoint"],
                                              "checkpoint.75": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac332a0304d0001c04bd9&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=0.75",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac332a0304d0001c04bd9&cid=5eb9877e136f432531e6f285&crid=5eb990f85ddc02539da7c715&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=thirdQuartile"],
                                              "checkpoint.100": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac332a0304d0001c04bd9&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=PERCENTAGE&play_percentage=1",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac332a0304d0001c04bd9&cid=5eb9877e136f432531e6f285&crid=5eb990f85ddc02539da7c715&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=complete"],
                                              "postroll.view": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac332a0304d0001c04bd9&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_VIEW",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac332a0304d0001c04bd9&cid=5eb9877e136f432531e6f285&crid=5eb990f85ddc02539da7c715&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_view"],
                                              "postroll.click": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac332a0304d0001c04bd9&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=POSTROLL_CLICK",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac332a0304d0001c04bd9&cid=5eb9877e136f432531e6f285&crid=5eb990f85ddc02539da7c715&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=endcard_click"],
                                              "video.close": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac332a0304d0001c04bd9&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=VIDEO_CLOSE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac332a0304d0001c04bd9&cid=5eb9877e136f432531e6f285&crid=5eb990f85ddc02539da7c715&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=video_close"],
                                              "video.unmute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac332a0304d0001c04bd9&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=UNMUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac332a0304d0001c04bd9&cid=5eb9877e136f432531e6f285&crid=5eb990f85ddc02539da7c715&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=unmute"],
                                              "video.mute": [
                                                  "https://ingest.vungle.com/tpat?event_id=5ebac332a0304d0001c04bd9&device_id=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&event_type=MUTE",
                                                  "https://events.api.vungle.com/v1/tpat?event_id=5ebac332a0304d0001c04bd9&cid=5eb9877e136f432531e6f285&crid=5eb990f85ddc02539da7c715&ifa=45451fc4-ea5d-42bb-8bfc-ca5b932c0344&test=0&os=iOS&event_type=mute"],
                                              "closeButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=close_button_click"],
                                              "nearCloseButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=near_close_button_click"],
                                              "download.ctaClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=cta_click"],
                                              "download.fullScreenClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=fullscreen_click"],
                                              "muteButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=mute_button_click"],
                                              "privacyButtonClick": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=privacy_button_click"],
                                              "storeKitOverlay.autoOpen.storeEndcardTimer": [
                                                  "http://ingest.vungle.com/tpat?event_id=563d9a4f044e3a06363808af&event_type=store_kit_overlay_auto_open"],
                                              "playableEndcardClick": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=playable_endcard_click"],
                                              "download.ASOIInteraction": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_interaction"],
                                              "download.ASOIComplete": [
                                                  "https://tpat-qa.api.vungle.io/v1/tpat?event_id=60ad042bbee8ba00019f1623&cid=5a7ff1b7860678983e002f5a&crid=5dc3f67e73edaa5a37be263d&ifa=4423dd36-2738-46dc-84d1-02a47f95320d1&test=0&os=iOS&event_type=asoi_complete"]},
               "delay": 0, "showClose": 2, "showCloseIncentivized": 2, "countdown": 0, "url": "", "videoWidth": 0,
               "videoHeight": 0, "md5": "fake_md5", "callToActionDest": "",
               "callToActionUrl": "https://apps.apple.com/us/app/toss-a-coin/id1046740065?uo=4&ppid=313f8c39-0eb3-45ad-88ff-891559d47302",
               "adType": "vungle_mraid",
               "templateURL": "https://cdn-lb.vungle.com/templates/88f37b43a983d8700fc2b7a0ca4b5a37.zip",
               "templateSettings": {"normal_replacements": {"ACTION_TRACKING": "false", "CTA_BUTTON_TEXT": "Download",
                                                            "CTA_BUTTON_URL": "https://apps.apple.com/us/app/angry-birds-2/id880047117?ppid=313f8c39-0eb3-45ad-88ff-891559d47302",
                                                            "INCENTIVIZED_CONTINUE_TEXT": "Continue",
                                                            "PRIVACY_BODY_TEXT": "Vungle, Inc. understands the importance of privacy. Vungle operates a mobile ad network (the 'Ad Network' or the 'Services') through which Vungle displays targeted, contextual ads.",
                                                            "PRIVACY_CLOSE_TEXT": "Read Vungle's Privacy Policy",
                                                            "PRIVACY_CONTINUE_TEXT": "Close",
                                                            "VUNGLE_PRIVACY_URL": "https://privacy.vungle.com/",
                                                            "AUTO_LOCALIZE": "true", "CTA_BUTTON_BACKGROUND": "#01b27a",
                                                            "CTA_BUTTON_TEXT_COLOR": "#fff",
                                                            "INCENTIVIZED_CLOSE_TEXT": "Close",
                                                            "APP_NAME": "Toss a Coin", "VIDEO_PROGRESS_BAR": "true",
                                                            "APP_DESCRIPTION": "Vungle",
                                                            "CLOSE_BUTTON_DELAY_SECONDS": "9999",
                                                            "CTA_BUTTON_BORDER": "transparent", "FULL_CTA": "true",
                                                            "INCENTIVIZED_BODY_TEXT": "Are you sure you want to skip this ad? You must finish watching to claim your reward.",
                                                            "INCENTIVIZED_CLOSE_BUTTON_DELAY_SECONDS": "9999",
                                                            "INCENTIVIZED_TITLE_TEXT": "Close this ad?",
                                                            "SHOW_CLOSE_BUTTON_COUNTDOWN": "true",
                                                            "THIRD_PAGE_STATIC_ENDCARD": "true",
                                                            "ENDCARD_CLOSE_BUTTON_AS_SKIP": "true",
                                                            "SKP_AFTER_ENDCARD": "true", }, "cacheable_replacements": {
                   "FONT_URL": {
                       "url": "https://fonts.gstatic.com/s/opensans/v13/cJZKeOuBrn4kERxqtaUH3SZ2oysoEQEeKwjgmXLRnTc.ttf",
                       "extension": "ttf"},
                   "MAIN_VIDEO": {"url": "https://cdn-lb.vungle.com/zen/OYOC0703-720x1280-Q2.mp4", "extension": "mp4"},
                   "POWERED_BY_VUNGLE": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/vungle.svg",
                                         "extension": "svg"}, "APP_ICON": {
                       "url": "https://cdn-lb.vungle.com/templates/creative_assets/5eb990f85ddc02539da7c715/1589219749753-Toss-a-coin_icon_copy.png",
                       "extension": "png"},
                   "APP_RATING": {"url": "https://cdn-lb.vungle.com/templates/defaults/img/4.5-stars.svg",
                                  "extension": "svg"}}}, "templateId": "57eea7983c5937912400002c",
               "template_type": "single_page_fullscreen", "ad_market_id": "", "chk": "fake_chk", "retryCount": 3,
               "asyncThreshold": 40,
               "ad_token": "eyJjYW1wYWlnbiI6IjVlYjk4NzdlMTM2ZjQzMjUzMWU2ZjI4NXw1ZWI5OTBmODVkZGMwMjUzOWRhN2M3MTV8ZGF0YXNjaS0tYmxyXzIwMTkxMTAxX3ZpZXdfY3RzXzM2NV9oZHdfbGF0X3NnZF9leHBsb2l0LS1zdWNjZXNzLS1tZWlzdGVyfDVlYmFjMzMyYTAzMDRkMDAwMWMwNGJkOSJ9",
               "video_object_id": "5eb98e4ba71f20254c64ada9", "requires_sideloading": False,
               "bid_token": "1|c173ad44d14fe336627037a99a41e47372dff0af|bqtc6cl8r8faq7qbmpcg", "data_science_cache": ""}
        adm_str = json.dumps(json.dumps(adm))
        over_ride_adm = 'seatbid.0.bid.0.adm@"' + adm_str + '"'
        over_ride_adm = over_ride_adm.replace("\"\"", "\"")
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v, debug='jaeger', override_bid_response_any=over_ride_adm))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        response_payload = r.json()

        ad_markup = response_payload['ads'][0]['ad_markup']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']
        assert_keys_exist(normal_replacements, "THIRD_PAGE_STATIC_ENDCARD")
        assert_that(normal_replacements['THIRD_PAGE_STATIC_ENDCARD'], equal_to("true"))
        assert_keys_exist(normal_replacements, "ENDCARD_CLOSE_BUTTON_AS_SKIP")
        assert_that(normal_replacements['ENDCARD_CLOSE_BUTTON_AS_SKIP'], equal_to("true"))
        assert_keys_exist(normal_replacements, "SKP_AFTER_ENDCARD")
        assert_that(normal_replacements['SKP_AFTER_ENDCARD'], equal_to("true"))
        # verify "static_endcard_served":true in delivery

        # Verified in delivery:
        #   "allow_static_endcard":true,
        #   "allow_skip_button":true,
        #   "allow_storekit_transition":true,
        #   "static_ec_close_button_delay":25
