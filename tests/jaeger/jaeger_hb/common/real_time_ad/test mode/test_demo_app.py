from http import HTTPStatus

import allure

from utils.behaviors import request_hbp_with_real_time_token, get_bid_response_obj_from_jaeger_explain
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema, request_payload


@allure.epic('Demo App')
class TestDemoApp(object):

    @allure.feature('Demo App')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue')
    @allure.description('Verify demoApp login endpoint')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', ['DSPKey'])
    def test_demoApp_login_01(self, pub_app_id, placement, sdk_v, demoApp_api_key):
        r = post(jaeger_demoApp_login, json=None,
                 headers=platform_headers(src_ip=us_ip, demoApp_DSPkey=demoApp_api_key,
                                          rtb_selector=None, sdk_version=sdk_v))
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        assert_that(response_payload['is_valid'], equal_to(True))


    @allure.feature('Demo App')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue')
    @allure.description('Verify demoApp login endpoint')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', ['invalid'])
    def test_demoApp_login_02(self, pub_app_id, placement, sdk_v, demoApp_api_key):
        r = post(jaeger_demoApp_login, json=None,
                 headers=platform_headers(debug=None, src_ip=us_ip, demoApp_DSPkey=demoApp_api_key,
                                          rtb_selector=None, sdk_version=sdk_v, demoApp_Explain='demoapp'))
        response_payload = r.json()
        assert_that(response_payload['is_valid'], equal_to(False))
        assert_that(response_payload['reason'], equal_to('DSP Key is invalid.'))

    @allure.feature('Demo App')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue')
    @allure.description('Verify demoApp login endpoint')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', [''])
    def test_demoApp_login_03(self, pub_app_id, placement, sdk_v, demoApp_api_key):
        r = post(jaeger_demoApp_login, json=None,
                 headers=platform_headers(debug='jaeger', src_ip=us_ip, demoApp_DSPkey=demoApp_api_key,
                                          rtb_selector=None, sdk_version=sdk_v))
        response_payload = r.json()
        assert_that(response_payload['is_valid'], equal_to(False))
        assert_that(response_payload['reason'], equal_to('DSP Key is empty, please check the request.'))


    @allure.feature('Demo App')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue')
    @allure.description('Verify demo app key is invalid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', ['121313', '', None])
    def test_generate_api_key_negative_01(self, pub_app_id, placement, partner, sdk_v, demoApp_api_key):
        demoApp_response = test_demoApp_response
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_test_mode_kraken_demo_app,
                                                no_pre_cache_token=True, explain=None,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1,
                                                demoApp_DSPkey=demoApp_api_key, demoApp_Response=demoApp_response,
                                                demoApp_Explain='demoapp')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload, 'nbr')
            assert_that(response_payload['ext']['err_msg'], equal_to("24: NSR: NO_SERV_DEMO_APP_DSP_KEY_FAILURE"))
            assert_keys_not_exist(response_payload['ext'], 'debug')

    @allure.feature('Demo App')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue')
    @allure.description('Verify demo app key valid, but dspReponse is invalid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', ['DSPKey'])
    @pytest.mark.parametrize('demoApp_response', ['', 'test123', None])
    def test_generate_api_key_negative_02(self, pub_app_id, placement, partner, sdk_v, demoApp_api_key, demoApp_response):
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_test_mode_kraken_demo_app,
                                                no_pre_cache_token=True, explain=False,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1,
                                                demoApp_DSPkey=demoApp_api_key, demoApp_Response=demoApp_response,
                                                demoApp_Explain='demoapp')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            assert_keys_exist(response_payload, 'nbr')
            assert_keys_not_exist(response_payload['ext'], 'debug')


    @allure.feature('Demo App')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue')
    @allure.description('Verify demo App does not work for non-test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', ['DSPKey'])
    def test_generate_api_key_negative_04(self, pub_app_id, placement, partner, sdk_v, demoApp_api_key):
        demoApp_response = test_demoApp_response
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_non_test_mode_kraken_demo_app,
                                                no_pre_cache_token=True, explain=None,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=0,
                                                demoApp_DSPkey=demoApp_api_key, demoApp_Response=demoApp_response,
                                                demoApp_Explain='demoapp')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'], not equal_to(50.001))

    @allure.feature('Demo App')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue')
    @allure.description('Verify "demo app key" and "dsp response" is valid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', ['DSPKey'])
    def test_generate_api_key_positive_01(self, pub_app_id, placement, partner, sdk_v, demoApp_api_key):
        demoApp_response = test_demoApp_response
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_test_mode_kraken_demo_app,
                                                no_pre_cache_token=True, explain=False,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1,
                                                demoApp_DSPkey=demoApp_api_key, demoApp_Response=demoApp_response,
                                                demoApp_Explain='demoapp')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_response_crid = bid_info['crid']
            bid_response_cid = bid_info['cid']

            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], '1')
            # decode demo_app_response
            mock_bid_response = json.loads(decode_demo_app_response(demoApp_response))
            mock_bid_info = mock_bid_response['seatbid'][0]['bid'][0]
            mock_bid_crid = mock_bid_info['crid']
            mock_bid_cid = mock_bid_info['cid']
            assert_that(mock_bid_crid in bid_response_crid)
            assert_that(mock_bid_cid in bid_response_cid)



    @allure.feature('Demo App')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue')
    @allure.description('Verify "demo app key" and "dsp reponse" is valid: banner placement')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_banner_placement])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', ['DSPKey'])
    def test_generate_api_key_positive_02(self, pub_app_id, placement, partner, sdk_v, demoApp_api_key):
        banner_response = {
                        "id": "6390b0e2fde0181a2a5377c5",
                        "seatbid": [
                            {
                                "bid": [
                                    {
                                        "id": "6390b0e2fde0181a2a5377c5",
                                        "impid": "1",
                                        "price": 98,
                                        "nurl": "http://kraken-qa1-apiqa-kraken.apiqa.svc.cluster.local:7700/win?price=${AUCTION_PRICE}",
                                        "burl": "http://kraken-qa1-apiqa-kraken.apiqa.svc.cluster.local:7700/burl?aid=kraken-test-aid&impid=kraken-test-impid&price=98.0",
                                        "lurl": "http://kraken-qa1-apiqa-kraken.apiqa.svc.cluster.local:7700/lurl?min=${MIN_BID_TO_WIN}&loss=${AUCTION_LOSS}",
                                        "adm": "<div>\n  <meta charset=\"utf-8\"/>\n  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1,user-scalable=no\"/>\n  <a id=\"exchange-ping-url\" href=\"https://cdn.liftoff.io/tracking_pixel.gif\" style=\"display:none\"></a>\n  <script>window.LIFTOFF_START_TS = Date.now()</script>\n  <script src=\"mraid.js\"></script>\n  <div style=\"display:none\">\n    <img id=\"liftoff-beacon\" src=\"https://impression-east.liftoff.io/vungle/beacon?ad_group_id=134601&amp;channel_id=24&amp;creative_id=171952&amp;auction_id=610b8673cf3ab2a40e8dad28&amp;origin=haggler-vungle067\"/>\n    <script type=\"text/javascript\" src=\"https://pixel.adsafeprotected.com/jload?anId=931342&advId=android&campId=banner-300x250&pubId=2082&chanId=c2774b41830&adsafe_par&uId=94bcc6cfb666440b54520d4c9af04b489ada4a19&impId=v.2_g.134601_a.610b8673cf3ab2a40e8dad28_c.24_t.ua_u.94bcc6cfb666440b&dealId=1041&bundleId=com.snaptube.premium\"></script><noscript><img src=\"https://pixel.adsafeprotected.com/?anId=931342&advId=android&campId=banner-300x250&pubId=2082&chanId=c2774b41830&adsafe_par&uId=94bcc6cfb666440b54520d4c9af04b489ada4a19&impId=v.2_g.134601_a.610b8673cf3ab2a40e8dad28_c.24_t.ua_u.94bcc6cfb666440b&dealId=1041&bundleId=com.snaptube.premium\" height=\"1\" width=\"1\" alt=\"\"></noscript>\n  </div>\n  <script src=\"https://cdn.liftoff.io/resources/polyfills-9146e55c725659011766.js\"></script>\n  <link href=\"https://cdn.liftoff.io/resources/liftoff-7971be576fd006dbabd5.css\" rel=\"stylesheet\"/>\n  <script src=\"https://cdn.liftoff.io/resources/liftoff-2cf307b4df39787ef4aa.js\"></script>\n  <link href=\"https://cdn.liftoff.io/resources/panning-f69f751147652a223ac7.css\" rel=\"stylesheet\"/>\n  <link href=\"https://cdn.liftoff.io/resources/generic-cta-aadd6ba00a1e81026cc3.css\" rel=\"stylesheet\"/>\n  <script src=\"https://cdn.liftoff.io/resources/panning-59789dd79590b7feffd6.js\"></script>\n  <script src=\"https://cdn.liftoff.io/resources/generic-cta-17799434eaed59a5a9b2.js\"></script>\n  <script src=\"https://cdn.liftoff.io/resources/simple-text-53340ed52ae6b8d91e07.js\"></script>\n  <script src=\"https://cdn.liftoff.io/resources/simple-image-f5fb66d2aebd9687437b.js\"></script>\n  <script>\n  Liftoff.init(JSON.parse(decodeURIComponent('{\"creative_policy\":{\"show_chinese_watermark\":false,\"show_ad_choices\":false,\"use_custom_close\":false,\"audio_policy\":\"always-mute\",\"remove_ad_wrapper\":false,\"russian_age_rating\":null,\"close_delay\":0,\"add_border\":false,\"animation_duration_limit\":0,\"block_strobing\":false,\"block_notifications\":false},\"products\":%5B%5D,\"enable_html_return\":false,\"bid_context\":{\"normalized_language\":\"ar\",\"creative_id\":171952,\"width\":300,\"source_app_name\":\"Snaptube\",\"is_reengagement\":false,\"source_app_id\":\"com.snaptube.premium\",\"is_interstitial\":false,\"exchange\":\"vungle\",\"ab_tests\":%5B\"ias-tracking-experiment\",\"vast-html-endscreen-control\",\"applovin-native-browser-control\",\"admarkup-madlib-html-refactoring-control\"%5D,\"platform\":\"android\",\"height\":250},\"html_return_delay\":\"5000\",\"click_config\":{\"clickthrough_url\":{\"url\":\"https://play.google.com/store/apps/details%3Fid=com.azarlive.android%26referrer=utm_source%253DLiftoff%2526utm_campaign%253DTest%252BCampaign%2526utm_content%253DTest%252BSource%252BApp_123456789%2526utm_term%253DTest%252BCreative\",\"type\":2},\"click_tracking_urls\":%5B{\"url\":\"https://click.liftoff.io/v1/campaign_click/_V3eb5Asmplhu-oO-bVR_7bYWDJv9mr9stJN3xUFQDeysfFkz8js76ynj_YvuUnFizTBFVsaCjZcNSFlRjYp7SiaYSeROXhD3bYxvaaLqjxjgUckrgCQTilJkET7mBhjNMUfQ2sx2tF0ghkGJ_BAo9epGQ2vCR3-0OH016uYzxviZFVtM558Wyj401jSJAwn8M4HxeXiHoUPLTsgP7LPSbavyreCOyyR8WLAO8WNtgVVtYokwBUHFEmiHviXDhsHERRqj1BpT7t7CIAy7NjUQvHtAXUaWYeL9vj-PiJCdfP_U1O8xvRpMIjTHkF0gDv4Lpv2YWSSUyeMjG8P5mdCYUm_blCvJHWWX4Cv0j9g90z43m6OdxePN4hOVo3FbHBUt2ENYJIpgQFT0iEaaGmv5BkkJjQxplGF5202Kq6uv863b2zFvAyJQdjPcAedPThA3PhevS8QDukD7Jn4e7gLGVQ17wR7gJsgH_KU3yww8X7EI5Ti5yGeeqZ0UKQiFpOkf-LaJvAqtI9L6Zz367tZUC2YyUnRt44F0B0Drh4\",\"type\":1}%5D},\"enable_logging\":false,\"logging_endpoint\":\"https://adexp.liftoff.io\",\"event_tracking_param\":\"acb220CMmbCBIYNjEwYjg2NzNjZjNhYjJhNDBlOGRhZDI4GLjilKixLyAYKLC_CjCiEDoUY29tLnNuYXB0dWJlLnByZW1pdW1CF2lhcy10cmFja2luZy1leHBlcmltZW50Qht2YXN0LWh0bWwtZW5kc2NyZWVuLWNvbnRyb2xCH2FwcGxvdmluLW5hdGl2ZS1icm93c2VyLWNvbnRyb2xCKGFkbWFya3VwLW1hZGxpYi1odG1sLXJlZmFjdG9yaW5nLWNvbnRyb2xKCmQ4MTI5YmY1ZTRQAloDVFVSYAJoBHIJdXMtZWFzdC0xgAEYkgECYXKYAQKhATMzMzMzM7M_qgEHMzAweDI1MLIBF1ZpZGVvIFBsYXllcnMgJiBFZGl0b3JzugEIU25hcHR1YmXCARttYWRsaWItNGU5ZTVhNjYyMmZmOGI2NTAyODTSAQUzNDA0NQ\",\"app_icon\":\"https://cdn.liftoff.io/customers/1041/creatives/2082-icon-250x250.png\"}')), {\n    image_originals: {\"577484\":{\"id\":577484,\"image_versions\":[{\"id\":1135349,\"version-id\":3,\"version-name\":\"lambda_png\",\"duration\":0.0,\"public-url\":\"https://cdn.liftoff.io/customers/45d4b09eba/image/lambda_png/1cefe6db1d8970ec12ab.png\",\"width\":230,\"height\":230,\"mime-type\":\"image/png\",\"filesize\":7161}]},\"621405\":{\"id\":621405,\"image_versions\":[{\"id\":2509805,\"version-id\":4,\"version-name\":\"lambda_jpg_65\",\"duration\":0.0,\"public-url\":\"https://cdn.liftoff.io/customers/45d4b09eba/image/lambda_jpg_65/6a47268c12b372f0d33c.jpg\",\"width\":2071,\"height\":627,\"mime-type\":\"image/jpeg\",\"filesize\":188574}]}},\n    video_originals: {},\n  }, JSON.parse(decodeURIComponent('{\"scenes\":%5B{\"id\":\"main\",\"layoutID\":52,\"transition\":null,\"layoutContent\":{\"css\":{\"CTA\":{\"font-size\":\"12px\"},\"Copy\":{\"z-index\":\"2\",\"font-size\":\"14px\",\"text-align\":\"center\",\"font-weight\":\"300\",\"line-height\":\"17px\",\"letter-spacing\":\"0.2px\"},\"Icon\":{\"overflow\":\"hidden\",\"border-radius\":\"25%25\"},\"Name\":{\"padding\":\"0\",\"font-size\":\"22px\",\"margin-top\":\"5px\",\"font-weight\":\"500\",\"line-height\":\"20px\"},\"Caption\":{\"color\":\"%23666\",\"font-size\":\"12px\",\"margin-top\":\"5px\"},\"Foreground\":{\"pointer-events\":\"none\"},\"CONTAINER - Header\":{\"z-index\":\"2\"}},\"containers\":%5B{\"id\":\"Background\",\"children\":%5B%5D},{\"id\":\"CONTAINER\",\"children\":%5B{\"id\":\"CONTAINER - Header\",\"children\":%5B{\"id\":\"Icon\",\"children\":%5B%5D},{\"id\":\"CONTAINER - Name\",\"children\":%5B{\"id\":\"Name\",\"children\":%5B%5D},{\"id\":\"Caption\",\"children\":%5B%5D},{\"id\":\"CTA\",\"children\":%5B%5D}%5D}%5D},{\"id\":\"Copy\",\"children\":%5B%5D},{\"id\":\"CONTAINER - Main Content\",\"children\":%5B{\"id\":\"Main Content - Background\",\"children\":%5B%5D},{\"id\":\"Main Content\",\"children\":%5B%5D}%5D}%5D},{\"id\":\"Foreground\",\"children\":%5B%5D}%5D,\"constraints\":{\"CONTAINER - Main Content\":{\"top\":{\"edge\":\"bottom\",\"anchor\":\"Copy\",\"distance\":\"4px\"},\"left\":0,\"right\":0,\"bottom\":0},\"Copy\":{\"top\":{\"edge\":\"bottom\",\"anchor\":\"CONTAINER - Header\",\"distance\":\"4px\"},\"left\":\"8px\",\"right\":\"8px\",\"centerHorizontal\":true},\"Main Content - Background\":{\"top\":0,\"left\":0,\"right\":0,\"bottom\":0},\"CTA\":{\"right\":0,\"bottom\":\"2.5px\",\"height\":\"25px\"},\"Icon\":{\"top\":0,\"left\":0,\"width\":\"50px\",\"matchHeightToWidth\":true},\"CONTAINER - Name\":{\"top\":0,\"left\":{\"edge\":\"right\",\"anchor\":\"Icon\",\"distance\":\"8px\"},\"right\":0,\"bottom\":0},\"Foreground\":{\"top\":0,\"left\":0,\"right\":0,\"bottom\":0},\"CONTAINER - Header\":{\"top\":\"8px\",\"left\":\"8px\",\"right\":\"8px\",\"height\":\"50px\"},\"Name\":{\"top\":0,\"left\":0,\"height\":\"20px\"},\"Main Content\":{\"top\":0,\"left\":0,\"right\":0,\"bottom\":0},\"Background\":{\"top\":0,\"left\":0,\"right\":0,\"bottom\":0},\"CONTAINER\":{\"top\":0,\"left\":0,\"right\":0,\"bottom\":0},\"Caption\":{\"top\":{\"edge\":\"bottom\",\"anchor\":\"Name\",\"distance\":0},\"left\":0,\"right\":{\"edge\":\"left\",\"anchor\":\"CTA\",\"distance\":\"8px\"},\"bottom\":0}},\"clickTargets\":%5B%5D,\"coordination\":%5B%5D,\"componentParams\":{\"CTA\":{\"params\":{\"blink\":{\"type\":\"boolean\",\"value\":null},\"uaCTA\":{\"type\":\"text\",\"value\":\"Y%C3%9CKLE\",\"metadata\":{\"languageID\":64,\"englishWord\":\"INSTALL\"}},\"abrCTA\":{\"type\":\"text\",\"value\":\"A%C3%87\",\"metadata\":{\"languageID\":64,\"englishWord\":\"OPEN\"}},\"activationCTA\":{\"type\":\"text\",\"value\":null},\"animateOnClickAnywhere\":{\"type\":\"boolean\",\"value\":false}},\"component\":\"generic-cta\"},\"Copy\":{\"params\":{\"text\":{\"type\":\"text\",\"value\":null},\"maxLines\":{\"type\":\"number\",\"value\":null}},\"component\":\"simple-text\"},\"Icon\":{\"params\":{\"hpos\":{\"type\":\"text\",\"value\":\"center\"},\"size\":{\"type\":\"text\",\"value\":\"contain\"},\"vpos\":{\"type\":\"text\",\"value\":\"center\"},\"image\":{\"type\":\"image_original\",\"value\":577484}},\"component\":\"simple-image\"},\"Name\":{\"params\":{\"text\":{\"type\":\"text\",\"value\":\"Azar\"},\"maxLines\":{\"type\":\"number\",\"value\":1}},\"component\":\"simple-text\"},\"Caption\":{\"params\":{\"text\":{\"type\":\"text\",\"value\":\"Canl%C4%B1 Video Sohbette Tan%C4%B1%C5%9F\"},\"maxLines\":{\"type\":\"number\",\"value\":1}},\"component\":\"simple-text\"},\"Main Content - Background\":{\"params\":{\"speed\":{\"type\":\"number\",\"value\":13},\"images\":{\"type\":\"array\",\"value\":%5B{\"image\":{\"type\":\"image_original\",\"value\":621405}}%5D},\"direction\":{\"type\":\"text\",\"value\":\"left\"}},\"component\":\"panning\"}}}}%5D}')));\n  </script>\n</div>\n",
                                        "adomain": [
                                            "domain1.com"
                                        ],
                                        "bundle": "com.azarlive.android",
                                        "crid": "demoAppbanner",
                                        "cat": [
                                            "Movies",
                                            "Music"
                                        ],
                                        "api": 7,
                                        "ext": {
                                            "skadn": {
                                                "version": "2.0",
                                                "network": "cDkw7geQsH.skadnetwork",
                                                "campaign": "45",
                                                "itunesitem": "880047117",
                                                "nonce": "473b1a16-b4ef-43ad-9591-fcf3aefa82a7",
                                                "sourceapp": "123456789",
                                                "timestamp": "1594406341",
                                                "signature": "MEQCIEQlmZRNfYzK",
                                                "ext": {}
                                            },
                                            "deeplink": "zalora://my//seg_s/m/",
                                            "imptrackers": [
                                                "https://us-event.app-install.bid/rtb/impr?id=123",
                                                "https://us-event.app-install.bid/rtb/impr?id=YnRyAgMAAAF6dACeAwAGRREAAAAwHZlv1LjyQ6eKNFvVILh75gACdXMB&price=${AUCTION_PRICE}"
                                            ]
                                        }
                                    }
                                ]
                            }
                        ],
                        "cur": "USD"
                    }
        mock_bid_response = encode_demo_app_response(banner_response).decode("utf-8")
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_test_mode_kraken_demo_app,
                                                no_pre_cache_token=True, explain=False,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1,
                                                demoApp_DSPkey=demoApp_api_key, demoApp_Response=mock_bid_response,
                                                demoApp_Explain='demoapp')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_response_crid = bid_info['crid']
            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], '1')
            # decode demo_app_response
            mock_bid_response = json.loads(decode_demo_app_response(mock_bid_response))
            mock_bid_info = mock_bid_response['seatbid'][0]['bid'][0]
            mock_bid_crid = mock_bid_info['crid']
            assert_that(mock_bid_crid in bid_response_crid)


    @allure.feature('Demo App')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue')
    @allure.description('Verify demo app key belongs to other account')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_other_account])
    @pytest.mark.parametrize('placement', [common_test_other_placement])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', ['12d5ee11c77bfa85213f3bc055d8df6b'])
    def test_generate_api_key_positive_03(self, pub_app_id, placement, partner, sdk_v, demoApp_api_key):
        demoApp_response = test_demoApp_response
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_test_mode_kraken_demo_app,
                                                no_pre_cache_token=True, explain=False,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1,
                                                demoApp_DSPkey=demoApp_api_key, demoApp_Response=demoApp_response,
                                                demoApp_Explain='demoapp')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_response_crid = bid_info['crid']
            bid_response_cid = bid_info['cid']

            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], '1')
            # decode demo_app_response
            mock_bid_response = json.loads(decode_demo_app_response(demoApp_response))
            mock_bid_info = mock_bid_response['seatbid'][0]['bid'][0]
            mock_bid_crid = mock_bid_info['crid']
            mock_bid_cid = mock_bid_info['cid']
            assert_that(mock_bid_crid in bid_response_crid)
            assert_that(mock_bid_cid in bid_response_cid)


    @allure.feature('Demo App')
    @allure.tag('normal', 'v1.256.0')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue')
    @allure.description('Verify other kraken endpoint can not serve demoAPP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', ['DSPKey'])
    def test_other_endpoint_cant_serve_demoapp(self, pub_app_id, placement, partner, sdk_v, demoApp_api_key):
        demoApp_response = test_demoApp_response
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=ext_test_mode_kraken_rtb_ids_vast,
                                                no_pre_cache_token=True, explain=False,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1,
                                                demoApp_DSPkey=demoApp_api_key, demoApp_Response=demoApp_response,
                                                demoApp_Explain='demoapp')
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            ext = response_payload['ext']
            assert_keys_exist(ext, 'err_msg')



    @allure.feature('Demo App')
    @allure.tag('normal')
    @allure.story('PBJ-4613 Demo App Development - Generate eDSP API Key'
                  'PBJ-4591 Demo App Development'
                  'PBJ-5192 Fix kraken issue'
                  'PBJ-5179 [Kraken] One service for idsp & edsp')
    @allure.description('Verify "demo app key" and "dsp response" is valid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_real_time_placement])
    @pytest.mark.parametrize('partner', ['max'])
    @pytest.mark.parametrize('sdk_v', [test_default_real_time_sdk_version])
    @pytest.mark.parametrize('demoApp_api_key', ['DSPKey'])
    def test_kranken_serve_as_demoApp(self, pub_app_id, placement, partner, sdk_v, demoApp_api_key):
        demoApp_response = test_demoApp_response
        info = request_hbp_with_real_time_token(partner, 11, pub_app_id=pub_app_id, placement_ref_id=placement,
                                                rtb=test_mode_kraken_default_demoApp,
                                                no_pre_cache_token=True, explain=True,
                                                test_device_id=gen_device_id(), sdk_v=sdk_v, is_test=1,
                                                demoApp_DSPkey=demoApp_api_key, demoApp_Response=demoApp_response)
        if info['is_hbp_responded_200']:
            response_payload = info['hbp_response']
            bid_info = response_payload['seatbid'][0]['bid'][0]
            bid_response_crid = bid_info['crid']
            bid_response_cid = bid_info['cid']

            assert_valid_schema(response_payload, response_schema.get_hbp_partner_schema(partner))
            assert_that(bid_info['price'], equal_to(50.001))
            assert_that(response_payload['ext']['test'], '1')
            # decode demo_app_response
            mock_bid_response = json.loads(decode_demo_app_response(demoApp_response))
            mock_bid_info = mock_bid_response['seatbid'][0]['bid'][0]
            mock_bid_crid = mock_bid_info['crid']
            mock_bid_cid = mock_bid_info['cid']
            assert_that(mock_bid_crid in bid_response_crid)
            assert_that(mock_bid_cid in bid_response_cid)
