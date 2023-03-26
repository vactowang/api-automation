import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.common import *
from utils.assertions import *
from settings import *
from data import response_schema


@allure.epic('jaeger v5')
@allure.feature('basic')
class TestTpat(object):

    @allure.tag('basic', 'smoke')
    @allure.story('tpat')
    @allure.description('Verify tpat moat keys from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_moat_keys(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            tpat = ad_markup['tpat']

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(str(tpat['moat']).count('is_enabled'), equal_to(1))
            assert_that(str(tpat['moat']).count('extra_vast'), equal_to(1))

    @allure.tag('basic', 'smoke')
    @allure.story('tpat')
    @allure.description('Verify tpat click URL from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_click_url(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            tpat = ad_markup['tpat']

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(str(tpat['clickUrl'][0]).count('http'), equal_to(1))

    @allure.tag('basic', 'smoke')
    @allure.story('tpat')
    @allure.description('Verify tpat check point URLs from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_check_point_url(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            tpat = ad_markup['tpat']

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(str(tpat['checkpoint.0'][0]).count('http'), equal_to(1))
            assert_that(str(tpat['checkpoint.25'][0]).count('http'), equal_to(1))
            assert_that(str(tpat['checkpoint.50'][0]).count('http'), equal_to(1))
            assert_that(str(tpat['checkpoint.75'][0]).count('http'), equal_to(1))
            assert_that(str(tpat['checkpoint.100'][0]).count('http'), equal_to(1))

    @allure.tag('basic', 'smoke')
    @allure.story('tpat')
    @allure.description('Verify tpat post roll URLs from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_post_roll_url(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            tpat = ad_markup['tpat']

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(str(tpat['postroll.view'][0]).count('http'), equal_to(1))
            assert_that(str(tpat['postroll.click'][0]).count('http'), equal_to(1))

    @allure.tag('basic', 'smoke')
    @allure.story('tpat')
    @allure.description('Verify tpat video control URLs from ads response')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    def test_video_ctl_url(self, pub_app_id):
        req = request_payload.jaeger_v5_ios(pub_app_id, 'DEFAULT02021')
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers())

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        if 'sleep' not in ad_markup:
            tpat = ad_markup['tpat']

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)
            assert_that(str(tpat['video.close'][0]).count('http'), equal_to(1))
            assert_that(str(tpat['video.unmute'][0]).count('http'), equal_to(1))
            assert_that(str(tpat['video.mute'][0]).count('http'), equal_to(1))

    @allure.feature('creative view')
    @allure.tag('normal', 'test_mode', 'v1.153.0')
    @allure.story('PBJ-793 CreativeView in VAST Not Being Fired')
    @allure.description('Verify the creativeView from checkpoint.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_check_point_url_creative_view(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        flag = 0
        for item in tpat['checkpoint.0']:
            if 'creativeview' in item:
                flag = 1
        assert_that(flag, equal_to(1))

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.157.0')
    @allure.story('PBJ-2596 Jaeger should ingest tpat urls')
    @allure.description('Verify the tpat url from event urls')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    def test_tpat_url_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        result = []
        for key, value in tpat.items():
            if key == 'moat':
                continue
            for url in value:
                if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                    result.append(key)
                    break
        assert_that(result, equal_to(['clickUrl', 'checkpoint.0', 'checkpoint.25', 'checkpoint.50', 'checkpoint.75',
                                      'checkpoint.100', 'postroll.view', 'video.close', 'video.unmute', 'video.mute']))

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.157.0', 'test_mode')
    @allure.story('PBJ-2596 Jaeger should ingest tpat urls')
    @allure.description('Verify the tpat url from event urls')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_tpat_url_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        result = []
        for key, value in tpat.items():
            if key == 'moat':
                continue
            for url in value:
                if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                    result.append(key)
                    break
        assert_that(result, equal_to(['clickUrl', 'checkpoint.0', 'checkpoint.25', 'checkpoint.50', 'checkpoint.75',
                                      'checkpoint.100', 'postroll.view', 'video.close', 'video.unmute', 'video.mute']))

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.157.0')
    @allure.story('PBJ-2596 Jaeger should ingest tpat urls')
    @allure.description('Verify the tpat url details')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    def test_tpat_url_details_1(self, pub_app_id, placement):
        test_ifa = gen_device_id()
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_ifa, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        for url in ad_markup['tpat']['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'adv')[0],
                            equal_to(str_to_json(ad_markup['app_id'].replace('$0$', ''))['app_id']))
                assert_that(parse_url_params(url, 'cid')[0], equal_to(ad_markup['campaign'].split('|')[0]))
                assert_that(parse_url_params(url, 'crid')[0], equal_to(ad_markup['campaign'].split('|')[1]))
                assert_that(parse_url_params(url, 'event_id')[0],
                            equal_to(str_to_json(ad_markup['app_id'].replace('$0$', ''))['eventID']))

                assert_that(parse_url_params(url, 'event_type')[0], equal_to('click'))
                assert_that(parse_url_params(url, 'hb')[0], equal_to('true'))
                assert_that(parse_url_params(url, 'int')[0], equal_to('true'))
                assert_that(parse_url_params(url, 'os')[0], equal_to('iOS'))
                assert_that(parse_url_params(url, 'pid')[0], equal_to('63b51b0d2f288d669880a221'))
                assert_that(parse_url_params(url, 'pub')[0], equal_to(common_test_app_10))
                assert_that(parse_url_params(url, 'test')[0], equal_to('false'))
                assert_that(parse_url_params(url, 'vid')[0], equal_to(test_ifa))
                assert_that(parse_url_params(url, 'vid_type')[0], equal_to('IFA'))

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.157.0', 'test_mode')
    @allure.story('PBJ-2596 Jaeger should ingest tpat urls')
    @allure.description('Verify the tpat url details in test mode with internal Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_tpat_url_details_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        for url in ad_markup['tpat']['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'adv')[0],
                            not equal_to(str_to_json(ad_markup['app_id'].replace('$0$', ''))['app_id']))
                assert_that(parse_url_params(url, 'cid')[0], equal_to(ad_markup['campaign'].split('|')[0]))
                assert_that(parse_url_params(url, 'crid')[0], equal_to(ad_markup['campaign'].split('|')[1]))
                assert_that(parse_url_params(url, 'event_id')[0],
                            equal_to(str_to_json(ad_markup['app_id'].replace('$0$', ''))['eventID']))

                assert_that(parse_url_params(url, 'event_type')[0], equal_to('click'))
                assert_that(parse_url_params(url, 'hb')[0], equal_to('false'))
                assert_that(parse_url_params(url, 'int')[0], equal_to('true'))
                assert_that(parse_url_params(url, 'os')[0], equal_to('iOS'))
                assert_that(parse_url_params(url, 'pid')[0], equal_to('59786bc2a43b3a0862002774'))
                assert_that(parse_url_params(url, 'pub')[0], equal_to(common_test_app))
                assert_that(parse_url_params(url, 'test')[0], equal_to('true'))
                assert_that(parse_url_params(url, 'vid')[0], equal_to(test_mode_device_id))
                assert_that(parse_url_params(url, 'vid_type')[0], equal_to('IFA'))

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.157.0', 'test_mode')
    @allure.story('PBJ-2596 Jaeger should ingest tpat urls')
    @allure.description('Verify the tpat url details in test mode with external Kraken')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_tpat_url_details_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        for url in ad_markup['tpat']['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'cid')[0], equal_to(ad_markup['campaign'].split('|')[0]))
                assert_that(parse_url_params(url, 'crid')[0], equal_to(ad_markup['campaign'].split('|')[1]))
                assert_that(parse_url_params(url, 'event_id')[0],
                            equal_to(str_to_json(ad_markup['app_id'].replace('$0$', ''))['eventID']))

                assert_that(parse_url_params(url, 'event_type')[0], equal_to('click'))
                assert_that(parse_url_params(url, 'hb')[0], equal_to('true'))
                assert_that(parse_url_params(url, 'int')[0], equal_to('false'))
                assert_that(parse_url_params(url, 'os')[0], equal_to('iOS'))
                assert_that(parse_url_params(url, 'pid')[0], equal_to('59786bc2a43b3a0862002774'))
                assert_that(parse_url_params(url, 'pub')[0], equal_to(common_test_app))
                assert_that(parse_url_params(url, 'test')[0], equal_to('true'))
                assert_that(parse_url_params(url, 'vid')[0], equal_to(test_mode_device_id))
                assert_that(parse_url_params(url, 'vid_type')[0], equal_to('IFA'))

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.166.0', 'test_mode')
    @allure.story('PBJ-2856 Jaeger needs to add TPAT events')
    @allure.description('Verify the new tpat events for multi-page vungle mraid in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_new_tpat_events_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_exist(ad_markup['tpat'], 'closeButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'nearCloseButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'download.ctaClick')
        assert_keys_exist(ad_markup['tpat'], 'download.fullScreenClick')
        assert_keys_exist(ad_markup['tpat'], 'muteButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'privacyButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'storeKitOverlay.autoOpen.storeEndcardTimer')

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.166.0')
    @allure.story('PBJ-2856 Jaeger needs to add TPAT events')
    @allure.description('Verify the new tpat events for multi-page vungle mraid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    def test_new_tpat_events_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_exist(ad_markup['tpat'], 'closeButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'nearCloseButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'download.ctaClick')
        assert_keys_exist(ad_markup['tpat'], 'download.fullScreenClick')
        assert_keys_exist(ad_markup['tpat'], 'muteButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'privacyButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'storeKitOverlay.autoOpen.storeEndcardTimer')

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.166.0')
    @allure.story('PBJ-2856 Jaeger needs to add TPAT events')
    @allure.description('Verify the new tpat events for vungle local')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_legacy])
    def test_new_tpat_events_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.9',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_exist(ad_markup['tpat'], 'close_button_click')
        assert_keys_exist(ad_markup['tpat'], 'near_close_button_click')
        assert_keys_exist(ad_markup['tpat'], 'cta_click')
        assert_keys_exist(ad_markup['tpat'], 'fullscreen_click')
        assert_keys_exist(ad_markup['tpat'], 'mute_button_click')
        assert_keys_exist(ad_markup['tpat'], 'privacy_button_click')
        assert_keys_exist(ad_markup['tpat'], 'store_kit_overlay_auto_open')

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.166.0', 'test_mode')
    @allure.story('PBJ-2856 Jaeger needs to add TPAT events')
    @allure.description('Verify the new tpat events for single page vungle mraid in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['AREYOUS82690'])
    def test_new_tpat_events_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_exist(ad_markup['tpat'], 'closeButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'nearCloseButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'download.ctaClick')
        assert_keys_exist(ad_markup['tpat'], 'download.fullScreenClick')
        assert_keys_exist(ad_markup['tpat'], 'muteButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'privacyButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'storeKitOverlay.autoOpen.storeEndcardTimer')

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.166.0')
    @allure.story('PBJ-2856 Jaeger needs to add TPAT events')
    @allure.description('Verify the new tpat events for single page vungle mraid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', ['AREYOUS82690'])
    def test_new_tpat_events_5(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_exist(ad_markup['tpat'], 'closeButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'nearCloseButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'download.ctaClick')
        assert_keys_exist(ad_markup['tpat'], 'download.fullScreenClick')
        assert_keys_exist(ad_markup['tpat'], 'muteButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'privacyButtonClick')
        assert_keys_exist(ad_markup['tpat'], 'storeKitOverlay.autoOpen.storeEndcardTimer')

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.171.0', 'test_mode')
    @allure.story('PBJ-2856 Jaeger needs to add TPAT events')
    @allure.description('Verify the new tpat events for vungle mraid in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, 'AREYOUS82690'])
    def test_new_tpat_events_6(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_exist(ad_markup['tpat'], 'download.ASOIInteraction')
        assert_keys_exist(ad_markup['tpat'], 'download.ASOIComplete')
        assert_keys_exist(ad_markup['tpat'], 'playableEndcardClick')

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3079 Jaeger needs to add Adaptive Creative TPAT events')
    @allure.description('Verify the new tpat events for vungle mraid')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement, 'AREYOUS82690'])
    def test_new_tpat_events_7(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_exist(ad_markup['tpat'], 'download.ASOIInteraction')
        assert_keys_exist(ad_markup['tpat'], 'download.ASOIComplete')
        assert_keys_exist(ad_markup['tpat'], 'playableEndcardClick')

    @allure.feature('tpat support')
    @allure.tag('normal', 'v1.171.0')
    @allure.story('PBJ-3079 Jaeger needs to add Adaptive Creative TPAT events')
    @allure.description('Verify the new tpat events for vungle local')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_legacy])
    def test_new_tpat_events_8(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(sdk_version='Vungle/6.3.9',
                                                                        rtb_selector=meister_rtb_ids))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_exist(ad_markup['tpat'], 'asoi_interaction')
        assert_keys_exist(ad_markup['tpat'], 'asoi_complete')
        assert_keys_exist(ad_markup['tpat'], 'playable_endcard_click')

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.172.0')
    @allure.story('PBJ-3075 Ads response for native ads')
    @allure.description('Verify the tpat tracker can be parsed correctly from the eDSP bid response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_tpat_native_placement_edsp_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that('https://' in tpat['clickUrl'][0])
        assert_that(tpat['download.ctaClick'][0], equal_to(normal_replacements['CTA_BUTTON_URL']))
        assert_that('https://' in tpat['download.ctaClick'][0])
        assert_that('https://' in tpat['checkpoint.0'][0])

    @allure.feature('native placement')
    @allure.tag('normal', 'v1.172.0', 'test_mode')
    @allure.story('PBJ-3075 Ads response for native ads')
    @allure.description('Verify the tpat tracker can be parsed correctly from the eDSP bid response in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_native_placement])
    def test_tpat_native_placement_edsp_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=fr_ip, sdk_version=test_default_real_time_sdk_version,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast, debug='jaeger'))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        normal_replacements = ad_markup['templateSettings']['normal_replacements']

        assert_that('https://' in tpat['clickUrl'][0])
        assert_that(tpat['download.ctaClick'][0], equal_to(normal_replacements['CTA_BUTTON_URL']))
        assert_that('https://' in tpat['download.ctaClick'][0])
        assert_that('https://' in tpat['checkpoint.0'][0])

    @allure.feature('click coordinate')
    @allure.tag('normal', 'v1.173.0', 'test_mode')
    @allure.story('PBJ-3150 Click coordinate reporting in Jaeger')
    @allure.description('Verify the click coordinates field will be returned for non-tencent eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_new_tpat_events_click_coordinates_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_exist(ad_markup['tpat'], 'video.clickCoordinates')

    @allure.feature('click coordinate')
    @allure.tag('normal', 'v1.173.0', 'test_mode')
    @allure.story('PBJ-3150 Click coordinate reporting in Jaeger')
    @allure.description('Verify the click coordinates field will be returned for tencent eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_new_tpat_events_click_coordinates_2(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(rtb_selector=ext_test_mode_kraken_vast_rtb_ids_tencent,
                                              sdk_version=test_default_real_time_sdk_version))

            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            assert_keys_exist(ad_markup['tpat'], 'video.clickCoordinates')

    @allure.feature('click coordinate')
    @allure.tag('normal', 'v1.173.0', 'test_mode')
    @allure.story('PBJ-3150 Click coordinate reporting in Jaeger')
    @allure.description('Verify the macros in event url will be replaced for tencent eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_new_tpat_events_click_coordinates_3(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(rtb_selector=ext_test_mode_kraken_vast_rtb_ids_tencent,
                                              sdk_version=test_default_real_time_sdk_version))

            response_payload = r.json()
            ad_markup = response_payload['ads'][0]['ad_markup']

            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            assert_that('{{{req_width}}}' in ad_markup['tpat']['video.clickCoordinates'][0])
            assert_that('{{{req_height}}}' in ad_markup['tpat']['video.clickCoordinates'][0])
            assert_that('{{{width}}}' in ad_markup['tpat']['video.clickCoordinates'][0])
            assert_that('{{{height}}}' in ad_markup['tpat']['video.clickCoordinates'][0])
            assert_that('{{{down_x}}}' in ad_markup['tpat']['video.clickCoordinates'][0])
            assert_that('{{{down_y}}}' in ad_markup['tpat']['video.clickCoordinates'][0])
            assert_that('{{{up_x}}}' in ad_markup['tpat']['video.clickCoordinates'][0])
            assert_that('{{{up_y}}}' in ad_markup['tpat']['video.clickCoordinates'][0])

    @allure.feature('click coordinate')
    @allure.tag('normal', 'v1.173.0', 'test_mode')
    @allure.story('PBJ-3150 Click coordinate reporting in Jaeger')
    @allure.description('Verify the macros in event url will not be replaced for non-tencent eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_new_tpat_events_click_coordinates_4(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=test_default_real_time_sdk_version))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_that('__REQ_WIDTH__' in ad_markup['tpat']['video.clickCoordinates'][0])
        assert_that('__REQ_HEIGHT__' in ad_markup['tpat']['video.clickCoordinates'][0])
        assert_that('__WIDTH__' in ad_markup['tpat']['video.clickCoordinates'][0])
        assert_that('__HEIGHT__' in ad_markup['tpat']['video.clickCoordinates'][0])
        assert_that('__DOWN_X__' in ad_markup['tpat']['video.clickCoordinates'][0])
        assert_that('__DOWN_Y__' in ad_markup['tpat']['video.clickCoordinates'][0])
        assert_that('__UP_X__' in ad_markup['tpat']['video.clickCoordinates'][0])
        assert_that('__UP_Y__' in ad_markup['tpat']['video.clickCoordinates'][0])

    @allure.feature('notification')
    @allure.tag('normal')
    @allure.story('PBJ-3141 Move win notification from checkpoint.0 from tpat to notification when SDK >= 6.11.0')
    @allure.description('Verify notification display in response when sdk>=6.11.0 for header bidding')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_notification_in_app_bidding(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        # assert_keys_exist(ad_markup, 'notification')
        # assert_that('http://' in ad_markup['notification'][0])

    @allure.feature('notification')
    @allure.tag('normal')
    @allure.story('PBJ-3141 Move win notification from checkpoint.0 from tpat to notification when SDK >= 6.11.0')
    @allure.description('Verify notification display in response when sdk>=6.11.0 for non header bidding')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_10])
    @pytest.mark.parametrize('placement', [common_test_placement_10])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_notification_no_head_bidding(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, rtb_selector=meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'notification')

    @allure.feature('notification')
    @allure.tag('normal')
    @allure.story('PBJ-3141 Move win notification from checkpoint.0 from tpat to notification when SDK < 6.11.0')
    @allure.description('Verify win notification display in checkpoint.0 when sdk < 6.11.0 for header bidding')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_win_notification_in_app_bidding(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'notification')

    @allure.feature('notification')
    @allure.tag('normal')
    @allure.story('PBJ-3141 Move win notification from checkpoint.0 from tpat to notification when SDK < 6.11.0')
    @allure.description('Verify win notification display in checkpoint.0 when sdk < 6.11.0 for non header bidding')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    def test_win_notification_non_head_bidding(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, rtb_selector=win_notification_meister_rtb_ids))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'notification')

    # @allure.feature('notification')
    # @allure.tag('normal')
    # @allure.story('PBJ-3141 Move win notification from checkpoint.0 from tpat to notification when SDK >= 6.11.0')
    # @allure.description('Verify notification display in response when sdk>=6.11.0 for eDSP')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('hb', [True])
    # def test_notification_edsp_1(self, pub_app_id, placement, sdk_v, hb):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v,
    #                                       rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     if 'notification' in ad_markup:
    #         noti

    @allure.feature('notification')
    @allure.tag('normal')
    @allure.story('PBJ-3141 Move win notification from checkpoint.0 from tpat to notification when SDK >= 6.11.0')
    @allure.description('Verify notification display in response when sdk < 6.11.0 for eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('hb', [True, False])
    def test_notification_edsp_2(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'notification')

    # @allure.feature('notification')
    # @allure.tag('normal')
    # @allure.story('PBJ-3141 Move win notification from checkpoint.0 from tpat to notification when SDK >= 6.11.0')
    # @allure.description('Verify notification display in response when sdk>=6.11.0 for test mode eDSP')
    # @pytest.mark.parametrize('pub_app_id', [common_test_app])
    # @pytest.mark.parametrize('placement', [common_test_placement])
    # @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    # @pytest.mark.parametrize('hb', [True, False])
    # def test_notification_test_mode_edsp_1(self, pub_app_id, placement, sdk_v, hb):
    #     req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=hb)
    #     r = post(ads_v5_endpoint_qa, json=req,
    #              headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v,
    #                                       rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
    #     response_payload = r.json()
    #     ad_markup = response_payload['ads'][0]['ad_markup']
    #
    #     assert_response_status_code(r.status_code, HTTPStatus.OK)
    #     assert_valid_schema(r.json(), response_schema.ads_v5)
    #     assert_keys_exist(ad_markup, 'notification')
    #     assert_that("http" in ad_markup['notification'][0])

    @allure.feature('notification')
    @allure.tag('normal')
    @allure.story('PBJ-3141 Move win notification from checkpoint.0 from tpat to notification when SDK >= 6.11.0')
    @allure.description('Verify notification display in response when sdk< 6.11.0 for test mode eDSP')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.10.1'])
    @pytest.mark.parametrize('hb', [False])
    def test_notification_test_mode_edsp_2(self, pub_app_id, placement, sdk_v, hb):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=hb)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, sdk_version=sdk_v,
                                          rtb_selector=ext_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)
        assert_keys_not_exist(ad_markup, 'notification')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0', 'test_mode')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify the burl in tpat.start when bill_notice_origin is sdk via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_burl_1(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids_1))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            tpat_start = ad_markup['tpat']['checkpoint.0']
            assertion_flag = False
            for url in tpat_start:
                if 'kraken' in url and '/win' in url:
                    assertion_flag = True
            assert_that(assertion_flag, 'Kraken burl not found!')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0', 'test_mode')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify the burl in tpat.start when bill_notice_origin is sdk via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_legacy])
    def test_rtb_burl_2(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(sdk_version='Vungle/6.3.9', rtb_selector=test_mode_kraken_rtb_ids_1))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            urls = []
            for item in ad_markup['tpat']['play_percentage']:
                if item['checkpoint'] == 0:
                    urls = item['urls']

            assertion_flag = False
            for url in urls:
                if 'kraken' in url and '/win' in url:
                    assertion_flag = True
            assert_that(assertion_flag, 'Kraken burl not found!')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify the burl in tpat.start when bill_notice_origin is sdk via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_burl_3(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_start = ad_markup['tpat']['checkpoint.0']
        assertion_flag = False
        for url in tpat_start:
            if 'kraken' in url and '/win' in url:
                assertion_flag = True
        assert_that(assertion_flag, 'Kraken burl not found!')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0', 'test_mode')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify the ext parma in the tpat url when bill_notice_origin is exchange via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_burl_4(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            tpat_start = ad_markup['tpat']['checkpoint.0']
            kraken_burl_flag = True
            tpat_ext_flag = False

            for url in tpat_start:
                if 'kraken' in url and '/win' in url:
                    kraken_burl_flag = False
                if '/api/v5/tpat' in url and 'ext=' in url:
                    tpat_ext_flag = True

            assert_that(kraken_burl_flag, 'Kraken burl found!')
            assert_that(tpat_ext_flag, 'The param of ext not found!')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0', 'test_mode')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify the ext parma in the tpat url when bill_notice_origin is exchange via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_legacy])
    def test_rtb_burl_5(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(sdk_version='Vungle/6.3.9', rtb_selector=test_mode_kraken_rtb_ids))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            urls = []
            for item in ad_markup['tpat']['play_percentage']:
                if item['checkpoint'] == 0:
                    urls = item['urls']

            kraken_burl_flag = True
            tpat_ext_flag = False

            for url in urls:
                if 'kraken' in url and '/win' in url:
                    kraken_burl_flag = False
                if '/api/v5/tpat' in url and 'ext=' in url:
                    tpat_ext_flag = True

            assert_that(kraken_burl_flag, 'Kraken burl found!')
            assert_that(tpat_ext_flag, 'The param of ext not found!')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify the ext parma in the tpat url when bill_notice_origin is exchange via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_burl_6(self, pub_app_id, placement):
        if env == 'qa' or env == 'regression':
            req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
            r = post(ads_v5_endpoint_qa, json=req,
                     headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_1))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_valid_schema(r.json(), response_schema.ads_v5)

            ad_markup = response_payload['ads'][0]['ad_markup']
            tpat_start = ad_markup['tpat']['checkpoint.0']
            kraken_win_url_flag = False
            tpat_ext_flag = False

            for url in tpat_start:
                if 'kraken' in url and '/win' in url:
                    kraken_win_url_flag = True
                if '/api/v5/tpat' in url and 'ext=' in url:
                    tpat_ext_flag = True

            assert_that(kraken_win_url_flag, 'Kraken win url not found!')
            assert_that(tpat_ext_flag, 'The param of ext not found!')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0', 'test_mode')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify the behavior is as before in tpat.start when bill_notice_origin is disabled via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_burl_7(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids_2))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_start = ad_markup['tpat']['checkpoint.0']
        kraken_burl_flag = True
        tpat_ext_flag = True

        for url in tpat_start:
            if 'kraken' in url and '/win' in url:
                kraken_burl_flag = False
            if '/api/v5/tpat' in url and 'ext=' in url:
                tpat_ext_flag = False

        assert_that(kraken_burl_flag, 'Kraken burl found!')
        assert_that(tpat_ext_flag, 'The param of ext found!')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0', 'test_mode')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify the behavior is as before in tpat.start when bill_notice_origin is disabled via iDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_legacy])
    def test_rtb_burl_8(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version='Vungle/6.3.9', rtb_selector=test_mode_kraken_rtb_ids_2))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        urls = []
        for item in ad_markup['tpat']['play_percentage']:
            if item['checkpoint'] == 0:
                urls = item['urls']

        kraken_burl_flag = True
        tpat_ext_flag = True

        for url in urls:
            if 'kraken' in url and '/win' in url:
                kraken_burl_flag = False
            if '/api/v5/tpat' in url and 'ext=' in url:
                tpat_ext_flag = False

        assert_that(kraken_burl_flag, 'Kraken burl found!')
        assert_that(tpat_ext_flag, 'The param of ext found!')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0', 'test_mode')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify the behavior is as before in tpat.start when bill_notice_origin is null via eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_rtb_burl_9(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_start = ad_markup['tpat']['checkpoint.0']
        kraken_win_url_flag = False
        tpat_ext_flag = True

        for url in tpat_start:
            if 'kraken' in url and '/win' in url:
                kraken_win_url_flag = True
            if '/api/v5/tpat' in url and 'ext=' in url:
                tpat_ext_flag = False

        assert_that(kraken_win_url_flag, 'Kraken win url not found!')
        assert_that(tpat_ext_flag, 'The param of ext found!')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0', 'test_mode')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify that Jaeger will not serve when bill_notice_origin is other string')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement_legacy])
    def test_rtb_burl_10(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req, headers=platform_headers(rtb_selector=test_mode_kraken_rtb_ids_3))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        assert_keys_exist(ad_markup, 'sleep')

    @allure.feature('rtb burl support')
    @allure.tag('normal', 'v1.178.0')
    @allure.story('PBJ-3223 RTB :: Support Billing Notice URL (burl)')
    @allure.description('Verify the behavior is as before in tpat.start when bill_notice_origin is not setup')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_banner_placement])
    def test_rtb_burl_11(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), banner=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_mraid))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_start = ad_markup['tpat']['checkpoint.0']
        kraken_win_url_flag = False
        tpat_ext_flag = True

        for url in tpat_start:
            if 'kraken' in url and '/win' in url:
                kraken_win_url_flag = True
            if '/api/v5/tpat' in url and 'ext=' in url:
                tpat_ext_flag = False

        assert_that(kraken_win_url_flag, 'Kraken win url not found!')
        assert_that(tpat_ext_flag, 'The param of ext found!')

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0')
    @allure.story('PBJ-3304 RTB :: Faulty Clicks and No Ad')
    @allure.description('Verify click tracking can handle the enter and tab symbol for VAST adm')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_click_tracking_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']

        assert_that(tpat['postroll.click'][0].find("\n"), equal_to(-1))
        assert_that(tpat['postroll.click'][0].find("\t"), equal_to(-1))

    @allure.feature('rtb support')
    @allure.tag('normal', 'v1.180.0', 'test_mode')
    @allure.story('PBJ-3304 RTB :: Faulty Clicks and No Ad')
    @allure.description('Verify click tracking can handle the enter and tab symbol for VAST adm in test mode')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_click_tracking_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast))

        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']

        assert_that(tpat['postroll.click'][0].find("\n"), equal_to(-1))
        assert_that(tpat['postroll.click'][0].find("\t"), equal_to(-1))

    @allure.feature('tapt ext')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when sdkv>=6.10.1 and hb=True')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_tapt_ext_01_idsp(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when sdkv>=6.10.1 and hb=True')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_tapt_ext_01_edsp(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=jp_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when sdkv>=6.10.1 and hb=True')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_tapt_ext_01_test_mode_edsp(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=jp_ip,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when sdkv>=6.10.1 and hb=True')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_tapt_ext_01_kraken(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=jp_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when hb=false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0', 'Vungle/6.10.0', 'Vungle/6.11.0'])
    def test_tapt_ext_02_idsp(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when hb=false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0', 'Vungle/6.10.0', 'Vungle/6.11.0'])
    def test_tapt_ext_02_edsp(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when hb=false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0', 'Vungle/6.10.0', 'Vungle/6.11.0'])
    def test_tapt_ext_02_test_mode_edsp(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when hb=false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0', 'Vungle/6.10.0', 'Vungle/6.11.0'])
    def test_tapt_ext_02_kraken(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=false from tapt for when hb=true and sdkv<6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.9.0'])
    def test_tapt_ext_03_idsp(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('false'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=false from tapt for when hb=true and sdkv<6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.9.0'])
    def test_tapt_ext_03_edsp(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id(), header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('false'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=false from tapt for when hb=true and sdkv<6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.9.0'])
    def test_tapt_ext_03_test_mode_edsp(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('false'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=false from tapt for when hb=true and sdkv<6.10.1')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.9.0'])
    def test_tapt_ext_03_kraken(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('false'))

    @allure.feature('tapt ext')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when sdkv>=6.10.1 and hb=True for android platform')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_tapt_ext_01_android(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when hb=false for android platform')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0', 'Vungle/6.10.0', 'Vungle/6.11.0'])
    def test_tapt_ext_02_android(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=ext1_non_test_mode_kraken_rtb_ids_vast, debug='jaeger'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=false from tapt when hb=true and sdkv<6.10.1 for android platform')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [android_common_test_app])
    @pytest.mark.parametrize('placement', [android_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.9.0'])
    def test_tapt_ext_03_android(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_android(pub_app_id, placement, android_id=test_mode_device_id,
                                                header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=ext1_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('false'))

    @allure.feature('tapt ext')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when sdkv>=6.10.1 and hb=True for amazon platform')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['VungleDroid/6.10.1', 'VungleDroid/6.11.0', 'VungleDroid/6.11.1'])
    def test_tapt_ext_01_amazon(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_amazon(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext  for amazon platform')
    @allure.description('Verify there is ic=true from tapt when hb=false')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0', 'Vungle/6.10.0', 'Vungle/6.11.0'])
    def test_tapt_ext_02_amazon(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_amazon(pub_app_id, placement, ifa=test_mode_device_id, header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=false from tapt when hb=true and sdkv<6.10.1 for amazon platform')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [amazon_common_test_app])
    @pytest.mark.parametrize('placement', [amazon_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.9.0'])
    def test_tapt_ext_03_amazon(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_amazon(pub_app_id, placement, ifa=test_mode_device_id,
                                               header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('false'))

    @allure.feature('tapt ext')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when sdkv>=6.10.1 and hb=True for windows platform')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_tapt_ext_01_windows(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ashwid=test_mode_device_id, header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=true from tapt when hb=false for windows platform')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.9.0', 'Vungle/6.10.0', 'Vungle/6.11.0'])
    def test_tapt_ext_02_windows(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ashwid=gen_device_id(), header_bidding=False)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip,
                                          rtb_selector=non_test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('true'))

    @allure.feature('tapt ext')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-3398 [Jaeger] Add whether need read bid info in tpat ext')
    @allure.description('Verify there is ic=false from tapt when hb=true and sdkv<6.10.1 for windows platform')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [windows_common_test_app])
    @pytest.mark.parametrize('placement', [windows_common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0', 'Vungle/6.9.0'])
    def test_tapt_ext_03_windows(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_windows(pub_app_id, placement, ashwid=test_mode_device_id,
                                                header_bidding=True)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(sdk_version=sdk_v, src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['clickUrl']:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                assert_that(parse_url_params(url, 'ic')[0], equal_to('false'))

    @allure.feature('click coordinate')
    @allure.tag('normal', 'v1.191.0')
    @allure.story('PBJ-3606 ClickCoordinate URLs should be only showed on SDK 6.11 or above')
    @allure.description('Verify the click coordinates field will be showed when SDK >= 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0', 'Vungle/6.11.1'])
    def test_new_tpat_events_click_coordinates_version_ctl_1(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_exist(ad_markup['tpat'], 'video.clickCoordinates')

    @allure.feature('click coordinate')
    @allure.tag('normal', 'v1.191.0')
    @allure.story('PBJ-3606 ClickCoordinate URLs should be only showed on SDK 6.11 or above')
    @allure.description('Verify the click coordinates field will not be showed when SDK < 6.11.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.9'])
    def test_new_tpat_events_click_coordinates_version_ctl_2(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(rtb_selector=ext_test_mode_kraken_rtb_ids_vast, sdk_version=sdk_v))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        assert_keys_not_exist(ad_markup['tpat'], 'video.clickCoordinates')

    @allure.feature('tapt')
    @allure.tag('normal')
    @allure.story('PBJ-3904 AD cannot play on iOS SDK when URL contains special characters')
    @allure.description('Verify the special chars will be removed from the tpat url for Aarki eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_tpat_url_special_chars_1(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast_aarki))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['checkpoint.0']:
            if 'https://is.snssdk.com' in url:
                assert_that('{timezone}' not in url)

    @allure.feature('tapt')
    @allure.tag('normal')
    @allure.story('PBJ-3904 AD cannot play on iOS SDK when URL contains special characters')
    @allure.description('Verify this change will not impact the other eDSP')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_tpat_url_special_chars_2(self, pub_app_id, placement):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['checkpoint.0']:
            if 'https://is.snssdk.com' in url:
                assert_that('{timezone}' in url)


    @allure.feature('tapt')
    @allure.tag('normal', 'v1.260.0')
    @allure.story('PBJ-5200 [Jaeger]Fix unsafe characters in URL in TPAT')
    @allure.description('Verify the characters can be encode in jaeger response')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    def test_tpat_url_special_chars_3(self, pub_app_id, placement):
        """
        " ":"",
        "<":"%3C",
        ">":"%3E",
        "{":"%7B",
        "}":"%7D",
        "$":"%24",
        """
        over_ride_burl = 'seatbid.0.bid.0.burl@"http://emily-ext.apiqa.svc.cluster.local:7700/$< > {burl}&?aid=kraken-test-aid&impid=kraken-test-impid&price=98.0"'
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          debug='jaeger', override_bid_response_any=over_ride_burl,sdk_version='Vungle/7.0.0'))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_checkpoint0 = ad_markup['tpat']['checkpoint.0']
        nurl = [x for i, x in enumerate(tpat_checkpoint0) if x.find('emily') != -1][0]
        assert_that("%24%3C%3E%7Bburl%7D" in nurl)


    @allure.feature('tapt')
    @allure.tag('normal')
    @allure.story('PBJ-4788 SDK 7.0 - Append a new parameter {{{remote_play}}} in tpat.0 url'
                  'PBJ-5040 SDK 7.0 - Support parameter {{{remote_play}}} in tpat.0 url')
    @allure.description('Verify new paramter is added to checkpoint.0 for non test mode edsp for sdk>=7.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0', 'Vungle/7.0.1'])
    def test_sdk_7_0_tpat_url_e(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['checkpoint.0']:
            if '/api/v7/tpat' in url:
                tpat_scrat_url = url
        assert_that('remote_play=%7B%7B%7Bremote_play%7D%7D%7D' in tpat_scrat_url)

    @allure.feature('tapt')
    @allure.tag('normal')
    @allure.story('PBJ-4788 SDK 7.0 - Append a new parameter {{{remote_play}}} in tpat.0 url')
    @allure.description('Verify new paramter is added to checkpoint.0 for non test mode idsp for sdk>=7.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0', 'Vungle/7.0.1'])
    def test_sdk_7_0_tpat_url_i(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=non_test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['checkpoint.0']:
            if '/api/v7/tpat' in url:
                tpat_scrat_url = url
        assert_that('remote_play=%7B%7B%7Bremote_play%7D%7D%7D' in tpat_scrat_url)

    @allure.feature('tapt')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4788 SDK 7.0 - Append a new parameter {{{remote_play}}} in tpat.0 url')
    @allure.description('Verify new paramter is added to checkpoint.0 for test mode edsp for sdk>=7.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0', 'Vungle/7.0.1'])
    def test_sdk_7_0_tpat_url_e_test_mode(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['checkpoint.0']:
            if '/api/v7/tpat' in url:
                tpat_scrat_url = url
        assert_that('remote_play=%7B%7B%7Bremote_play%7D%7D%7D' in tpat_scrat_url)

    @allure.feature('tapt')
    @allure.tag('normal', 'test_mode')
    @allure.story('PBJ-4788 SDK 7.0 - Append a new parameter {{{remote_play}}} in tpat.0 url')
    @allure.description('Verify new paramter is added to checkpoint.0 for test mode idsp for sdk>=7.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0', 'Vungle/7.0.1'])
    def test_sdk_7_0_tpat_url_i_test_mode(self, pub_app_id, placement, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=test_mode_kraken_rtb_ids,
                                          sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['checkpoint.0']:
            if '/api/v7/tpat' in url:
                tpat_scrat_url = url
        assert_that('remote_play=%7B%7B%7Bremote_play%7D%7D%7D' in tpat_scrat_url)

    @allure.feature('tapt')
    @allure.tag('normal')
    @allure.story('PBJ-4788 SDK 7.0 - Append a new parameter {{{remote_play}}} in tpat.0 url'
                  'PBJ-5040 SDK 7.0 - Support parameter {{{remote_play}}} in tpat.0 url')
    @allure.description('Verify no paramter remote_play added to checkpoint.0 for sdk<7.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6', 'Vungle/6.11.1', 'Vungle/6.12.1','Vungle/7.0.0-early1'])
    @pytest.mark.parametrize('rtb_ids', [non_test_mode_kraken_rtb_ids, ext_non_test_mode_kraken_rtb_ids_vast])
    def test_sdk_7_0_tpat_url_not_affect(self, pub_app_id, placement, sdk_v, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        for url in tpat['checkpoint.0']:
            if '/tpat' in url:
                tpat_scrat_url = url
        assert_that('remote_play=%7B%7B%7Bremote_play%7D%7D%7D' not in tpat_scrat_url)


    @allure.feature('tapt')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4879 Jaeger - add pass deeplink signal into tpat event')
    @allure.description('Verify new tpat event is added to tpat for sdk>=7.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_ids', [non_test_mode_kraken_rtb_ids, ext_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0', 'Vungle/7.0.1'])
    def test_sdk_7_0_tpat_url_non_test_mode(self, pub_app_id, placement, sdk_v, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        assert_keys_exist(tpat, 'deeplink.click')
        deeplink = url_decoder(tpat['deeplink.click'][0])
        assert_that("/api/v7/tpat" in deeplink)
        assert_that("event_type=deeplinkClick" in deeplink)
        assert_that("dl_suc={{{is_success}}}" in deeplink)


    @allure.feature('tapt')
    @allure.tag('normal', 'test_mode', 'v1.245.0')
    @allure.story('PBJ-4879 Jaeger - add pass deeplink signal into tpat event')
    @allure.description('Verify new tpat event is added to tpat for sdk>=7.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_ids', [test_mode_kraken_rtb_ids, ext_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0', 'Vungle/7.0.1'])
    def test_sdk_7_0_tpat_url_test_mode(self, pub_app_id, placement, sdk_v, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        assert_keys_exist(tpat, 'deeplink.click')
        deeplink = url_decoder(tpat['deeplink.click'][0])
        assert_that("/api/v7/tpat" in deeplink)
        assert_that("event_type=deeplinkClick" in deeplink)
        assert_that("dl_suc={{{is_success}}}" in deeplink)


    @allure.feature('tapt')
    @allure.tag('normal', 'v1.245.0')
    @allure.story('PBJ-4879 Jaeger - add pass deeplink signal into tpat event')
    @allure.description('Verify no deeplink.click event in tpat for sdk<7.0')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('rtb_ids', [non_test_mode_kraken_rtb_ids, ext_non_test_mode_kraken_rtb_ids_vast])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.6', 'Vungle/6.11.1', 'Vungle/6.12.1'])
    def test_sdk_7_0_tpat_not_affect(self, pub_app_id, placement, sdk_v, rtb_ids):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=rtb_ids,
                                          sdk_version=sdk_v))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_valid_schema(r.json(), response_schema.ads_v5)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        assert_keys_not_exist(tpat, 'deeplink.click')
