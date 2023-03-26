import pytest
import allure

from http import HTTPStatus

from data import request_payload
from utils.behaviors import request_hbp_no_notification, request_hbp
from utils.common import *
from utils.assertions import *
from settings import *
import time


@allure.epic('scrat - tpat')
class TestTpatRequest(object):

    @allure.feature('sdk tpat')
    @allure.tag('normal', 'v0.114.0')
    @allure.story('PBJ-3091 MAX has the same logic to send Vungle bill notification')
    @allure.description('Verify the tpat start event will not send bill notification when SDK >= 6.10.1')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.1', 'Vungle/6.10.2'])
    def test_tpat_start_event_1(self, pub_app_id, sdk_v):
        test_ifa = gen_device_id()
        response = request_hbp('max', 11, pub_app_id=pub_app_id, test_device_id=test_ifa, sdk_v='Vungle/6.10.0')
        time.sleep(0.1)

        if response['is_hbp_responded_200']:
            for url in response['ads_response']['ads'][0]['ad_markup']['tpat']['checkpoint.0']:
                if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                    tpat_start_url = url
            if 'adv' in tpat_start_url:
                adv = parse_url_params(tpat_start_url, 'adv')
            else:
                adv = None
            req = request_payload.tpat(adv=adv,
                                       cid=parse_url_params(tpat_start_url, 'cid'),
                                       crid=parse_url_params(tpat_start_url, 'crid'),
                                       event_id=parse_url_params(tpat_start_url, 'event_id'),
                                       event_type=parse_url_params(tpat_start_url, 'event_type'),
                                       hb=parse_url_params(tpat_start_url, 'hb'),
                                       int=parse_url_params(tpat_start_url, 'int'),
                                       os=parse_url_params(tpat_start_url, 'os'),
                                       pid=parse_url_params(tpat_start_url, 'pid'),
                                       pub=parse_url_params(tpat_start_url, 'pub'),
                                       test=parse_url_params(tpat_start_url, 'test'),
                                       vid=parse_url_params(tpat_start_url, 'vid'),
                                       vid_type=parse_url_params(tpat_start_url, 'vid_type'))
            r = get(tpat_endpoint_qa, params=req, headers=platform_headers(sdk_version=sdk_v))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(response_payload['msg'], equal_to('ok'))
            assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk tpat')
    @allure.tag('normal', 'v0.114.0')
    @allure.story('PBJ-3091 MAX has the same logic to send Vungle bill notification')
    @allure.description('Verify the tpat start event will send bill notification when SDK < 6.10.1')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_tpat_start_event_2(self, pub_app_id, sdk_v):
        test_ifa = gen_device_id()
        response = request_hbp('max', 11, pub_app_id=pub_app_id, test_device_id=test_ifa, sdk_v='Vungle/6.10.0')
        time.sleep(0.1)

        if response['is_hbp_responded_200']:
            for url in response['ads_response']['ads'][0]['ad_markup']['tpat']['checkpoint.0']:
                if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                    tpat_start_url = url
            if 'adv' in tpat_start_url:
                adv = parse_url_params(tpat_start_url, 'adv')
            else:
                adv = None
            req = request_payload.tpat(adv=adv,
                                       cid=parse_url_params(tpat_start_url, 'cid'),
                                       crid=parse_url_params(tpat_start_url, 'crid'),
                                       event_id=parse_url_params(tpat_start_url, 'event_id'),
                                       event_type=parse_url_params(tpat_start_url, 'event_type'),
                                       hb=parse_url_params(tpat_start_url, 'hb'),
                                       int=parse_url_params(tpat_start_url, 'int'),
                                       os=parse_url_params(tpat_start_url, 'os'),
                                       pid=parse_url_params(tpat_start_url, 'pid'),
                                       pub=parse_url_params(tpat_start_url, 'pub'),
                                       test=parse_url_params(tpat_start_url, 'test'),
                                       vid=parse_url_params(tpat_start_url, 'vid'),
                                       vid_type=parse_url_params(tpat_start_url, 'vid_type'))
            r = get(tpat_endpoint_qa, params=req, headers=platform_headers(sdk_version=sdk_v))

            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(response_payload['msg'], equal_to('ok'))
            assert_that(response_payload['code'], equal_to(200))
            # To check 'PBJ-4386'
            # Verify that `bflat_datasci_tags` added in hb-notification

    @allure.feature('sdk tpat')
    @allure.tag('normal', 'v0.114.0')
    @allure.story('PBJ-3397 [Scrat] Fix tpat > 6.10.1 still try to read bidinfo in cache')
    @allure.description('Verify tpat with ic=false should record bidinfo when is headerbiding and event=start')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.10.0'])
    def test_tpat_start_event_3(self, pub_app_id, sdk_v):
        test_ifa = gen_device_id()
        response = request_hbp('max', 11, pub_app_id=pub_app_id, test_device_id=test_ifa, sdk_v='Vungle/6.10.0')
        time.sleep(0.1)

        if response['is_hbp_responded_200']:
            for url in response['ads_response']['ads'][0]['ad_markup']['tpat']['checkpoint.0']:
                if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                    tpat_start_url = url
            r = get(tpat_start_url.replace('https://events.ads.vungle.com', scrat_all_host),
                    headers=platform_headers(sdk_version=sdk_v))
            response_payload = r.json()
            assert_response_status_code(r.status_code, HTTPStatus.OK)
            assert_that(response_payload['msg'], equal_to('ok'))
            assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk 7.0')
    @allure.tag('normal')
    @allure.story('PBJ-4801 SDK 7.0 - Scrat parse the new parameter {{{remote_play}}} in tpat.0 url')
    @allure.description('Verify Scrat parse the new parameter {{{remote_play}}} in tpat.0 url')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    def test_tpat_new_paramter(self, pub_app_id, placement_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast, sdk_version=sdk_v))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']['checkpoint.0']
        for url in tpat:
            if tpat_endpoint_v7_qa in url:
                tpat_start_url = url.replace('remote_play={{{remote_play}}}', 'remote_play=false')

                r = get(tpat_start_url, headers=platform_headers(sdk_version=sdk_v))
                response_payload = r.json()
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_that(response_payload['msg'], equal_to('ok'))
                assert_that(response_payload['code'], equal_to(200))

    @allure.feature('tpat')
    @allure.tag('normal', 'legacy')
    @allure.story('PBJ-4862 No TPAT click for Windows& Amazon on Legacy')
    @allure.description('Verify invlove postroll_click will record to kafka')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('os_ver', ['10'])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/5.0.9'])
    def test_invlove_tpat_for_vungle_local_01(self, pub_app_id, placement, os_ver, sdk_ver):
        if env == 'ci':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[0]
        elif env == 'qa' or env == 'regression':
            rtb = ext_test_mode_kraken_rtb_ids_vast.split(',')[1]
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, os_version=os_ver, ifa=test_mode_device_id)
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', rtb_selector=rtb, sdk_version=sdk_ver))

        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        tpat_play_percentage = tpat['play_percentage'][0]
        assert_that(tpat_play_percentage['checkpoint'] in [0, 1, 0.75])
        postroll_click_url = tpat['postroll_click'][0]
        r = get(postroll_click_url.replace('https://events.ads.vungle.com', scrat_all_host),
                headers=platform_headers(sdk_version=sdk_ver))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('tpat')
    @allure.tag('normal', 'legacy')
    @allure.story('PBJ-4862 No TPAT click for Windows& Amazon on Legacy')
    @allure.description('Verify invlove checkpoint.75 will record to kafka')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('os_ver', ['10'])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/5.0.9'])
    def test_invlove_tpat_for_vungle_local_02(self, pub_app_id, placement, os_ver, sdk_ver):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_liftoff_01, sdk_version=sdk_ver))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_urls = ad_markup['tpat']['play_percentage'][2]['urls']
        for url in tpat_urls:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                tpat_url = url
                break
            else:
                continue
        r = get(tpat_url.replace('https://events.ads.vungle.com', scrat_all_host),
                headers=platform_headers(sdk_version=sdk_ver))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('tpat')
    @allure.tag('normal', 'legacy')
    @allure.story('PBJ-4862 No TPAT click for Windows& Amazon on Legacy')
    @allure.description('Verify invlove checkpoint.100 will record to kafka')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('os_ver', ['10'])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/5.0.9'])
    def test_invlove_tpat_for_vungle_local_03(self, pub_app_id, placement, os_ver, sdk_ver):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_liftoff_01, sdk_version=sdk_ver))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat_urls = ad_markup['tpat']['play_percentage'][0]['urls']
        for url in tpat_urls:
            if 'https://events.ads.vungle.com/api/v5/tpat' in url:
                tpat_url = url
                break
            else:
                continue
        r = get(tpat_url.replace('https://events.ads.vungle.com', scrat_all_host),
                headers=platform_headers(sdk_version=sdk_ver))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('tpat')
    @allure.tag('normal' ,'v1.245.0')
    @allure.story('PBJ-4879 Jaeger - add pass deeplink signal into tpat event')
    @allure.description('Verify invlove deeplink.click will record to kafka')
    @allure.severity('normal')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement', [common_test_placement])
    @pytest.mark.parametrize('sdk_ver', ['Vungle/7.0.0'])
    def test_invlove_tpat_for_deeplink(self, pub_app_id, placement, sdk_ver):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(src_ip=au_ip, rtb_selector=ext_non_test_mode_kraken_rtb_ids_vast,
                                          sdk_version=sdk_ver))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)

        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']
        assert_keys_exist(tpat, 'deeplink.click')
        deeplink = url_decoder(tpat['deeplink.click'][0])
        r = get(deeplink.replace('https://events.ads.vungle.com', scrat_all_host).replace("{{{is_success}}}", "true"),
                headers=platform_headers(sdk_version=sdk_ver))
        response_payload = r.json()
        assert_response_status_code(r.status_code, HTTPStatus.OK)
        assert_that(response_payload['msg'], equal_to('ok'))
        assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk 7.0')
    @allure.tag('normal', 'v0.161.0', 'v0.165.0')
    @allure.story('PBJ-4827 Scrat - Make sure as-views still works for SDK7.0'
                  'PBJ-4917 Scrat - Fix app id in as views message by tpat start'
                  'PBJ-5091 Fix as view message for SDK7.0')
    @allure.description('Verify scrat produce as-views message through tpat start event when sdk>=7.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/7.0.0'])
    def test_tpat_start_event_produce_message_to_as_views(self, pub_app_id, placement_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_liftoff_01, sdk_version=sdk_v))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']['checkpoint.0']
        for url in tpat:
            if tpat_endpoint_v7_qa in url:
                tpat_start_url = url.replace('remote_play={{{remote_play}}}', 'remote_play=false')

                r = get(tpat_start_url, headers=platform_headers(sdk_version=sdk_v))
                response_payload = r.json()
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_that(response_payload['msg'], equal_to('ok'))
                assert_that(response_payload['code'], equal_to(200))

    @allure.feature('sdk 7.0')
    @allure.tag('normal','v0.161.0', 'v0.165.0')
    @allure.story('PBJ-4827 Scrat - Make sure as-views still works for SDK7.0'
                  'PBJ-4917 Scrat - Fix app id in as views message by tpat start')
    @allure.description('Verify scrat does not produce as-views message through tpat start event when sdk<7.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app])
    @pytest.mark.parametrize('placement_id', [common_test_placement])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.11.0'])
    def test_tpat_start_event_not_produce_message(self, pub_app_id, placement_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_liftoff_01, sdk_version=sdk_v))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']['checkpoint.0']
        for url in tpat:
            if tpat_endpoint_qa in url:
                tpat_start_url = url.replace('remote_play={{{remote_play}}}', 'remote_play=false')

                r = get(tpat_start_url, headers=platform_headers(sdk_version=sdk_v))
                response_payload = r.json()
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_that(response_payload['msg'], equal_to('ok'))
                assert_that(response_payload['code'], equal_to(200))
                # Verify that no message recored in as-views.

    @allure.feature('sdk 7.0')
    @allure.tag('normal','v0.161.0', 'v0.165.0')
    @allure.story('PBJ-4827 Scrat - Make sure as-views still works for SDK7.0'
                  'PBJ-4917 Scrat - Fix app id in as views message by tpat start')
    @allure.description('Verify scrat produce as-views message through tpat start event when sdk<7.0')
    @allure.severity('smoke')
    @pytest.mark.parametrize('pub_app_id', [common_test_app_no_coppa])
    @pytest.mark.parametrize('placement_id', ['DEFAULT-5045327'])
    @pytest.mark.parametrize('sdk_v', ['Vungle/6.12.0'])
    def test_tpat_start_event_produce_message_disable_reportAd(self, pub_app_id, placement_id, sdk_v):
        req = request_payload.jaeger_v5_ios(pub_app_id, placement_id, ifa=gen_device_id())
        r = post(ads_v5_endpoint_qa, json=req,
                 headers=platform_headers(debug='jaeger', src_ip=au_ip,
                                          rtb_selector=ext_non_test_mode_liftoff_01, sdk_version=sdk_v))

        assert_response_status_code(r.status_code, HTTPStatus.OK)
        response_payload = r.json()
        ad_markup = response_payload['ads'][0]['ad_markup']
        tpat = ad_markup['tpat']['checkpoint.0']
        for url in tpat:
            if tpat_endpoint_v7_qa in url:
                tpat_start_url = url.replace('remote_play={{{remote_play}}}', 'remote_play=false')

                r = get(tpat_start_url, headers=platform_headers(sdk_version=sdk_v))
                response_payload = r.json()
                assert_response_status_code(r.status_code, HTTPStatus.OK)
                assert_that(response_payload['msg'], equal_to('ok'))
                assert_that(response_payload['code'], equal_to(200))
                # Verify that message recored in as-views.
